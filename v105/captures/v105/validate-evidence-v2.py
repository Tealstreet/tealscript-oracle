import hashlib
import json
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PREVIOUS=runpy.run_path(str(BASE/'validate-evidence-v1.py'))
read,bound,clock=PREVIOUS['read'],PREVIOUS['bound'],PREVIOUS['clock']


def validate(revision=1,integrity=True,preservation=None):
    result=PREVIOUS['validate'](revision,integrity=integrity,preservation=preservation)
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');manifest=read(ROOT/'v105/bundle-manifest-v1.json');assets={a['sourceId']:a for a in manifest['entries']};viewport=read(BASE/'environment-v1/viewport-preregistration-v1.json')
    assert viewport['sourceSlotsConsumed']==0 and viewport['newLayoutId']==208474398 and viewport['pageId']==17
    assert viewport['uncertaintyBeforeScoring']==dict(axisXPx=2,axisYPx=3,strokeEdgePx=1,stepCombinedXPx=3)
    assert len(assets)==5 and len({a['slotId'] for a in assets.values()})==5
    for attempt in inventory['attempts']:
        source=attempt['source'];asset=assets[source['sourceId']];directory=BASE/source['sourceId'];start=read(directory/'attempt-v1/attempt-start-v1.json')
        assert source['slotId']==asset['slotId'] and start['sourceSha256']==asset['sha256'] and clock(viewport['registeredBeforeSourceAttemptsAtUtc'])<clock(start['startedAtUtc'])
        if source['saveBody']:
            saved=json.loads(bound(source['saveBody']));meta=(saved.get('result') or {}).get('metaInfo',{})
            if saved['success']:assert meta['description']==asset['indicatorTitle'] or meta.get('shortDescription')==asset['indicatorTitle']
        for session in attempt['sessions']:
            receipt=read(ROOT/session['sessionReceipt']['path']);assert receipt['viewportActions']==[] and receipt['inputMode']==0
            inspection_path=directory/'visual-inspection-v1.json';visual_path=directory/'derived-region-map-v1.json'
            if not visual_path.exists():continue
            visual=read(visual_path);inspection=read(inspection_path);assert visual['originalPng']==session['renderPng']
            if source['sourceId']=='v105-alpha-composite-v6':
                path=directory/'alpha-certificate-v1.json';certificate=read(path)
                assert runpy.run_path(str(BASE/'build-alpha-certificate-v1.py'))['build'](write=False)==certificate
                selection=read(directory/'profile-selection-v1.json');prereg=read(BASE/'environment-v1/profile-pipeline-preregistration-v1.json')
                recomputed=runpy.run_path(str(BASE/'select-profile-pipeline-v1.py'))['select']();recomputed.pop('selectedAtUtc');recorded=dict(selection);recorded.pop('selectedAtUtc');assert recorded==recomputed
                assert clock(prereg['registeredAtUtc'])<clock(start['startedAtUtc'])<clock(selection['selectedAtUtc'])<=clock(inspection['inspectedAtUtc'])
                assert certificate['originalPng']==session['renderPng'] and certificate['originalCsv']==session['csv'] and certificate['privateScriptId']==source['privateScriptId']
                expected_specs=[p for group in ['subjects','controls','lineControls'] for p in asset['sampling'][group]]+[asset['sampling']['background']]
                assert [p['frozenSpecification'] for p in certificate['patches']]==expected_specs
                assert len(certificate['patches'])==31 and len({p['patchId'] for p in certificate['patches']})==31
                raw_bytes=bytearray();comparison_bytes=bytearray()
                for patch in certificate['patches']:
                    x,y=patch['centerPx'];assert {(p['xPx'],p['yPx']) for p in patch['samples']}=={(xx,yy) for yy in range(y-2,y+3) for xx in range(x-2,x+3)}
                    for sample in patch['samples']:
                        raw_bytes.extend(sample['rawSample'][:3])
                        if sample['comparisonRgb8'] is not None:comparison_bytes.extend(sample['comparisonRgb8'])
                    if patch['edgeClearancePass']:assert patch['minimumSampleEdgeClearancePx']>=5
                assert bound(certificate['originalRgbSamples'])==bytes(raw_bytes)
                if selection['selectedPipeline']=='EMBEDDED_ICC_TO_FIXED_SRGB_RELATIVE_NO_BPC':
                    conversion=json.loads(bound(certificate['conversionReceipt']));assert conversion['blackPointCompensation'] is False and conversion['intent']=='relative-colorimetric' and conversion['channels']==3 and conversion['syntheticAlpha'] is False
                    assert conversion['inputProfile']==next(c['decodedIcc'] for c in selection['originalColorChunks'] if c['type']=='iCCP') and conversion['outputProfile']==selection['targetProfile']
                    for key in ['inputProfile','outputProfile','inputSamples','outputSamples','tool']:bound(conversion[key])
                    with tempfile.TemporaryDirectory() as tmp:
                        destination=Path(tmp)/'independent-srgb-rgb8-v1.bin';command=list(conversion['command']);command[-1]=str(destination)
                        actual=subprocess.run(command,capture_output=True,text=True);assert actual.returncode==0,actual.stderr
                        assert destination.read_bytes()==bound(certificate['convertedRgbSamples'])==bytes(comparison_bytes)
                controls={p['patchId']:p for p in certificate['patches']}
                exact={name:all(s['comparisonRgb8']==target for s in controls[name]['samples']) and controls[name]['flat'] and controls[name]['edgeClearancePass'] and controls[name]['occlusion']=='NONE' for name,target in {'RED':[255,0,0],'BLUE':[0,0,255],'PURPLE':[128,0,128]}.items()}
                assert certificate['opaqueGatePassed']==(selection['selectedPipeline'] is not None and all(exact.values()))
                assert len(certificate['facets'])==4
                if not certificate['opaqueGatePassed']:assert all(f['outcome']=='UNDECIDED' and not any(s['scoringEligible'] for s in f['subjects']) for f in certificate['facets'])
                for f,v in zip(certificate['facets'],visual['facets']):assert f['facetId']==v['facetId'] and (f['outcome']==v['outcome'] or v['outcome']=='UNDECIDED')
                result['counts']['originalFixedPixelSamples']=31*25;result['counts']['alphaProfileCertificates']=1
            else:
                path=directory/'table-certificate-v1.json';certificate=read(path)
                assert runpy.run_path(str(BASE/'build-table-certificate-v1.py'))['build'](source['sourceId'])==certificate
                assert certificate['originalPng']==session['renderPng'] and certificate['originalCsv']==session['csv'] and certificate['privateScriptId']==source['privateScriptId'] and certificate['slotId']==asset['slotId']
                assert certificate['frozenPredeclaredWindows']==asset['visualFacets'][0]['predeclaredWindows']
                assert certificate['outcome']==visual['facets'][0]['outcome'] or visual['facets'][0]['outcome']=='UNDECIDED'
                if certificate['notObservedCauses']:assert certificate['outcome']=='UNDECIDED'
                result['counts']['tableWindowCertificates']=result['counts'].get('tableWindowCertificates',0)+1
    assert result['counts']['uniquePrimaryPlotCells']<=1632
    result['policy']+='; distinct v105 slot/original title identities; metadata-only fixed RGB ICC pipeline, every exact opaque sample, derived/raw tuples, candidate classes and per-object frozen table windows'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
