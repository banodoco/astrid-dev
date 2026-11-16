# Generation speed

**Project:** Generation speed

**Goal:** When the model is already loaded, a generation returns in about the time the model takes: under 5 seconds of overhead on a rented machine, then under half a second, and under a tenth of a second on a creator's own computer.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 3–5

**Waiting on:** [Release 13](../../releases/13.md) publishing with the first tier of fixes, and the owner's go

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a warm machine that answers in seconds is what makes a rented or local engine feel like one tool. [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting): every second of a generation is accounted for, so a slow job explains itself.

## Outcome and scope

On 14 November 2026 a second image job on a warm rented machine took 242 seconds. ComfyUI spent 2.9 of them generating. The rest was Astrid repeating its cold path around ComfyUI: re-checking an unchanged installation, starting new processes, talking to the machine one small step at a time, and making the caller wait for clean-up.

When this project is done:

- **Rented machine, warm, same model:** overhead (wall time minus the model's own time) is under 5 seconds, then under 0.5 seconds.
- **Creator's own computer, warm (Astrid-managed or their own ComfyUI):** overhead under 0.1 seconds for a caller that is already running (the agent, the SDK, the App); the command line sits near the floor of starting a process (measured today at about 0.2 seconds for `generate --help` against a 17 ms Python floor).
- **First job and model switches are no slower than they must be:** a fresh rented machine does not reinstall an engine environment it has installed before, and the node and installation checks are cheap on every path.
- **Every second is accounted for.** Each result carries a timing breakdown whose parts add up to the wall time, with any remainder shown as `unaccounted`.
- **It stays that way.** Tests count remote operations, process starts, polls and hash passes on a warm job, and fail over a budget.

The estimate is in days of elapsed time at agent speed. Builds here are hours; the time goes to design and custody review rounds, paired proof, frozen-head CI and live runs.

### Target architecture

The end state, stated from first principles. Every task in [tasks.md](tasks.md) serves one of these and says which. **Target warm overhead: one round trip plus milliseconds: under 0.5 seconds rented, tens of milliseconds local.**

1. **Verify at state changes, compare per job.** Installation, claim, engine start and download are the moments facts change. Verify fully then, record the result, and on each job compare cheap digests against the record. Today the full verification runs on every job (`astrid/core/generation/managed_preparation.py:414-857`), and for node packs no record exists at all (`astrid/core/generation/engine_runner.py:909-940`).
2. **A resident process next to the GPU; a job is one message in and one message out.** Today a rented job is about twelve operations to dispatch, four Python starts on the machine, and a fetch per file (`astrid/packs/runpod/machine.py:431-449, 865-938, 1170-1203`).
3. **Control plane and data plane are separate.** The control plane owns what lives as long as a claim or an engine start: the lease, deadlines, idle expiry, the attestation and the reset. The data plane runs jobs and checks facts already in memory. Money safety is decided by the control plane, never recomputed on the job path. One qualification from the code: some money facts change with every job (the invocation fence; the idle expiry and its watchdog deadline, which must be in place before success is reported: `astrid/packs/runpod/worker_owner.py:640, 794-798`). In the end state those are a local, acknowledged update to the resident control agent on the machine, costing milliseconds, not a remote command and a new process as today (`astrid/packs/runpod/pod_watchdog.py:260-311`).
4. **Lean on ComfyUI.** It already keeps models resident and evicts on demand (`comfy/model_management.py:893-983`), validates on submit (`execution.py:846-1238`), caches unchanged nodes between jobs (`comfy_execution/caching.py:102-127`) and announces completion (`server.py:269-290`). Astrid adds only four things: gating before money is spent (on the host, before the claim), provenance (hash once), custody, and translating ComfyUI's errors into its own refusals. Two limits bound this: ComfyUI can queue the valid branches of a graph while reporting errors on the rest (`server.py:1115-1139`), and it lists file names, not verified bytes.
5. **Content addresses for inputs, compiled workflows and outputs.** An input already on the engine is not sent again; a compiled workflow is reused; an output is hashed once and that digest travels with it. Today inputs are named per task (`astrid/core/generation/backends/comfy_target.py:327`), which also defeats ComfyUI's cache.
6. **One path for local and remote, always measured.** The same resident executor serves the App, the agent and a rented machine; only the transport differs. Every result carries timing that sums to the wall time, and budget tests are a required check, so the cold path cannot creep back into the warm one.

Two rules follow from principles 1 and 4, and each has a failure behind it:

- **ComfyUI is the authority on what a node accepts; Astrid never refuses what ComfyUI would run.** On 15 November a live first-frame video job was refused for an input name that the node accepts at run time and that `/object_info` does not list. ComfyUI itself does not reject unknown input names (`execution.py:1128-1195`); the pre-check was stricter than the engine it guards.
- **Verify at a trust boundary once; inside a job, carry the digest.** What was installed, what was admitted and what was delivered are each worth proving once. Re-reading, re-hashing, re-emitting and re-auditing the same thing later in the same job proves it only to ourselves.

Astrid's own full check remains where nothing is submitted (dry run, readiness, listings, download planning) and before a claim. The table in [inputs.md](inputs.md#planning-evidence) gives each heavy step, what ComfyUI does, what Astrid adds and the leaner design.

### Included

1. **Phase 1, rented under 5 seconds.** A warm job stops being the cold path run again: no process starts on the machine, no re-audit, one exchange each way. **Design first:** the first sketch failed its review, and the phase opens with a design round led by the pod-custody owner.
2. **Phase 2, rented under 0.5 seconds.** A held-open channel, completion by push, compiled workflows reused.
3. **Phase 3, local under 0.1 seconds.** The narrow, change-driven check; push for admission, completion and results; one hash pass; a thin command line.
4. **Phase 4, the first job.** The engine environment kept on the volume; a node receipt; one installation audit; what a model switch costs, measured and reduced where Astrid causes it.
5. **Carry-overs from Release 13,** each as its own task: listed in [tasks.md](tasks.md).

Not included: the model's own load and generation time, and the provider's machine start-up time.

## Existing work and decision

Release 13 delivers the first tier on the existing path: a per-claim warm attestation, bundles each way, faster polling, per-phase timing, one schema fetch and compile per job, and one hash pass on delivery where proven in time. That is expected to bring a warm rented job to roughly 30 to 45 seconds of overhead; it cannot reach 5.

Three shapes for Phase 1 were examined; the evidence and the reviews are in [inputs.md](inputs.md#planning-evidence):

- **The host talks straight to ComfyUI on the machine.** Rejected by the owner: rented jobs must still pass through Astrid.
- **A new job service on its own port.** The engine endpoint is bound to the engine's one port and the engine supervisor holds one engine; both would need new work, one of them in the external lifecycle package.
- **Admit the job to the machine's resident Runtime host and keep its executor warm.** The least new machinery, but its first design note was stopped at review: today's pod job does not use the pod's Runtime, the per-job reset replaces that Runtime, and settlement and the watchdog deadline must complete before success is reported.

So Phase 1 begins with a decision, not a build: which execution boundary on the machine stays resident, and what the per-job reset is for.

## Sequence and readiness

Phase 4's small tasks and Phase 3's independent tasks can start as soon as a run is authorized; they do not wait for Phase 1's design. Phase 1 runs design, review stop, build, custody review, live proof. Phase 2 follows Phase 1. Two tasks need a change in another repository (VibeComfy for completion by push, the Runtime for admission by push) and are sequenced around those pins. Tasks, routes and the critical path are in [tasks.md](tasks.md).

Constraints: custody and money bounds do not move. Paid live runs are the orchestrator's.

## Interfaces and handoff

**Consumes:** Release 13's warm attestation, model-verification record and timing block (astrid-agent at the Release 13 tag); the engine supervisor (`astrid/core/generation/engine_custody.py`); the engine endpoint transport (`astrid/core/generation/engine_endpoint.py`, `engine_transport.py`); the pinned `runpod-lifecycle`, VibeComfy and Runtime versions.

**Produces:** a reviewed design for resident execution on a rented machine; a shared meter and budget tests that later work must keep green; a timing block whose parts sum to the wall time; a workflow-scoped readiness check other features can call. Cross-repository changes (VibeComfy websocket completion, Runtime push admission, any lifecycle change Phase 2 needs) are each called out in their task.

## Completion

- **Rented, live:** the same image model three times, a video edit twice, then the image model again, on one machine. For the second and third image jobs, wall time minus ComfyUI's reported time is under 5 seconds after Phase 1 and under 0.5 seconds after Phase 2, with `unaccounted` under 5% of the wall time.
- **Local:** on an Astrid-managed engine and on a person's own ComfyUI, median overhead under 0.1 seconds over twenty warm jobs from a resident caller.
- **First job:** on a fresh machine with a volume that has run Astrid before, the time from claim to the first result, less model load and generation, is reported and has no reinstall in it.
- **The budget tests** pass and are in the standing suite.
- **Negative cases:** a restarted engine, a new workflow requirement, a changed model folder, an unreachable warm executor, and an unknown submission outcome each take the verified path, never run a job twice, and say so in the timing block.

Limits: the targets are for small outputs (an image); large video outputs are bounded by transfer. Proof on Windows is local only.
