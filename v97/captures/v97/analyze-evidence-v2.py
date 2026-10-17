import csv
import json
import runpy
import sys
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
ORIGINAL = runpy.run_path(str(BASE / 'analyze-evidence-v1.py'))['analyze']


def analyze(revision):
    result = ORIGINAL(revision)
    for report in result['sources']:
        if not report.get('strictOwnIndexZeroPrefixAvailable'):
            continue
        raw = list(csv.reader((ROOT / report['csv']['path']).open(newline='')))
        headers, values = raw[0], raw[1:]
        rows = [dict(zip(headers, r)) for r in values[:128]]

        def pointer(i, title):
            col = headers.index(title)
            return {'rowOrdinal': i + 1, 'columnOrdinal': col + 1, 'headerRaw': title, 'valueRaw': values[i][col]}

        if report['item'] == 4:
            groups, current = [], []
            for i, row in enumerate(rows):
                if row['X_NA'] == '1':
                    current.append(i)
                elif current:
                    groups.append(current)
                    current = []
            if current:
                groups.append(current)
            observations = []
            for group in groups:
                targets = []
                for family in ['EMA', 'RMA', 'RSI', 'TSI']:
                    title, flag = family + '_HOLE', family + '_HOLE_NA'
                    finite = next((i for i in range(group[-1] + 1, 128) if rows[i][title] != ''), None)
                    targets.append({'property': title, 'duringInputHole': [{'target': pointer(i, title), 'naWitness': pointer(i, flag)} for i in group], 'targetHadMissingCellsDuringInputHole': any(rows[i][title] == '' for i in group), 'firstFiniteAfterInputHole': pointer(finite, title) if finite is not None else None, 'firstFiniteOwnIndex': finite, 'recoveryNaWitness': pointer(finite, flag) if finite is not None else None, 'captureStatus': 'CAPTURED' if finite is not None else 'NOT OBSERVED', 'cause': None if finite is not None else 'No finite target after this input-hole group inside the declared0..127 block'})
                observations.append({'ownInputHoleIndices': group, 'holeInputCells': [{'input': pointer(i, 'X'), 'naWitness': pointer(i, 'X_NA')} for i in group], 'targets': targets, 'completePriorInputBlock': {'csvSha256': report['csv']['sha256'], 'firstDataRowOrdinal': 1, 'lastDataRowOrdinal': 128, 'ownIndexRange': [0, 127], 'columns': [{'columnOrdinal': headers.index(t) + 1, 'headerRaw': t} for t in ['INPUT_INDEX', 'CLEAN', 'X', 'X_NA', 'CYCLE']]}, 'scope': 'Actual missingness and first finite target after each observed input-hole group; a target that stayed finite is explicitly distinguished from a target recovering from missingness. No output supplies a seed.'})
            report['nativeHoleRecoveryObservations'] = observations
        if report['item'] == 7:
            opportunities = [i for i, row in enumerate(rows) if F(row['INPUT_INDEX']) < F(row['LAG'])]
            report['nativeOwnOriginObservation'] = [pointer(0, t) for t in ['INPUT_INDEX', 'IS_FIRST', 'LAG', 'X', 'DYNAMIC', 'DYNAMIC_NA', 'PRIOR_X', 'PRIOR_PAYLOAD', 'PRIOR_NA']]
            report['facets'].append({'facet': 'Negative dynamic-history dependency before own origin', 'captureStatus': 'CAPTURED' if opportunities else 'NOT OBSERVED', 'hypothesisVerdict': 'UNDECIDED', 'cause': None if opportunities else 'This exact source has lag0 at index0 and no primary index<lag opportunity; complete history cannot manufacture a negative dependency. DYNAMIC_NA1 is not inferred.', 'details': {'actualOpportunityOwnIndices': opportunities, 'ownOriginCells': report['nativeOwnOriginObservation']}})
        if report['item'] == 14:
            pairs = [{'ownIndex': i, 'a': pointer(i, 'RANDOM_A'), 'b': pointer(i, 'RANDOM_B'), 'equalExportedRationals': F(row['RANDOM_A']) == F(row['RANDOM_B'])} for i, row in enumerate(rows)]
            differences = [pair for pair in pairs if not pair['equalExportedRationals']]
            report['seededStreamPrefixObservation'] = {'sourceOwnIndexRange': [0, 127], 'seedLiteral': 7, 'pairs': pairs, 'equalPairCount': len(pairs) - len(differences), 'differentPairCount': len(differences), 'firstDifferentPair': differences[0] if differences else None, 'scope': 'Two actual seed7 call-site vectors from their first calls in one independently certified source/session. Exported numeric equality/difference does not expose a PRNG state/algorithm, certify all seeds or establish hidden precision identity.'}
    return result
