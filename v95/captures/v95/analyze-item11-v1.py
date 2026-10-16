from fractions import Fraction as F


def analyze(c):
    for n in c.block:
        for model, a in [('SHARED_SLICE_WINDOW', [1, 20, 3, 9, 4]), ('ISOLATED_SLICE', [1, 2, 3, 4])]:
            for prefix, values, cap in [('A', a, 5), ('B', [1, 2, 3, 4], 4), ('VIEW', [20, 3, 9], 3)]:
                c.record(n, prefix + '_SIZE', model, F(len(values)))
                for slot in range(cap):
                    c.record(n, prefix + '_' + str(slot), model, F(values[slot]) if slot < len(values) else None, expected_blank=slot >= len(values))
            c.record(n, 'LAST', model, F(a[-1]))
        for title, value in [('BOX_ARRAY_SIZE', 2), ('BOX0_NA', 1), ('TABLE_ARRAY_SIZE', 1), ('TABLE0_NA', 1)]:
            c.record(n, title, 'TYPED_MISSING_ID_ARRAY_CONSTRUCTOR', F(value))
        sizes = {p: int(c.rows[n][p + '_SIZE']) for p in ['A', 'B', 'VIEW']}
        complete = sizes['A'] <= 5 and sizes['B'] <= 4 and sizes['VIEW'] <= 3
        c.criterion('Complete bounded collection slots / row' + str(n), complete, 'SUPPORTED', None if complete else 'Actual size exceeds exported cap; all present counts/slots retained', sizes)
    c.criterion('All reference kinds and drawing-object creation', False, cause='Outside this numeric slice/copy and arrays-of-missing-IDs contract; no drawing/table object was created')
