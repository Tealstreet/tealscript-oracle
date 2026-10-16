import csv
import json
import sys
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path


def inspect(path):
    raw = list(csv.reader(Path(path).open(newline='')))
    headers, data = raw[0], raw[1:]
    required = ['INPUT_INDEX', 'INPUT_TIME', 'CHART_CONFIRMED', 'IS_FIRST', 'FIRST_INDEX', 'FIRST_TIME']
    unique = all(headers.count(title) == 1 for title in required)
    rows = [dict(zip(headers, row)) for row in data]
    first = {title: rows[0].get(title) for title in required}
    last = {title: rows[-1].get(title) for title in required}
    candidate = False
    cause = 'SOURCE_OWN_FRONTIER_UNAVAILABLE_OR_NOT_INDEX_ZERO'
    try:
        candidate = unique and len(rows) >= 128 and first['INPUT_INDEX'] == '0' and first['IS_FIRST'] == '1' and first['FIRST_INDEX'] == '0' and F(first['INPUT_TIME']) == F(first['FIRST_TIME']) == F(rows[0]['time']) * 1000
        candidate = candidate and all(F(row['INPUT_INDEX']) == i and F(row['INPUT_TIME']) == F(row['time']) * 1000 and row['IS_FIRST'] == str(int(i == 0)) and row['FIRST_INDEX'] == '0' and row['FIRST_TIME'] == first['FIRST_TIME'] for i, row in enumerate(rows))
        candidate = candidate and all(F(a['time']) < F(b['time']) for a, b in zip(rows, rows[1:]))
        candidate = candidate and F(last['INPUT_INDEX']) + 1 == len(rows)
        cause = None if candidate else 'OWN_INDEX_ZERO_PREFIX_NOT_EXPORTED_OR_FRONTIER_GUARD_UNMET'
    except (ValueError, TypeError, ZeroDivisionError):
        pass
    try:
        requested_date = datetime.fromtimestamp(float(F(first['FIRST_TIME']) / 1000), timezone.utc).date().isoformat()
    except (ValueError, TypeError, OverflowError):
        requested_date = None
    return {'version': 'v1', 'csvPath': str(path), 'dataRows': len(rows), 'originalHeaders': headers, 'firstFrontierRaw': first, 'lastFrontierRaw': last, 'firstTimeRawSeconds': rows[0]['time'], 'lastTimeRawSeconds': rows[-1]['time'], 'preliminaryContiguousOwnIndexZeroCandidate': candidate, 'candidateCause': cause, 'observedOwnFirstTimeDateUtc': requested_date, 'scope': 'Capture navigation decision only. Final source/private metadata ownership, raw pointers and independent closure are separately validated; this preliminary inspection grants no numeric credit.'}


if __name__ == '__main__':
    print(json.dumps(inspect(sys.argv[1]), indent=2))
