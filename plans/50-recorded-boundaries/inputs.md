# Inputs — Recorded boundaries and an offline generation harness

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner asked on 12 Nov that "the updated plan is on main" after asking whether this structural work was set for the next release and captured as a project. That records the plan; it is not a choice of end state or of release placement. Next: the owner decides D1.

**Prior art:**
- [structural-runpod-design.md](../../releases/13/structural-runpod-design.md) (12 Nov, 01:45 UTC) is the design this plan completes.
  - Its §1 traces six paid-run failures to one mechanism: a typed fact flattened at a boundary that tests faked with shapes RunPod never returns.
  - Its §5 (piece B) defines the recording, scrubbing and replay rules.
  - Its §7 (piece D1) defines the harness.
- Already built in the Release 13 rehearsal: s1–s3 (`ad7723a8`, `ae0f284d`, `c474563d`, `4696668d`), the reason slice C1, the provider gate `f0535fef`. `tests/providers/test_provider_contract.py` exists, but there is no `tests/providers/recorded.py` loader.
- 12 Nov live evidence (Release 13 [decision log](../../releases/13/decisions.md), 12:41–12:56 UTC entries):
  - **Rejected failure publication:** a project task's failure with an empty log was refused. Runtime `runtime_protocol/service.py:9294-9321` treats an existing ownerless object as unproven even when its inline bytes are hash-verified. The Agent's `generic_host.py` reconcile loop (about 11590) then replayed the rejected `fail` forever, holding the GPU reservation and the executor's slot.
  - **Silent CLI:** `astrid/sdk/invocation.py:_runpod_generation_policy` read `task["spec"]["inputs"]`; the Runtime returns `spec.spec.inputs`. The fixture at `tests/packs/runpod/test_pack_actions.py:336` used the flat shape.
  - **Hidden wait reason:** the Runtime `_claim_task` reports only the first blocker (`store.py` about 4392-4419), so `insufficient_storage` hid the held slot.
- `tests/integrations/test_remote_machine_cpu.py -m integration` fails 24 of 25 tests on the unchanged base `b306b2be` with `ASTRID_RUNTIME_CHECKOUT` set ("target status task failed"); without it, 24 setup errors. Diagnosed 12 Nov: it is not environmental. Every failure is the same rejected publication: `runpod.setup` runs with no project and settles empty logs, then `runpod.status` under a project publishes the same empty-log digest inline and the Runtime refuses it (`service.py:9297-9321`). Agent `83eaa2402` (declared logs as task outputs, 12 Nov) introduced the trigger; stubbing `_log_outputs` makes the first test pass. CI has never run this file: Agent `main` lacks it, and the int/32 lanes run (42806140544) died in setup. So the one test that runs the real Agent against the real Runtime would have caught the 12 Nov stuck-task bug offline, had it run anywhere.
- Related plans:
  - [Plan 39](../39-green-mains/plan.md) (paused) owns CI greenness in general;
  - [Plan 34](../34-real-gpu-proof/plan.md) owns live GPU proof;
  - [Plan 40](../40-machine-lifetime-controls/plan.md) owns machine retention, and its deferred item "a provider-side or pod-side cap that holds when no host runs" is the prerequisite for retaining machines across a host restart.

**Approach:** Build on the existing CPU journey and provider-contract test rather than a new framework: recordings plus a replaying fake behind the existing seams, and a fault matrix inside the existing journey.
- **Alternatives considered:**
  - (a) keep fixing each boundary bug as found: cheapest now, but every one of the 11–12 Nov bugs was found only on a paid pod;
  - (b) a full simulator of RunPod and the Runtime: larger, and it drifts from the real services exactly as hand-written fakes do;
  - (c) contract tests against live services in CI: needs credentials and paid pods, against the safety rules.
- Recordings with a refusing replay are the smallest approach that ties tests to real shapes.

**Challenge:** Required: this touches a cross-repository contract (Agent–Runtime) and exceeds five days. Pending — an independent advisor critique of this draft is running (12 Nov). Next: record its findings and what was accepted.

**Proof and limits:** See [plan.md](plan.md#completion). The matrix proves behaviour only against recorded shapes. Shapes the services have never returned are not covered, so recordings must be refreshed when a provider or Runtime changes, and the ratchet makes a missing recording a test failure, not a silent pass.

**Review rounds:** Recommend one round at the end (S route), because the terminal-state contract (RB-4) changes when tasks and machines end, which is user-visible and cross-repository. No review stop: RB-4 is small, and RB-5 builds on it immediately, so a late finding costs one task.

**Run start:** Pending — No run is authorized. Next: the owner decides D1.

## Owner decisions

- **D1. Release placement.**
  - Options:
    - (a) phase 1 inside Release 13, before its gate: about 6–8 worker-days, and the candidate slips accordingly;
    - (b) only RB-1 (journey runnable) and RB-3 (replace the known-bad fixtures) inside Release 13, the rest as the first work after Release 13 publishes;
    - (c) all of it after Release 13.
  - **Recommendation: (b).** RB-1 and RB-3 are about a day together and cover the boundaries that failed live on 12 Nov. The full matrix is the right first project of the next release.
  - Pending.
- **D2. Machines across a host restart.** Today a host shutdown or restart releases every kept machine (`astrid/packs/runpod/adapter.py:659` `host_shutdown`, `worker_owner.py:270` `restart`), consistent with Plan 40 D12, because Astrid's idle and paid timers run only inside the host.
  - Options:
    - (a) keep that;
    - (b) keep machines across a restart once a pod-side or provider-side cap enforces the limits with no host (Plan 40's deferred item).
  - **Recommendation: (a) now, (b) as a Plan 40 follow-up.** Not in this plan.
  - Pending.

## Source identities

- **Agent:** Release 13 rehearsal `scratch/r13-rehearsal` at `dd5bc82236b59e8bcbd1662e8886552d45cda731`, plus the in-flight `r13/keep-warm` (`d072cf5d`), `r13/terminal-reconcile` and `r13/cli-wait-visibility`.
- **Runtime:** `42ae24aff8d2cb854f874ce134161077a3ba3641`, plus the in-flight `r13/inline-output-proof`.
- **runpod-lifecycle:** `f2948817eeb94af8dee76be21f6d673724f1606e`.
- **VibeComfy:** `c7a47e36d6fe27518c438ddaf911ae261dbc5693`.
- **Destination:** Agent and Runtime `main` through the Release 13 or next release candidate, per D1.

## References

- [Release 13 structural design](../../releases/13/structural-runpod-design.md)
- [Release 13 decision log](../../releases/13/decisions.md)
