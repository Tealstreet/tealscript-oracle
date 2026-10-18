import csv
import json
import runpy
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put,number=HELPERS['ref'],HELPERS['put'],HELPERS['number']


def verdict(codes,complete):
    if 'R' in codes:return 'REFUTED'
    return 'SUPPORTED' if complete and codes and all(c=='S' for c in codes) else 'UNDECIDED'


def encoded_ref(path,value):
    import hashlib
    raw=(json.dumps(value,indent=2)+'\n').encode()
    return dict(path=str(path.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def native_block(attempt,asset):
    source=attempt['source']
    block=dict(version='v1',sourceId=asset['sourceId'],sourceSha256=asset['sha256'],nativePrivateId=source['privateScriptId'],nativePrivateVersion=source['privateVersion'],rows=[],ownedTitles=[],completePrimaryCertificate=False,primaryRowOrdinals=[],testedRowOrdinals=[],uniqueVisualAnchorRowOrdinal=None)
    if not attempt['sessions']:return block
    session=attempt['sessions'][0]
    raw=list(csv.reader((ROOT/session['csv']['path']).open(newline='')));headers,data=raw[0],raw[1:]
    bindings=json.loads((ROOT/session['columnBindings']['path']).read_text())
    owned={c['originalHeader'] for c in bindings['columns'] if c.get('sourceLiteralPlotOrdinal') is not None and c['bindingStatus']=='OBSERVED' and c['owner']==source['privateScriptId']}
    selected=session['selectedPrimaryClosedRowOrdinals'];tested=selected if selected else session['eligibleClosedSourceRows']
    block.update(csv=session['csv'],columnBindings=session['columnBindings'],closureMask=session['closureMask'],ownedTitles=sorted(owned),completePrimaryCertificate=session['primaryInputCertificateValid'],primaryRowOrdinals=selected,testedRowOrdinals=tested,uniqueVisualAnchorRowOrdinal=session['uniqueVisualAnchorRowOrdinal'],originalClosedPredecessorRows=session['originalClosedPredecessorRowOrdinals'])
    def point(n,title):
        if headers.count(title)!=1:return None
        column=headers.index(title)
        return dict(csvSha256=session['csv']['sha256'],rowOrdinal=n,columnOrdinal=column+1,headerRaw=title,valueRaw=data[n-1][column])
    closed=set(session['independentlyClosedRowOrdinals'])
    for n in tested:
        phase=number(data[n-1][headers.index('CASE_ID')])
        predecessors=list(range(n-asset['requiredOriginalClosedPredecessors'],n))
        dependency_ok=all(p in closed for p in predecessors)
        if dependency_ok and predecessors:
            indices=[number(data[p-1][headers.index('INPUT_INDEX')]) for p in predecessors+[n]]
            times=[number(data[p-1][0]) for p in predecessors+[n]]
            dependency_ok=all(b==a+1 for a,b in zip(indices,indices[1:])) and all(b>a for a,b in zip(times,times[1:]))
        block['rows'].append(dict(rowOrdinal=n,phase=int(phase) if phase is not None and phase.denominator==1 else None,cells={p['title']:point(n,p['title']) for p in asset['plots']},chartTime=point(n,'time'),originalClosedDependencyAvailable=dependency_ok,originalClosedDependencyRowOrdinals=predecessors,primaryScoringCredit=bool(session['primaryInputCertificateValid'] and n in selected)))
    anchor=session['uniqueVisualAnchorRowOrdinal']
    block['visualAnchor']=dict(rowOrdinal=anchor,cells={t:point(anchor,t) for t in ['time','INPUT_TIME','INPUT_INDEX','CHART_CONFIRMED','CASE_ID','VISUAL_ANCHOR_TIME','VISUAL_ANCHOR_INDEX']}) if anchor else None
    return block


def comparisons(block,title,expected):
    result=[]
    for i,row in enumerate(block['rows']):
        point=row['cells'].get(title);phase=row['phase']
        raw=expected[phase] if phase is not None and phase in range(8) else None
        dependency=title not in ['LINE_TIME_X1_DELTA','BOX_TIME_DELTA'] or row['originalClosedDependencyAvailable']
        code='U' if title not in block['ownedTitles'] or point is None or raw is None or not dependency else 'S' if (point['valueRaw']=='' if raw=='' else number(point['valueRaw'])==number(raw)) else 'R'
        result.append(dict(rowOrdinal=row['rowOrdinal'],phase=phase,expectedRaw=raw,actualPointer='/rows/'+str(i)+'/cells/'+title,cellVerdict=code,cause=None if code=='S' else 'Actual owned closed raw value/blank contradicts the frozen source/request prediction' if code=='R' else 'Missing ownership/phase/original closed dependency; no value filled'))
    return result


def analyze(revision=1,write=False):
    inventory=json.loads((BASE/f'attempt-inventory-v{revision}.json').read_text())
    manifest=json.loads((ROOT/'v102/bundle-manifest-v1.json').read_text())
    contracts_path=BASE/'numeric-contracts-v1.json';contracts=json.loads(contracts_path.read_text())
    reports=[]
    for attempt in inventory['attempts']:
        asset=next(a for a in manifest['sources'] if a['sourceId']==attempt['source']['sourceId'])
        contract_index=next(i for i,c in enumerate(contracts['sources']) if c['sourceId']==asset['sourceId']);contract=contracts['sources'][contract_index]
        block=native_block(attempt,asset);directory=BASE/asset['sourceId'];block_path=directory/'native-cell-block-v1.json';block_ref=encoded_ref(block_path,block)
        properties=[]
        for index,frozen in enumerate(contract['contracts']):
            rows=comparisons(block,frozen['title'],frozen['expectedRawByPhase']);codes=[r['cellVerdict'] for r in rows]
            actual=[r['cells'][frozen['title']]['valueRaw'] for r in block['rows'] if r['cells'].get(frozen['title']) is not None]
            complete=block['completePrimaryCertificate'] and frozen['title'] in block['ownedTitles'] and len(rows)==32
            properties.append(dict(title=frozen['title'],sourcePlotOrdinal=frozen['sourcePlotOrdinal'],contractArtifact=ref(contracts_path),contractPointer='/sources/'+str(contract_index)+'/contracts/'+str(index),expectedRawByPhase=frozen['expectedRawByPhase'],nativeTargets=block_ref,comparisonRows=rows,observedRawCounts=dict(Counter(actual)),comparisonCounts=dict(Counter(codes)),verdict=verdict(codes,complete),intentOnly=frozen['intentOnly'],scope=frozen['scope']))
        alternatives=[]
        for family_index,family in enumerate(contract['alternatives']):
            variants=[]
            for variant_index,variant in enumerate(family['variants']):
                rows={title:comparisons(block,title,expected) for title,expected in variant['valuesByPhase'].items()}
                codes=[r['cellVerdict'] for values in rows.values() for r in values]
                complete=block['completePrimaryCertificate'] and set(rows)<=set(block['ownedTitles']) and all(len(v)==32 for v in rows.values())
                variants.append(dict(id=variant['id'],contractArtifact=ref(contracts_path),contractPointer='/sources/'+str(contract_index)+'/alternatives/'+str(family_index)+'/variants/'+str(variant_index),expectedRawByPhase=variant['valuesByPhase'],nativeTargets=block_ref,comparisonsByTitle=rows,comparisonCounts=dict(Counter(codes)),verdict=verdict(codes,complete)))
            supported=[v['id'] for v in variants if v['verdict']=='SUPPORTED'];undecided=[v['id'] for v in variants if v['verdict']=='UNDECIDED']
            alternatives.append(dict(id=family['id'],variants=variants,supportedVariantIds=supported,observation='ONLY_REGISTERED_VARIANT' if len(supported)==1 else 'MULTIPLE_REGISTERED_VARIANTS' if supported else 'UNDECIDED' if undecided else 'NEITHER_REGISTERED_VARIANT',scope='Only this finite separately mapped numeric alternative; no hidden lifecycle/token/appearance or cross-version inference'))
        observed_only=[]
        for title in contract['unpredictedRequestedTitles']:
            observed_only.append(dict(title=title,nativeTargets=block_ref,observedRawCounts=dict(Counter(r['cells'][title]['valueRaw'] for r in block['rows'] if r['cells'].get(title) is not None)),predictionStatus='UNSPECIFIED; actual raw source observations only'))
        visual_path=directory/'derived-region-map-v1.json'
        report=dict(version='v1',sourceId=asset['sourceId'],sourceSha256=asset['sha256'],pineVersion=asset['pineVersion'],family=asset['family'],sourceObservation=attempt['source'],nativeBlock=block_ref,primaryInputCertificateValid=block['completePrimaryCertificate'],primaryRows=block['primaryRowOrdinals'],properties=properties,numericAlternatives=alternatives,observedWithoutPrediction=observed_only,renderAssessment=ref(visual_path) if visual_path.exists() else None,renderAssessmentStatus='DERIVED / original PNG inspection bound separately' if visual_path.exists() else 'NOT OBSERVED / numerical boundary needs no appearance' if asset['kind']=='numeric-boundary' else 'UNDECIDED / visual assessment pending or native admission unavailable',dynamicContext='Independent source INPUT_INDEX/INPUT_TIME, confirmation, phase and anchor/predecessor certificate; no absolute rebased-index parity claim',uniquePrimaryPlotCells=len(block['primaryRowOrdinals'])*len(block['ownedTitles']) if block['completePrimaryCertificate'] else 0,scope='Native numeric getters, blanks and intent codes remain separate from original PNG appearance. No engine expected values, output filter, tolerance, hidden field, cross-version borrowing or historical-hold closure')
        if write:
            put(block_path,block)
            put(directory/'numeric-results-v1.json',report)
        reports.append(dict(sourceId=asset['sourceId'],report=encoded_ref(directory/'numeric-results-v1.json',report),primaryInputCertificateValid=report['primaryInputCertificateValid'],primaryRows=report['primaryRows'],uniquePrimaryPlotCells=report['uniquePrimaryPlotCells'],numericPropertyVerdicts=dict(Counter(p['verdict'] for p in properties)),numericAlternativeOutcomes={f['id']:dict(observation=f['observation'],supportedVariantIds=f['supportedVariantIds']) for f in alternatives},renderAssessment=report['renderAssessment']))
    return dict(version=f'v{revision}',representation='per-source-index-v1',requestCommit=inventory['requestCommit'],frozenNumericContracts=ref(contracts_path),sources=reports,uniquePrimaryPlotCells=sum(r['uniquePrimaryPlotCells'] for r in reports),nativeCellsNeverMultipliedByHypotheses=True,scope='Every immutable source report and native block retains complete comparisons and original raw target pointers. Index compression omits no property or contradictory cell.')


if __name__=='__main__':
    revision=int(sys.argv[1]) if len(sys.argv)>1 else 1
    result=analyze(revision,write=True);put(BASE/f'numeric-controls-v{revision}.json',result)
    print(json.dumps(dict(sources=len(result['sources']),uniquePrimaryPlotCells=result['uniquePrimaryPlotCells']),indent=2))
