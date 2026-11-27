# One process identity for Agent and Runtime

> **Current R16 authority, 27 November 2026:** The existing [recovery board #2050](https://github.com/banodoco/astrid-dev/issues/2050) and subsequent Lead rulings govern actual sessions, bases, writer reservations, proof venues and review budgets. The earlier CPU-only queue and provisional run-start conditions below are historical where they conflict. Installed/native outcome and the single release acceptance remain open; this planning correction creates no dispatch, replacement author or extra review round. See the [final programme review](../../releases/16/evidence/final-programme-review.md).

**Project:** One process identity for Agent and Runtime

**Goal:** A Runtime-managed host-only pack host starts and runs a task on macOS, Linux and Windows: process identity, peer custody and signalling live once in `runtime_protocol`, the source closure has one definition with golden vectors, every duplicate is deleted, a one-implementation test in each repository stops new copies, and every test in the area is green on all three OSes.

**Status:** active

**Owner:** Existing R16 Manager38 and technical owner on [board #2050](https://github.com/banodoco/astrid-dev/issues/2050); no reassignment

**Estimate:** 8–14 engineering days remaining implementation, plus 2–3 independent review, 1–2 integration and 3–5 native qualification days; conditional on the existing Lead settling an executable supervisor/continuation contract. New external capability and venue waits are unbounded here.

**Waiting on:** Existing producer/consumer and single lock joins on board #2050; the bounded R15 supervisor/continuation ruling and genuine three-platform proof. R12 publication and the old int/38 branch cut are satisfied historical prerequisites, not new gates.

**Start:** [Astrid contributor skill](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/start.md) and [domain map](https://github.com/banodoco/astrid-dev/blob/257a80bab15f753f1164994ca024efd01a4205e0/agent/shared/domains.md). Project metadata here feeds the generated [catalog](../../plans/index.md).

**Vision gaps:** [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

## Outcome and scope

A Runtime-managed host-only pack host (the local worker started with `--host-control-fd`) starts and runs a task on macOS, Linux and Windows. Today it can't start on any of them, because the Agent and the Runtime each carry their own copy of process identity, peer custody and source-closure measurement, and the copies have drifted ([inputs](inputs.md#planning-evidence)).

This plan gives each of those pieces exactly one home and deletes every other copy in the same change:

| Piece | One home | Deleted copies |
|---|---|---|
| Process identity and birth id | `runtime_protocol.platform.process_identity` and `process_birth_matches` (already the Runtime's one implementation) | Agent `ps-lstart` and `bootid:ticks` encoders and their translators |
| Peer custody and signalling (peer token, own token, token details, signal, one-shot resume, census) | `runtime_protocol.process_binding`, the one per-OS provider, with Darwin, Linux and Windows backends inside `runtime_protocol` | Darwin primitives in both custody brokers; the Agent's Darwin-only `_peer_token` |
| Source-closure definition | one Runtime-owned data file, `runtime_protocol/schemas/host-source-closure-v1.json`, with golden vectors, vendored to the Agent through `runtime.lock.json` | both hand-written component lists |
| Boot-manifest hash | the Agent's `astrid/core/_shared/boot_manifest.py` (already the only producer) | none in product code; the test's raw-file hash is fixed in release 12 |
| Role-custody designation ABI (phase 2) | `runtime_protocol/role_custody.py` | the shared classes copied between the two brokers on 20 Oct |

**Guard against recurrence:** a one-implementation test in each repository fails when a process-identity, peer-credential, signalling or closure primitive appears outside its home. The golden vectors and a three-OS host-spawn CI job back it up.

**All green:** every test in this area passes on macOS, Linux and Windows, with no xfail and no manual lane. That covers the installed-pack custody-spawn test with its xfail removed, the built-in-pack host-spawn test, the golden vectors, the four Linux boundary tests, and the other tests in the [inventory](tasks.md#test-inventory).

**Failure messages** on the host start path name the gate that refused (peer, birth, boot manifest, closure) and what differed.

**Not changed:**
- the custody file formats and designation versions;
- the wire protocol;
- the App;
- VibeComfy's own tick-only session registry. The Agent's adapter keeps translating to it, through the provider.

**Not building:**
- a new shared package or repository;
- a release-time conformance job (see [Interfaces](#interfaces-and-handoff));
- Linux custody without pidfd (a sandbox fallback), which belongs to [Plan 15](../15-openshell-safe-execution/plan.md).

## Existing work and decision

`runtime_protocol` is already shared: the Agent host imports it, and the host's verified import mapping and installed-origin probe already require it beside `astrid/`. The Runtime's Linux custody (1 Nov) and Windows identity code already live there. So the shortest path makes `runtime_protocol.process_binding`, which already calls itself "the one place", the real provider. The Agent then deletes its copies.

The closure has a different shape. Its two measurers must stay separate: the verifier never imports the host, and the host checks its closure before importing any Runtime code. So the single home is the definition: one data file plus vectors, which both measurers read and are tested against. The alternatives, the import constraints and the evidence are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Continue the existing [P38 recovery programme](https://github.com/banodoco/astrid-dev/issues/2050) through its exact provider review, Agent reader/closure adoption, single `runtime.lock.json` join, guards, installed host-spawn and common-role ABI. Preserve original IDs and all-green area/three-platform obligations. The old phase-one publication is an internal checkpoint; both retained phases converge into one R16 release through P31.

Credit the landed Runtime closure and authored Linux/Darwin/Windows providers, closure and birth readers and `38-08U` deferred/cold work. Source drafts and individual native producer tests do not establish integrated installed acceptance. `38-07` retains the exclusive lock/vendor join. Existing authors keep their functions; no second updater or provider is commissioned.

The [27 November contract follow-up](https://github.com/banodoco/astrid-dev/issues/2050#issuecomment-7225981241) distinguishes retained owner authority from a stronger frozen-supervisor-policy assumption. The Lead settles that precise trust boundary, then proves either authenticated supervisor delegation or a reachable quiescent R15 continuation using the existing transaction. A manual-only R15 exception requires an explicit product decision; permanent refusal does not satisfy the promised update. Keep native cold rollback, old service-start, Update-now and local-page consumption in the affected owners' proof. No PID/journal authority fallback and no unproved policy guarantee.

Use the current `release/16/plan-38` branches and current review/proof contracts. The historical `int/38` table remains an acceptance ledger, not dispatch instructions. Preserve product-specific role extensions, wire framing, retained native handles and independent pre-import measurement; the common ABI is not a general broker rewrite.

## Interfaces and handoff

- **Consumes:**
  - the exact accepted R16 Runtime/Agent provider pair and actual served-origin compatibility;
  - the Agent's `runtime.lock.json` and `scripts/vendor_lock.py`, which vendor Runtime artifacts by SHA;
  - the Runtime's `tests/astrid-agent.pin`.
- **Produces:**
  - the provider API in `runtime_protocol.process_binding`;
  - `host-source-closure-v1.json` and its vectors;
  - the one-implementation tests;
  - the `host-spawn` CI job.
- **Cross-repo landing follows [Plan 31](../31-releases-from-astrid-dev/plan.md)'s model of a release**, with no second mechanism:
  - the Runtime change merges first;
  - the Agent pins it in `runtime.lock.json`, `source_commit` and the vendored files, via `vendor_lock.py update`;
  - the Runtime's test pin names that Agent;
  - the release record carries both SHAs. Plan 31's `release-contract` already checks that the record's `runtime` equals the Agent's lock.
- **No new pin, lock or release-time job.** The Runtime's three hand-kept Agent test pins collapse into `tests/astrid-agent.pin`. Whether that pin later comes from the release record is Plan 31's call.
- **Overlap:** [Plan 13](../13-execution-host-refactor/plan.md) splits `generic_host.py`; A1 changes only its birth comparison and peer calls. Coordinate the merge order if both are active.

## Completion

The proof is these observable results:

- **End to end, on each OS.** On `ubuntu-latest`, `macos-latest` and `windows-latest`, in the `host-spawn` job, `POST /v1/control/local-worker/start` returns 200, and a task on a granted pack reaches `succeeded`:
  - for the built-in packs;
  - for an installed pack, where an ungranted pack is refused by name.

  No xfail, skip or manual lane remains on those tests.
- **One proof per bug:**
  - the Agent's peer token works on Linux and Windows (A1);
  - the Agent's and the Runtime's birth ids for the same process are equal on each OS (A1);
  - both closure measurers produce each vector's digest, including the installed-pair tree (P2r, A3);
  - the boot hash in the test comes from the Agent's API (E1).
- **Every test in the [inventory](tasks.md#test-inventory)** passes in a blocking job on each OS where it applies.
- **The guards hold.** Each repository's one-implementation test passes. It fails on a planted second copy (negative case).
- **No copies left.** `git grep` shows no copy from the [inventory](inputs.md#duplicate-inventory) left outside its home.

Limits:
- Backend-specific tests run on their own OS (decision D4).
- Windows host-only start may need more than the provider; E1 shows whether it does (D6).
- Upgrade-time journals with the old Agent birth format fail closed (D3).


## Historical Release 16 scope proposal (25 November 2026)

This is a proposed scoping amendment from [SYN-01](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md); scope, execution and publication remain subject to the existing independent reviews and owner decisions. Existing task progress, accepted decisions and historical evidence remain unchanged. Where historical sequencing differs, the following describes the proposed R16 task-level sequencing; it does not change existing delivery authority.

retain one identity/custody/closure and minimal common role ABI; change two-publication sequence into one R16 shipment with an internal phase-one checkpoint. State that duplication removal must preserve product-specific role extensions, wire framing, native retained handles and independent pre-import verification; it is not a generalized broker rewrite.
