# Inputs — Local speed

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner chose this scope on 15 November 2026 at about 10:45 UTC, relayed by the Release 13 orchestrator (session `session_011EzfW2L4ou5fDudzKLrc9d`) and recorded in the [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md): "we need the next release to get it very fast, RunPod is unimportant. Let's do a proper speed release after this one, focused on getting this as fast as possible. Think through it from first principles." The owner accepted the recommendation for each of D1 to D8 and all ten statements in the 15 November 2026 run-start message; see [Owner decisions](#owner-decisions).

**Prior art:** Measurements and code traces from Release 13 and [Plan 54](../54-warm-latency/inputs.md), plus five code readings and one independent review made for this plan on 15 November 2026 ([review.md](review.md)).

*Measured* (tester head `9acb55b60`, against a stand-in ComfyUI that answers instantly): a warm job takes 30.2 s (median); Release 12 takes 37.3 s. Command start to admission 17.0 s, admission to claim 0.4 s, claim to submit 11.4 s. Workflow emission runs three times (about 10 s); pack and registry scans about 8 s; pack files re-hashed on every schema lookup (3.2 s or more); 184 git processes on connect (1.8 s); one new Python process per task; 13 requests to ComfyUI.

*What ComfyUI needs and gives* (ComfyUI `6bfaacc`):
- Submitting validates synchronously and returns the job's identity (`server.py:1075-1139`). Validation walks the reachable graph and calls each node's own input rules (`execution.py:846-1091, 1128-1190`); model lists are cached on directory times (`folder_paths.py:471-518`). A custom node's own validation has no time bound.
- A websocket client receives start, cached, per-node, output and terminal events for its jobs; output events carry file name and folder, and are replayed when every node is cached (`execution.py:446-450, 565-577, 769-824`). The success event is sent before history is written; the event that follows history is `executing` with no node (`main.py:361-374`).
- The queue wakes on a condition, with no timer (`execution.py:1297-1314`).
- Nothing announces a restart, a new node pack or a changed model. An unknown node or a missing model is refused at submit with a typed error; a file that disappears later fails during execution with a typed event (`execution.py:1047-1079, 1146-1161`; `folder_paths.py:461-468`).
- Output events do not carry an absolute path. ComfyUI's own timer includes saving outputs and excludes queue wait (`main.py:349-377`).
- Global interrupt can stop another client's job; this version has a per-job cancel (`server.py:950, 1163`; `execution.py:1358`).

*What VibeComfy does per job* (VibeComfy `dba38f86`; astrid-agent `a91c35dfd`): loads and stages the bundle, emits and reloads a Python capsule, compiles for preflight and again for approval, rewrites output prefixes by re-emitting, polls history once a second, and fetches outputs through ComfyUI's view route (`local_job.py:90-138`; `local_server_engine.py:99-164, 214-337, 445-467`; `workflow_bundle.py:2749-2845`; `runtime/session.py:4200-4253, 4590-4600`). For a fixed graph, a second job differs only in literal values. No template interface exists; the approval record requires exact input equality and recompiles to defeat a forged record (`workflow_bundle.py:2003-2020`).

*What is resident today* (astrid-agent `a91c35dfd`): the Runtime and one pack host. The host starts one process per task, which gives a pinned pack source, a restricted environment and a killable scope (`generic_host.py:10612-10828`; `generic_host_worker.py`). Callers reach the host only through Runtime tasks; the SDK polls once a second (`sdk/invocation.py:3433-3457, 3637-3674`), and so does the idle host (`generic_host.py:14688`). Local execution changes process-wide environment and signal handlers (`local_server_engine.py:478, 577`), and the ComfyUI client allows one prompt per instance (`comfy_target.py:104, 267`).

*What the Runtime writes* (Runtime `6855dfa8`): SQLite in write-ahead mode at the default full synchronisation (`store.py:1198-1224, 1519-1535`); at least create, claim and settle as separate committed transactions, more with heartbeats; a stored output is a staged file forced to disk, linked into the store, and two directories forced (`cas.py:57-84, 155-174`). There is no request that waits (`server.py:1339-1421`) and none that records a finished job in one step; settlement requires a live claimed attempt (`service.py:8683-8723`).

*Callers* (astrid-agent `a91c35dfd`, astrid-app `d6ee9af2`): the command line is a new Python process per call that opens the Runtime each time (`core/generation/cli.py:730-742`); the agent tool server is resident but starts the command line for every call (`mcp_server.py:247-307`); agent skills tell agents to use the command line; the App creates tasks through the Runtime.

**Approach:** see [plan.md](plan.md#the-design). Alternatives compared: caching inside today's path (Plan 54's local tasks; reaches one to four seconds); a direct socket to the worker that bypasses the Runtime (two doors; D3); replying before the record is written (changes what success means; D2); returning ComfyUI's own file path (not today's result: the file is mutable and the caller has no stored, digested output). The chosen approach keeps the Runtime's existing steps and removes waits and repeats around them; a deeper Runtime change is conditional on LS-1.

**Challenge:** Reviewed — an independent Astra review of the starting hypothesis against the code ([review.md](https://github.com/banodoco/astrid-dev/blob/main/plans/55-local-speed/review.md)). Accepted from it: keep the Runtime's create, claim and settle and measure before redesigning; completion wakes on the history-ready event and reads history once; the output is fetched and hashed once, never handed over as ComfyUI's path; the resident worker is a separate supervised process because today's code changes process-wide state; the template needs a VibeComfy interface that keeps the approval record's protection; cancel by job only; a lost acknowledgement is never resubmitted; a two-step first spike. Left to the owner: D2, D4, D5, D6. The review's suggestion to keep per-job value checks was not taken, on the owner's bar that workflow validation stays only where there is a strong reason: ComfyUI validates every submission, so Astrid's check moves to template compile (see the keep list). Rejected: none.

**Proof and limits:** Completion is defined in [plan.md](plan.md#completion). Every time in the floor table is an estimate until LS-1 reports. The 30 s baseline was measured against a stand-in, not a real ComfyUI. Windows' slowest cases are unknown. The targets are medians for a small output on an idle queue; queue wait, large outputs and new inputs are reported, not promised.

**Review rounds:** Accepted — the owner's 15 November 2026 start message authorizes exactly one design stop, RS1 (one round), and one final round, R. Both have 0 rounds consumed. RS1 guards LS-4, LS-7, LS-8, LS-15, LS-9 and LS-10. Notify the owner when LS-3 is ready for review and when the completion PR is up.

**Run start:** Accepted — 15 November 2026 (Europe/Berlin), by the owner's own message in accountable manager session `chatgpt-workspace-6ee41b0f0cca/root`. This session answers for LS-1 to LS-15, RS1 and R finishing, follows astrid-dev → astrid-dev-manage, and owns this active plan. It may create branches and PRs, merge task PRs into `int/55-local-speed`, merge its own progress PRs on astrid-dev, and run each task's named CPU tests without asking. The first progress PR records this start and decisions; later progress PRs change tasks.md only. It must ask the owner before any product-repository main merge, any re-pin, any paid action (including GPU rental for LS-1 or LS-14), arranging a Windows tester for LS-13, any scope or decision change, and anything concerning publication of Release 14. A refused command is reported to the owner, never retried. Approved spend: zero. Advisor: no existing advisor session is attached; the configured judgment route will be commissioned for a genuine blocker. This manager was selected directly by the owner, with bounded task workers. Release 13 publication has been verified against the deployed manifest and its successful live canary; exact source identities are below. Without verified publication, only LS-1 and LS-2 would be allowed. Notify the owner when LS-1's measurements are in.

### Framing from the owner

Recorded from 15 November 2026, relayed by the Release 13 orchestrator (session `session_011EzfW2L4ou5fDudzKLrc9d`) at 10:45, 12:15 and 12:20 UTC and in the [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md).

- **The planning principle.** "Get rid of any nonsense unless there's a really strong reason, around validating the Comfy workflow." Every step on a warm job is deleted unless it names a concrete failure it prevents and its cost: [the keep list](#the-keep-list).
- **"Checks only when something changes"** means a change to what is installed or running: an add-on, a model, ComfyUI or Astrid installed, updated or restarted, or a pack or workflow edited. It never means request values: a new prompt or seed re-checks nothing.
- **Placement.** The resident helper is a general capability of Astrid core for long-lived pack sessions (start, supervise, restart, custody), used by the VibeComfy pack, with the ComfyUI connection and template logic in VibeComfy: D8.
- **Stages.** Under 2 s first, with [the time ledger](#the-time-ledger) showing what that needs; under 0.1 s after, confirmed by measurement: D1.

### Ten statements

Given to the owner by the orchestrator at 12:10 UTC on 15 November 2026. **Accepted in full by the owner on 15 November 2026**, with the exact qualifications below and D1 to D8. There are no contested statements.

1. Overhead is under 2 s in stage one; under 0.1 s is a measured stretch.
2. No program is started per job; one helper lives as long as ComfyUI does.
3. Push, not polling.
4. The workflow is prepared once; values are filled per job.
5. Heavy checks run only when the installation changes.
6. ComfyUI is the authority on node inputs.
7. Success still means saved and recorded, unless D2 says otherwise.
8. A standing local speed test runs on every build.
9. Rented-machine speed is out of scope.
10. The command line becomes a thin client; agents do not start a program per call.

Edges: a change made behind Astrid's back is caught only when ComfyUI refuses a job, restarts, or the installation changes (D6); an older ComfyUI may not be able to cancel a running job (D5).

Where the plan's wording is more exact than a statement: (2) the session lives until its pack or Astrid's installation changes; a ComfyUI restart renews the connection and re-reads the node list without ending the session. (1) Two independent estimates put an already-connected caller at 15 to 70 ms on Linux and 25 to 120 ms on Windows, so under 0.1 s is the design's aim and not only a hope; it stays unpromised until LS-1 measures it.

### Today's evidence

- **Rented machine, for context only** (Release 13 live rounds, 15 November): candidate A warm image job 215 s; candidate B with the first-tier fixes 153 to 156 s, of which about 50 s inside the machine's job is in no named phase and 31 s is collection ([Plan 54 inputs](../54-warm-latency/inputs.md)). The 50 s is the nearest measurement of what audits, node restore, dependency sync and doctor cost on a managed ComfyUI; it has not been split or measured locally.
- **A person's own ComfyUI:** the 30.2 s attribution by the test lane, in [the time ledger](#the-time-ledger).
- **Where Astrid repeats ComfyUI or itself:** the duplication survey and its two rules ("ComfyUI is the authority on what a node accepts; Astrid never refuses what ComfyUI would run"; "verify at a trust boundary once; inside a job, carry the digest"), merged in [pull request 659](https://github.com/banodoco/astrid-dev/pull/659).
- **Whether Plan 54 as written reaches under 0.1 s locally:** no; one to four seconds from caching alone, 0.2 to 2 s with a resident executor, held back by the Runtime's writes, the synchronous preview, the per-job process and one emission per job ([pull request 660](https://github.com/banodoco/astrid-dev/pull/660), with an independent Astra review that agreed). That answer is why this plan starts from the floor instead of from Plan 54.

### The keep list

The default is delete. A step stays on a warm job only if it names a failure it prevents. "When something changes" means install, update, a pack or workflow edit, a ComfyUI restart, or a refusal from ComfyUI. Costs marked * are estimates; the rest are measured on the stand-in (see the time ledger). LS-1 and LS-2 fill every estimate.

| Step today | Failure it prevents | Cost per warm job today | Verdict |
| --- | --- | --- | --- |
| Permission check on the request | Another program or user on the machine running jobs or reading results | about 1 ms* | **Keep**, once per connection plus a token per request |
| Create the task | A retried request running twice; no identity to cancel or record against | one committed write* | **Keep** |
| Claim by one executor | Two workers running the same job | one committed write* | **Keep** |
| Immediate lease renewal | Nothing, when the fresh lease already covers the job | one committed write* | **Delete**; renew only for long jobs |
| Working out the workflow, placement and settings | Running the wrong workflow or target | part of 17 s before admission | **Move** to when something changes; a lookup per job |
| Pack discovery and pack digests | Running a pack that was edited or corrupted after it was accepted | about 8 s | **Move**: verify when a pack is installed or updated and hold the result. Installed packs are not edited in place; a development checkout ends the session when its files change |
| Source identity by git (184 processes) | Connecting to a host built from different source | 1.8 s | **Move** to install and update |
| VibeComfy's graph and schema validation | A misspelt or renamed input silently ignored (ComfyUI accepts unknown input names); a wrong link type | inside emission and compile, about 10 s | **Delete per job.** Run once when the template is compiled, as a warning where ComfyUI would accept. ComfyUI itself checks classes, required inputs, link types, ranges, choices and each node's own rules on every submit |
| Reading ComfyUI's node list (4 times) | Compiling against a node set that has changed | small on the stand-in; a real list is megabytes* | **Delete per job**; read once per ComfyUI start, again after a refusal |
| Model presence check | Submitting a job whose model is missing | inside the above | **Delete**: ComfyUI refuses with a typed error, which is translated |
| Model content re-hash | A model file replaced by different bytes | off by default since Release 13 | **Stays off**; hash at download |
| Doctor | Starting a job on a broken installation | not measured locally | **Move** to install, update and after a failure. Astrid's own ComfyUI only |
| Installation audits (three per job) | A managed ComfyUI that has drifted from its lock | not measured locally | **Move** to when something changes. Astrid's own ComfyUI only |
| Node restore | Missing or wrong node packs in a managed ComfyUI | not measured locally | **Move**, as above |
| Dependency sync | Missing Python packages in a managed ComfyUI | not measured locally | **Move**, as above |
| Managed-engine preparation on a person's own ComfyUI | Nothing: there is nothing of ours to prepare | not measured | **Delete** |
| A new process per job | State leaking between jobs; running unpinned code | process start and imports, seconds | **Replace** with a session that lives exactly as long as its source is unchanged |
| Input file hashed and uploaded | ComfyUI reading a different file from the one the caller gave | proportional to size | **Keep**, once per file: named by content, skipped when present |
| Private output name per attempt | Collecting another job's file, or ComfyUI's cached earlier result | negligible | **Keep** |
| GPU state read before and after (two requests) | Nothing; it is diagnostic | about 2 ms* | **Delete** on success; read on failure |
| Polling for work, completion and result (three, each a second) | Nothing | up to 3 s | **Delete** |
| One history read; declared outputs present | Reporting success with a missing or wrong output | 1 to 8 ms* | **Keep** |
| Output fetched and hashed | The result changing after the reply (ComfyUI's file is mutable); no identity for the App and timeline | 1 to 8 ms per megabyte* | **Keep**, one pass |
| Output hashed again (four more passes locally) | A worker claiming a digest the bytes do not have | not measured | **Delete** all but one check at the store's boundary, if the store needs its own |
| Copy to the caller's folder | The caller having no file of their own | about 1 ms per megabyte* | **Keep** for the command line |
| Preview image before the reply | Nothing | not measured | **Move** after the reply |
| Log and evidence declarations on success | Nothing before the reply | not measured | **Move** after the reply |
| Settle: the record forced to disk | A reported success that is lost | 2 to 35 ms* | **Keep** (D2) |
| Forced disk write on create and claim | Nothing a waiting caller would not see as an error | part of the Runtime's writes* | **Delete if the Runtime can scope it**; LS-1 measures whether it matters |
| Version agreement | A new client talking to an old session | — | **Keep**, once per connection |

### The time ledger

The 30.2 s warm job on a person's own ComfyUI, measured by the test lane on `9acb55b60` against a stand-in. The four segments are exclusive and add up. The lines inside a segment come from a profiler and overlap (the re-hash runs inside emission and inside the scans), so they do not add up; LS-2 must produce exclusive times.

| Segment or line | Today | Measured? | Removed by | Left after | On the keep list? |
| --- | --- | --- | --- | --- | --- |
| **Command start to admission** | **17.0 s** | measured | | | |
| Emission, twice in the command | 6.6 s | measured | LS-4, LS-10 | 0; fill under 5 ms | fill only |
| Model registry twice, extension registry | 2.4 s | measured | LS-10, LS-15 | 0 | no |
| All 52 ready workflows loaded | 2.8 s | measured | LS-10, LS-15 | 0 | no |
| Source identity, 184 git processes | 1.8 s | measured | LS-10 | 0 | no |
| Interpreter, imports, connect process, the rest | about 3.4 s | by subtraction | LS-10 | 25 to 150 ms from the command line; 0 when connected | client start only |
| **Admission to claim** | **0.4 s** | measured | LS-7 | a few ms | create and claim |
| **Claim to submit, in the per-job process** | **11.4 s** | measured | | | |
| Finding the action entry | 4.2 s | measured | LS-8, LS-15 | 0 | no |
| Emission, third time | 3.5 s | measured | LS-4 | 0 | no |
| Pack files re-hashed on each schema lookup | 3.2 s or more | measured; overlaps emission | VibeComfy `e8f19340`, LS-4 | 0 | no |
| Model registry twice | 1.6 s | measured | LS-15 | 0 | no |
| Interpreter and imports of the per-job process | not split out | not measured | LS-8 | 0 | no |
| ComfyUI's node list, three reads; two compiles | small on the stand-in | not measured on a real ComfyUI | LS-15 | 0 | no |
| Managed-engine preparation | not split out | not measured | LS-15 | 0 | no |
| **Submit to result in the caller's hands** | **about 1.4 s** | by subtraction | | | |
| Completion poll, result poll | up to 1 s each | interval known, share not measured | LS-5, LS-7 | a few ms | one history read |
| Output passes, storage, record, preview, delivery | not split out | not measured | LS-6, LS-7 | 5 to 50 ms | fetch, one hash, record |

**For the first target, under 2 s:** the template (LS-4), the session (LS-8, LS-15) and the thin request (LS-10) remove about 28 s between them. The polls alone can then cost up to 3 s, so the held connection (LS-5) and the first half of the Runtime hand-off (LS-7) are needed too. Nothing else in the plan is required for under 2 s; the rest is for under 0.1 s, the first job and Windows.

**What LS-1 and LS-2 must measure before the scope is fixed:** exclusive times for the lines above; the per-job process's start and imports; managed-engine preparation on a person's own ComfyUI; the node list and submit validation on a real ComfyUI with a normal number of nodes and models; the Runtime's writes and forced flushes per job; the output passes; the same on Windows; and, for Astrid's own managed ComfyUI, the audits, node restore, dependency sync and doctor, which have only been measured on rented machines (about 50 s there, not yet split).

### Plan 54: what moves here

| Plan 54 task | Here |
| --- | --- |
| SP-10 compiled workflow reused; SP-28 incremental emission | Replaced by LS-4. With a template there is one emission per key, so incremental emission is not needed on the warm path |
| SP-13 completion by push; SP-32 progress to the caller | LS-5 |
| SP-14 read once, hash once; SP-35 failed fetch leaves nothing; thumbnail after the result | LS-6 |
| SP-15 no polling on the local path; durable-write budget | LS-7 |
| SP-25 one execution path (local half); local resident executor | LS-8 (core capability), LS-15 (the VibeComfy pack on it) |
| SP-24 errors translated; SP-31 unknown inputs are ComfyUI's to judge | LS-9 |
| SP-17 thin command line; SP-27 start-up hygiene | LS-10 |
| SP-12 inputs by content | LS-11 |
| SP-29 discovery fingerprint; SP-30 source identity | LS-12, off the critical path: they speed the first job, not the warm one |
| SP-9 workflow-scoped check; SP-33 one digest through the task child | Dropped for local: the check moves to the first job with a key, and the warm path has no task child |
| SP-1 to SP-8, SP-11, SP-18 to SP-23, SP-26, SP-34 | Stay in Plan 54 (rented machines) |

New here: the measured floor (LS-1), the fast-lane key and target generation (LS-3), resident sessions as a core capability (LS-8), the thin request with resolution on the resident side and the tool server in-process (LS-10), cancel by job only (LS-9), Windows as a budget of its own (LS-13).

Pull request 660 proposed staged local targets and a durability decision inside Plan 54; both are superseded by D1 and D2 here.

## Owner decisions

**Accepted — 15 November 2026, in the owner's run-start message.** D1 to D8 are each accepted as recommended. The operative decisions are below; the original options that follow remain as planning rationale, not pending decisions.

| Decision | Accepted choice |
| --- | --- |
| D1 | Commit to median overhead under 2 s for every caller on every system for the stated workload. Build for under 0.1 s for an already-connected caller, and promise it only once LS-1 has measured the floor. Report the slowest-in-twenty, retain the first-job targets, and measure the Windows CLI target before setting it. |
| D2 | Option (a): success means the output is stored and the result recorded on disk. Any change returns to the owner. |
| D3 | Every caller goes through the Runtime. |
| D4 | A Python CLI and an in-process agent tool server now; a native client requires a later owner decision based on measurements. |
| D5 | Require nothing of a person's ComfyUI. Use targeted cancel only where available; refuse a running cancel rather than use global interrupt. |
| D6 | Rely on ComfyUI's submission validation on the warm path and record the last target check. Same-name model replacement remains undetected. |
| D7 | Plan 54 is the rented-machine plan and queues behind Plan 55. No separate rented-machine speed work is included here. |
| D8 | Astrid core provides the resident-session capability to packs, with VibeComfy as its first user. Build only what that first user needs; ComfyUI-specific logic stays in VibeComfy. |

- **D1 The targets.** Median Astrid overhead for a one-megapixel image on an idle queue. Stage one: under 2 s for every caller on every system. Stage two: under 0.1 s for an already-connected caller; under 0.25 s from the command line on Linux and macOS, Windows' command-line target set after LS-1 measures it. Throughout: under 3 s (5 s on Windows) for the first job after a start or change. Resolved by the accepted choice above. Original recommendation: commit to stage one; build for stage two and promise it once LS-1 has measured the floor; medians, with the slowest-in-twenty reported.
- **D2 What success means.** (a) As today: a reply means the result is stored and recorded on disk; the forced writes are grouped. Estimated 15 to 70 ms on Linux, 25 to 120 ms on Windows. (b) The record survives Astrid crashing but not a power cut in the following second. (c) Reply first, record after: faster, and a caller can hold a result the record does not yet have. Recommendation: (a), and revisit only if LS-1 shows Windows missing D1.
- **D3 One door.** Every caller goes through the Runtime (recommended), or a direct connection to the worker for the SDK and command line. The direct door is quicker to build; the App would not use it, and permissions and the record would have two paths.
- **D4 The command line.** Agents use the command line, so it is the commonest caller. A Python client costs 25 to 150 ms to start on Linux and 80 to 500 ms on Windows; a small native client costs 3 to 20 ms and 10 to 60 ms, and is another thing to build, sign and update. Recommendation: Python client and the in-process tool server now; decide on a native client from LS-1's Windows numbers.
- **D5 The person's ComfyUI.** Require nothing of it: no extension, and features such as per-job cancel used where the version has them (recommended). On an older ComfyUI a running job then cannot be cancelled, only a queued one, because the only alternative can stop someone else's work. Alternative: a small optional extension that gives exact restart detection, cancel and duplicate protection.
- **D6 Trust in the person's ComfyUI on the warm path.** Astrid stops re-reading the node list every job and relies on ComfyUI to refuse what it cannot run; the record says when the target was last checked. A model file replaced under the same name is not detected, as today. Recommendation: accept.
- **D8 Where the resident session lives.** The owner's instinct (15 November 2026, relayed by the orchestrator at 12:15 UTC): a general capability Astrid core provides to packs (a pack declares it needs a long-lived session; core supervises and fences it), used first by the VibeComfy pack, with the ComfyUI connection and template logic in VibeComfy. The plan now does this (LS-8 core, LS-15 the pack, LS-4 and LS-5 in the VibeComfy package). The first draft described the helper as specific to local ComfyUI jobs. Alternative: build it inside the VibeComfy pack only, which is a little quicker and leaves every later pack to reinvent supervision. Recommendation: the owner's instinct, built for its first user only. Confirmed by the owner in the accepted choice above.
- **D7 Plan 54.** It becomes the rented-machine plan and queues behind this one. Any rented-machine speed work between Release 13 and this release is dropped unless it is also a donor here. Recommendation: yes.

## Source identities

### Run-start source identities

Release 13 is published. Its brief still says Draft / Not pinned, so that stale label was not used as the publication authority. The deployed [App manifest at `d7d48cfe3891d490b740e017081ae558970cd56e`](https://github.com/banodoco/astrid-app/blob/d7d48cfe3891d490b740e017081ae558970cd56e/public/install-manifest.json) specifies release 13, and [served-manifest canary 43760624263](https://github.com/banodoco/astrid-app/actions/runs/43760624263/job/132954388685) succeeded against that deployment on 15 November 2026. These are the starting product commits, not donor heads or the current main tips:

| Repository | Published Release 13 commit |
| --- | --- |
| astrid-agent | `9814193a73f606719e81883a8be197d27dd361d4` |
| VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` |
| astrid-runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` |

Plan read: all four requested files at `91035254`. Recording base: astrid-dev main `1e1c646ea428bfd022adc024bbc25bc08078ef93`; the four plan files were unchanged. Each changed product repository's integration branch is `int/55-local-speed`, based on its published commit above. Task PRs target it, and a draft PR from it to main opens when its first task lands. Progress stays on astrid-dev main through progress PRs; product-main promotion and re-pins still require the owner. No Release 14 publication action is authorized.

### Planning and donor identities

Planning read: astrid-agent `a91c35dfd` (Release 13 candidate A), VibeComfy `dba38f86`, Runtime `6855dfa8`, ComfyUI `6bfaacc`, astrid-app `d6ee9af2`. Base for code work: Release 13 as published, recorded at run start. Donors, to be checked against the published base: astrid-agent `r13/machines-wa-life` (repeat checks removed on a warm engine), `r13/machines-p3split` (named timing), `abef725c1` (in-process entry check), VibeComfy `e8f19340` (schema lookup memo). Rented-only branches (`r13/machines-wb-dispatch`, `r13/machines-p6obs`) are not donors.

## References

- [Independent review](review.md)
- [Windows tester report, 15 November 2026](https://github.com/banodoco/astrid-dev/issues/651): the first measurements on a person's Windows computer (RTX 4080 SUPER, one-megapixel turbo image): 157 s cold, 42 s with the model loaded, 178 s for an edit; the task host took 205 s to start because a rendering check hashed 21,545 files, now moved to the first render
- [Plan 54 inputs](../54-warm-latency/inputs.md): the rented-machine measurements, the duplication survey and the earlier local estimate
- [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md)
