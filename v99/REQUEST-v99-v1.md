# Oracle round v99 — direct constant color comparisons and v6 cast identity v1

## Authorized method — verbatim from v98

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

**Commit locally on master only. DO NOT push: the owner publishes after crossed QA.** The historical HANDOFF quotation does not authorize an author push. No native capture starts from an unpublished local draft. This round runs after v98 finishes; v98 RESPONSE-v98-v6 at baseline **913792b5f5c06fcc313cb9f2e1baf6356dafdf34** ends all four finite slots. Do not interrupt another active round, reopen its slots or borrow its budget.

Create **one NEW v99 throwaway layout**, already signed-in account, BINANCE:BTCUSDT,2 minutes, ordinary Candles, Etc/UTC. Record independent native creation identity, not URL alone. Keep **P425PrivateV79v1** and `sours-lat/P425PrivateV79v1/1`: no action. Preserve every existing saved layout, script, open tab and settings, including v91–v98 contexts. Passive before/after observations never authorize old-layout edits, reload or repair. V98's reported old-page3 context-preservation hold remains an observed hold, with no inferred cause or restoration action.

Use only native UI editor Save/Add/export/remove and ordinary native UI screenshots for source/context/diagnostic ownership. **No publication/share/visibility change, alerts, existing-layout edit, library publication/import, sign-in/reconnect, account-global change, subscription/upgrade/entitlement action, Bar Replay, reload, forced recalculation, history expansion/calendar navigation, synthetic ticks/feed, injected code/browser evaluation, hidden-object inspection or direct compiler/provider/hidden API.** Executing ANY source with a library import is forbidden. V97's navigation exception is not inherited. If a prerequisite requires a forbidden action, STOP that facet as BLOCKED-NEEDS-OWNER-APPROVAL; independent listed slots may continue.

Each source receives a distinct NEW PRIVATE unpublished saved script with exact source bytes/title. For the reused source retain the original V98 indicator title and bytes; use a new private Save, never overwrite an existing script/version. Remove only studies added for v99; never delete/rename old scripts or layouts. Missing independent inventory or metadata stays UNOBSERVED.

## Frozen sources and attempt budget

**Maximum5 PRIVATE Save attempts,5 Adds,5 original CSV exports,5 calculation sessions, zero retries/input variants/history actions.** Run the five slots in inventory order, one study at a time. A slot permits one Save and, only on exact-source success, one Add and one export after ordinary settling. Failed/partial entry, refusal, Add failure or unavailable export consumes that slot. Preserve actual differing executed bytes but never Add mismatched source; record CRLF-only transport normalization separately. No repair, replacement, renamed variant, extra Save/Add/download, input/settings change, manual reload/recalculation or budget borrowing. Retain failures and continue only to the next independent unchanged slot.

| Slot | Source path from v99/ | Bytes | SHA256 | Plot calls/counts |
| ---: | --- | ---: | --- | ---: |
| 1 | `sources/v99-direct-colors-core-v5.pine` | 6228 | `e13c3fb04d2f185317a8b00f23b0221e1ca30bbc274d3751bf399fcc5690551d` | 63 |
| 2 | `sources/v99-direct-colors-edge-v5.pine` | 6469 | `c3abd93c9ec3c40284ffcff595a0337ab9cfc6f9575066a04b009bf47fd1dbd1` | 63 |
| 3 | `../v98/sources/v98-color-constructors-v6.pine` | 8998 | `fba851172d72dbe8d9bd74b08ea4bc7857f57633294493d81e9b2f8cb87aa245` | 63 |
| 4 | `sources/v99-color-na-identity-v6.pine` | 5673 | `0d971a924a1dd51a52c4c4a9c3f2a8684e3b2a75b3d9a20d7570391154a9367f` | 63 |
| 5 | `sources/v99-array-self-v6.pine` | 5663 | `725b73650e970f028841a63ea3e712a4f40452bf858f71c60f53d7d257700b45` | 64 |

From v99/ verify `sha256sum -c SHA256SUMS`. [Inventory](SOURCE-INVENTORY-v1.md) and [manifest](bundle-manifest-v1.json) freeze all bytes and all literal plot ordinals/source. The four new probes are import-free and MIT-noticed. Slot3 is an immutable reference, **no copied source**. Slots1–4 each have63 numeric plot calls/counts; slot5 has64; each source uses a constant default plot color, no colorer, inputs, imports, provider, alert, strategy, drawing or private-library dependency.

## Item1 — immediate constant RGB and NEW comparisons, v5

V98's switch-selected RGB sweep supports BYTE_ROUND while the separate immediate RGB12.5/DF flag remains0. Those contexts cannot be substituted. Two different uninstalled direct-comparison policies fit the old flag and RGB50/80=true: truncating transparency predicts E0 at12.5; percent-rounding predicts DE; both reject DF. V99 explicitly queries those missing literals in the same immediate context. No policy is assumed native.

In the core and edge sources **every comparison directly spells `color.rgb(33,66,99,<numeric literal>) == #214263XX` or `color.new(#214263FF,<numeric literal>) == #214263XX` inside its own plot/f_code call**. No constructor result, transparency, palette value or equality is selected through a switch, series alias, array or loop. The helper only encodes the already formed Boolean; it receives no color. Both constructors query E0,DE,DF at every requested transparency, plus the listed neighbor tokens. Core has direct R/G/B/T for each constructor/case and direct12.5 NA controls. Edge has direct T per case/constructor. Raw getter and predicate contexts remain distinct.

| t | Compared source literal tokens | TRUNC /ROUND /CEIL /BYTE_ROUND /BYTE_FLOOR nominal labels |
| ---: | --- | --- |
| 12.1 | #214263DE / #214263DF / #214263E0 / #214263E1 | 224 / 224 / 222 / 224 / 224 |
| 12.5 | #214263DE / #214263DF / #214263E0 / #214263E1 | 224 / 222 / 222 / 223 / 223 |
| 12.9 | #214263DE / #214263DF / #214263E0 / #214263E1 | 224 / 222 / 222 / 222 / 222 |
| 22.9 | #214263DE / #214263DF / #214263E0 / #214263C4 / #214263C5 / #214263C6 / #214263C7 | 199 / 196 / 196 / 197 / 196 |
| 0.5 | #214263DE / #214263DF / #214263E0 / #214263FC / #214263FD / #214263FE / #214263FF | 255 / 252 / 252 / 254 / 253 |
| 99.5 | #214263DE / #214263DF / #214263E0 / #21426300 / #21426301 / #21426302 / #21426303 | 3 / 0 / 0 / 1 / 1 |

Freeze five comparison-only candidate policies from exact rational decimal inputs: BYTE_ROUND=round-half-up((100−t)*255/100), BYTE_FLOOR=floor((100−t)*255/100), PERCENT_TRUNC=round-half-up((100−floor(t))*255/100) for these nonnegative t, PERCENT_ROUND=round-half-up((100−round-half-up(t))*255/100), PERCENT_CEIL=round-half-up((100−ceil(t))*255/100). Predictions nominate **source literal tokens**, not decoded native stored bytes. Complete nominal flags are in the manifest, separately applicable to RGB and NEW.

For each policy/case/constructor, the nominated token's code predicts1 and every other compared token predicts0. Under these frozen finite-query predictions,12.5 separates TRUNC/E0, percent-round/DE and raw-byte-round/DF;12.1 separates percent-ceil from percent-round;22.9 separates trunc199, raw-round197 and percent-round196;0.5 separates255/254/253/252. No getter T is predicted from the comparison's nominal alpha: v98 already warns that constant comparison versus getter/series evaluation can differ. Getter outputs remain independent native targets, never a way to infer hidden storage.

Core calibrates the complete same-source four-literal equality matrix (self and all unordered pairs). The separate ordinary-literal calibration hypothesis predicts self1 and distinct-pair0; contrary codes refute that hypothesis without filtering rows. Edge calibrates only its stated local adjacent pairs and C0 self; this is a **partial graph**, with nonadjacent/global calibration unobserved. Do not borrow calibration or stored identity from another source/session. Actual calibration contradictions are retained; they forbid a unique literal/storage interpretation. Even a supported finite query vector is bounded to those exact expressions, not a universal quantizer.

**Falsifiable criterion:** independently for RGB and NEW report every raw comparison/getter/control on all64 primary rows. Require exact predicted flags for a policy's complete six-case query vector; any contrary defined code or Boolean-NA code refutes that nominal finite-vector policy. Where source admission/coverage is incomplete, mark affected policy UNDECIDED instead of treating absent flags as0. Report SUPPORTED/REFUTED/UNDECIDED per policy, and ONLY_FROZEN_MODEL /MULTIPLE_FROZEN_MODELS /NEITHER_MODEL separately. All-zero comparisons are NEITHER_LITERAL, multiple true comparisons MULTIPLE_LITERAL_MATCHES, and−1 BOOLEAN_NA_EQUALITY; preserve every observation without filtering. Extra compared neighbor02 at99.5 and partial literal calibration never justify adding a fitted sixth policy.

**NOT OBSERVED / HELD:** refusal, source mismatch, absent/ambiguous columns or insufficient physical closed coverage holds the affected criterion. A recorded false/−1/blank or contradictory getter/calibration is OBSERVED, not an unavailable export. Unexported getter channels, cross-context equivalence, nonadjacent calibration, hidden payloads, other RGB/transparency ranges and universal storage remain held. Never add tolerance, alter literal palettes, fit a row count or retrofit a model after capture. V98's four NEW NEITHER rows/frozen model verdicts stay unchanged; these new immediate NEW queries do not decode their switch-selected storage.

## Item2 — unchanged v98 constructors-v6 source

Execute **`../v98/sources/v98-color-constructors-v6.pine`**, SHA256 **fba851172d72dbe8d9bd74b08ea4bc7857f57633294493d81e9b2f8cb87aa245**,8,998 bytes, exactly. Do not copy it into v99, change its version/title, strip text or repair it. This is one new owner-authorized v99 slot; the consumed v98 slot remains consumed and numerically UNOBSERVED.

Its source,63 columns,16-case palettes and four original comparison-policy predictions are the frozen v98 Item1 contract, carried verbatim by reference to [v98 request](../v98/REQUEST-v98-v1.md#item1--constructors-literal-versus-series-arguments) and [v98 manifest](../v98/bundle-manifest-v1.json). This source intentionally has switch-selected literal-argument versus series routes and its separate exact direct12.5/DF control. Do not report it as the v5 immediate sweep or add v99 TRUNC to its four frozen v98 models.

**Falsifiable criterion:** return all four R/G/B/T/NA/five-literal-equality route vectors, candidate T/calibration/cross-route fields and exact direct flag/code for every primary row; four visits to each16-case input. Recompute the four frozen v98 policies independently per route and preserve contrary channels, codes, neither/multiple matches and non-injective calibration. Prior v5 data and old v96 v6 controls cannot supply its output.

**NOT OBSERVED / UNDECIDED:** any native refusal, tool/entry failure, wrong bytes, absent export/binding or inadequate closed phase block consumes the slot and holds affected numeric facets. No retry within v99, no source variant, no inferred acceptance/value from local compilation or another version. Outcomes outside all four models remain NEITHER_MODEL with vectors observed and storage undecided.

## Item3 — v6 cast values, array elements and history equality

The baseline v98 v6 cast has NA1 together with finite0/0/0/100 getters; cast/var self equality1 coexists with ARRAY_EQ_CAST0. The engine's1,280 contrary cells are1,024 CAST/VAR/ARRAY/CAST_HISTORY getter cells,128 missing-branch HISTORY getter cells and128 cast/var equality cells over64 rows. Those are observed native divergences, not precision uncertainty. This source repeats those five complete RGBA/NA tuple roles, adds the full typed-NA getter/NA control, and retains the exact CAST_EQ_SELF/VAR_EQ_CAST operations, and adds separately exposed relationships. It does not prescribe a hidden representation.

`cast=color(na)`, separate `color typedNa=na` with its own full getter/predicate tuple, an immutable `var retained=color(na)`, original one-slot `array.from(cast)`/`array.get`, two-slot twins from the same current cast, alternating current color, constant and selected history[1], scalar array-element history, retained history and guarded previous **array object's element** are separately named. Arrays are per-bar, sizes1/2, never mutated; the previous array access is guarded at actual own index0. Report direct `color(na)==color(na)`, alias self, retained/cast equality, one-slot/twin/cast equalities, inline repeated get, the plotted history self/cross comparisons and separate NA predicates, typed NA, transparent-black and present-literal controls. A source equality plot is its own observation, not evidence of cross-recalculation object identity.

**Falsifiable facets, frozen before capture:**

- NA_IMPLIES_BLANK_GETTERS predicts blank R/G/B/T when the same role's NA flag is1. Any finite getter refutes this conditional model; preserve the actual complete tuple.
- NA_IMPLIES_FALSE_EQUALITY predicts0 when an observed operand NA flag is1, including self. Apply this conditional model only where that exact operand binding has an exported NA predicate; inline direct-cast and repeated-get expressions lack their own NA predicates and retain their raw Boolean target without alias-based inference. SELF_EQUALITY_ALWAYS_TRUE instead predicts1 for each exposed self expression. Report both against each owned expression independently; a mixture refutes a uniform rule and does not license fitting per-name sentinels.
- EQUAL_COMPLETE_TUPLES_IMPLY_EQUALITY predicts ARRAY_EQ_CAST=1 if the actual same-row CAST/ARRAY R/G/B/T/NA tuples all agree. Refute on an observed0. Compare the Boolean itself separately; missing getters or equal tuples never manufacture a color identity.
- CAST_HISTORY_RAW_TRANSFER predicts the full CAST_HISTORY tuple equals the actual prior original CAST tuple. HISTORY_NA_TRANSFER predicts HISTORY_NA equals the actual prior CURRENT_NA. ARRAY_HISTORY_NA_TRANSFER and VAR_HISTORY_NA_TRANSFER use previous ARRAY_NA/VAR_NA. OBJECT_HISTORY_NA_TRANSFER uses the actual previous one-slot ARRAY_NA. TWIN_NA_TRANSFER compares each actual twin predicate with same-row CAST_NA. Contrary results refute their own relationships; they never become row exclusions.

Every equality, including HISTORY_EQ_EXPECTED and OBJECT_HISTORY_EQ_CAST_HISTORY, remains an independent target with its actual code. For a prior DF branch, previous CASE_ID/CURRENT_NA witness the selected expression, but no absent prior DF channel tuple is invented. Twin/array-history channels not plotted stay unobserved. If neither uniform equality rule or tuple implication works, retain the complete relation table and an UNDECIDED hidden model. Do not fit payload bits, reinterpret getter0 as NA0, or replace array equality with tuple equality.

**NOT OBSERVED / HELD:** refusal, missing ownership/columns, unavailable actual closed predecessor or inadequate phase coverage holds only the affected tuple/history/equality facet. Preserve original blanks and all finite getters even with NA1; no coalescing to generic missing or importing v5 behavior. An immutable var's suffix does not prove unexported own-index-zero initialization. No PRNG, realtime, cross-recalc, generic array equality or all-color identity contract is claimed.

### Item3 slot5 — exact batch77 minimal discriminator

Execute `sources/v99-array-self-v6.pine`, SHA256 **725b73650e970f028841a63ea3e712a4f40452bf858f71c60f53d7d257700b45**, as its own fifth slot. These are byte-for-byte the owner-selected batch77 proposal: the complete unchanged v98 v6 cast source, its63 original plots in the same order, followed by the proposal comment and exactly one added64th plot `f_code(fromArray == fromArray)` titled **ARRAY_EQ_SELF**. The frozen V98 title and proposal comment are intentional. Use a distinct new PRIVATE Save identity; no overwrite or source repair. The broader slot4 never substitutes for this minimal program.

**Falsifiable criterion:** the stable-initializer-folding/runtime-missing witness predicts ARRAY_EQ_SELF=0; the copied missing-cast-token witness predicts1. These incompatible continuations both reproduce the old v98 record; neither is a native fact or installed model. Retain the new source's original63 controls, complete CAST/ARRAY getter+NA tuples and actual own predecessor, and compare the semantic controls against v98 by corresponding CASE_ID and predecessor branch, keeping each source/session separate. INPUT_INDEX, INPUT_TIME and frontier metadata are context, not values expected to equal the older session. If unchanged controls recur with a physically closed ARRAY_EQ_SELF0, refute the copied-token witness for this source; with1, refute the runtime-missing witness. Report every raw cell and all primary-row consistency. One owned closed row can discriminate the two witnesses; the64-row block remains the full control/phase certificate. A changed original control is an observed context difference that holds extrapolation from the old program, never a reason to drop the row or fit the model. A selected finite vector does not establish universal storage, optimization or identity semantics.

**NOT OBSERVED / HELD:** failed admission, mismatched bytes, absent/ambiguous ownership, missing closure or no ARRAY_EQ_SELF column holds the discriminator; missing64-row coverage/predecessor separately holds that certificate/history facet while retaining actual partial observations. Any unexpected value or mixed closed results is observed, with the two-witness conclusion UNDECIDED. No baseline values are borrowed from slot4, v98 or the engine; each native control is scored from its own new CSV. No cross-source/session continuity or sample-completeness claim.

## Original exports, closure and primary selection

Export the naturally available complete native CSV once/successful source. Retain every original chart/builtin/source column, raw bytes/length/SHA256, decimal strings/signed zero/blanks, duplicate headers by ordinal and all rows through its frontier. Bind every literal plot ordinal (63 each for slots1–4;64 for slot5) to actual native CSV columns using exact executed SHA, new private source/version and genuinely exposed Save/Add metadata; titles alone do not establish ownership. A defined colorer or plot never creates an absent exported value. Separate complete exposed Save/Add compiler bodies, warnings/markers and immediate/settled UI. Admission success alone does not certify a running source; blank cells under runtime failure are not NA witnesses.

Independently classify physical2m closure from actual CSV units, export/observation UTC and CHART_CONFIRMED, also requiring INPUT_TIME milliseconds to match chart time. Return original-SHA/row/column/time closure masks. For the two constant v5 sources choose the first64 consecutive independently closed source-owned rows with increasing timestamps and consecutive INPUT_INDEX. For the reused v6 constructors and both v6 cast sources choose the earliest such64-row block starting CASE_ID0. Constructor has four visits/case; both cast sources have16 visits/phase. Each cast source independently requires the immediately preceding original row closed/owned with INPUT_INDEX−1; retain its actual full context and every subsequent original predecessor pointer without scoring it as an extra primary row. Allow actual market-time gaps; never synthesize bars or force120-second increments.

Selection uses only ownership/input context/physical closure, never getters, NA, equality, calibration or agreement with a model. If the one export lacks the required block/predecessor, record the specific facet NOT OBSERVED and retain partial values. Do not wait for preferred results, navigate history, re-export or stitch sessions. All outside/developing/present cells stay OBSERVED / EXCLUDED with exact causes, zero primary credit; no sampling-completeness or original-frontier reconstruction claim. Maximum planned primary plot cells:20,224, not a count of independent model tests.

## Return and preservation evidence

Return `v99/captures/v99/RESPONSE-v99-v1.md`, finite attempt inventory, per-source raw targets/numeric controls, model/property verdicts and facet capabilities, passive saved-layout/script/open-tab before/after comparison, `artifact-integrity-v1.json` (all dependency/return path/bytes/SHA256, self-excluded), read-only validator and `validation-result-v1.json`. Increment progress versions; never overwrite prior evidence. Distinguish unique plot cells, repeated hypothesis/pointer records, actual closed rows and exclusions.

Retain exact requested/executed bytes, separate original source references for the unchanged v98 source, new private source/version/plot identity as exposed, Save-form transport, complete separate Save/Add bodies/diagnostics, immediate/settled UI, context/settings, actual export/observation UTC, original CSV/bindings/closure/dependency receipts, failures and cleanup. Unexposed native feed/execution IDs, independent editor arrays and complete private inventory stay UNOBSERVED. Never infer them from local compiler output or inspect hidden state. Native tooling contributions require their own explicit license; no corpus-wide license change.

Each hypothesis record includes actual original CSV-SHA/row/column/header/raw-string input, target, calibration and dependency pointers, frozen prediction, SUPPORTED/REFUTED/UNDECIDED and exact exclusion/precision cause. Missing mathematical precision can hold a rational model, but a concrete engine binary64/string versus a concrete native raw cell remains exactly decidable during later consumption. Unexpected present values are OBSERVED, not unavailable because a candidate fails.

Preserve P425PrivateV79v1 and every existing layout/script/tab; record any actual before/after difference and unknown cause as a preservation hold, never repair an old layout. No engine change, fixture promotion, universal storage/identity, pixel/CSS/DPI claim or historical hold1/2/7/8/13/14/21 closure. Earlier evidence/budgets remain unchanged. **Local commit only; DO NOT push.**
