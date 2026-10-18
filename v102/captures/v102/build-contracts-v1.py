import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]


def artifact(path):
    raw = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def build():
    manifest = json.loads((ROOT / 'v102/bundle-manifest-v1.json').read_text())
    matrix_path = ROOT / 'v102/CASE-MATRIX-v1.json'
    matrix = json.loads(matrix_path.read_text())
    records = []
    for index, asset in enumerate(manifest['sources']):
        case = matrix['cases'][index]
        assert asset['sourceId'] == case['sourceId']
        family = asset['family']
        constants = {t:str(v) for t,v in case['fixedNumericHypotheses'].items() if isinstance(v,(int,float))}
        constants.update(SCALE_ZERO='0', SCALE_HUNDRED='100', CHART_CONFIRMED='1', VISUAL_ANCHOR_TIME='', VISUAL_ANCHOR_INDEX='')
        intent = {'EXPLICIT_INTENT','TEXT_RECIPE_CODE','WRAP_RECIPE_CODE','FINAL_POSITION_INTENT','EXTEND_RECIPE','STROKE_RECIPE'}
        alternatives = []
        if family in ['stack-false','stack-true']:
            constants.update(BLUE_PLOT='55', FILL_TOP='95', FILL_BOTTOM='5', EXPLICIT_INTENT='1' if family=='stack-true' else '0')
        if family == 'coordinate-render' and asset['pineVersion']==5:
            constants['BOX_TIME_DELTA']=''
        if family == 'box-text-layout':
            constants.update(TEXT_RECIPE_CODE='123', WRAP_RECIPE_CODE='1')
        if family == 'table-relocation':
            constants['FINAL_POSITION_INTENT']='9'
            alternatives.append(dict(id='table-collision-lifecycle', variants=[dict(id='RETAIN',values=dict(COLLISION_DELTA='3',FINAL_DELTA='3',OLD_TABLE_NA='0')),dict(id='INVALIDATE_REPLACE',values=dict(COLLISION_DELTA='2',FINAL_DELTA='2',OLD_TABLE_NA='1'))]))
        if family == 'linefill-sloped':
            alternatives.append(dict(id='same-pair-count-and-old-handle-delete',variants=[dict(id='ADDITIVE_INDEPENDENT',values=dict(SAME_PAIR_COUNT='2',AFTER_OLD_DELETE='1')),dict(id='REPLACEMENT_DISTINCT',values=dict(SAME_PAIR_COUNT='1',AFTER_OLD_DELETE='1')),dict(id='REPLACEMENT_ALIASED',values=dict(SAME_PAIR_COUNT='1',AFTER_OLD_DELETE='0'))]))
        if family == 'line-price':
            alternatives.extend([dict(id='exterior-interpolation',variants=[dict(id='INFINITE',values=dict(LEFT_EXTRAPOLATE='4',RIGHT_EXTRAPOLATE='28',DESC_LEFT='48',DESC_RIGHT='24')),dict(id='CLAMPED_ENDPOINTS',values=dict(LEFT_EXTRAPOLATE='10',RIGHT_EXTRAPOLATE='22',DESC_LEFT='42',DESC_RIGHT='30'))]),dict(id='mutated-slope',variants=[dict(id='UPDATED',values=dict(AFTER_MID='18',AFTER_RIGHT='34')),dict(id='STALE',values=dict(AFTER_MID='16',AFTER_RIGHT='28'))])])
        if family == 'line-price-vertical':
            alternatives.append(dict(id='vertical-price-result',variants=[dict(id='UNDEFINED',values=dict(VERTICAL_PRICE='',VERTICAL_NA='1')),dict(id='FINITE_ENDPOINT20',values=dict(VERTICAL_PRICE='20',VERTICAL_NA='0')),dict(id='FINITE_ENDPOINT40',values=dict(VERTICAL_PRICE='40',VERTICAL_NA='0'))]))
        if family.startswith('format-omitted-'):
            constants['REACHED_AFTER_OMITTED_CALL']='1'
        contracts = {title:[raw]*8 for title,raw in constants.items()}
        contracts['CASE_ID']=[str(p) for p in range(8)]
        if family == 'gap-style-geometry':
            for title,base in dict(LINE_CONTINUOUS=10,LINE_BREAK=20,AREA_CONTINUOUS=35,AREA_BREAK=45,STEP_CONTINUOUS=65,STEP_BREAK=75,DASH_BREAK=30,DOT_STEP_BREAK=85).items():
                if title in {p['title'] for p in asset['plots']}:
                    contracts[title]=['' if p in [3,4] else str(base+p) for p in range(8)]
            contracts['OFFSET_ZERO']=['90' if p==0 else '' for p in range(8)]
            contracts['HOLE_NA']=['1' if p in [3,4] else '0' for p in range(8)]
            alternatives.append(dict(id='offset-export-policy',variants=[dict(id='SOURCE_SERIES',valuesByPhase=dict(OFFSET_PLUS_ONE=['90' if p==0 else '' for p in range(8)])),dict(id='SCREEN_ALIGNED',valuesByPhase=dict(OFFSET_PLUS_ONE=['90' if p==1 else '' for p in range(8)]))]))
        if family == 'extend-stroke':
            contracts['EXTEND_RECIPE']=[str(p%4) for p in range(8)]
            contracts['STROKE_RECIPE']=[str(p%3) for p in range(8)]
        titles={p['title'] for p in asset['plots']}
        assert set(contracts)<=titles
        for item in alternatives:
            for variant in item['variants']:
                if 'values' in variant:
                    variant['valuesByPhase']={t:[v]*8 for t,v in variant.pop('values').items()}
                assert set(variant['valuesByPhase'])<=titles
        records.append(dict(sourceId=asset['sourceId'],source=artifact(ROOT/asset['path']),matrix=artifact(matrix_path),matrixPointer='/cases/'+str(index),contracts=[dict(title=t,sourcePlotOrdinal=next(p['sourcePlotOrdinal'] for p in asset['plots'] if p['title']==t),expectedRawByPhase=values,intentOnly=t in intent,scope='Numeric/blank source contract only; intent/getter never establishes appearance or hidden object identity') for t,values in contracts.items()],alternatives=alternatives,unpredictedRequestedTitles=sorted(titles-set(contracts)-set(t for item in alternatives for v in item['variants'] for t in v['valuesByPhase'])-{'INPUT_INDEX','INPUT_TIME'}),dynamicContextContracts=['INPUT_INDEX: source-owned consecutive integers, minimum200 in primary block','INPUT_TIME: original chart Unix seconds*1000; increasing real timestamps'],scope='Pre-registered request/source/rational hypotheses, frozen before examining this source output; not an engine/native model fit. Primary anchor blanks are explicit source context blanks. Numeric alternative vectors are separate scopes.'))
    return dict(version='v1',status='FROZEN_REQUEST_DERIVATION',sources=records,request=artifact(ROOT/'v102/REQUEST-v102-v1.md'),basis='Exact stated source/rational formulas and finite alternatives in the published v102 request and CASE-MATRIX; no engine output, inferred field, numeric tolerance, pixel outcome or post-capture fitting')


if __name__=='__main__':
    path=BASE/'numeric-contracts-v1.json';content=json.dumps(build(),indent=2)+'\n'
    if path.exists():assert path.read_text()==content
    else:path.write_text(content)
    print('PASS frozen numeric source contracts for25 sources')
