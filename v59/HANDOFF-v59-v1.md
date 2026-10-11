# Oracle probe round v59 — staged capture handoff v1

Staged only; no push or publication. This first group contains 22 NS-PARAM-NAMING naturals plus 10 renamed controls across Pine v5/v6. Native admission, errors and plot values are UNSPECIFIED. v58 already shipped, so no v58 files are changed. Before capture, verify `sha256sum -c SHA256SUMS` from this directory.

Read [group instructions](instructions/ns-param-naming-group-instructions-v1.md) and the per-source instructions. Run each program separately, preserving exact bytes and full compile/runtime diagnostics; export raw RESULT values for at least three confirmed bars when it runs. Record setup/inputs, source hashes, timestamps and confirmed cutoff. The 7 UDT names and 4 collection/scope combinations remain separate questions in each version. A renamed control cannot confer natural admission. Return records to `captures/v59/RESPONSE-v59.md` with source/CSV/screenshots under per-probe directories.

## Probe checklist

- [ ] [ns-param-naming-udt-renamed-control-v5-v59-v1](ns-param-naming-udt-renamed-control-v5-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-udt-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-array-parameter-v5-v59-v1](ns-param-naming-udt-array-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-array-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-box-parameter-v5-v59-v1](ns-param-naming-udt-box-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-box-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-line-parameter-v5-v59-v1](ns-param-naming-udt-line-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-line-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-label-parameter-v5-v59-v1](ns-param-naming-udt-label-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-label-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-map-parameter-v5-v59-v1](ns-param-naming-udt-map-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-map-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-matrix-parameter-v5-v59-v1](ns-param-naming-udt-matrix-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-matrix-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-table-parameter-v5-v59-v1](ns-param-naming-udt-table-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-table-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-renamed-control-v5-v59-v1](ns-param-naming-array-parameter-renamed-control-v5-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-array-parameter-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-v5-v59-v1](ns-param-naming-array-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-array-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-renamed-control-v5-v59-v1](ns-param-naming-array-local-renamed-control-v5-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-array-local-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-v5-v59-v1](ns-param-naming-array-local-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-array-local-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-renamed-control-v5-v59-v1](ns-param-naming-box-parameter-renamed-control-v5-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-box-parameter-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-v5-v59-v1](ns-param-naming-box-parameter-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-box-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-renamed-control-v5-v59-v1](ns-param-naming-box-local-renamed-control-v5-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-box-local-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-v5-v59-v1](ns-param-naming-box-local-v5-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-box-local-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-renamed-control-v6-v59-v1](ns-param-naming-udt-renamed-control-v6-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-udt-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-array-parameter-v6-v59-v1](ns-param-naming-udt-array-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-array-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-box-parameter-v6-v59-v1](ns-param-naming-udt-box-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-box-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-line-parameter-v6-v59-v1](ns-param-naming-udt-line-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-line-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-label-parameter-v6-v59-v1](ns-param-naming-udt-label-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-label-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-map-parameter-v6-v59-v1](ns-param-naming-udt-map-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-map-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-matrix-parameter-v6-v59-v1](ns-param-naming-udt-matrix-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-matrix-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-table-parameter-v6-v59-v1](ns-param-naming-udt-table-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-udt-table-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-renamed-control-v6-v59-v1](ns-param-naming-array-parameter-renamed-control-v6-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-array-parameter-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-v6-v59-v1](ns-param-naming-array-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-array-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-renamed-control-v6-v59-v1](ns-param-naming-array-local-renamed-control-v6-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-array-local-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-v6-v59-v1](ns-param-naming-array-local-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-array-local-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-renamed-control-v6-v59-v1](ns-param-naming-box-parameter-renamed-control-v6-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-box-parameter-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-v6-v59-v1](ns-param-naming-box-parameter-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-box-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-renamed-control-v6-v59-v1](ns-param-naming-box-local-renamed-control-v6-v59-v1.pine) — renamed-control; [instructions](instructions/ns-param-naming-box-local-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-v6-v59-v1](ns-param-naming-box-local-v6-v59-v1.pine) — natural; [instructions](instructions/ns-param-naming-box-local-v6-v59-v1-instructions-v1.md).
