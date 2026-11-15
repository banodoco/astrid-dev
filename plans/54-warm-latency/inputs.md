# Inputs — Generation speed

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Accepted — the owner chose this scope on 14 and 15 November 2026; her decisions are in the [Release 13 decision log](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/decisions.md) and listed under [Owner decisions](#owner-decisions). They were relayed by the Release 13 orchestrator (session `session_011EzfW2L4ou5fDudzKLrc9d`) to the advisor between about 22:40 and 23:50 UTC and recorded in `releases/13/decisions.md` on branch `r13-progress/decision-log`. Release 13 keeps its cutoff and ships the first tier; "put all the rest onto a speed-focused follow-up plan in astrid-dev, with context on everything else." See [Owner decisions](#owner-decisions).

**Prior art:** The live measurement ([timing table](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/evidence/live/p1-timing.md)), the code reviews summarised in the [strategy note](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/briefs/warm-latency-strategy.md), and the findings below.

*The measurement.* `releases/13/evidence/live/p1-timing.md` (`r13-progress/decision-log`, d6384df), build 6a6ab6f4d, RTX 5090:
- Warm same-model image jobs: 242 and 261 s wall for 2.88 and 3.01 s in ComfyUI. Preparation 17 to 18 s, execution 104 to 121 s, collection 47 s, release 21 to 22 s, 52 to 53 s outside every host phase. Of execution, 91 to 108 s is in no pod phase: 42 to 49 s before the pod job starts and about 40 s inside it.
- The engine was reused, nothing was loaded or hashed, and GPU memory did not move.
- First job on a fresh machine with a warm model volume: 13m49s.
- Video: the first edit paid a one-time load of about 50 GB (211 s in ComfyUI); the second was warm (70 s in ComfyUI) with about 300 s of overhead.
- Model switch: an image job after video reloaded the image model (62 s in ComfyUI).

*Where the time goes* (the machines manager's per-gap note G1 to G6 on compose `ee14644a4`; four independent code reviews of the same commit; summarised in `releases/13/briefs/warm-latency-strategy.md`). Per warm job on a rented machine:
- Seven or more provider calls and four git processes before the machine is touched; five remote commands and a file read to re-confirm it.
- About twelve operations to dispatch: a directory, each file uploaded and separately checksummed, a start (`astrid/packs/runpod/machine.py:865-938`). Each remote operation opens its own connection through the provider's proxy (`astrid/packs/runpod/remote_placement.py:1036-1054`).
- On the machine: four Python starts including a full catalogue listing (`machine.py:431-449`); three installation audits of 18 git processes and four environment probes each, two model-verification passes, node restore, dependency preparation and doctor, with nothing to change (`astrid/core/generation/managed_preparation.py:414-857`; `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py:189-214`).
- After generation: five Python starts to declare logs and one for the output manifest (`machine.py:456, 468`); one fetch per file; an installation re-check (`machine.py:1081, 1224`); a reset the caller waits for (`machine.py:1510, 1581`; `astrid/packs/runpod/pod_reset.py:287-329`); Runtime publication; several hash passes on delivery (`astrid/core/generation/delivery.py:103-174`, `astrid/sdk/media_open.py:153, 394`, `astrid/sdk/media_views.py:50-82`).

*Which placements pay what.*

| Cost on a warm second job | Rented | Astrid-managed local | Person's own ComfyUI |
|---|---|---|---|
| Installation audits, node restore, dependency preparation, doctor, model verification | yes | yes (same code) | no |
| Provider calls, dispatch, machine process starts, catalogue listing, per-file collection, reset | yes | no | no |
| One-second polls (pickup, status, ComfyUI history); Runtime publication; repeated hashing on delivery | yes | yes | yes |
| Schema fetched and workflow compiled twice in preflight (`astrid/packs/vibecomfy/local_server_engine.py:142, 219`) | yes | yes | yes |
| The caller's own process start | yes | yes | yes |

*Lean on ComfyUI* (independent review of ComfyUI at `6bfaacc`, VibeComfy at `dba38f86` and the Agent at `ee14644a4`):

| Step | ComfyUI does | Astrid adds | Needed on a warm job? | Leaner design |
|---|---|---|---|---|
| Graph validation | Validates classes, inputs, links, types, ranges and choices on submit and returns typed errors (`execution.py:846-1238`) | Fetches the whole `/object_info` (megabytes; ComfyUI rebuilds it per request, `server.py:754-814`) 3 times and compiles 9 times per job end to end (measured), each for a different stage of the workflow | Only its policy: refusal codes and guidance | Ask per node class (`server.py:816-822`) and per model folder (`server.py:342`); reuse the compiled projection; on a paid, warm engine submit and map ComfyUI's errors |
| Models | Lists files, keeps models resident, evicts on demand (`comfy/model_management.py:893-983`) | Digest pinning and verification | Identity, yes; re-verification, no | Verify on acquisition or change; keep the record |
| Node caching | Skips unchanged nodes between prompts (`comfy_execution/caching.py:102-127`) | Uploads inputs under `astrid/{task_id}` (`astrid/core/generation/backends/comfy_target.py:327`), so an identical input looks new and its descendants re-run | Attribution of outputs, yes | Name inputs by content; keep per-attempt output prefixes |
| Inputs | Reads its input folder; de-duplicates only after an upload | An HTTP upload per input per job, even on the same disk | Custody of bytes, yes | On a shared filesystem stage by link or copy into the input folder; skip when the content is already there |
| Outputs | Writes files and reports them in history | Download, hash, temp copy, publication, further hash passes: 3 on the rented path and 5 locally (measured) | Receipts and custody, yes; the repeats, no | Read once, hash once into the store; keep delivery copies independent of the store's file |
| Installation | Loaded node classes at start-up | Source, lock and environment attestation | A receipt, yes; a re-audit, no | Verify on mutation; a node receipt |
| Completion | Websocket events (`server.py:269-290`; `execution.py:496, 577, 824`) | Polls history every second (`vibecomfy/runtime/session.py:4200, 4236`) | Completion, yes | Subscribe before submit; keep a poll as fallback |

Limits of leaning on ComfyUI, which bound the design: it can queue the valid branches of a graph while reporting errors on others (`server.py:1115-1139`), so an optimistic submit must treat any reported error as a failure; a missing node class is reported without saying which pack provides it; a person's own ComfyUI exposes no restart signal (`/system_stats` has versions only, `server.py:689`) and its model list changes without a restart (`astrid/core/generation/asset_gaps.py:475`).

*Negative findings and constraints carried from Release 13.*
- A cross-job schema cache is unsafe as first proposed: live preflight uses model choices (`local_server_engine.py:170`) that change without a restart, and a person's ComfyUI gives no trustworthy incarnation. It needs a revision signal or a cheap freshness probe. Release 13 takes only "fetch and compile once per job".
- Moving evidence and clean-up after the result is custody-adjacent: evidence including the final `/system_stats` is recorded before settlement (`astrid/core/generation/job_evidence.py:89`), the prompt is drained before the engine lock is released (`managed_preparation.py:350`), and a clean-up failure latches uncertainty (`astrid/core/execution/generic_host.py:13825`).
- **There are no "two identical fetches" to merge** (cells' probe, 15 November). The first preflight compiles the original workflow; approval recompiles after private output prefixes and the media upload, which is a different workflow; the pinned Runtime then refreshes `/object_info` and recompiles before queueing to verify the approved projection. Measured: 3 schema requests and 9 graph compilations per job end to end. Reducing them needs a defined proof of "same workflow, same schema", not a cache.
- **Hash-once is not a local change** (cells' probe, 15 November). Output bytes are hashed 3 times on the rented path and 5 times locally, and the Runtime hashes publication and reads independently. Hard-linking a delivery to the Runtime's stored file would let a caller's edit corrupt durable bytes, which a test pins as a contract. Hash-once needs a change to the Runtime's integrity boundary and a Runtime pin.
- **Input reuse has a safe subset, which Release 13 takes:** skip the upload only when the content-named file is already present at the right size; otherwise upload with overwrite off; and if a file of that name exists at the wrong size, fall back to the per-task name and never repair the shared file, because ComfyUI's overwrite truncates in place.
- The engine endpoint addresses one port (`astrid/core/generation/engine_endpoint.py:346, 407`); requests have 15 and 25 second limits and close their connection (`astrid/core/generation/engine_transport.py:21, 27, 179`); the bridge refuses websocket upgrades (`engine_transport.py:319`).
- The engine supervisor holds one engine and transient command handles (`astrid/core/generation/engine_custody.py:1146`).
- No record exists that node packs were installed correctly: the install receipt holds recipe, model and health evidence only (`astrid/core/generation/engine_runner.py:909-940, 1017-1021`).

**Approach:** see [plan.md](plan.md#existing-work-and-decision). For Phase 1, three shapes were compared and none is yet chosen for build. Doing less (stopping at the first tier) was put to the owner and declined: D1.

**Challenge:** Reviewed — three independent passes checked this plan against the code; the stopped design is recorded in the [resident-host note](https://github.com/banodoco/astrid-dev/blob/r13-progress/decision-log/releases/13/briefs/warm-tier2-resident-host.md). A critique was required: the plan touches custody, release and cross-repository contracts. The advisor wrote the plan and is the standing critic; the orchestrator ruled that the advisor's critique counts, with independent passes checking claims against the code. Three passes were run and are reflected in this pack.
- *Check of the first draft.* Verdict: do not greenlight unchanged. Corrected citations; found the endpoint and supervisor claims overstated; found the simpler reuse of the machine's resident host; found missing tasks (watchdog publication, idle timers, declared logs, cancellation, concurrent admission) and proofs that counted operations without proving a job ran. All accepted.
- *Review stop on the resident-host note* (`releases/13/briefs/warm-tier2-resident-host.md`). Verdict: stop as written. Today's pod job runs the generation in the shell job's own process, not through the pod's Runtime (`astrid/core/generation/local_job.py:79-96`; `astrid/packs/vibecomfy/local_job.py:252`); the per-job reset replaces the Runtime owner and rotates its credentials, so nothing kept warm under it survives; settlement, the idle expiry, its watchdog deadline and the host timer must complete before success is reported (`astrid/packs/runpod/worker_owner.py:640, 794-798`; `astrid/packs/runpod/pod_watchdog.py:303-310`); a failed reset must release the machine at once as today (`machine.py:1508-1516, 1568`); reconciling an unknown outcome needs an idempotent request key stored before submission. All accepted: Phase 1 opens with a design round.
- *Lean-on-ComfyUI review and the narrower-check evaluation.* Reflected in the table and limits above.
- *Advisor's own critique.* (a) The largest risk is a second custodian on the machine. (b) Long-lived state goes stale: every job must bind to the live engine identity. (c) "Under 0.1 seconds" is not reachable from a fresh Python process; the plan says so. (d) Timing targets flake: the gates are counts and valid outputs; time is the witness. (e) The first estimate in days was human-shaped; the owner corrected it; and the first Phase 1 date was optimistic and failed review. Estimates here name the bottleneck.

**Proof and limits:** Completion is defined in [plan.md](plan.md#completion). Per-step seconds in the strategy note are estimates; only the totals quoted above are measured. The share of the pod-side block taken by each of audits, node restore, dependency preparation and doctor is not yet measured; SP-1 measures it.

**Review rounds:** Agreed by the owner on 15 November 2026 (D10): one review stop on the Phase 1 design (custody is built on it), one on the workflow-scoped check (every placement's readiness depends on it), and one final round before any release task.

**Run start:** Pending — No run is authorized. Next: when the owner starts a run after Release 13 publishes, record the date, the phases it covers, the accountable session, what it may do without asking, and the advisor session.

### Angles to explore

Open questions and hypotheses, not tasks. None is measured unless it says so. Each becomes a task only if the cheap check shows it matters.

| Angle | Why it might matter | Cheapest way to find out |
|---|---|---|
| Command-line start-up and imports | **Measured 15 November** (median of 5, installed copy of 6a6ab6f4d): `generate --help` 213 ms, `tasks --help` 144 ms, plain `--help` 1,010 ms, against a Python floor of 17 ms. Lazy imports would save about 70 to 80 ms per command; bytecode is not precompiled at install (351 `.pyc` for 972 `.py`). So the command line is not the half second to two seconds first assumed, except plain `--help` | Done; it is task SP-27. Still open: what the remaining 800 ms of plain `--help` is (pack discovery, `astrid/core/gateway/omp_agent.py:43-50`) |
| The agent's own loop | An agent may make five to twenty tool calls and read a long skill to produce one image; that can dwarf the job | Count tool calls and wall time per image in the tester sessions' transcripts |
| Perceived wait in the App and through MCP | A job that streams progress and a preview feels faster than a quicker silent one | Check whether ComfyUI's progress and preview events reach the App today; time to first visible sign of life |
| Step counts and Turbo defaults per model | Halving steps halves generation, which is now the part that matters; video took the same wall time at 8 and 20 steps only because overhead hid it | For each default, the fewest steps at which output is acceptable, from one live grid |
| Text encoders kept in system RAM across model switches | A switch back to the image model cost 62 s (measured); video's text encoder is 27 GB | During a switch, read ComfyUI's load lines: how much of the reload is the text encoder and how much the diffusion model |
| ComfyUI launch settings | High-VRAM mode, attention backend, fp8 weights, compiled graphs: possibly tens of per cent of generation and load | One live grid on one model with each flag; the recipe sets `--use-ck-attention --disable-comfy-compiler` today |
| Model load from a network volume | The first job reads tens of gigabytes; read speed there sets the cold start (video's first load: 211 s, measured) | `fio` or a timed `cat` of one model file on the volume against the machine's local disk; then consider copying hot models to local disk at claim |
| Fresh-machine bootstrap and engine install | About nine minutes of the first job (measured as a block); the environment is rebuilt on every new machine | SP-1's timing on a first job; `uv` cache and the environment kept on the volume (SP-20) |
| Claim and capacity wait, and GPU choice | Minutes when the chosen GPU is scarce; a cheaper, more available card may finish sooner end to end | The `capacity_wait` phase across the release's claims, by GPU type and hour |
| Idle retention length | A longer warm window turns cold starts into warm ones at a known price per idle minute | From claim history: the gap between consecutive jobs, against the 30-minute default |
| Several jobs per claim | A queue or a batch on one claim pays the fixed costs once; ComfyUI batches natively | How often the same person or agent submits more than one job within a minute |
| Speculative warm-up | Load the default model when a session starts or a claim is made, before the first prompt | Time from session start to first submit in real sessions |
| Transfer of inputs and outputs | Video outputs and reference clips are megabytes over the provider's proxy; per-file fetch is already being removed | Bytes and seconds per transfer from the timing block once SP-1 lands; then compression or a preview-first response |
| Output encoding | The video encode and container mux may be a visible share of a short clip | ComfyUI's per-node timing for the save node |
| Install and first-run time on a person's computer | The first impression: installer, Runtime start, the 17 GB first download | The tester reports' install time and download rate |
| Windows-specific costs | Antivirus scanning of model files and process start cost are much higher on Windows | The tester reports' A against A2 timings and install time |
| The Runtime's own latency | Admission, settlement and storage each involve a store write and an fsync | Timing inside the Runtime for one task, from its own logs |
| Workflow conversion in VibeComfy | Witness hashing was 3,058 hashes per save before its fix; other per-job walks may remain | A profile of one compile and one save-as-entry |
| Readiness and listing calls | `generate list` and `defaults` probe every target and fetch the full node list; agents call them often | Wall time of each call on a tester's machine |
| The size of the skills an agent reads | Token and reading time before the first action | Size of each skill file, and which parts a typical first generation needs |

## Owner decisions

- **D1 The targets.** Decided 14 November 2026: warm same-model overhead under 5 seconds on a rented machine for the work now in this plan, then under 0.5 seconds, and under 0.1 seconds locally. Source: orchestrator relay, 23:16 and 23:34 UTC.
- **D2 Warm attestation.** Decided 14 November 2026: approved. The first job on a claim verifies fully; later jobs with the same requirements skip re-verification; anything changed re-verifies. Same trust boundary as the model-verification record. Source: orchestrator relay, 23:16 UTC.
- **D3 Through Astrid.** Decided 14 November 2026: the fast path keeps Astrid's own job path, "for the sake of consistency". Source: orchestrator relay, 23:29 UTC.
- **D4 Every second accounted for.** Decided 14 November 2026. Source: orchestrator relay, 23:14 UTC.
- **D5 Release 13 keeps its cutoff.** Decided 14 November 2026: Release 13 ships the first tier; the rest is this plan. Source: orchestrator relay, 23:46 UTC.
- **D6 Model files are not re-hashed on every job.** Decided 14 November 2026: full verification is an explicit opt-in. Source: `releases/13/decisions.md`, 19:15 UTC entry.
- **D7 Lean on ComfyUI, with a narrower check.** Direction given 14 November 2026: "does Comfy not handle this?"; "we might need to check it for our reasons, like to know what to update and download, but maybe in a more narrow way". Source: orchestrator relay, 23:46 and 23:47 UTC. The principle and its limits are in the plan.
- **D8 Which execution boundary on a rented machine stays resident.** Open; decided at RS1. Options: a kept-warm job runner beside today's direct execution; the machine's Runtime host with a reset that preserves it; a new supervised service.
- **D9 Submit-first on a paid, warm engine.** Decided 15 November 2026: agreed, only when the claim is attested for the workflow's requirements, and with the translation of ComfyUI's errors to Astrid's typed refusals (SP-24) as its prerequisite. Source: orchestrator relay, 00:12 UTC.
- **D10 Review rounds and priority.** Decided 15 November 2026: two review stops (RS1, RS2) and one final round; priority directly after Release 13's follow-ups. Source: orchestrator relay, 00:12 UTC.

## Source identities

Pending — recorded at run start. Expected base: astrid-agent at the Release 13 tag, with VibeComfy, the Runtime and `runpod-lifecycle` at the versions that release pins. The analysis in this pack was made against astrid-agent `r13/compose` at `ee14644a4`, VibeComfy `dba38f86`, the Runtime `6855dfa8` and ComfyUI `6bfaacc`.

## References

On branch `r13-progress/decision-log`: `releases/13/briefs/warm-latency-strategy.md`; `releases/13/briefs/warm-tier2-resident-host.md` (stopped at review; kept as the record of that design); `releases/13/evidence/live/p1-timing.md`; `releases/13/decisions.md`, entries of 14 November from 19:15 UTC.
