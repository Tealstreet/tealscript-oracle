import csv
import hashlib
import json
import runpy
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def reference(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


class Context:
    def __init__(self, asset, session):
        self.asset = asset
        self.session = session
        self.path = ROOT / session['csv']['path']
        raw = list(csv.reader(self.path.open(newline='')))
        self.headers, self.data = raw[0], raw[1:]
        self.columns = {h: i for i, h in enumerate(self.headers)}
        self.rows = {n: dict(zip(self.headers, r)) for n, r in enumerate(self.data, 1)}
        self.closed = [int(m['row_ordinal']) for m in csv.DictReader((ROOT / session['closureMask']['path']).open()) if m['closed_numeric_eligible'] == '1']
        self.by_index = {int(self.rows[n]['INPUT_INDEX']): n for n in self.closed}
        self.records = []
        self.facets = []
        self.block = []
        minimum = asset['minimumConsecutiveClosedRows']
        for start in self.closed:
            if self.rows[start]['PHASE'] != '0':
                continue
            candidate = list(range(start, start + minimum))
            if all(n in self.closed for n in candidate) and all(int(self.rows[n]['INPUT_INDEX']) == int(self.rows[start]['INPUT_INDEX']) + j for j, n in enumerate(candidate)):
                self.block = candidate
                break

    def pointer(self, n, title):
        i = self.columns[title]
        return {'rowOrdinal': n, 'columnOrdinal': i + 1, 'headerRaw': self.headers[i], 'valueRaw': self.data[n - 1][i]}

    def record(self, n, title, model, expected=None, expected_blank=False, precision='EXACT_INTEGER_OR_BINARY_FRACTION', cause=None, input_titles=()):
        actual = self.rows[n][title]
        try:
            numeric_actual = F(actual)
        except (ValueError, ZeroDivisionError):
            numeric_actual = None
        if model == 'NATIVE_TARGET_VECTOR':
            verdict = 'UNDECIDED'
        elif expected_blank:
            verdict = 'SUPPORTED' if actual == '' else 'REFUTED'
        elif actual == '':
            verdict = 'REFUTED'
        elif numeric_actual is None:
            verdict = 'REFUTED'
        elif numeric_actual == expected:
            verdict = 'SUPPORTED'
        else:
            verdict = 'UNDECIDED' if precision == 'EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION' else 'REFUTED'
        item = {'property': title, 'model': model, 'captureStatus': 'CAPTURED', 'verdict': verdict, 'nativeCell': self.pointer(n, title), 'inputCells': [self.pointer(n, t) for t in input_titles], 'predictedRational': str(F(expected)) if expected is not None else None, 'predictedBlank': expected_blank, 'precision': precision, 'cause': cause, 'closedScoringEligible': True, 'nativeNumericParsingStatus': 'FINITE_RATIONAL_STRING' if numeric_actual is not None else 'ORIGINAL_BLANK' if actual == '' else 'ORIGINAL_NONFINITE_OR_NONNUMERIC_STRING'}
        if numeric_actual is not None and expected is not None:
            item['exactExportedStringResidual'] = str(numeric_actual - expected)
        self.records.append(item)
        return item

    def criterion(self, name, observed, verdict='UNDECIDED', cause=None, details=None):
        self.facets.append({'facet': name, 'captureStatus': 'CAPTURED' if observed else 'NOT OBSERVED', 'hypothesisVerdict': verdict if observed else 'UNDECIDED', 'cause': cause, 'details': details})

    def output(self):
        counts = Counter(r['verdict'] for r in self.records)
        summary = []
        for key in sorted({(r['model'], r['property']) for r in self.records}):
            records = [r for r in self.records if (r['model'], r['property']) == key]
            c = Counter(r['verdict'] for r in records)
            verdict = 'REFUTED' if c['REFUTED'] else 'UNDECIDED' if c['UNDECIDED'] else 'SUPPORTED'
            summary.append({'model': key[0], 'property': key[1], 'captureStatus': 'CAPTURED', 'counts': dict(c), 'verdict': verdict})
        return {'sourceId': self.asset['id'], 'sourceSha256': self.asset['sha256'], 'item': self.asset['item'], 'captureStatus': 'CAPTURED', 'csv': reference(self.path), 'columnBindings': self.session['columnBindings'], 'closureMask': self.session['closureMask'], 'selectedBlockDataRowOrdinals': self.block, 'closedRowsAvailable': len(self.closed), 'strictOwnIndexZeroPrefixAvailable': self.session['strictOwnIndexZeroPrefixAvailable'], 'facets': self.facets, 'propertyVerdicts': summary, 'comparisonCounts': dict(counts), 'records': self.records, 'scope': 'Exact source/version and the explicitly keyed native rows only; no engine approval, generic family parity, recovered old frontier or sampling-completeness claim.'}


def analyze(inventory_name, revision):
    inventory = json.loads((BASE / inventory_name).read_text())
    assets = {a['id']: a for a in json.loads((ROOT / 'v95/bundle-manifest-v1.json').read_text())['sources']}
    reports = []
    for attempt in inventory['attempts']:
        asset = assets[attempt['source']['sourceId']]
        if not attempt['sessions']:
            reports.append({'sourceId': asset['id'], 'sourceSha256': asset['sha256'], 'item': asset['item'], 'captureStatus': 'NOT OBSERVED / numeric results', 'nativeAdmission': attempt['status'], 'facets': [{'facet': 'Native numeric result', 'captureStatus': 'NOT OBSERVED', 'hypothesisVerdict': 'UNDECIDED', 'cause': 'Native refusal or unavailable source-bound export; raw diagnostics retained'}]})
            continue
        assert len(attempt['sessions']) == 1 and asset['item'] < 20
        context = Context(asset, attempt['sessions'][0])
        context.criterion('Required consecutive closed row block and all phases0..15', bool(context.block), 'SUPPORTED', None if context.block else 'Naturally exported closed rows do not meet the required block', {'minimumRows': asset['minimumConsecutiveClosedRows'], 'selectedBlock': context.block})
        module = BASE / f'analyze-item{asset["item"]}-v1.py'
        assert module.exists(), 'Missing finite family analyzer: ' + str(module)
        runpy.run_path(str(module))['analyze'](context)
        reports.append(context.output())
    return {'version': f'v{revision}', 'requestCommit': '325b86491f8310806ac214914479d217ea3bb7e4', 'inventory': inventory_name, 'policy': 'Native raw strings and exact rational predictions remain separate. No cell normalization or fitted tolerance. A precision-dependent rational discrepancy remains UNDECIDED with its exact residual. A missing or contrary adequate integer/presence witness is retained as a refutation. All present excluded cells remain in the original CSV and closure masks.', 'sources': reports}
