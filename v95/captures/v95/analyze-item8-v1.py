from datetime import datetime, timezone
from fractions import Fraction as F


def analyze(c):
    instants = [(3, 8, 6), (3, 8, 7), (11, 1, 5), (11, 1, 6)]
    membership, day_boundaries, week_boundaries = [], [], []
    for n in c.block:
        row = c.rows[n]
        phase = int(row['PHASE']) % 4
        month, day, hour = instants[phase]
        fields = {'FIXED_TIME': int(datetime(2026, month, day, hour, 30, tzinfo=timezone.utc).timestamp()) * 1000, 'NY_HOUR': [1, 3, 1, 1][phase], 'NY_MINUTE': 30, 'UTC_HOUR': hour, 'NY_DAY': day, 'NY_MONTH': month, 'NY_WEEKDAY': 1}
        for title, expected in fields.items():
            c.record(n, title, 'FROZEN_LITERAL_DST_CONVERSION', F(expected), input_titles=['PHASE'])
        h = int(row['CHART_NY_HOUR'])
        inside = h >= 23 or h < 2
        membership.append((n, inside))
        c.record(n, 'SESSION_IN', 'OVERNIGHT_MEMBERSHIP_FROM_OWN_NY_CLOCK', F(inside), input_titles=['CHART_NY_HOUR', 'CHART_NY_MINUTE'])
        for title in ['SESSION_OPEN', 'SESSION_CLOSE']:
            if inside:
                c.record(n, title, 'NATIVE_TARGET_VECTOR', input_titles=['INPUT_TIME', 'CHART_NY_HOUR'])
            else:
                c.record(n, title, 'OUTSIDE_SESSION_MASK', expected_blank=True, input_titles=['CHART_NY_HOUR'])
        for title in ['CHART_NY_HOUR', 'CHART_NY_MINUTE', 'DAY_OPEN', 'WEEK_CHANGE']:
            c.record(n, title, 'NATIVE_TARGET_VECTOR', input_titles=['INPUT_TIME'])
        prior = c.by_index.get(int(row['INPUT_INDEX']) - 1)
        if prior is not None and row['DAY_OPEN'] and c.rows[prior]['DAY_OPEN'] and F(row['DAY_OPEN']) != F(c.rows[prior]['DAY_OPEN']):
            day_boundaries.append({'priorDayOpenCell': c.pointer(prior, 'DAY_OPEN'), 'dayOpenCell': c.pointer(n, 'DAY_OPEN')})
        if row['WEEK_CHANGE'] == '1':
            week_boundaries.append(c.pointer(n, 'WEEK_CHANGE'))
        c.record(n, 'TF_SECONDS', 'DECLARED_2M_TIMEFRAME', F(120))
        c.record(n, 'CHART_CLOSE_TIME', 'DECLARED_2M_PHYSICAL_CLOSE', F(row['INPUT_TIME']) + 120000, input_titles=['INPUT_TIME'])
    transitions = [{'priorRowOrdinal': a[0], 'rowOrdinal': b[0]} for a, b in zip(membership, membership[1:]) if a[1] != b[1]]
    both = any(x[1] for x in membership) and any(not x[1] for x in membership)
    c.criterion('Naturally loaded inside/outside session discriminator', both, 'UNDECIDED', None if both else 'Both membership states do not occur in the bounded native block')
    c.criterion('Naturally loaded membership transition', bool(transitions), 'UNDECIDED', None if transitions else 'No actual membership transition observed in the bounded block', transitions)
    c.criterion('Actual own-source day-boundary witness', bool(day_boundaries), 'UNDECIDED', None if day_boundaries else 'No native DAY_OPEN transition in the bounded block; actual cells remain observed', day_boundaries)
    c.criterion('Actual own-source week-boundary witness', bool(week_boundaries), 'UNDECIDED', None if week_boundaries else 'No native WEEK_CHANGE1 in the bounded block; actual zeros remain observed', week_boundaries)
    c.criterion('Actual market bars on a DST transition date', False, cause='Deferred; the fixed timestamp conversions are source literals, not date-selected market bars')
