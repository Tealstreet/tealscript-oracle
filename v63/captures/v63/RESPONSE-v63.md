# v63 native capture response v2

All eight unchanged indicators have independent Chrome MCP observations: four RUNS with original native CSV exports and four compilation refusals. No source remains unattempted.

[Attempt inventory](attempt-inventory-v2.json) · [Audit](audit-v2.json) · [Integrity hashes](environment-v1/integrity-v2.json)

Captured on the mini, account sours-lat, BINANCE:BTCUSDT ordinary candles, Binance provider, 2 minutes, Etc/UTC, 24x7 session, default inputs. All 19 bundled SHA256 checks pass. Exact source bytes/hashes, compiler markers with all owners/codes/sites, full Save/compiler response bodies, screenshots, snapshots and actual chart settings are retained. Codes absent from v5 responses are explicitly unavailable.

All four native CSVs retain original time/OHLC/Volume and positional observer bytes, numeric strings and missing cells. Each contains at least 32 confirmed closed bars; cutoff and open-row timestamps are recorded independently. No realtime or engine-derived native evidence is claimed.

## Observed answers

- The `ta.change` and `ta.highest` sources compile and RUN in both Pine versions. Every closed native `ta.change` Plot string is `1`. The `ta.highest` Plot is a changing price-valued series; all original strings are retained in its CSV, with raw ranges below.
- For both highest captures, a derived Decimal comparison of the native CSV matches Plot exactly to `2 * maximum physical high over 13 bars + 1` on every closed row with sufficient CSV history. This is a comparison against native observations, explicitly separate from those observations. Compilation/runtime admission does not establish execution of the custom Holder method body.
- Custom `ta.crossover` and `ta.rsi` sources refuse in both versions at 8:5: their constructs cannot shadow existing builtin functions; native advises renaming the method or receiver variable. v6 exposes CE10195; v5 codes are unavailable.
- Each method name and version is an independent exact-source observation. These results do not extend to a general namespace policy.
- Response v2 supersedes the earlier draft summary that assumed Plot=41. Native CSV bytes and captured screenshots are unchanged; the per-source observations record the original actual strings.

## Per-source evidence

| Source | Native outcome | Diagnostic or closed raw observer | Evidence |
| --- | --- | --- | --- |
| `custom-ta-change-v5-v61-v1.pine` | RUNS | Plot=1; 985 closed bars | [observation](custom-ta-change-v5-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-change-v6-v61-v1.pine` | RUNS | Plot=1; 985 closed bars | [observation](custom-ta-change-v6-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-crossover-v5-v61-v1.pine` | COMPILE-ERROR | code unavailable 8:5 ta.crossover() constructs cannot shadow existing built-in functions. Rename the method or the variable that it is called with. | [observation](custom-ta-crossover-v5-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-crossover-v6-v61-v1.pine` | COMPILE-ERROR | CE10195 8:5 ta.crossover() constructs cannot shadow existing built-in functions. Rename the method or the variable that it is called with. | [observation](custom-ta-crossover-v6-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-highest-v5-v61-v1.pine` | RUNS | Plot=165179.34 to 166469; 247 unique original strings; 985 closed bars | [observation](custom-ta-highest-v5-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-highest-v6-v61-v1.pine` | RUNS | Plot=165179.34 to 166469; 247 unique original strings; 985 closed bars | [observation](custom-ta-highest-v6-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-rsi-v5-v61-v1.pine` | COMPILE-ERROR | code unavailable 8:5 ta.rsi() constructs cannot shadow existing built-in functions. Rename the method or the variable that it is called with. | [observation](custom-ta-rsi-v5-v61-v1/attempt-v1/observation-v4.json) |
| `custom-ta-rsi-v6-v61-v1.pine` | COMPILE-ERROR | CE10195 8:5 ta.rsi() constructs cannot shadow existing built-in functions. Rename the method or the variable that it is called with. | [observation](custom-ta-rsi-v6-v61-v1/attempt-v1/observation-v4.json) |
