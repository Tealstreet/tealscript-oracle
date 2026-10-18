import csv
import json
import runpy
import struct
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put,epoch=HELPERS['ref'],HELPERS['put'],HELPERS['epoch']


def build(source_id):
    directory=BASE/source_id
    inspection_path=directory/'visual-inspection-v1.json'
    inspection=json.loads(inspection_path.read_text())
    attempt=directory/'attempt-v1';session_dir=attempt/'session-mode0-v1'
    observation=json.loads((attempt/'observation-v1.json').read_text())
    session=json.loads((session_dir/'row-set-observation-v1.json').read_text())
    receipt=json.loads((session_dir/'session-receipt-v1.json').read_text())
    png=ROOT/session['renderPng']['path'];data=png.read_bytes()
    assert data[:8]==b'\x89PNG\r\n\x1a\n'
    width,height=struct.unpack('>II',data[16:24])
    original=ref(png)
    assert original['sha256']==inspection['inspectedOriginalPngSha256']
    rows=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=rows[0]
    def point(n,title):
        c=headers.index(title)
        return dict(csvSha256=session['csv']['sha256'],rowOrdinal=n,columnOrdinal=c+1,headerRaw=title,valueRaw=rows[n][c])
    anchor=session['uniqueVisualAnchorRowOrdinal']
    anchor_points={t:point(anchor,t) for t in ['time','INPUT_TIME','INPUT_INDEX','CASE_ID','CHART_CONFIRMED','VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX']} if anchor else None
    calibration=inspection.get('axisCalibration')
    projected=None
    if calibration and anchor_points:
        ticks=[]
        for tick in calibration['xTicks']:
            matches=[n for n,row in enumerate(rows[1:],1) if row[0]==str(tick['unixSeconds'])]
            assert len(matches)==1
            n=matches[0];ticks.append(dict(**tick,originalTime=point(n,'time'),originalOwnIndex=point(n,'INPUT_INDEX')))
        a,b=ticks[:2]
        scale=(b['xPx']-a['xPx'])/(int(b['originalOwnIndex']['valueRaw'])-int(a['originalOwnIndex']['valueRaw']))
        def x(n):return a['xPx']+scale*(int(rows[n][headers.index('INPUT_INDEX')])-int(a['originalOwnIndex']['valueRaw']))
        primary=session['selectedPrimaryClosedRowOrdinals']
        projected=dict(xTicks=ticks,pixelsPerOwnIndex=scale,anchorXPx=x(anchor),primaryXPx=[dict(rowOrdinal=n,xPx=x(n),visible=calibration['studyPlotBoundsPx'][0]<=x(n)<=calibration['studyPlotBoundsPx'][2]) for n in primary],yTicks=calibration['yTicks'],coordinateUncertaintyPx=calibration['coordinateUncertaintyPx'],basis='DERIVED from visible native axis labels and their exact original CSV source-index/time rows. Actual source-index differences calibrate x; no forced120-second gap filling, hidden geometry, CSS/DPI/font metric or universal raster claim.')
    screenshot_start,screenshot_end=receipt.get('screenshotAtUtc'),receipt.get('screenshotCompletedAtUtc')
    windows=[session['nativeExportUtc'],screenshot_start,screenshot_end]
    same_clock_bar=all(windows) and len({int(epoch(t)//120) for t in windows})==1
    return dict(version='v1',role='DERIVED REGION MAP / manual inspection of the one original native PNG',sourceId=source_id,sourceSha256=observation['sourceSha256'],nativePrivateId=observation['privateScriptId'],nativePrivateVersion=observation['privateVersion'],sourceObservation=ref(attempt/'observation-v1.json'),originalPng=original,originalDimensionsPx=dict(width=width,height=height),originalCsv=session['csv'],sessionReceipt=session['sessionReceipt'],renderContext=ref(session_dir/'render-context-v1.txt'),manualInspection=ref(inspection_path),visualAnchor=anchor_points,anchorCertificate='OWNED / unique closed source marker' if anchor_points else 'UNDECIDED / unique source-owned marker unavailable',screenshotUtcWindow=dict(start=screenshot_start,end=screenshot_end),exportAndPngClockBarUnchanged=same_clock_bar,nativeFrameId=None,nativeFrameIdStatus='UNOBSERVED; UTC windows and source marker bind this finite plate, not an invented provider tick frame or cross-session continuity',derivedCalibration=projected,facets=inspection['facets'],exposedAppearanceMetadata=inspection.get('exposedAppearanceMetadata',dict(theme='Dark chart UI observed in original PNG',zoom=None,dpi=None,resolvedFont=None)),preservedUnobserved=['Unexposed zoom/DPI/resolved-font metrics and native frame ID','Every absent, clipped, already occluded, nonintersecting or precision-ambiguous region','All historical v93 appearance/context holds and universal raster/color/identity contracts'],scope='One unchanged source/session/viewport only. Original PNG bytes are unchanged. Regions and uncertainty are DERIVED; numeric getters/intent never replace an absent pixel witness, and PNG pixels never supply missing getter values.')


if __name__=='__main__':
    source_id=sys.argv[1];result=build(source_id)
    put(BASE/source_id/'derived-region-map-v1.json',result)
    print(json.dumps(dict(sourceId=source_id,originalPng=result['originalPng'],anchor=result['visualAnchor']['INPUT_INDEX']['valueRaw'] if result['visualAnchor'] else None,facets=len(result['facets']))))
