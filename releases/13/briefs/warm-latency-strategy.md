# Warm-job latency: strategy

**Asked by Hannah, 14 Nov 2026:** understand and eliminate every level of the delay on a warm job; "the goal is that it should be almost 0 s". **Lead:** the Release 13 advisor. **First implementation lane:** machines, card `r13/machines-warm`. Written 23:30 UTC Sat; revised as evidence lands.

## The evidence
Live, build 6a6ab6f4d, RTX 5090, the same image model run back to back. The second job took **219 s**. ComfyUI itself reported **2.88 s**. The engine was reused, nothing was loaded or hashed, and GPU memory did not move. So about 216 s is overhead:

| Where | Seconds | Covered by a phase today |
|---|---|---|
| Outside every host phase | ~30 | no |
| Host preparation | 17 | yes |
| Before the pod job starts | ~42 | no |
| Pod: prepare to align | ~51 | partly |
| Pod job, in no phase | ~42 | no |
| Pod job phases (incl. the 2.9 s) | 13 | yes |
| Tail | ~7 | no |
| Collection of one PNG | 47 | yes |
| Release | 21 | yes |

Two thirds of the time is in steps nobody had named. That is the first finding: the delay hid because nothing required the phases to add up.

## Working explanation (to be confirmed by the deep-dives)
The warm path is the cold path run again. Each job starts new processes on the pod, re-derives and re-checks facts that were settled when the pod was claimed, talks to the pod through many separate remote commands with polling between them, and makes the caller wait for clean-up before it gets its result. No single step is slow; there are many of them, in series, each with a round trip.

Four structural causes:
1. **Facts are checked per job that are true per claim.** Install integrity, alignment, engine health, source identity.
2. **The pod has no resident worker for jobs.** Every job pays process start-up and imports, then rediscovers the engine that is already running.
3. **Transport is per step.** Each step is a remote command or a detached job that is polled; latency multiplies by the number of steps.
4. **The result waits for housekeeping.** Collection goes the long way round, and release and reset finish before the caller hears back.

And one meta cause: **no budget.** Nothing counts round trips or asserts that timed phases cover the wall time, so a new step costs nothing to add.

## The plan
**1. Instrument first (tonight).** One clock on the host from command start to result printed; pod phases nested inside the host's execution interval; an explicit `unaccounted` remainder. P3 (`timing.v2`, 916a654d8) is the candidate; the tail deep-dive says what it still misses. Plus a CPU harness on the existing fake pod that counts remote round trips and process starts for a warm job and fails over a budget. This is what stops the delay coming back.

**2. Understand each area (tonight; three Astra deep-dives, Luna helpers as needed, and machines' own per-gap note as first evidence).** Host and transport; pod side; collection, release and the instrument. Each returns the ordered steps of a warm job, the round trips, what is per claim and not per job, and the structural reason.

**3. Fix in two tiers.**
- **For Release 13 (target: under 30 s of overhead on a warm job, ideally under 10 s):** skip per-claim checks when the claim already holds a matching prepared record; return the result before release and reset; fetch outputs in one round trip; fast polling (P4, merged). Each card carries a round-trip budget test.
- **After Release 13 ("almost 0 s"):** a resident job service on the pod, so a warm job is one request: send the workflow and inputs, get the result. Checks move to claim time by construction. A plan of its own.

**4. Verify live.** The orchestrator repeats the same run (image ×3, video edit ×2, image again) and posts the four numbers per job. Done means the table above with every row named and the total within target.

## Rules for this work
- Custody and money bounds do not move: nothing here extends a claim or skips release; release only stops blocking the result.
- A fix without a budget test is not finished.
- One lane writes code (machines). The advisor and reviewers read.

---

# Design and cards (00:10 UTC Sun 15 Nov)

**Target set by Hannah (23:16 Sat):** overhead on a warm same-model job under 5 s for Release 13; under 0.5 s as a follow-up. She approved the per-claim attestation.

Sources: machines' findings note (G1 to G6) and four Astra reviews of compose ee14644a (host and transport; pod side; collection, release and the instrument; the direct route). Nothing below is measured except the table at the top.

## What a warm job does today
- **Before the pod is touched:** 7 or more provider calls (liveness, inventory, machine, GPU catalogue, rate) and four git processes, per job. Runtime admission, with 1 s pickup and status polls.
- **Preparation:** 5 remote commands and a file read to re-confirm a pod that has not changed.
- **Dispatch:** a directory, then each file uploaded and separately checksummed, then a start: about 12 operations. Every operation opens and closes its own connection through RunPod's proxy.
- **On the pod:** four Python starts before generation, including a full catalogue listing. Then three complete installation audits (18 git processes and four environment probes each, importing torch), two model-verification passes, node restore, dependency preparation and doctor, with nothing to change.
- **After generation:** six more Python starts to declare logs; the host fetches each file one at a time, re-verifies the installation, runs a reset job and waits for it, then publishes to the Runtime, and the caller's side hashes the output five times.

None of this is slow by itself. It is the cold path, repeated, in series, over a transport that pays a connection per step.

## Tier 1: what machines builds now (one lane, three workers)
| Card | What | Removes |
|---|---|---|
| W-A | Per-claim attestation, as a set of attested workflow requirements (in flight) | The pod-side audits, the preparation status check, the collection-time re-verification |
| W-B | One dispatch bundle (one upload, one start); one verified output bundle; log declarations in one process (in flight) | About 10 dispatch operations, N file fetches, five Python starts |
| W-C | Result first, reset after, behind the existing `ready` gate; a reset failure fences the lease at the next start as today | 21 s from the caller's wait |
| W-D | Validate the selected entry only; no catalogue listing on the pod | One CLI cold start |
| W-E | One connection held for the job, not one per operation | A proxy handshake per operation |
| W-F | Polls at 0.2 s: host pickup, caller status, ComfyUI history | Up to 3 s |
| W-G | On an attested claim, one liveness call; identity, GPU and rate facts cached for the claim | 6 or more provider calls |
| W-H | The instrument: P3 plus a pod whole-job span, the caller's clock started at process entry, and a budget test on `machine_case` with one shared counter of remote operations and process starts | Lets none of this come back |

**Expected result: about 30 to 45 s of overhead** (my estimate from the step counts; unmeasured). It cannot reach 5 s: one pod-side Python start and import, the Runtime round trips and the remaining operations are several seconds each.

## Tier 2: under 5 s. The direct route
Once a claim is attested, a later job with attested requirements does not go through the pod's Astrid at all. The host compiles the workflow and talks to the pod's ComfyUI directly: upload inputs, submit, watch, download. The channel exists: the authenticated engine endpoint through the pod agent (`astrid/core/generation/engine_endpoint.py`, `engine_transport.py`; the lifecycle's engine bridge), tested but not used by the pod path (`packs/runpod/adapter.py:5`). No bundle, no pod process, and no pod Runtime state to reset.

What must still hold, and how:
- **Lease, cost and deadline checks, the invocation fence, idle timers:** unchanged, on the host. The watchdog deadline update is today a Python command on the pod; it needs an acknowledged update through the agent.
- **Requirements:** the host compares the workflow's requirements with the attested set. Anything new takes the full path.
- **Logs and receipts for every generation:** the host writes the job record and reads the engine log slice through the agent.
- **Cancellation and containment:** as the attached path does it; never resubmit after an uncertain acceptance.
- **Clean-up:** inputs and outputs for that prompt, through the agent, after delivery.

Astra's verdict, which I share: under 5 s is plausible for small outputs; twelve hours is credible for a prototype, **not for a safe release**, because it changes custody paths (watchdog, fences, cancellation) that this release has refused to ship unproven. Estimate: 8 to 12 product files, a lifecycle-agent change, and at least one live round.

## Tier 3: under 0.5 s
A pooled connection, completion events over a websocket (the bridge refuses upgrades today), compiled workflows and schema cached per claim, the output streamed in the same exchange, and settlement and delivery that hash once. A plan of its own, after Tier 2 is measured.

## Honest answer on the cutoff
- **By 13:00 UTC Sunday:** Tier 1, measured live. Roughly a sixfold improvement, to about 30 to 45 s.
- **Under 5 s:** not safely by 13:00. A prototype behind a setting by Sunday night is realistic; proven and reviewed, Monday or Tuesday.
- **Hannah's choice:** move the cutoff until Tier 2 is proven, or ship Tier 1 in Release 13 and Tier 2 as the next release within days.

---

# Revision (00:40 UTC Sun): Tier 2 goes through Astrid, and a third horizon

## Tier 2, revised: a resident Astrid job service on the pod
Hannah asked whether Tier 2's outcome can be had without bypassing Astrid. It can, and it is the better design; **the direct route above is dropped.**

A job service starts once when the claim is attested. It holds the verified state and the compiled schema in memory, takes each job in one exchange over the existing engine endpoint proxy (pointed at the service's loopback port; no agent change), runs it in process, and returns the result and its evidence in the same exchange.

- **One job path:** the same compile, validation, job record, evidence and settlement as today, without the process starts and re-audits.
- **Custody stays put:** fence, deadline and watchdog checks remain pod-side and in process. New risks are a stale long-lived process (the attestation's incarnation check covers it) and a crash (fall back to the full path).
- **Two round trips per job** against six to ten for the direct route. Expected overhead 2 to 4 s (estimate).
- **Supervision:** extend the existing engine supervisor; do not add a second custodian.
- **Open choice:** if the pod's Runtime stays in the job path, the reset stays (off the caller's wait after W-C). If the service settles straight to the host, there is nothing to reset.
- **Time to proven:** 2 to 2.5 days. Not by the Sunday cutoff.

**First CPU test,** on `machine_case`: after one full job attests the claim, a second job with the same requirements issues at most three remote operations, starts zero pod processes, runs zero audit commands, and returns a result carrying the job record and timing. Fail-closed cases forcing the full path: supervisor restarted; new workflow requirement; service not answering; attestation absent or corrupt.

## Which placements pay what
| Cost on a warm second job | RunPod | Local-managed | Attached |
|---|---|---|---|
| Installation audits ×3, node restore, dependency preparation, doctor, model verification ×2 | yes | yes (same code) | no |
| Provider calls, dispatch, pod process starts, catalogue listing, per-file collection, reset | yes | no | no |
| 1 s polls (pickup, status, ComfyUI history); Runtime publication; five hash passes on delivery | yes | yes | yes |
| Schema fetched and workflow compiled twice in preflight | yes | yes | yes |
| The caller's own process start | yes | yes | yes |

So the attestation (W-A) must be keyed on supervisor incarnation and install identity, with the claim id as an extra field when there is one, or local-managed keeps the largest block.

## Third horizon: local overhead under 0.1 s
For a warm same-model job on local-managed or attached, after Tier 1. Seconds are estimates.

| Remaining cost | Today | Design | After |
|---|---|---|---|
| Caller's process start and imports | 0.5 to 2 s for the CLI | Callers that matter are already running (the agent's MCP server, the SDK, the App). The CLI becomes a thin client of the running host over a local socket, with lazy imports | 0 for resident callers; about 0.1 s for the CLI, which is the floor for a Python process |
| Admission and pickup | up to 1 s of polling, twice | The host is told of the task and the caller of the result by push, on the same local connection | under 10 ms |
| Schema fetch and compile | 0.2 to 1 s, done twice | Cached per engine incarnation and workflow digest; a job binds inputs to a compiled graph | under 5 ms |
| Input upload | per input, every job | Skip when the engine already holds that content (by digest) | 0 for repeats |
| Completion | 1 s history poll | ComfyUI's websocket pushes completion | milliseconds |
| Evidence and prompt clean-up | three stats calls and three queue calls before returning | After the result is returned | 0 on the caller's wait |
| Output read, publication, delivery | read, then about five hash passes and copies | One read, one hash, published by link, delivered by link | 10 to 30 ms for an image |

Total for a resident caller: roughly 40 to 80 ms for an image.

**Cards, after Release 13, in order of seconds removed:**
1. L1: schema and compile cache per engine incarnation.
2. L2: completion by websocket.
3. L3: push for admission and result; no polling on the local path.
4. L4: hash once; link, not copy.
5. L5: evidence and clean-up after the result.
6. L6: thin CLI over the local socket.
7. L7: input reuse by digest.

L1, L2 and L4 also serve the pod service and are the route from Tier 2 to under 0.5 s there.

**The budget test for "under 0.1 s local overhead":** a resident host and a fake ComfyUI that completes instantly and announces it over a websocket. Run one job to warm, then assert on the second:
- no sleep and no poll (a fake clock that fails if anything waits);
- no `/object_info` request and no compile;
- at most three engine requests (optional upload, submit, output read);
- each output byte hashed exactly once (an instrumented hasher);
- no process started;
- and, as a secondary check, median overhead under 100 ms over twenty runs.

Counts are the gate; the time is the witness. Counts do not flake.
