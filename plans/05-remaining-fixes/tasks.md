# Tasks: Release fixes integration

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

## Task index

| ID / outcome | Route | Depends on | Progress |
|---|---|---|---|
| [SF-INVENTORY](#sf-inventory) — disposition ledger | N / Luna | Promoted Plan 02 integration and Plan 04 heads | Not started |
| [M-00](#m-00) — map planning IDs to existing runner/card rows | Not stated in source; decide at setup | SF-INVENTORY; immutable donor diffs and named source contracts | Not started |
| [SF-RANK2](#sf-rank2) — host-cancel fix | X / Terra + Luna | SF-INVENTORY; Plan 02 integration and Plan 04 behavior and receipts | Not started |
| [SF-RANK9](#sf-rank9) — VibeComfy boundary test | N / Luna | SF-INVENTORY; Plan 02 integration | Not started |
| [SF-GENERATION-EXTRAS](#sf-generation-extras) — installed boundary, IDs, SDK fixtures | X / Terra + Luna | SF-INVENTORY; Plan 02 integration | Not started |
| [SF-CAS](#sf-cas) — Runtime CAS composition | S / Sol + Luna | Post-CE Runtime; SF-INVENTORY | Not started |
| [SF-RUNTIME-FOLD](#sf-runtime-fold) — Runtime fold composition | S / Sol + Luna | Post-CE Runtime; SF-CAS; SF-INVENTORY | Not started |
| [SF-RUNPOD-OWNER](#sf-runpod-owner) — CPU-testable owner/custody behavior | S / Sol + Luna | Plan 02 integration/K27; SF-INVENTORY | Not started |
| [SF-AGENT-FOLD](#sf-agent-fold) — record Plan 06 ownership | S / Sol + Luna (Plan 06 PK-6) | Plan 06 PK-6 | Fold transferred to Plan 06 PK-6 |
| [SF-H3-PARKED](#sf-h3-parked) — preserve exclusions | N / Luna | Source ledger | Not started |
| [SF-ALREADY-COVERED](#sf-already-covered) — retain source proof and check inclusion | N / Luna | Source ledger; relevant Plan 02 integration and Plan 04 heads | Not started |
| [SF-COMPOSE](#sf-compose) — final producer-to-consumer composition | X / Terra + Luna | Selected independent rows; actual S invariants | Not started |
| [SF-PROMOTE](#sf-promote) — publish exact reviewed heads | N / Luna | SF-COMPOSE review | Not started |

Route labels and model bindings follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md#routing-and-bindings). Progress is recorded here; the queue alone owns project status.

## Task details

### SF-INVENTORY

- **Outcome:** Map each accepted ledger item to one inclusion, equivalence, or deferment record against actual Plan 02 integration and Plan 04 `pre-main` heads.
- **Route:** N / Luna.
- **Dependencies and inputs:** Exact promoted Plan 02 integration and Plan 04 heads; accepted receipts and donor ledger in [inputs.md](inputs.md).
- **Work:** Compare donor changes and current behavior; do not implement changes already covered.
- **Focused checks:** Record exact SHA and changed-behavior or patch-equivalence evidence. Ancestry alone does not prove a later revert preserved behavior.
- **Done:** Every member has one evidenced disposition and any replacement/fold mapping is explicit.

### M-00

- **Outcome:** Map these planning IDs into the existing runner/card rows.
- **Route:** The source document gives no route; set it at task setup using the shared routing table.
- **Dependencies and inputs:** SF-INVENTORY; immutable donor diffs and named source contracts.
- **Work:** Derive exact `FILES` and test-node lists from those inputs. This is bounded source selection, not open-ended discovery.
- **Focused checks:** No wildcard selectors or broad suites. Preserve the existing named check boundaries below.
- **Done:** Existing runner/card rows refer to the correct planning IDs and exact files/nodes; no new assignment is inferred here.

### SF-RANK2

- **Outcome:** Integrate host-cancel behavior only if absent, preserving current execution receipts.
- **Route:** X / Terra + Luna; very hard only for cancellation/receipt interaction, not routine containment.
- **Dependencies and inputs:** SF-INVENTORY; donor `aff7686d0f6e6314dd5531600d173bbd265e437e` in [inputs.md](inputs.md).
- **Work:** Reconcile the host-cancel change with Plan 02 integration and Plan 04 without disturbing current receipts.
- **Focused checks:** `tests/core/execution/test_cancellation_rereview.py`; add named affected nodes only if conflict resolution changes another boundary.
- **Done:** The behavior is included or evidenced equivalent, with receipt behavior preserved.

### SF-RANK9

- **Outcome:** Add the independent VibeComfy boundary test only if absent after Plan 02 integration.
- **Route:** N / Luna.
- **Dependencies and inputs:** SF-INVENTORY; donor `1ac3b91fedf4a15842ff655442869569d4855396` in [inputs.md](inputs.md).
- **Work:** Preserve the test-only boundary improvement without a product rewrite.
- **Focused checks:** Exact changed nodes in `tests/test_porting_emitter.py`; no broad emitter sweep.
- **Done:** Included or evidenced equivalent on the selected candidate.

### SF-GENERATION-EXTRAS

- **Outcome:** Reconcile installed-boundary, canonical-ID, and SDK-fixture changes with Plan 02 integration once.
- **Route:** X / Terra + Luna for installed-boundary/ID/routing conflict resolution; SF-INVENTORY handles mechanical unchanged inclusion.
- **Dependencies and inputs:** SF-INVENTORY; donors `9c06b674dfe27d513eccc528e14fb423cf3a1881`, `7ab6aa10859b19bc3b13cf90966cc0da18026c68`, and `9d6af90b1ae4bd4a7afd346942c07e57f75201c7` in [inputs.md](inputs.md).
- **Work:** Reconcile with Plan 02 integration once; do not replay whole files merely to count changes.
- **Focused checks:** Freeze exact affected nodes from the donor diff within `tests/test_installed_wheel_smoke.py`, `tests/test_installer_wheel.py`, `tests/core/generation/test_entries.py`, `test_listing.py`, and `tests/sdk/test_generation_target.py`.
- **Done:** Selected behavior is included or evidenced equivalent, with the node list tied to the immutable donor diff.

### SF-CAS

- **Outcome:** Compose Runtime CAS/publication/restore behavior on post-CE Runtime; it remains a separate lane and is not automatically a generation dependency.
- **Route:** S / Sol + Luna.
- **Dependencies and inputs:** Post-CE Runtime; donor `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373` and existing RI-R checks in [inputs.md](inputs.md).
- **Work:** Preserve current stop, editing-lease, and unknown-outcome behavior. Do not substitute custody `103f97803f7f391e2c810ebdf086f798326cd75a`.
- **Focused checks:** Select the existing RI-R named CAS/publication/restore checks for this donor's transaction invariants and affected consumer calls.
- **Done:** Commit/fence/restore composition is covered; coupled invariants are the reason for the S route.

### SF-RUNTIME-FOLD

- **Outcome:** Compose the Runtime fold with SF-CAS on post-CE Runtime if it is not already equivalent.
- **Route:** S / Sol + Luna.
- **Dependencies and inputs:** Post-CE Runtime; SF-CAS; donor `287042b2426f7465a1fba77bba075766f18f26b1` in [inputs.md](inputs.md).
- **Work:** Treat this as a later increment; do not reopen a completed CE phase.
- **Focused checks:** Exact fold-changed cancellation-fence and commit/restore tests from its seven-file delta; affected Agent/Runtime tuple checks and canonical consumer locks.
- **Done:** Fold behavior is composed or evidenced equivalent with tuple and lock checks; no unrelated checks are added.

### SF-RUNPOD-OWNER

- **Outcome:** Preserve or integrate CPU-testable owner/custody behavior after Plan 02 integration/K27, without unrelated ancestry.
- **Route:** S / Sol + Luna.
- **Dependencies and inputs:** Plan 02 integration/K27; donor `aee88cb87c4acd249023d16f096bce5f40c1b6f9` in [inputs.md](inputs.md).
- **Work:** Use fakes only; no provider or GPU work. If a live-provider outcome cannot be proved, retain that explicit limitation rather than deferring all CPU implementation.
- **Focused checks:** `tests/packs/runpod/test_preparation_rollback.py`, `tests/sdk/test_runpod_product_owner.py`, and exact affected target/placement nodes.
- **Done:** CPU behavior is included or evidenced equivalent; any live-provider claim remains explicitly unproved.

### SF-AGENT-FOLD

- **Outcome:** Keep the Agent fold's completion record here; Plan 06 PK-6 owns execution exactly once.
- **Route:** S / Sol + Luna in Plan 06 PK-6.
- **Dependencies and inputs:** Plan 06 PK-6; donor `47d67d8d13bcbf4ab437bc41ae6ec5b6cf60598b` in [inputs.md](inputs.md).
- **Work:** Do not merge both the fold and its superseded members.
- **Focused checks:** Plan 06 must record whole-fold inclusion or documented behavior/byte-equivalent final result. Its 46-file production ancestry is not tests-only.
- **Done:** Recorded as fold transferred to Plan 06 PK-6, which closes it; this plan does not wait for it.

### SF-H3-PARKED

- **Outcome:** Preserve the exclusion of deferred H3 production scope from this CPU initiative.
- **Route:** N / Luna.
- **Dependencies and inputs:** Exact source SHAs `d88a1c69e45fb5d2e729e449d4b2c1b8062b6956` and `ed985e81bbdf8e5b0535cf10ce28e1196ab56145` in [inputs.md](inputs.md).
- **Work:** Record the existing parked reason; do not dispatch an S worker merely to record parked work.
- **Focused checks:** No GPU/model readiness claim.
- **Done:** Both sources and their exclusion are preserved in the disposition record.

### SF-ALREADY-COVERED

- **Outcome:** Retain the source-published case-matrix packet and its original remote/evidence proof; check relevant pre-main inclusion independently.
- **Route:** N / Luna.
- **Dependencies and inputs:** Source head `c7073ff98a2b456ee1aca065d2d473962271d94e` and superseded-member records in [inputs.md](inputs.md).
- **Work:** Link the exact source head and test evidence; do not reimplement. Source publication does not prove pre-main inclusion and does not require a product merge of the packet.
- **Focused checks:** Verify relevant pre-main inclusion only as part of the inventory; no extra product check is specified.
- **Done:** Source proof is retained and inclusion is separately evidenced or explicitly deferred.

### SF-COMPOSE

- **Outcome:** Coordinate final producer-to-consumer composition once after selected independent rows.
- **Route:** X / Terra + Luna; Sol resolves only the actual S invariants above.
- **Dependencies and inputs:** Selected independent rows; actual S invariants; canonical locks/pins.
- **Work:** Resolve combined behavior once and scope an independent Astra review.
- **Focused checks:** Rerun exact checks affected by combined changes, including CE boundaries only when changed. No broad suites.
- **Done:** Canonical locks/pins and affected checks agree with the composed tuple; scoped review is recorded.

### SF-PROMOTE

- **Outcome:** Promote only exact reviewed candidate heads.
- **Route:** N / Luna, after SF-COMPOSE review.
- **Dependencies and inputs:** Fresh immutable candidates and then-current target identities per changed repository; remote receipts.
- **Work:** Follow existing no-force publication rules; do not create empty changes for already-covered repositories.
- **Focused checks:** Confirm exact reviewed `pre-main` heads and remote receipt.
- **Done:** Each selected candidate is promoted under existing publication authority; no unreviewed or empty repository publication.
