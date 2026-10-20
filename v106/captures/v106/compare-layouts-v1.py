import json
import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
HELPERS=runpy.run_path(str(BASE/'package-evidence-v1.py'))
ref,put=HELPERS['ref'],HELPERS['put']
import re


def signature(text):
    return dict(url=re.search(r'url="([^"]+)"',text)[1],canvas=re.findall(r'Canvas "([^"]+)"',text),checkedRadios=re.findall(r'radio "([^"]+)" checked',text),activeLayout=re.findall(r'button "Logged in as [^"]+ Active layout: ([^"]+)"',text))


def compare():
    before_path=BASE/'environment-v1/native-layout-list-before-response-v1.json'
    after_path=BASE/'environment-v2/native-layout-list-after-response-v1.json'
    before=json.loads(before_path.read_text());after=json.loads(after_path.read_text())
    indexed={r['id']:r for r in after};assert len(before)==21 and len(after)==22
    records=[dict(nativeId=r['id'],name=r['name'],before=r,after=indexed.get(r['id']),equal=r==indexed.get(r['id'])) for r in before]
    tabs=[]
    for page in range(1,18):
        old=BASE/f'environment-v1/page-{page}-before-v1.txt';new=BASE/f'environment-v2/page-{page}-after-v1.txt'
        a,b=signature(old.read_text()),signature(new.read_text())
        tabs.append(dict(pageId=page,beforeEvidence=ref(old),afterEvidence=ref(new),before=a,after=b,equal=a==b))
    creation=json.loads((BASE/'environment-v1/native-layout-create-response-v1.json').read_text())
    assert indexed[creation['id']]['image_url']==creation['image_url'] and creation['id'] not in {r['id'] for r in before}
    result=dict(version='v1',beforeSavedRecords=ref(before_path),afterSavedRecords=ref(after_path),savedRecordComparisons=records,openTabComparisons=tabs,allBeforeRecordsUnchanged=all(r['equal'] for r in records),allOpenTabSignaturesUnchanged=all(r['equal'] for r in tabs),preservationHolds=[dict(pageId=r['pageId'],cause='Passive before/after context differs; cause UNOBSERVED; no restoration performed') for r in tabs if not r['equal']],onlyNewLayout=indexed[creation['id']],privateLibrary='P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action',oldPrivateScripts='No overwrite/rename/delete action; complete private inventory UNOBSERVED',scope='Full native saved-record equality plus passive URL/chart/context signatures; all historical holds remain held, with no old-context restoration or hidden inspection')
    put(BASE/'environment-v2/existing-layout-comparison-v1.json',result)
    return dict(oldSavedRecordsUnchanged=sum(r['equal'] for r in records),oldOpenTabsUnchanged=sum(r['equal'] for r in tabs),preservationHolds=len(result['preservationHolds']),newLayout=creation)


if __name__=='__main__':print(json.dumps(compare(),indent=2))
