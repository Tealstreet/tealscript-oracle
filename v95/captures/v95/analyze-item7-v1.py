from fractions import Fraction as F


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Own origin for pre-origin dynamic/history missingness', prefix, 'UNDECIDED', None if prefix else 'Own index-zero row omitted; no pre-origin behavior inferred')
    for n in c.block:
        row = c.rows[n]
        x, i, lag = F(row['X']), int(row['INPUT_INDEX']), int(row['LAG'])
        c.record(n, 'X', 'DECLARED_PHASE_INPUT', F(row['PHASE']), input_titles=['PHASE'])
        c.record(n, 'LAG', 'DECLARED_DYNAMIC_LAG', F(int(row['PHASE']) % 5), input_titles=['PHASE'])
        for title, expected in [('REC_X', x + 100), ('COPY_X', x + 200)]:
            c.record(n, title, 'DISTINCT_SCALAR_COPY_WITH_ORIGINAL_ALIAS', expected, input_titles=['X'])
        for title in ['REC_PAYLOAD', 'COPY_PAYLOAD']:
            c.record(n, title, 'SHALLOW_REFERENCE_FIELD_COPY', x + 300, input_titles=['X'])
        c.record(n, 'REC_PAYLOAD', 'DEEP_REFERENCE_FIELD_COPY', x, input_titles=['X'])
        c.record(n, 'COPY_PAYLOAD', 'DEEP_REFERENCE_FIELD_COPY', x + 300, input_titles=['X'])
        dependency = c.by_index.get(i - lag)
        if dependency is not None:
            r = c.record(n, 'DYNAMIC', 'WITNESSED_DYNAMIC_HISTORY', F(c.rows[dependency]['X']), input_titles=['INPUT_INDEX', 'LAG'])
            r['dependencyCells'] = [c.pointer(dependency, 'X')]
            c.record(n, 'DYNAMIC_NA', 'WITNESSED_DYNAMIC_HISTORY', F(0))
        elif prefix and i < lag:
            c.record(n, 'DYNAMIC', 'WITNESSED_PRE_ORIGIN_HISTORY', expected_blank=True, input_titles=['INPUT_INDEX', 'LAG'])
            c.record(n, 'DYNAMIC_NA', 'WITNESSED_PRE_ORIGIN_HISTORY', F(1))
        else:
            c.criterion('Dynamic history dependency / row' + str(n), False, cause='The required own input dependency is not exported')
        prior = c.by_index.get(i - 1)
        if prior is not None:
            for title, increment in [('PRIOR_X', 100), ('PRIOR_PAYLOAD', 300)]:
                r = c.record(n, title, 'DISTINCT_PER_BAR_REFERENCE_HISTORY', F(c.rows[prior]['X']) + increment, input_titles=['INPUT_INDEX'])
                r['dependencyCells'] = [c.pointer(prior, 'X')]
            c.record(n, 'PRIOR_NA', 'WITNESSED_PREVIOUS_REFERENCE', F(0))
        elif prefix and i == 0:
            for title in ['PRIOR_X', 'PRIOR_PAYLOAD']:
                c.record(n, title, 'WITNESSED_PRE_ORIGIN_REFERENCE', expected_blank=True)
            c.record(n, 'PRIOR_NA', 'WITNESSED_PRE_ORIGIN_REFERENCE', F(1))
