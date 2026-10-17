import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
CHANNELS = ['R', 'G', 'B', 'T', 'NA']
ROUTES = ['LITERAL_RGB', 'LITERAL_NEW', 'SERIES_RGB', 'SERIES_NEW']
VALUES = ['CAST', 'VAR', 'ARRAY', 'HISTORY', 'CAST_HISTORY', 'NZ_DEFAULT', 'NZ_REPLACEMENT', 'GRAD_CAST', 'GRAD_NA']


def number(raw):
    try:
        return F(raw)
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def half_up(value):
    return (2 * value.numerator + value.denominator) // (2 * value.denominator)


def analyze(revision=1):
    inventory = json.loads((BASE / f'attempt-inventory-v{revision}.json').read_text())
    manifest = json.loads((ROOT / 'v98/bundle-manifest-v1.json').read_text())
    inventory['attempts']=[a for a in inventory['attempts'] if a['source']['sourceId']=='v98-color-constructors-v6']
    reports = []
    for attempt in inventory['attempts']:
        source = attempt['source']
        asset = next(a for a in manifest['sources'] if a['sourceId'] == source['sourceId'])
        report = dict(sourceId=asset['sourceId'], sourceSha256=asset['sha256'], pineVersion=asset['pineVersion'], admissionObserved=True, nativeCompileSuccess=source['nativeCompileSuccess'], rows=[], propertyVerdicts=[], facets=[])
        reports.append(report)
        if not attempt['sessions']:
            report['facets'].append(dict(facet='Source-bound numeric vectors', captureStatus='NOT OBSERVED', verdict='UNDECIDED', cause=attempt['status']))
            continue
        session = attempt['sessions'][0]
        raw = list(csv.reader((ROOT / session['csv']['path']).open(newline='')))
        headers, data = raw[0], raw[1:]
        bindings = json.loads((ROOT / session['columnBindings']['path']).read_text())
        owned = {c['originalHeader'] for c in bindings['columns'] if c.get('owner') == source['privateScriptId'] and c['bindingStatus'] == 'OBSERVED'}
        selected = session['selectedFirst64ConsecutiveClosedRows']
        counts = defaultdict(Counter)

        def point(n, title):
            if title not in headers or n < 1 or n > len(data):
                return None
            col = headers.index(title)
            return dict(csvSha256=session['csv']['sha256'], rowOrdinal=n, columnOrdinal=col+1, headerRaw=title, valueRaw=data[n-1][col])

        def value(n, title):
            p = point(n, title)
            return number(p['valueRaw']) if p else None

        def comparison(n, model, predictions, inputs=(), dependencies=(), raw_expected=False, cause=None):
            cells = [point(n, title) for title in predictions]
            parts = []
            for title, expected in predictions.items():
                p = point(n, title)
                actual = p['valueRaw'] if p and raw_expected else number(p['valueRaw']) if p else None
                if title not in owned or p is None or expected == 'UNDECIDED':
                    parts.append('UNDECIDED')
                elif raw_expected:
                    parts.append('SUPPORTED' if actual == expected else 'REFUTED')
                elif expected is None:
                    parts.append('SUPPORTED' if p['valueRaw'] == '' else 'REFUTED')
                elif actual == F(expected):
                    parts.append('SUPPORTED')
                elif actual is not None and actual.denominator != 1 and title.endswith('_T'):
                    parts.append('UNDECIDED')
                else:
                    parts.append('REFUTED')
            verdict = 'REFUTED' if 'REFUTED' in parts else 'UNDECIDED' if 'UNDECIDED' in parts else 'SUPPORTED'
            counts[model].update([verdict])
            return dict(model=model, nativeCells=cells, inputCells=[point(n,t) for t in inputs], dependencyCells=list(dependencies), predictions={k: str(v) if isinstance(v,F) else v for k,v in predictions.items()}, rawStringPrediction=raw_expected, cellVerdicts=parts, verdict=verdict, captureStatus='CAPTURED' if all(p is not None and p['headerRaw'] in owned for p in cells) else 'PARTIAL / NOT OBSERVED', cause=cause, precisionPolicy='Exact integer flags and raw strings; discrepant fractional T with unresolved export precision is UNDECIDED, never rounded or fitted')

        report.update(csv=session['csv'], columnBindings=session['columnBindings'], closureMask=session['closureMask'], selectedDataRowOrdinals=selected, historyPredecessorDataRowOrdinal=session['historyPredecessorDataRowOrdinal'], originalRowsRetained=session['dataRows'], primaryUniquePlotCells=len(selected)*len(owned), scope='One unchanged source execution; source/input/physical closure only selects rows; contrary getters, blanks and -1 codes retained')
        report['facets'].append(dict(facet='Earliest64 phase-zero independently closed consecutive own rows', captureStatus='CAPTURED' if len(selected)==64 else 'NOT OBSERVED', verdict='SUPPORTED' if len(selected)==64 else 'UNDECIDED', cause=None if len(selected)==64 else 'Insufficient eligible natural rows or predecessor'))
        for n in selected:
            phase = int(value(n,'CASE_ID'))
            row = dict(rowOrdinal=n, timeRaw=data[n-1][0], allRequestedRawCells=[point(n,p['title']) for p in asset['plots']], nativeContextCells=[point(n,t) for t in ['time','INPUT_INDEX','INPUT_TIME','CHART_CONFIRMED','CASE_ID']], comparisons=[])
            entries = row['comparisons']
            controls = ['EQ_LITERAL_SELF','EQ_LITERAL_DISTINCT'] if asset['item']==1 else ['EQ_PRESENT_SELF','EQ_PRESENT_DISTINCT']
            entries.append(comparison(n,'PRESENT_LITERAL_SELF_DISTINCT_CALIBRATION',dict(zip(controls,[1,0]))))
            if asset['item'] == 1:
                case = manifest['constructorCases'][phase]
                t = F(case['transparencyRaw'])
                a = (100-t)*255/100
                predicted = dict(BYTE_ROUND=half_up(a),BYTE_FLOOR=a.numerator//a.denominator,PERCENT_ROUND_THEN_BYTE_ROUND=half_up((100-half_up(t))*F(255,100)),PERCENT_CEIL_THEN_BYTE_ROUND=half_up((100-(-(-t.numerator//t.denominator)))*F(255,100)))
                assert predicted == case['candidatePredictedAlphaLabel']
                entries.append(comparison(n,'FROZEN_INPUT_TRANSPARENCY_AND_PALETTE_LABEL',dict(TRANSP_INPUT=t,C0_ALPHA_LABEL=case['literalAlphaLabels'][0]),['CASE_ID','INPUT_INDEX']))
                palette = [f'C{j}_T' for j in range(5)]
                adjacent = [f'EQ_C{j}_C{j+1}' for j in range(4)]
                for j, alpha in enumerate(case['literalAlphaLabels']):
                    entries.append(comparison(n,f'PALETTE_C{j}_NEAREST_PERCENT_GETTER_CANDIDATE',{f'C{j}_T':half_up(100-F(alpha*100,255))},['CASE_ID','C0_ALPHA_LABEL']))
                entries.append(comparison(n,'ADJACENT_DISTINCT_STORED_LITERAL_CANDIDATE',{title:0 for title in adjacent},['CASE_ID']+controls))
                row['routes'] = []
                for route in ROUTES:
                    targets = [f'{route}_{c}' for c in CHANNELS]
                    eqs = [f'{route}_EQ_C{j}' for j in range(5)]
                    codes = [value(n,title) for title in eqs]
                    matches = [j for j,code in enumerate(codes) if code==1]
                    outcome = 'BOOLEAN_NA_EQUALITY' if -1 in codes else 'UNEXPECTED_OR_UNAVAILABLE_CODE' if any(c not in [0,1] for c in codes) else 'MULTIPLE_LITERAL_MATCHES' if len(matches)>1 else 'NEITHER_LITERAL' if not matches else 'SINGLE_LITERAL_MATCH'
                    row['routes'].append(dict(route=route,actualTupleCells=[point(n,title) for title in targets],actualEqualityCells=[point(n,title) for title in eqs],equalityObservation=outcome,matchingCandidateIndices=matches,matchingSourceTokens=[case['literals'][j] for j in matches],literalCalibrationGraph=[point(n,title) for title in adjacent+controls+palette],hiddenStoredByte='UNOBSERVED; matching source token is ordinary Pine equality, not hidden storage recovery'))
                    for model, alpha in predicted.items():
                        j = case['literalAlphaLabels'].index(alpha)
                        prediction={f'{route}_R':33,f'{route}_G':66,f'{route}_B':99,f'{route}_T':half_up(100-F(alpha*100,255)),f'{route}_NA':0}
                        prediction.update({title:int(k==j) for k,title in enumerate(eqs)})
                        prediction.update({title:0 for title in adjacent})
                        prediction.update(EQ_LITERAL_SELF=1,EQ_LITERAL_DISTINCT=0)
                        prediction.update({f'C{k}_T':half_up(100-F(a0*100,255)) for k,a0 in enumerate(case['literalAlphaLabels'])})
                        entries.append(comparison(n,route+'/'+model,prediction,['CASE_ID','TRANSP_INPUT','C0_ALPHA_LABEL'],cause='Frozen full tuple/equality/getter/calibration conjunction; no post-capture quantizer. Integer contradictions refute even if another component has precision uncertainty.'))
                for title in ['RGB_EQ_LITERAL_SERIES','NEW_EQ_LITERAL_SERIES','LITERAL_EQ_RGB_NEW','SERIES_EQ_RGB_NEW']:
                    entries.append(comparison(n,'DIRECT_ROUTE_EQUALITY/'+title,{title:1},controls))
                entries.append(comparison(n,'OLD_RGB12_5_TERNARY_MATCH_DF',{'EXACT_RGB12_5_EQ_DF':1},controls))
                entries.append(comparison(n,'OLD_RGB12_5_DEFINED_EQUALITY_MATCH_DF',{'EXACT_RGB12_5_EQ_DF_CODE':1},controls))
                entries.append(comparison(n,'OLD_TERNARY_VS_NA_PRESERVING_CODE',{'EXACT_RGB12_5_EQ_DF':int(value(n,'EXACT_RGB12_5_EQ_DF_CODE')==1)},['EXACT_RGB12_5_EQ_DF_CODE']))
                row['case'] = case
            else:
                prev=n-1
                row['predecessorRawCells']=[point(prev,p['title']) for p in asset['plots']]
                row['historyInputDependency'] = dict(rowOrdinal=prev,sourceIndex=value(prev,'INPUT_INDEX').numerator,phase=value(prev,'CASE_ID').numerator,currentNa=point(prev,'CURRENT_NA'),indexCells=[point(prev,'INPUT_INDEX'),point(n,'INPUT_INDEX')],timeCells=[point(prev,'INPUT_TIME'),point(n,'INPUT_TIME')])
                tuples={name:[point(n,f'{name}_{c}') for c in CHANNELS] for name in VALUES}
                row['valueTuples']=tuples
                for model, vector, extra in [('A_ORDINARY_MISSING_PROPAGATION',[None,None,None,None,1],{}),('B_PRESENT_TRANSPARENT_BLACK',[0,0,0,100,0],{'CAST_EQ_BLACK100':1}),('C_PRESENT_OPAQUE_BLACK',[0,0,0,0,0],{'CAST_EQ_BLACK0':1}),('D_NON_NA_WITH_BLANK_GETTERS',[None,None,None,None,0],{})]:
                    p={f'CAST_{c}':v for c,v in zip(CHANNELS,vector)}
                    p.update(extra)
                    entries.append(comparison(n,model,p,['CASE_ID']+controls))
                ordinary={}
                for name in ['VAR','ARRAY','CAST_HISTORY']:
                    ordinary.update({f'{name}_{c}':v for c,v in zip(CHANNELS,[None,None,None,None,1])})
                for name,vector in [('NZ_DEFAULT',[0,0,0,100,0]),('NZ_REPLACEMENT',[33,66,99,13,0])]:
                    ordinary.update({f'{name}_{c}':v for c,v in zip(CHANNELS,vector)})
                if int(value(prev,'CASE_ID'))%2==0:
                    ordinary.update({f'HISTORY_{c}':v for c,v in zip(CHANNELS,[None,None,None,None,1])})
                entries.append(comparison(n,'A_ORDINARY_MISSING_TRANSFER_AND_FALLBACK_CANDIDATE',ordinary,['CASE_ID','CAST_NA'],[point(prev,'CASE_ID'),point(prev,'CURRENT_NA')],cause='T13 for literal DF is the explicit nearest-percent getter candidate; fallback identities and cast NA are separate models.'))
                for name in ['VAR','ARRAY']:
                    prediction={f'{name}_{c}':point(n,f'CAST_{c}')['valueRaw'] for c in CHANNELS}
                    entries.append(comparison(n,name+'_RAW_TUPLE_TRANSFER_FROM_CAST',prediction,[f'CAST_{c}' for c in CHANNELS],raw_expected=True))
                entries.append(comparison(n,'CAST_HISTORY_RAW_TUPLE_FROM_ORIGINAL_PREDECESSOR',{f'CAST_HISTORY_{c}':point(prev,f'CAST_{c}')['valueRaw'] for c in CHANNELS},['INPUT_INDEX'],[point(prev,f'CAST_{c}') for c in CHANNELS]+[point(prev,'INPUT_INDEX')],raw_expected=True))
                entries.append(comparison(n,'HISTORY_NA_FROM_ORIGINAL_ALTERNATING_PREDECESSOR',{'HISTORY_NA':point(prev,'CURRENT_NA')['valueRaw']},['CASE_ID','INPUT_INDEX'],[point(prev,'CURRENT_NA'),point(prev,'CASE_ID'),point(prev,'INPUT_INDEX')],raw_expected=True))
                if int(value(prev,'CASE_ID'))%2==0:
                    entries.append(comparison(n,'HISTORY_CAST_BRANCH_RAW_TUPLE_FROM_ORIGINAL_PREDECESSOR',{f'HISTORY_{c}':point(prev,f'CAST_{c}')['valueRaw'] for c in CHANNELS},['CASE_ID'],[point(prev,f'CAST_{c}') for c in CHANNELS]+[point(prev,'CASE_ID')],raw_expected=True))
                else:
                    entries.append(comparison(n,'HISTORY_DF_BRANCH_LITERAL_RGB_AND_NEAREST_PERCENT_GETTER',dict(HISTORY_R=33,HISTORY_G=66,HISTORY_B=99,HISTORY_T=13,HISTORY_NA=0),['CASE_ID'],[point(prev,'CASE_ID'),point(prev,'CURRENT_NA')],cause='Previous selected DF expression is witnessed by original phase/current-NA; no preceding exported DF channel tuple exists. T13 is a separate nearest-percent candidate, not invented previous getter evidence.'))
                for title in ['VAR_EQ_CAST','ARRAY_EQ_CAST','HISTORY_EQ_EXPECTED','CAST_EQ_SELF']:
                    entries.append(comparison(n,'DEFINED_EQUALITY_IDENTITY_CANDIDATE/'+title,{title:1},['CAST_NA','TYPED_NA_NA']+controls,[point(prev,'CASE_ID')] if title=='HISTORY_EQ_EXPECTED' else []))
                for name,vector in [('NZ_DEFAULT',[0,0,0,100,0]),('NZ_REPLACEMENT',[33,66,99,13,0])]:
                    p={f'{name}_{c}':v for c,v in zip(CHANNELS,vector)} if value(n,'CAST_NA')==1 else {f'{name}_{c}':point(n,f'CAST_{c}')['valueRaw'] for c in CHANNELS}
                    entries.append(comparison(n,name+'_NA_PREDICATE_FALLBACK_RELATIONSHIP',p,['CAST_NA']+[f'CAST_{c}' for c in CHANNELS],raw_expected=value(n,'CAST_NA')!=1,cause='Explicit test of whether na predicate and nz recognize the same sentinel; a contradiction never alters either observation.'))
                entries.append(comparison(n,'GRAD_CAST_EQUALS_BARE_NA_COMPLETE_RAW_TUPLE',{f'GRAD_CAST_{c}':point(n,f'GRAD_NA_{c}')['valueRaw'] for c in CHANNELS},[f'GRAD_NA_{c}' for c in CHANNELS],raw_expected=True))
                entries.append(comparison(n,'TYPED_NA_PREDICATE_CONTROL',{'TYPED_NA_NA':1},controls))
                entries.append(comparison(n,'OLD_CAST_NA_TERNARY_VS_PRESERVING_CODE',{'EXACT_NA_CAST':int(value(n,'EXACT_NA_CAST_CODE')==1)},['EXACT_NA_CAST_CODE','CAST_NA']))
            report['rows'].append(row)
        report['propertyVerdicts']=[dict(model=model,counts=dict(c),verdict='REFUTED' if c['REFUTED'] else 'UNDECIDED' if c['UNDECIDED'] else 'SUPPORTED') for model,c in sorted(counts.items())]
        report['comparisonCounts']=dict(sum(counts.values(),Counter()))
        report['facets'].append(dict(facet='Hidden storage / generic quantizer / cross-recalculation identity',captureStatus='NOT OBSERVED',verdict='UNDECIDED',cause='Native numeric getters and ordinary source literal equality only; no byte decoding, universal model, engine approval or closure of old holds.'))
    return dict(version=f'v{revision}',requestCommit=inventory['requestCommit'],sources=reports,selectionPolicy=manifest['primarySelection'],pointerCountsAreNotUniqueCells=True)
