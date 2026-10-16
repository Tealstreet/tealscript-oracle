import runpy
from fractions import Fraction as F
from pathlib import Path


def analyze(c):
    helpers = runpy.run_path(str(Path(__file__).with_name('analyze-item15-v1.py')))
    encoder, decode, candidate = [helpers[name] for name in ['encoder', 'decode', 'candidate']]
    alphabet = helpers['ALPHABET']
    for n in c.block:
        calibrated = encoder(c, n)
        witnesses = {prefix: decode(c, n, prefix, cap, calibrated) for prefix, cap in [('REPLACE', 4), ('ALL', 4), ('REPEAT', 5), ('SUBSTRING', 3)]}
        candidate(c, n, 'REPLACE', 4, 'ABxy', 'ZERO_BASED_OCCURRENCE1', witnesses['REPLACE'])
        candidate(c, n, 'REPLACE', 4, 'xyAB', 'FIRST_OCCURRENCE_ALTERNATIVE', witnesses['REPLACE'])
        for prefix, cap, text in [('ALL', 4, 'xyxy'), ('REPEAT', 5, 'x-x-x'), ('SUBSTRING', 3, 'Bxy')]:
            candidate(c, n, prefix, cap, text, 'FROZEN_LITERAL_STRING_OPERATION', witnesses[prefix])
        for model, parts in [('SPLIT_RETAINS_EMPTY_FIELD', ['a', '', 'b']), ('SPLIT_DROPS_EMPTY_FIELD', ['a', 'b'])]:
            c.record(n, 'PARTS', model, F(len(parts)))
            for slot in range(3):
                text = parts[slot] if slot < len(parts) else ''
                c.record(n, 'PART' + str(slot) + '_LEN', model, F(len(text)))
                c.record(n, 'PART' + str(slot) + '_CODE', model, F(alphabet.index(text) if text else -1))
        size = F(c.rows[n]['PARTS'])
        c.criterion('Complete bounded split distribution / row' + str(n), size.denominator == 1 and 0 <= size <= 3, 'SUPPORTED', None if size.denominator == 1 and 0 <= size <= 3 else 'Actual split shape exceeds the three bounded slots or lost integer precision')
        for slot in range(3):
            length = c.rows[n]['PART' + str(slot) + '_LEN']
            code = c.rows[n]['PART' + str(slot) + '_CODE']
            try:
                length_number, code_number = F(length), F(code)
                good = calibrated and length_number in [0, 1] and (code_number == -1 if length_number == 0 else code_number.denominator == 1 and 0 <= code_number < len(alphabet))
            except (ValueError, ZeroDivisionError):
                good = False
                length_number, code_number = None, None
            text = '' if good and length_number == 0 else alphabet[int(code_number)] if good else None
            c.criterion('Complete split slot identity / row' + str(n) + '/slot' + str(slot), good, 'SUPPORTED', None if good else 'Length/code/calibration is absent, contrary, unknown or exceeds one-character slot witness', {'lengthCell': c.pointer(n, 'PART' + str(slot) + '_LEN'), 'codeCell': c.pointer(n, 'PART' + str(slot) + '_CODE'), 'decodedString': text})
        c.record(n, 'NO_MATCH_POS', 'NATIVE_TARGET_VECTOR', cause='Actual no-match position preserved; no -1/0/NA substitution')
        c.record(n, 'NO_MATCH_NA', 'NATIVE_NO_MATCH_PRESENCE_WITNESS', F(c.rows[n]['NO_MATCH_POS'] == ''), input_titles=['NO_MATCH_POS'])
        for title in ['TRIM_EQ', 'UPPER_EQ', 'LOWER_EQ']:
            c.record(n, title, 'FROZEN_LITERAL_EQUALITY', F(1))
        c.record(n, 'TONUMBER', 'LITERAL_NEGATIVE_DECIMAL_PARSE', F(-5, 2))
