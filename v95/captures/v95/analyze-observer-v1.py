import csv
import hashlib
import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path('/Users/samuelsteady/cs/tealscript-oracle')


def ref(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def num(value):
    try:
        return F(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def analyze(source_id):
    directory = ROOT / 'v95/captures/v95' / source_id / 'attempt-v1'
    receipt = json.loads((directory / 'capture-receipt-v1.json').read_text())
    observer = receipt.get('observer')
    if observer is None:
        return {'version': 'v1', 'sourceId': source_id, 'item': 20, 'captureStatus': 'NOT OBSERVED / live observer', 'cause': receipt['status'], 'receipt': ref(directory / 'capture-receipt-v1.json'), 'eventCompleteness': False}
    base = directory / 'observer-window-v1'
    events = [json.loads(line) for line in (base / 'events-v1.jsonl').read_text().splitlines()]
    inspections = []
    for pointer in observer['sampleInspections']:
        path = ROOT / pointer['path']
        assert ref(path) == pointer
        inspection = json.loads(path.read_text())
        for name in ['csv', 'columnBindings', 'closureMask']:
            assert ref(ROOT / inspection[name]['path']) == inspection[name]
        inspections.append(inspection)
    facets = []
    records = []

    def criterion(name, observed, verdict='UNDECIDED', cause=None, details=None):
        facets.append({'facet': name, 'captureStatus': 'CAPTURED' if observed else 'NOT OBSERVED', 'hypothesisVerdict': verdict if observed else 'UNDECIDED', 'cause': cause, 'details': details})

    def record(inspection, target, prop, model, expected, inputs=(), scoring='LIVE_OBSERVER_EXCLUDED_FROM_CLOSED_SCORING'):
        pointers = target['nativeCellPointers']
        actual = num(target['valuesRaw'].get(prop))
        records.append({'property': prop, 'model': model, 'csv': inspection['csv'], 'nativeCell': pointers.get(prop), 'inputCells': [pointers.get(p) for p in inputs], 'predictedRational': str(expected) if expected is not None else None, 'actualValueRaw': target['valuesRaw'].get(prop), 'captureStatus': 'CAPTURED' if prop in pointers else 'NOT OBSERVED', 'verdict': 'UNDECIDED' if expected is None or prop not in pointers else 'SUPPORTED' if actual == expected else 'REFUTED', 'closedScoringEligible': scoring == 'CLOSED_BASELINE', 'scoringScope': scoring})

    if inspections:
        first = inspections[0]
        data = list(csv.reader((ROOT / first['csv']['path']).open(newline='')))
        headers, rows = data[0], data[1:]
        ordinals = first['first32ClosedBaselineDataRowOrdinals']
        criterion('First native export supplies32 independently closed baseline rows', len(ordinals) == 32, 'SUPPORTED', None if len(ordinals) == 32 else 'Original first export lacks32 source-bound closed rows', {'originalDataRowOrdinals': ordinals, 'csv': first['csv']})
        for n in ordinals:
            values = dict(zip(headers, rows[n - 1]))
            target = {'valuesRaw': values, 'nativeCellPointers': {h: {'rowOrdinal': n, 'columnOrdinal': i + 1, 'headerRaw': h, 'valueRaw': rows[n - 1][i]} for i, h in enumerate(headers)}}
            for prop in ['TICKS', 'UDT_STICKY', 'CHART_CONFIRMED']:
                record(first, target, prop, 'CLOSED_BASELINE_NATIVE_RELATIONSHIP', F(1), scoring='CLOSED_BASELINE')
            for prop, previous in [('COMMITTED_DELTA', 'PREVIOUS_COMMITTED'), ('UDT_DELTA', 'PREVIOUS_ORDINARY')]:
                if num(values.get(previous)) is not None:
                    record(first, target, prop, 'CLOSED_BASELINE_UNIT_COMMIT_DELTA', F(1), [previous], 'CLOSED_BASELINE')
                    current = 'COMMITTED' if prop == 'COMMITTED_DELTA' else 'UDT_ORDINARY'
                    record(first, target, current, 'CLOSED_BASELINE_PREVIOUS_COMMIT_PLUS_ONE', num(values[previous]) + 1, [previous], 'CLOSED_BASELINE')
            record(first, target, 'UDT_ORDINARY', 'CLOSED_BASELINE_EQUAL_ORDINARY_COUNTERS', num(values.get('COMMITTED')), ['COMMITTED'], 'CLOSED_BASELINE')
            record(first, target, 'SEEN_TIME', 'CLOSED_BASELINE_OWN_TIME_BINDING', num(values.get('INPUT_TIME')), ['INPUT_TIME'], 'CLOSED_BASELINE')
    else:
        criterion('First native export supplies32 independently closed baseline rows', False, cause='No native observer CSV was returned')

    open_tuples = []
    close_tuples = []
    next_tuples = []
    for inspection in inspections:
        for target in inspection['targetTuples']:
            classification = target['actualClassification']
            pair = (inspection, target)
            if classification == 'OPEN_REALTIME_SAMPLE':
                open_tuples.append(pair)
            elif classification == 'ACTUAL_CONFIRMED_REALTIME_CLOSE':
                close_tuples.append(pair)
            elif classification == 'NEXT_BAR_FIRST_FLAG_OBSERVED':
                next_tuples.append(pair)
            for prop, previous in [('COMMITTED_DELTA', 'PREVIOUS_COMMITTED'), ('UDT_DELTA', 'PREVIOUS_ORDINARY')]:
                if num(target['valuesRaw'].get(previous)) is not None:
                    record(inspection, target, prop, 'OBSERVED_TUPLE_UNIT_COMMIT_DELTA', F(1), [previous])
                    current = 'COMMITTED' if prop == 'COMMITTED_DELTA' else 'UDT_ORDINARY'
                    record(inspection, target, current, 'OBSERVED_TUPLE_PREVIOUS_COMMIT_PLUS_ONE', num(target['valuesRaw'][previous]) + 1, [previous])
            record(inspection, target, 'UDT_STICKY', 'OBSERVED_TUPLE_STICKY_EQUALS_TICKS', num(target['valuesRaw'].get('TICKS')), ['TICKS'])
            record(inspection, target, 'SEEN_TIME', 'OBSERVED_TUPLE_OWN_TIME_BINDING', num(target['valuesRaw'].get('INPUT_TIME')), ['INPUT_TIME'])

    recalc = any(e['eventKind'] in ['RECALCULATION_OR_HISTORICAL_WITNESS_CHANGE', 'COUNTER_DROP_OR_RECALCULATION_WITNESS', 'UI_CSV_COUNTER_MISMATCH_OR_RECALCULATION_WITNESS'] for e in events)
    stable = bool(inspections) and all(i['historicalClockWitnesses'] == inspections[0]['historicalClockWitnesses'] for i in inspections)
    bound = all(i['requiredGetterBindingStatus'] == 'CAPTURED' and i['sourceId'] == source_id and i['privateId'] == receipt['privateId'] for i in inspections)
    clocks = [num(t['valuesRaw'].get('CLOCK')) for _, t in open_tuples]
    distinct = len(clocks) >= 2 and all(x is not None for x in clocks) and all(b > a for a, b in zip(clocks, clocks[1:]))
    same_key = len({t['valuesRaw'].get('INPUT_TIME') for _, t in open_tuples + close_tuples}) == 1
    close_clock = num(close_tuples[-1][1]['valuesRaw'].get('CLOCK')) if close_tuples else None
    actual_close = close_clock is not None and distinct and close_clock >= clocks[-1]
    continuity = bool(inspections) and stable and bound and not recalc
    enough = distinct and same_key and actual_close and continuity
    details = {'distinctAdvancingOpenSamples': len(open_tuples), 'actualRealtimeCloseSamples': len(close_tuples), 'sameKey': same_key, 'historicalClockWitnessesUnchanged': stable, 'recalculationOrWitnessChangeObserved': recalc, 'unchangedPrivateVersionSourceOwnership': bound, 'nativeExecutionIdentity': None, 'nativeExecutionIdentityStatus': 'UNOBSERVED', 'interveningExecutionCountAndSequence': 'UNOBSERVED'}
    criterion('Compatible unchanged same-source sampled-update and actual-close context', enough, 'SUPPORTED', None if enough else 'Requires at least2 advancing open clocks, actual later same-key realtime close, source ownership and no contradictory recalculation witness', details)
    if enough:
        ordinary_finite = all(num(t['valuesRaw'].get(p)) is not None for _, t in open_tuples for p in ['COMMITTED', 'UDT_ORDINARY'])
        ordinary_equal = ordinary_finite and all(num(t['valuesRaw'].get('COMMITTED')) == num(open_tuples[0][1]['valuesRaw'].get('COMMITTED')) and num(t['valuesRaw'].get('UDT_ORDINARY')) == num(open_tuples[0][1]['valuesRaw'].get('UDT_ORDINARY')) for _, t in open_tuples)
        ticks = [num(t['valuesRaw'].get('TICKS')) for _, t in open_tuples]
        sticky = [num(t['valuesRaw'].get('UDT_STICKY')) for _, t in open_tuples]
        growth = all(x is not None for x in ticks + sticky) and ticks == sticky and all(b > a for a, b in zip(ticks, ticks[1:]))
        criterion('Ordinary counters roll back between genuine sampled same-key updates', True, 'SUPPORTED' if ordinary_equal else 'REFUTED', details=details)
        criterion('Varip and UDT sticky agree and increase between sampled same-key updates', True, 'SUPPORTED' if growth else 'REFUTED', details={**details, 'ticksRational': [str(x) if x is not None else None for x in ticks], 'stickyRational': [str(x) if x is not None else None for x in sticky]})
    else:
        for name in ['Ordinary counters roll back between genuine sampled same-key updates', 'Varip and UDT sticky agree and increase between sampled same-key updates']:
            criterion(name, False, cause='Sampled native values remain observed; full live context/continuity criterion is not met', details=details)
    next_ok = bool(next_tuples) and continuity
    reset = next_ok and all(num(t['valuesRaw'].get('TICKS')) == 1 and num(t['valuesRaw'].get('UDT_STICKY')) == 1 for _, t in next_tuples)
    criterion('Next-bar first-execution sticky reset', next_ok, 'SUPPORTED' if reset else 'REFUTED', None if next_ok else 'Actual source-bound realtime IS_NEW1 first event not captured with compatible continuity; later values do not substitute')
    return {'version': 'v1', 'sourceId': source_id, 'item': 20, 'sourceSha256': receipt['sourceSha256'], 'captureStatus': 'FINITE NATIVE OBSERVATIONS WITH EXPLICIT FACET VERDICTS', 'receipt': ref(directory / 'capture-receipt-v1.json'), 'declaration': ref(base / 'declaration-v1.json') if (base / 'declaration-v1.json').exists() else None, 'eventLog': ref(base / 'events-v1.jsonl'), 'sampleInspections': observer['sampleInspections'], 'facets': facets, 'records': records, 'comparisonCounts': dict(Counter(r['verdict'] for r in records)), 'sourceSessions': 1, 'sourceSessionScope': observer['sourceSessionScope'], 'actualNativeCalculationSessionCount': None, 'exports': observer['exports'], 'inspectedCsvs': len(inspections), 'exportAttemptSlots': observer['exportAttempts'], 'observerTerminationCause': observer['endCause'], 'nativeExecutionIdentity': None, 'eventCompleteness': False, 'uiCsvSameExecution': None, 'scope': 'Fresh same-source sampled relationships only. No original MTF as-of inputs, historical clock recovery, exact intervening tick count or generic live parity.'}


if __name__ == '__main__':
    print(json.dumps(analyze(sys.argv[1]), indent=2))
