# Oracle v98 response v5

Native observations returned for 4 of four finite source slots. All four slots have ended. Exact requested bytes and separate complete exposed Save/Add compiler bodies are retained, including any refusals or runtime diagnostics. No retry, repair, source/input variant or history navigation.

| Source | Admission | Original / closed rows | Primary original rows | Private source/version |
| --- | --- | ---: | --- | --- |
| v98-color-constructors-v5 | CAPTURED | 310 / 309 | 15–78 | `USER;b2db574ac6a840de8d5a557c39e77b9f` / 1.0 |
| v98-color-constructors-v6 | PARTIAL ENTRY / MCP FAILURE; SLOT CONSUMED; NO RETRY | UNOBSERVED | NOT OBSERVED | `None` / None |
| v98-color-na-cast-v5 | CAPTURED; CLEANUP SELECTOR FAILURE RECORDED AND SAME STUDY REMOVED | 303 / 302 | 4–67 | `USER;7020aee1d4924ef7abf255cf611a24ff` / 1.0 |
| v98-color-na-cast-v6 | CAPTURED | 305 / 304 | 4–67 | `USER;7bfa5b1ce45342d2a04fe5ff233a5661` / 1.0 |

Primary selection is the earliest64 consecutive source-owned independently closed rows beginning at CASE_ID0, with increasing timestamps and consecutive INPUT_INDEX. Cast sources additionally retain the immediately preceding closed owned original row. Physical2m closure, export UTC, CHART_CONFIRMED and own millisecond INPUT_TIME are jointly checked. Each available complete constructor block has four visits per case; each available cast block has16 per phase. Admission/coverage is NOT OBSERVED for a stopped entry slot. No getter, NA predicate or equality result is an eligibility filter. All original rows/columns/strings/blanks and developing tails remain retained with explicit masks and zero primary credit outside the selected block.

**v98-color-constructors-v5**

| Route | Equality outcome counts across64 rows | Frozen full-model verdicts |
| --- | --- | --- |
| LITERAL_RGB | {"SINGLE_LITERAL_MATCH": 64} | BYTE_FLOOR: REFUTED; BYTE_ROUND: SUPPORTED; PERCENT_CEIL_THEN_BYTE_ROUND: REFUTED; PERCENT_ROUND_THEN_BYTE_ROUND: REFUTED; SUPPORTED_FROZEN_MODELS |
| LITERAL_NEW | {"NEITHER_LITERAL": 4, "SINGLE_LITERAL_MATCH": 60} | BYTE_FLOOR: REFUTED; BYTE_ROUND: REFUTED; PERCENT_CEIL_THEN_BYTE_ROUND: REFUTED; PERCENT_ROUND_THEN_BYTE_ROUND: REFUTED; NEITHER_MODEL |
| SERIES_RGB | {"SINGLE_LITERAL_MATCH": 64} | BYTE_FLOOR: REFUTED; BYTE_ROUND: SUPPORTED; PERCENT_CEIL_THEN_BYTE_ROUND: REFUTED; PERCENT_ROUND_THEN_BYTE_ROUND: REFUTED; SUPPORTED_FROZEN_MODELS |
| SERIES_NEW | {"SINGLE_LITERAL_MATCH": 64} | BYTE_FLOOR: REFUTED; BYTE_ROUND: SUPPORTED; PERCENT_CEIL_THEN_BYTE_ROUND: REFUTED; PERCENT_ROUND_THEN_BYTE_ROUND: REFUTED; SUPPORTED_FROZEN_MODELS |

Old RGB12.5 EQ_DF ternary / Boolean-NA-preserving code combinations: `{('0', '0'): 64}`. Full 16-case × four-route × four-visit R/G/B/T/NA and five-equality vectors, candidate actual T getters, adjacency graph, cross-route equality and each frozen rational-policy prediction are in numeric controls. BOOLEAN_NA_EQUALITY, NEITHER_LITERAL, MULTIPLE_LITERAL_MATCHES and calibration contradictions are distinct observations. A supported source-literal equality never proves an unexposed stored alpha byte.

**v98-color-constructors-v6**

Numeric observations NOT OBSERVED; see the native refusal/context receipts.

**v98-color-na-cast-v5**

| Value | Phase0 R / G / B / T / NA raw tuple |
| --- | --- |
| CAST | 0 / 0 / 0 / 100 / 0 |
| VAR | 0 / 0 / 0 / 100 / 0 |
| ARRAY | 0 / 0 / 0 / 100 / 0 |
| HISTORY | 33 / 66 / 99 / 13 / 0 |
| CAST_HISTORY | 0 / 0 / 0 / 100 / 0 |
| NZ_DEFAULT | 0 / 0 / 0 / 100 / 0 |
| NZ_REPLACEMENT | 0 / 0 / 0 / 100 / 0 |
| GRAD_CAST | 255 / 0 / 0 / 50 / 0 |
| GRAD_NA | 255 / 0 / 0 / 50 / 0 |

Here ∅ means an original blank cell, not a synthesized color. Every phase and predecessor is retained independently. The v5 −1 code remains Boolean NA, distinct from0/false and a blank numeric getter. VAR/ARRAY and constant/selected-branch history transfers use actual same-source predecessor/target pointers. For a prior DF branch, CASE_ID/CURRENT_NA witness the expression; no absent preceding DF channel tuple is invented. Literal DF T13 is a separate nearest-percent getter hypothesis.

- A_ORDINARY_MISSING_PROPAGATION: **REFUTED**; {'REFUTED': 64}
- A_ORDINARY_MISSING_TRANSFER_AND_FALLBACK_CANDIDATE: **REFUTED**; {'REFUTED': 64}
- B_PRESENT_TRANSPARENT_BLACK: **SUPPORTED**; {'SUPPORTED': 64}
- C_PRESENT_OPAQUE_BLACK: **REFUTED**; {'REFUTED': 64}
- D_NON_NA_WITH_BLANK_GETTERS: **REFUTED**; {'REFUTED': 64}
- GRAD_CAST_EQUALS_BARE_NA_COMPLETE_RAW_TUPLE: **SUPPORTED**; {'SUPPORTED': 64}
- NZ_DEFAULT_NA_PREDICATE_FALLBACK_RELATIONSHIP: **SUPPORTED**; {'SUPPORTED': 64}
- NZ_REPLACEMENT_NA_PREDICATE_FALLBACK_RELATIONSHIP: **SUPPORTED**; {'SUPPORTED': 64}

The ordinary-missing, finite-black and non-NA/blank-getter alternatives are bounded tuple candidates. NZ fallback recognition and cast-versus-bare-na gradient equivalence are separate tests; neither overwrites the native cast predicate or supplies hidden identity.

**v98-color-na-cast-v6**

| Value | Phase0 R / G / B / T / NA raw tuple |
| --- | --- |
| CAST | 0 / 0 / 0 / 100 / 1 |
| VAR | 0 / 0 / 0 / 100 / 1 |
| ARRAY | 0 / 0 / 0 / 100 / 1 |
| HISTORY | 33 / 66 / 99 / 13 / 0 |
| CAST_HISTORY | 0 / 0 / 0 / 100 / 1 |
| NZ_DEFAULT | 0 / 0 / 0 / 100 / 0 |
| NZ_REPLACEMENT | 33 / 66 / 99 / 13 / 0 |
| GRAD_CAST | 255 / 0 / 0 / 50 / 0 |
| GRAD_NA | 255 / 0 / 0 / 50 / 0 |

Here ∅ means an original blank cell, not a synthesized color. Every phase and predecessor is retained independently. The v5 −1 code remains Boolean NA, distinct from0/false and a blank numeric getter. VAR/ARRAY and constant/selected-branch history transfers use actual same-source predecessor/target pointers. For a prior DF branch, CASE_ID/CURRENT_NA witness the expression; no absent preceding DF channel tuple is invented. Literal DF T13 is a separate nearest-percent getter hypothesis.

- A_ORDINARY_MISSING_PROPAGATION: **REFUTED**; {'REFUTED': 64}
- A_ORDINARY_MISSING_TRANSFER_AND_FALLBACK_CANDIDATE: **REFUTED**; {'REFUTED': 64}
- B_PRESENT_TRANSPARENT_BLACK: **REFUTED**; {'REFUTED': 64}
- C_PRESENT_OPAQUE_BLACK: **REFUTED**; {'REFUTED': 64}
- D_NON_NA_WITH_BLANK_GETTERS: **REFUTED**; {'REFUTED': 64}
- GRAD_CAST_EQUALS_BARE_NA_COMPLETE_RAW_TUPLE: **SUPPORTED**; {'SUPPORTED': 64}
- NZ_DEFAULT_NA_PREDICATE_FALLBACK_RELATIONSHIP: **SUPPORTED**; {'SUPPORTED': 64}
- NZ_REPLACEMENT_NA_PREDICATE_FALLBACK_RELATIONSHIP: **SUPPORTED**; {'SUPPORTED': 64}

The ordinary-missing, finite-black and non-NA/blank-getter alternatives are bounded tuple candidates. NZ fallback recognition and cast-versus-bare-na gradient equivalence are separate tests; neither overwrites the native cast predicate or supplies hidden identity.

Read-only validation: **PASS**; 918 original rows, 915 independently closed archive rows, 192 primary rows and 12096 unique primary plot cells. 4544 model records and 82880 raw pointer references are repeated analysis records, not unique cells. See [validation](validation-result-v5.json), [numeric controls](numeric-controls-v5.json), [attempt inventory](attempt-inventory-v5.json) and [facet capabilities](facet-capabilities-v5.json).

Only new layout `208272282/xAMH4kSC` (`oracle-v98-v1`) is used. Every successfully added own study has been removed and the new layout saved; builtin Vol remains. Full native records and passive before/after signatures are compared individually; any context difference is recorded as a preservation hold, never repaired by editing an old layout. See [preservation comparison](environment-v2/existing-layout-comparison-v1.json).

P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. New private scripts are distinct saves; no old script is overwritten/deleted/renamed. Full private script inventory, independent editor marker arrays, unexposed native feed/execution IDs and actual calculation counts remain UNOBSERVED. Per-source compiler diagnostics keep exposed warnings/errors separate from immediate/settled UI and absent arrays.

Run `python3 v98/captures/v98/validate-evidence-v4.py 5` from repository root. [Integrity](artifact-integrity-v5.json) covers request/frozen sources, all returned artifacts and referenced prior dependencies, self-excluded. [Tooling rights](CAPTURE-TOOLING-LICENSE-v1.md) apply only to new capture tooling. No engine change/fixture promotion, hidden storage decoder, universal color model, rendered pixel/DPI/CSS contract or closure of historical holds1/2/7/8/13/14/21 follows from this capture.

Native action totals: 3 PRIVATE source Saves, 3 Adds, 3 original exports, 1 consumed partial-entry slot(s). Stopped constructor v6 has no Save/Add/compiler result, no executed-byte identity and no numeric credit. No retry or budget borrowing.

Preservation observations: 13/13 saved records unchanged; 0 saved-record differences; 8/9 open-tab signatures unchanged; 1 open-tab differences. Native page IDs were reassigned after the MCP bridge restart and were mapped by stable layout URL.

**PRESERVATION HOLD — original page3**: before `{"activeLayout": ["oracle-v91-v1"], "canvas": ["Chart for BINANCE:BTCUSDT, 2 minutes"], "checkedRadios": ["2 minutes", "Candles"], "url": "https://www.tradingview.com/chart/RRvYItzu/"}`; after `{"activeLayout": ["oracle-v91-v1"], "canvas": ["Chart for BYBIT:BTCUSDT.P, 2 minutes"], "checkedRadios": ["2 minutes", "Candles"], "url": "https://www.tradingview.com/chart/RRvYItzu/"}`. The actual context difference is observed; cause is UNOBSERVED. No old layout reload, edit or restoration was performed by this workflow; unchanged-tab preservation cannot be certified for this context. Numeric observations belong only to the independently identified new v98 layout.
