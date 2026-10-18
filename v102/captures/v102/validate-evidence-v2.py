import json
import runpy
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PRIOR=runpy.run_path(str(BASE/'validate-evidence-v1.py'))
bound=PRIOR['bound']


def validate(revision=1,integrity=True,preservation=None):
    result=PRIOR['validate'](revision,integrity=False,preservation=preservation)
    index=json.loads((BASE/f'numeric-controls-v{revision}.json').read_text())
    manifest=json.loads((ROOT/'v102/bundle-manifest-v1.json').read_text())
    assets={a['sourceId']:a for a in manifest['sources']}
    builder=runpy.run_path(str(BASE/'build-facet-assessments-v2.py'))['build']
    counts=Counter(result['counts'])
    for entry in index['sources']:
        path=BASE/entry['sourceId']/'facet-assessment-v2.json';assessment=json.loads(path.read_text())
        assert builder(entry['sourceId'])==assessment
        assert assessment['sourceSha256']==assets[entry['sourceId']]['sha256'] and assessment['numericReport']==entry['report']
        assert [c['caseId'] for c in assessment['cases']]==assets[entry['sourceId']]['caseIds']
        for case in assessment['cases']:
            assert case['verdict'] in ['SUPPORTED','REFUTED','UNDECIDED']
            for field in ['numeric','visual','admission']:
                evidence=case[field]
                if evidence is not None:assert evidence['verdict'] in ['SUPPORTED','REFUTED','UNDECIDED']
            if case['caseId'].endswith(':box-point-copy-no-set_xloc-v5'):assert case['v5BoxXlocCredit']==0
            if case['caseId'].endswith(':label-time-index-point-copy'):assert case['unobservedIntermediateLabelTimeTransition']
            counts['sourceCase_'+case['verdict']]+=1
        counts['perSourceCaseAssessments']+=1
    if integrity:
        refs=json.loads((BASE/f'artifact-integrity-v{revision}.json').read_text())['artifacts']
        assert len({r['path'] for r in refs})==len(refs)
        for reference in refs:bound(reference)
        counts['integrityBoundFiles']=len(refs)
    result['counts']=dict(counts)
    result['policy']+=' Separate per-case numeric/admission/visual conjunctions are recomputed; intermediate unexposed label time state and v5 box xloc retain zero credit. Case counts are not native parity counts.'
    return result


if __name__=='__main__':print(json.dumps(validate(int(sys.argv[1]) if len(sys.argv)>1 else 1),indent=2))
