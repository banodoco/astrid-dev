# Local speed

**Project:** Local speed

**Goal:** On your own computer with the model already loaded, a generation comes back in the time the model takes: Astrid adds under a tenth of a second for a caller that is already connected.

**Status:** active

**Owner:** ChatGPT manager — `chatgpt-workspace-6ee41b0f0cca/root`

**Estimate:** 2–3

**Waiting on:** LS-2 CPU meter before LS-3/RS1; owner approval for the LS-5 re-pin and LS-6 scope. GPU proof waits for GPU and does not hold CPU work under D9. [Run authorization and published base](inputs.md#run-start-source-identities).

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

**Real CPU measurements, 16 November 2026.** The original `comfy_floor.py` and `integrated_floor.py` ran against isolated, real ComfyUI on standard hosted Linux and Windows runners, without a model or GPU. Each cell has twenty samples after a separately retained warmup. Overhead is calculated for each sample as caller wall time minus client-observed ComfyUI start-to-success; queue time is not subtracted. These are floor probes, **not the installed Agent generation path or a claim that Plan 55 is fast**.

| Actual CPU workload and path | Linux median / slowest, ms | Windows median / slowest, ms |
| --- | ---: | ---: |
| Trivial graph, transport | 3.20 / 3.82 | 3.33 / 4.16 |
| Trivial graph, Runtime, one caller | 15.94 / 43.02 | 134.37 / 286.72 |
| Trivial graph, Runtime, two callers | 29.61 / 34.81 | 161.39 / 388.18 |
| One-megapixel image, transport | 4.83 / 6.05 | 5.49 / 5.93 |
| One-megapixel image, Runtime, one caller | 41.35 / 319.63 | 225.63 / 592.06 |
| One-megapixel image, Runtime, two callers | 178.49 / 225.22 | 284.01 / 546.03 |

The one-megapixel input is a seeded synthetic RGB image. ComfyUI saved 904,486-byte PNGs on Linux and 927,815-byte PNGs on Windows; the trivial graph saved 338 bytes. The Runtime probes create, claim and settle through actual HTTP/CAS and assert exact stored bytes, a succeeded task and a managed-output association after settlement. Post-settlement verification is outside the timed interval. The two-caller experiment includes admission-lock/queue contention and cannot be attributed wholly to Runtime writes.

| One-caller, one-megapixel integrated phase | Linux median / slowest, ms | Windows median / slowest, ms |
| --- | ---: | ---: |
| Runtime create | 3.01 / 40.03 | 22.29 / 166.37 |
| Runtime claim | 2.69 / 4.38 | 16.79 / 122.65 |
| Fill hand-prepared graph slots | 0.03 / 0.04 | 0.02 / 0.03 |
| POST through acceptance (not pure validation) | 1.29 / 204.79 | 1.68 / 172.84 |
| Observed success to history-ready | 0.38 / 0.41 | 0.56 / 0.93 |
| One history read | 0.79 / 1.05 | 0.73 / 0.84 |
| Fetch and hash output (not store) | 1.87 / 3.56 | 2.57 / 3.55 |
| Prepare inline output descriptor | 1.38 / 2.46 | 2.99 / 3.20 |
| Runtime settle, including store and record | 28.82 / 307.79 | 159.98 / 550.77 |

**Correction to the earlier estimates:** the unchanged one-caller Runtime floor has a Windows median of 225.63 ms, so the previous 25–120 ms total estimate does not support a sub-100-ms promise. Linux's 41.35 ms median fits that aspiration for this probe, but its 319.63 ms slowest sample does not establish a tail guarantee. Both OSes fit the stage-one 2-second floor in these CPU cells. Hand-prepared slot filling is not the proposed VibeComfy template implementation; POST time is not isolated node-validation cost; the fetch/hash phase excludes storage. Native flush counts and the installed Agent's repeated work belong to LS-2 and must not be invented from transaction counts or these suite durations.

For LS-3, retain durable success and the existing create/claim/settle path for stage one; the measurements do not justify weakening D2. The conditional deeper Runtime work is a design question for the tighter target after the standing meter attributes the actual costs, not an automatic permission to combine or omit durable writes.

Evidence: [derived summary and original record identities](../../releases/14/evidence/ls1/real-cpu-20261116.json), [CPU execution PR #353](https://github.com/banodoco/astrid-agent/pull/353), [actual run 43858887774](https://github.com/banodoco/astrid-agent/actions/runs/43858887774). The summary names original artifact/file hashes, exact source commits, Python/OS versions, sample counts and recomputed overhead. The original archives retain full probe records, outputs, commands and exit codes. The probe bytes differ by Windows checkout line endings and are hashed separately; no cross-OS byte identity or equal hardware is implied.

D1 is unchanged: **commit to median overhead under 2 s for every caller** for the stated workload; build for the tighter targets below and promise them only when measured. GPU and Windows-with-GPU results remain waiting for GPU, not a gate on CPU work under [D9 in #728](https://github.com/banodoco/astrid-dev/pull/728).

| Caller | Linux and macOS design target | Windows design target |
| --- | --- | --- |
| Already connected (SDK, App, agent tool server) | under 0.1 s, not yet qualified end to end | under 0.1 s aim; current unchanged Runtime CPU floor does not meet it |
| Command line | under 0.25 s | measured first; target not yet set |
| First job after a start, update or change | under 3 s | under 5 s |

Queue wait is reported separately and never subtracted silently. The first-job and CLI targets have not been measured by this resident floor probe. Large video, new-input, arbitrary-custom-node and warm-model performance are not inferred from the small synthetic image.

### Included

Phase 1, the floor and the meter: LS-1, LS-2. Phase 2, design: LS-3, RS1. Phase 3, the fast lane: LS-4 to LS-11, LS-15. Phase 4, the first job and Windows: LS-12, LS-13. Phase 5, proof: LS-14, R.

### Not included

Rented machines (Plan 54). Model loading time and anything inside ComfyUI. Changing what a person's ComfyUI has installed. New workflows.

## Existing work and decision

The measurements, the code traces and the independent review are in [inputs.md](inputs.md#planning-evidence). In short: nothing in today's path is slow because the work is hard; it is slow because every job repeats work whose answer has not changed, in new processes, with polling between them.

What this plan takes from Plan 54, drops and adds is listed in [inputs.md](inputs.md#plan-54-what-moves-here). The decision to design from the floor up, and to leave rented machines out, is the owner's (15 November 2026).

Smaller alternatives considered: caching inside today's path (Plan 54's local tasks; reaches one to four seconds); a direct socket to the worker that bypasses the Runtime is faster to build and leaves two doors (D3).

## Sequence and readiness

The owner's 16 November D9 follow-up replaces the GPU-gated sequence. The real-ComfyUI CPU floor is measured above. Next finish LS-2, write LS-3 from those numbers and the standing meter, then conduct the one RS1 design review on CPU/stand-in evidence. Later GPU findings may reopen a design finding, but do not hold this work. After RS1 the dependency order is **LS-4 → LS-8 → LS-15 → LS-7 → LS-10**.

Alongside, without waiting for RS1: LS-12, the safe cancellation and per-case work in LS-9, the code parts of LS-13 and LS-14, and the approved portions of LS-5 and LS-6. The exact LS-5 re-pin and LS-6 scope proposal remain proposals until the owner accepts them. Live GPU cells of LS-1, Windows-with-GPU measurement, live LS-14 proof and final R remain open; no incomplete code task is marked complete merely because it does not need a GPU.

A task is done only when its code and focused proof have landed and the standing meter demonstrates the relevant change on the stand-in or real CPU path. Calibration-test durations and artifact hashes are not speed evidence. Spend, publication and product-main promotion retain their owner gates. Plan 54 remains queued.

Task details are in [tasks.md](tasks.md). The owner's 15 November 2026 run authorization is recorded in [inputs.md](inputs.md#planning-evidence); its limits govern this run.

## Interfaces and handoff

**Developer pickup:** [Current branches, open issues, exact reproductions and next actions](developer-handoff.md). This guide preserves unresolved permission and meter failures; it does not waive proof or mark tasks complete.

**Consumes:** Release 13 as published (astrid-agent, VibeComfy and Runtime at the Release 13 pins); the test lane's attached-ComfyUI harness; Release 13's per-phase timing block; donor branches named in [inputs.md](inputs.md#source-identities).

**Produces:** a VibeComfy template interface (compile once, fill per job) and a held ComfyUI connection; a Runtime hand-off for local jobs; a resident worker in the pack host; a thin command-line client; a standing budget test that fails a pull request which adds a process start, a wait or a forced disk write to the warm local path. Plan 54 can reuse the worker and the template for rented machines.

## Completion

- The standing budget test passes on Linux and Windows against a stand-in ComfyUI: on the second job with the same key, no process is started, nothing sleeps or polls, the workflow is not compiled, each output byte is hashed once, and the number of forced disk writes before the reply is within the budget LS-3 sets. It also asserts a valid output and a job record.
- Live, on a GPU machine with a warm model: the targets in D1 are met for the default image workflow and reported for the default video workflow, on Linux and on Windows.
- Negative cases, each ending in the same typed result as today: ComfyUI restarted between jobs; a model removed; a node pack removed; the workflow edited; Astrid updated; the worker killed mid-job; two callers at once; a cancel.
- Limits: the numbers are for a warm model and a caller on the same machine. The first job after a change is slower by design and has its own target.
