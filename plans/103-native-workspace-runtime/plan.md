# A native authoritative workspace runtime

**Project:** A native authoritative workspace runtime

**Goal:** A creator's workspace can operate headlessly and preserve, edit and recover work through a native Rust runtime even without Python, Node, an agent or the editor.

**Status:** queued

**Owner:** Unassigned

**Estimate:** TBD

**Waiting on:** Plan 100 conformance and ownership boundary, Plan 102 kernel/commit contract, Plan 101 native controller for distribution; independent scope/release and data migration approval.

**Start:** [Astrid agent start document](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [LS-006 — Independent creative foundation](../../vision/gaps/LS-006-independent-creative-foundation.md) (primary) · [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting) · [Safe user control](../../vision/gaps/F-002-safe-user-control.md) (supporting) · [Creative execution](../../vision/gaps/F-003-creative-execution.md) (supporting)

**Contributes to closure:** LS-006: E4: headless authoritative core and safe data migration.

## Outcome and scope

**Draft proposal — owner agreed the direction on 26 November 2026, but detailed project scope, independent challenge and release placement are pending. No implementation authorized.**

Implement the existing authoritative workspace Runtime in modular Rust crates: typed contracts/auth, durable project/resource store (SQLite and CAS), event/receipt ledger, task admission/leases/fencing/cancel/retry, media transfer/verification, worker coordination, permissions/credential grants, backup/restore and crash recovery. Native timeline kernel from Plan 102 is integrated by the single commit coordinator. Keep deterministic core separate from provider-specific behavior. Prefer explicit types and bounded transactions, no giant service/store translation or new language-specific extension requirement.

Run the Rust candidate and Python reference in separate roots behind the same contract; no concurrent writers to a live realm, no shadow writes with external effects. Preserve public errors, idempotency and canonical digests; build implementation-independent differential tests using Plan 100. Retain data format where sound; if migration is necessary, explicit versioned verified backup, preflight, copy/validate and atomic owner switch with rollback eligibility. Preserve projects, media, credentials, history, external references and receipts; no silent downgrade, no destructive repair. Native OS custody and permissions remain as strong as current qualified behavior. Integrate with Plan 101 controller and same local/hosted clients; Python/Node become managed optional capability environments rather than a core dependency.

Out: rewriting ComfyUI, provider model loops, React, renderer, every pack, arbitrary historical unsupported migrations, multi-master sync or replacing the existing cloud product. A new core without qualified cutover is not project completion.

## Existing work and decision

Runtime inventory ~103 Python implementation files/~3.98 MB and ~400 test files; service.py and store.py are large. The public workspace contract, SQLite/CAS ownership, upgrade logic, native process custody and current tests are valuable reference, not a structural template. Plan 35 state, Plan 36 credentials, Plan 38 process identity, Plans 39/91 green tests, Plan 50 recorded boundaries and Plan 62 manifest eliminate relevant duplication. See [architecture](../100-language-independent-foundation/architecture.md). See [inputs](inputs.md#planning-evidence) for alternatives, review limits and outstanding owner decisions. This is not an authorization to alter accepted existing projects.

## Sequence and readiness

After reference and interface review, build read-only project/CAS and contract smoke in isolated roots, then durable mutation, task lifecycle, auth/custody and timeline integration with incremental parity. Stage migration/adoption against copies; rehearse interruption and rollback before release qualification. Cut over only after independent full integrated parity and explicit owner approval. Remove obsolete Python daemon ownership paths when qualified; retain client/support Python modules as needed. The [task outline](tasks.md) is not a dispatch packet. Re-estimate after the first bounded evidence slice; do not assign to a release or start product work without a recorded run decision.

## Interfaces and handoff

Consumes Plan 100 versioned conformance suite and ABI, Plan 102 pinned kernel, current SQLite/CAS and backup formats, Plan 101 controller manifest/custody, accepted identity/state/credential contracts. Produces native Runtime executable(s), versioned crates, contract-compatible endpoints/clients, migration/recovery receipts and three-OS qualification with exact source/artifact IDs. Plans 104/105 consume this core. Release and data cutover are distinct owner decisions.

## Completion

- Native core starts with no Python/Node or UI; independent clients open/create/edit/reopen a project, read media, admit/cancel/settle a fixture task and inspect durable receipts. Unsupported creative capability is explicitly reported, not silently faked.
- Run reference vs candidate conformance and negative fixtures at exact revisions (auth, concurrent writes, leases, retries, stale identity, backup restore, malformed/oversized input, digest mismatch, filesystem custody, interrupted writes). No weakened reference expectations.
- Qualify migration on realistic copies including large media/custom elements/history/credentials and active-task refusal. Verify same project identities and content hashes; crash at each cutover boundary, recovery and rollback eligibility; old/new cannot both own the realm.
- Installed Windows/Linux/macOS matrix, supported local UI/hosted/CLI and agent/worker flows; compare measured performance and memory against accepted baseline. No unsupported GPU or cloud guarantee.
- Independent review of security, storage durability, migration and parity; explicit owner cutover approval and release integration evidence. Retire duplicate authoritative daemon paths only after proof.

Scope completion is contribution to LS-006, not automatic gap closure; qualify the integrated release separately and record limits.
