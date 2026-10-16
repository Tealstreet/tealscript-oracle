import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'v94/captures/v94'
CHANNELS = ['R', 'G', 'B', 'T', 'NA']
PACKINGS = {'nominal': F(1, 2), '127of255': F(127, 255), '128of255': F(128, 255)}
CONVERSIONS = ['identity', 'floor', 'nearest-half-up']


def reference(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def rational(value):
    return str(F(value))


def gradient(t, lower, upper, family, a1=None, conversion='identity'):
    t = min(F(1), max(F(0), F(t)))
    a0 = 1 - F(lower[3], 100)
    a1 = 1 - F(upper[3], 100) if a1 is None else a1
    a = (1 - t) * a0 + t * a1
    if family == 'S':
        rgb = [(1 - t) * l + t * u for l, u in zip(lower[:3], upper[:3])]
    else:
        rgb = [((1 - t) * a0 * l + t * a1 * u) / a if a else F(0) for l, u in zip(lower[:3], upper[:3])]
    if conversion == 'floor':
        rgb = [F(x.numerator // x.denominator) for x in rgb]
    if conversion == 'nearest-half-up':
        rgb = [F((x + F(1, 2)).numerator // (x + F(1, 2)).denominator) for x in rgb]
    return rgb + [100 * (1 - a), F(0)]


def analyze(limit=6):
    assets = json.loads((ROOT / 'v94/bundle-manifest-v1.json').read_text())['sources'][:limit]
    reports = []
    for asset in assets:
        directory = BASE / asset['id'] / 'attempt-v1'
        session = directory / 'session-mode0-v1'
        path = session / 'chart-native-v1.csv'
        csv_ref = reference(path)
        raw = list(csv.reader(path.open(newline='')))
        headers, rows = raw[0], raw[1:]
        columns = {h: i for i, h in enumerate(headers)}
        masks = list(csv.DictReader((session / 'row-closure-mask-v1.csv').open()))
        chosen, run = [], []
        for mask in masks:
            n = int(mask['row_ordinal'])
            row = rows[n - 1]
            finite = 'rsi' not in asset['id'] or (row[columns['RSI_NA']] == '0' and row[columns['RSI']] != '')
            if mask['closed_numeric_eligible'] != '1' or not finite:
                run = []
                continue
            if run and (n != run[-1] + 1 or F(row[0]) != F(rows[run[-1] - 1][0]) + 120):
                run = []
            run.append(n)
            if len(run) == 32:
                chosen = run
                break
        assert len(chosen) == 32, asset['id']
        counters, row_reports = {}, []

        def point(n, title):
            i = columns[title]
            return {'rowOrdinal': n, 'columnOrdinal': i + 1, 'headerRaw': headers[i], 'valueRaw': rows[n - 1][i]}

        def compare(model, group, values, predictions):
            verdicts = []
            for title, actual, expected in zip(group, values, predictions):
                verdict = 'SUPPORTED' if actual != '' and F(actual) == expected else 'REFUTED'
                key = model + '/' + title
                counters.setdefault(key, Counter())[verdict] += 1
                verdicts.append({'property': title, 'predictedRational': rational(expected), 'verdict': verdict})
            return {'model': model, 'properties': verdicts, 'tupleVerdict': 'SUPPORTED' if all(v['verdict'] == 'SUPPORTED' for v in verdicts) else 'REFUTED'}

        for n in chosen:
            row = dict(zip(headers, rows[n - 1]))
            entries, controls = [], {}
            if 'clamp' in asset['id']:
                for title, value in {'BELOW_X': -5, 'MIDDLE_X': 5, 'ABOVE_X': 15}.items():
                    controls[title] = F(value)
                for prefix, endpoint in [('LOWER', [0, 0, 0, 0]), ('UPPER', [100, 200, 50, 100])]:
                    controls.update({prefix + '_' + c: F(v) for c, v in zip(CHANNELS[:4], endpoint)})
                aliases = {'Below R': ('BELOW', 0), 'Middle G': ('MIDDLE', 1), 'Middle B': ('MIDDLE', 2), 'Middle T': ('MIDDLE', 3), 'Above R': ('ABOVE', 0), 'Above T': ('ABOVE', 3)}
                for family in ['S', 'P']:
                    predictions = {}
                    for prefix in ['BELOW', 'MIDDLE', 'ABOVE']:
                        expected = gradient(F(row[prefix + '_X']) / 10, [0, 0, 0, 0], [100, 200, 50, 100], family)
                        predictions[prefix] = expected
                        titles = [prefix + '_' + c for c in CHANNELS]
                        entries.append(compare(family, titles, [row[t] for t in titles], expected))
                    for title, (prefix, channel) in aliases.items():
                        entries.append(compare(family, [title], [row[title]], [predictions[prefix][channel]]))
            elif 'rsi' in asset['id']:
                for prefix, endpoint in [('LOWER', [255, 0, 0, 0]), ('UPPER', [0, 255, 0, 50])]:
                    controls.update({prefix + '_' + c: F(v) for c, v in zip(CHANNELS[:4], endpoint)})
                controls.update({'RSI_NA': F(0), 'Signal': F(row['RSI']), 'INPUT_CLOSE': F(row['close'])})
                t = F(row['RSI']) / 100
                sets = {'S': set(), 'P': set()}
                actual = tuple(F(row['RESULT_' + c]) if row['RESULT_' + c] else None for c in CHANNELS[:3])
                for family in ['S', 'P']:
                    for packing, a1 in PACKINGS.items():
                        for conversion in CONVERSIONS:
                            predicted = gradient(t, [255, 0, 0, 0], [0, 255, 0, 50], family, a1, conversion)
                            sets[family].add(tuple(predicted[:3]))
                            titles = ['RESULT_' + c for c in CHANNELS]
                            entries.append(compare(family + '/' + packing + '/' + conversion, titles, [row[t] for t in titles], predicted))
                discrimination = {'inputRsiRaw': row['RSI'], 'ratioFromRsiRational': rational(t), 'ratioColumnRaw': row['RATIO_UNCLAMPED'], 'ratioColumnBoundary': 'Retained independently; no assertion of infinite-precision division equality to the exported RSI string.', 'interior': 0 < t < 1, 'frozenRgbSetsDisjoint': sets['S'].isdisjoint(sets['P']), 'observedRgbMembership': {f: actual in values for f, values in sets.items()}, 'nativePresenceRaw': row['RESULT_NA'], 'precisionCause': None, 'scope': 'Frozen RGB-set discrimination only. T and NA are scored independently and may refute every full RGBA submodel.'}
            else:
                phase = int(row['PHASE'])
                x = [F(-1), F(0), F(1, 4), F(1, 2), F(3, 4), F(1), F(2)][phase]
                controls.update({'PHASE': F(int(row['INPUT_INDEX']) % 7), 'GRADIENT_X': x})
                endpoints = [('PARTIAL', [10, 20, 30, 40], [210, 120, 230, 80], 'PARTIAL_LOWER', 'PARTIAL_UPPER'), ('TRANSPARENT_LOWER', [10, 20, 30, 100], [210, 120, 230, 20], 'TRANSPARENT_LOWER_INPUT', 'TRANSPARENT_UPPER_INPUT'), ('OPAQUE', [10, 20, 30, 0], [210, 120, 230, 0], 'OPAQUE_LOWER', 'OPAQUE_UPPER')]
                for prefix, lower, upper, lp, up in endpoints:
                    for ep, values in [(lp, lower), (up, upper)]:
                        controls.update({ep + '_' + c: F(v) for c, v in zip(CHANNELS[:4], values)})
                    for family in ['S', 'P']:
                        titles = [prefix + '_' + c for c in CHANNELS]
                        entries.append(compare(family, titles, [row[t] for t in titles], gradient(F(row['GRADIENT_X']), lower, upper, family)))
            for title, value in controls.items():
                entries.append(compare('SOURCE_CONTROL', [title], [row[title]], [value]))
            titles = sorted({p['property'] for e in entries for p in e['properties']} | {'INPUT_TIME', 'INPUT_INDEX', 'CHART_CONFIRMED', 'time', 'close'})
            if 'rsi' in asset['id']:
                titles += ['RSI', 'RATIO_UNCLAMPED']
            record = {'rowOrdinal': n, 'timeRaw': row['time'], 'captureStatus': 'CAPTURED', 'closureStatus': 'INDEPENDENTLY_CLOSED', 'cells': [point(n, t) for t in titles], 'comparisons': entries}
            if 'rsi' in asset['id']:
                record['rgbDiscrimination'] = discrimination
            row_reports.append(record)
        summary = []
        for key, counts in sorted(counters.items()):
            model, title = key.rsplit('/', 1)
            summary.append({'model': model, 'property': title, 'captureStatus': 'CAPTURED', 'rowsCompared': sum(counts.values()), 'counts': dict(counts), 'verdict': 'REFUTED' if counts['REFUTED'] else 'SUPPORTED'})
        model_verdicts = {}
        for model in sorted({s['model'] for s in summary}):
            props = [s for s in summary if s['model'] == model]
            model_verdicts[model] = {'captureStatus': 'CAPTURED', 'verdict': 'REFUTED' if any(p['verdict'] == 'REFUTED' for p in props) else 'SUPPORTED', 'contraryCellComparisons': sum(p['counts'].get('REFUTED', 0) for p in props), 'scope': 'Only the explicit 32-row source-bound block and frozen predictions; no universal gradient or engine verdict.'}
        coverage = {'selectedDataRowOrdinals': chosen, 'consecutiveIndependentlyClosedRows': len(chosen), 'selectionRule': 'First naturally exported 32 consecutive independently closed rows; RSI additionally requires finite input, never filters result presence.', 'allCsvRowsRetained': True, 'otherRows': 'Original cells and independent closure retained; outside this explicit numeric comparison block; no sampling-completeness claim.'}
        if 'rsi' in asset['id']:
            coverage.update(distinctInteriorRatios=len({r['rgbDiscrimination']['ratioFromRsiRational'] for r in row_reports if r['rgbDiscrimination']['interior']}), separatingRatioRows=sum(r['rgbDiscrimination']['interior'] and r['rgbDiscrimination']['frozenRgbSetsDisjoint'] for r in row_reports), missingResultRows=sum(rows[n - 1][columns['RESULT_NA']] != '0' for n in chosen), rgbTupleMatches={m: sum(all(p['verdict'] == 'SUPPORTED' for p in e['properties'][:3]) for r in row_reports for e in r['comparisons'] if e['model'] == m) for m in model_verdicts if m != 'SOURCE_CONTROL'})
        if 'discriminators' in asset['id']:
            coverage['observedPhases'] = sorted({int(rows[n - 1][columns['PHASE']]) for n in chosen})
            assert coverage['observedPhases'] == list(range(7))
        reports.append({'sourceId': asset['id'], 'sourceSha256': asset['sha256'], 'requestedSource': 'v94/' + asset['path'], 'csv': csv_ref, 'columnBindings': reference(session / 'column-bindings-v1.json'), 'closureMask': reference(session / 'row-closure-mask-v1.csv'), 'coverage': coverage, 'propertyVerdicts': summary, 'modelVerdicts': model_verdicts, 'rows': row_reports})
    return {'version': 'v1', 'captureStatus': 'CAPTURED', 'comparisonPolicy': 'Exact rational predictions from original raw decimal strings; no tolerance, observed-cell rounding, fitted algorithm or transparency quantizer. RGB conversions and alpha packing remain separate frozen hypotheses.', 'precisionBoundary': 'SUPPORTED denotes equality for the captured exported strings under that explicitly named model, not recovery of hidden internal precision or an unbounded algorithm. Integer-scale contrary RGB/T/NA values remain observed refutations.', 'residualScope': ['No RSI seed/primitive or synthetic-harness equivalence claim', 'No engine approval or fixture promotion', 'No historical hold closure', 'No universal interpolation/gamma/raster claim'], 'sources': reports}


if __name__ == '__main__':
    result = analyze()
    print(json.dumps({r['sourceId']: {'coverage': r['coverage'], 'models': r['modelVerdicts']} for r in result['sources']}, indent=2))
