import csv
import json
import runpy
import struct
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
HELPERS = runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref, put, number, epoch = HELPERS['ref'], HELPERS['put'], HELPERS['number'], HELPERS['epoch']


def intersection(a, b):
    return [max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])]


def build(source_id):
    asset = next(a for a in json.loads((ROOT/'v104/bundle-manifest-v1.json').read_text())['entries'] if a['sourceId']==source_id)
    directory=BASE/source_id
    inspection_path=directory/'visual-inspection-v1.json'
    inspection=json.loads(inspection_path.read_text())
    session_dir=directory/'attempt-v1/session-mode0-v1'
    session=json.loads((session_dir/'row-set-observation-v1.json').read_text())
    observation=json.loads((directory/'attempt-v1/observation-v1.json').read_text())
    receipt=json.loads((session_dir/'session-receipt-v1.json').read_text())
    png=ROOT/session['renderPng']['path'];raw_png=png.read_bytes()
    assert raw_png[:8]==b'\x89PNG\r\n\x1a\n'
    width,height=struct.unpack('>II',raw_png[16:24]);png_ref=ref(png)
    assert png_ref['sha256']==inspection['inspectedOriginalPngSha256']
    rows=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=rows[0]
    def point(n,title):
        c=headers.index(title)
        return dict(csvSha256=session['csv']['sha256'],rowOrdinal=n,columnOrdinal=c+1,headerRaw=title,valueRaw=rows[n][c])
    anchor=session['uniqueVisualAnchorRowOrdinal']
    calibration=inspection.get('axisCalibration')
    registration=None;held=[]
    if anchor is None or not session['primaryInputCertificateValid']:
        held.append('Unique closed retained anchor and complete owned32+8 row certificate unavailable')
    if calibration and anchor:
        ticks=[]
        for tick in calibration['xTicks']:
            matches=[n for n,r in enumerate(rows[1:],1) if r[0]==str(tick['unixSeconds'])]
            assert len(matches)==1
            n=matches[0];ticks.append(dict(**tick,time=point(n,'time'),ownIndex=point(n,'INPUT_INDEX')))
        a,b=ticks[:2];spacing=(b['xPx']-a['xPx'])/float(number(b['ownIndex']['valueRaw'])-number(a['ownIndex']['valueRaw']))
        anchor_index=number(rows[anchor][headers.index('INPUT_INDEX')]);xa=a['xPx']+spacing*float(anchor_index-number(a['ownIndex']['valueRaw']))
        pane=calibration['paneInteriorBoundsPx'];w=pane[2]-pane[0];h=pane[3]-pane[1]
        primary_x=[xa-31*spacing,xa]
        predecessor_x=[xa-39*spacing,xa]
        if not (pane[0]<=predecessor_x[0]<=predecessor_x[1]<=pane[2]):held.append('Full own A-39..A primary-plus-predecessor viewport is outside original pane')
        if not (pane[0]<=primary_x[0]<=primary_x[1]<=pane[2]):held.append('Full fixed primary X(A-31)..X(A) interval is outside original pane')
        if asset['visualPane']!='main':
            margin=(pane[2]-xa)/spacing
            if not (240<=h<=600 and 16<=spacing<=24):held.append('Natural indicator viewport lies outside frozen feasibility envelope; no viewport repair')
        else:margin=None
        registration=dict(xTicks=ticks,anchorXPx=xa,pixelsPerOwnBar=spacing,paneInteriorBoundsPx=pane,primaryWindowXPx=primary_x,primaryPlusPredecessorsWindowXPx=predecessor_x,paneWidthPx=w,paneHeightPx=h,rightMarginBars=margin,uncertaintyPx=dict(x=2,y=3,strokeEdge=1),uncertaintySource=ref(BASE/'numeric-contracts-v1.json'))
    else:
        held.append('Exposed native axis calibration unavailable')
    manual={f['facetId']:f for f in inspection['facets']}
    assert set(manual)=={f['facetId'] for f in asset['visualFacets']}
    facets=[]
    for frozen in asset['visualFacets']:
        finding=manual[frozen['facetId']];spec=frozen['pixelWindow'];window=None
        if registration:
            xa=registration['anchorXPx'];spacing=registration['pixelsPerOwnBar'];pane=registration['paneInteriorBoundsPx'];w=registration['paneWidthPx'];h=registration['paneHeightPx'];pad=spec['paddingPx']
            if spec['coordinates']=='pane-fraction-top-down':
                window=[pane[0]+w*spec['x'][0]-pad,pane[1]+h*spec['y'][0]-pad,pane[0]+w*spec['x'][1]+pad,pane[1]+h*spec['y'][1]+pad]
            elif spec['coordinates']=='anchor-bars/value':
                y0=calibration['yZeroPx'];y100=calibration['yHundredPx']
                y=lambda v:y0-v*(y0-y100)/100
                window=[xa+spec['x'][0]*spacing-pad,y(spec['y'][1])-pad,xa+spec['x'][1]*spacing+pad,y(spec['y'][0])+pad]
            else:
                assert spec['coordinates']=='anchor-bars/ohlc-margin'
                ticks=calibration['priceTicks'];one,two=ticks[:2];slope=(two['yPx']-one['yPx'])/(two['value']-one['value']);y=lambda v:one['yPx']+(v-one['value'])*slope
                primary=session['selectedPrimaryClosedRowOrdinals'];high=max(float(rows[n][headers.index('high')]) for n in primary);low=min(float(rows[n][headers.index('low')]) for n in primary)
                window=[xa+spec['x'][0]*spacing-pad,min(y(high),y(low))-spec['y'][1]-pad,xa+spec['x'][1]*spacing+pad,max(y(high),y(low))-spec['y'][0]+pad]
            if 'intersectPaneFractions' in spec:
                f=spec['intersectPaneFractions'];clip=[pane[0]+f['x'][0]*w,pane[1]+f['y'][0]*h,pane[0]+f['x'][1]*w,pane[1]+f['y'][1]*h];window=intersection(window,clip)
        requested_window=list(window) if window else None
        outcome=finding['outcome'];assert outcome in ['SUPPORTED_A','SUPPORTED_B','CONTRARY','UNDECIDED']
        causes=list(held)
        if window:
            pad=spec['paddingPx'];required=window if spec['coordinates']=='anchor-bars/ohlc-margin' else [window[0]+pad,window[1]+pad,window[2]-pad,window[3]-pad]
            if required[0]<0 or required[1]<0 or required[2]>width or required[3]>height:causes.append('Required preregistered subject window clips original screenshot bounds')
            window=intersection(window,[0,0,width,height])
        if finding.get('notObservedCause'):causes.append(finding['notObservedCause'])
        if causes:outcome='UNDECIDED'
        verdict='SUPPORTED' if outcome=='SUPPORTED_A' else 'REFUTED' if outcome in ['SUPPORTED_B','CONTRARY'] else 'UNDECIDED'
        facets.append(dict(facetId=frozen['facetId'],frozenModels=dict(A=frozen['modelA'],B=frozen['modelB']),frozenPixelWindow=spec,derivedWindowPx=window,derivedRequestedWindowPx=requested_window,paddingScope='Fixed padding clipped only to original image extent; missing required subject or overlay OHLC-margin windows stay held',outcome=outcome,verdict=verdict,modelAVerdict='SUPPORTED' if outcome=='SUPPORTED_A' else 'REFUTED' if outcome in ['SUPPORTED_B','CONTRARY'] else 'UNDECIDED',modelBVerdict='SUPPORTED' if outcome=='SUPPORTED_B' else 'REFUTED' if outcome in ['SUPPORTED_A','CONTRARY'] else 'UNDECIDED',manualFinding=finding,notObservedCauses=causes,scope='This registered window and actually readable unoccluded controls only; no transferred version/API, universal raster/font or intent-to-pixel claim'))
    result=dict(version='v1',role='DERIVED REGION MAP / original native PNG, fixed preregistered windows',sourceId=source_id,sourceSha256=asset['sha256'],nativePrivateId=observation['privateScriptId'],nativePrivateVersion=observation['privateVersion'],sourceObservation=ref(directory/'attempt-v1/observation-v1.json'),originalPng=png_ref,originalDimensionsPx=dict(width=width,height=height),originalCsv=session['csv'],sessionReceipt=session['sessionReceipt'],manualInspection=ref(inspection_path),registration=registration,retainedAnchor={t:point(anchor,t) for t in ['time','INPUT_INDEX','INPUT_TIME','CASE_ID','CHART_CONFIRMED','VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX']} if anchor else None,screenshotUtcWindow=dict(start=receipt['screenshotAtUtc'],end=receipt['screenshotCompletedAtUtc']),nativeFrameId=None,nativeFrameIdStatus='UNOBSERVED; retained source guard, source/session/CSV and clocks do not invent a provider frame',facets=facets,exposedAppearanceMetadata=inspection.get('exposedAppearanceMetadata',dict(theme='Dark native chart UI observed',zoom=None,dpi=None,resolvedFont=None)),scope='Original bytes unchanged. Lifetime guard retains the one-time object plate. Context and numeric state never supply missing pixels; absent/overlapping/unreadable controls stay held.')
    pixel_path=directory/'pixel-certificate-v1.json'
    if pixel_path.exists():
        pixel=json.loads(pixel_path.read_text());assert pixel['originalPng']==png_ref and pixel['originalCsv']==session['csv']
        result['pixelCertificate']=ref(pixel_path)
        if asset['sourceId']=='v104-alpha-composite-v6':assert result['facets'][0]['outcome']==pixel['alphaFiniteDecision']['outcome']
    return result


if __name__=='__main__':
    result=build(sys.argv[1]);put(BASE/sys.argv[1]/'derived-region-map-v1.json',result)
    print(json.dumps(dict(sourceId=sys.argv[1],facets={f['facetId']:f['verdict'] for f in result['facets']})))
