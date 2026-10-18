import csv
import json
import runpy
import sys
from fractions import Fraction
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PREVIOUS=runpy.run_path(str(BASE/'validate-evidence-v2.py'))
read=PREVIOUS['read']


def validate(revision=1,integrity=True,preservation=None):
    result=PREVIOUS['validate'](revision,integrity=integrity,preservation=preservation)
    inventory=read(BASE/f'attempt-inventory-v{revision}.json')
    for attempt in inventory['attempts']:
        source=attempt['source'];directory=BASE/source['sourceId'];path=directory/'step-certificate-v1.json'
        if not path.exists():continue
        certificate=read(path);assert runpy.run_path(str(BASE/'build-step-certificate-v1.py'))['build'](source['sourceId'])==certificate
        session=attempt['sessions'][0];assert certificate['originalPng']==session['renderPng'] and certificate['originalCsv']==session['csv'] and certificate['privateScriptId']==source['privateScriptId']
        visual=read(directory/'derived-region-map-v1.json');assert visual['facets'][0]['outcome']==certificate['outcome'] or visual['facets'][0]['outcome']=='UNDECIDED'
        raw=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers=raw[0];a=certificate['anchorOwnIndex'];b=visual['registration']['pixelsPerOwnBar'];xa=visual['registration']['anchorXPx']
        assert certificate['frozenCombinedXPxUncertainty']==3 and len(certificate['transitions'])==2
        for transition in certificate['transitions']:
            phase=transition['phase'];assert phase in [8,24];idx=a-((a-phase)%32)
            assert transition['ownIndex']==idx and Fraction(transition['inputIndex']['valueRaw'])==idx
            for key in ['chartTime','inputIndex','phase32','step','previousStep','anchorRulerDelta']:
                p=transition[key];assert p['csvSha256']==session['csv']['sha256'] and raw[p['rowOrdinal']][p['columnOrdinal']-1]==p['valueRaw'] and headers[p['columnOrdinal']-1]==p['headerRaw']
            x=xa+(idx-a)*b;ai,bi=transition['candidateIntervalsPx']['A'],transition['candidateIntervalsPx']['B'];assert ai==[x-3,x+3] and bi==[x-b/2-3,x-b/2+3]
            if transition['outcome'] in ['SUPPORTED_A','SUPPORTED_B']:
                assert bi[1]<ai[0] and 16<=b<=24 and abs(transition['observedRulerXPx']-x)<=2
                assert all(transition[k] for k in ['rulerSourceJoin','stepFormulaJoin','blueVerticalReadable','bothBlueArmsReadable','redRulerUnobscuredPortionsReadable'])
                candidate=ai if transition['outcome']=='SUPPORTED_A' else bi;assert candidate[0]<=transition['observedTurnXPx']<=candidate[1]
        result['counts']['stepCertificates']=result['counts'].get('stepCertificates',0)+1
    result['policy']+='; separate v5/v6 modulo32 STEP/ruler/raw-arm/vertical certificates with strict three-pixel candidate intervals'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1])),indent=2))
