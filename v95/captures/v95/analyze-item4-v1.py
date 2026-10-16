from fractions import Fraction as F


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Own contiguous index0..127 startup and all hole/recovery dependencies', prefix and all(i in c.by_index for i in range(128)), 'UNDECIDED', None if prefix else 'Own index-zero input prefix absent; no recursive seed or startup/recovery rule fitted')
    for n in c.block:
        row = c.rows[n]
        i, cycle = int(row['INPUT_INDEX']), int(row['CYCLE'])
        hole = i < 3 or cycle in [12, 13, 32, 33, 34]
        c.record(n, 'CYCLE', 'DECLARED_INPUT_CYCLE', F(i % 64), input_titles=['INPUT_INDEX'])
        c.record(n, 'CLEAN', 'DECLARED_INTEGER_INPUT', F(i % 11 - 5), input_titles=['INPUT_INDEX'])
        c.record(n, 'X', 'DECLARED_HOLE_MASK', None if hole else F(i % 11 - 5), expected_blank=hole, input_titles=['INPUT_INDEX', 'CYCLE'])
        c.record(n, 'X_NA', 'DECLARED_HOLE_MASK', F(hole), input_titles=['INPUT_INDEX', 'CYCLE'])
        for function in ['EMA', 'RMA', 'RSI', 'TSI']:
            for suffix in ['CLEAN', 'HOLE']:
                r = c.record(n, function + '_' + suffix, 'NATIVE_TARGET_VECTOR', cause='Exact native suffix vector; startup/recursive dependency guard retained')
                r.update(closedScoringEligible=prefix, exclusionCause=None if prefix else 'OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED')
            c.record(n, function + '_HOLE_NA', 'NATIVE_OUTPUT_PRESENCE_WITNESS', F(row[function + '_HOLE'] == ''), input_titles=[function + '_HOLE'])
