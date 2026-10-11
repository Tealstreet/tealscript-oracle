# v60 native capture response v2

All 29 exact assets have native observations. Consumer outcomes: RUNS: 5, COMPILE-ERROR: 22. Library outcomes: RUNS: 2.

Captured through Chrome MCP on the designated mini, account `sours-lat`, using ordinary BINANCE:BTCUSDT candles, 2 minutes, Etc/UTC display and the provider's 24x7 session. All 60 source/instruction SHA256 checks pass. [Audit](audit-v1.json) · [Attempt inventory](attempt-inventory-v2.json) · [Integrity record](environment-v1/integrity-v1.json)

All 5 successful indicator captures include original native CSV bytes with time/OHLC/Volume and every authored plot, preserving duplicate headers, numeric strings and missing cells. Each attempt retains exact executed source/hash, marker owners and warnings, actual setup and inputs, capture/export times, confirmed CSV cutoff, screenshot and snapshot. Open rows remain separate. No realtime behavior is inferred. Native v5 diagnostics often expose no code; missing codes are left unspecified.

## Observed answers

- All four v5 typed/untyped array/map float-to-int reassignment witnesses RUN with VALUE=20. All four v6 witnesses fail at the assignment (7:5), CE10173. No value is inferred for refused v6 sources.
- Unused first UDT receiver indicators fail at 5:13 in both versions; v6 exposes CE10236. The exact unexported-method library sources compile successfully via native Save compiler responses. They were neither added to the chart nor published; no numeric or imported-method credit is assigned to those compile-only admissions.
- Private import: both v5 sources fail at import because a Pine v5 consumer cannot import the pinned v6 library. Private visibility is therefore UNOBSERVED in v5. In v6 the exported forward control RUNS with RESULT=13.5, establishing library access; the private receiver source fails at 4:11 with CE10271. The immutable sours-lat/R2Nsaa411cdaddab/1 publication is reused unchanged.
- Both volume-multiply defaults fail at 4:3; v6 exposes CE10134. All four method UDF-helper-default witnesses fail at 4:29; v6 exposes CE10133. Exact declaration/call source forms remain separate.
- All four direct tuple RHS witnesses fail at the opening bracket, 3:7; v6 exposes CE10156.
- All three v5 legal-literal optional-only overload probes fail at the second declaration, 4:5: overloads have the same required parameters. The declaration-only probe also refuses, so this exact refusal does not depend on choosing omitted versus supplied calls.

## Outstanding scope

No staged v60 source remains unattempted. The v5 private-visibility question remains masked by native import-version incompatibility; no substitute or republished library was used. v61 is not bundled in this oracle repository and was not reconstructed from the ledger-only description.

## Per-source evidence

| Source | Group | Native outcome | Diagnostic or closed raw readout | Evidence |
| --- | --- | --- | --- | --- |
| `v60-array-reassign-v5-untyped-v1.pine` | collection-reassignment | RUNS | CSV column 7 VALUE: 20 | [observation](v60-array-reassign-v5-untyped-v1/attempt-v1/observation-v4.json) |
| `v60-array-reassign-v5-typed-v1.pine` | collection-reassignment | RUNS | CSV column 7 VALUE: 20 | [observation](v60-array-reassign-v5-typed-v1/attempt-v1/observation-v4.json) |
| `v60-array-reassign-v6-untyped-v1.pine` | collection-reassignment | COMPILE-ERROR | CE10173 7:5 Cannot assign a value of the "array<int>" type to the "copied" variable. The variable is declared with the "array<float>" type. | [observation](v60-array-reassign-v6-untyped-v1/attempt-v1/observation-v4.json) |
| `v60-array-reassign-v6-typed-v1.pine` | collection-reassignment | COMPILE-ERROR | CE10173 7:5 Cannot assign a value of the "array<int>" type to the "copied" variable. The variable is declared with the "array<float>" type. | [observation](v60-array-reassign-v6-typed-v1/attempt-v1/observation-v4.json) |
| `v60-map-reassign-v5-untyped-v1.pine` | collection-reassignment | RUNS | CSV column 7 VALUE: 20 | [observation](v60-map-reassign-v5-untyped-v1/attempt-v1/observation-v4.json) |
| `v60-map-reassign-v5-typed-v1.pine` | collection-reassignment | RUNS | CSV column 7 VALUE: 20 | [observation](v60-map-reassign-v5-typed-v1/attempt-v1/observation-v4.json) |
| `v60-map-reassign-v6-untyped-v1.pine` | collection-reassignment | COMPILE-ERROR | CE10173 7:5 Cannot assign a value of the "map<string, int>" type to the "copied" variable. The variable is declared with the "map<string, float>" type. | [observation](v60-map-reassign-v6-untyped-v1/attempt-v1/observation-v4.json) |
| `v60-map-reassign-v6-typed-v1.pine` | collection-reassignment | COMPILE-ERROR | CE10173 7:5 Cannot assign a value of the "map<string, int>" type to the "copied" variable. The variable is declared with the "map<string, float>" type. | [observation](v60-map-reassign-v6-typed-v1/attempt-v1/observation-v4.json) |
| `unused-udt-v5-indicator-v1.pine` | unused-udt-receiver | COMPILE-ERROR | code not exposed 5:13 The 'p' argument is not used. The first method argument should be used. | [observation](unused-udt-v5-indicator-v1/attempt-v1/observation-v4.json) |
| `unused-udt-v5-library-v1.pine` | unused-udt-receiver | RUNS | Compile-only admission; no chart execution/publication | [observation](unused-udt-v5-library-v1/attempt-v1/observation-v4.json) |
| `unused-udt-v6-indicator-v1.pine` | unused-udt-receiver | COMPILE-ERROR | CE10236 5:13 The "p" argument is not used. The first method argument should be used. | [observation](unused-udt-v6-indicator-v1/attempt-v1/observation-v4.json) |
| `unused-udt-v6-library-v1.pine` | unused-udt-receiver | RUNS | Compile-only admission; no chart execution/publication | [observation](unused-udt-v6-library-v1/attempt-v1/observation-v4.json) |
| `private-method-private-receiver-v5-v2.pine` | private-import-visibility | COMPILE-ERROR | code not exposed 3:8 Cannot import the 'lib' library into a script coded in Pine Script™ v5. Convert the script to Pine Script™ v6 to use this library.; code not exposed 4:11 Could not find method or method reference 'pick' for 'float' | [observation](private-method-private-receiver-v5-v2/attempt-v1/observation-v5.json) |
| `private-method-exported-forward-control-v5-v2.pine` | private-import-visibility | COMPILE-ERROR | code not exposed 3:8 Cannot import the 'lib' library into a script coded in Pine Script™ v5. Convert the script to Pine Script™ v6 to use this library. | [observation](private-method-exported-forward-control-v5-v2/attempt-v1/observation-v5.json) |
| `private-method-private-receiver-v6-v2.pine` | private-import-visibility | COMPILE-ERROR | CE10271 4:11 Could not find method or method reference 'float.pick' | [observation](private-method-private-receiver-v6-v2/attempt-v1/observation-v5.json) |
| `private-method-exported-forward-control-v6-v2.pine` | private-import-visibility | RUNS | CSV column 7 RESULT: 13.5 | [observation](private-method-exported-forward-control-v6-v2/attempt-v1/observation-v5.json) |
| `default-boundary-volume-multiply-v5-1x-v1.pine` | default-expression-boundaries | COMPILE-ERROR | code not exposed 4:3 The default value assigned to a parameter must be either a literal value (e.g., `5`) or a built-in variable (e.g., `close`). | [observation](default-boundary-volume-multiply-v5-1x-v1/attempt-v1/observation-v4.json) |
| `default-boundary-volume-multiply-v6-1x-v1.pine` | default-expression-boundaries | COMPILE-ERROR | CE10134 4:3 The default value assigned to a parameter must be either a literal value (e.g., "5") or a built-in variable (e.g., "close"). | [observation](default-boundary-volume-multiply-v6-1x-v1/attempt-v1/observation-v4.json) |
| `method-header-helper-default-function-v5-1x-v1.pine` | default-expression-boundaries | COMPILE-ERROR | code not exposed 4:29 The default value cannot be a function, variable or calculation. | [observation](method-header-helper-default-function-v5-1x-v1/attempt-v1/observation-v4.json) |
| `method-header-helper-default-receiver-v5-1x-v1.pine` | default-expression-boundaries | COMPILE-ERROR | code not exposed 4:29 The default value cannot be a function, variable or calculation. | [observation](method-header-helper-default-receiver-v5-1x-v1/attempt-v1/observation-v4.json) |
| `method-header-helper-default-function-v6-1x-v1.pine` | default-expression-boundaries | COMPILE-ERROR | CE10133 4:29 The default value cannot be a function, variable or calculation. | [observation](method-header-helper-default-function-v6-1x-v1/attempt-v1/observation-v4.json) |
| `method-header-helper-default-receiver-v6-1x-v1.pine` | default-expression-boundaries | COMPILE-ERROR | CE10133 4:29 The default value cannot be a function, variable or calculation. | [observation](method-header-helper-default-receiver-v6-1x-v1/attempt-v1/observation-v4.json) |
| `tuple-rhs-literal-v5-v60-v1.pine` | tuple-rhs-shapes | COMPILE-ERROR | code not exposed 3:7 Syntax error at input '[' | [observation](tuple-rhs-literal-v5-v60-v1/attempt-v1/observation-v4.json) |
| `tuple-rhs-mixed-v5-v60-v1.pine` | tuple-rhs-shapes | COMPILE-ERROR | code not exposed 3:7 Syntax error at input '[' | [observation](tuple-rhs-mixed-v5-v60-v1/attempt-v1/observation-v4.json) |
| `tuple-rhs-literal-v6-v60-v1.pine` | tuple-rhs-shapes | COMPILE-ERROR | CE10156 3:7 Syntax error at input "[" | [observation](tuple-rhs-literal-v6-v60-v1/attempt-v1/observation-v4.json) |
| `tuple-rhs-mixed-v6-v60-v1.pine` | tuple-rhs-shapes | COMPILE-ERROR | CE10156 3:7 Syntax error at input "[" | [observation](tuple-rhs-mixed-v6-v60-v1/attempt-v1/observation-v4.json) |
| `optional-only-overloads-v5-declaration-v60-v1.pine` | optional-only-overloads | COMPILE-ERROR | code not exposed 4:5 The 'read' function has overloads with the same required parameters. The type of required parameters must be different in overloaded versions of functions. | [observation](optional-only-overloads-v5-declaration-v60-v1/attempt-v1/observation-v4.json) |
| `optional-only-overloads-v5-omitted-v60-v1.pine` | optional-only-overloads | COMPILE-ERROR | code not exposed 4:5 The 'read' function has overloads with the same required parameters. The type of required parameters must be different in overloaded versions of functions. | [observation](optional-only-overloads-v5-omitted-v60-v1/attempt-v1/observation-v4.json) |
| `optional-only-overloads-v5-supplied-v60-v1.pine` | optional-only-overloads | COMPILE-ERROR | code not exposed 4:5 The 'read' function has overloads with the same required parameters. The type of required parameters must be different in overloaded versions of functions. | [observation](optional-only-overloads-v5-supplied-v60-v1/attempt-v1/observation-v4.json) |
