from decimal import Decimal, localcontext
from fractions import Fraction as F


def matrix_product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def residual(a, b):
    return [[str(a[i][j] - b[i][j]) for j in range(2)] for i in range(2)]


def analyze(c):
    a, b = [[F(4), F(1)], [F(1), F(3)]], [[F(1), F(2)], [F(2), F(4)]]
    identity = [[F(1), F(0)], [F(0), F(1)]]
    with localcontext() as context:
        context.prec = 80
        sqrt5 = Decimal(5).sqrt()
        eigenvalue_references = [str((Decimal(7) + sqrt5) / 2), str((Decimal(7) - sqrt5) / 2)]
    for n in c.block:
        row = c.rows[n]
        for title, expected in [('A_RANK', 2), ('B_RANK', 1), ('EIGEN_COUNT', 2)]:
            c.record(n, title, 'FROZEN_LITERAL_MATRIX_RANK_AND_COUNT', F(expected))
        count = F(row['EIGEN_COUNT'])
        c.criterion('Complete bounded eigenvalue array / row' + str(n), count.denominator == 1 and 0 <= count <= 2, 'SUPPORTED', None if count.denominator == 1 and 0 <= count <= 2 else 'Actual native count exceeds two exported slots or has inadequate integer precision; raw values remain observed')
        for title, expected in [('A_DET', 11), ('B_DET', 0)]:
            c.record(n, title, 'FROZEN_LITERAL_DETERMINANT', F(expected), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION')
        inverse = [[F(3, 11), F(-1, 11)], [F(-1, 11), F(4, 11)]]
        pseudo = [[F(1, 25), F(2, 25)], [F(2, 25), F(4, 25)]]
        for prefix, expected in [('INV', inverse), ('PINV', pseudo)]:
            for i in range(2):
                for j in range(2):
                    c.record(n, prefix + '_' + str(i) + '_' + str(j), 'FROZEN_INVERSE' if prefix == 'INV' else 'FROZEN_MOORE_PENROSE_B_OVER25', expected[i][j], precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION')
        for title in ['EIGEN_0', 'EIGEN_1', 'EVEC_0_0', 'EVEC_0_1', 'EVEC_1_0', 'EVEC_1_1']:
            r = c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Native eigen signs/order preserved; no normalization or reordering')
            r['unorderedEigenvalueDecimal80References'] = eigenvalue_references
            r['referenceStatus'] = 'Derived mathematical sqrt5 references, not exact native binary64 predictions'
        titles = ['EIGEN_0', 'EIGEN_1'] + [prefix + '_' + str(i) + '_' + str(j) for prefix in ['EVEC', 'INV', 'PINV'] for i in range(2) for j in range(2)]
        if any(row[title] == '' for title in titles):
            c.criterion('Full bounded inverse/pinv/eigen tuple / row' + str(n), False, cause='One or more requested native cells are blank; every actual cell remains retained')
            continue
        ev = [[F(row['EVEC_' + str(i) + '_' + str(j)]) for j in range(2)] for i in range(2)]
        inv = [[F(row['INV_' + str(i) + '_' + str(j)]) for j in range(2)] for i in range(2)]
        pinv = [[F(row['PINV_' + str(i) + '_' + str(j)]) for j in range(2)] for i in range(2)]
        associations = []
        for orientation in ['COLUMNS', 'ROWS']:
            for k in range(2):
                vector = [ev[0][k], ev[1][k]] if orientation == 'COLUMNS' else ev[k]
                value = F(row['EIGEN_' + str(k)])
                parts = [sum(a[i][j] * vector[j] for j in range(2)) - value * vector[i] for i in range(2)]
                associations.append({'orientation': orientation, 'nativeEigenvalueOrdinal': k, 'nativeEigenvalueRaw': row['EIGEN_' + str(k)], 'vectorComponentsRational': [str(x) for x in vector], 'A_times_v_minus_lambda_v_Rational': [str(x) for x in parts], 'squaredResidualRational': str(sum(x * x for x in parts)), 'precisionVerdict': 'UNDECIDED; exact exported-string residuals are retained without a selected tolerance or hidden precision model'})
        bp, pb = matrix_product(b, pinv), matrix_product(pinv, b)
        details = {'nativeCells': [c.pointer(n, title) for title in titles], 'inputLiteralMatrices': {'A': [[4, 1], [1, 3]], 'B': [[1, 2], [2, 4]], 'basis': 'Frozen exact source program assignments; no independent hidden matrix state inspection'}, 'inverseIdentityResidualRational': residual(matrix_product(a, inv), identity), 'B_PINV_B_minus_B_Rational': residual(matrix_product(bp, b), b), 'PINV_B_PINV_minus_PINV_Rational': residual(matrix_product(pb, pinv), pinv), 'B_PINV_symmetryResidualRational': residual(bp, [list(x) for x in zip(*bp)]), 'PINV_B_symmetryResidualRational': residual(pb, [list(x) for x in zip(*pb)]), 'eigenAssociations': associations, 'noSignsFlippedOrOrderChanged': True}
        c.criterion('Bounded eigen-association and numerical residual vectors / row' + str(n), True, 'UNDECIDED', 'No universal tolerance or hidden precision bound selected; all exact rational residuals are supplied for later falsifiable replay', details)
    c.criterion('Singular inverse, near-singular cutoff sweep and generic solver parity', False, cause='Deferred; singular inverse is not called and no parameter/source variant is executed')
