import csv
import json
import runpy
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
HELPERS = runpy.run_path(str(BASE / 'package-evidence-v1.py'))
ref, put, number = HELPERS['ref'], HELPERS['put'], HELPERS['number']


def status(codes, complete):
    if 'R' in codes:
        return 'REFUTED'
    return 'SUPPORTED' if complete and len(codes) == 32 and set(codes) == {'S'} else 'UNDECIDED'


def expected(contract, row, anchor_index):
    rule, title = contract['rule'], contract['title']
    own = number(row['INPUT_INDEX'])
    phase = int(own % 8)
    if rule == 'BUILD_EVENT':
        return contract['prediction'] if own == anchor_index else ''
    if rule == 'CONSTANT':
        return contract['prediction']
    if rule in ['PHASE_FORMULA', 'OFFSET_POLICY']:
        return contract['prediction'][phase]
    if rule == 'MOD32_FORMULA':
        return contract['prediction'][int(own % 32)]
    if rule == 'UNIQUE_BUILD_MARKER':
        return str(anchor_index) if own == anchor_index and title == 'VISUAL_ANCHOR_INDEX' else row['INPUT_TIME'] if own == anchor_index else ''
    if title == 'CASE_ID':
        return str(phase)
    if title == 'INPUT_TIME':
        return str(number(row['time']) * 1000)
    if title == 'CHART_CONFIRMED':
        return '1'
    return None


def analyze(revision=1, write=False):
    inventory = json.loads((BASE / f'attempt-inventory-v{revision}.json').read_text())
    manifest = json.loads((ROOT / 'v103/bundle-manifest-v1.json').read_text())
    contracts_path = BASE / 'numeric-contracts-v1.json'
    contracts = json.loads(contracts_path.read_text())
    entries = []
    for attempt in inventory['attempts']:
        source = attempt['source']
        asset = next(a for a in manifest['sources'] if a['sourceId'] == source['sourceId'])
        frozen = next(a for a in contracts['sources'] if a['sourceId'] == source['sourceId'])
        directory = BASE / asset['sourceId']
        session = attempt['sessions'][0] if attempt['sessions'] else None
        block = dict(version='v1', sourceId=asset['sourceId'], sourceSha256=asset['sha256'], sourceObservation=ref(directory/'attempt-v1/observation-v1.json'), nativePrivateId=source['privateScriptId'], nativePrivateVersion=source['privateVersion'], rows=[], predecessors=[], visualAnchor=None, primaryCertificate=False, ownedTitles=[], primaryScoringCells=0)
        if session:
            raw = list(csv.reader((ROOT / session['csv']['path']).open(newline='')))
            headers, data = raw[0], raw[1:]
            bindings = json.loads((ROOT/session['columnBindings']['path']).read_text())
            owned = {c['originalHeader'] for c in bindings['columns'] if c.get('sourceLiteralPlotOrdinal') is not None and c['bindingStatus']=='OBSERVED' and c['owner']==source['privateScriptId']}
            def point(n, title):
                if headers.count(title) != 1:
                    return None
                c = headers.index(title)
                return dict(csvSha256=session['csv']['sha256'], rowOrdinal=n, columnOrdinal=c+1, headerRaw=title, valueRaw=data[n-1][c])
            def row_record(n):
                return dict(rowOrdinal=n, chartTime=point(n,'time'), cells={p['title']:point(n,p['title']) for p in asset['plots']})
            block.update(csv=session['csv'], rowSet=ref(Path(ROOT/session['sessionReceipt']['path']).parent/'row-set-observation-v1.json'), columnBindings=session['columnBindings'], closureMask=session['closureMask'], primaryCertificate=session['primaryInputCertificateValid'], ownedTitles=sorted(owned), rows=[row_record(n) for n in session['selectedPrimaryClosedRowOrdinals']], predecessors=[row_record(n) for n in session['originalClosedPredecessorRowOrdinals']])
            anchor = session['uniqueVisualAnchorRowOrdinal']
            block['visualAnchor'] = row_record(anchor) if anchor is not None else None
            block['primaryScoringCells'] = len(block['rows'])*len(owned) if block['primaryCertificate'] else 0
        block_path = directory/'native-cell-block-v1.json'
        if write:
            put(block_path, block)
        block_ref = ref(block_path) if block_path.exists() else None
        properties, alternatives = [], []
        anchor_index = number(block['visualAnchor']['cells']['INPUT_INDEX']['valueRaw']) if block['visualAnchor'] else None
        for contract in frozen['contracts']:
            title = contract['title']
            comparisons = []
            for row in block['rows']:
                context = {t:p['valueRaw'] for t,p in row['cells'].items() if p is not None}
                context['time'] = row['chartTime']['valueRaw']
                prediction = expected(contract, context, anchor_index)
                actual = row['cells'].get(title)
                code = 'U' if actual is None or title not in block['ownedTitles'] else 'S' if title=='INPUT_INDEX' and block['primaryCertificate'] else 'U' if prediction is None else 'S' if (actual['valueRaw']=='' if prediction=='' else number(actual['valueRaw'])==number(prediction)) else 'R'
                comparisons.append(dict(rowOrdinal=row['rowOrdinal'], expectedRaw=prediction, actual=actual, comparison=code, scope='Owned consecutive input context only; no absolute-index replay parity' if title=='INPUT_INDEX' else contract.get('primaryMeaning','Finite source formula/control; no pixel credit')))
            codes = [r['comparison'] for r in comparisons]
            prop = dict(title=title, sourcePlotOrdinal=contract['sourcePlotOrdinal'], rule=contract['rule'], frozenContract=contract, verdict=status(codes,block['primaryCertificate']), comparisonCounts=dict(Counter(codes)), comparisonRows=comparisons, nativeBlock=block_ref, observedRawCounts=dict(Counter(r['actual']['valueRaw'] for r in comparisons if r['actual'])), buildEventObservations=1 if contract['rule']=='BUILD_EVENT' and block['primaryCertificate'] and title in block['ownedTitles'] else 0, intentionalPrimaryBlanks=31 if contract['rule']=='BUILD_EVENT' and block['primaryCertificate'] else None)
            properties.append(prop)
            if contract['rule']=='OFFSET_POLICY':
                variants=[]
                for name,values in [('SOURCE_SERIES',contract['prediction']),('SCREEN_ALIGNED',contract['alternativeScreenAligned'])]:
                    rows=[]
                    for row in block['rows']:
                        own=number(row['cells']['INPUT_INDEX']['valueRaw']);actual=row['cells'].get(title);prediction=values[int(own%8)]
                        code='U' if actual is None or title not in block['ownedTitles'] else 'S' if (actual['valueRaw']=='' if prediction=='' else number(actual['valueRaw'])==number(prediction)) else 'R'
                        rows.append(dict(rowOrdinal=row['rowOrdinal'],actual=actual,expectedRaw=prediction,comparison=code))
                    variants.append(dict(id=name,verdict=status([r['comparison'] for r in rows],block['primaryCertificate']),comparisons=rows))
                alternatives.append(dict(title=title,variants=variants,supportedVariantIds=[v['id'] for v in variants if v['verdict']=='SUPPORTED'],scope='CSV export policy only; no screen displacement from raw values'))
        report=dict(version='v1',sourceId=asset['sourceId'],sourceSha256=asset['sha256'],sourceObservation=source,nativeBlock=block_ref,frozenContracts=ref(contracts_path),properties=properties,numericAlternatives=alternatives,primaryInputCertificate=block['primaryCertificate'],uniquePrimaryPlotCells=block['primaryScoringCells'],scope='Build getters:31 intentional blanks and1 event, never32 independent getter observations. Context/intent/blank cells are counted once; absent sources receive no native credit. Visual models and maps are independent.')
        path=directory/'numeric-results-v1.json'
        if write:
            put(path,report)
        entries.append(dict(sourceId=asset['sourceId'],report=ref(path) if path.exists() else None,uniquePrimaryPlotCells=report['uniquePrimaryPlotCells'],propertyVerdicts=dict(Counter(p['verdict'] for p in properties))))
    return dict(version=f'v{revision}',sources=entries,uniquePrimaryPlotCells=sum(e['uniquePrimaryPlotCells'] for e in entries),maximumProspectiveCells=9600,scope='Unique requested primary plot cells including context, intent and intentional blanks; models and transports never multiply credit')


if __name__ == '__main__':
    revision=int(sys.argv[1])
    result=analyze(revision,write=True)
    put(BASE/f'numeric-controls-v{revision}.json',result)
    print(json.dumps(dict(sources=len(result['sources']),uniquePrimaryPlotCells=result['uniquePrimaryPlotCells'])))
