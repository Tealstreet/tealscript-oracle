from fractions import Fraction as F


def analyze(c):
    defaults = {'INT': 7, 'FLOAT': F(5, 4), 'BOOL': 1, 'STRING_LENGTH': 3, 'STRING_EXACT': 1, 'ENUM_A': 1, 'SESSION_LENGTH': 9, 'SESSION_EXACT': 1, 'TF_LENGTH': 1, 'TF_EXACT': 1, 'SYMBOL_LENGTH': 15, 'SYMBOL_EXACT': 1, 'PRICE': F(25, 2), 'TIME': 1767225600000, 'COLOR_R': 10, 'COLOR_G': 20, 'COLOR_B': 30, 'COLOR_T': 40, 'GENERIC': 2, 'TEXT_LENGTH': 4, 'TEXT_EXACT': 1}
    for n in c.block:
        for title, expected in defaults.items():
            c.record(n, title, 'UNCHANGED_DECLARED_NATIVE_DEFAULT', F(expected))
        c.record(n, 'INPUT_CLOSE', 'OWN_SOURCE_CHART_CLOSE_BINDING', F(c.rows[n]['close']), precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION', input_titles=['close'])
        c.record(n, 'SOURCE', 'DEFAULT_SOURCE_EQUALS_OWN_CLOSE', F(c.rows[n]['INPUT_CLOSE']), input_titles=['INPUT_CLOSE'])
    c.criterion('Default inputs unchanged in one native session', True, 'SUPPORTED', details={'metadata': 'Save/Add complete native metaInfo.inputs and defaults are retained in observation-v1.json and original compiler bodies', 'inputChanges': 0})
    c.criterion('Options/range/step/confirm/active/display enforcement and external source selection', False, cause='Deferred; no input/settings state was changed or external source selected')
