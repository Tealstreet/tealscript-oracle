import csv
import json
import runpy
import sys
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
OLD = ROOT / 'v95/captures/v95'
OldContext = runpy.run_path(str(OLD / 'analyze-evidence-v1.py'))['Context']


def number(value):
    try:
        return F(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def exact_short_dyadic(value):
    if value is None:
        return True
    d = value.denominator
    if d & (d - 1) or abs(value.numerator).bit_length() > 53:
        return False
    k = d.bit_length() - 1
    decimal = str(abs(value.numerator) * 5 ** k).rstrip('0') or '0'
    return len(decimal) <= 16


def recurrence(inputs, alpha, seed, gates=None):
    state, finite, output, guards = None, [], [], []
    valid = True
    for i, x in enumerate(inputs):
        if gates is not None and not gates[i]:
            output.append(None)
            guards.append(valid)
            continue
        if x is not None:
            if state is None:
                finite.append(x)
                if seed == 'FIRST_FINITE':
                    state = x
                elif len(finite) >= 3:
                    state = sum(finite[-3:]) / 3
                valid = valid and exact_short_dyadic(state)
            else:
                intermediates = [state * (1 - alpha), x * alpha, state * (1 - alpha) + x * alpha]
                state = intermediates[-1]
                valid = valid and all(exact_short_dyadic(v) for v in intermediates)
        output.append(state)
        guards.append(valid)
    return output, guards


class Context(OldContext):
    def __init__(self, asset, source, session):
        self.asset = {**asset, 'id': source['sourceId'], 'item': asset['v95Item']}
        self.source, self.session = source, session
        self.path = ROOT / session['csv']['path']
        raw = list(csv.reader(self.path.open(newline='')))
        self.headers, self.data = raw[0], raw[1:]
        self.columns = {h: i for i, h in enumerate(self.headers)}
        self.rows = {n: dict(zip(self.headers, r)) for n, r in enumerate(self.data, 1)}
        self.closed = list(session['eligibleDataRowOrdinals'])
        self.by_index = {int(self.rows[n]['INPUT_INDEX']): n for n in self.closed}
        self.records, self.facets = [], []
        self.block = session['primaryModelDataRowOrdinals']

    def dependency(self, record, n, titles):
        record['completePriorInputBlock'] = {'csvSha256': self.session['csv']['sha256'], 'firstDataRowOrdinal': 1, 'lastDataRowOrdinal': n, 'ownIndexRange': [0, n - 1], 'columns': [{'columnOrdinal': self.columns[t] + 1, 'headerRaw': t} for t in titles], 'scope': 'All original rows in this same source/session, no exported output is used as a seed'}
        return record

    def model(self, n, title, name, expected, exact, inputs):
        r = self.record(n, title, name, expected, expected_blank=expected is None, precision='EXACT_INTEGER_OR_BINARY_FRACTION' if exact else 'EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION')
        r['precisionCause'] = None if exact else 'Independent rational candidate has unresolved native binary arithmetic/export precision; discrepancies remain UNDECIDED without tolerance or fitting'
        self.dependency(r, n, inputs)
        return r


def conditional(c):
    xs = [F(c.rows[n]['X']) for n in c.block]
    gates = [c.rows[n]['GATE'] == '1' for n in c.block]
    predictions = {}
    for seed in ['FIRST_FINITE', 'SMA3_FINITE']:
        predictions[('EMA_ALL', seed)] = recurrence(xs, F(1, 2), seed)
        for clock, enabled in [('GATED_CALL_CLOCK', gates), ('EVERY_CHART_BAR_CLOCK', None)]:
            values, guards = recurrence(xs, F(1, 2), seed, enabled)
            if enabled is None:
                values = [v if gates[i] else None for i, v in enumerate(values)]
            predictions[('EMA_BRANCH', seed + '/' + clock)] = values, guards
    finite_calls, discriminators = [], []
    for i, n in enumerate(c.block):
        row = c.rows[n]
        c.record(n, 'X', 'DECLARED_INTEGER_INPUT', F((n - 1) % 11 - 5), input_titles=['INPUT_INDEX'])
        c.record(n, 'GATE', 'DECLARED_PHASE_GATE', F((n - 1) % 16 % 3 != 0), input_titles=['PHASE'])
        if gates[i]:
            finite_calls.append(i)
        for (title, model), (values, guards) in predictions.items():
            c.model(n, title, 'EMA3_ALPHA_1_2/' + model, values[i], guards[i], ['X', 'GATE'])
            if title == 'EMA_BRANCH':
                c.record(n, 'BRANCH_EMA_NA', 'EMA3_SEED_AND_CLOCK_PRESENCE/' + model, F(values[i] is None), input_titles=['GATE'])
        a = predictions[('EMA_BRANCH', 'FIRST_FINITE/GATED_CALL_CLOCK')][0][i]
        b = predictions[('EMA_BRANCH', 'FIRST_FINITE/EVERY_CHART_BAR_CLOCK')][0][i]
        if gates[i] and number(row['EMA_BRANCH']) is not None and row['BRANCH_EMA_NA'] == '0' and a is not None and b is not None and a != b:
            discriminators.append(n)
        for title, expected, blank in [('BRANCH_EMA_NA', F(not gates[i]), False), ('SMA_BRANCH', sum(xs[j] for j in finite_calls[-3:]) / 3 if gates[i] and len(finite_calls) >= 3 else None, not gates[i] or len(finite_calls) < 3), ('SMA_ALL', sum(xs[max(0, i - 2):i + 1]) / 3 if i >= 2 else None, i < 2)]:
            if title == 'BRANCH_EMA_NA' and gates[i]:
                expected = F(0)
            name = 'FIRST_FINITE_SEED_BRANCH_PRESENCE_CANDIDATE' if title == 'BRANCH_EMA_NA' else 'FROZEN_CLOCK_AND_MASK_CONTROL'
            r = c.record(n, title, name, expected, expected_blank=blank, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION' if expected is not None and expected.denominator != 1 else 'EXACT_INTEGER_OR_BINARY_FRACTION')
            c.dependency(r, n, ['X', 'GATE'])
        c.record(n, 'BRANCH_SMA_NA', 'FROZEN_SMA_SEED_OR_GATE_MASK', F(not gates[i] or len(finite_calls) < 3), input_titles=['GATE'])
    c.criterion('At least three finite gated first-seed clock discriminators from own first call', len(discriminators) >= 3, 'SUPPORTED', None if len(discriminators) >= 3 else 'Insufficient frozen-candidate discrimination', {'dataRowOrdinals': discriminators, 'scope': 'Candidate distinctions are fixed before inspecting native targets; individual numeric precision guards remain separate'})


def recursive(c):
    inputs = {title: [number(c.rows[n][title]) for n in c.block] for title in ['CLEAN', 'X']}
    for family, alpha in [('EMA', F(1, 2)), ('RMA', F(1, 3))]:
        for source, suffix in [('CLEAN', 'CLEAN'), ('X', 'HOLE')]:
            title = family + '_' + suffix
            for seed in ['FIRST_FINITE', 'SMA3_FINITE']:
                values, guards = recurrence(inputs[source], alpha, seed)
                poisoned = False
                for i, n in enumerate(c.block):
                    value = values[i]
                    c.model(n, title, family + '3/' + seed + '/SKIP_MISSING_OBSERVATIONS', value, guards[i], [source])
                    c.model(n, title, family + '3/' + seed + '/MISSING_SLOT_OUTPUT_MASK', None if inputs[source][i] is None else value, guards[i], [source])
                    poisoned = poisoned or inputs[source][i] is None
                    c.model(n, title, family + '3/' + seed + '/POISON_AFTER_MISSING_INPUT', None if poisoned else value, guards[i], [source])
                    if suffix == 'HOLE':
                        c.record(n, family + '_HOLE_NA', family + '3/' + seed + '/SKIP_MISSING_NA_MASK', F(value is None), input_titles=['X_NA'])
    for n in c.block:
        i, row = n - 1, c.rows[n]
        hole = i < 3 or i % 64 in [12, 13, 32, 33, 34]
        c.record(n, 'CLEAN', 'DECLARED_CLEAN_INTEGER_INPUT', F(i % 11 - 5), input_titles=['INPUT_INDEX'])
        c.record(n, 'CYCLE', 'DECLARED_CYCLE64', F(i % 64), input_titles=['INPUT_INDEX'])
        c.record(n, 'X_NA', 'LEADING_AND_INTERIOR_HOLE_MASK', F(hole), input_titles=['INPUT_INDEX', 'CYCLE'])
        c.record(n, 'X', 'LEADING_AND_INTERIOR_HOLE_INPUT', F(i % 11 - 5) if not hole else None, expected_blank=hole, input_titles=['CLEAN', 'X_NA'])
        for family in ['EMA', 'RMA', 'RSI', 'TSI']:
            c.record(n, family + '_HOLE_NA', 'ACTUAL_NATIVE_TARGET_NA_WITNESS', F(row[family + '_HOLE'] == ''), input_titles=[family + '_HOLE'])
    c.criterion('RSI3 and TSI3/5 native trajectories remain independent targets', True, 'UNDECIDED', 'Complete own input vectors and masks are observed; an EMA candidate agreement does not certify RSI/TSI algorithms')
    c.criterion('Generic consume-slot arithmetic beyond the explicit missing-slot output-mask candidate', False, cause='No replacement value or repair/seed rule is prescribed for a missing arithmetic operand; no post-capture recurrence is fitted')


def implicit(c):
    runpy.run_path(str(OLD / 'analyze-item5-v1.py'))['analyze'](c)
    trs = []
    for n in c.block:
        row = c.rows[n]
        h, l = F(row['INPUT_HIGH']), F(row['INPUT_LOW'])
        previous = F(c.rows[n - 1]['INPUT_CLOSE']) if n > 1 else None
        tr = h - l if previous is None else max(h - l, abs(h - previous), abs(l - previous))
        trs.append(tr)
        if n == 1:
            c.record(n, 'TR', 'FIRST_BAR_HIGH_MINUS_LOW', tr, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['INPUT_HIGH', 'INPUT_LOW'])
    for seed in ['FIRST_FINITE', 'SMA3_FINITE']:
        values, guards = recurrence(trs, F(1, 3), seed)
        for i, n in enumerate(c.block):
            c.model(n, 'ATR', 'ATR3_RMA_ALPHA_1_3/' + seed, values[i], False, ['INPUT_OPEN', 'INPUT_HIGH', 'INPUT_LOW', 'INPUT_CLOSE'])
            c.record(n, 'ATR_NA', 'ATR3_SEED_MASK/' + seed, F(values[i] is None), input_titles=['INPUT_INDEX'])


def analyze(revision):
    inventory = json.loads((BASE / f'attempt-inventory-v{revision}.json').read_text())
    assets = {a['id']: a for a in json.loads((ROOT / 'v97/bundle-manifest-v1.json').read_text())['sources']}
    reports = []
    for attempt in inventory['attempts']:
        source = attempt['source']
        if not attempt['sessions']:
            reports.append({'sourceId': source['sourceId'], 'sourceSha256': source['sourceSha256'], 'captureStatus': 'NOT OBSERVED / native numeric export', 'nativeAdmission': attempt['status'], 'facets': [{'facet': 'Own index-zero prefix/startup', 'captureStatus': 'NOT OBSERVED', 'hypothesisVerdict': 'UNDECIDED', 'cause': attempt['status']}], 'records': []})
            continue
        session = attempt['sessions'][attempt['selectedFinalSession']]
        c = Context(assets[source['originalSourceId']], source, session)
        c.criterion('One original source-owned complete index-zero export with independently closed0..127', bool(c.block), 'SUPPORTED', None if c.block else '; '.join(session['prefixFailureCauses']), {'frontier': session['frontier'], 'primaryDataRowOrdinals': c.block})
        for n in c.block:
            for title in [p['title'] for p in c.asset['plotColumns']]:
                c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Original native target/control string; hypothesis comparisons are separate')
        item = source['item']
        if c.block:
            if item == 2:
                conditional(c)
            elif item == 4:
                recursive(c)
            elif item == 5:
                implicit(c)
            else:
                runpy.run_path(str(OLD / f'analyze-item{item}-v1.py'))['analyze'](c)
            if item == 3:
                for n in c.block:
                    i = n - 1
                    if i % 16 >= 5:
                        c.record(n, 'LOCAL_FIRST', 'REINITIALIZE_EACH_PHASE_BLOCK', F(i - i % 16 + 5), input_titles=['INPUT_INDEX', 'PHASE'])
                        c.record(n, 'LOCAL_FIRST', 'REINITIALIZE_EACH_VISIT', F(i), input_titles=['INPUT_INDEX'])
            if item == 10:
                c.record(1, 'FIXNAN', 'OWN_FIRST_INPUT_MISSING_FIXNAN', expected_blank=True, input_titles=['X', 'X_NA'])
                c.record(1, 'FIXNAN_NA', 'OWN_FIRST_INPUT_MISSING_FIXNAN', F(1), input_titles=['X_NA'])
        result = c.output()
        result.update(originalSourceId=source['originalSourceId'], selectedFinalSession=attempt['selectedFinalSession'], earlierSessionsNeverStitched=True, sourceFrontier=session['frontier'], allOriginalRowsRetained=True, selectedBlockOwnIndices=[0, 127], scope='Fresh exact v95 source/private version in v97 only; primary models use independently certified same-source indices0..127. All later native rows remain archived, without old-frontier, live execution, PRNG algorithm, universal parity or engine approval.')
        vector_summary = []
        for title in [p['title'] for p in c.asset['plotColumns']]:
            finite = [n for n in c.closed if c.rows[n][title] != '']
            vector_summary.append({'property': title, 'firstFiniteClosedCell': c.pointer(finite[0], title) if finite else None, 'firstFiniteOwnIndex': c.rows[finite[0]]['INPUT_INDEX'] if finite else None, 'primary128BlankOwnIndices': [n - 1 for n in c.block if c.rows[n][title] == ''], 'scope': 'Original raw vector/presence summary, not a predicted algorithm'})
        result['nativeVectorPresenceSummary'] = vector_summary
        if item == 5 and c.block:
            transitions = []
            closed_set = set(c.closed)
            for n in c.closed:
                if n <= 1 or n - 1 not in closed_set:
                    continue
                a, b = number(c.rows[n - 1]['DIRECTION']), number(c.rows[n]['DIRECTION'])
                if a is not None and b is not None and a != b:
                    transitions.append({'previous': c.pointer(n - 1, 'DIRECTION'), 'current': c.pointer(n, 'DIRECTION'), 'completePriorOhlcInputs': {'csvSha256': session['csv']['sha256'], 'firstDataRowOrdinal': 1, 'lastDataRowOrdinal': n, 'columns': [{'columnOrdinal': c.columns[t] + 1, 'headerRaw': t} for t in ['INPUT_OPEN', 'INPUT_HIGH', 'INPUT_LOW', 'INPUT_CLOSE']]}, 'scope': 'Every observed closed-vector direction transition, with all preceding own OHLC archived; no later fitted model block'})
            result['allClosedDirectionTransitions'] = transitions
        reports.append(result)
    return {'version': f'v{revision}', 'requestCommit': inventory['requestCommit'], 'inventory': f'attempt-inventory-v{revision}.json', 'precisionPolicy': 'Exact source integers and short dyadic candidates require representable intermediates and at most16 significant decimal digits; unresolved native arithmetic/export residues stay UNDECIDED. No tolerance, output-derived seed, binary64 decoding, rounding fit or normalization.', 'sourcePrefixPolicy': 'Only the selected single original final CSV may certify a complete own prefix; all earlier diagnostic exports remain separate. Present excluded cells and contrary masks are retained.', 'sources': reports}
