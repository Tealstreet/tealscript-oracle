from fractions import Fraction as F


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Own index-zero prefix for recursive EMA startup/first-call seed', prefix, 'UNDECIDED', None if prefix else 'The own index-zero input rows are absent; no seed reconstructed from suffix outputs')
    gated_seen = []
    discriminating = []
    for n in c.closed:
        row = c.rows[n]
        if row['GATE'] == '1':
            gated_seen.append(n)
        if n not in c.block:
            continue
        phase, index = int(row['PHASE']), int(row['INPUT_INDEX'])
        c.record(n, 'X', 'DECLARED_INTEGER_INPUT', F(index % 11 - 5), input_titles=['INPUT_INDEX'])
        c.record(n, 'GATE', 'DECLARED_GATE', F(phase % 3 != 0), input_titles=['PHASE'])
        for title in ['EMA_ALL', 'EMA_BRANCH']:
            record = c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Recursive seed/prefix remains independent of a suffix value')
            record.update(closedScoringEligible=prefix, exclusionCause=None if prefix else 'OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED')
        if row['GATE'] == '0':
            for title in ['SMA_BRANCH', 'EMA_BRANCH']:
                c.record(n, title, 'EXPLICIT_GATE0_MASK', expected_blank=True, input_titles=['GATE'])
            for title in ['BRANCH_SMA_NA', 'BRANCH_EMA_NA']:
                c.record(n, title, 'EXPLICIT_GATE0_NA_WITNESS', F(1), input_titles=['GATE'])
            continue
        if len(gated_seen) < 3:
            continue
        branch_deps = gated_seen[-3:]
        chart_deps = [c.by_index.get(index - k) for k in range(2, -1, -1)]
        if any(p is None for p in chart_deps):
            continue
        branch = sum(F(c.rows[p]['X']) for p in branch_deps) / 3
        chart = sum(F(c.rows[p]['X']) for p in chart_deps) / 3
        if branch != chart:
            discriminating.append(n)
        for model, expected, deps in [('GATED_CALL_CLOCK', branch, branch_deps), ('EVERY_CHART_BAR_CLOCK', chart, chart_deps)]:
            precision = 'EXACT_INTEGER_OR_BINARY_FRACTION' if expected.denominator == 1 else 'EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION'
            r = c.record(n, 'SMA_BRANCH', model, expected, precision=precision, input_titles=['GATE', 'X'])
            r['dependencyCells'] = [c.pointer(p, 'X') for p in deps]
        precision = 'EXACT_INTEGER_OR_BINARY_FRACTION' if chart.denominator == 1 else 'EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION'
        r = c.record(n, 'SMA_ALL', 'UNCONDITIONAL_LAST3_CONTROL', chart, precision=precision)
        r['dependencyCells'] = [c.pointer(p, 'X') for p in chart_deps]
        c.record(n, 'BRANCH_SMA_NA', 'THREE_WITNESSED_GATED_INPUTS_FINITE', F(0))
    c.criterion('At least three bounded SMA clock discriminators', len(discriminating) >= 3, 'SUPPORTED', None if len(discriminating) >= 3 else 'Insufficient witnessed three-call windows with differing candidates', {'discriminatingDataRowOrdinals': discriminating, 'scope': 'Bounded SMA windows only; no recursive EMA startup certificate'})
