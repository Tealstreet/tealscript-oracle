from datetime import datetime, timezone
from fractions import Fraction as F

ALPHABET = '0123456789.-:+/ ABXYZabcxyzNn'
assert len(set(ALPHABET)) == len(ALPHABET)


def encoder(c, n, dash=False):
    fields = {'ENCODER_0': 0, 'ENCODER_A': ALPHABET.index('A')}
    if dash:
        fields['ENCODER_DASH'] = ALPHABET.index('-')
    valid = True
    for title, expected in fields.items():
        c.record(n, title, 'INDEPENDENT_ENCODER_CALIBRATION', F(expected))
        try:
            valid = valid and F(c.rows[n][title]) == expected
        except ValueError:
            valid = False
    return valid


def decode(c, n, prefix, cap, calibrated):
    row = c.rows[n]
    titles = [prefix + '_LEN'] + [prefix + '_C' + str(k) for k in range(cap)]
    pointers = [c.pointer(n, title) for title in titles]
    result = {'prefix': prefix, 'cap': cap, 'alphabet': ALPHABET, 'rawCellPointers': pointers, 'encoderCalibrated': calibrated, 'decodedString': None}
    try:
        length = F(row[prefix + '_LEN'])
        codes = [F(row[prefix + '_C' + str(k)]) for k in range(cap)]
        if not calibrated:
            raise ValueError('Encoder calibration failed; cannot attribute output solely to formatting/operation')
        if length.denominator != 1 or not 0 <= length <= cap:
            raise ValueError('Length missing/noninteger or exceeds the frozen cap')
        length = int(length)
        if not all(x.denominator == 1 and 0 <= x < len(ALPHABET) for x in codes[:length]):
            raise ValueError('Unknown/negative/missing/noninteger character code inside actual string length')
        if not all(x == -1 for x in codes[length:]):
            raise ValueError('Padding guard is contrary beyond actual length')
        result['decodedString'] = ''.join(ALPHABET[int(x)] for x in codes[:length])
        result['captureStatus'] = 'CAPTURED'
        result['cause'] = None
    except (ValueError, ZeroDivisionError) as error:
        result['captureStatus'] = 'NOT OBSERVED / full string identity'
        result['cause'] = str(error)
    c.criterion('Complete positional string witness / ' + prefix + '/row' + str(n), result['captureStatus'] == 'CAPTURED', 'SUPPORTED', result['cause'], result)
    return result


def candidate(c, n, prefix, cap, text, model, witness):
    cause = 'Composed-program literal/encoding candidate; formatter/operation attribution independently requires the complete calibrated witness'
    c.record(n, prefix + '_LEN', model, F(len(text)), cause=cause)
    for k in range(cap):
        value = ALPHABET.index(text[k]) if k < len(text) else -1
        c.record(n, prefix + '_C' + str(k), model, F(value), cause=cause)
    okay = witness['captureStatus'] == 'CAPTURED'
    c.criterion('Decoded literal candidate / ' + prefix + '/' + model + '/row' + str(n), okay, 'SUPPORTED' if okay and witness['decodedString'] == text else 'REFUTED', None if okay else witness['cause'], {'expectedString': text, 'actualDecodedString': witness['decodedString'], 'scope': 'This exact bounded composed program only'})


def analyze(c):
    for n in c.block:
        p = int(c.rows[n]['PHASE'])
        x = [F(-5, 2), F(0), F(5, 4), F(25, 2)][p % 4]
        c.record(n, 'X', 'DECLARED_BINARY_FORMAT_INPUT', x, input_titles=['PHASE'])
        hour = 6 if p % 2 == 0 else 7
        epoch = int(datetime(2026, 3, 8, hour, 30, tzinfo=timezone.utc).timestamp()) * 1000
        c.record(n, 'FIXED_TIME', 'DECLARED_FIXED_TIMESTAMP', F(epoch), input_titles=['PHASE'])
        calibrated = encoder(c, n, True)
        witnesses = {prefix: decode(c, n, prefix, cap, calibrated) for prefix, cap in [('TOSTRING', 6), ('FORMAT', 6), ('TIME', 5), ('MISSING', 6)]}
        candidate(c, n, 'TOSTRING', 6, ['-2.50', '0.00', '1.25', '12.50'][p % 4], 'FROZEN_TWO_DECIMAL_TOSTRING', witnesses['TOSTRING'])
        for model in ['ONE_DECIMAL_TIES_UP', 'ONE_DECIMAL_TIES_AWAY', 'ONE_DECIMAL_TIES_EVEN']:
            text = ['-2.5', '0.0', '1.2' if model == 'ONE_DECIMAL_TIES_EVEN' else '1.3', '12.5'][p % 4]
            candidate(c, n, 'FORMAT', 6, text, model, witnesses['FORMAT'])
        candidate(c, n, 'TIME', 5, '01:30' if p % 2 == 0 else '03:30', 'FROZEN_DST_TIME_FORMAT', witnesses['TIME'])
        for title in ['MISSING_LEN'] + ['MISSING_C' + str(k) for k in range(6)]:
            c.record(n, title, 'NATIVE_TARGET_VECTOR', cause='Missing-number stringify is an open native target, preserved without empty/NaN substitution')
    c.criterion('Unicode-wide behavior and strings beyond the supplied caps', False, cause='Deferred; unknown code/overflow remains a full-identity hold, never a runtime cap expansion')
