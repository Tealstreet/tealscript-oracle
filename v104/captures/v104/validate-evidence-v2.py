import csv
import hashlib
import json
import runpy
import sys
from fractions import Fraction
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PREVIOUS=runpy.run_path(str(BASE/'validate-evidence-v1.py'))
read,bound,clock=PREVIOUS['read'],PREVIOUS['bound'],PREVIOUS['clock']


def validate(revision=1,integrity=True,preservation=None):
    result=PREVIOUS['validate'](revision,integrity=integrity,preservation=preservation)
    inventory=read(BASE/f'attempt-inventory-v{revision}.json');viewport=read(BASE/'environment-v1/viewport-preregistration-v1.json')
    assert viewport['uncertaintyBeforeScoring']==dict(axisXPx=2,axisYPx=3,strokeEdgePx=1,stepCombinedXPx=3)
    assert viewport['sourceSlotsConsumed']==0 and viewport['newLayoutId']==208421791 and viewport['pageId']==16
    for attempt in inventory['attempts']:
        source=attempt['source'];directory=BASE/source['sourceId'];start=read(directory/'attempt-v1/attempt-start-v1.json')
        assert clock(viewport['registeredBeforeSourceAttemptsAtUtc'])<clock(start['startedAtUtc'])
        assert start['sourceSha256']==source['sourceSha256'] and start['saveLimit']==start['addLimit']==1
        for session in attempt['sessions']:
            receipt=read(ROOT/session['sessionReceipt']['path']);assert receipt['viewportActions']==[] and receipt['inputMode']==0
            map_path=directory/'derived-region-map-v1.json'
            if not map_path.exists():continue
            visual=read(map_path);registration=visual['registration']
            if registration:
                assert registration['uncertaintyPx']==dict(x=2,y=3,strokeEdge=1)
                left,right=registration['primaryPlusPredecessorsWindowXPx'];assert abs((right-left)/registration['pixelsPerOwnBar']-39)<1e-8
            pixel_path=directory/'pixel-certificate-v1.json'
            if not pixel_path.exists():continue
            certificate=read(pixel_path);window=visual['facets'][0]['derivedRequestedWindowPx']
            if window and visual['facets'][0]['outcome']!='UNDECIDED':
                for profile in certificate['rowProfiles']:
                    assert window[0]<=profile['xFirstPx']<=profile['xLastPx']<=window[2] and window[1]<=profile['yPx']<=window[3]
                for profile in certificate['columnProfiles']:
                    assert window[0]<=profile['xPx']<=window[2] and window[1]<=profile['yFirstPx']<=profile['yLastPx']<=window[3]
            relation_path=directory/'pixel-relations-v1.json'
            if relation_path.exists():
                relation=read(relation_path)
                assert runpy.run_path(str(BASE/'build-pixel-relations-v1.py'))['build'](source['sourceId'])==relation
                assert relation['originalPng']==session['renderPng'] and relation['originalCsv']==session['csv']
                assert visual['facets'][0]['outcome']==relation['outcome'] or visual['facets'][0]['outcome']=='UNDECIDED'
                if source['sourceId']=='v104-glyph-advance-v6':
                    independent={}
                    for profile in certificate['rowProfiles']:
                        wanted=profile['specification']['exactBodySample'];positions=[i for r in profile['runs'] if r['sample']==wanted for i in range(r['first'],r['last']+1)]
                        independent[profile['specification']['name']]=max(positions)-min(positions)+1
                    assert independent==relation['outerBodyWidthsInclusivePx']
                    mono=independent['monoW']-independent['monoI'];default=independent['defaultW']-independent['defaultI']
                    assert relation['candidateIntervalsPx']==dict(A=[-4,4],B=[default-4,default+4])
                    if relation['outcome']=='SUPPORTED_A':assert abs(mono)<=4 and default-4>4
                    assert relation['observedMonospaceDifferencePx']==mono and relation['observedDefaultDifferencePx']==default
                elif source['sourceId']=='v104-dash-period-v6':
                    ranges=[];normalized=[]
                    for measurement in relation['measurements']:
                        runs=measurement['completeInteriorStrokeRuns'];periods=[runs[i+1]['first']-runs[i]['first'] for i in range(len(runs)-1)]
                        assert periods==measurement['periodsPx'] and len(periods)==measurement['completeInteriorPeriodCount']
                        if periods:ranges.append([min(periods),max(periods)]);normalized.append([Fraction(min(periods),measurement['sourceWidth']),Fraction(max(periods),measurement['sourceWidth'])])
                    constant=len(ranges)==3 and max(r[0] for r in ranges)<=min(r[1] for r in ranges)
                    scaled=len(normalized)==3 and max(r[0] for r in normalized)<=min(r[1] for r in normalized)
                    if relation['outcome']=='SUPPORTED_A':assert constant and not scaled and all(m['completeInteriorPeriodCount']>=3 for m in relation['measurements'])
                    if relation['outcome']=='SUPPORTED_B':assert scaled and not constant and all(m['completeInteriorPeriodCount']>=3 for m in relation['measurements'])
                result['counts']['pixelRelations']=result['counts'].get('pixelRelations',0)+1
            if source['sourceId']=='v104-alpha-composite-v6':
                assert len(certificate['patches'])==6
                for patch in certificate['patches']:
                    x,y=patch['centerPx'];assert {(p['xPx'],p['yPx']) for p in patch['samples']}=={(xx,yy) for yy in range(y-2,y+3) for xx in range(x-2,x+3)}
                if not certificate['alphaFiniteDecision']['exactOpaqueControls']:assert visual['facets'][0]['outcome']=='UNDECIDED'
    for pattern in ['*/attempt-v1/save-response-v1.json','*/attempt-v1/add-response-v1.json','*/attempt-v1/session-*/chart-native-v1.csv','*/attempt-v1/session-*/render-v1.png']:
        assert len(list(BASE.glob(pattern)))<=13
    result['policy']+='; initial viewport clocks and frozen uncertainty; independently recomputed original-pixel profiles and finite width/period relations'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
