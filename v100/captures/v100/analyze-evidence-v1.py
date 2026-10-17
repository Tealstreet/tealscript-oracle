import csv
import hashlib
import json
import runpy
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']
CONTEXT=['INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED','CASE_ID']


def number(raw):
    try:return F(raw)
    except (ValueError,TypeError,ZeroDivisionError):return None


def virtual_ref(path,obj):
    raw=(json.dumps(obj,indent=2)+'\n').encode()
    return dict(path=str(path.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def verdict(codes,complete):
    if 'R' in codes:return 'REFUTED'
    if complete and codes and all(c=='S' for c in codes):return 'SUPPORTED'
    return 'UNDECIDED'


def classify(records):
    supported=[c for c in records if c['verdict']=='SUPPORTED']
    undecided=[c for c in records if c['verdict']=='UNDECIDED']
    return dict(observation='ONLY_FROZEN_VECTOR' if len(supported)==1 else 'MULTIPLE_FROZEN_VECTORS' if supported else 'NEITHER_FROZEN_VECTOR' if records and not undecided else 'UNDECIDED / incomplete matching coverage',supportedClassIds=[c['classId'] for c in supported],supportedModelIds=[i for c in supported for i in c['modelIds']],notYetRefutedClassIds=[c['classId'] for c in supported+undecided],classVerdictCounts=dict(Counter(c['verdict'] for c in records)),representativeVerdictCounts=dict(sum((Counter({c['verdict']:len(c['modelIds'])}) for c in records),Counter())))


def native_block(attempt,asset):
    source=attempt['source']
    block=dict(version='v1',sourceId=asset['sourceId'],sourceSha256=asset['sha256'],nativePrivateId=source['privateScriptId'],nativePrivateVersion=source['privateVersion'],rows=[],ownedColumns=[],requiredPrimaryRows=asset['minimumPrimaryClosedRows'],completePrimaryInputCertificate=False,primaryRowOrdinals=[],testedRowOrdinals=[],nativeStatus=attempt['status'],modelMaskLegend={'S':'Exact frozen integer prediction matches this actual owned closed cell','R':'Actual owned closed cell contradicts the frozen integer prediction, including present blank/unexpected code','U':'Ownership/phase/input/prediction unavailable; no value filled'},encodingLimit='V5 value ? 1 : 0 collapses false/Boolean NA; no absent NA/getter/calibration channel is inferred')
    if not attempt['sessions']:return block
    session=attempt['sessions'][0];path=ROOT/session['csv']['path']
    raw=list(csv.reader(path.open(newline='')));headers,data=raw[0],raw[1:]
    bindings=json.loads((ROOT/session['columnBindings']['path']).read_text())
    owned={c['originalHeader'] for c in bindings['columns'] if c.get('owner')==source['privateScriptId'] and c['bindingStatus']=='OBSERVED'}
    selected=session['selectedPrimaryConsecutiveClosedRows'];tested=selected if selected else session['eligibleDataRowOrdinals']
    block.update(csv=session['csv'],columnBindings=session['columnBindings'],closureMask=session['closureMask'],ownedColumns=sorted(owned),primaryRowOrdinals=selected,testedRowOrdinals=tested,completePrimaryInputCertificate=session['primaryInputCertificateValid'],scope='Complete fixed primary block when available; otherwise all naturally available eligible closed partial rows for refutation only. Other original rows remain archived/excluded; no output filter or session stitching.')
    def point(n,title):
        if headers.count(title)!=1:return None
        col=headers.index(title)
        return dict(csvSha256=session['csv']['sha256'],rowOrdinal=n,columnOrdinal=col+1,headerRaw=title,valueRaw=data[n-1][col])
    for n in tested:
        cells={p['title']:point(n,p['title']) for p in asset['plots']}
        phase=number(cells.get('CASE_ID',{}).get('valueRaw')) if cells.get('CASE_ID') else None
        index=number(cells['INPUT_INDEX']['valueRaw']) if cells.get('INPUT_INDEX') else None
        phase_valid=asset.get('phaseModulo') is None or phase is not None and phase.denominator==1 and index is not None and phase==index%asset['phaseModulo'] and 'CASE_ID' in owned
        block['rows'].append(dict(rowOrdinal=n,inputCells=[point(n,t) for t in ['time']+CONTEXT if t in headers],cells=cells,phaseValue=int(phase) if phase is not None and phase.denominator==1 else None,phaseInputValid=phase_valid,primaryScoringCredit=bool(session['primaryInputCertificateValid'] and n in selected),actualClosedObservation=True))
    return block


def score_scope(block,block_ref,family,spec,mapping_ref,original_ref,packing_models=None):
    columns=spec['columnTitles'];records=[];owned=set(block['ownedColumns'])
    complete=block['completePrimaryInputCertificate'] and set(columns)<=owned
    for class_index,signature in enumerate(spec['classes']):
        matrices=[];all_codes=[];properties={};route_counts=Counter()
        expected_rows={r['CASE_ID']:r['expected'] for r in signature.get('rows',[])}
        if family=='packing':
            for mid in signature['modelIds']:
                route=packing_models[int(mid.split(':')[1])].get('getterRoute')
                route_counts['scalar-getter field absent' if route is None else route]+=1
        for row_index,row in enumerate(block['rows']):
            phase=row['phaseValue'] if row['phaseInputValid'] else None
            mask=[]
            for j,title in enumerate(columns):
                target=row['cells'].get(title)
                if family in ['scalar','packing']:
                    expected=signature['expectedCodes'][j];property_key=title
                else:
                    property_key=(str(phase) if phase is not None else 'UNOBSERVED_PHASE')+'/'+title
                    if phase in expected_rows:expected=expected_rows[phase][title]
                    else:
                        values={r[title] for r in expected_rows.values()}
                        expected=next(iter(values)) if len(values)==1 else None
                code='U' if title not in owned or target is None or expected is None else 'S' if number(target['valueRaw'])==number(expected) else 'R'
                mask.append(code);all_codes.append(code)
                item=properties.setdefault(property_key,dict(property=title,phase=phase if family=='materialization' else None,expectedRawInteger=expected,comparisonCodes=[],nativeRowOrdinals=[]))
                item['comparisonCodes'].append(code);item['nativeRowOrdinals'].append(row['rowOrdinal'])
            matrices.append(dict(rowOrdinal=row['rowOrdinal'],nativeBlockRowPointer='/rows/'+str(row_index),phase=phase,cellVerdicts=''.join(mask)))
        property_verdicts=[]
        if family=='materialization':
            for phase,expected in expected_rows.items():
                for title in columns:properties.setdefault(str(phase)+'/'+title,dict(property=title,phase=phase,expectedRawInteger=expected[title],comparisonCodes=[],nativeRowOrdinals=[]))
        for item in properties.values():
            expected_count=4 if family=='materialization' else block['requiredPrimaryRows']
            codes=item.pop('comparisonCodes');item['counts']=dict(Counter(codes));item['requiredSamples']=expected_count
            item['verdict']=verdict(codes,complete and len(codes)==expected_count)
            item['cause']=None if item['verdict']!='UNDECIDED' else 'Missing complete requested owned/closed row or phase/column/prediction coverage; matching partial data never supports a full property'
            property_verdicts.append(item)
        record=dict(classId=signature['classId'],family=family,modelIds=signature['modelIds'],memberCount=len(signature['modelIds']),predictionMap=dict(artifact=mapping_ref,jsonPointer='/'+family+'/classes/'+str(class_index)),originalPredictionFile=original_ref,originalMemberPointerRule={'scalar':'/representativeModels/<S:id>','packing':'/models/<P:index>','materialization':'/candidates/<B:id>'}[family],originalQueryIndexes=spec.get('originalQueryIndexes',spec.get('originalNewQueryIndexes')),testedColumns=columns,nativeTargets=dict(artifact=block_ref,rowsJsonPointer='/rows',cellDictionary='cells/<exact column title>; each pointer carries original CSV SHA/row/column/header/raw string'),expectedCodes=signature.get('expectedCodes'),expectedRows=signature.get('rows'),comparisonRows=matrices,comparisonCodeCounts=dict(Counter(all_codes)),propertyVerdicts=property_verdicts,verdict=verdict(all_codes,complete),completeOwnedClosedCertificate=complete,exclusionCause=None if complete else 'Support held: complete requested primary input/ownership/closure certificate is unavailable; actual contrary owned closed cells still refute',memberGetterRoutes=dict(route_counts),scope=spec.get('scope',spec.get('predicate')))
        records.append(record)
    return dict(family=family,scope=spec.get('scope',spec.get('predicate')),columnTitles=columns,classes=records,adjudication=classify(records),classCompression='Every member has exactly the same mapped frozen vector, verified against its original prediction record. Membership counts do not multiply native cells or parity credit.')


def analyze(revision=1,write=False):
    inventory=json.loads((BASE/f'attempt-inventory-v{revision}.json').read_text());manifest=json.loads((ROOT/'v100/bundle-manifest-v1.json').read_text())
    mapping_path=ROOT/manifest['predictionMap'];mapping=json.loads(mapping_path.read_text());mapping_ref=ref(mapping_path)
    original_paths={'scalar':ROOT/'v100/predictions/proposed-v100-predictions-v2.json','packing':ROOT/'v100/predictions/packing-proposed-predictions-v2.json','materialization':ROOT/'v100/predictions/proposed-materialization-predictions-v1.json'}
    originals={k:ref(p) for k,p in original_paths.items()};packing_models=json.loads(original_paths['packing'].read_text())['models']
    reports=[];blocks=[]
    for attempt in inventory['attempts']:
        asset=next(s for s in manifest['sources'] if s['sourceId']==attempt['source']['sourceId'])
        directory=BASE/asset['sourceId'];block=native_block(attempt,asset);block_path=directory/'native-cell-block-v1.json';block_ref=virtual_ref(block_path,block)
        if write:put(block_path,block)
        blocks.append(block)
        families=['scalar','packing'] if asset['slot']==1 else ['materialization']
        scopes=[score_scope(block,block_ref,family,mapping[family],mapping_ref,originals[family],packing_models) for family in families]
        report=dict(sourceId=asset['sourceId'],sourceSha256=asset['sha256'],pineVersion=asset['pineVersion'],slot=asset['slot'],nativeCompileSuccess=attempt['source']['nativeCompileSuccess'],nativeBlock=block_ref,nativePrivateId=block['nativePrivateId'],nativePrivateVersion=block['nativePrivateVersion'],requiredPrimaryRows=block['requiredPrimaryRows'],primaryRowOrdinals=block['primaryRowOrdinals'],testedRowOrdinals=block['testedRowOrdinals'],completePrimaryInputCertificate=block['completePrimaryInputCertificate'],ownedPlotColumns=len(block['ownedColumns']),scopes=scopes,unobserved=['Color NA predicate and false/Boolean-NA distinction in v5 ternary outputs','Unexported getters/calibration/hidden packed payloads/unexpanded aliases','Native feed/execution IDs, independent editor arrays, actual calculation count and full private inventory'],scope='New unchanged source execution only; frozen author hypotheses are not native inputs, recovered bytes, generic identity or engine approval')
        if asset['slot']==1:
            title='DIRECT_RGB_NEW_12P1_EQ';first=next((r for r in block['rows'] if title in block['ownedColumns'] and r['cells'].get(title) is not None),None)
            report['directDiscriminator']=dict(property=title,firstOwnedClosedCell=first['cells'][title] if first else None,predictions={'S:4835':0,'S:4843':1},oneClosedCellVerdicts={mid:'UNDECIDED' if not first else 'SUPPORTED' if number(first['cells'][title]['valueRaw'])==value else 'REFUTED' for mid,value in [('S:4835',0),('S:4843',1)]},fullScalarClassVerdicts={mid:next(c['verdict'] for c in scopes[0]['classes'] if mid in c['modelIds']) for mid in ['S:4835','S:4843']},rawObservedCodeCounts=dict(Counter(r['cells'][title]['valueRaw'] for r in block['rows'] if r['cells'].get(title) is not None and title in block['ownedColumns'])),scope='One owned physically closed numeric code can distinguish the two single-column predictions; it does not certify either complete19-code vector or hidden Boolean/color semantics')
        if write:put(directory/'numeric-results-v1.json',report)
        reports.append(report)
    shared=[]
    version_reports={r['pineVersion']:r for r in reports if r['slot'] in [2,3]}
    for signature in mapping['materialization']['classes']:
        statuses={};refs={}
        for version in [5,6]:
            source=version_reports.get(version)
            row=next((c for c in source['scopes'][0]['classes'] if c['classId']==signature['classId']),None) if source else None
            statuses[str(version)]=row['verdict'] if row else 'UNDECIDED'
            refs[str(version)]=dict(sourceId=source['sourceId'],nativeBlock=source['nativeBlock'],classId=signature['classId']) if source else None
        status='REFUTED' if 'REFUTED' in statuses.values() else 'SUPPORTED' if set(statuses.values())=={'SUPPORTED'} else 'UNDECIDED'
        shared.append(dict(classId=signature['classId'],modelIds=signature['modelIds'],verdict=status,separateSourceVerdicts=statuses,separateSourceTargets=refs,sharedSupportHeld=not all(version in version_reports and version_reports[version]['completePrimaryInputCertificate'] for version in [5,6]),scope='Same B ID must match both separately owned version vectors. A contrary version refutes; missing coverage never supplies cross-version support or borrowed values.'))
    counts=Counter();model_counts=Counter()
    for report in reports:
        for scope in report['scopes']:
            for record in scope['classes']:
                counts[record['verdict']]+=1;model_counts[record['verdict']]+=len(record['modelIds'])
    return dict(version=f'v{revision}',requestCommit=inventory['requestCommit'],predictionMap=mapping_ref,projectionMembershipAudit=ref(BASE/'prediction-membership-audit-v1.json'),sources=reports,sharedMaterialization=dict(classes=shared,adjudication=classify(shared)),classVerdictCounts=dict(counts),scopedRepresentativeVerdictCounts=dict(model_counts),membershipCountsAreNotNativeCells=True,noCombinedScalarPackingModel=True,scope='Only mapped19/17 codes and independent19-phase six-field vectors. No fitted quantizer/row filter/byte decoder, alias-completeness, fixture promotion or historical-hold closure.')
