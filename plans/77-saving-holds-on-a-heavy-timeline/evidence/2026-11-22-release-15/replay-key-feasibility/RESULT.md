# Plan 77 feasibility of storing successful replay keys

The deterministic replay can be separated from the current-state checks. The existing verifier and its in-process key cannot be persisted as-is. A safe startup cache would reuse only the separated replay result. Runtime would still check structural and live facts on every start, bind the cache to the effective verifier and schemas, and run a complete replay on a miss. The read-and-hash work scales with stored bytes. At about 1,000 comparable edges the measured raw-throughput proxy is about 22 s, and a parse-and-canonicalize implementation could spend about four minutes on the same JSON slice alone. Keep startup operation and progress first. The sidecar merits a small measured design only if this retained linear cost fits the startup target.

## One accepted record

Runtime source was `77c38d037f98f744bd8f41c15d95429c124a8003`. `TimelineCommitStore._verify_accepted_replay` passes a request, prepared record, source and base closures, continuation bindings and inverse history to the deterministic authoring validators. Its sequential wrapper currently makes SQL reads. It can be separated into read-and-confirm and pure validation. The current key is checked after the in-memory traversal has built inputs, tied them to a live snapshot and rechecked custody. It has no persisted verifier-version binding. [Exact source dependency map](runtime-dependencies.md)

| Input or check | Required boundary |
| --- | --- |
| Complete ledger receipt and history edge | Key exact stored result, records and private capture metadata and the typed row fields. Bind realm, project, timeline, publication and ordinal. Include command, merge mode, publisher, request hash, original and landing heads, provider/compiler, recorder ABI and result. Keep one matching receipt, sequence bounds, lineage, head count and missing rows checked. |
| Source, base and accepted documents | Key exact verified closure inputs, including parent, shot and internal revisions, manifests, selected bindings and their typed identities. Independently establish presence, canonical closure, dependency graph, precise prior and accepted head, and actual required CAS and retained input bytes. IDs or stored digest strings alone cannot stand in for verified bytes. |
| Sequential capture, event chain and undo or materialization ancestry | The pure part reads captured context, prepared document, each original and landing command boundary, effect and dependency, prior binding continuations, and inverse source history. The wrapper also reads the current project realm and exact semantic event rows. Validate these outside the cache or feed their verified content into the key. Recompute the event and receipt prefix from actual rows. Use an ordered rolling prefix and separately checked dependency digests. Do not reread or hash a whole prefix for every record. Keep ancestry, cycle and reservation checks on actual state. |
| Verifier and authorization | Namespace success by the effective verifier implementation, contract and schema/resolver identity, plus key format. Historical provider and compiler version fields do not identify today's verifier. Keep owner custody, realm and active scope, current request authorization, storage checks and physical fences outside reuse. The deterministic validation kernel operates on resolved values. No wall clock participates in the inspected kernel. |

Current source still checks retained input content via live table joins and verifies closure and object custody before a replay can hit. Stage timing for those reads and validations is open. In particular, a content-key hit cannot suppress missing dependencies, an actual bad CAS object, or present-day authorization failure. Whole-document and sequential capture JSON are stored in SQLite history metadata, receipts and revision rows. Those bytes are not CAS references that the current clean marker can exempt from the timeline integrity walk.

## Exact stored-byte observation

The immutable, sidecar-free signed 300-clip archive retained its exact SHA before and after the read. Its 32 ordered history edges and selected receipt, revision, event and input rows contributed 427.2 MB. This diagnostic used SQLite reads and length-framed SHA-256, with a warm filesystem cache and no semantic replay or actual CAS storage reads.

| Read-only diagnostic | Time |
| --- | ---: |
| One actual archived fixture pass, approximately 30 edges | 0.867 s |
| Repeated same-byte passes equivalent to 992 edges, approximately 13.24 GB | 21.743 s |
| One 32-edge JSON parse, canonical encoding and hash slice, 423.5 MB | 7.669 s |
| Grouped ancestry, receipt uniqueness, active-head and event hash/link sample | 0.011 s |
| SQLite quick and foreign-key checks on that archive | 0.087 s and 0.005 s |

At the observed byte mix a real 1,000-edge walk would touch about 13.35 GB. Linear estimates from these observations are roughly 22–27 s warm for raw read/hash, or 240 s for the measured canonical JSON slice if it ran at the same per-edge rate. Repeating the same data gives a throughput proxy. A distinct signed 1,000-edge archive, cold I/O, memory pressure, full closure/CAS work and complete startup are unmeasured. The grouped sample is cheap. The current per-history receipt lookup shows a table scan and took 0.214 s for the simple 32-edge ancestry and receipt check. Grouping/counting once matters at depth. The samples do not establish that all uncached work is cheap. [Read/hash receipt](read-hash-cost.json) · [Structure and canonical JSON receipt](canonical-and-structure-cost.json)

## Review and decision

A digest names inputs. It does not prove a success entry was issued by the verifier. A malformed, missing, stale-version or unverifiable sidecar must give more verification. The Lead's accepted directory-writer threat scope must be explicit or the success entries need an independently protected authenticity boundary. Keep it outside SQL, tie it to the right verifier and scope, and prove Release 14 start and doctor tolerate the result. Doctor ignores all persisted successes and keeps the complete checks. A crash-truncated or stale proof can lose a hit. It may never make an unverified key hit.

The independent reviewer must start with unchanged in-owner corruption and real restart/undo tests. Change each input separately, including equal-shaped rewrites, event facts, slot bindings, retained object bytes at the same identity, lookup absence, schema dependency and verifier behavior. Each case must miss or be refused by an uncached gate. Hold bytes fixed and bump verifier semantics to invalidate the entire namespace. Check crash, partial sidecar, substitution, cross-realm and older Runtime compatibility separately. A true unchanged hit may skip only the separated replay. Measure all raw and remaining check stages against an actual fixture at depth before qualifying anything.
