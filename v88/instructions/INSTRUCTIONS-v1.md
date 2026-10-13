# Oracle v88 requested-daily first-change discriminator instructions v1

## Authorization and chart prerequisite

**ALLOWED: Save as a PRIVATE unpublished script, Add to chart, then remove only the request-added study. FORBIDDEN: publish/share, visibility change, new layout, symbol/interval change to any saved layout, alerts, or any library action. Anything beyond this authorized method: STOP as BLOCKED-NEEDS-OWNER-APPROVAL.**

Required context is **BINANCE:BTCUSDT,1D**. Use an already configured matching chart, or an existing unsaved chart context that can display that symbol/interval without creating a layout or changing any saved layout. Before any action record chart identity, symbol, interval, timezone, existing studies and saved/unsaved state. Do not change the symbol/interval of a saved layout, even temporarily; do not disable autosave or change persistent settings to work around it. If the required context is unavailable within this scope, stop as **BLOCKED-NEEDS-OWNER-APPROVAL**. Do not substitute a 2-minute chart or aggregated daily feed.

Use native Pine Editor Save as a PRIVATE unpublished script and Add to chart. Remove only each request-added study after its evidence/export is complete, preserving all original studies and chart state. No publication,Share,visibility change,new layout,alerts,library publication/import or other library action. Retain the private saved scripts; no script deletion is authorized. If any additional action is required, stop rather than broaden authorization.

## Four independent captures

Verify SHA256SUMS. Capture the unchanged v5 discriminator twice and unchanged v6 control twice, each as attempt-v1 and attempt-v2 under its own source directory. Source hashes, filenames and byte lengths are in bundle-manifest-v1.json. Do not repair a refusal or change a version, expression, lookahead, inputs or identifier. Keep omitted calc_bars_count/max_bars_back at native defaults; do not add a counter seed or calibrate against the old target values. Native status and all numeric/boolean outcomes are **UNSPECIFIED**.

For each capture record exact executed source/hash, source-matched Save/compile transaction, timestamps, private script identity, Add outcome and fresh calculation. Do not count a cached/no-op compiler response or stale plot buffer as an independent run. Record raw complete compiler/editor diagnostics separately if any. Save and Add must happen through the native editor, not direct API substitution.

Export chart OHLCV and all fifteen plotted observer columns with original numeric strings and empty cells. Request the complete available daily dataset including its earliest row; preserve source/context/cutoff and exact headers. Use an existing authorized export path only; if data export or earlier-row inspection needs a prohibited layout/setting/account action, stop and report the missing evidence. Native OHLCV must be actual exported daily input, not synthetic values or reconstructed aggregates.

## Requested history frontier, not only the visible chart start

The per-request observers are REQUEST_TIME,REQUEST_BAR_INDEX,REQUEST_ISFIRST,REQUEST_CHANGE,REQUEST_COUNTER,REQUEST_CHANGE_IS_NA. The carried FIRST_REQUEST_* fields record the first actual f_observers evaluation, even if that requested bar precedes the exported chart window. The capture does not seed those values; native execution supplies them. These carried fields are assigned once when their time is initially missing, independently of barstate.isfirst, so that flag itself remains evidence rather than an assumption.

Locate the first requested time/index and any REQUEST_ISFIRST=1 row. Retain a Data Window/screenshot of that earliest row when accessible. If it is outside the exported chart window, record that fact and the carried first time/index/isfirst/change/missing/counter instead of inventing a row. If carried fields remain missing or the earliest requested frame cannot be identified, report FRONTIER-UNOBSERVED; no initialization truth is inferred from a late cumulative counter alone. Record chart-first time separately from first requested time and any earlier evaluated history exposed by native evidence.

The v5 probe preserves a missing boolean change as an empty REQUEST_CHANGE cell plus REQUEST_CHANGE_IS_NA=1; false is numeric0 with missing-mask0. The v6 probe uses its ordinary true/false numeric projection and the same numeric missingness observer. Do not treat a blank v5 first change as false or true, or replace missing cells. Export FIRST_REQUEST_CHANGE_IS_NA alongside FIRST_REQUEST_CHANGE. Record the native distinction if observed without prescribing it.

CHART_ISCONFIRMED identifies closed daily rows. Mark the developing/open daily row unscored and record the capture cutoff/clock. Match REQUEST_TIME to chart daily keys rather than assuming each visible row is a new requested evaluation. Explain any merge gaps or repeated requested timestamps. Keep lookahead_on unchanged.

## Return and questions

Return captures/v88/RESPONSE-v88-v1.md,attempt-inventory-v1.json and four per-attempt executed-v1.pine,observation-v1.json,CSV,raw diagnostics,source-matched transactions,first-bar screenshots/Data Window readings and checksums. Use a four-row summary table: source/version/attempt,private identity,freshness,chart earliest time,requested earliest time/index,isfirst,first change plus missing mask,first counter,closed-row count and repeated-run agreement. Record study removal and unchanged chart/layout state.

Settle whether the first evaluated requested daily timeframe.change("1D") is false,true or missing in each version; show the requested history frontier that produces the counter. Compare both repeats per version and align shared closed daily times across v5/v6. If histories differ, state their actual boundaries instead of calibrating counters. If fields are missing,incomplete or no fresh execution occurs, return UNOBSERVED/CONTEXT-UNMET and the precise reason. Any prohibited action needed gives BLOCKED-NEEDS-OWNER-APPROVAL.

This round is an independent first-change discriminator. It omits the original pivot array from the minimal probe; it does not by itself reconstruct every historical requested context of the original v4 corpus program. No engine change or parity credit is made by the capture agent. The owner will adjudicate the first-change/history-frontier hypothesis against the unchanged original after the observations land.
