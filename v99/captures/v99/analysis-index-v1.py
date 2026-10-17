import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]


def ref(path):
    raw=path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def compact(numeric):
    index={k:v for k,v in numeric.items() if k not in ['sources','sixCaseDirectComparisonPolicies']}
    index['format']='per-source-index-v1'
    index['sources']=[]
    for report in numeric['sources']:
        entry={k:v for k,v in report.items() if k not in ['rows','baselinePhaseGroupCertificates']}
        entry.update(numericResults=ref(BASE/report['sourceId']/'numeric-results-v1.json'),rowRecordCount=len(report['rows']),completeReportKeys=sorted(report))
        index['sources'].append(entry)
    index['sixCaseDirectComparisonPolicies']={route:{k:v for k,v in proof.items() if k!='sourceCertificates'} for route,proof in numeric['sixCaseDirectComparisonPolicies'].items()}
    index['sixCaseDirectCertificate']=ref(BASE/'direct-six-case-certificate-v1.json')
    return index


def hydrate(index):
    if index.get('format')!='per-source-index-v1':return index
    def bound(reference):
        raw=(ROOT/reference['path']).read_bytes()
        assert len(raw)==reference['bytes'] and hashlib.sha256(raw).hexdigest()==reference['sha256']
        return json.loads(raw)
    numeric={k:v for k,v in index.items() if k not in ['format','sources','sixCaseDirectCertificate']}
    numeric['sources']=[]
    for entry in index['sources']:
        report=bound(entry['numericResults'])
        assert len(report['rows'])==entry['rowRecordCount'] and sorted(report)==entry['completeReportKeys']
        assert all(report[k]==v for k,v in entry.items() if k not in ['numericResults','rowRecordCount','completeReportKeys'])
        numeric['sources'].append(report)
    numeric['sixCaseDirectComparisonPolicies']=bound(index['sixCaseDirectCertificate'])['policies']
    assert {route:{k:v for k,v in proof.items() if k!='sourceCertificates'} for route,proof in numeric['sixCaseDirectComparisonPolicies'].items()}==index['sixCaseDirectComparisonPolicies']
    return numeric
