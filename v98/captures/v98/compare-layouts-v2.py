import json
import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
PACKAGE=runpy.run_path(str(BASE/'package-evidence-v3.py'))
ref,put=PACKAGE['ref'],PACKAGE['put']
signature=runpy.run_path(str(BASE/'validate-evidence-v4.py'))['signature']


def compare():
    before_path=BASE/'environment-v1/native-layout-list-before-response-v1.json'
    after_path=BASE/'environment-v2/native-layout-list-after-response-v1.json'
    before=json.loads(before_path.read_text());after=json.loads(after_path.read_text())
    indexed={r['id']:r for r in after}
    records=[dict(nativeId=r['id'],name=r['name'],before=r,after=indexed.get(r['id']),equal=r==indexed.get(r['id'])) for r in before]
    tabs=[]
    for page in range(1,10):
        old=BASE/f'environment-v1/page-{page}-before-v1.txt' if page<9 else BASE/'environment-v1/v97-layout-before-v1.txt'
        new=BASE/f'environment-v2/page-{page}-after-v1.txt'
        a,b=signature(old.read_text()),signature(new.read_text())
        tabs.append(dict(pageId=page,beforeEvidence=ref(old),afterEvidence=ref(new),before=a,after=b,equal=a==b))
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text())
    assert len(before)==13 and len(after)==14
    assert indexed[creation['id']]['image_url']==creation['image_url']
    result=dict(version='v1',beforeSavedRecords=ref(before_path),afterSavedRecords=ref(after_path),savedRecordComparisons=records,openTabComparisons=tabs,allBeforeRecordsUnchanged=all(r['equal'] for r in records),allOpenTabSignaturesUnchanged=all(r['equal'] for r in tabs),preservationHolds=[dict(pageId=r['pageId'],cause='Passive before/after context differs; cause UNOBSERVED; no old layout edit or restoration was performed') for r in tabs if not r['equal']],onlyNewLayout=indexed[creation['id']],privateLibrary='P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1 unchanged; no action',oldPrivateScripts='No overwrite/delete/rename action; full private script inventory UNOBSERVED',scope='Full native saved-record equality plus passive open-tab context signatures. V91 existing saved/open discrepancy preserved. No hidden browser inspection.')
    put(BASE/'environment-v2/existing-layout-comparison-v1.json',result)
    return dict(oldSavedRecordsUnchanged=sum(r['equal'] for r in records),oldOpenTabsUnchanged=sum(r['equal'] for r in tabs),openTabPreservationHolds=sum(not r['equal'] for r in tabs),newLayout=creation)


if __name__=='__main__':
    print(json.dumps(compare(),indent=2))
