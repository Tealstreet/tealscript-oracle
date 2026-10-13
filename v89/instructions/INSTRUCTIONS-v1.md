# Oracle v89 requested-daily discriminator instructions v1

## Fixed existing chart and authorization

**ALLOWED: Save as a PRIVATE unpublished script, Add to the existing basic BINANCE:BTCUSDT 2-minute UTC chart, then remove only the request-added study. FORBIDDEN: publish/share, visibility change, new or different layout, any symbol/interval/layout-setting change, alerts, or any library action. Anything beyond this authorized method: STOP as BLOCKED-NEEDS-OWNER-APPROVAL.**

Use ONLY the already-open saved chart **basic**, layout ID **xlvYwHdH**, **BINANCE:BTCUSDT, 2 minutes, Etc/UTC**. This is the context observed by v88. Verify the actual native chart model/checked interval, not the stale URL interval parameter. Record chart identity, actual symbol/interval/timezone, original studies/properties and saved state before starting. If they differ, STOP BLOCKED-NEEDS-OWNER-APPROVAL. Do not switch charts, load another layout, navigate to a daily interval, disable autosave or change settings. All daily calculations occur inside the explicit request.security("BINANCE:BTCUSDT", "1D", ..., lookahead=barmerge.lookahead_on); the chart stays 2m throughout.

Save through the native Pine Editor as a PRIVATE unpublished script, Add to that existing chart, export/inspect through the existing permitted path, then remove only the study added for that attempt. Preserve all prior studies and layout settings. Leave the private saved script; no deletion is authorized. No publication, share, visibility change, new layout, symbol/interval change, alert, library action or account change. If anything more is needed, record BLOCKED rather than change the chart or broaden scope.

## Four fresh captures

Run sha256sum -c SHA256SUMS in v89/. Capture each exact v5/v6 source twice, independently, with attempt-v1 and attempt-v2 directories. Keep source bytes, version, explicit request symbol/timeframe, lookahead and omitted calc_bars_count/max_bars_back unchanged. All native values and phases are UNSPECIFIED; never calibrate a counter to the old corpus result or repair a refusal.

For each attempt retain executed-v1.pine and its hash, private script identity, native Save/compile transaction, Add outcome, UTC capture clock, actual chart context and complete raw compiler/editor diagnostics separately. Establish fresh compilation/calculation; cached no-op responses or stale plot buffers do not constitute a second capture. Save and Add use the native editor, not a direct compiler API substitute. If execution is refused, preserve the refusal rather than editing the source.

Export the available **2-minute chart OHLCV and all sixteen observer plots**, per chart row, preserving exact headers, numeric strings and empty cells. Do not request a chart interval change or reconstruct daily OHLCV from 2m bars. Use only the existing permitted export path. If export is unavailable, record exactly which evidence is unobserved, without performing a prohibited action. A cropped available export is valid if its frontier limitations are recorded; no layout change to obtain earlier rows is authorized.

## Observers and calculation frontier

CHART_TIME, CHART_BAR_INDEX and CHART_ISCONFIRMED describe the 2m chart row. REQUEST_TIME, REQUEST_BAR_INDEX, REQUEST_ISFIRST, REQUEST_FIRST_EVALUATED, REQUEST_CHANGE, REQUEST_COUNTER and REQUEST_CHANGE_IS_NA are evaluated **inside the daily request** and merged onto each chart row with lookahead_on. Daily values can repeat over many 2m rows: repeated output rows are not additional daily evaluations or counter increments.

REQUEST_FIRST_EVALUATED marks the first actual f_observers evaluation before first_time is assigned. FIRST_REQUEST_TIME, FIRST_REQUEST_BAR_INDEX, FIRST_REQUEST_ISFIRST, FIRST_REQUEST_CHANGE, FIRST_REQUEST_COUNTER and FIRST_REQUEST_CHANGE_IS_NA carry that first evaluation's snapshot to later chart rows. Its assignment is independent of barstate.isfirst; neither barstate.isfirst nor a visible-window start is assumed to mark the actual requested calculation frontier. If the first daily frame precedes the exported chart window, report that and read the carried snapshot instead of inventing an earlier row. Retain an accessible Data Window/screenshot with these fields; do not change chart interval or settings to inspect them.

In v5, a missing timeframe.change bool is an empty REQUEST_CHANGE with REQUEST_CHANGE_IS_NA=1; false is 0 with missing mask 0. The same distinction is carried by FIRST_REQUEST_CHANGE and FIRST_REQUEST_CHANGE_IS_NA. The v6 control projects its true/false result and exposes the same numeric missingness mask. Preserve blanks; do not relabel missing as false. If carried fields are unavailable, report FRONTIER-UNOBSERVED rather than inferring initialization from a late count.

Record both chart and requested history boundaries. CHART_ISCONFIRMED establishes only the 2m row's confirmation, not the daily request's closure. Record capture clock and the current requested daily time; identify developing/open daily intervals separately and leave them unscored. Keep their raw rows. Do not count developing daily rows as closed because their 2m chart rows are confirmed. No waiting for daily rollover or chart change is required. Compare repeats on their common confirmed chart rows whose requested daily bars are closed, while retaining all frontier observations separately.

## Return and adjudication question

Return captures/v89/RESPONSE-v89-v1.md, attempt-inventory-v1.json and four per-attempt sources, observations, chart CSVs, raw diagnostics/transactions, accessible Data Window screenshots and checksums. A four-row summary identifies source/version/attempt, freshness, chart earliest time, first requested time/index/isfirst/change/missing/counter, requested-first-evaluated visibility, closed chart/daily coverage and repeat agreement. Record removal of each added study and unchanged chart/layout/symbol/interval/timezone and original study state.

Settle whether the first actual requested daily timeframe.change("1D") is false, true or missing in v5/v6, and whether the carried frontier/count differs across repeats or versions. Align by REQUEST_TIME, not chart row number. If histories differ, report actual boundaries without shifting counts. The engine replay will mirror the captured 2m chart context. This minimal discriminator omits the original pivot array and does not certify complete original-program historical/provider equivalence. No engine change or parity credit is made by the capture agent.
