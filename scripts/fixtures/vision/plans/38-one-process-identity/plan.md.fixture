# One process identity for Agent and Runtime

**Project:** One process identity for Agent and Runtime

**Goal:** A Runtime-managed host-only pack host starts and runs a task on macOS, Linux and Windows: process identity, peer custody and signalling live once in `runtime_protocol`, the source closure has one definition with golden vectors, every duplicate is deleted, a one-implementation test in each repository stops new copies, and every test in the area is green on all three OSes.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 10–13: phase 1 7–9, phase 2 3–4

**Waiting on:** release 12 published, then Plan 20's Agent `main` group landed (owner's order, 9 Nov)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

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

Start after release 12 is published to `main` (owner, 9 Nov 2026). Release 12 carries the two fixture fixes, the harness fix and a strict, declared xfail on the custody-spawn test that links here.

**Phase 1: host-only start works on all three OSes.**
1. **T0** re-inventories the area tests at the published release-12 heads. **W0** adds the Runtime worker setup script that the proofs need.
2. **P1** builds the provider in the Runtime. **P2r** sets the closure definition there, in parallel.
3. **RS1** review stop on the provider.
4. **A1–A3** move the Agent onto the provider and the shared closure definition, deleting its copies. **L1** fixes the Linux boundary lane, and **F1** fixes the rest of the inventory.
5. **G1** and **G2** add the guards. **E1** adds the three-OS host-spawn job and removes the xfail.
6. **T1** words the failure messages. Then the review (**R**) and publication (**Pub**).

**Phase 2: one role-custody core.**
- **C1** and **C2**: the designation ABI classes move into `runtime_protocol`, and both brokers keep only their own extensions.
- **R2** review, then publication with the next release.

Work lands by PR on `int/38-one-process-identity` in the Runtime and the Agent, cut from each `main` after release 12. Only the Release skill moves either branch to `main`. Recording this plan does not authorize implementation. Details, the critical path and proof are in [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:**
  - release 12's Agent and Runtime `main` heads;
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
