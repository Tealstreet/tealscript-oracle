# Oracle v97 response v6

Progress return: 6 of14 eligible source/version slots returned. Selection is frozen against v95 response v24 at c7790f48d913a0736606af6bb94a2f2ee011f309, after completed v95 and v96. Mandatory items2–5 supply8 slots; only explicit own-origin holds activate items7/10/14 v5+v6. The other24 reservations are skipped with exact reasons. No new or modified Pine is used.

| Source | Final single CSV rows | Prefix criterion | CSVs / calendar selections |
| --- | ---: | --- | --- |
| v97-conditional-clock-v5 | 23754 | CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX | 2 / 1 |
| v97-conditional-clock-v6 | 23755 | CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX | 1 / 0 |
| v97-udf-state-v5 | 23757 | CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX | 1 / 0 |
| v97-udf-state-v6 | 23759 | CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX | 1 / 0 |
| v97-recursive-holes-v5 | 23761 | CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX | 1 / 0 |
| v97-recursive-holes-v6 | 23763 | CAPTURED / COMPLETE_OWN_INDEX_ZERO_PREFIX | 1 / 0 |

Each successful prefix is owned by its exact unchanged v95 source SHA and new private source/version. The first physical row must be INPUT_INDEX0/IS_FIRST1/FIRST_INDEX0 with INPUT_TIME=FIRST_TIME=CSV time×1000; every subsequent source index and timestamp is checked through the last row. At least0..127 are independently physically closed and native-confirmed. Item5 additionally requires own OHLC to agree with actual chart columns. Real timestamp gaps remain archived; no rows are synthesized or joined.

Every original CSV, header/column ordinal, string, blank/NA, fractional residue, chart/builtin input and later row is retained. Separate cropped diagnostic and post-navigation sessions are never spliced. Only the selected final single CSV may establish the startup prefix; earlier closed archive rows earn no startup credit. The primary model block is exactly own0..127, without output/NA/mask filtering. Complete prior inputs are referenced by original source/session SHA, row range and column ordinals.

| Source | First finite native targets (own index; raw value) |
| --- | --- |
| v97-conditional-clock-v5 | EMA_ALL=2; `-4`; EMA_BRANCH=4; `-2.6666666666666665` |
| v97-conditional-clock-v6 | EMA_ALL=2; `-4`; EMA_BRANCH=4; `-2.6666666666666665` |
| v97-udf-state-v5 | LOCAL_FIRST=5; `5` |
| v97-udf-state-v6 | LOCAL_FIRST=5; `5` |
| v97-recursive-holes-v5 | EMA_CLEAN=2; `-4`; EMA_HOLE=5; `-1`; RMA_CLEAN=2; `-4`; RMA_HOLE=5; `-1`; RSI_CLEAN=3; `100`; RSI_HOLE=6; `100`; TSI_CLEAN=7; `1`; TSI_HOLE=10; `1` |
| v97-recursive-holes-v6 | EMA_CLEAN=2; `-4`; EMA_HOLE=5; `-1`; RMA_CLEAN=2; `-4`; RMA_HOLE=5; `-1`; RSI_CLEAN=3; `100`; RSI_HOLE=6; `100`; TSI_CLEAN=7; `1`; TSI_HOLE=10; `1` |

These are observed targets, independently from algorithm verdicts. [Numeric controls](numeric-controls-v6.json) points to immutable per-source reports containing every primary native target and frozen seed/clock/hole/copy/NA/random candidate record, native NA witnesses, raw pointers, exact residuals, precision causes and property verdict counts. First-finite EMA versus SMA3 seeds, gated versus every-bar clocks, LOCAL_FIRST first reach versus reinitialization, EMA/RMA missing-output/poison alternatives and independent OHLC-derived ATR seed candidates retain distinct verdicts. No exported target supplies a recurrence seed. RSI/TSI, DMI/Supertrend and random streams retain independent native vectors and unresolved algorithm facets. Later Supertrend transitions, when present, are an explicitly scoped raw closed-vector witness table with all preceding own OHLC; they do not introduce a fitted later model block.

A mask or adequately precise integer/dyadic contradiction is a refutation. A native fractional discrepancy with unresolved arithmetic/export precision remains observed and UNDECIDED, without tolerance or rounding/seed/PRNG fit. Source admission, prefix availability, property hypotheses, precision and engine parity remain separate. Own index0 does not recover original v95/v91 frontiers, missing first live events or old clocks.

Read-only audit: PASS. 6 returned sources certify a complete own prefix; 768 primary own rows; 7 original CSVs with 142851 archive rows. Archive counts include any overlap between separate frontiers and are not unique executions. 28768 model records and 36908 raw pointer references are not unique cells. Native/compiler bodies and separate immediate/settled UI are retained, including all exposed warning/error channels; independent editor marker arrays and native instance/feed/execution IDs remain UNOBSERVED.

Only new layout208236729/euz5a92K, oracle-v97-v1, BINANCE:BTCUSDT2m ordinary Candles UTC is used. Each returned own study is removed; default builtin Volume remains. Every selected source has a distinct new PRIVATE unpublished save name and exact original Pine title. P425PrivateV79v1 and sours-lat/P425PrivateV79v1/1: no action. No existing-layout edit, publication/share/visibility/import/alert, reconnect/account/entitlement action, replay, reload/forced recalc, source repair/retry or input variant occurred.

Remaining: 8 selected slots. End-of-round saved-record/tab preservation comparison and final new-layout save are pending. Later in-progress source files are outside this immutable progress revision; their bytes are not overwritten or silently claimed captured.

Run `python3 v97/captures/v97/validate-evidence-v2.py 6`. Canonical evidence for this revision: selection-inventory-v1.json, attempt-inventory-v6.json, numeric-controls-v6.json, facet-capabilities-v6.json, account-actions-v6.json, validation-result-v6.json and artifact-integrity-v6.json, plus every included immutable source/session artifact. The integrity manifest includes frozen request dependencies and self-excludes. New tooling rights are separately stated in CAPTURE-TOOLING-LICENSE-v1.md.

This is a fresh capture contract only: no engine fix/fixture promotion, universal algorithm certificate, recovered live/update completeness or closure of historical holds1/2/7/8/13/14/21 is approved. Consumption and crossed QA remain required.
