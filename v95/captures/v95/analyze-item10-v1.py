from fractions import Fraction as F


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Own origin for pre-origin Boolean/fixnan startup', prefix, 'UNDECIDED', None if prefix else 'Own first input row absent; repeated FIRST fields do not recover startup')
    previous_finite = None
    for n in c.closed:
        row = c.rows[n]
        if n in c.block:
            phase = int(row['PHASE']) % 4
            x = [None, F('-2.9'), F(0), F('2.9')][phase]
            c.record(n, 'X', 'DECLARED_TYPED_NA_INPUT', x, expected_blank=x is None, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['PHASE'])
            c.record(n, 'X_NA', 'DECLARED_TYPED_NA_INPUT', F(x is None), input_titles=['PHASE'])
            c.record(n, 'NZ', 'DECLARED_NZ17_REPLACEMENT', F(17) if x is None else x, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['PHASE', 'X_NA'])
            integer = [None, F(-2), F(0), F(2)][phase]
            for title in ['INT_CAST', 'FLOAT_CAST']:
                c.record(n, title, 'INTEGER_TRUNCATION_TOWARD_ZERO', integer, expected_blank=integer is None, input_titles=['PHASE', 'X_NA'])
            c.record(n, 'INT_NA', 'INTEGER_TRUNCATION_TOWARD_ZERO', F(integer is None), input_titles=['X_NA'])
            expected_bool = (-1 if c.asset['pineVersion'] == 5 else 0) if x is None else int(x != 0)
            c.record(n, 'BOOL_ENCODE', 'FROZEN_VERSIONED_BOOLEAN_DOMAIN', F(expected_bool), input_titles=['PHASE', 'X_NA'])
            prior = c.by_index.get(int(row['INPUT_INDEX']) - 1)
            if prior is not None:
                r = c.record(n, 'BOOL_HISTORY_ENCODE', 'WITNESSED_PREVIOUS_BOOLEAN_INPUT', F(int(c.rows[prior]['PHASE']) % 2 == 0), input_titles=['INPUT_INDEX'])
                r['dependencyCells'] = [c.pointer(prior, 'PHASE')]
            elif prefix and int(row['INPUT_INDEX']) == 0:
                c.record(n, 'BOOL_HISTORY_ENCODE', 'VERSIONED_PRE_ORIGIN_BOOLEAN', F(-1 if c.asset['pineVersion'] == 5 else 0))
            if x is not None:
                c.record(n, 'FIXNAN', 'FINITE_FIXNAN_CONTROL', F(row['X']), input_titles=['X'])
                c.record(n, 'FIXNAN_NA', 'FINITE_FIXNAN_CONTROL', F(0))
            elif previous_finite is not None:
                r = c.record(n, 'FIXNAN', 'CARRY_PREVIOUS_FINITE_INPUT', F(c.rows[previous_finite]['X']))
                r['dependencyCells'] = [c.pointer(previous_finite, 'X')]
                c.record(n, 'FIXNAN_NA', 'CARRY_PREVIOUS_FINITE_INPUT', F(0))
                c.record(n, 'FIXNAN', 'PROPAGATE_MISSING_CHART_SLOT', expected_blank=True)
                c.record(n, 'FIXNAN_NA', 'PROPAGATE_MISSING_CHART_SLOT', F(1))
            for title in ['STRING_LENGTH', 'STRING_EMPTY_EQ', 'STRING_NA']:
                c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Missing-string representation is an open native target; no empty/NaN normalization')
            c.record(n, 'STRING_NUMERIC_PARSE', 'LITERAL_NEGATIVE_DECIMAL_PARSE', F('-2.50'))
        if row['X'] != '':
            previous_finite = n
