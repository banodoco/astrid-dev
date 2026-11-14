# Warm-job latency

**Project:** Warm-job latency

**Goal:** When the model is already loaded, a generation returns in about the time the model takes: under 5 seconds of overhead on a rented machine, then under half a second, and under a tenth of a second on a creator's own computer.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 9–13

**Waiting on:** [Release 13](../../releases/13.md) publishing with the first tier of fixes, and the owner's go

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a warm machine that answers in seconds is what makes a rented or local engine feel like one tool. [Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (supporting): every second of a generation is accounted for, so a slow job explains itself.

## Outcome and scope

On 14 November 2026 a second image job on a warm rented machine took 242 seconds. ComfyUI spent 2.9 of them generating. The rest was Astrid repeating its cold path: re-checking an installation that had not changed, starting new processes, talking to the machine one small step at a time, and making the caller wait for clean-up.

When this project is done:

- **Rented machine, warm, same model:** overhead (wall time minus the model's own time) is under 5 seconds, then under 0.5 seconds.
- **Creator's own computer, warm (Astrid-managed or their own ComfyUI):** overhead is under 0.1 seconds for a caller that is already running (the agent, the SDK, the App); the command line is at the floor of starting a process, about 0.1 seconds.
- **Every second is accounted for.** Each result carries a timing breakdown whose parts add up to the wall time, with any remainder shown as `unaccounted`.
- **It stays that way.** Tests count remote operations, process starts, polls and hash passes on a warm job, and fail when a budget is exceeded.

Included:

1. **Phase 1, a resident Astrid job service on the rented machine.** Started once when the claim is attested, it holds the verified state and compiled schema in memory, takes each job in one exchange and returns the result and its evidence in the same exchange. Jobs still pass through Astrid: the same compile, validation, job record, evidence and settlement.
2. **Phase 2, rented under 0.5 seconds.** A held-open connection, completion pushed over ComfyUI's websocket, schema and compiled workflows cached per engine start, one hash pass.
3. **Phase 3, local under 0.1 seconds.** The same caches and push on the local path, admission and results without polling, evidence after the result, a thin command line.
4. **Carried from Release 13:** any first-tier card that misses the Release 13 freeze (listed in [tasks.md](tasks.md)).

Not included: model load time, generation time, the first job on a fresh machine (installing the engine environment is its own work), and provider start-up time.

## Existing work and decision

Release 13 delivers the first tier on the existing path: a per-claim attestation so later jobs skip re-verification, one bundle each way, the result returned before the reset, faster polling, and per-phase timing. That is expected to bring a warm rented job to roughly 30 to 45 seconds of overhead. It cannot reach 5: a process start on the machine and the remaining round trips cost seconds each.

This project builds on that attestation, the existing engine supervisor, and the authenticated engine endpoint that already reaches a loopback port on the machine. The alternative of sending warm jobs straight from the host to ComfyUI was designed and rejected: it would give rented jobs a second code path and move custody checks. Evidence, alternatives, the critique and the owner's choices are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Phase 1 first: it removes the most seconds and defines the protocol the later phases reuse. A review stop follows the protocol and the supervision design, before the service is built on them. Phase 2 and Phase 3 share three tasks (schema and compile cache, websocket completion, hash once) and can run in parallel after Phase 1's protocol is reviewed. Nothing here starts before Release 13 publishes and the owner starts a run. Tasks, routes and the critical path are in [tasks.md](tasks.md).

Constraints: custody and money bounds do not move. A service that cannot prove it is the one the attestation describes is not used; the job takes the full path. Paid live runs are the orchestrator's.

## Interfaces and handoff

**Consumes:** Release 13's warm attestation record and timing block (astrid-agent, the Release 13 tag), the engine supervisor (`astrid/core/generation/engine_custody.py`), the engine endpoint transport (`astrid/core/generation/engine_endpoint.py`, `engine_transport.py`) and the pinned `runpod-lifecycle` version.

**Produces:** a versioned job-service protocol (one request, one response carrying result, evidence and timing); budget tests that later work must keep green; and a timing block whose parts sum to the wall time. Phase 2 may need a lifecycle change to allow websocket upgrades through the engine bridge; that is a cross-repository contract change and is called out in its task.

## Completion

- A live run on a rented machine: the same image model three times, a video edit twice, then the image model again. For the second and third image jobs, wall time minus ComfyUI's reported time is under 5 seconds after Phase 1 and under 0.5 seconds after Phase 2, with `unaccounted` under 5% of the wall time.
- A local run on an Astrid-managed engine and on a person's own ComfyUI: median overhead under 0.1 seconds over twenty warm jobs from a resident caller.
- The budget tests pass and are part of the standing suite.
- Negative cases: a restarted supervisor, a new workflow requirement, an unreachable service and a corrupt or missing attestation each take the full verified path and say so in the timing block.

Limits: the targets are for small outputs (an image); large video outputs are bounded by transfer. Proof on Windows is local only.
