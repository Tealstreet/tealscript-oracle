import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[3]
capture = Path(__file__).resolve().parent
checks = {}

def read(name):
    return json.loads((capture / name).read_text())

pins = read('source-preflight-v1.json')['sources']
assert len(pins) == 13
for pin in pins:
    data = (root / pin['path']).read_bytes()
    assert len(data) == pin['bytes']
    assert hashlib.sha256(data).hexdigest() == pin['sha256']
    assert not re.search(rb'^\s*import\s', data, re.M)
    assert not pin['executedInV92']
checks['unchangedImportFreeSourcePins'] = len(pins)

inventory = read('attempt-inventory-v1.json')
for key in ['saveAttempts', 'addAttempts', 'newPrivateScripts', 'nativeCsvDownloads', 'completeCompilerBodies', 'executedSourceFiles']:
    assert inventory[key] == 0
assert inventory['capabilityOnlyAttempts'][0]['compilerDiagnostics'] is None
assert not list(capture.rglob('executed-*.pine'))
assert not list(capture.rglob('*.csv'))
assert (capture / 'realtime-events-v1.jsonl').read_bytes() == b''
assert (capture / 'developing-input-events-v1.jsonl').read_bytes() == b''
checks['unexecutedAndUninventedArtifactClaims'] = 'PASS'

facets = read('facet-capabilities-v1.json')['facets']
assert {item['facet'] for item in facets} == {'a', 'b-unavailable', 'b-available-zero-total', 'c', 'd', 'e'}
references = {}
for facet in facets:
    assert facet['facetVerdict'] == 'NOT OBSERVED'
    assert facet['workflowStatus'] == 'BLOCKED-NEEDS-OWNER-APPROVAL'
    assert facet['closedScoreCredit'] == 0
    assert facet['missingFields'] and facet['sourceSessionIdentity'] is None
    assert facet['capabilityAbsentConclusion'] is False
    for item in facet['evidence']:
        data = (root / item['path']).read_bytes()
        assert len(data) == item['bytes']
        assert hashlib.sha256(data).hexdigest() == item['sha256']
        references[item['path']] = item
checks['independentFacetVerdicts'] = len(facets)
checks['nativeEvidenceHashes'] = len(references)

actions = read('environment-v1/account-actions-v1.json')
assert not actions['connectClicked'] and not actions['modalDismissed']
assert not actions['newThrowawayLayoutCreated']
assert actions['savedLayoutMutations'] == actions['scriptMutations'] == 0
assert actions['library']['actions'] == 0 and not actions['forbiddenActionsTaken']
for item in actions['beforeAfterVisibleContext']:
    assert item['beforeVisibleContext'] == item['afterVisibleContext']
    assert item['afterVisibleContext']['disconnected']
    data = (root / item['after']['path']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['after']['sha256']
checks['preservedExistingLayoutVisibleContexts'] = len(actions['beforeAfterVisibleContext'])

text_files = 0
for path in capture.rglob('*'):
    if not path.is_file() or path.suffix == '.jpg':
        continue
    data = path.read_bytes()
    assert not re.search(rb'(?im)^(?:cookie|set-cookie|authorization):', data), path
    text_files += 1
checks['publicTextAuthenticationHeaderScans'] = text_files

for name in ['footprint-full-distribution-v1.json', 'presence-state-observations-v1.json', 'cumulative-original-frontier-v1.json', 'dxy-execution-input-completeness-v1.json', 'developing-input-context-v1.json']:
    read(name)
checks['familyReports'] = 5
print(json.dumps({'version': 'v1', 'result': 'PASS', 'checks': checks}, indent=2))
