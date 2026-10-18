import csv
import json
import runpy
import sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put,number=HELPERS['ref'],HELPERS['put'],HELPERS['number']


def samples(profile):
    return {i:r['sample'] for r in profile['runs'] for i in range(r['first'],r['last']+1)}


def build(source_id):
    assert source_id in ['v104-step-turn-v5','v104-step-turn-v6']
    directory=BASE/source_id;pixel_path=directory/'pixel-certificate-v1.json';pixel=json.loads(pixel_path.read_text())
    inspection=json.loads((directory/'visual-inspection-v1.json').read_text());axis=inspection['axisCalibration']
    session=json.loads((ROOT/pixel['rowSet']['path']).read_text());raw=list(csv.reader((ROOT/pixel['originalCsv']['path']).open(newline='')));headers=raw[0]
    anchor=session['uniqueVisualAnchorRowOrdinal'];a=int(number(raw[anchor][headers.index('INPUT_INDEX')]))
    b=pixel['registration']['pixelsPerOwnBar'];xa=pixel['registration']['anchorXPx'];y0,y100=axis['yZeroPx'],axis['yHundredPx'];yp=lambda v:y0-v*(y0-y100)/100
    rows={int(number(raw[n][headers.index('INPUT_INDEX')])):n for n in session['selectedPrimaryClosedRowOrdinals']+session['originalClosedPredecessorRowOrdinals']}
    profiles={p['specification']['name']:p for p in pixel['rowProfiles']+pixel['columnProfiles']}
    def point(n,title):
        c=headers.index(title);return dict(csvSha256=pixel['originalCsv']['sha256'],rowOrdinal=n,columnOrdinal=c+1,headerRaw=title,valueRaw=raw[n][c])
    transitions=[]
    for phase in [8,24]:
        index=a-((a-phase)%32);n=rows[index];previous=rows[index-1]
        turn=profiles['turn'+str(phase)];ruler=profiles['ruler'+str(phase)];lower=profiles['lower'+str(phase)];upper=profiles['upper'+str(phase)]
        blue=turn['specification']['exactStrokeSample'];red=ruler['specification']['exactStrokeSample'];tx=turn['xPx'];rx=ruler['xPx']
        column=samples(turn);ruler_samples=samples(ruler);low=samples(lower);high=samples(upper)
        required=range(round(yp(75))+2,round(yp(25))-1);vertical=all(column.get(y)==blue for y in required)
        ruler_clear=all(ruler_samples.get(y)==red for y in list(range(round(yp(90))+3,round(yp(75))-3))+list(range(round(yp(25))+3,round(yp(10))-3)))
        lower_blue=[x for x,value in low.items() if value==blue];upper_blue=[x for x,value in high.items() if value==blue]
        arm_ends=[max(lower_blue),min(upper_blue)] if phase==8 else [max(upper_blue),min(lower_blue)]
        arms=all(abs(x-tx)<=1 for x in arm_ends)
        expected_ruler=xa+(index-a)*b;ai=[expected_ruler-3,expected_ruler+3];bi=[expected_ruler-b/2-3,expected_ruler-b/2+3]
        separate=bi[1]<ai[0];join=abs(rx-expected_ruler)<=2 and int(number(raw[n][headers.index('PHASE32')]))==phase and number(raw[anchor][headers.index('RULER'+str(phase)+'_DELTA')])==index-a
        formula=number(raw[n][headers.index('STEP')])==(75 if phase==8 else 25) and number(raw[previous][headers.index('STEP')])==(25 if phase==8 else 75)
        complete=16<=b<=24 and separate and join and formula and vertical and arms and ruler_clear
        am=ai[0]<=tx<=ai[1];bm=bi[0]<=tx<=bi[1]
        outcome='SUPPORTED_A' if complete and am and not bm else 'SUPPORTED_B' if complete and bm and not am else 'CONTRARY' if complete and not am and not bm else 'UNDECIDED'
        transitions.append(dict(phase=phase,ownIndex=index,chartTime=point(n,'time'),inputIndex=point(n,'INPUT_INDEX'),phase32=point(n,'PHASE32'),step=point(n,'STEP'),previousStep=point(previous,'STEP'),anchorRulerDelta=point(anchor,'RULER'+str(phase)+'_DELTA'),expectedRulerXPx=expected_ruler,observedRulerXPx=rx,observedTurnXPx=tx,observedArmEndpointsXPx=arm_ends,candidateIntervalsPx=dict(A=ai,B=bi),strictlyDisjoint=separate,rulerSourceJoin=join,stepFormulaJoin=formula,blueVerticalReadable=vertical,bothBlueArmsReadable=arms,redRulerUnobscuredPortionsReadable=ruler_clear,outcome=outcome))
    outcomes={r['outcome'] for r in transitions};outcome=outcomes.pop() if len(outcomes)==1 else 'UNDECIDED' if 'UNDECIDED' in outcomes else 'CONTRARY'
    return dict(version='v1',sourceId=source_id,sourceSha256=pixel['sourceSha256'],privateScriptId=pixel['privateScriptId'],originalPng=pixel['originalPng'],originalCsv=pixel['originalCsv'],pixelCertificate=ref(pixel_path),rowSet=pixel['rowSet'],anchorOwnIndex=a,registeredPixelsPerBar=b,frozenCombinedXPxUncertainty=3,transitions=transitions,outcome=outcome,scope='Two own closed modulo32 transitions, both actual blue arms/verticals and independent red ruler portions; no ruler-coincidence inference, fitted tolerance, viewport rescue or transferred version credit.')


if __name__=='__main__':
    result=build(sys.argv[1]);put(BASE/sys.argv[1]/'step-certificate-v1.json',result)
    print(json.dumps(dict(sourceId=sys.argv[1],outcome=result['outcome'],turns=[dict(phase=r['phase'],turnXPx=r['observedTurnXPx'],rulerXPx=r['observedRulerXPx']) for r in result['transitions']])))
