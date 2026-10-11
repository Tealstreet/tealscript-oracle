# Oracle probe round v61 — capture handoff v1

Two separate groups, 11 active sources: 6 indicator consumers, 4 dependent compile-only libraries and 1 v5 publication prerequisite. Two original v5 dependent sources are preserved as excluded provenance (13 Pine assets total). No v61 captures or native predictions are bundled. Every exact-source native outcome remains UNSPECIFIED until observed.

Run `sha256sum -c SHA256SUMS` from v61. The [bundle manifest](bundle-manifest-v1.json) identifies active sources, hashes, roles, excluded sources and per-source instructions. Return `v61/captures/v61/RESPONSE-v61.md` with an attempt inventory and integrity hashes. Record source identity, all compiler/Save responses, phase, exact message/code/site, screenshots, actual settings and outcome per attempt. An unavailable prerequisite is CONTEXT-UNMET, not semantic refusal. Engine results never substitute for native observations.

## Version-compatible private visibility

The [v60 response](../v60/captures/v60/RESPONSE-v60.md) showed that v5 private visibility was masked by import-version incompatibility: a v5 consumer cannot import the pinned v6 library. Those attempts do not settle private visibility. v6 exported forwarding ran and private receiver access refused in an indicator; v61 asks the distinct dependent-library compilation question.

For v6, reuse the immutable `sours-lat/R2Nsaa411cdaddab/1` publication exactly. Its [published v58 source](../v58/captures/v58/prerequisites/root2-library-aa411cdaddab-v58-v1/publication-v1/published-source-v1.pine) SHA is `d6afd2cab8dae06301bcef249685bcff2b3d986c144deda2c13e99094759fa45`. Do not update or substitute that publication.

For v5, compile and publish the bundled `private-transitive-base-v5-v61-v1.pine` as a dedicated v5 library. Only version/title differ from that v58 source; private `pick` and exported `forward` bodies are unchanged. Preserve exact source, source SHA, Pine version and actual immutable owner/title/version. Then bind BOTH v5-v2 dependent templates to it: replace only `CAPTURE_OWNER/PrivateTransitBase5v61/1` with the actual published path. Preserve executed source, hash and import-only diff. These templates must import a v5-published library. Never convert them to v6 or inline helper bodies. If v5 publication/access is impossible, record the exact blocker and leave v5 visibility UNOBSERVED/CONTEXT-UNMET.

The two original `private-transitive-v5-*-v1.pine` files remain byte-exact provenance and are EXCLUDED from capture; running them against the v6 publication would repeat the masking error. The [original producer packet](instructions/private-PROBE-REQUEST-v3.json) and [producer instructions](instructions/private-producer-INSTRUCTIONS-v1.md) are preserved; this handoff supersedes only their v5 binding instruction. Their historical absolute paths are provenance, not downloadable dependencies.

Compile the version-matched control library first, then the private witness independently. Preserve compile admission separately from publication and execution. Do not publish invalid libraries. If an admitted dependent library can be published, record its immutable publication and execute a separate indicator importing it as `b` and plotting `b.read(3.5)`; retain exact indicator source/hash and original native CSV. No numerical prediction is required. An import/access/version blocker settles neither method visibility question.

## Direct tuple RHS group

The six identifier/string/bool v5/v6 probes and their instructions are copied byte-for-byte from be9795's [producer packet](instructions/tuple-PROBE-REQUEST-v1.json). This is a separate group from transitive private visibility and from v60 numeric/call RHS witnesses. Paste each unchanged. Record admission or refusal with all compiler markers and screenshot; do not infer a general tuple rule from earlier shapes. For admitted indicators, export time/OHLC/Volume and all plots on BINANCE:BTCUSDT, 2m, Etc/UTC after 32 closed bars. Preserve exact numeric strings, missing cells, duplicate headers, actual chart settings and confirmed cutoff. No live-state claim is requested.

## Source checklist

### transitive-private-visibility

- [private-transitive-base-v5-v61-v1.pine](private-transitive-base-v5-v61-v1.pine) — [library-prerequisite instructions](instructions/private-transitive-base-v5-v61-v1-instructions-v1.md); Can the exact v5 prerequisite be compiled and published for version-compatible dependent library probes?

- [private-transitive-v5-control-v2.pine](private-transitive-v5-control-v2.pine) — [library-compile-only instructions](instructions/private-transitive-v5-control-v2-instructions-v1.md); Exported forwarding control through the immutable library

- [private-transitive-v5-private-v2.pine](private-transitive-v5-private-v2.pine) — [library-compile-only instructions](instructions/private-transitive-v5-private-v2-instructions-v1.md); Private external receiver access in a dependent library: exact phase and diagnostic

- [private-transitive-v6-control-v1.pine](private-transitive-v6-control-v1.pine) — [library-compile-only instructions](instructions/private-transitive-v6-control-v1-instructions-v1.md); Exported forwarding control through the immutable library

- [private-transitive-v6-private-v1.pine](private-transitive-v6-private-v1.pine) — [library-compile-only instructions](instructions/private-transitive-v6-private-v1-instructions-v1.md); Private external receiver access in a dependent library: exact phase and diagnostic



### tuple-rhs-shapes

- [tuple-rhs-booleans-v5-v61-v1.pine](tuple-rhs-booleans-v5-v61-v1.pine) — [consumer instructions](instructions/tuple-rhs-booleans-v5-v61-v1-instructions-v1.md); Does Pine v5 admit or refuse a direct tuple RHS of booleans, and at what exact site/diagnostic?

- [tuple-rhs-booleans-v6-v61-v1.pine](tuple-rhs-booleans-v6-v61-v1.pine) — [consumer instructions](instructions/tuple-rhs-booleans-v6-v61-v1-instructions-v1.md); Does Pine v6 admit or refuse a direct tuple RHS of booleans, and at what exact site/diagnostic?

- [tuple-rhs-identifiers-v5-v61-v1.pine](tuple-rhs-identifiers-v5-v61-v1.pine) — [consumer instructions](instructions/tuple-rhs-identifiers-v5-v61-v1-instructions-v1.md); Does Pine v5 admit or refuse a direct tuple RHS of identifiers, and at what exact site/diagnostic?

- [tuple-rhs-identifiers-v6-v61-v1.pine](tuple-rhs-identifiers-v6-v61-v1.pine) — [consumer instructions](instructions/tuple-rhs-identifiers-v6-v61-v1-instructions-v1.md); Does Pine v6 admit or refuse a direct tuple RHS of identifiers, and at what exact site/diagnostic?

- [tuple-rhs-strings-v5-v61-v1.pine](tuple-rhs-strings-v5-v61-v1.pine) — [consumer instructions](instructions/tuple-rhs-strings-v5-v61-v1-instructions-v1.md); Does Pine v5 admit or refuse a direct tuple RHS of strings, and at what exact site/diagnostic?

- [tuple-rhs-strings-v6-v61-v1.pine](tuple-rhs-strings-v6-v61-v1.pine) — [consumer instructions](instructions/tuple-rhs-strings-v6-v61-v1-instructions-v1.md); Does Pine v6 admit or refuse a direct tuple RHS of strings, and at what exact site/diagnostic?
