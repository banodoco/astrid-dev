# Inputs — Local speed

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner chose this scope on 15 November 2026 at about 10:45 UTC, relayed by the Release 13 orchestrator (session `session_011EzfW2L4ou5fDudzKLrc9d`) and recorded in the [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md): "we need the next release to get it very fast, RunPod is unimportant. Let's do a proper speed release after this one, focused on getting this as fast as possible. Think through it from first principles." The targets and the points in [Owner decisions](#owner-decisions) are not yet decided.

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

**Challenge:** Reviewed — an independent Astra review of the starting hypothesis against the code ([review.md](https://github.com/banodoco/astrid-dev/blob/main/plans/55-local-speed/review.md)). Accepted from it: keep the Runtime's create, claim and settle and measure before redesigning; completion wakes on the history-ready event and reads history once; the output is fetched and hashed once, never handed over as ComfyUI's path; the resident worker is a separate supervised process because today's code changes process-wide state; the template needs a VibeComfy interface that keeps the approval record's protection; cancel by job only; a lost acknowledgement is never resubmitted; a two-step first spike. Left to the owner: D2, D4, D5, D6. Rejected: none.

**Proof and limits:** Completion is defined in [plan.md](plan.md#completion). Every time in the floor table is an estimate until LS-1 reports. The 30 s baseline was measured against a stand-in, not a real ComfyUI. Windows' slowest cases are unknown. The targets are medians for a small output on an idle queue; queue wait, large outputs and new inputs are reported, not promised.

**Review rounds:** Pending — recommended: one stop after the design (RS1, one round) and one final round. RS1 protects LS-4, LS-7, LS-8, LS-9 and LS-10 from being built on a wrong approval rule, hand-off or crash rule. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run after Release 13 publishes, record the date, the tasks it covers, the accountable session, what it may do without asking, and the advisor session.

### Plan 54: what moves here

| Plan 54 task | Here |
| --- | --- |
| SP-10 compiled workflow reused; SP-28 incremental emission | Replaced by LS-4. With a template there is one emission per key, so incremental emission is not needed on the warm path |
| SP-13 completion by push; SP-32 progress to the caller | LS-5 |
| SP-14 read once, hash once; SP-35 failed fetch leaves nothing; thumbnail after the result | LS-6 |
| SP-15 no polling on the local path; durable-write budget | LS-7 |
| SP-25 one execution path (local half); local resident executor | LS-8 |
| SP-24 errors translated; SP-31 unknown inputs are ComfyUI's to judge | LS-9 |
| SP-17 thin command line; SP-27 start-up hygiene | LS-10 |
| SP-12 inputs by content | LS-11 |
| SP-29 discovery fingerprint; SP-30 source identity | LS-12, off the critical path: they speed the first job, not the warm one |
| SP-9 workflow-scoped check; SP-33 one digest through the task child | Dropped for local: the check moves to the first job with a key, and the warm path has no task child |
| SP-1 to SP-8, SP-11, SP-18 to SP-23, SP-26, SP-34 | Stay in Plan 54 (rented machines) |

New here: the measured floor (LS-1), the fast-lane key and target generation (LS-3), the thin request with resolution on the resident side and the tool server in-process (LS-10), cancel by job only (LS-9), Windows as a budget of its own (LS-13).

Pull request 660 proposed staged local targets and a durability decision inside Plan 54; both are superseded by D1 and D2 here.

## Owner decisions

- **D1 The targets.** Proposed: median Astrid overhead for a one-megapixel image on an idle queue, under 0.1 s for an already-connected caller on every system; under 0.25 s from the command line on Linux and macOS, Windows' command-line target set after LS-1 measures it; under 3 s (5 s on Windows) for the first job after a start or change. Alternative: a slowest-in-twenty target instead of a median, which is stricter and may not be reachable on Windows. Recommendation: medians, with the slowest-in-twenty reported.
- **D2 What success means.** (a) As today: a reply means the result is stored and recorded on disk; the forced writes are grouped. Estimated 15 to 70 ms on Linux, 25 to 120 ms on Windows. (b) The record survives Astrid crashing but not a power cut in the following second. (c) Reply first, record after: faster, and a caller can hold a result the record does not yet have. Recommendation: (a), and revisit only if LS-1 shows Windows missing D1.
- **D3 One door.** Every caller goes through the Runtime (recommended), or a direct connection to the worker for the SDK and command line. The direct door is quicker to build; the App would not use it, and permissions and the record would have two paths.
- **D4 The command line.** Agents use the command line, so it is the commonest caller. A Python client costs 25 to 150 ms to start on Linux and 80 to 500 ms on Windows; a small native client costs 3 to 20 ms and 10 to 60 ms, and is another thing to build, sign and update. Recommendation: Python client and the in-process tool server now; decide on a native client from LS-1's Windows numbers.
- **D5 The person's ComfyUI.** Require nothing of it: no extension, and features such as per-job cancel used where the version has them (recommended). On an older ComfyUI a running job then cannot be cancelled, only a queued one, because the only alternative can stop someone else's work. Alternative: a small optional extension that gives exact restart detection, cancel and duplicate protection.
- **D6 Trust in the person's ComfyUI on the warm path.** Astrid stops re-reading the node list every job and relies on ComfyUI to refuse what it cannot run; the record says when the target was last checked. A model file replaced under the same name is not detected, as today. Recommendation: accept.
- **D7 Plan 54.** It becomes the rented-machine plan and queues behind this one. Any rented-machine speed work between Release 13 and this release is dropped unless it is also a donor here. Recommendation: yes.

## Source identities

Planning read: astrid-agent `a91c35dfd` (Release 13 candidate A), VibeComfy `dba38f86`, Runtime `6855dfa8`, ComfyUI `6bfaacc`, astrid-app `d6ee9af2`. Base for code work: Release 13 as published, recorded at run start. Donors, to be checked against the published base: astrid-agent `r13/machines-wa-life` (repeat checks removed on a warm engine), `r13/machines-p3split` (named timing), `abef725c1` (in-process entry check), VibeComfy `e8f19340` (schema lookup memo). Rented-only branches (`r13/machines-wb-dispatch`, `r13/machines-p6obs`) are not donors.

## References

- [Independent review](review.md)
- [Plan 54 inputs](../54-warm-latency/inputs.md): the rented-machine measurements, the duplication survey and the earlier local estimate
- [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md)
