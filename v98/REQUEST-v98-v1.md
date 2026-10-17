# Oracle round v98 — v5 color storage and NA-cast discriminators v1

## Authorized method — verbatim from v97

Save as PRIVATE unpublished script, Add to chart, remove studies after; MAY create a new throwaway layout and change symbol/interval/settings on it only; STILL FORBIDDEN: publish, share, any visibility change, any change to EXISTING saved layouts, alerts, library publication/import; anything beyond: STOP as BLOCKED-NEEDS-OWNER-APPROVAL.

## HANDOFF §4 — verbatim rules

- Repo `Tealstreet/tealscript-oracle`, local `~/cs/tealscript-oracle`. Publish capture requests
  straight to its `master`; a capture agent polls and answers (`RESPONSE-vNN-*.md` + captures).
  Head check: `git ls-remote https://github.com/Tealstreet/tealscript-oracle refs/heads/master`.
- Tests consume a SHA-pinned sparse checkout via `packages/tealscript/oracle-fixtures.json`
  (`node scripts/oracle-fixtures.mjs fetch`). Never commit raw captures into tealchart or
  tealstreet-next.
- **Request rules:** never ask for publication, sharing, visibility changes, alerts, edits to
  existing layouts, or library publication/import. A new throwaway layout is allowed; keep layout
  `P425PrivateV79v1` if possible. Reuse the v90 authorized-method text verbatim.

## Local authoring, schedule and layout boundary

**This bundle is committed locally on master only. DO NOT push: the owner will push after crossed QA.** The historical HANDOFF quotation above does not authorize the author to push. Do not start native capture from an unpushed local draft. After owner publication, run after v97 has finished its finite round or explicitly completed with capability holds. V97 response v14 is already complete at this authoring baseline; do not interrupt another active request or extend any earlier round's budget.

Baseline: oracle **962bbf90b269e98f26af84d86f7cb83972c11f44**. V96's two v5 control flags are actual exported 0: `color.rgb(33,66,99,12.5) == #214263DF ? 1 : 0` and `na(color(na)) ? 1 : 0`; v6 exports 1. Constructor T is 13 in both. They remain separately observed contradictions, without a selected v5 representation. This request asks for discriminating native evidence, not a chosen implementation or permission to fit one. In v5 a zero from `condition ? 1 : 0` need not distinguish false from Boolean NA, so the new equality codes preserve that distinction.

Create **one NEW v98 throwaway layout** in the already signed-in account, BINANCE:BTCUSDT, 2 minutes, ordinary Candles, Etc/UTC. Record independent native creation identity; a URL alone is insufficient. Preserve every pre-existing saved layout/script/open tab and their settings, including all v91–v97 contexts and **P425PrivateV79v1**, plus `sours-lat/P425PrivateV79v1/1`: no action. Passive before/after observations must not edit those layouts. Each source receives a distinct NEW PRIVATE unpublished saved script, retaining its exact indicator title and bytes. Remove only studies added for this request; never delete scripts or layouts or overwrite/rename an old study.

Use only native UI editor Save/Add/export/remove and ordinary native UI screenshots for source/context/diagnostic ownership. **No publication/share/visibility change, alerts, existing-layout edit, library publication/import, sign-in/reconnect, account-global change, subscription/upgrade/entitlement action, Bar Replay, reload, forced recalculation, history expansion/calendar navigation, synthetic ticks/feed, injected code/browser evaluation, hidden-object inspection or direct compiler/provider/hidden API.** Executing ANY source containing a library import is the forbidden import action. V97's navigation exception is not inherited. If a prerequisite requires a forbidden action, STOP that facet as BLOCKED-NEEDS-OWNER-APPROVAL; independent listed slots may continue.

## Frozen sources and finite attempt budget

Four new import-free indicator sources, in order: constructors v5, constructors v6, NA-cast v5, NA-cast v6. **Maximum 4 PRIVATE Save attempts, 4 Adds, 4 original CSV exports, 4 calculation sessions, zero retries, zero input variants and zero history/navigation actions.** One study at a time. A slot permits one Save and, only after exact-source success, one Add and one export after ordinary settling. Partial/failed entry, refusal, Add failure or unavailable export consumes the slot. Preserve the actual differing executed bytes but never Add mismatched source. Record CRLF-only Save transport normalization separately. No source repair/replacement, renamed variant, extra Save/Add/download, setting/input change, manual reload/recalculation or budget borrowing. Ordinary observation/screenshots do not authorize extra calculations. Retain refusals and proceed only to the next independent unchanged listed slot.

From v98/ run `sha256sum -c SHA256SUMS`. [Source inventory](SOURCE-INVENTORY-v1.md) and [manifest](bundle-manifest-v1.json) freeze exact bytes, all literal plot ordinals, candidate literals and selection/budget. Each source has **63 numeric plot calls / 63 plot counts**, default constant plot color, no colorer, inputs, imports, requests, alerts, strategies, drawings or private-library dependency. Candidate colors are literal Pine tokens; the integer alpha labels identify source tokens only, not decoded native storage. All new Pine sources carry their own MIT SPDX notice; no corpus-wide license is changed.

| Source | Bytes | SHA256 | Plot calls |
| --- | ---: | --- | ---: |
| `v98/sources/v98-color-constructors-v5.pine` | 9015 | `718cee58cafa93bcf402485fc0bbf8213f8a0c31e1e496019041b63ce8b7d42c` | 63 |
| `v98/sources/v98-color-constructors-v6.pine` | 8998 | `fba851172d72dbe8d9bd74b08ea4bc7857f57633294493d81e9b2f8cb87aa245` | 63 |
| `v98/sources/v98-color-na-cast-v5.pine` | 5506 | `5a0b9dae7bbfe1692be0df2ba1738d5d6d1831d8e00b2c9c70616ffa554d4663` | 63 |
| `v98/sources/v98-color-na-cast-v6.pine` | 5489 | `c1b586591b542c8e4efaa35c38d5246ea0ad7acc28ba6ccd5f068dd02331574a` | 63 |

## Item1 — constructors, literal versus series arguments

Both versions sweep 16 cases using `CASE_ID = bar_index % 16`. `TRANSP_INPUT` is selected from the frozen numeric literal list. `LITERAL_RGB` and `LITERAL_NEW` select calls whose constructor arguments are literal, respectively `color.rgb(33,66,99,t_literal)` and `color.new(#214263FF,t_literal)`. `SERIES_RGB` and `SERIES_NEW` pass the phase-selected series transparency to those same constructors. A literal-argument call is not an assertion that its switch-selected result has const qualifier. All four results export **R/G/B/T/NA plus five independent ordinary literal-equality codes**. Never borrow a constructor or qualifier's output for another.

Five neighboring, distinct *source literal tokens* C0..C4 are frozen per case, including all four byte-policy predictions below. Export `C0_ALPHA_LABEL`, every Cj's actual T getter, adjacent literal-equality codes `EQ_C0_C1`..`EQ_C3_C4`, and the same-row fixed DF-self/DF-versus-E0 calibration. Do not assume distinct hex spellings have distinct native stored values. Cross-comparisons RGB_EQ_LITERAL_SERIES, NEW_EQ_LITERAL_SERIES, LITERAL_EQ_RGB_NEW and SERIES_EQ_RGB_NEW directly expose equality across those routes without inferring it from equal getters.

The exact original v96 constructor ternary is separately retained as `EXACT_RGB12_5_EQ_DF`, alongside `EXACT_RGB12_5_EQ_DF_CODE` for the identical direct comparison. All other equality and NA-predicate plots use **v5: −1=Boolean NA,0=false,1=true; v6:0=false,1=true**, with no illegal v6 na(bool) call. Retain unexpected codes/blanks as actual observations. Equality to `na` is otherwise tested via a typed `color typedNa = na` variable, avoiding a literal-na comparison admission experiment that could consume the complete cast source.

Frozen competing policies, for t in 0..100: BYTE_ROUND=round-half-up((100−t)*255/100); BYTE_FLOOR=floor((100−t)*255/100); PERCENT_ROUND=round-half-up((100−round-half-up(t))*255/100); PERCENT_CEIL=round-half-up((100−ceil(t))*255/100). These are **hypotheses, not native values**. The accompanying candidate nearest-percent getter model is round-half-up(100−alpha*100/255), tested separately from literal equality. Full predicted literal tokens and exact rational nominal alphas are in the manifest; the four labels in the last column below have order BYTE_ROUND /BYTE_FLOOR /PERCENT_ROUND /PERCENT_CEIL.

| CASE_ID | t | C0 /C1 /C2 /C3 /C4 literal tokens | Four predicted alpha labels |
| ---: | ---: | --- | --- |
| 0 | 12.1 | #214263DE / #214263DF / #214263E0 / #214263E1 / #214263E2 | 224 / 224 / 224 / 222 |
| 1 | 12.5 | #214263DD / #214263DE / #214263DF / #214263E0 / #214263E1 | 223 / 223 / 222 / 222 |
| 2 | 12.9 | #214263DC / #214263DD / #214263DE / #214263DF / #214263E0 | 222 / 222 / 222 / 222 |
| 3 | 0.4 | #214263FB / #214263FC / #214263FD / #214263FE / #214263FF | 254 / 253 / 255 / 252 |
| 4 | 0.5 | #214263FB / #214263FC / #214263FD / #214263FE / #214263FF | 254 / 253 / 252 / 252 |
| 5 | 99.5 | #21426300 / #21426301 / #21426302 / #21426303 / #21426304 | 1 / 1 / 0 / 0 |
| 6 | 0.0 | #214263FB / #214263FC / #214263FD / #214263FE / #214263FF | 255 / 255 / 255 / 255 |
| 7 | 10.0 | #214263E3 / #214263E4 / #214263E5 / #214263E6 / #214263E7 | 230 / 229 / 230 / 230 |
| 8 | 15.0 | #214263D6 / #214263D7 / #214263D8 / #214263D9 / #214263DA | 217 / 216 / 217 / 217 |
| 9 | 50.0 | #2142637D / #2142637E / #2142637F / #21426380 / #21426381 | 128 / 127 / 128 / 128 |
| 10 | 100.0 | #21426300 / #21426301 / #21426302 / #21426303 / #21426304 | 0 / 0 / 0 / 0 |
| 11 | 22.1 | #214263C4 / #214263C5 / #214263C6 / #214263C7 / #214263C8 | 199 / 198 / 199 / 196 |
| 12 | 22.5 | #214263C3 / #214263C4 / #214263C5 / #214263C6 / #214263C7 | 198 / 197 / 196 / 196 |
| 13 | 22.9 | #214263C2 / #214263C3 / #214263C4 / #214263C5 / #214263C6 | 197 / 196 / 196 / 196 |
| 14 | 32.1 | #214263AB / #214263AC / #214263AD / #214263AE / #214263AF | 173 / 173 / 173 / 171 |
| 15 | 32.5 | #214263AA / #214263AB / #214263AC / #214263AD / #214263AE | 172 / 172 / 171 / 171 |

**Falsifiable criterion:** for each version/constructor/argument route independently, report all 64 selected R/G/B/T/NA/equality vectors, four visits to each case. Under a byte-policy hypothesis, RGB=33/66/99 and NA=0, the nominated literal's equality=1, other distinct stored candidates' equality=0 and the candidate T output must match the actual tuple; Boolean-NA codes, contrary channels or equality/calibration contradictions are explicit refutations of that fully specified hypothesis, never row exclusions. Record original codes and the partial literal calibration graph. Report identical/different route equality directly. Non-half cases such as 12.1 distinguish percent-round(alpha 224) from percent-ceil(alpha 222), while 12.5's neighboring literals adjudicate the old constructor root without assuming a byte from T=13. The control t=50 repeats the known constructor/half-opacity setting.

**NOT OBSERVED / UNDECIDED:** refusal, mismatched source, absent/ambiguous columns, insufficient closed phase coverage or missing inputs holds only the affected criterion. NEITHER_LITERAL (all defined equality codes 0), BOOLEAN_NA_EQUALITY (codes −1), MULTIPLE_LITERAL_MATCHES and calibration contradictions remain distinct observed outcomes; preserve all their raw getters/NA/codes. Multiple equalities or non-injective literal calibration do not establish a unique stored byte. If no frozen hypothesis matches, return NEITHER_MODEL; retain native vectors and leave storage UNDECIDED. Never select another quantizer after seeing the data, add epsilon/tolerance, alter the palette, fit a row count or equate getter percent with hidden color storage.

## Item2 — color(na) across storage, history and consumers

Each version exports R/G/B/T/NA for nine independently named values:

| Prefix | Exact source operation |
| --- | --- |
| CAST | `cast = color(na)` |
| VAR | `var color retained = color(na)`; never reassigned |
| ARRAY | a new per-bar `array.from(cast)` then `array.get(slot,0)` |
| HISTORY | `alternating[1]`, where current alternating uses cast at even CASE_ID and #214263DF at odd CASE_ID |
| CAST_HISTORY | `cast[1]` |
| NZ_DEFAULT | `nz(cast)` |
| NZ_REPLACEMENT | `nz(cast,#214263DF)` |
| GRAD_CAST | `color.from_gradient(5,0,10,cast,#FF0000)` |
| GRAD_NA | the independent positional bare-na lower endpoint control `color.from_gradient(5,0,10,na,#FF0000)` |

Also export the exact old `na(color(na)) ? 1 : 0` and its direct Boolean-NA-preserving `EXACT_NA_CAST_CODE`, typed-na NA code, same-row present self/distinct equality calibration, cast equality to itself/typed-na/opaque black/transparent black/DF, VAR_EQ_CAST, ARRAY_EQ_CAST and HISTORY_EQ_EXPECTED. Every equality and NA predicate other than the two explicitly preserved old ternaries uses the version-specific Boolean-NA-preserving encoding. HISTORY_EQ_EXPECTED compares with the phase-derived previous expression, using typedNa only at actual own index0; it supplies no engine/native seed. CASE_ID, CURRENT_NA and INPUT_INDEX identify the alternating input; derive its dependency index as INPUT_INDEX−1 and join the actual preceding original row. Keep the cast-prefix and selected-branch-history facets separate; no drawing/colorer value is invented.

**Falsifiable criterion:** record the complete native tuple/code per value on every primary row and original same-source previous row. Compare VAR/ARRAY transfer and both history tuples/NA masks to their witnessed source expressions and preceding exported cells; compare the equality codes independently of getters. No hidden object identity or cross-recalculation sameness follows. An immutable var's captured values are observations of that execution, not proof of its unexported index0 initialization. For HISTORY, independently verify source index predecessor by 1 and actual prior CASE_ID/current tuple context; missing first-row dependencies never become a default color.

Frozen alternatives are deliberately separable: (A) ordinary missing propagation predicts CAST_NA=1 with blank channel getters, missing VAR/ARRAY/history when their predecessor is the cast, default-nz transparent-black getters and replacement-nz DF getters; (B) transparent-black present cast predicts CAST_NA=0, getters 0/0/0/100, defined CAST_EQ_BLACK100=1; (C) opaque-black present cast predicts CAST_NA=0, getters 0/0/0/0, defined CAST_EQ_BLACK0=1; (D) a non-NA predicate with blank channel getters refutes both ordinary-missing and finite-black tuples without inventing a replacement color. Each is a bounded tuple/predicate candidate, not a complete native storage implementation. For nz, test the separately stated missing/fallback identity relationship against both actual output tuples; do not assume na() and nz() recognize exactly the same sentinel. Literal-DF/T and equality calibration remain owned controls, not inferred colors.

GRAD_CAST versus GRAD_NA equality of complete exported tuples is a separate frozen equivalence hypothesis: match requires exact raw present values and identical observed blanks/NA; any contrary tuple refutes equivalence for that version, without overriding either cast's NA predicate. This midpoint does not certify all gradient ratios or a storage algorithm. Every observed tuple, including ones outside all four alternatives, remains a native target vector; acceptance is not conditioned on a preferred outcome.

**NOT OBSERVED / UNDECIDED:** missing getter/NA/equality/nz/gradient binding, unavailable previous exported input, refusal, insufficient closed rows or inadequate raw precision holds only that operation/row facet. Non-finite/missing getter cells with an explicit native NA/presence witness are observed results, not absent exports. `−1`,0,false-like flags and blanks are not coerced to one another. Unseen present colors, identity, hidden payloads and general propagation remain held; never fill them from v6, another qualifier, an array control or the bare-na gradient.

## Original CSV, closure and deterministic primary selection

Export the naturally available complete native CSV **once per successful source**, retaining every chart/builtin/source column, original bytes/SHA256/length, raw numeric strings/signed zero/blanks/NA, duplicate headers by ordinal and every original row through the frontier. Bind all 63 literal source plot ordinals to actual CSV columns using exact executed SHA, distinct private source/version and genuinely exposed Save/Add plot metadata. Titles alone do not establish ownership. Missing native fields stay UNOBSERVED; a plot/colorer definition never creates an absent CSV value or authorizes hidden decoding. No full own-index-zero prefix, history navigation or selected source-index value is required for these finite facets.

Independently classify each physical row using observed CSV time units, physical 2m close, actual export/observation UTC and CHART_CONFIRMED together; source INPUT_TIME milliseconds must agree with native chart time. Return raw-SHA/ordinal/time closure masks. The **primary block is the earliest 64 consecutive independently closed rows starting at CASE_ID=0 with strictly increasing timestamps and consecutive source INPUT_INDEX**, selected only by source ownership/input indices and physical closure. For each NA-cast source additionally require that the original immediately preceding row is closed, owned and index−1; retain it as the history dependency, without adding it to the 64-row score. Verify subsequent history dependencies against original row ordinals, including real market-time gaps; never synthesize bars or force timestamps to 120-second increments.

Constructor primary blocks have four visits/case; cast primary blocks 16 visits/phase. NA/getter/equality values are **never selection or eligibility filters**. If 64 such rows or the predecessor are not available in the single export, record the specific block/history criterion NOT OBSERVED and preserve all partial cells. Do not wait for preferred values, navigate, re-export, repeat entry or splice sessions. All other historical rows and developing/present cells remain OBSERVED / EXCLUDED with exact causes and zero primary credit. No sampling-completeness or live/update/cross-recalculation claim.

## Return and preservation evidence

Return `v98/captures/v98/RESPONSE-v98-v1.md`, finite attempt inventory, per-source numeric targets/controls and model/property verdicts, facet capabilities, passive account/layout/script/tab preservation comparison, `artifact-integrity-v1.json` (path/bytes/SHA256 of all dependencies/returns, self-excluded), a read-only validator and `validation-result-v1.json`. Progress responses/artifacts increment names; never overwrite earlier evidence. Treat source admission, closure/coverage, vector observations, equality calibration and each model verdict as separate statuses. Counts distinguish unique plot cells from repeated model/pointer records.

For each attempt retain exact requested/executed bytes/hash, private source/version/plot identity as exposed, Save form/source transport, separate complete exposed Save/Add compiler bodies, warnings/markers and immediate/settled UI separately, context/settings/feed state, export/observation UTC and original CSV/bindings/closure/dependency receipts. A refusal is observed admission, not a value match or permission to repair. Runtime failure must retain the exact exposed error and executing-source ownership; Save/Add success alone is not a running-vector certificate, and blank private columns under failure are not numeric/NA witnesses. Missing independent editor arrays, native feed/execution IDs and unexposed metadata remain UNOBSERVED. Record cleanup and the untouched existing-layout/private-library proof without unauthorized inspection. New contributed capture tooling must state its own explicit license separately; no corpus-wide rights are implied.

Every hypothesis record needs actual raw target/input/calibration/dependency pointers (CSV SHA, original row/column ordinals, header and raw string), prediction, SUPPORTED/REFUTED/UNDECIDED status and any precision/exclusion cause. Exact integer flags distinguish hypotheses; fractional getter discrepancy with unresolved export precision remains OBSERVED/UNDECIDED, without rounding/fitting. This does not waive exact comparison of a concrete engine float/string with a concrete native export during later consumption. Unexpected present values remain OBSERVED, never UNOBSERVED because they contradict a candidate.

No engine fix/fixture promotion, universal color model, rendered pixel/CSS/DPI contract, original-frontier reconstruction or closure of historical holds 1/2/7/8/13/14/21 is requested. All older evidence, budgets and holds remain unchanged. **Local commit only; owner push after crossed QA.** Native publication/share/visibility/import/reconnect/account-global/existing-layout actions remain forbidden.
