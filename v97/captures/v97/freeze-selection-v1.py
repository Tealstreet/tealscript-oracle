import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def ref(path):
    raw = path.read_bytes()
    return {'path': str(path.relative_to(ROOT)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def freeze():
    path = BASE / 'selection-inventory-v1.json'
    assert not path.exists(), 'Selection already frozen'
    manifest = json.loads((ROOT / 'v97/bundle-manifest-v1.json').read_text())
    for artifact in manifest['basisArtifacts']:
        assert ref(ROOT / artifact['path']) == artifact
    published = git('ls-files', 'v95/captures/v95/RESPONSE-v95-v*.md').splitlines()
    response = ROOT / max(published, key=lambda p: int(re.search(r'-v(\d+)\.md$', p)[1]))
    response_text = response.read_text()
    assert 'all40 requested source/version slots returned' in response_text
    assert (ROOT / 'v96/captures/v96/validation-result-v1.json').exists()
    original = (ROOT / 'v95/REQUEST-v95-v1.md').read_text()
    sections = {int(n): text for n, text in re.findall(r'### \((\d+)\)(.*?)(?=\n### |\n## |\Z)', original, re.S)}
    holds = {7: 'Own origin for pre-origin dynamic/history missingness', 10: 'Own origin for pre-origin Boolean/fixnan startup', 14: 'Own index-zero prefix for seeded random stream replay'}
    skip = {6: 'Incomplete preceding anchor and fractional math are distinct from own-origin seed holds', 8: 'Missing natural transitions/DST-date opportunity; not an omitted-own-zero seed facet', 9: 'Old unanchored original frontier is outside this fresh anchored-source contract', 11: 'Bounded alias/copy controls captured; no explicit own-origin hold', 12: 'Fractional precision and observed missing percentile are not own-origin holds', 13: 'Declared defaults captured; no explicit own-origin hold', 15: 'Bounded formatting captured; no explicit own-origin hold', 16: 'Bounded string operations captured; no explicit own-origin hold', 17: 'Unplotted merged-array full count cannot be supplied by an origin load', 18: 'Runtime RE10094 and blank source plots; not an own-origin seed hold', 19: 'Precision and nondiscriminating orientation; not an own-origin seed hold', 20: 'Missed first live events and unobserved execution identity cannot be recreated by closed history'}
    records = []
    for asset in manifest['sources']:
        item = asset['v95Item']
        assert ref(ROOT / asset['path']) == {k: asset[k] for k in ['path', 'bytes', 'sha256']}
        assert not re.search(rb'^\s*import\s', (ROOT / asset['path']).read_bytes(), re.M)
        numeric_path = ROOT / f"v95/captures/v95/{asset['id']}/attempt-v1/numeric-results-v1.json"
        numeric = json.loads(numeric_path.read_text())
        facets = numeric['facets']
        citations = []
        if item <= 5:
            eligible = True
            reason = 'REQUIRED / explicit v97 items2–5 mandate and own-prefix hold'
            selected = [(i, f) for i, f in enumerate(facets) if f['captureStatus'].startswith('NOT OBSERVED') and ('own' in f['facet'].lower())]
        elif item in holds:
            eligible = True
            reason = 'ACTIVATED / exact completed v95 own-origin hold'
            selected = [(i, f) for i, f in enumerate(facets) if f['facet'] == holds[item]]
            assert len(selected) == 1 and selected[0][1]['captureStatus'] == 'NOT OBSERVED'
            assert holds[item] in response_text and selected[0][1]['cause'] in response_text
        else:
            eligible = False
            reason = 'SKIPPED / ' + skip[item]
            selected = []
        for i, facet in selected:
            citations.append({'artifact': ref(numeric_path), 'jsonPointer': f'/facets/{i}', 'exactFacet': facet})
        if eligible:
            assert citations
        records.append({'sourceId': asset['id'].replace('v95-', 'v97-', 1), 'originalSourceId': asset['id'], 'v95Item': item, 'pineVersion': asset['pineVersion'], 'source': ref(ROOT / asset['path']), 'eligible': eligible, 'selectionReason': reason, 'holdCitations': citations, 'reviewedNumericArtifact': ref(numeric_path), 'originalUnchangedCriterion': {'artifact': ref(ROOT / 'v95/REQUEST-v95-v1.md'), 'item': item, 'exactText': '### (' + str(item) + ')' + sections[item]}})
    result = {'version': 'v1', 'frozenAtUtc': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'), 'repositoryCommitAtSelection': git('rev-parse', 'HEAD'), 'requestCommit': 'b8803b5c985d2b415bf2d6f9c5c5f8f3ddb5b260', 'publishedV95Response': ref(response), 'publishedV95ResponseCommit': git('log', '-1', '--format=%H', '--', str(response.relative_to(ROOT))), 'publishedV95ResponseOriginSection': response_text.split('## Explicit own-origin holds for subsequent request selection')[1].split('## Evidence, preservation and audit')[0], 'v96CompletedReturn': ref(ROOT / 'v96/captures/v96/RESPONSE-v96-v1.md'), 'v96CompletedReturnCommit': git('log', '-1', '--format=%H', '--', 'v96/captures/v96/RESPONSE-v96-v1.md'), 'mandatorySlots': 8, 'activatedConditionalSlots': 6, 'skippedConditionalReservations': 24, 'selectedSourceSlots': 14, 'maximumSaves': 14, 'maximumAdds': 14, 'maximumCalendarSelections': 14, 'maximumOriginalCsvs': 28, 'maximumCalculationSessions': 28, 'sourceRetries': 0, 'inputVariants': 0, 'newPineSources': 0, 'records': records}
    assert sum(r['eligible'] for r in records) == 14
    path.write_text(json.dumps(result, indent=2) + '\n')
    return {'selectedSourceSlots': 14, 'response': str(response.relative_to(ROOT)), 'responseCommit': result['publishedV95ResponseCommit']}


if __name__ == '__main__':
    print(json.dumps(freeze(), indent=2))
