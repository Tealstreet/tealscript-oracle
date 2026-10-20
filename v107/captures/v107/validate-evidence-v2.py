import json
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PREVIOUS=runpy.run_path(str(BASE/'validate-evidence-v1.py'))
read,bound,clock=PREVIOUS['read'],PREVIOUS['bound'],PREVIOUS['clock']


def validate(revision=1,integrity=True,preservation=None):
    result=PREVIOUS['validate'](revision,integrity=integrity,preservation=preservation)
    manifest=read(ROOT/'v107/bundle-manifest-v1.json');assets={a['sourceId']:a for a in manifest['entries']}
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');viewport=read(BASE/'environment-v1/viewport-preregistration-v1.json')
    assert viewport['sourceSlotsConsumed']==0 and viewport['newLayoutId']==208603104 and viewport['pageId']==19
    policy=manifest['viewportPrerequisite']
    assert viewport['viewportContract']==policy and policy['wholePrimaryPlus8PredecessorsVisible'] is False
    assert policy['primaryOrPredecessorBarVisibilityRequired'] is False
    for key in ['pixelsPerBar','studyPaneHeightPx','paneSize']:assert policy[key]==dict(recordActual=True,gated=False,requiredRange=None)
    approval=read(BASE/'environment-v2/owner-reconnect-authorization-v1.json');assert approval['standingApproval'] is True and approval['reconnectActions']==1
    assert len(assets)==len({a['slotId'] for a in assets.values()})==4
    assert viewport['uncertaintyBeforeScoring']==dict(axisXPx=2,axisYPx=3,strokeEdgePx=1)
    for attempt in inventory['attempts']:
        source=attempt['source'];asset=assets[source['sourceId']];directory=BASE/source['sourceId'];start=read(directory/'attempt-v1/attempt-start-v1.json')
        assert source['slotId']==asset['slotId'] and start['sourceSha256']==asset['sha256']
        assert clock(viewport['registeredBeforeSourceAttemptsAtUtc'])<clock(start['startedAtUtc'])
        if source['saveBody']:
            saved=json.loads(bound(source['saveBody']));meta=(saved.get('result') or {}).get('metaInfo',{})
            if saved['success']:assert meta['description']==asset['indicatorTitle'] or meta.get('shortDescription')==asset['indicatorTitle']
        for session in attempt['sessions']:
            receipt=read(ROOT/session['sessionReceipt']['path']);assert receipt['viewportActions']==[] and receipt['inputMode']==0
            visual_path=directory/'derived-region-map-v1.json'
            if not visual_path.exists():continue
            visual=read(visual_path);inspection=read(directory/'visual-inspection-v1.json');certificate=read(directory/'table-certificate-v2.json')
            assert runpy.run_path(str(BASE/'build-table-certificate-v2.py'))['build'](source['sourceId'])==certificate
            assert certificate['originalPng']==session['renderPng']==visual['originalPng'] and certificate['originalCsv']==session['csv']
            assert certificate['privateScriptId']==source['privateScriptId'] and certificate['slotId']==asset['slotId']
            frozen=asset['visualFacets'][0]['predeclaredWindows'];assert certificate['frozenPredeclaredWindows']==frozen
            assert certificate['outcome']==visual['facets'][0]['outcome'] or visual['facets'][0]['outcome']=='UNDECIDED'
            if certificate['notObservedCauses']:assert certificate['outcome']=='UNDECIDED'
            pane=certificate['paneInteriorBoundsPx'];assert pane==visual['registration']['paneInteriorBoundsPx']
            assert visual['registration']['historicalBarVisibilityRequired'] is False
            assert visual['registration']['barSpacingGated'] is False and visual['registration']['paneSizeGated'] is False
            def map_region(bounds,uv):
                x,y,right,bottom=bounds;u,z,v,w=uv
                return [x+(right-x)*u,y+(bottom-y)*v,x+(right-x)*z,y+(bottom-y)*w]
            assert certificate['derivedEnvelopesPx']=={name:map_region(pane,region) for name,region in frozen['envelopes'].items()}
            for item in certificate['namedWindows']:
                name=item['objectIdentity'];label=item['regionIdentity'];obj=inspection['tableObjects'].get(name)
                if label=='envelope':expected=map_region(pane,frozen['envelopes'][name])
                else:
                    bounds=obj['exteriorPx'];kind,_,key=label.partition('/')
                    spec=frozen['body'] if kind=='body' and not key else frozen['bodies'][key] if kind=='body' else (frozen['completeText'][key] if isinstance(frozen['completeText'],dict) else frozen['completeText']) if kind=='text' else frozen['frame'][key] if kind=='frame' else frozen['divider'][int(key)-1] if kind=='divider' else frozen['completeText']
                    expected=map_region(bounds,spec)
                assert item['derivedWindowPx']==expected
                if certificate['outcome']!='UNDECIDED':assert not item['occludingObjects']
            if certificate['outcome']!='UNDECIDED':
                assert not certificate['notObservedCauses']
                assert all(obj['registrationReadable'] for obj in inspection['tableObjects'].values() if obj.get('exteriorPx'))
                assert inspection['facets'][0]['outcome']==certificate['outcome']
            result['counts']['tableWindowCertificates']=result['counts'].get('tableWindowCertificates',0)+1
    assert result['counts']['uniquePrimaryPlotCells']<=1184
    result['counts']['ownerAuthorizedReconnectActions']=1
    result['policy']+='; v107 right-side source identities, fixed per-table envelopes/body/text/frame/divider mappings, original scan tuples and all declared overlay intersections'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
