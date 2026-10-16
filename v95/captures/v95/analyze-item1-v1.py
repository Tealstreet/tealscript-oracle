from datetime import datetime
from fractions import Fraction as F


def analyze(c):
    export_ms = F(str(datetime.fromisoformat(c.session['nativeObservationUtc'].replace('Z', '+00:00')).timestamp())) * 1000
    positive = [n for n in c.closed if c.rows[n]['N'] in ['1', '2']]
    twos = [n for n in positive if c.rows[n]['N'] == '2']
    c.criterion('At least32 closed N1/2 chart rows and one N2 discriminator', len(positive) >= 32 and bool(twos), 'SUPPORTED', None if len(positive) >= 32 and twos else 'Required naturally occurring tuple counts not observed', {'positiveRows': len(positive), 'twoIntrabarRows': len(twos)})
    counts = {str(k): sum(c.rows[n]['N'] == str(k) for n in c.closed) for k in [0, 1, 2]}
    too_large = [n for n in c.closed if int(c.rows[n]['N']) > 2]
    c.criterion('Complete bounded arrays on every N<=2 closed row', not too_large, 'SUPPORTED', None if not too_large else 'Present N>2 exceeds the two exported slots; full arrays held for those rows', {'closedCountDistribution': counts, 'largerArrayDataRowOrdinals': too_large})
    arrays = ['ltc', 'lo', 'lh', 'll', 'lc', 'lv', 'lx']
    for n in c.closed:
        row = c.rows[n]
        count = int(row['N'])
        chart_open = F(row['INPUT_TIME'])
        chart_close = F(row['CHART_CLOSE_TIME'])
        c.record(n, 'CHART_CLOSE_TIME', 'NATIVE_2M_PHYSICAL_CLOSE', chart_open + 120000, input_titles=['INPUT_TIME'])
        for name in arrays:
            c.record(n, 'N_' + name, 'TUPLE_ARRAY_LENGTH_AGREEMENT', F(count), input_titles=['N'])
        for slot in range(2):
            titles = [prefix + '_' + str(slot) for prefix in ['LT', 'LTC', 'LO', 'LH', 'LL', 'LC', 'LV', 'LX']]
            if slot >= count:
                for title in titles:
                    c.record(n, title, 'GUARDED_ABSENT_SLOT_BLANK', expected_blank=True, input_titles=['N'])
                continue
            for title in titles:
                c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Source-owned lower-timeframe tuple target; no independent hidden provider value inferred', input_titles=['N', 'INPUT_TIME', 'CHART_CLOSE_TIME'])
            lt, ltc = row['LT_' + str(slot)], row['LTC_' + str(slot)]
            if lt and ltc:
                c.record(n, 'LTC_' + str(slot), 'ONE_MINUTE_INTRABAR_PHYSICAL_CLOSE', F(lt) + 60000, input_titles=['LT_' + str(slot)])
                inside = chart_open <= F(lt) < F(ltc) <= chart_close
                physical = F(ltc) <= export_ms
                c.criterion('Intrabar containment and physical close / row' + str(n) + '/slot' + str(slot), True, 'SUPPORTED' if inside and physical else 'REFUTED', details={'dataRowOrdinal': n, 'slot': slot, 'chartOpenRaw': row['INPUT_TIME'], 'chartCloseRaw': row['CHART_CLOSE_TIME'], 'intrabarOpenRaw': lt, 'intrabarCloseRaw': ltc, 'nativeExportUtc': c.session['nativeObservationUtc']})
            else:
                c.criterion('Intrabar time identity / row' + str(n) + '/slot' + str(slot), True, 'REFUTED', cause='Present array count but raw time slot blank; contradiction retained in source cells')
            lc, lx = row['LC_' + str(slot)], row['LX_' + str(slot)]
            if lc:
                c.record(n, 'LX_' + str(slot), 'EXPRESSION_LX_EQUALS_2LC_PLUS1', 2 * F(lc) + 1, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['LC_' + str(slot)])
            if slot == 1 and row['LT_0'] and lt:
                c.criterion('Strictly increasing tuple times / row' + str(n), True, 'SUPPORTED' if F(lt) > F(row['LT_0']) else 'REFUTED', details={'dataRowOrdinal': n, 'firstOpenRaw': row['LT_0'], 'secondOpenRaw': lt})
    c.criterion('Original MTF developing input/as-of identity', False, cause='Outside v95 item1 closed lower-timeframe tuple contract; historical holds unchanged')
