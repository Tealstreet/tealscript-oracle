import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent


def ref(path):
    raw=path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def half_up(value):return (2*value.numerator+value.denominator)//(2*value.denominator)


def audit():
    manifest=json.loads((ROOT/'v100/bundle-manifest-v1.json').read_text())
    mapping=json.loads((ROOT/manifest['predictionMap']).read_text())
    frozen={}
    for item in manifest['predictionArtifacts']:
        actual=ref(ROOT/item['path'])
        assert actual['bytes']==item['bytes'] and actual['sha256']==item['sha256']
        frozen[item['path']]=json.loads((ROOT/item['path']).read_text())
    for source,binding in zip(manifest['sources'],mapping['sourceBindings']):
        assert source['path']==binding['path'] and source['sha256']==binding['sha256'] and source['plots']==binding['plots']
    scalar=frozen['v100/predictions/proposed-v100-predictions-v2.json']
    packing=frozen['v100/predictions/packing-proposed-predictions-v2.json']
    material=frozen['v100/predictions/proposed-materialization-predictions-v1.json']
    totals={};member_bindings={}
    for family,original,key,prefix in [('scalar',scalar,'representativeModels','S'),('packing',packing,'models','P')]:
        group=mapping[family];indexes=group['originalQueryIndexes'];seen=set();routes=Counter();members=[]
        assert len(indexes)==len(group['columnTitles'])=={'scalar':19,'packing':17}[family]
        assert [original['queries'][i]['title'] for i in indexes]==group['columnTitles']
        for class_index,signature in enumerate(group['classes']):
            assert len(signature['expectedCodes'])==len(indexes)
            for model_id in signature['modelIds']:
                assert model_id.startswith(prefix+':') and model_id not in seen
                seen.add(model_id);i=int(model_id.split(':')[1]);record=original[key][i]
                if family=='scalar':assert record['id']==i
                vector=''.join(str(record['predictions'][q]) for q in indexes)
                assert vector==signature['expectedCodes'],model_id
                if family=='packing':
                    route=record.get('getterRoute');routes['scalar-getter field absent' if route is None else route]+=1
                    members.append(dict(modelId=model_id,classId=signature['classId'],originalJsonPointer='/models/'+str(i),file=record['file'],row=record['row'],getterRouteField=route,routeScope='scalar-getter' if route is None else route))
        assert seen=={prefix+':'+str(i) for i in range(len(original[key]))}
        totals[family]=dict(classes=len(group['classes']),modelIds=len(seen),mappedColumns=len(indexes),originalQueryIndexes=indexes,getterRoutes=dict(routes))
        member_bindings[family]=members
    assert totals['scalar']['modelIds']==7753 and totals['scalar']['classes']==263
    assert totals['packing']['modelIds']==45769 and totals['packing']['classes']==108
    assert totals['packing']['getterRoutes']=={'scalar-getter field absent':38569,'packed-byte-decode':7200}
    group=mapping['materialization'];seen=set()
    for signature in group['classes']:
        assert len(signature['rows'])==19
        for model_id in signature['modelIds']:
            assert model_id not in seen;seen.add(model_id);i=int(model_id.split(':')[1]);candidate=material['candidates'][i];assert candidate['id']==i
            expected_alphas=group['commonPredictedControlAlphas']+[candidate['predictions'][q] for q in group['originalNewQueryIndexes']]
            for phase,(row,alpha) in enumerate(zip(signature['rows'],expected_alphas)):
                assert row['CASE_ID']==phase and row['predictedAlphaLabel']==alpha
                assert F(row['transparencyLiteral'])==F(str(group['phaseTransparencies'][phase]))
                palette=group['phasePalettes'][phase]
                expected=dict(NEW_R='33',NEW_G='66',NEW_B='99',NEW_T=str(half_up(100-F(alpha*100,255))),NEW_EQ_C0=str(int(alpha==palette[0])),NEW_EQ_C1=str(int(alpha==palette[-1])))
                assert row['expected']==expected
    assert seen=={'B:'+str(i) for i in range(816)} and len(group['classes'])==8
    totals['materialization']=dict(classes=8,recipesPerVersion=len(seen),phases=19,fieldsPerPhase=6,separateVersions=[5,6])
    return dict(version='v1',status='PASS',predictionMap=ref(ROOT/manifest['predictionMap']),frozenPredictionFiles=[ref(ROOT/item['path']) for item in manifest['normativePredictions']],sourceBindings=mapping['sourceBindings'],scopes=totals,packingMemberBindings=member_bindings['packing'],scope='Projection/membership audit of frozen author inputs only; no native output or hidden representation is supplied. Every P getter route/file/row remains independently identified.')


if __name__=='__main__':
    result=audit();path=BASE/'prediction-membership-audit-v1.json';text=json.dumps(result,indent=2)+'\n'
    if path.exists():assert path.read_text()==text
    else:path.write_text(text)
    print(json.dumps(dict(status=result['status'],scopes=result['scopes']),indent=2))
