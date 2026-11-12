# Recorded boundaries and an offline generation harness

**Project:** Recorded boundaries and an offline generation harness

**Goal:** A generation failure at any boundary (RunPod, the Runtime, the engine) is found and named on a CPU without renting a GPU, because every boundary is tested against recorded real responses and an offline end-to-end harness injects each failure and checks the product's answer.

**Status:** queued

**Owner:** Unassigned

**Estimate:** Phase 1 about 6–8; phase 2 TBD

**Waiting on:** the owner's scope decision (D1); Release 13's in-flight terminal-reconcile and Runtime inline-proof fixes, which phase 1 builds its fault rows on

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each, then run `python3 scripts/astrid_dev.py sync`. Its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): generation on a rented GPU must fail with a named cause, not a silent hang, before it can be relied on. [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting): failures that leave a task stuck or a machine billing are operational-lifecycle failures.

## Outcome and scope

A contributor changing the generation path can run one CPU command and see, for every boundary the path crosses and every failure we know of, whether the product still ends in a defined state and says why. Concretely:

1. **Recorded responses are the only boundary test data.**
   - Provider (RunPod REST and GraphQL), Runtime protocol (task read model, claim, settle, fail, cancel, and their rejections) and engine CLI (JSON lines, failed-command output) shapes come from recordings captured during paid runs we already make, scrubbed by a fixed type-preserving allowlist.
   - A replaying fake refuses any request it has no recording for.
   - A ratchet stops new hand-written boundary shapes.
2. **The fixtures that hid the 11–12 Nov live bugs are replaced by recordings:**
   - the flat task spec;
   - `networkVolumeId`;
   - the `tasks logs` source;
   - the empty-log output that the Runtime refused.
3. **The CPU journey `tests/integrations/test_remote_machine_cpu.py` runs in the shared worker environment and on CI.** Today it fails 24 of 25 tests locally on the unchanged base.
4. **An offline fault matrix** asserts, for each injected failure, both a named reason in the receipt or CLI and a defined terminal state for the task and the machine. Failures covered:
   - provider stock and 429;
   - a pod that dies;
   - an engine install or doctor failure;
   - a failure publication the Runtime rejects;
   - an expired lease;
   - a host stopped mid-publication;
   - a storage wait;
   - a held concurrency slot.
5. **One written terminal-state contract** for a failed attempt and its machine: what "unknown" versus "definitely rejected" means, who decides each end state, and when a machine is kept or released (Plan 40 D12 as amended by D13). Every transition has a test in the matrix.
6. **A visibility rule** enforced by a lint or ratchet: no wait loop without a reason line, and no `from None` without a typed reason.

**Phase 2 (committed, not estimated):**
- a real pod agent in the harness;
- a no-op CPU engine, so the harness needs no ComfyUI;
- migrating the remaining raw boundary readers;
- lifecycle typed errors (a lifecycle pin bump);
- a container CI job for the harness.

**Not included:**
- keeping machines across a host restart (needs Plan 40's deferred pod-side cap; see D2);
- GPU validation itself ([Plan 34](../34-real-gpu-proof/plan.md));
- greening other CI lanes ([Plan 39](../39-green-mains/plan.md)).

## Existing work and decision

This finishes the structural design written for Release 13 on 12 Nov ([structural-runpod-design.md](../../releases/13/structural-runpod-design.md)), whose pieces A (one provider boundary, slices s1–s3), C1 (a reason vocabulary) and the provider gate are already in the Release 13 rehearsal. Pieces B (recordings and replay) and D1 (the offline harness) were planned for Release 13 and not built.

The 12 Nov live batch added a second boundary the design did not cover, the Agent–Runtime protocol:
- **A stuck failure publication:** a rejected `fail` retried forever, so the task stayed `running` and every later task waited.
- **A silent CLI:** it read `spec.inputs` where the Runtime returns `spec.spec.inputs`.

Both were invisible to tests because the fakes agreed with the code, not with the Runtime. Evidence, alternatives and the challenge are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Phase 1 order is in [tasks.md](tasks.md):
1. make the CPU journey runnable (RB-1) and land the recording library (RB-2) in parallel;
2. then replace the known-bad fixtures (RB-3) and write the terminal-state contract (RB-4);
3. then the fault matrix (RB-5) and the visibility ratchet (RB-6);
4. one review round at the end.

Recordings are captured passively during paid runs already authorized for Release 13; this plan authorizes no spend of its own. Recording this plan authorizes no implementation; D1 decides whether phase 1 starts inside Release 13.

## Interfaces and handoff

**Consumes:**
- Agent Release 13 rehearsal `scratch/r13-rehearsal` (`dd5bc822` at writing) plus the in-flight branches `r13/terminal-reconcile`, `r13/cli-wait-visibility` and `r13/keep-warm`;
- Runtime `42ae24af` plus `r13/inline-output-proof`;
- runpod-lifecycle `f294881`;
- the recordings in `briefs/evidence/runpod-recorded/` (manager scratch; RB-2 moves them into the Agent repository).

**Produces:**
- `tests/providers/recorded.py` and per-provider recording folders;
- recorded Runtime and engine shapes;
- a runnable CPU journey with a fault matrix;
- `docs/` text for the terminal-state contract;
- a ratchet in CI.

Later engine or provider work builds on the recording folders and the matrix.

## Completion

- One documented CPU command runs the journey and fault matrix green on the integrated revisions.
- Each 11–12 Nov live failure has a matrix row that fails on its pre-fix revision and passes after: `networkVolumeId`, the unclassified stock reason, the bare False verification, the 429 storm, the readback overwrite, the rejected failure publication, the silent wait.
- **Negative case:** a hand-written provider or Runtime dict in a new test fails the ratchet.
- **Limits:** this proves behaviour against recorded shapes, not against shapes RunPod or the Runtime have not yet returned; live GPU proof stays with Plan 34 and the release gate.
