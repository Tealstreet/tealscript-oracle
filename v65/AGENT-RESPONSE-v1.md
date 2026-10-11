# v65 agent response v1

Evidence inventory: [attempt-inventory-v1.json](captures/v65/attempt-inventory-v1.json), SHA256 `abb08c50d8bc79bdd7f6fa0b1a020a9e610bb6cc30b0a575f735f542e0d1be4e`. Reconciled after batch 54 `63e15382af5994da428386e978ee53d266aa74fa` and batch 55 `d2add4a0f33b85807a190ec982114649170fe332` were pushed to pine-parity-integration-v4. Snapshot: CONSUMED 2.

CONSUMED means a verified root is in those pushed commits and its listed fixture entries are byte-authenticated. PENDING means branch evidence only, with no pushed integration credit. UNMET records masked/excluded evidence rather than native negative authority.

Typed optional-only method refusal and untyped optional-only function admission/value control are consumed as distinct witnesses, not one generic overload ban.

| Asset | State / root owner | Pushed batch commit | Native outcome / scope | Fixture entries |
| --- | --- | --- | --- | --- |
| `v61-v5-optional-only-typed-method-declaration-g6-v1` | CONSUMED / g6qooy / v5-optional-overload | 54 / `63e15382af5994da428386e978ee53d266aa74fa` | COMPILE-ERROR; Closed-row/compile scope only; see verified root receipt | `v65/captures/v65/v61-v5-optional-only-typed-method-declaration-g6-v1/attempt-v1/observation-v3.json` (SHA256 `a3e06009d5985ec8f2207694dd0d4d8e44cd721adb38f6f8c2e624ef637be6e2`) |
| `v61-v5-optional-only-untyped-function-declaration-g6-v1` | CONSUMED / g6qooy / v5-optional-overload | 54 / `63e15382af5994da428386e978ee53d266aa74fa` | RUNS; Closed-row/compile scope only; see verified root receipt | `v65/captures/v65/v61-v5-optional-only-untyped-function-declaration-g6-v1/attempt-v1/native-v1.csv` (SHA256 `03666770b2cecc57c02c342681870061a0fc74a01db3e36e4b214ca84c48f343`)<br>`v65/captures/v65/v61-v5-optional-only-untyped-function-declaration-g6-v1/attempt-v1/observation-v3.json` (SHA256 `6d00c96fba7444a56ee5d1368103bb0ef3f8d65f6172434a0cab44c16edfc939`) |

## Receipt authority v1

- v5-optional-overload: root `7f804f3245993a0e4bd0bdcf7557a4699e48a86f`; verification `/home/sam/cs/docs/tealscript-parity-archive/ledger/v59v60-v5-optional-overload-g6qooy-v1/VERIFY-DELTA-be9795-v1.md` (SHA256 `9499668ef0e3e289a59e5e11c7e910b083c0a3beef09c5e792043ad2cf66176a`); freeze `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch54-v2/FREEZE-v1.json`; push `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch54-v2/PUSH-v1.json`.

## Pending extensions and unmet requests v1

Batch 56 extensions remain pending: naming, tuple v4 (`c98bcb0554`, v70), unused-UDT v4 (`ed5a5220`, v71), and custom-ta v5 (`6d179e8c`, v72). Their later evidence does not change this v59–v69 pushed-consumption snapshot.

Unmet requests: DXY live initial-open missing-volume/two updates/close; nested-6 exact confirmed requested-daily context; v5 footprint availability (no successful, accessible v5 footprint observation in these consumed receipts); v5 direct private-receiver visibility masked by the incompatible import. V61 compatible dependent-library and v67 namespace visibility are separately consumed and do not erase that direct-receiver gap. None receives inferred parity credit.

No realtime, visual-only, open-row or library-publication numeric credit. Fixture metadata belongs to packages/tealscript/oracle-fixtures.json at the listed batch/root commit; paths above are oracle-relative.
