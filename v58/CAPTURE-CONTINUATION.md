# v58 capture continuation

Resume native TradingView recording in this repository on `master`. Capture requests, artifacts and agent responses now belong to `Tealstreet/tealscript-oracle`; do not put new captures into `tealstreet-next` or advance the application's fixture pin automatically. No application dependencies or engine changes are needed.

At the handoff, no v58 attempts or results have been recorded. The request contains 18 groups, 422 consumers and 27 library prerequisites. All native outcomes remain unspecified. Previous rounds' results are summarized in `../CAPTURE-RESPONSE.md`; they are not v58 evidence. On later resumes, read the committed v58 response and attempt inventory before continuing so completed captures are not repeated.

## Start here

1. Read `../CLAUDE.md`, `HANDOFF-v58-v1.md` and `bundle-manifest-v1.json`. The round handoff and literal per-source instruction files own the capture contract; preserve their source bytes and defaults.
2. Check source integrity from this directory with `shasum -a 256 -c SHA256SUMS` on macOS, or `sha256sum -c SHA256SUMS` where available. The inventory has 918 checksum entries, including its 449 Pine assets.
3. Use only Chrome MCP for authorized browser work, on the designated capture machine. Verify its connection and TradingView session before attempts. A tooling or login failure is an environment blocker, not a Pine result. Do not substitute CUA, raw browser protocols or another local browser.
4. Start imported-method acquisition with the cross-group single-float pair in group-18's capture priority, following `instructions/group-18-capture-v1.md` and the paired per-source instructions. Library publication requires the authorization described in the round handoff. Preserve exact library bytes, actual immutable owner/title/version and both consumers' binding to the same publication. If the prerequisite cannot be acquired, record `PUBLICATION-BLOCKED`; do not rewrite helpers or infer consumer admission.
5. Continue with the group plans and individual instructions. Default context is ordinary BINANCE:BTCUSDT candles with UTC chart display; source-specific instructions take precedence. Groups 3 and 5 need physical-window/live context; absent context stays `CONTEXT-UNMET`.

## Record and return

Write the response to `captures/v58/RESPONSE-v58.md` relative to this directory, with separate per-attempt evidence directories. Retain exact executed source, template/executed hashes, import-only diffs where required, setup, inputs, symbol/provider identity, timeframe/session/timezone, capture timestamp and closed-bar cutoff.

Record `RUNS`, `COMPILE-ERROR`, `RUNTIME-ERROR`, `PUBLICATION-BLOCKED` or `CONTEXT-UNMET`. Preserve complete diagnostic text/code/location/bar, including compilation errors. A successful compile alone is not a numeric or live-state observation. Save original CSV bytes, duplicate headers, numeric strings and missing cells; keep separately timed and live attempts distinct. Include screenshots and logs required by each instruction.

Commit and push capture evidence and agent responses to this repository's `master` at coherent batch boundaries. Never rewrite history or repair an exact source to make it compile. The receiving implementation agent reviews observations and promotes selected regression inputs through an immutable application fixture pin separately.
