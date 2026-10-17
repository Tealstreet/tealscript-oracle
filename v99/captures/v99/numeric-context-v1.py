import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent


def number(raw):
    try:return F(raw)
    except (ValueError,TypeError,ZeroDivisionError):return None


class Context:
    def __init__(self,attempt,asset):
        self.attempt,self.asset=attempt,asset
        self.source=attempt['source']
        self.session=attempt['sessions'][0] if attempt['sessions'] else None
        self.counts=defaultdict(Counter)
        self.applicable=defaultdict(Counter)
        self.rows=[]
        if not self.session:return
        raw=list(csv.reader((ROOT/self.session['csv']['path']).open(newline='')))
        self.headers,self.data=raw[0],raw[1:]
        bindings=json.loads((ROOT/self.session['columnBindings']['path']).read_text())
        self.owned={c['originalHeader'] for c in bindings['columns'] if c.get('owner')==self.source['privateScriptId'] and c['bindingStatus']=='OBSERVED'}
        self.selected=self.session['selectedFirst64ConsecutiveClosedRows']

    def point(self,n,title):
        if title not in self.headers or not 1<=n<=len(self.data):return None
        c=self.headers.index(title)
        return dict(csvSha256=self.session['csv']['sha256'],rowOrdinal=n,columnOrdinal=c+1,headerRaw=title,valueRaw=self.data[n-1][c])

    def value(self,n,title):
        p=self.point(n,title)
        return number(p['valueRaw']) if p else None

    def row(self,n):
        r=dict(rowOrdinal=n,timeRaw=self.data[n-1][0],allRequestedRawCells=[self.point(n,p['title']) for p in self.asset['plots']],nativeContextCells=[self.point(n,t) for t in ['time','INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED'] if t in self.headers],comparisons=[])
        if self.asset.get('requiresOriginalClosedPredecessor'):
            r['predecessorRawCells']=[self.point(n-1,p['title']) for p in self.asset['plots']]
            r['originalPredecessor']=dict(rowOrdinal=n-1,contextCells=[self.point(n-1,t) for t in ['INPUT_INDEX','INPUT_TIME','CASE_ID','CURRENT_NA'] if t in self.headers])
        self.rows.append(r)
        return r

    def compare(self,row,model,predictions,inputs=(),dependencies=(),raw=False,applies=True,cause=None):
        n=row['rowOrdinal'];points=[self.point(n,t) for t in predictions];parts=[]
        for title,expected in predictions.items():
            p=self.point(n,title)
            if p is None or title not in self.owned:parts.append('UNDECIDED')
            elif expected=='UNDECIDED':parts.append('UNDECIDED')
            elif raw:parts.append('SUPPORTED' if p['valueRaw']==expected else 'REFUTED')
            elif expected is None:parts.append('SUPPORTED' if p['valueRaw']=='' else 'REFUTED')
            else:parts.append('SUPPORTED' if number(p['valueRaw'])==F(expected) else 'REFUTED')
        scalar='REFUTED' if 'REFUTED' in parts else 'UNDECIDED' if 'UNDECIDED' in parts else 'SUPPORTED'
        verdict=scalar if applies else 'UNDECIDED'
        self.counts[model].update([verdict])
        if applies:self.applicable[model].update([verdict])
        record=dict(model=model,nativeCells=points,inputCells=[self.point(n,t) for t in inputs],dependencyCells=list(dependencies),predictions={k:str(v) if isinstance(v,F) else v for k,v in predictions.items()},rawStringPrediction=raw,cellVerdicts=parts,rawScalarRelationshipVerdict=scalar,verdict=verdict,modelApplicable=applies,captureStatus='CAPTURED' if all(p is not None and p['headerRaw'] in self.owned for p in points) else 'PARTIAL / NOT OBSERVED',cause=cause,selectionIndependentOfOutputs=True)
        row['comparisons'].append(record)
        return record

    def report(self):
        r=dict(sourceId=self.asset['sourceId'],sourceSha256=self.asset['sha256'],pineVersion=self.asset['pineVersion'],admissionObserved=self.source['nativeCompileSuccess'] is not None,nativeCompileSuccess=self.source['nativeCompileSuccess'],rows=self.rows,propertyVerdicts=[],facets=[])
        if not self.session:
            r['facets'].append(dict(facet='Numeric source vectors',captureStatus='NOT OBSERVED',verdict='UNDECIDED',cause=self.attempt['status']))
            return r
        r.update(csv=self.session['csv'],columnBindings=self.session['columnBindings'],closureMask=self.session['closureMask'],selectedDataRowOrdinals=self.selected,historyPredecessorDataRowOrdinal=self.session['historyPredecessorDataRowOrdinal'],originalRowsRetained=self.session['dataRows'],primaryUniquePlotCells=len(self.selected)*len(self.owned),comparisonCounts=dict(sum(self.counts.values(),Counter())))
        for model,counts in sorted(self.counts.items()):
            actual=self.applicable[model]
            verdict='REFUTED' if actual['REFUTED'] else 'UNDECIDED' if actual['UNDECIDED'] or not actual else 'SUPPORTED'
            r['propertyVerdicts'].append(dict(model=model,counts=dict(counts),applicableCounts=dict(actual),verdict=verdict))
        r['facets']=[dict(facet='Frozen64-row coverage',captureStatus='CAPTURED' if len(self.selected)==64 else 'NOT OBSERVED',verdict='SUPPORTED' if len(self.selected)==64 else 'UNDECIDED'),dict(facet='Hidden color storage, universal equality, cross-recalculation identity and var own-zero initialization',captureStatus='NOT OBSERVED',verdict='UNDECIDED',cause='Bounded same-source exports only; no decoder, fitted policy, source variant or engine approval')]
        return r


def classify(verdicts):
    supported=[k for k,v in verdicts.items() if v=='SUPPORTED']
    return dict(frozenModelVerdicts=verdicts,supportedFrozenModels=supported,observation='ONLY_FROZEN_MODEL' if len(supported)==1 else 'MULTIPLE_FROZEN_MODELS' if supported else 'NEITHER_MODEL' if verdicts and all(v=='REFUTED' for v in verdicts.values()) else 'UNDECIDED',hiddenModel='UNDECIDED; finite source expressions only')
