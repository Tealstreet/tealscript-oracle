from fractions import Fraction as F


def analyze(c):
    pivot_rows, missing_anchor_rows, complete_anchors, diverging_rows = [], [], [], []
    for n in c.block:
        row = c.rows[n]
        i, p = int(row['INPUT_INDEX']), int(row['PHASE'])
        x = p // 2 if p <= 7 else (15 - p) // 2
        for title, value in [('X', x), ('LEFT', 1 + p % 3), ('RIGHT', 1 + p % 2), ('ANCHOR', p == 0)]:
            c.record(n, title, 'DECLARED_PIVOT_INPUT', F(value), input_titles=['PHASE'])
        for title, field, left, right, high, witness in [('PIVOT_HIGH', 'X', int(row['LEFT']), int(row['RIGHT']), True, 'HIGH_NA'), ('PIVOT_LOW', 'X', int(row['LEFT']), int(row['RIGHT']), False, 'LOW_NA'), ('IMPLICIT_HIGH', 'INPUT_HIGH', 2, 2, True, None), ('IMPLICIT_LOW', 'INPUT_LOW', 2, 2, False, None)]:
            indices = list(range(i - right - left, i + 1))
            deps = [c.by_index.get(j) for j in indices]
            if any(d is None or c.rows[d][field] == '' for d in deps):
                c.criterion('Pivot dependency / ' + title + '/row' + str(n), False, cause='A required own input window is omitted or missing')
                continue
            values = [F(c.rows[d][field]) for d in deps]
            candidate, before, after = values[left], values[:left], values[left + 1:]
            for model in ['LEFTMOST_PLATEAU', 'RIGHTMOST_PLATEAU']:
                strict_left = model == 'LEFTMOST_PLATEAU'
                left_ok = all((candidate > v if strict_left else candidate >= v) if high else (candidate < v if strict_left else candidate <= v) for v in before)
                right_ok = all((candidate >= v if strict_left else candidate > v) if high else (candidate <= v if strict_left else candidate < v) for v in after)
                present = left_ok and right_ok
                r = c.record(n, title, model + '_CURRENT_CONFIRMATION_ROW', candidate if present else None, expected_blank=not present, input_titles=['INPUT_INDEX'] + (['LEFT', 'RIGHT'] if witness else []))
                r['strengths'] = {'left': left, 'right': right, 'binding': 'Own source series' if witness else 'Frozen literal2/2 implicit high/low overload'}
                r['dependencyCells'] = [c.pointer(d, field) for d in deps]
                if witness:
                    c.record(n, witness, model + '_CURRENT_CONFIRMATION_ROW', F(not present))
            pivot_rows.append(n)
        for title in ['LEVEL_COUNT', 'DEV_COUNT']:
            c.record(n, title, 'TRADITIONAL_ELEVEN_BOUNDED_LEVELS', F(11))
        if int(row['LEVEL_COUNT']) > 11 or int(row['DEV_COUNT']) > 11:
            c.criterion('Complete pivot-level array / row' + str(n), False, cause='Native count exceeds11 exported slots; actual count and slots remain observed')
        anchor = i - p
        previous = [c.by_index.get(j) for j in range(anchor - 16, anchor)]
        current = [c.by_index.get(j) for j in range(anchor, i + 1)]
        previous_ok = all(d is not None for d in previous)
        current_ok = all(d is not None for d in current)
        if not previous_ok:
            missing_anchor_rows.append(n)
        elif p == 0:
            complete_anchors.append(n)
        if any(row['LEVEL_' + str(k)] and row['DEV_' + str(k)] and F(row['LEVEL_' + str(k)]) != F(row['DEV_' + str(k)]) for k in range(11)):
            diverging_rows.append(n)
        for prefix, deps, complete in [('LEVEL', previous, previous_ok), ('DEV', current, current_ok)]:
            for k in range(11):
                r = c.record(n, prefix + '_' + str(k), 'NATIVE_TARGET_VECTOR', cause='Every bounded native slot retained; anchor input guard is independent')
                r.update(closedScoringEligible=complete, exclusionCause=None if complete else 'COMPLETE_ANCHOR_INPUT_INTERVAL_NOT_EXPORTED')
            if not complete:
                continue
            h = max(F(c.rows[d]['INPUT_HIGH']) for d in deps)
            l = min(F(c.rows[d]['INPUT_LOW']) for d in deps)
            close = F(c.rows[deps[-1]]['INPUT_CLOSE'])
            pivot = (h + l + close) / 3
            for k, value in enumerate([pivot, 2 * pivot - l, 2 * pivot - h]):
                r = c.record(n, prefix + '_' + str(k), 'TRADITIONAL_BOUND_ANCHOR_HLC_FORMULA', value, precision='EXPORTED_DECIMAL_INPUT_OR_FRACTIONAL_PRECISION')
                r['dependencyCells'] = [c.pointer(d, field) for d in deps for field in ['INPUT_HIGH', 'INPUT_LOW', 'INPUT_CLOSE']]
        prior = c.by_index.get(i - 1)
        if p > 0 and prior is not None:
            for k in range(11):
                title = 'LEVEL_' + str(k)
                value = c.rows[prior][title]
                r = c.record(n, title, 'NONDEVELOPING_SAME_ANCHOR_INVARIANCE', F(value) if value else None, expected_blank=value == '')
                r['dependencyCells'] = [c.pointer(prior, title), c.pointer(prior, 'ANCHOR')]
    c.criterion('Dynamic pivot windows with preceding own confirmation context', bool(pivot_rows), 'UNDECIDED', None if pivot_rows else 'No complete own pivot window')
    c.criterion('Every scored completed-anchor interval exported', not missing_anchor_rows, 'UNDECIDED', None if not missing_anchor_rows else 'Only missing prior-anchor rows are excluded; later complete intervals remain eligible', {'missingPriorAnchorDataRowOrdinals': missing_anchor_rows})
    c.criterion('Three complete sixteen-row phase blocks plus pivot context', len(c.block) >= 48 and bool(pivot_rows), 'SUPPORTED', None if len(c.block) >= 48 and pivot_rows else 'Required naturally loaded phase/context block absent')
    c.criterion('At least three witnessed completed-anchor intervals', len(complete_anchors) >= 3, 'SUPPORTED', None if len(complete_anchors) >= 3 else 'Fewer than three fully exported prior-anchor intervals', {'completeAnchorStartDataRowOrdinals': complete_anchors})
    c.criterion('Native developing/nondeveloping value discriminator', bool(diverging_rows), 'SUPPORTED', None if diverging_rows else 'No distinct exported values in the bounded block', {'differentValueDataRowOrdinals': diverging_rows, 'scope': 'Original native numeric cells differ; no hidden precision or general pivot algorithm claim'})
