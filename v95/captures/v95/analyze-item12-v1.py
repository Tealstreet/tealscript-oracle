from fractions import Fraction as F


def analyze(c):
    for n in c.block:
        c.record(n, 'SIZE', 'FOUR_ELEMENT_LITERAL_ARRAY', F(4))
        for model, values in [('MISSING_SEARCH_MATCHES', [1, 1, 1]), ('MISSING_SEARCH_NEVER_MATCHES', [0, -1, -1])]:
            for title, value in zip(['INCLUDES_NA', 'INDEX_NA', 'LASTINDEX_NA'], values):
                c.record(n, title, model, F(value))
        for title, expected in [('SUM', F(7)), ('AVG', F(7, 3)), ('MEDIAN', F(3)), ('MIN', F(1)), ('MAX', F(3)), ('VARIANCE', F(8, 9))]:
            precision = 'EXACT_INTEGER_OR_BINARY_FRACTION' if expected.denominator == 1 else 'EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION'
            c.record(n, title, 'REDUCTION_SKIPS_NA', expected, precision=precision)
            c.record(n, title, 'REDUCTION_PROPAGATES_NA', expected_blank=True)
        r = c.record(n, 'STDEV', 'NATIVE_TARGET_VECTOR', cause='Native fractional target; frozen skip-NA reference is sqrt(8/9), with no fitted tolerance')
        r['candidateMath'] = {'model': 'REDUCTION_SKIPS_NA', 'squareRootRadicandRational': '8/9'}
        c.record(n, 'STDEV', 'REDUCTION_PROPAGATES_NA', expected_blank=True)
        c.record(n, 'PERCENTILE', 'NATIVE_TARGET_VECTOR', cause='Exact original array/percentile call target; no repaired sorting or NA normalization')
        for position, values in [('NA_FIRST', [None, 1, 3, 3]), ('NA_LAST', [1, 3, 3, None])]:
            for slot, value in enumerate(values):
                c.record(n, 'SORTED_' + str(slot), position, F(value) if value is not None else None, expected_blank=value is None)
                c.record(n, 'SORTED_NA_' + str(slot), position, F(value is None))
            for tie in ['FORWARD_EQUAL_KEYS', 'REVERSE_EQUAL_KEYS']:
                equal = [2, 3] if tie == 'FORWARD_EQUAL_KEYS' else [3, 2]
                indices = [1, 0] + equal if position == 'NA_FIRST' else [0] + equal + [1]
                for slot, value in enumerate(indices):
                    c.record(n, 'ORDER_' + str(slot), position + '/' + tie, F(value))
        c.criterion('Complete four-slot sort/order witnesses / row' + str(n), int(c.rows[n]['SIZE']) <= 4, 'SUPPORTED', None if int(c.rows[n]['SIZE']) <= 4 else 'Actual collection size exceeds the four exported slots')
    c.criterion('Empty arrays, arbitrary NA/key types and all reduction flags', False, cause='Deferred; these literal nonempty numeric arrays establish only their captured inputs')
