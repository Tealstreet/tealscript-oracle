import csv
import json
import math
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put,number=HELPERS['ref'],HELPERS['put'],HELPERS['number']
PNG=runpy.run_path(str(BASE/'read-png-pixels-v1.py'))


def build(source_id):
    directory=BASE/source_id;session_dir=directory/'attempt-v1/session-mode0-v1'
    inspection_path=directory/'visual-inspection-v1.json';inspection=json.loads(inspection_path.read_text())
    spec_path=directory/'pixel-inspection-v1.json';spec=json.loads(spec_path.read_text())
    session=json.loads((session_dir/'row-set-observation-v1.json').read_text())
    observation=json.loads((directory/'attempt-v1/observation-v1.json').read_text())
    original=ROOT/session['renderPng']['path'];png=PNG['decode'](original);pixel=png.pop('pixel')
    rows=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=rows[0]
    calibration=inspection['axisCalibration'];ticks=[]
    for tick in calibration['xTicks']:
        found=[n for n,r in enumerate(rows[1:],1) if r[0]==str(tick['unixSeconds'])];assert len(found)==1
        ticks.append((tick['xPx'],number(rows[found[0]][headers.index('INPUT_INDEX')])))
    spacing=(ticks[1][0]-ticks[0][0])/float(ticks[1][1]-ticks[0][1]);anchor=session['uniqueVisualAnchorRowOrdinal']
    own=number(rows[anchor][headers.index('INPUT_INDEX')]);xa=ticks[0][0]+spacing*float(own-ticks[0][1])
    result=dict(version='v1',sourceId=source_id,sourceSha256=observation['sourceSha256'],privateScriptId=observation['privateScriptId'],privateVersion=observation['privateVersion'],originalPng=ref(original),originalCsv=session['csv'],sessionReceipt=session['sessionReceipt'],rowSet=ref(session_dir/'row-set-observation-v1.json'),inspection=ref(inspection_path),samplingSpecification=ref(spec_path),pngMetadata=png,registration=dict(anchorXPx=xa,pixelsPerOwnBar=spacing,axisXPxUncertainty=2,axisYPxUncertainty=3,strokeEdgePxUncertainty=1),patches=[],rowProfiles=[],columnProfiles=[],scope='Exact original PNG sample coordinates; source/model intent never supplies missing pixels. No color transform or image modification.')
    if source_id=='v104-alpha-composite-v6':
        y0,y100=calibration['yZeroPx'],calibration['yHundredPx'];yp=lambda value:y0-value*(y0-y100)/100
        names=['upper-composite','upper-purple','upper-blue','lower-composite','lower-purple','lower-red']
        centers=[(-26.5,72.5),(-16.5,72.5),(-6.5,72.5),(-26.5,27.5),(-16.5,27.5),(-6.5,27.5)]
        for name,(dx,value) in zip(names,centers):
            x,y=math.floor(xa+dx*spacing+0.5),math.floor(yp(value)+0.5)
            left,right=([-30,-23] if dx==-26.5 else [-20,-13] if dx==-16.5 else [-10,-3]);bottom,top=([55,90] if value==72.5 else [10,45])
            bounds=[xa+left*spacing,yp(top),xa+right*spacing,yp(bottom)]
            clearance=min(x-2-bounds[0],y-2-bounds[1],bounds[2]-(x+2),bounds[3]-(y+2))
            samples=[dict(xPx=xx,yPx=yy,sample=pixel(xx,yy)) for yy in range(y-2,y+3) for xx in range(x-2,x+3)]
            unique=sorted({tuple(p['sample']) for p in samples})
            result['patches'].append(dict(name=name,frozenAnchorOffsetBars=dx,frozenValue=value,rounding='Nearest original pixel; .5 toward positive infinity',centerPx=[x,y],sourcePlateBoundsPx=bounds,minimumEdgeClearancePx=clearance,atLeastFivePixelsFromEdges=clearance>=5,samples=samples,flat=len(unique)==1,uniqueSamples=[list(v) for v in unique]))
        patches={p['name']:p for p in result['patches']}
        controls={'upper-purple':[128,0,128],'lower-purple':[128,0,128],'upper-blue':[0,0,255],'lower-red':[255,0,0]}
        controls_exact=all(patches[name]['uniqueSamples']==[value] for name,value in controls.items())
        frozen=next(f for f in json.loads((ROOT/'v104/CASE-MATRIX-v1.json').read_text())['facets'] if f['facetId'].startswith(source_id+':'))
        matches={}
        for name in ['upper-composite','lower-composite']:
            tuples=patches[name]['uniqueSamples'];sample=tuples[0] if len(tuples)==1 else None
            found=[family for family in ['encodedChannelBlend','linearLightBlend'] if sample in frozen['additionalCandidates'][family]]
            if sample==frozen['additionalCandidates']['opaqueOverwrite']['upper' if name.startswith('upper') else 'lower']:found.append('opaqueOverwrite')
            matches[name]=dict(observedSample=sample,matchingFiniteFamilies=found,uniqueFamily=len(found)==1)
        complete=controls_exact and all(p['flat'] and p['atLeastFivePixelsFromEdges'] for p in result['patches'])
        families=[m['matchingFiniteFamilies'] for m in matches.values()]
        outcome='SUPPORTED_A' if complete and all(len(f)==1 and f[0] in ['encodedChannelBlend','linearLightBlend'] for f in families) else 'SUPPORTED_B' if complete and families==[['opaqueOverwrite'],['opaqueOverwrite']] else 'CONTRARY' if complete and all(m['observedSample'] is not None for m in matches.values()) else 'UNDECIDED'
        result['alphaFiniteDecision']=dict(exactOpaqueControls=controls_exact,allPatchesComplete=complete,composites=matches,outcome=outcome,scope='These finite channel candidates only. Fractional-versus-byte alpha, resolved display color space, universal compositing/storage and global raster metrics remain held.')
    for profile in spec.get('rowProfiles',[]):
        x0,x1,y=profile['xFirstPx'],profile['xLastPx'],profile['yPx'];assert all(isinstance(v,int) for v in [x0,x1,y]) and x0<=x1
        runs=PNG['rle']([(x,pixel(x,y)) for x in range(x0,x1+1)])
        result['rowProfiles'].append(dict(specification=profile,yPx=y,xFirstPx=x0,xLastPx=x1,runs=runs))
    for profile in spec.get('columnProfiles',[]):
        y0,y1,x=profile['yFirstPx'],profile['yLastPx'],profile['xPx'];assert all(isinstance(v,int) for v in [y0,y1,x]) and y0<=y1
        runs=PNG['rle']([(y,pixel(x,y)) for y in range(y0,y1+1)])
        result['columnProfiles'].append(dict(specification=profile,xPx=x,yFirstPx=y0,yLastPx=y1,runs=runs))
    return result


if __name__=='__main__':
    result=build(sys.argv[1]);put(BASE/sys.argv[1]/'pixel-certificate-v1.json',result)
    print(json.dumps(dict(sourceId=sys.argv[1],patches=len(result['patches']),rowProfiles=len(result['rowProfiles']),columnProfiles=len(result['columnProfiles']),alphaDecision=result.get('alphaFiniteDecision'))))
