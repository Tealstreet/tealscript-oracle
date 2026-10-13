# Oracle round v89 — requested daily counter on the existing 2m chart handoff v1

**ALLOWED: Save as a PRIVATE unpublished script, Add to the existing basic BINANCE:BTCUSDT 2-minute UTC chart, then remove only the request-added study. FORBIDDEN: publish/share, visibility change, new or different layout, any symbol/interval/layout-setting change, alerts, or any library action. Anything beyond this authorized method: STOP as BLOCKED-NEEDS-OWNER-APPROVAL.**

v88 was BLOCKED because no daily chart was permitted. This round needs **no layout, symbol or interval change**. Run the v5 discriminator and v6 control, **two fresh captures each**, on the existing saved **basic** chart, ID **xlvYwHdH**, **BINANCE:BTCUSDT 2 minutes, Etc/UTC**. Do not use the stale URL interval to identify the actual chart. Read [instructions/INSTRUCTIONS-v1.md](instructions/INSTRUCTIONS-v1.md).

Both sources explicitly use request.security("BINANCE:BTCUSDT", "1D", ..., lookahead=barmerge.lookahead_on). Export native 2m chart OHLCV and all **16 observer plots per chart row**: chart time/index/confirmation; requested daily time/index/isfirst/first-evaluated marker/change/missing-mask/counter; and the carried first evaluation's time/index/isfirst/change/missing-mask/counter. Daily observer repetition across 2m chart rows is expected merging, not repeated counter updates. Carried first-evaluation fields can identify the requested frontier even when it predates the chart export.

| Source | Bytes | SHA256 | Captures |
|---|---:|---|---:|
| [v89-v5-requested-daily-counter-p4250m-v1.pine](v89-v5-requested-daily-counter-p4250m-v1.pine) | 2638 | `348244d550c9a9b867654f98620f07da23ad79e96d5734c7097dcfcfa90486f2` | 2 |
| [v89-v6-requested-daily-counter-p4250m-v1.pine](v89-v6-requested-daily-counter-p4250m-v1.pine) | 2617 | `eb286a21a27c5a6f369f20c9daf192f993338e78253e969ce6bede12008f88ea` | 2 |

Native outcomes are **UNSPECIFIED**. Preserve missing vs false and exact numeric strings. Keep open/developing requested daily intervals unscored even if their 2m chart rows are confirmed; record capture clock and both history frontiers. No daily-chart navigation, provider synthesis or counter calibration. The original source hash is d91765c9517a779ff170b0b6632d4941fac93206a3c48be8015b4758e5d6cf20 (native v4 corpus5-pivot-request-counter-v1); its measured +1 across 24,545 closed cells is a question, not an expected answer. The minimal probe omits the pivot array and does not establish full original context equivalence.

Verify sha256sum -c SHA256SUMS from v89/. Return v89/captures/v89/RESPONSE-v89-v1.md and four independent attempts with exact executed sources, source-matched native transactions, CSVs and first-frontier observations. Save PRIVATE, Add, export/inspect, remove only each added study; leave the existing chart and its original studies unchanged. If another action is needed, STOP **BLOCKED-NEEDS-OWNER-APPROVAL**. Publication here is the source request only; no TradingView publication is authorized.
