from decimal import Decimal, localcontext
from fractions import Fraction as F


def weighted(rows, source):
    values = [(F(r[source]), F(r['INPUT_VOLUME'])) for r in rows if r[source] != '' and r['INPUT_VOLUME'] != '']
    weight = sum(v for _, v in values)
    if weight <= 0:
        return None
    mean = sum(x * v for x, v in values) / weight
    variance = sum(v * (x - mean) ** 2 for x, v in values) / weight
    with localcontext() as context:
        context.prec = 80
        deviation = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    return weight, mean, variance, str(deviation)


def analyze(c):
    positive, nonzero, missing_windows, zero_rows = [], [], [], []
    for n in c.block:
        row = c.rows[n]
        i, p = int(row['INPUT_INDEX']), int(row['PHASE'])
        c.record(n, 'ANCHOR', 'DECLARED_PHASE0_ANCHOR', F(p == 0), input_titles=['PHASE'])
        c.record(n, 'MULT', 'DECLARED_SERIES_MULTIPLIER', F(p % 3), input_titles=['PHASE'])
        c.record(n, 'INPUT_CLOSE', 'OWN_SOURCE_CHART_CLOSE_BINDING', F(row['close']), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['close'])
        if 'Volume' in row and row['Volume']:
            c.record(n, 'INPUT_VOLUME', 'OWN_SOURCE_NATIVE_VOLUME_CONTROL', F(row['Volume']), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['Volume'])
        c.record(n, 'HOLE_SOURCE', 'DECLARED_PHASE5_SOURCE_HOLE', None if p == 5 else F(row['INPUT_CLOSE']), expected_blank=p == 5, input_titles=['PHASE', 'INPUT_CLOSE'])
        c.record(n, 'HOLE_NA', 'DECLARED_PHASE5_SOURCE_HOLE', F(p == 5), input_titles=['PHASE'])
        deps = [c.by_index.get(j) for j in range(i - p, i + 1)]
        complete = all(d is not None and c.rows[d]['INPUT_CLOSE'] and c.rows[d]['INPUT_VOLUME'] for d in deps)
        if not complete:
            missing_windows.append(n)
            continue
        native_inputs = [c.rows[d] for d in deps]
        candidate = weighted(native_inputs, 'INPUT_CLOSE')
        if candidate is None:
            zero_rows.append(n)
            for title in ['VWAP', 'UPPER', 'LOWER', 'SERIES_VWAP', 'SERIES_UPPER', 'SERIES_LOWER', 'HOLE_VWAP', 'HOLE_UPPER', 'HOLE_LOWER', 'TWO_ARG', 'VWAP_NA', 'HOLE_VWAP_NA']:
                c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Actually observed nonpositive anchor weight; no zero-total native behavior is prescribed')
            c.criterion('Positive VWAP weight / row' + str(n), False, cause='Actual anchor weight is nonpositive or missing; no invented weight/input')
            continue
        positive.append(n)
        weight, mean, variance, deviation = candidate
        if variance > 0:
            nonzero.append(n)
        for title in ['VWAP', 'SERIES_VWAP', 'TWO_ARG']:
            r = c.record(n, title, 'WITNESSED_ANCHOR_WEIGHTED_MEAN', mean, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION')
            r['dependencyCells'] = [c.pointer(d, field) for d in deps for field in ['INPUT_CLOSE', 'INPUT_VOLUME', 'ANCHOR']]
        c.record(n, 'VWAP_NA', 'POSITIVE_WITNESSED_WEIGHT_PRESENCE', F(0))
        for title in ['UPPER', 'LOWER', 'SERIES_UPPER', 'SERIES_LOWER']:
            r = c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Bounded native band target; exact mathematical weighted variance retained separately without a fitted tolerance')
            r['candidateMath'] = {'weightRational': str(weight), 'meanRational': str(mean), 'weightedPopulationVarianceRational': str(variance), 'sqrtVarianceDecimal80Reference': deviation, 'sqrtReferenceStatus': 'Derived mathematical reference, not a native binary64 output prediction', 'multiplierRational': '3/2' if title in ['UPPER', 'LOWER'] else str(F(row['MULT'])), 'sign': '+' if 'UPPER' in title else '-'}
        if row['MULT'] == '0' and row['SERIES_VWAP']:
            for title in ['SERIES_UPPER', 'SERIES_LOWER']:
                c.record(n, title, 'ZERO_MULTIPLIER_EQUALS_OWN_NATIVE_MEAN', F(row['SERIES_VWAP']), input_titles=['SERIES_VWAP', 'MULT'])
        hole_candidate = weighted(native_inputs, 'HOLE_SOURCE')
        if hole_candidate is None:
            continue
        hole_mean = hole_candidate[1]
        passed_hole = p >= 5
        for model in ['SKIP_HOLE', 'POISON_UNTIL_NEXT_ANCHOR']:
            missing = model == 'POISON_UNTIL_NEXT_ANCHOR' and passed_hole
            r = c.record(n, 'HOLE_VWAP', model, None if missing else hole_mean, expected_blank=missing, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION')
            r['dependencyCells'] = [c.pointer(d, field) for d in deps for field in ['HOLE_SOURCE', 'INPUT_VOLUME', 'ANCHOR']]
            c.record(n, 'HOLE_VWAP_NA', model, F(missing), input_titles=['PHASE', 'HOLE_NA'])
            for title in ['HOLE_UPPER', 'HOLE_LOWER']:
                if missing:
                    c.record(n, title, model, expected_blank=True)
                else:
                    c.criterion(model + ' band presence / ' + title + '/row' + str(n), True, 'SUPPORTED' if row[title] else 'REFUTED', details={'nativeCell': c.pointer(n, title), 'anchorInputDataRowOrdinals': deps})
        for title in ['HOLE_UPPER', 'HOLE_LOWER']:
            c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Raw hole-band output retained independently of presence-model verdicts')
    c.criterion('Complete own anchor-input windows', not missing_windows and bool(c.block), 'SUPPORTED', None if not missing_windows and c.block else 'Only affected incomplete anchor rows held', {'missingInputWindowDataRowOrdinals': missing_windows})
    c.criterion('Positive total volume weight actually observed', bool(positive), 'SUPPORTED', None if positive else 'No positive witnessed anchor weight')
    c.criterion('Nonzero weighted variance for multiplier discrimination', bool(nonzero), 'SUPPORTED', None if nonzero else 'No nonzero witnessed anchor variance', {'nonzeroVarianceDataRowOrdinals': nonzero})
    c.criterion('Actually observed nonpositive total-volume domain', bool(zero_rows), 'UNDECIDED', None if zero_rows else 'No such native weight state occurred in the bounded observed inputs', {'dataRowOrdinals': zero_rows})
    c.criterion('Unavailable-volume and original unanchored frontier domains', False, cause='No provider-unavailability or original-prefix identity is inferred from this fresh anchored probe')
