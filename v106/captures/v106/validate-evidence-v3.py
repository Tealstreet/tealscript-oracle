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
    manifest=read(ROOT/'v106/bundle-manifest-v1.json');assets={a['sourceId']:a for a in manifest['entries']}
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');viewport=read(BASE/'environment-v1/viewport-preregistration-v1.json')
    assert viewport['sourceSlotsConsumed']==0 and viewport['newLayoutId']==208556660 and viewport['pageId']==18
    assert len(assets)==len({a['slotId'] for a in assets.values()})==4
    assert viewport['uncertaintyBeforeScoring']==dict(axisXPx=2,axisYPx=3,strokeEdgePx=1,stepCombinedXPx=3)
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
            visual=read(visual_path);inspection=read(directory/'visual-inspection-v1.json');certificate=read(directory/'table-certificate-v1.json')
            assert runpy.run_path(str(BASE/'build-table-certificate-v1.py'))['build'](source['sourceId'])==certificate
            assert certificate['originalPng']==session['renderPng']==visual['originalPng'] and certificate['originalCsv']==session['csv']
            assert certificate['privateScriptId']==source['privateScriptId'] and certificate['slotId']==asset['slotId']
            frozen=asset['visualFacets'][0]['predeclaredWindows'];assert certificate['frozenPredeclaredWindows']==frozen
            assert certificate['outcome']==visual['facets'][0]['outcome'] or visual['facets'][0]['outcome']=='UNDECIDED'
            if certificate['notObservedCauses']:assert certificate['outcome']=='UNDECIDED'
            pane=certificate['paneInteriorBoundsPx'];assert pane==visual['registration']['paneInteriorBoundsPx']
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
    geometry=read(BASE/'v106-table-survival-v5/geometry-registration-v1.json')
    visual=read(BASE/'v106-table-survival-v5/derived-region-map-v1.json')
    registration=visual['registration'];assert geometry['originalPngSha256']==visual['originalPng']['sha256']
    assert geometry['paneInteriorBoundsPx']==registration['paneInteriorBoundsPx']
    first=registration['primaryPlusPredecessorsWindowXPx'][0]
    assert abs(first-geometry['primaryPlusPredecessorFirstCenterXPx'])<1e-9
    left,right=geometry['xTicks'];bar_count=30
    assert (right['unixSeconds']-left['unixSeconds'])/120==bar_count
    spacing=(right['xPx']-left['xPx'])/bar_count
    assert abs(spacing-registration['pixelsPerOwnBar'])<1e-9
    upper=left['xPx']+2-4*((right['xPx']-left['xPx']-4)/bar_count)+1
    assert upper==geometry['primaryPlusPredecessorFirstCenterUpperBoundPx']<geometry['paneInteriorBoundsPx'][0]
    assert visual['facets'][0]['outcome']=='UNDECIDED'
    entry_attempts=1
    for attempt in inventory['attempts'][1:]:
        source=attempt['source'];stop=json.loads(bound(source['sourceEntryStop']))
        assert source['saveBody'] is None and source['addBody'] is None and source['privateScriptId'] is None
        assert source['nativeEntryAttempted']==stop['nativeEntryAttempted']
        entry_attempts+=int(stop['nativeEntryAttempted'])
    assert entry_attempts==2
    result['counts'].update(actualNativeSourceEntryAttempts=2,completeNativeSourceEntries=1,partialNativeSourceEntries=1,noEntryPrerequisiteHolds=2)
    assert result['counts']['uniquePrimaryPlotCells']<=1184
    result['policy']+='; v106 right-side source identities, fixed per-table envelopes/body/text/frame/divider mappings, original scan tuples and all declared overlay intersections'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
