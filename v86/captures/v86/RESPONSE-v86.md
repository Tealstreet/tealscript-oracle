# Oracle v86 response v1

**UNRESOLVED ordering stability.** All three native private Save/Add attempts report **COMPILE-ERROR**. Their complete settled editor lists have identical ordered semantic tuples: **41 errors followed by four warnings**, 45 markers each. Attempts 1 and 2 lost their immediate samples during local evidence collection; attempts 2 and 3 also use HTTP 304 full-compiler responses after unchanged native Save. These observations do not certify three complete fresh Save/Add orders.

The exact source is 155567 bytes, SHA-256 `55cccc9a7b55364a6bd129d4dd7fddd8949c3fc6b467cff708a58bbe966d9961`, byte-identical to the historical v9 source. Attribution, licensing comments, title, whitespace and EOF bytes remain intact. No source repair, runtime export or engine change occurred.

| Attempt | Outcome | Full compiler channel | Immediate editor | Settled markers | Warning positions (1-based) | Ordered semantic-list SHA-256 | Observed settled equality |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| [1](v86-mixed-error-order-1x-v1/attempt-v1/observation-v1.json) | COMPILE-ERROR | Complete Save/new 23020 HTTP 200 and translate 23084 HTTP 200 | UNOBSERVED | 45 | 42–45 | `9a23c5f75d1dca8e442882bd1d5bebdaa746bcb15430fc9e2552efbbaa89d066` | Same tuple list |
| [2](v86-mixed-error-order-1x-v1/attempt-v2/observation-v1.json) | COMPILE-ERROR | Complete translate 23154 HTTP 304; no-op Save | UNOBSERVED | 45 | 42–45 | `9a23c5f75d1dca8e442882bd1d5bebdaa746bcb15430fc9e2552efbbaa89d066` | Same tuple list |
| [3](v86-mixed-error-order-1x-v1/attempt-v3/observation-v1.json) | COMPILE-ERROR | Complete translate 23219 HTTP 304; no-op Save | Complete, separately timestamped | 45 | 42–45 | `9a23c5f75d1dca8e442882bd1d5bebdaa746bcb15430fc9e2552efbbaa89d066` | Same tuple list |

## Separate compiler and editor observations

All four full compiler bodies report `success:false` and expose **14 `reason2.errors` entries followed by an empty `reason2.warnings` array**. The errors' original template messages, exposed codes, context substitutions and sites are preserved exactly. The ordered full error arrays agree across all four responses, independently of editor comparisons. This full-compiler channel stops at the first missing function at line 1724 and does not expose the editor's complete 41-error/four-warning list; no missing entries were reconstructed.

Each attempt also has a complete, exact-source background `translate_light` POST response: request 23006, 23106 or 23172, all HTTP 200. These expose **41 errors and four warnings** in separate `result.errors` and `result.warnings` arrays. Those raw arrays agree across the three source-matched background responses. Their `success:true` describes the analysis response, not native compilation acceptance. The initial request 23000 analyzes the native new-draft template, not the requested source; its raw body is retained as incidental setup evidence and receives no source-matched credit.

The editor's error order interleaves diagnostic categories by ascending source site: undeclared identifiers at lines 1255–1411, missing functions at 1724–2125, undeclared identifiers at 2206–2509, then the missing function at 2515. All errors precede the four consistency warnings, whose sites are lines 129, 134, 943 and 943. No version advisory occurs in this v6 editor list. Raw compiler arrays, immediate samples when observed, and settled arrays remain independent channels in [compiler/editor comparison](compiler-editor-comparison-v1.json).

The comparison tuple is severity, exact message, start line/column and exposed code value. Code-link targets, end sites, owner/resource and original indices remain in the raw arrays. There are no identical duplicate UI tuples to collapse in these lists. Reopening changes the resource URI; that difference remains visible in the raw arrays. Equality of the sampled semantic lists is an observation, not fresh-repetition stability credit.

## Native actions, collection limits and restoration

Attempt 1 created PRIVATE unpublished script `USER;42d15eb57bfe4936a52d85c752492c5a`, version `1.0`. Attempts 2 and 3 reopened that round-created script, verified its saved CRLF text against the original LF bytes, pasted the exact original buffer, invoked native Save and Add, then removed only the newly added study. Every executed source file, source-matched POST and settled source buffer matches the requested bytes. The raw reopened text is retained separately.

Attempts 1 and 2 completed native Save/Add and produced the captured refusals, but local stdout truncation interrupted collection before their immediate arrays and action timestamps were persisted. Those fields are explicitly null/UNOBSERVED. Complete native request/response bodies and later settled arrays were recovered through **Chrome MCP's native file outputs**, read in bounded chunks. No direct compiler API or alternate browser protocol was used. Attempt 3 retained all immediate and settled samples. No missing timestamp or array was invented.

All three request-added error studies were removed. Each restored chart context and the round's final context match the initial symbol, interval, timezone, style, main-series properties, original studies/inputs and other study properties. No Publish, Share, visibility change, new layout, saved-layout setting change, alert, library publication or IMPORT occurred. The one private unpublished Save remains on the account; no script was deleted.

[Attempt inventory](attempt-inventory-v1.json) binds source identity, response identity/cache state, timestamps, marker counts and evidence paths. [Audit](audit-v1.json) passes with the two disclosed incomplete immediate channels. All four request `SHA256SUMS` entries pass; [integrity inventory](integrity-v1.json) records artifact hashes and byte counts, excluding itself. No ordering rule, expected-value generation, runtime credit or engine change is requested or claimed.
