# Local speed

**Project:** Local speed

**Goal:** On your own computer with the model already loaded, a generation comes back in the time the model takes: Astrid adds under a tenth of a second for a caller that is already connected.

**Status:** active

**Owner:** Release 14 Lead (`session_011EzfW3Zy19ncNecpQnKb7D`), by [packet dispatch](../../releases/14/run.md)

**Estimate:** 2–3

**Waiting on:** LS-3, the design ([R14-P55-01](../../releases/14/packets/R14-P55-01.md)); owner approval for paid GPU work, a Windows tester, re-pins and product-main merges

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each, then run `python3 scripts/astrid_dev.py sync`. Its priority is its place in [priority.md](../../plans/priority.md).

**Vision gaps:** [Portable generation](../../vision/gaps/F-008-portable-generation.md) (primary): a person who already runs ComfyUI will only route work through Astrid if Astrid costs them nothing they can feel.

## Outcome and scope

Today a warm job on a person's own ComfyUI takes about 30 seconds of Astrid's time around a few seconds of the model's. This project is the release after Release 13, and it is about that path only. Rented machines are out of scope and stay in [Plan 54](../54-warm-latency/plan.md).

It is designed from the work that is fundamentally required, not by trimming today's path.

### What a warm local job fundamentally needs

1. Carry the request to a process that already holds state.
2. Put this job's values into a workflow that was prepared earlier, and check those values.
3. Stage an input file if there is one and ComfyUI does not already have it.
4. ComfyUI validates, queues, runs and saves. This is ComfyUI's time, not Astrid's.
5. Learn that it finished, and which files it wrote, by being told.
6. Take the output once: read it once, hash it once, put it where the caller wants it.
7. Record the job.
8. Reply.

Everything else Astrid does today answers a question whose answer only changes when something is installed, updated, added, removed or restarted: which workflows exist, where they run, what nodes and models are present, whether the installation is the one that was approved. Those answers are computed when the state changes and held, not recomputed per job.

### The design

- **A fast lane, entered by a key.** The key is the workflow's identity, the shape of its inputs (which optional inputs are present, list lengths), where it runs, the running ComfyUI, and the Astrid installation. The first job with a key takes the full path and leaves behind a prepared workflow and the facts it verified. Every later job with that key takes the fast lane.
- **Leaving the fast lane costs nothing to detect.** ComfyUI restarting drops the held connection. A workflow or installation change changes the key. A model that has gone, or a node that no longer accepts the workflow, is refused by ComfyUI itself; that refusal sends the job round the full path once, which produces the same typed refusal as today. The fast lane never guesses: any surprise is the full path.
- **A prepared workflow.** VibeComfy compiles a workflow once into a template with named slots. A job fills the slots (prompt, seed, sizes, input file names, a private output prefix). Astrid does not validate the graph per job: ComfyUI validates every submission itself, and its refusal is translated into Astrid's typed refusal. The [keep list](inputs.md#the-keep-list) names every step that stays on a warm job and why.
- **One held connection to ComfyUI.** Submit against it, be woken by it when the job's history is ready, read that history once, and pass progress through. No polling. The connection is shared; what is per job (the one-prompt-per-attempt rule, the witnessed prompt) stays per job.
- **The output handled once.** One read, hashing as it streams, written to the store and to the caller's destination from the same bytes. The preview image is made after the reply.
- **Resident sessions, a capability Astrid gives to packs.** A pack declares that an action needs a long-lived session. Astrid core starts it, pins its source, gives it a clean environment, fences it, and ends it when its source or the installation changes or when it misbehaves. The session is a separate process from the host. The VibeComfy pack is the first user: its session holds the catalogue, placements, templates and the ComfyUI connection. Everything that knows about ComfyUI (the connection, the template, completion) lives in the VibeComfy package; core knows nothing about ComfyUI. Packs that do not declare a session keep a process per job (D8).
- **One door.** Every caller (the App, the SDK, the command line, an agent) still asks through the Runtime, so there is one record and one set of permissions. The existing create, claim and settle steps stay; what goes is the three places that poll once a second (the host looking for work, VibeComfy looking for completion, the caller looking for the result). The Runtime gains a way to wait for work and to wait for a result. A deeper Runtime change (admission and claim in one step, the output published in one pass) is built only if LS-1 shows the existing steps do not fit the budget. A direct door that bypasses the Runtime was considered and is not proposed (D3).
- **A thin request.** The caller sends what was asked (which workflow, which values). Working out what that means moves to the resident side, where the answers are already in memory. The command line becomes a small client; the agent tool server calls in-process instead of starting the command line.
- **Success keeps its meaning.** A reply still means a stored, recorded result. The saving comes from doing the forced disk writes once and together, not from replying early (D2).
- **Cancel only what is ours.** A cancel names the job. Astrid never uses ComfyUI's global interrupt, which can stop someone else's work on a person's ComfyUI.

### What stays

- The Runtime is the record of every job and the authority on who may ask.
- Every output has a content digest and is stored unchanged.
- Refusals keep their types and wording.
- Install and download decisions (what is missing, what to fetch, is this ready) keep their full checks; they are state-change work and are not on the warm path.
- A job never takes another job's output: a private output name per attempt, and declared outputs confirmed in the result.
- Astrid never stops, restarts or interrupts work on a person's ComfyUI that it did not start.

### The floor, and the targets

Estimates, not measurements; LS-1 measures them before anything is built.

| Step | Linux | Windows |
| --- | --- | --- |
| Request and reply | 0.2 to 2 ms | 0.5 to 5 ms |
| Check the request, name the job | 0.1 to 2 ms | 0.2 to 3 ms |
| Fill and check the template | 0.2 to 5 ms | 0.5 to 8 ms |
| ComfyUI's own validation and queue wake-up | 1 to 10 ms | 2 to 20 ms |
| Woken at completion, one history read | 1 to 8 ms | 2 to 15 ms |
| Read, hash and store a one-megabyte output | 1 to 8 ms | 2 to 20 ms |
| Record and force to disk | 1 to 15 ms | 2 to 35 ms |
| **Already-connected caller, total** | **15 to 70 ms** | **25 to 120 ms** |
| A new command-line process on top | 25 to 150 ms in Python | 80 to 500 ms in Python |

Two independent estimates (the advisor's and an Astra review that was not shown it) agree that under 0.1 s is plausible for an already-connected caller on both systems, with Windows' slowest cases unproven. They also agree on what is outside the number: waiting behind another job in ComfyUI's queue, a large output (about 50 to 330 ms per 100 MB to read and hash), a new input file, and a custom node whose own validation is slow.

Proposed targets (D1), after a first stage of under 2 s for every caller: median overhead for a one-megapixel image, measured as caller wall time minus ComfyUI's own start-to-success span.

| Caller | Linux and macOS | Windows |
| --- | --- | --- |
| Already connected (SDK, App, agent tool server) | under 0.1 s | under 0.1 s, confirmed by measurement |
| Command line | under 0.25 s | measured first; target set from LS-1 |
| First job after a start, update or change | under 3 s | under 5 s |

Queue wait is reported separately and never subtracted silently.

### Included

Phase 1, the floor and the meter: LS-1, LS-2. Phase 2, design: LS-3, RS1. Phase 3, the fast lane: LS-4 to LS-11, LS-15. Phase 4, the first job and Windows: LS-12, LS-13. Phase 5, proof: LS-14, R.

### Not included

Rented machines (Plan 54). Model loading time and anything inside ComfyUI. Changing what a person's ComfyUI has installed. New workflows.

## Existing work and decision

The measurements, the code traces and the independent review are in [inputs.md](inputs.md#planning-evidence). In short: nothing in today's path is slow because the work is hard; it is slow because every job repeats work whose answer has not changed, in new processes, with polling between them.

What this plan takes from Plan 54, drops and adds is listed in [inputs.md](inputs.md#plan-54-what-moves-here). The decision to design from the floor up, and to leave rented machines out, is the owner's (15 November 2026).

Smaller alternatives considered: caching inside today's path (Plan 54's local tasks) reaches one to four seconds and stops there, because the per-job process, the polling and the per-job resolution remain. A direct socket to the worker that bypasses the Runtime is faster to build and leaves two doors (D3).

## Sequence and readiness

LS-1 first, in two steps. A throwaway script does only steps 2, 4, 5 and 6 against a real ComfyUI and prints the overhead: the floor that is not ours to remove. Then the existing Runtime steps and real output storage are added to it, unchanged, and each is timed. That second step decides whether the deeper Runtime change is needed at all. Both run on Linux and on Windows. LS-2 turns the test lane's attached harness into the standing meter. LS-3 is the design, and RS1 reviews it once, because the door, the durability rule and the worker's lifetime are what LS-7 to LS-10 are built on.

LS-5, LS-6 and LS-11 do not wait for the design: they are needed under any door.

Real bottlenecks: the design review; two re-pins (VibeComfy for the template and the connection, the Runtime for the hand-off and the record); a live measurement on a GPU machine where Astrid and ComfyUI run together; a Windows measurement, which needs a tester or a Windows machine.

Task details are in [tasks.md](tasks.md). The owner's 15 November 2026 run authorization is recorded in [inputs.md](inputs.md#planning-evidence); its limits govern this run.

## Interfaces and handoff

**Consumes:** Release 13 as published (astrid-agent, VibeComfy and Runtime at the Release 13 pins); the test lane's attached-ComfyUI harness; Release 13's per-phase timing block; donor branches named in [inputs.md](inputs.md#source-identities).

**Produces:** a VibeComfy template interface (compile once, fill per job) and a held ComfyUI connection; a Runtime hand-off for local jobs; a resident worker in the pack host; a thin command-line client; a standing budget test that fails a pull request which adds a process start, a wait or a forced disk write to the warm local path. Plan 54 can reuse the worker and the template for rented machines.

## Completion

- The standing budget test passes on Linux and Windows against a stand-in ComfyUI: on the second job with the same key, no process is started, nothing sleeps or polls, the workflow is not compiled, each output byte is hashed once, and the number of forced disk writes before the reply is within the budget LS-3 sets. It also asserts a valid output and a job record.
- Live, on a GPU machine with a warm model: the targets in D1 are met for the default image workflow and reported for the default video workflow, on Linux and on Windows.
- Negative cases, each ending in the same typed result as today: ComfyUI restarted between jobs; a model removed; a node pack removed; the workflow edited; Astrid updated; the worker killed mid-job; two callers at once; a cancel.
- Limits: the numbers are for a warm model and a caller on the same machine. The first job after a change is slower by design and has its own target.
