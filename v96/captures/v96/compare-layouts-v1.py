import json
import runpy
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
helpers = runpy.run_path(str(BASE / 'package-evidence-v1.py'))
ref, put = helpers['ref'], helpers['put']
signature = runpy.run_path(str(BASE / 'validate-evidence-v1.py'))['signature']


def compare():
    before_path = BASE / 'environment-v1/native-layout-list-before-response-v1.json'
    after_path = BASE / 'environment-v2/native-layout-list-after-response-v1.json'
    before = json.loads(before_path.read_text())
    after = json.loads(after_path.read_text())
    indexed = {r['id']: r for r in after}
    records = [{'nativeId': r['id'], 'name': r['name'], 'before': r, 'after': indexed.get(r['id']), 'equal': r == indexed.get(r['id'])} for r in before]
    tabs = []
    for name in ['basic', 'oracle-v90', 'oracle-v91', 'oracle-v92', 'oracle-v93', 'oracle-v94', 'oracle-v95']:
        earlier = ROOT / f'v95/captures/v95/environment-v2/{name}-after-v1.txt'
        if name == 'oracle-v95':
            earlier = BASE / 'environment-v1/v95-layout-before-v1.txt'
        later = BASE / f'environment-v2/{name}-after-v1.txt'
        old, new = signature(earlier.read_bytes()), signature(later.read_bytes())
        tabs.append({'name': name, 'beforeEvidence': ref(earlier), 'afterEvidence': ref(later), 'before': old, 'after': new, 'equal': old == new})
    result = {'version': 'v1', 'allBeforeRecordsUnchanged': all(r['equal'] for r in records), 'allOpenTabSignaturesUnchanged': all(r['equal'] for r in tabs), 'beforeSavedRecords': ref(before_path), 'afterSavedRecords': ref(after_path), 'savedRecordComparisons': records, 'openTabComparisons': tabs, 'scope': 'Full saved-record equality and passive open-tab context signatures; no old saved-layout mutation. V91 pre-existing saved/open discrepancy remains unchanged.', 'privateLibrary': 'sours-lat/P425PrivateV79v1/1 unchanged; no action'}
    assert len(before) == 11 and len(after) == 12
    assert result['allBeforeRecordsUnchanged'] and result['allOpenTabSignaturesUnchanged']
    assert indexed[208235696]['image_url'] == 'SaYl4TD3'
    put(BASE / 'environment-v2/existing-layout-comparison-v1.json', result)
    return {'oldSavedRecordsUnchanged': len(records), 'oldOpenTabSignaturesUnchanged': len(tabs), 'newLayout': indexed[208235696]}


if __name__ == '__main__':
    print(json.dumps(compare(), indent=2))
