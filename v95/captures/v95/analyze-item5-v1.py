from fractions import Fraction as F


def analyze(c):
    prefix = c.session['strictOwnIndexZeroPrefixAvailable']
    c.criterion('Own OHLC index0..127 prefix for ATR/DMI/Supertrend startup', prefix and all(i in c.by_index for i in range(128)), 'UNDECIDED', None if prefix else 'Own OHLC prefix omitted; seed-dependent target vectors have zero startup scoring credit')
    transitions = []
    for n in c.block:
        row = c.rows[n]
        for own, chart in [('INPUT_OPEN', 'open'), ('INPUT_HIGH', 'high'), ('INPUT_LOW', 'low'), ('INPUT_CLOSE', 'close')]:
            c.record(n, own, 'OWN_SOURCE_CHART_OHLC_BINDING', F(row[chart]), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=[chart])
        prior = c.by_index.get(int(row['INPUT_INDEX']) - 1)
        if prior is not None:
            h, l, previous = F(row['INPUT_HIGH']), F(row['INPUT_LOW']), F(c.rows[prior]['INPUT_CLOSE'])
            r = c.record(n, 'TR', 'WITNESSED_PREVIOUS_CLOSE_TRUE_RANGE', max(h - l, abs(h - previous), abs(l - previous)), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['INPUT_HIGH', 'INPUT_LOW'])
            r['dependencyCells'] = [c.pointer(prior, 'INPUT_CLOSE')]
            a, b = c.rows[prior]['DIRECTION'], row['DIRECTION']
            if a and b and F(a) != F(b):
                transitions.append({'priorRowOrdinal': prior, 'rowOrdinal': n, 'priorDirectionRaw': a, 'directionRaw': b})
        for title in ['ATR', 'DI_PLUS', 'DI_MINUS', 'ADX', 'SUPERTREND', 'DIRECTION']:
            r = c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Own-source exact target retained; complete recursive OHLC startup is a separate guard')
            r.update(closedScoringEligible=prefix, exclusionCause=None if prefix else 'OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED')
        for value, flag in [('ATR', 'ATR_NA'), ('ADX', 'ADX_NA'), ('SUPERTREND', 'TREND_NA')]:
            c.record(n, flag, 'NATIVE_OUTPUT_PRESENCE_WITNESS', F(row[value] == ''), input_titles=[value])
    c.criterion('Naturally observed Supertrend direction transitions', bool(transitions), 'UNDECIDED', None if transitions else 'No direction transition inside the bounded native block', transitions)
