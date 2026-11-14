# Tier 2: warm jobs through the machine's resident host

**Status: STOPPED AT REVIEW, 01:00 UTC Sun 15 Nov 2026. Do not build from this note.** An independent review found blocking gaps: today's pod job does not use the pod's Runtime; the per-job reset replaces that Runtime, so nothing kept warm under it survives; settlement, the idle expiry, its watchdog deadline and the host timer must complete before success is reported; a failed reset must release the machine at once; reconciliation needs an idempotent request key. The design restarts as task SP-2 of plan 54 (astrid-dev PR #654), led by the pod-custody owner. Kept as the record of this attempt. Original status: design note for review, 00:30 UTC Sun 15 Nov 2026. Author: the Release 13 advisor. It replaces the "resident job service" sketch in `warm-latency-strategy.md`. Not for Release 13; it is the first phase of the speed plan (plan 54).

## The decision
**Do not build a new service.** The rented machine already runs a resident Astrid Runtime and a pack host that claims and executes tasks (`astrid/packs/runpod/pod_reset.py:308,324`; `astrid/sdk/autobootstrap.py:503`; `astrid/core/execution/generic_host.py:14031,14096`). A warm job should be admitted to that host and run by an executor it keeps warm. Today's cost exists because dispatch stages a shell job that starts four Python processes and re-audits (`astrid/packs/runpod/machine.py:431-449, 925-938`).

Two alternatives were checked and rejected:
- **A new daemon on its own port.** The engine endpoint is bound to the engine's single port (`astrid/core/generation/engine_endpoint.py:346,407`) and the engine supervisor holds one engine (`astrid/core/generation/engine_custody.py:1146`). Both would need new work, one of them in the external lifecycle package.
- **The host talking straight to ComfyUI.** A second code path for rented jobs; custody checks move. The owner asked for one path through Astrid.

## What a warm job does
Precondition: the claim holds a warm attestation (Release 13, card W-A) that covers this workflow's requirements, bound to the current supervisor incarnation.

1. **Host, before the machine:** lease, cost, deadline and fence checks as today; one liveness call. Compare the workflow's requirements with the attested set. Not covered → the full path.
2. **One remote command, up:** a small non-Python client on the machine (curl to the machine's Runtime on loopback) submits the job envelope: workflow, bound inputs, the invocation fence, the deadline. Inputs travel in the same request for small files, or as one bundle before it.
3. **On the machine:** the resident host admits the task and runs it in a **kept-warm executor**, the pattern the Wan pack already uses (`generic_host.py:1166-1170`, `_WARM_SESSION_ADAPTERS`). The executor holds the imported libraries and the compiled schema. It checks the attestation against the live supervisor's identity, takes the engine lock, submits to ComfyUI, and collects.
4. **The same command returns:** the result manifest, the job record (timing, VRAM, engine log slice) and small outputs, in one response. Large outputs follow in one verified bundle.
5. **After the result:** prompt clean-up, the machine's realm reset and the watchdog deadline publication run behind the existing `ready` gate. The next job's start waits (bounded) on `ready`. A failed reset fences the lease at the next start, as today.

Remote operations on the caller's wait: liveness, the job command, and at most one output fetch. Process starts on the machine: none.

## Custody, unchanged
- Lease admission, cost and deadline checks, the invocation fence, settlement, idle timers: on the host, as today.
- The fence and deadline are checked again on the machine by the executor, in process, where the shell job checks them now.
- One admission and settlement authority on the machine: its Runtime. The executor does not settle by a side door.
- Declared logs for every generation: produced by the executor and returned with the result.
- Cancellation: the host cancels the task through the machine's Runtime; the executor interrupts its own prompt and drains, as the attached path does.
- A second request while one runs: refused or queued by the machine's Runtime, never run concurrently on one engine.

## When it falls back, and how
| Situation | Behaviour |
|---|---|
| No attestation, or it does not cover the requirements | Full path; the result says why |
| Supervisor incarnation differs from the attestation | Attestation void; full path |
| The warm executor is not running or does not answer in a short bound | Start it once; if that fails, full path |
| The job command's outcome is unknown (connection lost after submit) | **Never resubmit.** Reconcile by task id through the machine's Runtime: fetch the result if it finished, cancel if still running, and only then decide |
| Reset after the result fails | Lease fenced at the next start; reported then |

## Open decisions for the review
1. **The executor boundary.** The host spawns a child per task (`generic_host.py:10809`) and the pod runner needs main-thread signal custody (`astrid/packs/vibecomfy/local_job.py:61,84`). Option A: a kept-warm child, as the Wan adapter does. Option B: run in the host process. Recommendation: A; it reuses a proven pattern and keeps signal handling in a process of its own.
2. **Does the realm reset stay?** The job still changes the machine's Runtime state, so yes, but off the caller's wait. Removing it would need the machine's Runtime out of the path, which contradicts "one admission authority".
3. **How the result returns.** One long-running command whose output is the result (simple; the agent polls it at 0.5 s), or submit then a second command to fetch. Recommendation: one command; add a fetch only for large outputs.

## Budget tests (the gate)
On the fake claimed machine (`tests/packs/runpod/test_job_on_claimed_machine.py`, `machine_case`), with one shared counter that every remote operation, process start, poll and hash pass goes through:
- After one full job attests the claim, a second job with the same requirements issues at most three remote operations before the result, starts zero processes on the machine, runs zero audit commands, **and returns valid outputs and a job record** (counts alone do not prove a job ran).
- One test per row of the fallback table.
- Cancellation mid-job and a second admission while one runs.
- A crash of the warm executor between jobs: the next job restarts it or takes the full path, and nothing is left holding the engine lock.

## Build lane
Four workers after the review, about two to three hours of build, then custody review rounds:
1. **Warm executor** (S): `astrid/core/execution/generic_host.py` (a warm adapter for generation jobs beside the Wan one), `astrid/packs/vibecomfy/local_job.py`, `astrid/core/generation/managed_preparation.py` (use the attestation, hold compiled state).
2. **Dispatch and return** (X): `astrid/packs/runpod/machine.py` (`_start`, poll, fetch → one command), `astrid/packs/runpod/generation.py`.
3. **Fallback and reconciliation** (S): the same files; the unknown-outcome path first.
4. **Meter and budget tests** (X): `astrid/packs/runpod/remote_placement.py`, the fake machine in `tests/packs/runpod/`, `astrid/core/execution/phase_timing.py`.

Expected overhead on a warm same-model job: 3 to 5 s, almost all of it the two proxy round trips and the agent's 0.5 s command poll (estimate; unmeasured). Getting under 0.5 s needs a held-open channel to the machine's Runtime, which is the lifecycle change this note avoids; it belongs to the next phase.
