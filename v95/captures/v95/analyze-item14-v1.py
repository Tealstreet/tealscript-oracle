from fractions import Fraction as F


def rounded(x, model):
    if model == 'TIES_UP':
        y = x + F(1, 2)
        return y.numerator // y.denominator
    if model == 'TIES_AWAY':
        y = abs(x) + F(1, 2)
        return (1 if x >= 0 else -1) * (y.numerator // y.denominator)
    floor = x.numerator // x.denominator
    residue = x - floor
    return floor + (residue > F(1, 2) or residue == F(1, 2) and floor % 2 == 1)


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Own index-zero prefix for seeded random stream replay', prefix, 'UNDECIDED', None if prefix else 'Own startup input prefix omitted; sampled random values do not establish the full seed/stream identity')
    seen = set()
    for n in c.block:
        row = c.rows[n]
        x = F(row['X'])
        seen.add(x)
        expected_x = [F(-5, 2), F(-3, 2), F(-1, 2), F(1, 2), F(3, 2), F(5, 2)][int(row['PHASE']) % 6]
        c.record(n, 'X', 'DECLARED_SIX_HALF_TIES', expected_x, input_titles=['PHASE'])
        for model in ['TIES_UP', 'TIES_AWAY', 'TIES_EVEN']:
            c.record(n, 'ROUND', model, F(rounded(x, model)), input_titles=['X'])
        floor = x.numerator // x.denominator
        ceil = -((-x).numerator // (-x).denominator)
        integer = (1 if x >= 0 else -1) * (abs(x).numerator // abs(x).denominator)
        controls = {'ROUND1': x, 'FLOOR': F(floor), 'CEIL': F(ceil), 'INT': F(integer), 'MIN': min(x, F(0), F(1)), 'MAX': max(x, F(0), F(1)), 'ABS': abs(x), 'LOG_INPUT': abs(x) + 1}
        for title, expected in controls.items():
            c.record(n, title, 'EXACT_BINARY_HALF_SCALAR_CONTROL', expected, input_titles=['X'])
        c.record(n, 'AVG', 'VARIADIC_THREE_VALUE_MEAN', (x + 1) / 3, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['X'])
        for title in ['POW', 'EXP', 'LOG']:
            c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Bounded native transcendental target with exact input; no fitted algorithm or universal tolerance', input_titles=['X', 'LOG_INPUT'])
        tick = F(row['MINTICK'])
        actual_tick_input = F(row['TICK_INPUT'])
        r = c.record(n, 'TICK_INPUT', 'NATIVE_TARGET_VECTOR', cause='Actual native product string is retained; decimal source text is not substituted for a hidden binary64 value', input_titles=['MINTICK', 'X'])
        r['derivedProductFromExportedStringsRational'] = str(tick * x)
        if tick > 0:
            for model in ['TIES_UP', 'TIES_AWAY', 'TIES_EVEN']:
                r = c.record(n, 'TICK_ROUND', 'EXPORTED_INPUT_RATIO/' + model, tick * rounded(actual_tick_input / tick, model), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['MINTICK', 'TICK_INPUT'])
                r['ratioFromExportedStringsRational'] = str(actual_tick_input / tick)
                r['scope'] = 'Frozen rational ratio candidate from actual strings; no assertion that this recovers the hidden binary64 half-tie exactly'
        i = int(row['INPUT_INDEX'])
        deps = [c.by_index.get(j) for j in range(i - 2, i + 1)]
        if all(d is not None for d in deps):
            r = c.record(n, 'SUM3', 'THREE_WITNESSED_HALF_INPUT_SUM', sum(F(c.rows[d]['X']) for d in deps))
            r['dependencyCells'] = [c.pointer(d, 'X') for d in deps]
        for title in ['RANDOM_A', 'RANDOM_B']:
            r = c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Same-source sampled seeded output; own origin guard controls stream replay')
            r.update(closedScoringEligible=prefix, exclusionCause=None if prefix else 'OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED')
        if prefix:
            c.record(n, 'RANDOM_A', 'EQUAL_INDEPENDENT_SEEDED_CALL_SITE_STREAMS', F(row['RANDOM_B']), input_titles=['RANDOM_B'])
    c.criterion('All six distinct half-tie inputs observed', len(seen) == 6, 'SUPPORTED', None if len(seen) == 6 else 'Naturally exported block lacks one or more half-tie phases', {'actualInputRationals': sorted(str(x) for x in seen)})
