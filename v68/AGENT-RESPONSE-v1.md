# v68 agent response v1

Evidence inventory: [attempt-inventory-v1.json](captures/v68/attempt-inventory-v1.json), SHA256 `79808064f1c7c5e818b6305533fcdf17bf24663450ba93312bec740d0a3fae8d`. Reconciled after batch 54 `63e15382af5994da428386e978ee53d266aa74fa` and batch 55 `d2add4a0f33b85807a190ec982114649170fe332` were pushed to pine-parity-integration-v4. Snapshot: CONSUMED 4.

CONSUMED means a verified root is in those pushed commits and its listed fixture entries are byte-authenticated. PENDING means branch evidence only, with no pushed integration credit. UNMET records masked/excluded evidence rather than native negative authority.

Unused-receiver indicator refusals and used-receiver controls are consumed. Pine v4 unused-UDT is a separate batch-56 pending extension.

| Asset | State / root owner | Pushed batch commit | Native outcome / scope | Fixture entries |
| --- | --- | --- | --- | --- |
| `unused-udt-receiver-only-v5-control-v1` | CONSUMED / vmp8l6 / unused-UDT | 55 / `d2add4a0f33b85807a190ec982114649170fe332` | RUNS; Closed-row/compile scope only; see verified root receipt | `v68/captures/v68/unused-udt-receiver-only-v5-control-v1/attempt-v1/executed-v1.pine` (SHA256 `42afeb382a78f6011fd562367a20eacaf9ab6a722a9e8bb3644f8f4dfb8bc689`)<br>`v68/captures/v68/unused-udt-receiver-only-v5-control-v1/attempt-v1/native-v1.csv` (SHA256 `190dc8820f2e6692c93316ca9a27da34c45b5b406942cba2fc8b9ea49daca580`)<br>`v68/captures/v68/unused-udt-receiver-only-v5-control-v1/attempt-v1/observation-v3.json` (SHA256 `c600d6319e782753f9c3f32d42095f6732bff0415aca5965eeee88aeaf763a9a`) |
| `unused-udt-receiver-only-v5-natural-v1` | CONSUMED / vmp8l6 / unused-UDT | 55 / `d2add4a0f33b85807a190ec982114649170fe332` | COMPILE-ERROR; Closed-row/compile scope only; see verified root receipt | `v68/captures/v68/unused-udt-receiver-only-v5-natural-v1/attempt-v1/executed-v1.pine` (SHA256 `b155aa7a6b3e7e87f59f915023746b286c61a12099440897fde09642e7b24e1d`)<br>`v68/captures/v68/unused-udt-receiver-only-v5-natural-v1/attempt-v1/observation-v3.json` (SHA256 `06ca3e0381c7fece4fb6b495c46c23e78692d8905b456c014702f5faf2884dac`) |
| `unused-udt-receiver-only-v6-control-v1` | CONSUMED / vmp8l6 / unused-UDT | 55 / `d2add4a0f33b85807a190ec982114649170fe332` | RUNS; Closed-row/compile scope only; see verified root receipt | `v68/captures/v68/unused-udt-receiver-only-v6-control-v1/attempt-v1/executed-v1.pine` (SHA256 `18386d44613d34d1cf5b4234b536319187ec29662bdfb30980a0676fa99a9813`)<br>`v68/captures/v68/unused-udt-receiver-only-v6-control-v1/attempt-v1/native-v1.csv` (SHA256 `945079a72441d27914ae94f75b633ecb3b57d432a35aa9abf996034dab51e857`)<br>`v68/captures/v68/unused-udt-receiver-only-v6-control-v1/attempt-v1/observation-v3.json` (SHA256 `e57df3c6c462eded5e173f755fbb10b2c93e088f39b912389734fa8f4e83e68e`) |
| `unused-udt-receiver-only-v6-natural-v1` | CONSUMED / vmp8l6 / unused-UDT | 55 / `d2add4a0f33b85807a190ec982114649170fe332` | COMPILE-ERROR; Closed-row/compile scope only; see verified root receipt | `v68/captures/v68/unused-udt-receiver-only-v6-natural-v1/attempt-v1/executed-v1.pine` (SHA256 `60174829689c0f1a854f190b5d1778eacb84d740c1e84798bc54722e071b5e1f`)<br>`v68/captures/v68/unused-udt-receiver-only-v6-natural-v1/attempt-v1/observation-v3.json` (SHA256 `f4df8763efe88647caa587a34c84c207a33f1e24f0dd53747baa8b4d60d9745a`) |

## Receipt authority v1

- unused-UDT: root `dfc907f54d229da4fd473be7cb130ac70ff00133`; verification `/home/sam/cs/docs/tealscript-parity-archive/ledger/v59v60-unused-udt-receiver-vmp8l6-v1/VERIFY-DELTA-jjs8ff-v2.md` (SHA256 `72fc8c308b5ee49b626714d79e377e84e4353f38cffdff67d9f8b179a012b7be`); freeze `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch55-v3/FREEZE-v1.json`; push `/home/sam/cs/docs/tealscript-parity-archive/ledger/restart-20261006/integration-batch55-v3/PUSH-v1.json`.

## Pending extensions and unmet requests v1

Batch 56 extensions remain pending: naming, tuple v4 (`c98bcb0554`, v70), unused-UDT v4 (`ed5a5220`, v71), and custom-ta v5 (`6d179e8c`, v72). Their later evidence does not change this v59–v69 pushed-consumption snapshot.

Unmet requests: DXY live initial-open missing-volume/two updates/close; nested-6 exact confirmed requested-daily context; v5 footprint availability (no successful, accessible v5 footprint observation in these consumed receipts); v5 direct private-receiver visibility masked by the incompatible import. V61 compatible dependent-library and v67 namespace visibility are separately consumed and do not erase that direct-receiver gap. None receives inferred parity credit.

No realtime, visual-only, open-row or library-publication numeric credit. Fixture metadata belongs to packages/tealscript/oracle-fixtures.json at the listed batch/root commit; paths above are oracle-relative.
