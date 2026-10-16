from fractions import Fraction as F


def analyze(c):
    expected = {'M_SIZE': 3, 'COPY_SIZE': 0, 'DONOR_SIZE': 2, 'REMOVED': 1, 'MERGED_0': 1, 'MERGED_1': 20, 'MERGED_2': 30, 'KEY_0': 2, 'KEY_1': 3, 'KEY_2': 1, 'VALUE_0': 20, 'VALUE_1': 30, 'VALUE_2': 100}
    for n in c.block:
        for title, value in expected.items():
            c.record(n, title, 'FROZEN_INSERTION_ORDER_MERGE_CLEAR_REINSERT', F(value))
        for model, original in [('SHALLOW_REFERENCE_VALUE_COPY', 6), ('DEEP_REFERENCE_VALUE_COPY', 1)]:
            c.record(n, 'REF_ORIGINAL', model, F(original))
            c.record(n, 'REF_COPY', model, F(6))
        row = c.rows[n]
        known = all(row['KEY_' + str(k)] in ['1', '2', '3'] for k in range(3))
        try:
            size = F(row['M_SIZE'])
        except (ValueError, ZeroDivisionError):
            size = None
        complete = size == 3 and known and len({row['KEY_' + str(k)] for k in range(3)}) == 3 and all(row['VALUE_' + str(k)] != '' for k in range(3))
        c.criterion('Complete final key/value slots / row' + str(n), complete, 'SUPPORTED', None if complete else 'Native final count, unique known keys or finite value witnesses do not establish the complete three-slot distribution; actual cells remain observed', {'actualSizeRaw': row['M_SIZE'], 'actualKeyCodesRaw': [row['KEY_' + str(k)] for k in range(3)], 'keyCodeDomain': {'1': 'A', '2': 'B', '3': 'C'}})
    c.criterion('Unexposed merged-array count and arbitrary key/value types', False, cause='Only the three supplied merged slots and the final map count/order are captured; no omitted count or generic type coverage is invented')
