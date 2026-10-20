import json
import math
from collections import Counter
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']
PNG=runpy.run_path(str(BASE/'read-png-pixels-v1.py'))


def mapped(bounds,relative):
    x0,y0,x1,y1=bounds;u0,u1,v0,v1=relative
    return [x0+(x1-x0)*u0,y0+(y1-y0)*v0,x0+(x1-x0)*u1,y0+(y1-y0)*v1]


def intersects(a,b):
    return max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3])


def build(source_id):
    directory=BASE/source_id;inspection_path=directory/'visual-inspection-v1.json';inspection=json.loads(inspection_path.read_text())
    asset=next(a for a in json.loads((ROOT/'v107/bundle-manifest-v1.json').read_text())['entries'] if a['sourceId']==source_id);facet=asset['visualFacets'][0];frozen=facet['predeclaredWindows']
    session_dir=directory/'attempt-v1/session-mode0-v1';session=json.loads((session_dir/'row-set-observation-v1.json').read_text());observation=json.loads((directory/'attempt-v1/observation-v1.json').read_text())
    pane=inspection['axisCalibration']['paneInteriorBoundsPx'];objects=inspection['tableObjects'];occluders=inspection['occlusionRegionsPx'];png=PNG['decode'](ROOT/session['renderPng']['path']);pixel=png['pixel']
    envelopes={name:mapped(pane,region) for name,region in frozen['envelopes'].items()};windows=[];causes=[]
    for name,envelope in envelopes.items():
        obj=objects.get(name);regions=[('envelope',envelope)];bounds=obj.get('exteriorPx') if obj else None
        if bounds:
            if not (envelope[0]<=bounds[0]<bounds[2]<=envelope[2] and envelope[1]<=bounds[1]<bounds[3]<=envelope[3]):causes.append(name+' complete exterior leaves its frozen envelope')
            if not obj['registrationReadable']:causes.append(name+' complete exterior cannot be registered from all readable boundary segments')
            regions.append(('body',mapped(bounds,frozen['body'])))
            text=frozen['completeText']
            for label,region in (text.items() if isinstance(text,dict) else [('completeText',text)]):
                if label.startswith('subject') and name!='subject' or label.startswith('control') and name!='control':continue
                regions.append(('text/'+label,mapped(bounds,region)))
            for label,region in frozen.get('bodies',{}).items():
                if label.startswith('subject') and name!='subject' or label.startswith('control') and name!='control':continue
                regions.append(('body/'+label,mapped(bounds,region)))
            for label,region in frozen.get('frame',{}).items():regions.append(('frame/'+label,mapped(bounds,region)))
            for i,region in enumerate(frozen.get('divider',[])):regions.append(('divider/'+str(i+1),mapped(bounds,region)))
        elif name!='original':causes.append(name+' required named table exterior absent or unreadable')
        for label,region in regions:
            overlaps=[o for o in occluders if intersects(region,o['boundsPx'])]
            if overlaps:causes.append(name+'/'+label+' intersects '+','.join(o['identity'] for o in overlaps))
            x0,y0,x1,y1=region;ym=round((y0+y1)/2);xm=round((x0+x1)/2);left=max(0,math.floor(x0));right=min(png['width']-1,math.ceil(x1)-1);top=max(0,math.floor(y0));bottom=min(png['height']-1,math.ceil(y1)-1)
            row=PNG['rle']([(x,pixel(x,ym)) for x in range(left,right+1)]) if 0<=ym<png['height'] else []
            column=PNG['rle']([(y,pixel(xm,y)) for y in range(top,bottom+1)]) if 0<=xm<png['width'] else []
            full_rows=[];histogram=Counter()
            for y in range(top,bottom+1):
                samples=[(x,pixel(x,y)) for x in range(left,right+1)]
                histogram.update(tuple(rgb) for x,rgb in samples)
                full_rows.append(dict(yPx=y,runs=PNG['rle'](samples)))
            windows.append(dict(objectIdentity=name,regionIdentity=label,derivedWindowPx=region,conservativeOriginalPixelCellBounds=[left,top,right+1,bottom+1],fullOriginalRows=full_rows,rawSampleHistogram=[dict(sample=list(rgb),pixels=count) for rgb,count in sorted(histogram.items())],coveredPixelCells=sum(histogram.values()),occludingObjects=overlaps,rawCenterRow=dict(yPx=ym,runs=row),rawCenterColumn=dict(xPx=xm,runs=column),finding=obj.get('windowFindings',{}).get(label,'UNOBSERVED') if obj else 'UNOBSERVED; no complete registered exterior'))
    finding=inspection['facets'][0];causes+=finding.get('notObservedCauses',[])
    outcome='UNDECIDED' if causes else finding['outcome']
    return dict(version='v2',sourceId=source_id,slotId=asset['slotId'],sourceSha256=asset['sha256'],privateScriptId=observation['privateScriptId'],privateVersion=observation['privateVersion'],originalPng=session['renderPng'],originalCsv=session['csv'],rowSet=ref(session_dir/'row-set-observation-v1.json'),manualInspection=ref(inspection_path),frozenPredeclaredWindows=frozen,paneInteriorBoundsPx=pane,derivedEnvelopesPx=envelopes,registeredTableObjects=objects,namedWindows=windows,outcome=outcome,notObservedCauses=list(dict.fromkeys(causes)),pixelCoverageRule='Conservative original pixel cells intersecting each continuous fixed window: floor minima, ceil maxima exclusive; full row RLE and raw channel histogram, no color conversion or synthetic alpha',scope='Complete per-object fixed envelopes, exterior registration, body/text/individual frame bands/divider strips; raw scan pointers do not complete unreadable glyphs or infer occluded structures.')


if __name__=='__main__':
    result=build(sys.argv[1]);put(BASE/sys.argv[1]/'table-certificate-v2.json',result)
    print(json.dumps({'sourceId':sys.argv[1],'outcome':result['outcome'],'windows':len(result['namedWindows']),'causes':result['notObservedCauses']}))
