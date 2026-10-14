# Oracle round v90 — authorized throwaway-layout context capture v1

## Authorized method — verbatim

Save as PRIVATE unpublished script, Add to chart, remove studies after; MAY create a new throwaway layout and change symbol/interval/settings on it only; STILL FORBIDDEN: publish, share, any visibility change, any change to EXISTING saved layouts, alerts, library publication/import; anything beyond: STOP as BLOCKED-NEEDS-OWNER-APPROVAL.

Keep `sours-lat/P425PrivateV79v1/1` unchanged: no action. All requested sources are import-free indicators. Do not execute historical publication/import instructions. Only the NEW throwaway layout(s) created for this round may change. If the account cannot create a layout or select an exact requested interval without sign-in, upgrade, subscription/account/global-preference change, STOP BLOCKED-NEEDS-OWNER-APPROVAL; do not substitute a symbol or interval. Do not delete layouts or private scripts; remove only studies added for the request. Preserve existing saved layouts, scripts, study/input settings and visibility. Record initial and post-attempt existing-layout identity; no layout IDs are inferred from URL parameters.

Use native UI capture/export only; no Bar Replay, injected browser code, direct compiler/provider API, synthetic ticks, source repair or fabricated values. Capture status and complete compiler response, immediate and settled editor markers separately, preserving their observed order, text, severity, line/column and exposed codes. A missing channel is UNOBSERVED, never an empty list. Keep every failed/partial attempt.

All native status, values and marker order are UNSPECIFIED. Save exact executed Pine bytes and SHA256, private script/study identity, actual symbol/interval/timezone/session/feed status, UTC observation times, source hash and original CSV column ordinals. Export original bytes with all headers, numeric strings and empty cells; preserve original screenshots and compiler/editor artifacts. Do not round values or replace blanks. Report native rejection as an observation, not permission to repair.

Closed scoring: provide a per-row mask and reason, keyed to original CSV SHA256 and row ordinal; exclude physical-open/developing rows. For request data additionally require the requested day closed at every relevant observation. Do not treat a chart-confirmed row as proof that its requested daily bar is closed. Preserve excluded rows in raw exports. Pair by exact timestamp/source/context, never row position alone. If provider values drift between captures, retain and attribute each difference; do not choose a convenient attempt, average, clamp or silently waive a column.

Return `v90/captures/v90/RESPONSE-v90-v1.md`, `attempt-inventory-v1.json`, and per-probe/attempt directories containing executed-v1.pine, observation-v1.json, raw native CSV(s), raw markers/compiler responses/screenshots, row-closure-mask-v1.csv and column-bindings-v1.json. Hash every consumed file. Derived tables must identify source CSV hash/row/column and stay separate from raw evidence. State every account action and whether any prerequisite was unavailable.
## Request groups

|Request ID|Sources / attempts|Required new-layout context|Covers|
|---|---:|---|---|
|v90-dxy-live|2 /2|TVC:DXY2m UTC, physically live|v81 natural/renamed INITIAL+two updates+CLOSE input frames|
|v90-daily-context|4 /8|BTCUSDT1D then BTCUSDT2m UTC|blockedv88; fresh daily provider inputs relevant to context1/2|
|v90-cum-prefix|4 /8|BTCUSDT2m UTC, full calculation frontier|context7/8, exact original plus prefix companion|
|v90-footprint-presence|2 /4|BTCUSDT2m UTC, actual footprint availability|context21, exact original plus native summary fields|

Read each `instructions/<request-id>-v1.md` before that group. May reuse a throwaway layout created for THIS round after completing the prior group; no changes to old layouts. Run `sha256sum -c SHA256SUMS` from v90/. The manifest binds all source/instruction hashes; reused sources are byte-identical, not rewritten. Capture the groups independently: a DXY-market/entitlement block must not hide the daily/prefix results. No study/source should remain attached after its capture.

Read HOLD-MAP-v1.json for limits. This request does not recreate past timenow schedules or developing-daily snapshots, permit library imports, or assign stable order to unstable marker channels. No engine change or parity closure is asserted by design/publication. Daily provider companions are not inlined replacements for the imported nested originals. Raw prior observations remain untouched.
