# V79 publication and capture instructions v1

## Question and existing hold

Does an importer using an accessible, immutable **Pine v5** library refuse private members in v5 and v6, while exported members and exported forwarding through private members run? The earlier v60 v5 question imported the v6 library `sours-lat/R2Nsaa411cdaddab/1` and was masked by a version error. Reusing that library does not answer this question. Exact native outcome, text, code and site here are UNSPECIFIED.

## Publish the prerequisite first

1. Use the capture agent’s authenticated TradingView account. Record its actual publisher username; do not assume it is `sours-lat`. Open a standard BINANCE:BTCUSDT 2-minute chart, regular/24x7 session, Etc/UTC. Record actual chart metadata and ensure at least 32 confirmed bars are available.
2. In the Pine Editor create a **new library draft**, paste `v79-library-v5-v1.pine` verbatim, and Save as `P425PrivateV79v1`. Keep `//@version=5`. Do not use a conversion command or substitute a v6 library. Record saved source, SHA256, complete diagnostics and a screenshot of the version directive and library declaration.
3. Add the library to the chart. Record whether Save and Add succeed, and preserve both internal-private demonstration plots and any runtime errors. Their native values must be measured rather than copied from local engine output.
4. Select the Pine Editor’s **Publish library** command (the publishing button can read “Publish indicator/strategy/library”). Create a new **public, open-source library publication**, title `P425PrivateV79v1`, using the description below. Complete the publication dialog. This is publication version **1**, not an update of an existing different script. If publication is unavailable, or a same-named publication already has different bytes/version, record PUBLICATION-UNAVAILABLE / CONTEXT-UNMET and stop the private-visibility part. Do not replace this prerequisite with another version or silently change its title.
5. Open the resulting published library/version. Save the publication URL, actual `publisher/P425PrivateV79v1/1` import path, visibility, version number, published source and SHA256, Save/publish observations and screenshots. Verify the published source remains Pine v5 and matches the supplied library source. If the platform transforms the text, retain both byte sequences and describe the transformation; changed semantics or a changed version leaves the context unmet.
6. Materialize the six consumer templates using the exact publisher username, e.g. `python3 bind-import-v1.py --publisher ACTUAL_USERNAME --output bound-v1`. This helper changes **only** the one `__PUBLISHER__` token. It neither publishes nor verifies publication. Retain its `BOUND-SOURCES-v1.json`; bind actual executed source hashes separately from template hashes. Consumers import explicit immutable version `/1`; never use an unpinned/latest version.
7. Run the exported-controls source in v5 first, then v6. Record the exact executed bytes, compilation result and four observed plots. A control must successfully resolve that exact publication and run before private-call diagnostics for that importing version receive visibility credit. Import/access/version errors remain CONTEXT-UNMET, including a secondary private-call error behind them.

Publication description: “Minimal Pine v5 library for reproducible member-visibility captures. It provides exported function and method access controls and exported forwarding through one private function and one private method. The demonstration plots record internal private-member use. Consumers test external access independently; this publication contains no market logic or TradingView data requests.”

## Run the six indicators independently

Use fresh indicator drafts in the same authenticated account/context. The two exported-controls programs observe direct exported method/function calls and both internal-private forwarding routes. The private-receiver and private-function programs each contain one disputed call, so a refusal cannot hide another visibility question. Attempt all three roles for each version, without combining or repairing rejected calls.

For every source record Save/compile, Add-to-chart and runtime phases separately, executed source/hash, full error and warning text, caret line:column, and exposed native CE code (absent if unavailable). Capture a screenshot of each refusal. If admitted, export original chart OHLCV plus every named plot for at least 32 confirmed bars, raw CSV/hash, actual settings and confirmed cutoff. Keep open/live rows separate. Library source, publication identity and version must remain unchanged throughout.

Return `v79/captures/v79/RESPONSE-v79.md`, an attempt inventory, publication receipt, bound/executed sources, raw observations, screenshots and CSVs. Include failures of the prerequisite. Per-role/per-version records remain separate. A private receiver refusal does not settle the private ordinary-function namespace call, or vice versa. No branch, engine fix or parity credit is authorized by this request alone.

## Documentation

The [Pine v5 Libraries manual](https://www.tradingview.com/pine-script-docs/v5/concepts/libraries/) distinguishes exported definitions from library-internal definitions and describes explicitly versioned imports. The [publishing guide](https://www.tradingview.com/pine-script-docs/writing/publishing/) documents the editor’s publication flow. These links motivate the experiment; they do not supply its observed native diagnostics.
