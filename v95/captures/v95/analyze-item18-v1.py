from fractions import Fraction as F


def analyze(c):
    fixed = {'PRE_SUB_SOURCE': 9, 'COPY_01': 9, 'SUB_00': 77, 'JOIN_ROWS': 3, 'JOIN_COLS': 3, 'JOIN_ELEMENTS': 9}
    joined = [[9, 9, 8], [1, 1, 8], [1, 1, 8]]
    for n in c.block:
        for title, value in fixed.items():
            c.record(n, title, 'EXCLUSIVE_FILL_ISOLATED_NUMERIC_SUBMATRIX', F(value))
        c.record(n, 'PRE_SUB_SOURCE', 'SHARED_NUMERIC_SUBMATRIX_ALTERNATIVE', F(77))
        for r in range(3):
            for col in range(3):
                c.record(n, 'JOIN_' + str(r) + '_' + str(col), 'REVERSE_BOTH_AXES_SWAP_RESHAPE_ROW_MAJOR_CONCAT', F(joined[r][col]))
        for model, columns in [('CONCAT_MUTATES_SOURCE', 3), ('CONCAT_ISOLATED_RETURN', 2)]:
            for title, value in [('ROWS', 3), ('COLS', columns), ('ELEMENTS', 3 * columns)]:
                c.record(n, title, model, F(value))
        row = c.rows[n]
        try:
            rows, cols, elements = [F(row[t]) for t in ['JOIN_ROWS', 'JOIN_COLS', 'JOIN_ELEMENTS']]
            complete = rows.denominator == cols.denominator == elements.denominator == 1 and 0 <= rows <= 3 and 0 <= cols <= 3 and elements == rows * cols
        except (ValueError, ZeroDivisionError):
            complete = False
        c.criterion('Complete bounded joined matrix / row' + str(n), complete, 'SUPPORTED', None if complete else 'Native dimensions/counts are absent, inconsistent or exceed the exported3x3 cap; all raw counts/slots retained', {'rowsRaw': row['JOIN_ROWS'], 'columnsRaw': row['JOIN_COLS'], 'elementsRaw': row['JOIN_ELEMENTS']})
    c.criterion('Matrix UDT aliasing and all numeric transformations', False, cause='Outside this exact small numeric composed program; no repair or shape-normalizing variant executed')
