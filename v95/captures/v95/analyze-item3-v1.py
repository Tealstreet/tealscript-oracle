from fractions import Fraction as F


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Complete reset blocks for independent textual UDF call sites', bool(c.block), 'SUPPORTED', None if c.block else 'No complete witnessed phase0..15 block')
    c.criterion('First-reach local var initialization from own index-zero prefix', prefix, 'UNDECIDED', None if prefix else 'Own source prefix absent; LOCAL_FIRST retained without reconstructing its initialization')
    for n in c.block:
        p = int(c.rows[n]['PHASE'])
        for title, expected in [('A', p + 1), ('B', 10 * (p + 1)), ('NESTED', 5 * (p + 1))]:
            c.record(n, title, 'INDEPENDENT_TEXTUAL_CALL_SITE_RESET', F(expected), input_titles=['PHASE'])
        c.record(n, 'GATED', 'INDEPENDENT_GATED_CALL_SITE_RESET', F(100 * (p // 2 + 1)) if p % 2 == 0 else None, expected_blank=p % 2 == 1, input_titles=['PHASE'])
        c.record(n, 'GATED_NA', 'EXPLICIT_GATED_PRESENCE', F(p % 2 == 1), input_titles=['PHASE'])
        if p < 5:
            c.record(n, 'LOCAL_FIRST', 'EXPLICIT_LOCAL_BRANCH_MASK', expected_blank=True, input_titles=['PHASE'])
            c.record(n, 'LOCAL_FIRST_NA', 'EXPLICIT_LOCAL_BRANCH_MASK', F(1), input_titles=['PHASE'])
        elif prefix:
            c.record(n, 'LOCAL_FIRST', 'LOCAL_VAR_FIRST_REACH_INDEX5', F(5), input_titles=['PHASE', 'FIRST_INDEX'])
            c.record(n, 'LOCAL_FIRST_NA', 'LOCAL_VAR_FIRST_REACH_INDEX5', F(0))
        else:
            r = c.record(n, 'LOCAL_FIRST', 'NATIVE_TARGET_VECTOR', cause='First-reach initialization depends on an omitted own prefix')
            r.update(closedScoringEligible=False, exclusionCause='OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED')
            c.record(n, 'LOCAL_FIRST_NA', 'LOCAL_BRANCH_FINITE_PRESENCE', F(0), input_titles=['PHASE'])
