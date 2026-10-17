import runpy
from pathlib import Path

BASE=Path(__file__).resolve().parent
SHARED=runpy.run_path(str(BASE/'numeric-context-v1.py'))
Context=SHARED['Context']
CHANNELS=['R','G','B','T','NA']


def analyze(attempt,asset):
    c=Context(attempt,asset)
    if not c.session:return c.report()
    roles=['CAST','VAR','ARRAY','HISTORY','CAST_HISTORY','TYPED_NA']
    operands={'CAST_EQ_SELF':['CAST_NA'],'VAR_EQ_CAST':['VAR_NA','CAST_NA'],'ARRAY_EQ_CAST':['ARRAY_NA','CAST_NA'],'ARRAY_EQ_SELF':['ARRAY_NA'],'TWIN0_EQ_CAST':['TWIN0_NA','CAST_NA'],'TWINS_EQ':['TWIN0_NA','TWIN1_NA'],'CAST_HISTORY_EQ_CAST':['CAST_HISTORY_NA','CAST_NA'],'CAST_HISTORY_EQ_SELF':['CAST_HISTORY_NA'],'ARRAY_HISTORY_EQ_ARRAY':['ARRAY_HISTORY_NA','ARRAY_NA'],'ARRAY_HISTORY_EQ_CAST_HISTORY':['ARRAY_HISTORY_NA','CAST_HISTORY_NA'],'ARRAY_HISTORY_EQ_SELF':['ARRAY_HISTORY_NA'],'HISTORY_EQ_SELF':['HISTORY_NA'],'HISTORY_EQ_CAST':['HISTORY_NA','CAST_NA'],'HISTORY_EQ_EXPECTED':['HISTORY_NA'],'OBJECT_HISTORY_EQ_CAST_HISTORY':['OBJECT_HISTORY_NA','CAST_HISTORY_NA'],'TYPED_NA_EQ_SELF':['TYPED_NA_NA'],'CAST_EQ_TYPED_NA':['CAST_NA','TYPED_NA_NA'],'ARRAY_EQ_TYPED_NA':['ARRAY_NA','TYPED_NA_NA'],'CAST_EQ_BLACK100':['CAST_NA']}
    selfs=['CAST_EQ_SELF','ARRAY_EQ_SELF','INLINE_ARRAY_SELF_EQ','CAST_HISTORY_EQ_SELF','ARRAY_HISTORY_EQ_SELF','HISTORY_EQ_SELF','TYPED_NA_EQ_SELF']
    for n in c.selected:
        row=c.row(n)
        row['valueTuples']={role:[c.point(n,role+'_'+channel) for channel in CHANNELS] for role in roles}
        row['independentEqualityTargets']=[c.point(n,p['title']) for p in asset['plots'] if '_EQ_' in p['title'] or p['title'].endswith('_EQ')]
        for role in roles:
            flag=role+'_NA'
            c.compare(row,'NA_IMPLIES_BLANK_GETTERS/'+role,{role+'_'+channel:None for channel in CHANNELS[:-1]},[flag],applies=c.value(n,flag)==1,cause='Conditional applies only when this exact exported role has NA1; finite getters then refute. All rows remain in the original selection.')
        for title,flags in operands.items():
            c.compare(row,'NA_IMPLIES_FALSE_EQUALITY/'+title,{title:0},flags,applies=any(c.value(n,flag)==1 for flag in flags),cause='Conditional uses only actually exported predicates of exact operands; an unavailable predicate is never inferred from an alias or getter.')
        for title in ['DIRECT_CAST_PAIR_EQ','INLINE_ARRAY_SELF_EQ']:
            c.compare(row,'NA_IMPLIES_FALSE_EQUALITY/'+title,{title:0},applies=False,cause='Exact inline operands lack exported NA predicates; alias CAST_NA/ARRAY_NA cannot activate this conditional. Raw Boolean remains observed.')
        for title in selfs:c.compare(row,'SELF_EQUALITY_ALWAYS_TRUE/'+title,{title:1})
        tuple_titles=[role+'_'+channel for role in ['CAST','ARRAY'] for channel in CHANNELS]
        complete=all(t in c.owned and c.point(n,t) is not None for t in tuple_titles)
        equal=complete and all(c.point(n,'CAST_'+channel)['valueRaw']==c.point(n,'ARRAY_'+channel)['valueRaw'] for channel in CHANNELS)
        c.compare(row,'EQUAL_COMPLETE_TUPLES_IMPLY_EQUALITY',{'ARRAY_EQ_CAST':1},tuple_titles,applies=equal,cause='Frozen implication test only when both actual full tuples agree; a contrary Boolean refutes it without inventing color identity.')
        c.compare(row,'CAST_HISTORY_RAW_TRANSFER',{'CAST_HISTORY_'+channel:c.point(n-1,'CAST_'+channel)['valueRaw'] for channel in CHANNELS},['INPUT_INDEX'],[c.point(n-1,'CAST_'+channel) for channel in CHANNELS]+[c.point(n-1,'INPUT_INDEX')],raw=True)
        for model,target,prior in [('HISTORY_NA_TRANSFER','HISTORY_NA','CURRENT_NA'),('ARRAY_HISTORY_NA_TRANSFER','ARRAY_HISTORY_NA','ARRAY_NA'),('VAR_HISTORY_NA_TRANSFER','VAR_HISTORY_NA','VAR_NA'),('OBJECT_HISTORY_NA_TRANSFER','OBJECT_HISTORY_NA','ARRAY_NA')]:
            c.compare(row,model,{target:c.point(n-1,prior)['valueRaw']},['INPUT_INDEX','CASE_ID'],[c.point(n-1,prior),c.point(n-1,'INPUT_INDEX'),c.point(n-1,'CASE_ID')],raw=True)
        for twin in ['TWIN0_NA','TWIN1_NA']:c.compare(row,'TWIN_NA_TRANSFER/'+twin,{twin:c.point(n,'CAST_NA')['valueRaw']},['CAST_NA'],raw=True)
        c.compare(row,'PRESENT_LITERAL_SELF_DISTINCT_CALIBRATION',{'EQ_PRESENT_SELF':1,'EQ_PRESENT_DISTINCT':0})
    report=c.report()
    report['unexportedChannels']='Twin, scalar-array/var history and array-object history RGBA channels are UNOBSERVED; only their actually plotted predicates/equalities are retained.'
    report['hiddenIdentityVerdict']='UNDECIDED; incompatible self/missingness/tuple rules remain independently falsifiable, without per-name payload fitting.'
    return report
