import csv
import hashlib
import io
import json
import sys
from datetime import datetime
from fractions import Fraction as F
from pathlib import Path

root=Path('/Users/samuelsteady/cs/tealscript-oracle')
config=json.load(sys.stdin)
base=root/config['directory'];path=base/'chart-native-v1.csv'
asset=next(a for a in json.loads((root/'v95/bundle-manifest-v1.json').read_text())['sources']if a['id']==config['sourceId'])
source_dir=root/'v95/captures/v95'/asset['id']/'attempt-v1'
meta=json.loads((source_dir/'add-response-v1.json').read_text())['result']['metaInfo']
assert meta['scriptIdPart']==config['privateId'] and meta['pine']['version']=='1.0'
assert hashlib.sha256((source_dir/'executed-v1.pine').read_bytes()).hexdigest()==asset['sha256']
raw=list(csv.reader(path.read_bytes().decode('utf-8-sig').splitlines()));headers,data=raw[0],raw[1:]
columns=[];named={};unresolved=[]
requested={p['title']:p['sourcePlotOrdinal']for p in asset['plotColumns']}

def ref(p):
 b=p.read_bytes();return {'path':str(p.relative_to(root)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,obj):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(obj,indent=2)+'\n')
def number(value):
 try:return F(value)
 except (TypeError,ValueError,ZeroDivisionError):return None

for n,h in enumerate(headers,1):
 c={'columnOrdinal':n,'originalHeader':h}
 if n<=5:
  assert h==['time','open','high','low','close'][n-1];c.update(owner='Native main chart',bindingStatus='OBSERVED')
 elif h=='Volume' and h not in requested:c.update(owner='Native builtin Vol · BTC',bindingStatus='OBSERVED')
 else:
  candidates=[pid for pid,s in meta['styles'].items()if s.get('title')==h]
  if len(candidates)==1 and headers.count(h)==1 and h in requested:
   c.update(owner=meta['scriptIdPart'],privateVersion='1.0',sourceSha256=asset['sha256'],nativePlotId=candidates[0],sourceLiteralPlotOrdinal=requested[h],bindingStatus='OBSERVED');named[h]=n-1
  else:c.update(owner=None,candidateNativePlotIds=candidates,bindingStatus='UNOBSERVED / ownership unresolved');unresolved.append(n)
 columns.append(c)
missing=[h for h in requested if h not in named]
bindings={'version':'v1','sourceId':asset['id'],'sourceSha256':asset['sha256'],'privateId':meta['scriptIdPart'],'privateVersion':'1.0','csv':ref(path),'columns':columns,'unresolvedColumnOrdinals':unresolved,'missingOrAmbiguousRequestedPlotTitles':missing,'nativeExposedPlotMetadata':meta.get('plots'),'sourceSessionIdentity':config['sourceSessionIdentity'],'inputChanges':0,'snapshotIsAdditionalCalculationSession':None,'calculationContinuityStatus':'UNOBSERVED in a single sample; checked across raw clock/state witnesses without assuming runtime continuity','instanceId':None,'instanceIdStatus':'UNOBSERVED; exact private-version, metadata, native ownership UI and fresh download clocks independently bind the CSV'}
write(base/'column-bindings-v1.json',bindings)
download=json.loads((base/'chart-download-v1.json').read_text());clock=download['exportTrigger']['startedAtUtc'];epoch=datetime.fromisoformat(clock.replace('Z','+00:00')).timestamp()
assert download['sha256']==bindings['csv']['sha256'] and epoch<=download['downloadModifiedAtEpoch']
window=config['window'];target=F(window['barCloseEpochMs']if config['requestedKind']=='NEXT_BAR_FIRST'else window['barOpenEpochMs'])
out=io.StringIO(newline='');writer=csv.writer(out,lineterminator='\n');writer.writerow(['csv_sha256','row_ordinal','time_raw_seconds','input_time_raw_ms','input_index_raw','native_confirmed_raw','export_utc','physical_close_epoch','physically_closed','closed_numeric_eligible','event_target','present_cell_status','blank_column_ordinals','exclusion_cause'])
closed_baseline=[];tuples=[];hist=[]
for n,row in enumerate(data,1):
 assert len(row)==len(headers)
 def value(h):return row[named[h]]if h in named else None
 own_time=number(value('INPUT_TIME'));own_index=number(value('INPUT_INDEX'));confirmed=value('CHART_CONFIRMED');close=int(row[0])+120
 consistent=own_time==int(row[0])*1000
 physical=close<=epoch and confirmed=='1' and consistent
 event=own_time==target
 baseline=config['sampleOrdinal']==0 and physical and own_time<F(window['barOpenEpochMs']) and not missing
 if baseline:closed_baseline.append(n)
 cause=''if baseline else 'LIVE_OBSERVER_TUPLE_EXCLUDED_FROM_CLOSED_SCORING'if event else 'REPEATED_OBSERVER_SNAPSHOT_EXCLUDED_FROM_CLOSED_SCORING'if config['sampleOrdinal']>0 else 'PHYSICALLY_OPEN_OR_CONTEXT_UNMET'
 writer.writerow([bindings['csv']['sha256'],n,row[0],value('INPUT_TIME'),value('INPUT_INDEX'),confirmed,clock,close,int(physical),int(baseline),int(event),'OBSERVED'if baseline else'OBSERVED / EXCLUDED',json.dumps([i for i,x in enumerate(row,1)if x==''],separators=(',',':')),cause])
 if physical and own_time<F(window['barOpenEpochMs']) and len(hist)<32:hist.append({'rowOrdinal':n,'timeRaw':row[0],'inputIndexRaw':value('INPUT_INDEX'),'clockRaw':value('CLOCK')})
 if event:
  pointers={h:{'rowOrdinal':n,'columnOrdinal':i+1,'headerRaw':headers[i],'valueRaw':row[i]}for h,i in named.items()}
  values={h:p['valueRaw']for h,p in pointers.items()};rt=values.get('IS_REALTIME');history=values.get('IS_HISTORY');new=values.get('IS_NEW')
  event_clock=number(values.get('CLOCK'));completion=datetime.fromisoformat(download['exportTrigger']['completedAtUtc'].replace('Z','+00:00')).timestamp();deadline_met=completion<=window['deadlineEpochMs']/1000;open_clock=event_clock is not None and deadline_met and epoch<window['barCloseEpochMs']/1000;close_clock=event_clock is not None and deadline_met
  classification='OPEN_REALTIME_SAMPLE'if consistent and open_clock and confirmed=='0'and rt=='1'and history=='0'else'ACTUAL_CONFIRMED_REALTIME_CLOSE'if physical and close_clock and rt=='1'and history=='0'else'CLOSED_HISTORICAL_EXPORT'if physical else'CONTEXT_UNMET_TUPLE'
  if config['requestedKind']=='NEXT_BAR_FIRST':classification='NEXT_BAR_FIRST_FLAG_OBSERVED'if consistent and close_clock and confirmed=='0'and rt=='1'and history=='0'and new=='1'else'NEXT_BAR_FIRST_EVENT_MISSED_OR_CONTEXT_UNMET'
  comparisons=[]
  for prop,expected,inputs in [('COMMITTED_DELTA',F(1) if number(values.get('PREVIOUS_COMMITTED')) is not None else None,['PREVIOUS_COMMITTED']),('UDT_DELTA',F(1) if number(values.get('PREVIOUS_ORDINARY')) is not None else None,['PREVIOUS_ORDINARY']),('UDT_STICKY',number(values.get('TICKS')),['TICKS']),('SEEN_TIME',own_time,['INPUT_TIME'])]:
   actual=number(values.get(prop));comparisons.append({'property':prop,'captureStatus':'CAPTURED' if prop in pointers else 'NOT OBSERVED / getter ownership unbound','nativeCell':pointers.get(prop),'inputCells':[pointers.get(h)for h in inputs],'predictedRational':str(expected)if expected is not None else None,'rawRelationshipVerdict':'SUPPORTED'if actual is not None and expected is not None and actual==expected else'REFUTED'if expected is not None else'UNDECIDED','eventCertificateCredit':'PENDING / continuity and full window requirements are checked independently'})
  tuples.append({'rowOrdinal':n,'timeRaw':row[0],'valuesRaw':values,'nativeCellPointers':pointers,'actualClassification':classification,'physicalCloseBoundMet':physical,'ownTimeAgreesWithNativeChartTime':consistent,'presentCellStatus':'OBSERVED / EXCLUDED FROM CLOSED SCORING','sameExecutionAsUiScreenshot':None,'sameExecutionAsUiStatus':'UNOBSERVED; UI/CSV are not equated merely because they share a bar key','rawWithinTupleComparisons':comparisons})
(base/'row-closure-mask-v1.csv').write_text(out.getvalue())
inspection={'version':'v1','sourceId':asset['id'],'sourceSha256':asset['sha256'],'privateId':meta['scriptIdPart'],'privateVersion':'1.0','sourceSessionIdentity':config['sourceSessionIdentity'],'sampleOrdinal':config['sampleOrdinal'],'requestedKind':config['requestedKind'],'targetInputTimeRationalMs':str(target),'window':window,'nativeExportUtc':clock,'csv':ref(path),'columnBindings':ref(base/'column-bindings-v1.json'),'closureMask':ref(base/'row-closure-mask-v1.csv'),'originalDataRows':len(data),'originalColumnCount':len(headers),'first32ClosedBaselineDataRowOrdinals':closed_baseline[:32],'historicalClockWitnesses':hist,'targetTuples':tuples,'requiredGetterBindingStatus':'CAPTURED'if not missing and not unresolved else'NOT OBSERVED / source ownership or getter fields unbound','eventTargetTupleStatus':'CAPTURED'if len(tuples)==1 and not missing else'NOT OBSERVED / target absent, ambiguous or unbound','sampleConfig':config,'residualScope':'Own-source sampled relationships only. No intervening-event completeness, old clocks, requested-provider as-of identity, original execution or generic live parity.'}
write(base/'sample-inspection-v1.json',inspection)
print(json.dumps({'inspection':ref(base/'sample-inspection-v1.json'),'sourceId':asset['id'],'sampleOrdinal':config['sampleOrdinal'],'requestedKind':config['requestedKind'],'csv':inspection['csv'],'bindingStatus':inspection['requiredGetterBindingStatus'],'targetStatus':inspection['eventTargetTupleStatus'],'targetTuples':tuples,'historicalClockWitnesses':hist,'baselineRows':len(closed_baseline[:32])}))
