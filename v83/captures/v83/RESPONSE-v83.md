# Oracle v83 native compilation response v1

**55 source-exact native private Save/Add repetitions captured; all 55 full compiler outcomes are COMPILE-ERROR.** Eleven unchanged sources have five repetitions each. No source repair, runtime/numeric credit, historical group-wide credit, or general diagnostic-order rule is claimed.

All five complete marker arrays per source, including immediate and five-second settled samples, timestamps, severity, exact text, owner, exposed code, sites, native order and exact occurrence counts, are in [compiler-editor-comparison-v1.json](compiler-editor-comparison-v1.json). They are preserved without sorting, deduplication, or compiler/editor merging. The following table reports the settled array lengths in repetition order; it does not replace those full arrays.

| Shape | Settled marker counts, repetitions 1–5 | Observed settled arrays |
| --- | --- | --- |
| nonliteral-callable-default | 2, 2, 2, 2, 2 | Advisory, default-value error |
| unused-method-receiver | 1, 2, 1, 2, 1 | Advisory only on 1/3/5; advisory, unused-self error on 2/4 |
| namespace-named-receiver | 1, 2, 1, 2, 1 | Advisory only on 1/3/5; advisory, namespace method error on 2/4 |
| builtin-method-shadow-declaration | 2, 2, 2, 2, 2 | Advisory, ta.ema shadowing error |
| optional-only-overload-declaration | 2, 2, 2, 2, 2 | Advisory, overload required-parameter error |
| library-version-refusal | 2, 3, 2, 3, 2 | Advisory, missing float.pick error on 1/3/5; advisory, missing float.pick error, import-version error on 2/4 |
| builtin-name-object-declaration | 2, 2, 2, 2, 2 | Advisory, invalid object-name error |
| private-library-namespace-method | 2, 2, 2, 2, 2 | Advisory, missing lib.pick error |
| unavailable-footprint-type | 2, 2, 2, 2, 2 | Advisory, invalid footprint type error |
| missing-builtin-receiver-id | 2, 2, 2, 2, 2 | Advisory, missing id parameter error |
| unavailable-footprint-call | 2, 2, 2, 2, 2 | Advisory, unavailable request.footprint error |

The native `getModelMarkers` arrays place `PINE_VERSION_OUTDATED` first in all 55 settled samples: **55 advisories and 51 error occurrences**, including six advisory-only lists. Eight sources expose one identical raw settled-array variant across their five samples. The unused-receiver, namespace-named-receiver and library-version sources each expose two variants. These are timed observations from this editor run; the producer retains classification authority. Absence of an editor error does not imply acceptance. The first unused-receiver attempt's provisional `UNSETTLED` classification in `observation-v1.json` is superseded by `observation-v2.json`, which binds its full native refusal without changing its original marker evidence.

Compiler bodies remain a separate channel: **66 complete source-matched full Save/translate responses**, with 22 HTTP 200 and 44 HTTP 304. Each first repetition produces one private Save/new response and one Add/translate response. Repetitions 2–5 invoke unchanged native Save, which emits no new Save request, then native Add, which exposes the cached translate refusal. HTTP 304 bodies are browser cache reuse, not proof of fresh server evaluations. Ten additional source-matched native background `translate_light` responses are retained separately; parse-title and auth receipts are not credited as full compilation.

Every full response exposes `success:false` and one `reason2.errors` occurrence. All 66 expose empty `result.metaInfo.warnings`. `reason2.warnings` is absent for unused-method-receiver, optional-only-overload-declaration, library-version-refusal and unavailable-footprint-type; it is an empty array for the other seven sources. Missing arrays are not reconstructed. The library-version full compiler error is the v5/v6 import refusal; the editor's missing float.pick error is a separate observed diagnostic. Native full-response error codes are not exposed. Advisory codes in editor arrays remain separate.

The [attempt inventory](attempt-inventory-v1.json) binds each executed-source SHA-256, request id, full-response digest, private `USER` script identity/version, raw compiler errors and all five attempts. Every source was saved privately under its unique, versioned probe name, preserving its exact original indicator title and source bytes. Every saved identity is a new `USER` script at version `1.0`, created by this request; no publication identity or publication URL was created. Exact editor files preserve requested LF bytes and trailing-newline presence; multipart requests retain native wire CRLF, verified against the same source after transport newline conversion.

Each Add creates one error study despite compilation refusal. All **55 request-added study ids** were removed individually; pre-existing studies were never removed or re-added. Before every Add and after every restoration, the full main-series properties, symbol `BINANCE:BTCUSDT`, interval `2`, timezone `Etc/UTC`, style `1`, original script id `zy7yxn` and its encrypted input payload, and every other native study's identity/properties match the pre-request record exactly. Before/after receipts are in [environment-v1](environment-v1/chart-context-before-v1.json).

Authorized actions were native private unpublished Save, Add, read-only inspection and removal of request-added studies. **No Publish (including private publication), Share, visibility change, new/saved layout action, symbol/interval/setting change, alert, library publication or manual library import occurred.** Existing source import declarations were resolved only through ordinary compilation. No direct compiler API substitute or chart data export was used.

Validation: [audit-v1.json](audit-v1.json) passes 55 exact executed-source checks, 66 full compiler source/identity bindings, all native background-source bindings, and 55 complete chart restorations. All 21 request-bundle checksums pass; [integrity-v1.json](integrity-v1.json) binds every returned evidence artifact. The eleven representatives do not automatically credit their 78 historical group attempts.
