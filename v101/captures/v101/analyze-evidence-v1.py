import csv
import json
import runpy
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
HELPERS = runpy.run_path(str(BASE / 'package-evidence-v1.py'))
ref, put = HELPERS['ref'], HELPERS['put']


def number(raw):
    try:
        return F(raw)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def verdict(codes, complete):
    if 'R' in codes:
        return 'REFUTED'
    return 'SUPPORTED' if complete and codes and all(c == 'S' for c in codes) else 'UNDECIDED'


def analyze(revision=1):
    inventory = json.loads((BASE / f'attempt-inventory-v{revision}.json').read_text())
    manifest = json.loads((ROOT / 'v101/bundle-manifest-v1.json').read_text())
    asset = manifest['sources'][0]
    mapping_path = ROOT / manifest['predictionMap']
    mapping = json.loads(mapping_path.read_text())
    recipe_path = ROOT / mapping['recipeFile']['path']
    recipes = json.loads(recipe_path.read_text())
    attempt = inventory['attempts'][0]
    source = attempt['source']
    block = dict(version='v1', sourceId=asset['sourceId'], sourceSha256=asset['sha256'], nativePrivateId=source['privateScriptId'], nativePrivateVersion=source['privateVersion'], sourcePlotOrdinals=asset['plots'], rows=[], ownedTitles=[], primaryRowOrdinals=[], testedRowOrdinals=[], completePrimaryCertificate=False)
    if attempt['sessions']:
        session = attempt['sessions'][0]
        raw = list(csv.reader((ROOT / session['csv']['path']).open(newline='')))
        headers, rows = raw[0], raw[1:]
        bindings = json.loads((ROOT / session['columnBindings']['path']).read_text())
        owned = {c['originalHeader'] for c in bindings['columns'] if c.get('sourceLiteralPlotOrdinal') is not None and c.get('owner') == source['privateScriptId'] and c['bindingStatus'] == 'OBSERVED'}
        selected = session['selectedPrimaryConsecutiveClosedRows']
        tested = selected if selected else session['eligibleDataRowOrdinals']
        block.update(csv=session['csv'], columnBindings=session['columnBindings'], closureMask=session['closureMask'], ownedTitles=sorted(owned), primaryRowOrdinals=selected, testedRowOrdinals=tested, completePrimaryCertificate=session['primaryInputCertificateValid'])
        for n in tested:
            cells = {}
            for title in ['time'] + [p['title'] for p in asset['plots']]:
                cells[title] = None if headers.count(title) != 1 else dict(csvSha256=session['csv']['sha256'], rowOrdinal=n, columnOrdinal=headers.index(title) + 1, headerRaw=title, valueRaw=rows[n - 1][headers.index(title)])
            block['rows'].append(dict(rowOrdinal=n, cells=cells, physicallyClosed=True, primaryScoringCredit=bool(block['completePrimaryCertificate'] and n in selected)))
    owned = set(block['ownedTitles'])
    complete = block['completePrimaryCertificate']
    columns = [p['title'] for p in asset['plots'][3:]]
    models = []
    for index, frozen in enumerate(mapping['models']):
        properties, all_codes = [], []
        for plot in frozen['expectedColumns']:
            title, expected = plot['title'], plot['expectedRawCode']
            comparisons = []
            for row in block['rows']:
                target = row['cells'][title]
                code = 'U' if title not in owned or target is None else 'S' if number(target['valueRaw']) == number(expected) else 'R'
                comparisons.append(dict(target=target, verdict=code, cause='Owned closed raw code differs from frozen integer, including present blank/unexpected code' if code == 'R' else 'Missing or ambiguous column ownership' if code == 'U' else None))
                all_codes.append(code)
            codes = [c['verdict'] for c in comparisons]
            properties.append(dict(sourcePlotOrdinal=plot['sourcePlotOrdinal'], title=title, expectedRawCode=expected, predictionPointer='/models/' + str(index) + '/expectedColumns/' + str(plot['sourcePlotOrdinal'] - 3), observedRawCounts=dict(Counter(c['target']['valueRaw'] for c in comparisons if c['target'] is not None)), comparisons=comparisons, verdict=verdict(codes, complete and len(codes) == 64), coverageCause=None if complete and title in owned else 'Full64-row owned/closed property certificate unavailable'))
        models.append(dict(modelId=frozen['modelId'], predictionMap=ref(mapping_path), predictionPointer='/models/' + str(index), recipeFile=ref(recipe_path), recipePointer='/models/' + str(next(i for i, r in enumerate(recipes['models']) if r['id'] == frozen['modelId'])), testedColumns=columns, allSourcePlotOrdinals=asset['plots'], properties=properties, comparisonCounts=dict(Counter(all_codes)), verdict=verdict(all_codes, complete and set(columns) <= owned), scope='Exact37-code frozen vector on this unchanged new source execution only'))
    supported = [m['modelId'] for m in models if m['verdict'] == 'SUPPORTED']
    undecided = [m['modelId'] for m in models if m['verdict'] == 'UNDECIDED']
    summary = ('ONLY_CM_A' if supported == ['CM-A'] else 'ONLY_CM_B' if supported == ['CM-B'] else 'MULTIPLE' if len(supported) > 1 else 'UNDECIDED' if undecided else 'NEITHER')
    reference = mapping['controlReference']
    old = list(csv.reader((ROOT / reference['csv']['path']).open(newline='')))
    prior_controls = []
    for plot in asset['plots'][3:39]:
        title = plot['title']
        col = old[0].index(title)
        old_pointer = dict(csvSha256=reference['csv']['sha256'], rowOrdinal=reference['referenceDataRowOrdinal'], columnOrdinal=col + 1, headerRaw=title, valueRaw=old[reference['referenceDataRowOrdinal']][col])
        comparisons = []
        for row in block['rows']:
            target = row['cells'][title]
            code = 'U' if title not in owned or target is None else 'S' if number(target['valueRaw']) == number(old_pointer['valueRaw']) else 'R'
            comparisons.append(dict(target=target, verdict=code))
        prior_controls.append(dict(sourcePlotOrdinal=plot['sourcePlotOrdinal'], title=title, priorReference=old_pointer, targets=comparisons, verdict=verdict([c['verdict'] for c in comparisons], complete and len(comparisons) == 64), priorReferenceScope='Provenance only; every actual target is from the new original v101 export'))
    prior_codes = [c['verdict'] for p in prior_controls for c in p['targets']]
    control_verdict = verdict(prior_codes, complete and len(prior_codes) == 64 * 36)
    contexts = []
    for plot in asset['plots'][:3]:
        title = plot['title']
        cells = [r['cells'][title] for r in block['rows']]
        available = title in owned and all(p is not None and number(p['valueRaw']) is not None for p in cells)
        values = [number(p['valueRaw']) for p in cells] if available else []
        if title == 'INPUT_INDEX':
            matches = available and all(v.denominator == 1 for v in values) and all(b == a + 1 for a, b in zip(values, values[1:]))
        elif title == 'INPUT_TIME':
            matches = available and all(number(r['cells'][title]['valueRaw']) == 1000 * number(r['cells']['time']['valueRaw']) for r in block['rows']) and all(b > a for a, b in zip(values, values[1:]))
        else:
            matches = available and all(v == 1 for v in values)
        contexts.append(dict(sourcePlotOrdinal=plot['sourcePlotOrdinal'], title=title, contract=mapping['contextPredictions'][plot['sourcePlotOrdinal']], targets=cells, verdict='REFUTED' if available and not matches else 'SUPPORTED' if complete and len(cells) == 64 and matches else 'UNDECIDED', physicalClosureRequiredIndependently=True))
    new_title = columns[-1]
    actual = [r['cells'][new_title] for r in block['rows'] if new_title in owned and r['cells'][new_title] is not None]
    single = {m['modelId']:next(p['verdict'] for p in m['properties'] if p['title'] == new_title) for m in models}
    return dict(version=f'v{revision}', source=source, nativeBlock=block, contextProperties=contexts, models=models, modelSummary=summary, supportedModelIds=supported, undecidedModelIds=undecided, discriminator=dict(title=new_title, observedRawCounts=dict(Counter(p['valueRaw'] for p in actual)), firstOwnedClosedCell=actual[0] if actual else None, perColumnVerdicts=single, scope='A contrary owned closed code refutes its numeric prediction even with partial coverage; full model support requires all37 columns and64 rows'), priorControls=prior_controls, priorControlVerdict=control_verdict, priorSurfaceExtrapolation='BOUNDED_REPEATED_CONTROLS_MATCH' if control_verdict == 'SUPPORTED' else 'HELD / changed or missing new controls', uniquePrimaryPlotCells=len(block['primaryRowOrdinals']) * len(owned) if complete else 0, uniquePrimaryColorCodeCells=len(block['primaryRowOrdinals']) * len(owned & set(columns)) if complete else 0, encodingLimit=mapping['encoding'], unobserved=['Hidden native alpha/storage/identity and Boolean-NA distinction', 'Generic equality, missing casts, gradients, unqueried inputs and universal algorithm identification', 'Independent editor marker arrays, native feed/execution IDs, actual backend calculation count and complete private script inventory'], scope='Frozen finite author hypotheses only; no native target supplied by models or old evidence, post-capture fit, tolerance, hidden-byte decoding, parity-credit multiplication or historical-hold closure')


if __name__ == '__main__':
    revision = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    result = analyze(revision)
    put(BASE / f'numeric-controls-v{revision}.json', result)
    print(json.dumps(dict(modelSummary=result['modelSummary'], discriminator=result['discriminator'], priorControlVerdict=result['priorControlVerdict']), indent=2))
