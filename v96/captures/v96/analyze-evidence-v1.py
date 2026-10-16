import csv
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def number(value):
    try:
        return F(value)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def analyze(revision=1):
    inventory = json.loads((BASE / f'attempt-inventory-v{revision}.json').read_text())
    manifest = json.loads((ROOT / 'v96/bundle-manifest-v1.json').read_text())
    reports = []
    for attempt in inventory['attempts']:
        source = attempt['source']
        report = {'sourceId': source['sourceId'], 'sourceSha256': source['sourceSha256'], 'captureStatus': 'NATIVE ADMISSION OBSERVED / numeric prerequisites evaluated separately', 'nativeCompileSuccess': source['nativeCompileSuccess'], 'propertyVerdicts': [], 'rows': [], 'facets': []}
        if not attempt['sessions']:
            report['facets'].append({'facet': 'Source-bound numeric results', 'captureStatus': 'NOT OBSERVED', 'hypothesisVerdict': 'UNDECIDED', 'cause': attempt['status']})
            reports.append(report)
            continue
        assert len(attempt['sessions']) == 1
        session = attempt['sessions'][0]
        raw = list(csv.reader((ROOT / session['csv']['path']).open(newline='')))
        headers, data = raw[0], raw[1:]
        bindings = json.loads((ROOT / session['columnBindings']['path']).read_text())
        owned = {c['originalHeader'] for c in bindings['columns'] if c.get('owner') == source['privateScriptId'] and c['bindingStatus'] == 'OBSERVED'}
        selected = session['selectedFirst32ConsecutiveClosedRows']
        report.update(csv=session['csv'], columnBindings=session['columnBindings'], closureMask=session['closureMask'], selectedDataRowOrdinals=selected, allOriginalRowsRetained=True, scope='Frozen five cases and controls on the same explicit first32 closed rows; no storage decoding, output-presence filtering, fitted quantizer, byte inference from T alone or universal algorithm claim')
        report['facets'].append({'facet': 'First32 consecutive source-bound independently closed rows', 'captureStatus': 'CAPTURED' if len(selected) == 32 else 'NOT OBSERVED', 'hypothesisVerdict': 'SUPPORTED' if len(selected) == 32 else 'UNDECIDED', 'cause': None if len(selected) == 32 else 'Insufficient naturally available closed source rows'})
        counts, statuses = {}, {}

        def point(n, title):
            if title not in headers:
                return None
            col = headers.index(title)
            return {'rowOrdinal': n, 'columnOrdinal': col + 1, 'headerRaw': title, 'valueRaw': data[n - 1][col]}

        def compare(n, title, model, expected=None, semantic_ready=True, cause=None, inputs=()):
            pointer = point(n, title)
            captured = title in owned and pointer is not None
            actual = number(pointer['valueRaw']) if pointer else None
            raw_verdict = 'UNDECIDED' if expected is None or not captured else 'SUPPORTED' if actual == expected else 'REFUTED'
            verdict = raw_verdict if semantic_ready else 'UNDECIDED'
            result = {'property': title, 'model': model, 'nativeCell': pointer, 'inputCells': [point(n, t) for t in inputs], 'captureStatus': 'CAPTURED' if captured else 'NOT OBSERVED / exact-source ownership unavailable', 'predictedRational': str(expected) if expected is not None else None, 'verdict': verdict, 'rawScalarRelationshipVerdict': raw_verdict, 'semanticCalibrationAdequate': semantic_ready, 'cause': cause, 'closedScoringEligible': captured and semantic_ready, 'internalPackedRepresentationStatus': 'UNOBSERVED; ordinary Pine literal equality/getters only'}
            counts.setdefault((model, title), Counter())[verdict] += 1
            statuses.setdefault((model, title), Counter())[result['captureStatus']] += 1
            return result

        for n in selected:
            row = dict(zip(headers, data[n - 1]))
            entries, cases = [], []
            basic = all(t in owned for t in ['EQ_SELF', 'EQ_DISTINCT']) and number(row.get('EQ_SELF')) == 1 and number(row.get('EQ_DISTINCT')) == 0
            constructor_ready = all(t in owned for t in ['CTOR12_5_EQ_DF', 'CTOR50_EQ_80']) and number(row.get('CTOR12_5_EQ_DF')) == 1 and number(row.get('CTOR50_EQ_80')) == 1
            controls = {'EQ_SELF': 1, 'EQ_DISTINCT': 0, 'CTOR12_5_EQ_DF': 1, 'CTOR50_EQ_80': 1, 'G12_LOWER_T': 10, 'G12_UPPER_T': 15, 'G22_LOWER_T': 20, 'G22_UPPER_T': 25, 'G32_LOWER_T': 30, 'G32_UPPER_T': 35, 'CLAMP_LOWER_T': 0, 'CLAMP_UPPER_T': 100, 'MISSING_LOWER_NA': 1, 'MISSING_UPPER_T': 0}
            for title, value in controls.items():
                model = 'NOMINAL_ENDPOINT_T_GETTER_CANDIDATE' if title.endswith('_T') else 'FROZEN_EQUALITY_OR_CONSTRUCTOR_CONTROL'
                entries.append(compare(n, title, model, F(value)))
            for title in ['CTOR12_5_T', 'LITERAL_DF_T', 'LITERAL_E0_T', 'LITERAL_DE_T']:
                entries.append(compare(n, title, 'OPEN_NATIVE_CALIBRATION_GETTER_TARGET', cause='Actual getter retained without assuming continuous-alpha or integer-percent conversion'))
            entries.append(compare(n, 'gradient12_5', 'ORIGINAL_COLORED_LINE_CLOSE_VALUE', number(row.get('close')), inputs=['close']))
            for candidate in manifest['candidates']:
                name = candidate['id']
                channels = [name + '_' + c for c in ['R', 'G', 'B', 'T', 'NA']]
                rgb = [int(candidate['floor'][k:k + 2], 16) for k in [1, 3, 5]]
                for channel, value in zip(['R', 'G', 'B', 'NA'], rgb + [0]):
                    entries.append(compare(n, name + '_' + channel, 'FROZEN_LITERAL_RGB_AND_PRESENT_CANDIDATE', F(value)))
                flag_names = [('FLOOR', candidate['floor']), ('HALF_UP', candidate['halfUp'])]
                if candidate['preT'] is not None:
                    flag_names.append(('PRE_T', candidate['preT']))
                flags = {model: number(row.get(name + '_EQ_' + model)) for model, _ in flag_names}
                flag_ownership = all(name + '_EQ_' + model in owned for model, _ in flag_names)
                boolean_flags = all(value in [F(0), F(1)] for value in flags.values())
                present = name + '_NA' in owned and number(row.get(name + '_NA')) == 0
                equality_ready = basic and flag_ownership and boolean_flags
                for model, literal in flag_names:
                    entries.append(compare(n, name + '_EQ_' + model, 'ORDINARY_COLOR_LITERAL_EQUALITY/' + literal, F(1), equality_ready, None if equality_ready else 'Calibrating equality/flag ownership/domain unavailable or contrary; raw flag is still retained', ['EQ_SELF', 'EQ_DISTINCT', name + '_NA']))
                matches = [model for model, value in flags.items() if value == 1]
                observed = 'UNDECIDED / equality calibration or ownership' if not equality_ready else 'NEITHER_LITERAL' if not matches else 'MULTIPLE_LITERALS' if len(matches) > 1 else matches[0] + '_ONLY'
                byte_ready = equality_ready and present and len(matches) == 1
                t_title = name + '_T'
                if name.startswith('G'):
                    base = {'G12': 12, 'G22': 22, 'G32': 32}[name]
                    for model, value in [('FLOOR_ALPHA_NEAREST_PERCENT_GETTER', F(base + 1)), ('HALF_UP_ALPHA_NEAREST_PERCENT_GETTER', F(base)), ('NOMINAL_CONTINUOUS_T_GETTER', F(base) + F(1, 2)), ('ENDPOINT_ALPHA_MIDPOINT_CONTINUOUS_T_GETTER', 100 * (1 - F(candidate['alpha']) / 255))]:
                        entries.append(compare(n, t_title, model, value))
                else:
                    entries.append(compare(n, t_title, 'BOTH_ALPHA_LITERAL_CANDIDATES_CAN_SHOW_T50', F(50), cause='T50 alone is nondiscriminating; missing and present-transparent endpoints stay distinct'))
                cases.append({'case': name, 'frozenInputs': candidate, 'actualChannelCells': [point(n, t) for t in channels], 'actualEqualityCells': {model: point(n, name + '_EQ_' + model) for model, _ in flag_names}, 'equalityObservation': observed, 'literalEqualityCalibrationAdequate': equality_ready, 'constructorControlsMatch': constructor_ready, 'nativePresenceZeroObserved': present, 'literalCandidateVerdict': 'SUPPORTED / ' + matches[0] if byte_ready else 'UNDECIDED / byte facet' if not byte_ready else None, 'constructorPackingControlsVerdict': 'SUPPORTED for these controls' if constructor_ready else 'CONTRARY OR UNOBSERVED; not an exclusion of gradient observations', 'byteFacetCause': None if byte_ready else 'Absent/contrary equality calibration, native missingness, MULTIPLE or NEITHER literal outcome prevents a unique calibrated literal-candidate certificate; actual channels and flags remain observed', 'scope': 'Observed equality to the explicit source literal under these controls, never direct hidden alpha-byte/storage recovery'})
            titles = [p['title'] for p in next(a for a in manifest['sources'] if a['sourceId'] == source['sourceId'])['plots']]
            report['rows'].append({'rowOrdinal': n, 'timeRaw': row['time'], 'allRequestedRawCells': [point(n, title) for title in titles], 'nativeContextCells': [point(n, title) for title in ['time', 'close', 'INPUT_INDEX', 'INPUT_TIME', 'CHART_CONFIRMED']], 'basicEqualityCalibrationAdequate': basic, 'constructorControlsMatch': constructor_ready, 'comparisons': entries, 'cases': cases})
        report['propertyVerdicts'] = [{'model': model, 'property': title, 'captureStatus': 'CAPTURED' if set(statuses[(model, title)]) == {'CAPTURED'} else 'PARTIAL OR NOT OBSERVED / exact ownership unavailable', 'rawCaptureStatusCounts': dict(statuses[(model, title)]), 'counts': dict(values), 'verdict': 'REFUTED' if values['REFUTED'] else 'UNDECIDED' if values['UNDECIDED'] else 'SUPPORTED'} for (model, title), values in sorted(counts.items())]
        report['comparisonCounts'] = dict(sum(counts.values(), Counter()))
        report['facets'].append({'facet': 'Hidden packed color representation and universal alpha quantizer', 'captureStatus': 'NOT OBSERVED', 'hypothesisVerdict': 'UNDECIDED', 'cause': 'Only ordinary literal equality and numeric getters are authorized; no packed decoder, tolerance fitting or generic algorithm certificate'})
        reports.append(report)
    return {'version': f'v{revision}', 'requestCommit': inventory['requestCommit'], 'inventory': f'attempt-inventory-v{revision}.json', 'capturePolicy': 'All five cases and controls use the same first32 eligible rows. Every contrary zero, missing result and calibration contradiction remains an actual observation; no post-result eligibility filter.', 'scope': 'Neither capture nor Git publication approves7f006314, changes application expectations, closes historical holds or certifies raster/byte storage/generic gradient parity.', 'sources': reports}
