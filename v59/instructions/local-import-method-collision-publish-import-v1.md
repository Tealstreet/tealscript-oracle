# Local/imported same-name method collision — publish/import procedure v1

Question: does a compatible imported bool-receiver own() method remain callable beside an incompatible local float-receiver own() method? v5 and v6 are separate capture attempts. These are two consumers and two exact library-version prerequisites, not a local/imported precedence certificate. Native admission/values/errors are UNSPECIFIED.

## Sam's publication and import sequence

1. Open TradingView's Pine Editor under the account that will run the probes. Create a new library script and paste **local-import-collision-library-v5-v59-v1.pine** exactly, preserving library("Minimal") and export method own(bool self). Save this dedicated test script. Compile/add it to the chart. If refused, save its full diagnostic and mark the v5 consumer PUBLICATION-BLOCKED; do not rewrite the export.
2. In the Pine Editor, choose **Publish… / Publish Script** to create a new library publication. Keep title **Minimal** and enter description **Private test library exporting own(bool), used to capture coexistence with a local own(float) method.** Select **Continue**, choose **Private** privacy and **Open** visibility (libraries are open-source), then **Publish**. Record the publication URL, actual TradingView username, import name and immutable version, plus the exact published source and its SHA256. The stored QA/Minimal/1 is a fixture, not an existing publication claim. Do not overwrite an unrelated existing library; if this exact title cannot be acquired, record the blocker before any separately authorized title adaptation.
3. Open **local-import-collision-v5-v59-v1.pine** as a personal indicator. Replace only the three-component path QA/Minimal/1 on its import line with the actual username/Minimal/V5_VERSION selected from the editor's library autocomplete; keep `as lib` and every other byte. Do not assume the version is1. Save/export the executed source, its SHA256 and the import-only diff. Record which published library source hash/version was bound.
4. Compile/add the v5 consumer independently. Capture admission/refusal, all diagnostics and their locations, then runtime status and raw CSV if it runs. Both plots are unnamed: preserve their ordinal positions and duplicate headers. Never change the calls to lib.own(...), remove the local float method, or paste the imported bool method into the consumer to force success.
5. Return to the same dedicated library script and paste **local-import-collision-library-v6-v59-v1.pine** exactly. Compile it. Choose **Publish…**, then **Update existing script**; select that dedicated **Minimal** publication. Enter release note **Exact Pine v6 test-library source; v5 capture remains pinned to its earlier version.** Review the source difference (only the version directive changes), select **Continue**, then **Publish new version**. Record the newly assigned immutable V6_VERSION and published source/hash; retain the earlier V5_VERSION and its source/hash. A library refusal leaves the corresponding consumer PUBLICATION-BLOCKED.
6. Open **local-import-collision-v6-v59-v1.pine** separately. Change only QA/Minimal/1 to the actual username/Minimal/V6_VERSION. Keep all other bytes, including the local method, implicit receiver calls and `as lib`. Save/hash the executed source and import-only diff. Compile/capture it independently; do not silently bind the v6 consumer to the v5 source or overwrite the v5 result.
7. For each consumer use standard BINANCE:BTCUSDT candles, 2-minute timeframe, UTC display, at least8 confirmed rows. Export time/OHLC and both plot columns; keep original cells. Record actual setup, capture time, closed cutoff, warnings and runtime errors/bar where exposed. Capture true/false close>open rows when physically present; do not fabricate inputs. Return records to captures/v59/RESPONSE-v59.md with library publication records and separate consumer executed sources.

Import templates after the explicitly recorded binding (angle-bracket fields below are not runnable until filled):

```pine
import <ACTUAL_USERNAME>/Minimal/<V5_VERSION> as lib
import <ACTUAL_USERNAME>/Minimal/<V6_VERSION> as lib
```

Each line belongs only in its matching consumer. These are not two imports to add to one script. Prerequisite acquisition, import binding and method dispatch outcomes remain separate. The all-local original strings in the producer request are provenance only, not additional staged probes or native value predictions.

Authority for the publishing workflow: a library must be published before import; private libraries work in personal scripts, and import identities require an explicit version that increments on updates. The Pine Editor exposes Publish Script and a library publication dialog. [TradingView Libraries](https://www.tradingview.com/pine-script-docs/concepts/libraries/#publishing-a-library), [Using a library](https://www.tradingview.com/pine-script-docs/concepts/libraries/#using-a-library), [Publication settings and updates](https://www.tradingview.com/pine-script-docs/writing/publishing/#script-updates).

## Exact-source assets

- [v5 library](../local-import-collision-library-v5-v59-v1.pine)
- [v5 consumer](../local-import-collision-v5-v59-v1.pine)
- [v6 library](../local-import-collision-library-v6-v59-v1.pine)
- [v6 consumer](../local-import-collision-v6-v59-v1.pine)
