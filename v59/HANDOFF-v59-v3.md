# Oracle probe round v59 — staged capture handoff v3

Supersedes HANDOFF-v59-v2.md and bundle-manifest-v2.json. Governing manifest: [bundle-manifest-v3.json](bundle-manifest-v3.json). This staged round contains **64 consumers (54 naturals +10 controls) and2 library prerequisites**, across3 groups. All earlier62 Pine sources remain unchanged. Native expectations are UNSPECIFIED; no commit, push or publication has occurred.

The added imported-method pair needs a real private published library before consumer capture. Sam must follow the [exact publish/import sequence](instructions/local-import-method-collision-publish-import-v1.md), record distinct v5/v6 immutable versions and source hashes, and save the import-only executed-source derivatives. Library refusal is PUBLICATION-BLOCKED, not consumer method refusal. Do not alter method calls or inline the imported implementation. Earlier v59 capture instructions remain in their groups.

Before capture run `sha256sum -c SHA256SUMS`. Run each consumer separately, preserving diagnostics, warnings and raw positional plot columns; collect source hashes, chart setup, timestamps and confirmed cutoff. Return records to captures/v59/RESPONSE-v59.md.

## Groups

- [NS-PARAM-NAMING initial probes](instructions/ns-param-naming-group-instructions-v1.md)
- [NS-PARAM-NAMING namespace-call and ta addendum](instructions/ns-param-naming-namespace-calls-group-instructions-v1.md)
- [Imported/local method collision with publish/import steps](instructions/local-import-method-collision-publish-import-v1.md)

## Consumer checklist

- [ ] [ns-param-naming-udt-renamed-control-v5-v59-v1](ns-param-naming-udt-renamed-control-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-array-parameter-v5-v59-v1](ns-param-naming-udt-array-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-array-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-box-parameter-v5-v59-v1](ns-param-naming-udt-box-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-box-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-line-parameter-v5-v59-v1](ns-param-naming-udt-line-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-line-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-label-parameter-v5-v59-v1](ns-param-naming-udt-label-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-label-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-map-parameter-v5-v59-v1](ns-param-naming-udt-map-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-map-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-matrix-parameter-v5-v59-v1](ns-param-naming-udt-matrix-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-matrix-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-table-parameter-v5-v59-v1](ns-param-naming-udt-table-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-table-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-renamed-control-v5-v59-v1](ns-param-naming-array-parameter-renamed-control-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-array-parameter-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-v5-v59-v1](ns-param-naming-array-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-array-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-renamed-control-v5-v59-v1](ns-param-naming-array-local-renamed-control-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-array-local-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-v5-v59-v1](ns-param-naming-array-local-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-array-local-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-renamed-control-v5-v59-v1](ns-param-naming-box-parameter-renamed-control-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-box-parameter-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-v5-v59-v1](ns-param-naming-box-parameter-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-box-parameter-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-renamed-control-v5-v59-v1](ns-param-naming-box-local-renamed-control-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-box-local-renamed-control-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-v5-v59-v1](ns-param-naming-box-local-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-box-local-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-renamed-control-v6-v59-v1](ns-param-naming-udt-renamed-control-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-array-parameter-v6-v59-v1](ns-param-naming-udt-array-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-array-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-box-parameter-v6-v59-v1](ns-param-naming-udt-box-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-box-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-line-parameter-v6-v59-v1](ns-param-naming-udt-line-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-line-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-label-parameter-v6-v59-v1](ns-param-naming-udt-label-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-label-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-map-parameter-v6-v59-v1](ns-param-naming-udt-map-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-map-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-matrix-parameter-v6-v59-v1](ns-param-naming-udt-matrix-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-matrix-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-udt-table-parameter-v6-v59-v1](ns-param-naming-udt-table-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-udt-table-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-renamed-control-v6-v59-v1](ns-param-naming-array-parameter-renamed-control-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-array-parameter-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-parameter-v6-v59-v1](ns-param-naming-array-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-array-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-renamed-control-v6-v59-v1](ns-param-naming-array-local-renamed-control-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-array-local-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-array-local-v6-v59-v1](ns-param-naming-array-local-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-array-local-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-renamed-control-v6-v59-v1](ns-param-naming-box-parameter-renamed-control-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-box-parameter-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-parameter-v6-v59-v1](ns-param-naming-box-parameter-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-box-parameter-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-renamed-control-v6-v59-v1](ns-param-naming-box-local-renamed-control-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-box-local-renamed-control-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-box-local-v6-v59-v1](ns-param-naming-box-local-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-box-local-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-array-v5-v59-v1](ns-param-naming-namespace-call-array-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-array-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-box-v5-v59-v1](ns-param-naming-namespace-call-box-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-box-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-color-v5-v59-v1](ns-param-naming-namespace-call-color-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-color-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-label-v5-v59-v1](ns-param-naming-namespace-call-label-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-label-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-line-v5-v59-v1](ns-param-naming-namespace-call-line-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-line-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-linefill-v5-v59-v1](ns-param-naming-namespace-call-linefill-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-linefill-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-map-v5-v59-v1](ns-param-naming-namespace-call-map-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-map-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-math-v5-v59-v1](ns-param-naming-namespace-call-math-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-math-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-matrix-v5-v59-v1](ns-param-naming-namespace-call-matrix-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-matrix-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-polyline-v5-v59-v1](ns-param-naming-namespace-call-polyline-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-polyline-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-str-v5-v59-v1](ns-param-naming-namespace-call-str-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-str-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-table-v5-v59-v1](ns-param-naming-namespace-call-table-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-table-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-array-v6-v59-v1](ns-param-naming-namespace-call-array-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-array-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-box-v6-v59-v1](ns-param-naming-namespace-call-box-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-box-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-color-v6-v59-v1](ns-param-naming-namespace-call-color-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-color-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-label-v6-v59-v1](ns-param-naming-namespace-call-label-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-label-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-line-v6-v59-v1](ns-param-naming-namespace-call-line-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-line-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-linefill-v6-v59-v1](ns-param-naming-namespace-call-linefill-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-linefill-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-map-v6-v59-v1](ns-param-naming-namespace-call-map-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-map-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-math-v6-v59-v1](ns-param-naming-namespace-call-math-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-math-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-matrix-v6-v59-v1](ns-param-naming-namespace-call-matrix-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-matrix-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-polyline-v6-v59-v1](ns-param-naming-namespace-call-polyline-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-polyline-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-str-v6-v59-v1](ns-param-naming-namespace-call-str-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-str-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-namespace-call-table-v6-v59-v1](ns-param-naming-namespace-call-table-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-namespace-call-table-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-ta-custom-sma-v5-v59-v1](ns-param-naming-ta-custom-sma-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-ta-custom-sma-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-ta-custom-ema-v5-v59-v1](ns-param-naming-ta-custom-ema-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-ta-custom-ema-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-ta-custom-w0Value-v5-v59-v1](ns-param-naming-ta-custom-w0Value-v5-v59-v1.pine); [instructions](instructions/ns-param-naming-ta-custom-w0Value-v5-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-ta-custom-sma-v6-v59-v1](ns-param-naming-ta-custom-sma-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-ta-custom-sma-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-ta-custom-ema-v6-v59-v1](ns-param-naming-ta-custom-ema-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-ta-custom-ema-v6-v59-v1-instructions-v1.md).
- [ ] [ns-param-naming-ta-custom-w0Value-v6-v59-v1](ns-param-naming-ta-custom-w0Value-v6-v59-v1.pine); [instructions](instructions/ns-param-naming-ta-custom-w0Value-v6-v59-v1-instructions-v1.md).
- [ ] [local-import-collision-v5-v59-v1](local-import-collision-v5-v59-v1.pine); [instructions](instructions/local-import-collision-v5-v59-v1-instructions-v1.md).
- [ ] [local-import-collision-v6-v59-v1](local-import-collision-v6-v59-v1.pine); [instructions](instructions/local-import-collision-v6-v59-v1-instructions-v1.md).

## Library prerequisites

- [ ] [local-import-collision-library-v5-v59-v1](local-import-collision-library-v5-v59-v1.pine); [instructions](instructions/local-import-collision-library-v5-v59-v1-instructions-v1.md).
- [ ] [local-import-collision-library-v6-v59-v1](local-import-collision-library-v6-v59-v1.pine); [instructions](instructions/local-import-collision-library-v6-v59-v1-instructions-v1.md).
