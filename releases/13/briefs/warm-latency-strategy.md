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
