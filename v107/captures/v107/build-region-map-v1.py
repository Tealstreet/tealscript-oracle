import csv
import json
import runpy
import struct
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']


def build(source_id):
    asset=next(a for a in json.loads((ROOT/'v107/bundle-manifest-v1.json').read_text())['entries'] if a['sourceId']==source_id)
    directory=BASE/source_id;inspection_path=directory/'visual-inspection-v1.json';inspection=json.loads(inspection_path.read_text())
    session_dir=directory/'attempt-v1/session-mode0-v1';session=json.loads((session_dir/'row-set-observation-v1.json').read_text())
    observation=json.loads((directory/'attempt-v1/observation-v1.json').read_text());receipt=json.loads((session_dir/'session-receipt-v1.json').read_text())
    png=ROOT/session['renderPng']['path'];raw=png.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',raw[16:24]);png_ref=ref(png)
    assert png_ref['sha256']==inspection['inspectedOriginalPngSha256']
    calibration=inspection.get('axisCalibration') or {};pane=calibration.get('paneInteriorBoundsPx');registration=None;causes=[]
    if not session['primaryInputCertificateValid']:causes.append('Unique source-owned physically closed CSV anchor/32+8 certificate unavailable')
    if pane:
        x0,y0,x1,y1=pane
        assert 0<=x0<x1<=width and 0<=y0<y1<=height
        registration=dict(paneInteriorBoundsPx=pane,paneWidthPx=x1-x0,paneHeightPx=y1-y0,uncertaintyPx=dict(x=2,y=3,strokeEdge=1),uncertaintySource=ref(BASE/'numeric-contracts-v1.json'),recordOnlyHorizontalCalibration=calibration.get('xTicks'),recordOnlyBarSpacingPx=calibration.get('pixelsPerBar'),historicalBarVisibilityRequired=False,barSpacingGated=False,paneSizeGated=False)
    else:causes.append('Actual study plotting-area bounds unavailable for named table-window registration')
    rows=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=rows[0];anchor=session['uniqueVisualAnchorRowOrdinal']
    def point(title):
        c=headers.index(title);return dict(csvSha256=session['csv']['sha256'],rowOrdinal=anchor,columnOrdinal=c+1,headerRaw=title,valueRaw=rows[anchor][c])
    findings={f['facetId']:f for f in inspection['facets']};assert set(findings)=={f['facetId'] for f in asset['visualFacets']};facets=[]
    for frozen in asset['visualFacets']:
        finding=findings[frozen['facetId']];spec=frozen['pixelWindow'];assert spec['coordinates']=='pane-fraction-top-down';window=None;requested=None;held=list(causes)
        if pane:
            x0,y0,x1,y1=pane;w=x1-x0;h=y1-y0;pad=spec['paddingPx']
            body=[x0+w*spec['x'][0],y0+h*spec['y'][0],x0+w*spec['x'][1],y0+h*spec['y'][1]]
            requested=[body[0]-pad,body[1]-pad,body[2]+pad,body[3]+pad];window=[max(0,requested[0]),max(0,requested[1]),min(width,requested[2]),min(height,requested[3])]
        if finding.get('notObservedCause'):held.append(finding['notObservedCause'])
        outcome='UNDECIDED' if held else finding['outcome'];assert outcome in ['SUPPORTED_A','SUPPORTED_B','CONTRARY','UNDECIDED']
        verdict='SUPPORTED' if outcome=='SUPPORTED_A' else 'REFUTED' if outcome in ['SUPPORTED_B','CONTRARY'] else 'UNDECIDED'
        facets.append(dict(facetId=frozen['facetId'],frozenModels=dict(A=frozen['modelA'],B=frozen['modelB']),frozenPixelWindow=spec,derivedWindowPx=window,derivedRequestedWindowPx=requested,outcome=outcome,verdict=verdict,modelAVerdict='SUPPORTED' if outcome=='SUPPORTED_A' else 'REFUTED' if outcome in ['SUPPORTED_B','CONTRARY'] else 'UNDECIDED',modelBVerdict='SUPPORTED' if outcome=='SUPPORTED_B' else 'REFUTED' if outcome in ['SUPPORTED_A','CONTRARY'] else 'UNDECIDED',manualFinding=finding,notObservedCauses=held,scope='Fresh exact table source/version/private/session and individually unoccluded screen-anchored windows only; CSV owns numeric anchor independently of any PNG bar position'))
    return dict(version='v1',role='DERIVED SCREEN-ANCHORED TABLE REGION MAP',sourceId=source_id,sourceSha256=asset['sha256'],nativePrivateId=observation['privateScriptId'],nativePrivateVersion=observation['privateVersion'],sourceObservation=ref(directory/'attempt-v1/observation-v1.json'),originalPng=png_ref,originalDimensionsPx=dict(width=width,height=height),originalCsv=session['csv'],sessionReceipt=session['sessionReceipt'],manualInspection=ref(inspection_path),registration=registration,retainedAnchor={t:point(t) for t in ['time','INPUT_INDEX','INPUT_TIME','CASE_ID','CHART_CONFIRMED','VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX']} if anchor else None,screenshotUtcWindow=dict(start=receipt['screenshotAtUtc'],end=receipt['screenshotCompletedAtUtc']),nativeFrameId=None,nativeFrameIdStatus='UNOBSERVED; screenshot clocks are not provider frame identities',facets=facets,exposedAppearanceMetadata=inspection.get('exposedAppearanceMetadata'),scope='Original bytes unchanged. Pane/bar measurements recorded without pass ranges. No historical-bar visibility gate; complete table/control/absence windows remain mandatory. Counts and source intent cannot supply pixels.')


if __name__=='__main__':
    result=build(sys.argv[1]);put(BASE/sys.argv[1]/'derived-region-map-v1.json',result)
    print(json.dumps(dict(sourceId=sys.argv[1],facets={f['facetId']:f['outcome'] for f in result['facets']})))
