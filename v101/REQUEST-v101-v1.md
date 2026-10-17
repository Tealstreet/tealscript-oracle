# Oracle round v101 — constant RGB opacity operation order v1

## Authorized method — verbatim from v100/v99/v98

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

**Commit locally on master only. DO NOT push: the owner publishes after crossed QA.** The historical HANDOFF quotation does not authorize an author push. No native capture starts from this unpublished draft. Baseline oracle is **b23c3d71f00e83cb40c4ab3d65be269788605f89**, after completed v100. Run after v100 and without interrupting another active round, reopening consumed slots or borrowing budgets. New evidence never supplies retroactive credit to older captures.

Create **one NEW v101 throwaway layout**, already signed-in account, BINANCE:BTCUSDT,2 minutes, ordinary Candles, Etc/UTC. Record independently exposed native creation identity, not URL alone. Keep **P425PrivateV79v1** and `sours-lat/P425PrivateV79v1/1`: no action. Preserve every existing saved layout, script, open tab, private library and settings, including v91–v100 contexts. Passive before/after observations never authorize edits, reload or repair. Older preservation holds remain held; retain differences and unknown causes without restoration.

Only native editor Save/Add/export/remove and ordinary native UI screenshots for source/context/diagnostic ownership are allowed. **No publication/share/visibility change, alerts, existing-layout edit, library publication/import, sign-in/reconnect, account-global/account/entitlement/subscription/upgrade changes, Bar Replay, reload, forced recalculation, history expansion/calendar navigation, synthetic ticks/feed, injected code/browser evaluation, hidden-object inspection or direct compiler/provider/hidden API.** Executing ANY source with a library import is forbidden. V97 navigation permission is not inherited. If a prerequisite needs a forbidden action, STOP that facet as BLOCKED-NEEDS-OWNER-APPROVAL.

Use a distinct NEW PRIVATE unpublished saved script, exact source bytes/title; never overwrite an existing script/version. The frozen indicator title intentionally still says **V100 immediate color discriminator v5**: source identity is SHA/private Save/version/session, never title alone. Save under a distinct new private saved-script identity without repairing or changing source bytes/title. If native UI cannot distinguish that new script without editing the source, record the slot held rather than overwrite an old script. Remove only the study added for v101. Never delete/rename old scripts or layouts, repair sources, or change inputs/settings between observations. Unexposed identities or independent inventory stay UNOBSERVED.

## Frozen source and finite attempt budget

**One slot only: maximum1 PRIVATE Save attempt,1 Add,1 original CSV export,1 calculation session, zero retries/input variants/history actions.** This inherits v99/v100's zero-retry ceiling. One Save, then only on exact-source success one Add and one naturally available export after ordinary settling. Any failed/partial entry, refusal, Add failure or missing export consumes the slot. Preserve executed differing bytes but never Add a mismatched source; record CRLF-only transport normalization separately. No repair, replacement, renamed source variant, extra Save/Add/download, manual reload/recalculation or budget borrowing.

| Slot | Frozen source path from v101/ | Bytes | SHA256 | Plots | Primary closed rows |
| ---: | --- | ---: | --- | ---: | ---: |
| 1 | `sources/proposed-v101-rgb90-v5-v1.pine` | 4895 | `542bdcaf0a1823869f097e65207caed2a2ea7b403b7dd993a11224018a7538f2` | 40 | 64 |

From v101/ run `sha256sum -c SHA256SUMS`. [Inventory](SOURCE-INVENTORY-v1.md) and [manifest](bundle-manifest-v1.json) bind exact bytes and all40 plot ordinals. This is byte-identical to the accepted batch78 v100-consumption-v1 proposal, including the original V100 title, helper, comments and all39 unchanged previous columns. Its first4,768 bytes are the exact v100 immediate source, SHA256 `43e6eb7eed958867961de5630dce3b36e630d0af20d8e268851ba6740d31db79`; the only appended source line exports **DIRECT_RGB_NEW_90_EQ**. No source substitution or added code. The source is import-free, MIT-noticed, with40 distinct numeric plots and constant default plot colors: no inputs, colorers, library, provider, alert, strategy, drawing, var/history or realtime observer.

## Pre-registered witnesses and exact predictions

The normative [prediction map](predictions/prediction-map-v1.json) binds all40 columns: three context contracts,36 repeated constant-color control codes, and one new discriminator. The complete [witness recipes](predictions/countermodels-v1.json) are copied byte-for-byte from the accepted proposal; their older explanatory status is historical metadata, not a native model claim or restriction on the separately authorized engine implementation. [Pre-registered tables](PRE-REGISTERED-PREDICTIONS-v1.md) list every per-model numeric code. All are frozen author-input hypotheses, never capture results or engine-derived native targets. Two witnesses independently reproduce all23,448 previously observed constant-color cells across v96/v98/v99/v100; this fits the observed surface but does not identify hidden native storage or every unobserved input.

Both witnesses use ordinary IEEE binary64 operations in the listed order, float32 only at explicit Math.fround steps, and shared NEW byte `Math.round(255*(1-Math.trunc(t)/100))`. CM-A RGB byte is `Math.round(((100-t)*255)/100)`; CM-B RGB byte is `Math.round(255*(1-t/100))`. Their constructor scalar is `Math.fround(2.55)*(100-(100*(1-Math.fround(a/255))))`; literal scalar is `2.55*(100-(100*Math.fround(1-a/255)))`. Pack in g,b,a,r low-to-high order by `g+b*256+a*65536+r*16777216`; RGB applies signed `|0`, NEW applies `Math.trunc`, literal leaves the sum unchanged. Equality compares the resulting `.toFixed(1)` strings exactly. No tolerant comparison to native outputs is permitted: this string conversion is part of the falsifiable witness recipe.

| New source-owned numeric column | CM-A | CM-B |
| --- | ---: | ---: |
| `DIRECT_RGB_NEW_90_EQ` | 0 (RGB26 vs NEW25) | 1 (RGB25 vs NEW25) |

At t90 the two binary64 operation orders place the RGB intermediate on opposite sides of a half tie. One properly owned physically closed exported0 refutes CM-B's new-column prediction; exported1 refutes CM-A's. Mixed0/1 rows refute both constant complete vectors. Any blank/unexpected value stays OBSERVED and contrary to these numeric predictions, with execution/ownership cause investigated only through allowed exposed evidence. No third model, quantizer, source repair or post-capture fit.

**Falsifiable full-vector property:** independently score CM-A and CM-B against every37 color-code column on all64 primary closed rows. SUPPORTED means the entire frozen vector repeats exactly in every owned primary row; any contrary owned closed cell REFUTES that finite vector, even if full coverage is missing. Partial matching coverage is UNDECIDED. Report ONLY_CM_A / ONLY_CM_B / MULTIPLE / NEITHER for this finite source-vector scope. Preserve the complete old39-column control execution independently. A changed original control is observed: it refutes any witness predicting otherwise and holds extrapolation from the older execution rather than being filtered out. A new-code-only result can distinguish the new query with partial coverage while full-vector support remains held.

**Encoding limit:** the unchanged v5 helper is `value ? 1 : 0`; false and Boolean NA can both become0. Code0 is the actual numeric output, not proof of defined false/non-missing color. Neither code, equal getter, fitted vector nor surviving witness proves hidden byte identity, universal storage, Boolean-NA distinction, generic equality, missing-color casts, or a gradient algorithm.

**NOT OBSERVED / HELD, separately for the new code, each repeated control, each context property, each witness full vector and prior-surface extrapolation:** refusal, wrong bytes, missing admission/running ownership, absent/ambiguous column binding or physical closure holds the affected property. Missing64-row coverage holds its full-block certificate without erasing valid observed partial distinctions/contradictions. Missing controls hold old-to-new extrapolation; never substitute old native values as absent new targets. A present zero, blank or unexpected code remains an observation, not an unavailable export. All omitted facets and universal identification remain held.

## Original export, physical closure and primary selection

Export the naturally available complete original native CSV once. Preserve every chart/builtin/source column and all original rows through the frontier, original bytes/length/SHA256, decimal strings, signed zero, blanks and duplicate headers by ordinal. Bind all40 literal source plot ordinals to actual columns using exact executed source SHA, distinct private source/version and genuinely exposed Save/Add plot metadata. Titles alone do not prove ownership. Retain separate complete exposed Save and Add compiler bodies, warnings/markers and immediate/settled UI. Admission alone is not a running-source certificate; blanks under runtime failure are not numeric/NA witnesses.

Independently classify physical2m closure from native chart time units, actual export/observation UTC and CHART_CONFIRMED; INPUT_TIME milliseconds must agree with chart time. Return original CSV-SHA/row/column/time closure masks. Select the **first64 consecutive independently closed source-owned rows** with increasing timestamps and consecutive INPUT_INDEX. Use ownership/input context/closure only, never getter/equality/model agreement. No predecessor or own-index-zero requirement. Retain real market-time gaps; do not synthesize bars or force120-second timestamp increments.

Maximum primary plot cells **2,560=64×40**, including192 context cells;37 color-code columns contribute2,368 unique cells (2,304 repeated controls +64 new-query cells). Repeated models/hypotheses do not multiply native cells or parity credit. All other closed and developing/present cells stay OBSERVED / EXCLUDED with exact causes, zero primary credit. No sampling-completeness, full-history, original-frontier or realtime identity claim. If the one export lacks a block/metadata facet, retain partial observations and mark that certificate NOT OBSERVED/HELD. Never wait for preferred results, navigate history, re-export, splice sessions or retry.

## Return and preservation evidence

Return `v101/captures/v101/RESPONSE-v101-v1.md`, finite attempt inventory, raw numeric-controls/property/facet verdicts, `artifact-integrity-v1.json` covering every dependency/return path/length/SHA256 (self-excluded), a read-only validator and `validation-result-v1.json`. Increment versions; never overwrite previous evidence. Preserve all original requested/executed bytes, Save-form transport, actual source/private version/plot identities as exposed, separate Save/Add/compiler/error bodies, context/settings/feed state, timestamps, original CSV, bindings, closure/dependency receipts, failures and cleanup. Missing native feed/execution IDs, independent editor arrays or complete private inventory remain UNOBSERVED; do not inspect hidden state or infer them from a local compiler.

For both witnesses include exact prediction-file SHA/pointer, all source plot ordinals, original CSV-SHA/row/column/header/raw target pointers, actual comparisons, SUPPORTED/REFUTED/UNDECIDED and exact exclusions/causes. Old reference CSV pointers are provenance only; every target comes from this new original source-owned export. No tolerance, inferred alpha as target, amended palette, post-hoc quantizer or fitted row filter. Exact raw-code comparisons are decidable; unresolved capture precision remains explicitly separate and never rewrites raw numbers.

Passively record before/after saved-layout/script/open-tab comparisons and preservation holds, keeping P425PrivateV79v1 and all old layouts/scripts/tabs/private libraries/account state unchanged. Do not repair an unknown old-layout difference. Contributions of native tooling need their own explicit license; no corpus-wide license rewrite. No engine fix, fixture promotion, universal color/identity model, pixel/CSS/DPI contract, original-frontier reconstruction or historical hold1/2/7/8/13/14/21 closure. **Local commit only; DO NOT push.**
