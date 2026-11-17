# Local speed: the fast lane

[Plan](plan.md) · [Inputs](inputs.md) · [Decisions](decisions.md) · [LS-3 card](tasks.md)

**LS-3 / R14-P55-01 — RS1 rework submitted for the Lead's finding check.** This note
specifies the implementation; it does not claim that the fast lane exists or
that a latency target has passed. The packet changes this file only. The Lead
owns review, integration and the task record. [RS1's one review round][rs1]
returned findings RS1.1–RS1.9; this revision applies them and the owner's
[D14][d14]. It does not commission another round.

## Basis, scope and evidence

The packet and [authority][authority] are pinned at astrid-dev
`1c6b21f3e6fda84384871805719ebba6e03b626c`. The PR base is
`4b774b114dcc97b11cfe50ad69eeac18b0308711` on `release/14/plan-55`, including
the floor table merged from [#756][floor-pr]. Read together: the
[handover][handover], [developer handoff](developer-handoff.md),
[time ledger](inputs.md#the-time-ledger), [keep list](inputs.md#the-keep-list),
[D1–D8](inputs.md#owner-decisions), [D9][d9], [D10–D13](decisions.md),
[RS1's rulings][rs1] and [D14][d14]. Older claims that the floor is unmerged,
that the LS-5 pin or LS-6 scope still awaits approval, or that this packet must finish
LS-1/LS-2 first are superseded by those decisions and this packet. They are
not rewritten here.

Code references below are immutable source readings:

| Source | Revision and meaning |
| --- | --- |
| Agent | `cb1a590e0008dde7e3fc2d3fbf341ef98401b32a`, the frozen RS1 source input; this snapshot pins the older VibeComfy below, and is not a claim about later live branch heads |
| Installed VibeComfy baseline | `dba38f8644c46f652376f2cd5112ea161e40f09b`, used by the floor/baseline tuple |
| VibeComfy design input | `7fde33e2523281f840121b93a8a865a7f5d847de`, D10's approved dependency candidate, with reusable transport; this is not a claim that Agent's plan branch imports it yet |
| Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c`, unchanged published pin |
| ComfyUI | `6bfaacc67c2103481e5f0c84d75257cd0581d86a`, the CPU floor's server; behavior traced in [inputs](inputs.md#planning-evidence), not a minimum version imposed on users |

**Measured constraints.** The [real CPU floor][floor] has twenty observations
per cell after a separate warmup. One-megapixel results through the unchanged
Runtime are:

| Callers | Linux median / slowest-in-twenty, ms | Hosted Windows median / slowest-in-twenty, ms |
| --- | ---: | ---: |
| One | 41.35 / 319.63 | 225.63 / 592.06 |
| Two | 178.49 / 225.22 | 284.01 / 546.03 |

The files were 904,486 and 927,815 bytes, respectively. This is a resident
probe, not the installed Agent. The two-caller cell includes contention; its
difference cannot be attributed wholly to disk writes. Linux's median fits
100 ms in one cell, while neither that cell's tail nor the two-caller median
establishes a universal 100 ms result.

The [Linux installed-path baseline][linux-meter] instead used an 82-byte,
16×16 image and one second-job observation per caller: SDK 22.2798 s, Python
CLI 16.8292 s. A separate instrumented invocation counted 13 Comfy requests,
8/9 process starts, 8 workflow compiles, 2 bundle compiles, 3 emissions and
25 Python output-hash streams. Its 166/162 native flushes include background
activity in the caller interval; they are not an attributed per-job write
budget. The [dated handover][handover] records Windows observations of
66.7/32.2 s and incomplete native attribution. The [later checkpoint][later]
records a successful Linux meter and a Windows trace-conversion timeout.
None is a median optimization result or completed LS-2 qualification.

**Metric and decision.** Measure caller entry to usable reply, subtract only
that prompt's observed Comfy execution interval, and report queue wait
separately without silently removing it. A successful synchronous reply
includes a stored result, its durable Runtime record, and completed delivery
where the caller requested a local file. Stage one remains D1's median under
2 s on the stated warm workload. Preserve create → claim → settle for that
stage. The floor gives no reason to weaken D2 or bypass D3. Missing GPU,
video, native-client and real-Windows-machine cells do not hold this note
(D9); their assumptions and LS-14 checks are listed below.

| D1 target, retained | Linux / macOS | Windows |
| --- | --- | --- |
| Stage-one warm overhead, all callers | Median under 2 s | Median under 2 s |
| Connected-caller design target | Under 0.1 s, unqualified end to end | Under 0.1 s aim; owner choice below |
| Fresh Python CLI design target | Under 0.25 s | Measure before setting the tighter target |
| First job after start/update/change | Under 3 s | Under 5 s |

Report slowest-in-twenty beside the median. Neither the CPU probe nor these
targets constitute macOS or warm-model qualification.

## 1. The fast-lane key and what the first job leaves behind

A cache entry belongs to an admitted immutable source snapshot, never just a
pathname. Use a canonical, versioned key over the following identities:

| Key component | Changes that invalidate it |
| --- | --- |
| Realm/project and admitted capability digest; applicable permission/configuration generation | A different authority scope, revoked policy, different effective settings or capability declaration |
| Pack snapshot and workflow source closure | Any changed Python, companion, declared dependency or workflow revision; include both content identity and selected entry |
| Workflow variant and compiler/adapter/template-format identity | A different graph variant, compiler, VibeComfy pin or binding format |
| Input shape and binding plan | Different optional-input presence, list lengths, structural switches, node topology or sink declarations |
| Resolved placement, target generation and schema digest | Another target, either transport being replaced, restart/refusal refresh, or changed schema/model-choice mapping |
| Astrid installation/source generation | Agent update, executable/environment change or replacement admitted pack snapshot |

Prompt text, seed, dimensions, model selectors and staged input names are
values when they fit an already-declared slot. They do not by themselves
invalidate the key. A selector that changes topology, a list length, or
undeclared executable behavior changes shape and takes the full path. Output
prefixes are private values generated from the task/attempt identity, never
shared cache data or an unchecked caller override.

The first job resolves the named workflow and placement, verifies admitted
source bytes, fetches target schema/model choices, and performs the full
approved preparation. LS-4 then retains a frozen graph, typed slots and their
exact node/input locations, declared final sinks, schema/source digests and
last-target-check provenance. The VibeComfy pack session also retains its
catalogue and placement lookup. A managed installation retains audit,
restore, dependency-sync and doctor results for that installation generation.
An attached user's server gets no managed installation work.

The managed cache is anchored in existing code, not a second preparation
pipeline: [`ManagedEnginePreparation.prepare`][a-managed-preparation] owns
install locking, receipt/source/environment audits and native alignment;
[`prepare_native_workflow` and `run_native_doctor`][a-native-preparation] own
the verified-interpreter dependency synchronization and doctor;
[`VibeComfyEngine.prepare_session`][a-managed-engine] owns engine readiness and
warmth. Retain those results with their source, recipe, environment, declared
node/dependency and target generations. A changed requirement, failed audit,
install/update or relevant engine failure invalidates them and re-enters those
same checks. Caching does not grant consent to restore nodes or install an
add-on, and an attached target never enters this managed path.

The first job still gets its own Runtime task, attempt, seed, input identity,
output prefix, acceptance journal and output. A later job is another execution;
reusing a template never reuses the previous result or prompt identity.

**Approval is an authority boundary.** Today's
[`ApprovedProjectionRecord.assert_matches`][v-bundle] recompiles to reject a
digest-consistent forged record; decoding a record does not confer authority.
LS-4 must add a prepared-template interface, not skip that check around an
ordinary decoded record. Only the trusted compile/admission path registers an
immutable prepared object in the pack session. A request supplies values and
an opaque, generation-scoped handle; it cannot supply graph bytes, slot
locations or an authoritative record. Lookup must bind the handle to the
source/capability/target key. Serialized handles do not survive a session
restart. A fabricated, cross-session or wrong-generation handle takes normal
admission or is refused; it cannot authorize a prompt.

Filling copies the immutable graph, checks slot types/shape and protocol bounds,
binds fresh output names, freezes the exact submitted payload and digests it.
It performs no graph/schema/range/model-presence preflight per job. ComfyUI
remains that authority (D6); compile-time structural checks warn wherever
ComfyUI would accept. Authorization, path containment and finite transport
bounds are separate checks and remain. Executable Python with untracked
file/time/environment dependencies, mutable hooks or an unfreezable graph
keeps the full per-job path. A Python object is not a security sandbox: arbitrary
pack code cannot join the trusted template process merely by presenting a handle.

**Code to change:** VibeComfy [workflow bundle][v-bundle],
[workflow compile][v-workflow], [schema validation][v-validate] and
[`authorized_queue_payload`][v-execution] (LS-4); Agent
[`_approve_live` and output-prefix binding][a-local],
[entry resolution][a-entries], [source discovery][a-discovery],
[pack admission][a-imports] and [source setup][a-source] (LS-12/LS-15).
Managed LS-15 also changes [managed preparation][a-managed-preparation],
[native preparation][a-native-preparation] and the
[managed engine][a-managed-engine], including their existing node-restore,
dependency-sync and doctor calls; §4 maps their ownership.
The per-job queue fence must accept only the new prepared authority or the
unchanged full approval path. Proof: every default workflow and 1,000 varied
bindings match today's complete compile byte for byte; forged handles fail;
shape/schema/source changes miss; distinct attempts have distinct prefixes;
fill is under 5 ms. This is required proof, not a result of this note.

## 2. Target generation: one HTTP and websocket pair

A target generation is a locally assigned identity for one selected target,
one HTTP pool and one websocket, with a shared client identity and a single
invalidation latch. Open the websocket before submitting, carry its
`client_id` in each POST, and route events by the accepted prompt ID. Both
transports and all schema facts belong to that generation. One live URL or an
old websocket beside a newly connected HTTP listener does not establish
continuity.

A replacement TCP/HTTP pool, websocket loss, changed managed-process identity,
or contradictory endpoint evidence retires the whole pair before another
fast submit. Disable implicit POST retries and hidden pool replacement that
would preserve a stale generation. An in-flight POST keeps its old transport
alive until its acknowledgement is classified; it is never replayed on a new
pool. Atomically stop new submissions, mark all associated attempts for
reconciliation, and invalidate target-dependent templates and upload-presence
facts. Reconciliation of known prompts may use a separate bounded connection;
it does not resurrect the old generation.

Reopen both transports, refetch schema/model choices, and record a new
last-check time before the next full-path preparation. A Comfy restart renews
this target state; it need not restart the pack process if its admitted source
and Astrid installation are unchanged. Outstanding attempts stay associated
with their old generation until settled or reported unknown.

**Agent-side I/O carries the same generation (RS1.8).** Extend
[`ComfyTargetClient`][a-target], not only VibeComfy's transport: its constructor
receives the immutable target-generation handle and its shared retirement
latch. `request_json`, `submit_prompt`, `upload_media`, `download_output` and
cancel check that handle under the dispatch guard before starting I/O. Requests
queued before retirement are refused if they have not started. No upload,
download, cancel or other control request may silently reconnect a retired
client; retained upload-presence facts have the same generation key.

Check the generation again before installing a downloaded file, retaining an
upload name or reporting a successful control response. Bytes or acknowledgements
arriving after retirement are evidence for reconciliation, not new-generation
success. An already-started POST is still classified conservatively, as above;
retirement does not erase possible acceptance. Recovery creates a separately
authorized connection for the recorded old prompt and never re-enables its old
client. Proof must retire the pair before and during each upload, download and
cancel and show no new request or destination publication through a stale handle.

**Limit on a user's server.** Standard ComfyUI exposes no durable incarnation
token. Managed lifecycle ownership can supply stronger process identity;
attached mode cannot prove that two connections accepted at the same URL
belong to one immutable server instance. Record that identity as unverified,
retain guarded loopback/redirect/proxy rules, and rely on submission validation
within the accepted D5/D6 boundary. Do not call a local generation number a
verified Comfy boot ID, silently add an extension, or infer that absent history
means no execution occurred.

**Completion.** On the inspected ComfyUI, `execution_success` precedes history;
`executing` with `node = null` follows it. That latter prompt-scoped event wakes
one history read. Validate terminal status, declared sinks and attribution as
today, including all-cached, failed and interrupted jobs. A completion event is
not sufficient output evidence. If a server cannot supply the needed event,
leave the fast lane; only the explicit disconnect/incompatibility recovery
path may perform bounded history/queue reconciliation. It is labelled in the
record and cannot pass the normal zero-poll budget.

**Code to change:** VibeComfy [`ComfyTransport` / `ComfyAttempt`][v-transport],
[`_wait_for_server_history`][v-session] and [runtime run][v-run] (LS-5);
Agent [`ComfyTargetClient`][a-target] and [attached adapter][a-attached]. The
approved transport already separates shared I/O from an attempt; its existing
bounded polling fallback is not by itself the complete zero-poll fast lane.
Keep one attempted POST per **Comfy attempt** and a separate witnessed-prompt
set. The single definite-rejection recovery in §3 allocates a new Comfy attempt;
it never resets an old client's submit flag.

## 3. Leaving the fast lane and reaching the full path

Full path means fresh resolution/preparation under existing permissions and
typed refusals. It is not permission to rerun an accepted or uncertain job.
Track definite-rejection recovery with one explicit used/not-used flag per
logical invocation, not recursive retry. Ordinary cold preparation is not a
submitted attempt and does not consume that recovery allowance.

| Case | Action and submission rule |
| --- | --- |
| First job, evicted entry, new variant/shape, unfreezable builder | Full preparation; allocate/retain this invocation's identity. Submit only after a valid prepared/full approval exists. Unfreezable builders stay on the ordinary process path. |
| Workflow, companion, admitted pack or effective settings change | Stop using the old key; atomically select a newly verified snapshot and full preparation. Never reread mutable code through an old handle. |
| Astrid/source/environment update | Retire the resident generation as in §4/§8; re-handshake and use full preparation. |
| Either target transport drops, restart or listener continuity is uncertain | Retire the pair and reconcile all old attempts as in §2/§6. New jobs prepare against a new generation. Old accepted/unknown jobs are not submitted again. |
| Node/model removed and ComfyUI definitively refuses before enqueue | Apply RS1.3: a definite typed rejection with **no prompt ID and no acceptance evidence** invalidates target facts and permits one full-path refresh/recompile. If it succeeds, allocate one fresh Comfy attempt under the same live Runtime task/attempt/fence, with a new client, witness, journal and private output prefix, then submit once. If refresh fails, return the existing typed missing-node/model/precondition refusal and repair choices. Never reset the rejected client's submit flag. |
| Failure after enqueue, including a model disappearing during execution | Record the typed terminal failure. Invalidate readiness for the next request; do not regenerate this job automatically. |
| Timeout, malformed/empty acknowledgement, disconnect during POST, or failure to persist acceptance | Mark acceptance unknown, reconcile if owned evidence permits, otherwise return the existing recoverable unknown outcome. A second POST is forbidden. |
| Cached uploaded input absent or the wrong size | Invalidate the presence fact and use LS-11's private per-task upload name. Never repair/overwrite a shared content-named file. |
| Changed authorization, expired lease/fence, revoked capability or scope mismatch | Refuse through Runtime. A full path cannot bypass the refusal. |
| Output truncated, mutated, unattributed or missing | Refuse publication/delivery; retain the original prompt identity for retrieval recovery. Full preparation can serve a later explicit request but cannot conceal this failure by regenerating. |

A definite rejection is established by the existing typed pre-enqueue protocol
response, not an arbitrary HTTP error or merely the absence of a prompt ID.
The [Lead's RS1.3 ruling][rs1] preserves the job that can succeed today after
refreshing its schema. Persist the rejected Comfy attempt's evidence, then use
a new child-attempt ID/ordinal for the refreshed payload. Its witness starts
empty; its journal and output prefix cannot overlap the rejected attempt.
Recheck the Runtime lease/fence and unchanged caller consent before submitting.
There remain **one POST per Comfy attempt and at most two Comfy attempts per
logical invocation** on this specific path. It adds no Runtime create/claim.

If the refresh fails or the second Comfy attempt is definitively rejected,
return the full-path typed refusal; there is no further refresh/submit loop.
An accepted first attempt, a timeout, malformed acknowledgement, lost witness
or uncertain acceptance never qualifies. A user-requested retry after an
unknown outcome is a new invocation with explicit provenance, not automatic
recovery. The rejected and replacement attempts' additional evidence writes
belong to the fallback case, outside §5's successful warm-job allocation.

**Code to change:** [local preparation/approval][a-local],
[pack action dispatch][a-local-job], [target submission/cancel][a-target],
[VibeComfy queue and failure evidence][v-run], [session failure state][v-session]
and LS-8's adapter under the existing session owner (LS-9/LS-15). LS-9's proof is one case per
row with the current typed result, plus successful fresh-schema recovery,
refresh failure, second rejection and lost acknowledgement. Assert one POST
per Comfy attempt, exactly one bounded replacement only on definite rejection,
distinct clients/witnesses/journals/prefixes, no unrelated cancel and no
unexpected source/installation mutation.

## 4. Resident helper: lifetime, state and isolation

LS-8 adds a module such as `astrid/core/execution/resident_sessions.py` and a
worker entry beside `generic_host_worker.py`; these names are proposed, not
existing APIs. They implement the retained pack-worker adapter and its bounded
message protocol **under the existing host session owner**, not another session
manager or scheduler. [Plan 13][plan13] draws its map on `release/14/main` and
redraws it after Plan 55 lands. The source map below is this note's pinned Agent
input, not a claim that it replaces that release-branch map. Release 14 adds
narrow host wiring; the broad host extraction remains Release 15's.

### Existing ownership and the precise extension seams (RS1.1)

All paths in this table are relative to `astrid/`. None is replaced by a parallel
registry, scheduler or process owner.

| Existing module / proposed module | Reuse or extension | `generic_host.py` seam |
| --- | --- | --- |
| [`core/execution/managed_tool_session.py`][a-managed-session] | **Reuse and narrowly extend** `ManagedToolSession`, `SessionBinding`, `AdmissionToken`, `open`, `admit`, `adapter_for`, `settle`, `cancel` and verified `release`. The resident worker is an adapter in this same custody slot. Preserve binding/generation checks, single dispatch per token and occupied poisoned slots when release is unproved. An adapter supplies token-specific `cancel_admission`; it must not fall through to whole-engine cancel. | The owner is constructed at 6814; `_hold_session_slot`, `release_managed_session` and `_release_idle_session` at 7274–7330 remain the owner controls. Extend the VibeComfy session open/admit/dispatch/settle path in `_run_task_impl` (13309–13972); keep Runtime settlement in the parent. |
| [`core/execution/persistent_supervisor.py`][a-persistent-supervisor] | **Reuse unchanged** as the opt-in durable JSONL wrapper for already-admitted jobs. Do not instantiate another `PersistentJsonlSupervisor` inside the helper: its own attempt/fence/capacity journal would duplicate the outer lifecycle. | `persistent_supervisor` at 15007–15062 continues to call `run_task` and `cancel_task`; `run` / `_run_claim_slots` remain the canonical Runtime claim loops. |
| [`core/execution/warm_hold.py`][a-warm-hold] | **Reuse** `WarmHolds.lease/release` and generation-checked idle callbacks. The existing holder lock and lease count prevent eviction during active use. Idle policy does not become a second admission queue. | `_hold_session_slot`, `_settle_session_hold`, `_warm_session` and `_release_idle_session`; retain the distinct managed-engine idle ownership rather than adding a competing timer. |
| [`core/execution/task_scope.py`][a-task-scope] | **Reuse** task process-scope birth evidence, termination/reap and absence confirmation for ordinary children and helper lifetime. Per-job authorization remains a separate Runtime fence even when a process spans jobs. | Existing launch/cleanup in `_run_task_impl`, plus host shutdown; delegate helper lifetime to the adapter without moving scope ownership into `generic_host.py`. |
| [`core/execution/custody_broker.py`][a-custody-broker] | **Reuse** authenticated role/birth-bound launch, observation, signalling and release. A PID or process group number alone is not custody. Preserve retained ownership after uncertain cleanup. | Existing host/engine role wiring and `_track_process` / `_untrack_process`; the adapter receives the already-owned launch/observe operations. |
| [`core/execution/process_group.py`][a-process-group] | **Reuse** `popen_owned_group`, `observe_tree`, `terminate_tree`, `verify_tree_absent` and `release_group`, including retained-handle containment and platform protections. No replacement subprocess manager. | The retained-child pattern in `_ManagedWanChildAdapter` (915 onward) and `prepare_wan_session` / `invoke_wan_session` (7333–7417) is a donor for inert construction, owner-before-start and fenced invocation, not a change to Wan behavior. |
| Proposed `core/execution/resident_sessions.py` and worker entry | **Add only the adapter/protocol**: captured-source start, bounded typed job frames, per-job context/evidence, generation invalidation and verified child shutdown. It has no Runtime task registry, claim loop or independent restart election. | `_register_impl` advertises supported resident descriptors (§7); `claim_once` / `_execute_claimed_task` select the adapter after ordinary claim; `_run_task_impl` dispatches; existing shutdown (7420–7515) fences and releases it. |
| [`core/generation/managed_preparation.py`][a-managed-preparation], [`packs/vibecomfy/native_preparation.py`][a-native-preparation], [`core/generation/backends/vibecomfy.py`][a-managed-engine] | **Extend existing readiness reuse**: `ManagedEnginePreparation.prepare`, node-restore/alignment, `prepare_native_workflow` / `run_native_doctor` and `VibeComfyEngine.prepare_session` remain the install/audit/sync/doctor authorities. Cache their verified results by §1's generations. Replace the backend's job-wide cleanup calls with §6's per-job path; defer idle model release until quiescent. | The existing preparation and VibeComfy open/admit path in `_run_task_impl`; the host keeps install custody, source checks and consent, while the pack caches immutable results and owns Comfy semantics. |

Today's host serializes use of its session slot with `_session_task_lock`;
`CapabilityDescriptor` already distinguishes serial and concurrent admission.
Do not simply remove that lock or create a manager per request. LS-8 keeps one
owner and extends only the token-scoped dispatch interval for the declared
concurrent adapter after LS-15 removes process-global job state. Lifecycle
replacement/release remains exclusive and quiescent; Runtime resource limits
still bound concurrency. Ordinary serial adapters keep their current behavior.

A manifest declaration opts an admitted action into the resident capability.
Initial support is limited to the VibeComfy integration needed here. Declaration
alone grants no new permission and does not make arbitrary Python safe. Actions
without it, untrusted/executable custom hooks and workflows that cannot obey
the session contract keep their per-job child. Core supplies supervision and
fences; the pack owns catalogue, placement, templates and ComfyUI transport.
Core must not acquire ComfyUI schema, model or queue logic (D8).

| Lifetime or state | Rule |
| --- | --- |
| Session identity | Admitted pack/source digest + installation/environment generation + authority scope. Share neither mutable data nor authority across a different realm/project scope. |
| Launch | Reuse current captured-source validation, restricted child-environment construction, network restrictions and owned process-scope primitives. Start only from the verified snapshot and dependency environment; no ambient working-directory imports. |
| May retain | Immutable catalogue/manifest facts, prepared templates, placement/managed readiness for their generations, transport pairs and bounded job maps. |
| Must remain per job | Inputs, seed, attempt root, output prefix, prompt ownership, progress cursor, cancellation state, lease/fence/epoch, receipt and delivery state. Clear these on completion; do not reuse an attempt client. |
| Authority | Parent owns Runtime admission/publication credentials. The helper receives only the selected job's scoped operations/lease context; a returned result is rechecked by the parent and Runtime. A helper cannot create arbitrary tasks, widen effects or settle another attempt. |
| Source/install change | Stop new dispatch immediately, mark old jobs for reconciliation, revoke the session's ability to act, then terminate its owned process scope. Keep the admitted bytes and attempt evidence needed for recovery; never hot-reload modules in the old interpreter. |
| Crash, broken fence or protocol violation | Fence all affected in-flight jobs, terminate and prove release of the helper's owned process scope, and reconcile each prompt without replay before admitting a replacement. An unproved release keeps the slot occupied. This invokes no global Comfy interrupt; §6 explicitly replaces the managed backend's current global cleanup behavior. |
| Idle/shutdown | Explicit host-owned shutdown closes transports and releases memory. Idle eviction is allowed only with no live job; the next job takes full preparation. No independent scheduler/daemon election is introduced. |

Before concurrent jobs are enabled, LS-15 replaces `os.environ` mutation,
signal-handler installation and process-global working state in the local
runner with explicit job contexts. Process-level signals belong to the helper
supervisor; an ordinary job cancel is a scoped message. Use a bounded number
of active jobs and the existing Runtime resource/lease admission, with no
process creation between two supported warm jobs. The submit lock covers only
submission bookkeeping; it must not hold across GPU execution or delivery.

Development trees do not get an mtime-only content guarantee. Run from the
captured immutable bytes; a file watcher is an invalidation hint, not proof.
On an edit, watcher overflow, unavailable observation or snapshot uncertainty,
retire the session and use existing content verification on the full path.
If the platform cannot reliably support the claimed edit detection without
per-job content checks, that development tree remains ineligible for the fast
lane. Installed immutable snapshots are the supported warm case.

**Code to change:** the ownership table above, [host source custody, child environment and dispatch][a-host],
[`generic_host_worker.run`][a-worker], [pack imports][a-imports],
[manifest schema v3][a-schema] and [VibeComfy manifest][a-manifest] (LS-8);
[local job runner][a-local-job], [local server runner][a-local] and
[run action][a-action] (LS-15). Process scope lives in
[`task_scope.py`][a-task-scope], [`custody_broker.py`][a-custody-broker] and
[`process_group.py`][a-process-group], not in the host's wiring. Preserve their
platform custody, including Windows Job Objects; this is not a claim of a
complete OS sandbox. Proof must cover source/install change, kill, cross-job
fence refusal, ordinary per-job actions, two concurrent isolated contexts,
warm-hold expiry races and retention of an unproved-release slot.

## 5. Runtime hand-off, output and write budget

### Work and result notifications

The pinned Runtime offers cursor-paged event reads through
[`events_page`][r-service] and [GET routes][r-server]; it has no wait endpoint.
LS-7 adds bounded authenticated waiting for eligible work and for a selected
task's result on top of those durable states. Notifications contain IDs/cursors
and cause a state read; they are not a second source of truth or a claim grant.

The exact Agent seams are [`GenericPackHost.claim_once` and
`_claim_once_impl`][a-host] (14154 onward), the idle waits in `run` and
`_run_claim_slots`, and the SDK's
[`_wait_for_kernel_task_loop`][a-invocation] (3433–3656), whose `poll_seconds`
default is one second at its callers. Also replace the separate
`_settle_task_managed_outputs` visibility retry (3272–3307) with the durable
result/output wake. Preserve claim gates, capability readiness, budgets and
claim-versus-task identity checks. Today's empty `claim_next` itself writes an
idempotent empty outcome; waiting must be a read-only eligibility operation,
not a succession of empty claims with a timer hidden inside the server.

Register a waiter and recheck the authoritative predicate under the same
coordination lock used to publish a committed transition. Release that lock
before blocking. Notify only after commit; a rollback cannot announce a
successful result. This check/register/recheck discipline must cover admission
between an empty read and going to sleep. Two awakened hosts still use the
unchanged atomic `claim_next`; one wins. Result waiters read the settled result
and output associations, not a helper's optimistic completion event.

Keep durable event cursors and the Runtime instance/epoch in the subscription.
Reconnect by re-authenticating and reading the current task/cursor; a missed
notification or a Runtime restart is repaired from state. A stale cursor may
require a fresh scoped snapshot, never another create or execute. Wake for an
actual task transition, a scheduled lease deadline, cancellation or shutdown.
Connection keepalives and bounded request expiry must not become periodic
GET/claim loops on the warm path. Server restart/disconnect recovery is
explicitly counted separately. There is no sleep between ready work and claim
or between durable settlement and the caller's wakeup.

Create, claim and settle keep their idempotency, current epoch, capability,
resource reservation, task/attempt and lease-fence checks. Retrying a lost
Runtime response uses the exact frozen command/key; an unrelated new request
gets a new key. Suppress immediate renewal only when the fresh lease covers
the operation with a margin. Long or stalled GPU jobs still renew before
expiry, and lease deadlines/cancellation remain active while callers wait.

### The output trust boundary

Fetch each output attributed to the witnessed prompt once, hash that stream
once on the Agent side, and carry digest, length and attribution through the
[VibeComfy result][v-run], Agent result manifest and [host settlement][a-host].
A transforming hook is a new producer and cannot reuse the original receipt.
The Runtime still verifies bytes at its own boundary. The receipt is not a
worker-supplied permission to use Runtime's media-import verified-object
shortcut. Retain lease/fence/epoch and declared-output checks throughout.

The current [Runtime publication][r-service] stages bytes, journals filesystem
publication, makes CAS objects reachable, and atomically commits task/result,
associations, effects and idempotency metadata in [SQLite][r-store]. These are
an ordered filesystem/DB protocol, not one physical transaction. Preserve its
recovery of orphan objects after rollback/crash. D2 requires output durability
before durable terminal metadata and acknowledgement. No borrowed Comfy path,
writable CAS alias, hardlink-as-immutability claim or success-before-settlement
is allowed. Delivery creates an independent caller file, atomically installed
only after verification; truncation leaves the prior destination intact.

D11 permits a bounded streaming improvement over existing object routes;
**[D14][d14] settles RS1.5: the caller keeps its own hash on every verified
transfer.** Runtime reads and hashes the actual chunks it transmits, checks
length/digest, and sends the negotiated protocol's successful end-of-message
marker only after those checks pass. Independently, the caller hashes the bytes
it actually receives and compares their digest and length with the expected
object identity from the authorized Runtime result. Only after its own checks
and the completion marker pass may it rename the temporary file. Neither
negotiation nor a server-side successful verification removes that caller pass.

A header, an earlier verified file descriptor, or receiving the expected byte
count alone does not establish success: the underlying file can change. Old
protocols, ranges and other producers retain their existing caller verification
as well. Count the Agent producer's one collection hash, Runtime trust-boundary
hashes and the caller's independent receipt hash separately, even when the
caller is the Agent SDK. The old one-hash wording cannot be used to delete a
D14-required pass or label it uncounted. LS-6 removes redundant passes within
a boundary; it cannot promise one total end-to-end pass. Tests must corrupt
equal-length data despite a claimed successful transfer, truncate after all
payload bytes but before completion, and mutate mid-stream; none may replace
the caller's prior destination or yield a verified receipt.

### Thumbnail and evidence follow-up

The reply need not wait for thumbnail extraction. Use the existing
[Runtime-backed thumbnail capability][a-thumbnail] with a durable follow-up
intent bound to the settled source digest, project and attempt. Record that
intent atomically with the primary settlement/effect; the trusted host admits
or resumes the ordinary thumbnail task with a deterministic idempotency key.
On restart, reconcile pending intents from Runtime state, including the crash
between main settlement and thumbnail admission. Do not give the generation
helper task-admission/project-write powers or rely on its caller to stay alive.
A thumbnail failure remains a visible retryable enhancement failure and does
not rerun successful generation. Reuse `generation.thumbnail.attach` and the
existing effect checks. Diagnostic log formatting may follow the reply;
critical acceptance, output custody and result evidence may not disappear.

### Budget: explicit design limits, not invented measurements

For the supported warm fixture—one small new output, existing installation
and Runtime directories, idle queue, no new input, lease still valid—set:

| Work before usable reply | Stage-one design ceiling |
| --- | --- |
| Runtime lifecycle | **3 outer committed transactions**: create, claim, settle. Nested savepoints are not extra commits. No unconditional renewal or progress-only transaction. |
| SQLite commit syncs, assumed | **3 WAL syncs**, one for each of those commits with `synchronous=FULL`; checkpoint and WAL-reuse/header syncs are counted separately below. Verify the actual setting and count with LS-2, not by inferring them from three commits. |
| Thin resolution and descriptor registration | **0 extra warm-job commits**. §7 resolves from admitted data and records normalization/replay identity in the existing create transaction. Descriptor registration shares startup/change registration and is counted in the first-job/change path. |
| VibeComfy attempt evidence | **8 explicit file sync calls** allocated to prepared attempt + prepared journal (2), acceptance witness (1), history observation (1), final attempt/metadata/completion + terminal journal (4). Consolidate duplicate snapshots, not these evidence boundaries. |
| Runtime one-new-output publication | **9 explicit application file/directory sync calls** under the current successful POSIX inline-output recipe described below. Do not drop an integrity or recovery boundary to hit the number. |
| Caller file durability, when requested | At most **1 additional file-sync call** in the ordinary atomic-copy path; preserve any platform-required publication operation and report it. |
| Repeated warm work | **0** worker processes, compiles, emissions, schema fetches, pack scans, audits and success-path sleeps/polls. CLI has its separately counted one process start. |
| Noncritical logs, previews, repeated manifest snapshots | **0 additional forced writes on the reply's critical path**; durable thumbnail intent shares settlement. |

The VibeComfy allocation is a proposed consolidation of its existing
[`attempt.json` writer][v-attempt], [runtime milestones][v-session] and
[transaction journal][v-journal]. It is not a claim that today's path already
uses eight calls; the full-path baseline demonstrably does more. Its atomic
JSON file replacement is not evidence of a separate directory flush or a
power-loss-safe remote acceptance protocol. Recovery remains conservative
when a witness is missing.

The Runtime figure is source-derived, **not measured native I/O**: staged
output file (1); publication-journal file and directory (2); staging-root
directory (1); copied CAS file (1); CAS prefix directory (1); stage directory
and its removed directory's parent (2); journal unlink directory (1). The
sum is nine. These sites are in [`_stage_outputs`,
`_begin_cas_publication_journal`, `_copy_open_file_at`,
`_publish_staged_outputs`, `_discard_staged_outputs`][r-service] and
[`write_bytes_at`][r-dirfd]. The journal and cleanup ordering stays intact.
Reused objects, multiple declared outputs and failure cleanup are separate
cases with their own recorded vector, not a reason to mask a surplus.

Thus the reference one-output path allocates **17 application sync calls,
plus the optional caller call**. [`store.py` at 1525][r-store] enforces WAL
but does not set `synchronous`; RS1.6's explicit design assumption is the
default **FULL** mode and **three WAL commit syncs** for the three successful
write transactions. [SQLite's contract][sqlite-sync] adds a WAL sync for each
FULL transaction; checkpoints and WAL header reuse have further sync work.
The nominal allocation is therefore **20 calls plus the optional caller call,
before separately counted checkpoint/reuse and platform operations**. This is
an assumption for the named fixture, not a measured native ceiling.

LS-2's forced-write counter checks it: record the effective SQLite mode and
attribute commit, checkpoint/WAL reuse, filesystem publication, background
maintenance and platform write-through separately, including any work that
lands before the reply. Do not suppress a coincident checkpoint or weaken
durability to force three observed syncs. Native counts, especially Windows'
mapping from these calls, remain **NO-RESULT** until that attribution exists.
LS-7 must explain any difference while preserving durability; LS-13 maps the
Windows operations and LS-14 enforces the resulting vector with zero observer
gaps. A missing vector cannot pass qualification. Do not substitute 166/162
from the instrumented baseline or relax a check to absorb excess writes.

**Deeper Runtime change is conditional.** The observed Windows one-caller
medians were create 22.29 ms, claim 16.79 ms and settle 159.98 ms; these are
separate phase medians and must not be summed as a total median. Stage one
retains those operations. LS-1b plus attributed LS-2/LS-7 evidence may justify
combined local admission/claim or a narrowly scoped one-pass custody path for
the tighter target. Any second half of LS-7 remains an **owner decision after
that evidence**, not permission to implement it now. Such a proposal must
preserve D2/D3, stale-worker and duplicate-settle refusal and crash ordering,
go through the Lead and obtain the owner's exact Runtime re-pin. There is no
general `synchronous=OFF`,
after-reply task record or newly trusted worker in this design.

**Code to change:** Runtime [service][r-service], [store][r-store],
[server][r-server], [CAS][r-cas], [platform publication][r-platform] and
[client generator][r-generator] (LS-7 and D11's LS-6 scope); Agent
[host claim/heartbeat/settle][a-host], [SDK waits][a-invocation],
[delivery][a-delivery] and [thumbnail backfill][a-thumbnail]. Regenerate clients
from their templates; do not patch generated copies alone.

## 6. Job identity, concurrent callers, cancel and recovery

Carry this tuple through every message and evidence record: request
idempotency key; Runtime realm/instance/epoch; task and attempt IDs; lease ID
and fence; admitted source/session generation; target generation; **Comfy
child-attempt ID/ordinal**; exact bound prompt digest; accepted prompt ID if
known; and private output prefix. A
session-local handle never replaces Runtime identity. Before POST, persist the
selected prompt digest, source, target and an intent that makes a crash around
submission conservatively recoverable. After acknowledgement, persist its
prompt witness before trusting history or outputs. A client-chosen prompt UUID
is useful evidence, not proof of server-side deduplication.

Two callers have different request/attempt objects and prefixes, even with an
identical template key. Runtime controls claim/resource concurrency; the pack
multiplexes transport events by witnessed prompt ID. Authorize subscriptions
and reads against the original project/caller scope. Bound each progress queue
and coalesce replaceable progress/preview frames; an unowned binary preview
is not attributed to whichever job happens to be active. Slow consumers may
lose intermediate previews, never terminal state. Terminal/result state is
recoverable from Runtime and cannot be blocked by subscriber backpressure.

A caller disconnect cancels its subscription, **not the job**. The admitted
job retains its lease and continues to stored settlement; reconnect attaches
to the same task. Local-file delivery may be incomplete and retryable without
regenerating. An explicit authorized cancel names the Runtime task, resolves
only its witnessed prompt, and races with completion under Runtime's terminal
fence. Killing the resident process is not a substitute for job cancel.

### Managed and attached cancellation (RS1.2)

The pinned [`VibeComfyEngine.cancel` and `_cold_free`][a-managed-engine]
currently send `/interrupt {}`, `/queue {"clear": true}` and model unload/free.
`_contain` also prepends global interrupt after a poisoned or pending-fence
state, including on a later release. Those paths are incompatible with the
shared-target guarantee; the new resident adapter **must not reuse them as
job cancellation**. The existing
[`ComfyTargetClient.cancel_prompt`][a-target] is also insufficient: adding a
`prompt_id` to `/interrupt` does not prove that an old server honors it, and
even the inspected server's legacy handler checks before interrupting outside
the queue mutex.

Use the inspected server's dedicated
[`POST /api/jobs/{job_id}/cancel`][comfy-server] for both target kinds. It
calls [`PromptQueue.interrupt_if_running`][comfy-execution], which checks the
identity and signals under the same queue mutex; queued deletion also selects
only the named ID. No queue snapshot followed by a global interrupt is an
acceptable substitute.

**Detect support safely on an attached target.** `ComfyTargetClient` gains
this exact bounded, witnessed-ID route in its allowlist. On an authorized
cancel, call it for that witnessed prompt; the operation itself is idempotent
and specific to that ID, so no destructive capability probe or guessed job is
needed. A valid `{"cancelled": <boolean>}` response on this dedicated route
establishes route support for the current target generation. A 404/405/501 is
unsupported, not permission to try `/interrupt`. A malformed acknowledgement,
timeout or generation change leaves the cancel outcome unknown and uses only
bounded reconciliation. The inspected [feature list][comfy-features] does not
advertise atomic cancellation: neither a guessed feature flag, version string,
`OPTIONS` result nor an HTTP 200 from legacy `/interrupt` is capability proof.

If the dedicated route is absent, queued cancellation may still use
`/queue {"delete": [owned_prompt_id]}`. Confirm the owned job's outcome from
queue/history; if it is running or may have raced into running, return the
existing typed unsupported/uncertain result without any interrupt. On the
dedicated route, `cancelled: false` is a no-op, not proof of terminal
cancellation; even `true` means cancellation was dispatched and still needs
the terminal observation before reporting confirmed completion. Retire this
capability observation with the target generation (§2). Require no extension
or installation change on the user's server.

**Scope the managed backend itself.** Add token-specific `cancel_admission`
on its adapter, resolve that token to one witnessed Comfy attempt, and route
`cancel` through the same atomic operation above. Keep cancellation, pending
native evidence and late-result rejection per invocation. Refactor `_contain`
so it never prepends a global interrupt, clears the entire queue or frees
models as fallout from a job failure, cancellation or poisoned token. A
session-wide uncertainty fences admission and reconciles each affected job;
it must not stop the other job's prompt. `release` / `_cold_free` become
exclusive **idle** lifecycle operations: require the current owner binding,
no live tokens or unresolved prompts, and verified quiescence before model
release. They send no global interrupt or queue clear. If quiescence or process
release cannot be proved, keep custody fenced and occupied. A later ordinary
operation cannot silently reset that state.

The helper's process scope and the managed Comfy engine's lifecycle custody
remain distinct. Cancelling A cannot kill a helper or target serving B.
Before enabling concurrent native dispatch, LS-8/LS-15 must supply the
token-specific adapter and lifecycle guards above; existing serial adapters
stay serial. This changes the named backend code, rather than assuming its
current global cleanup is safe merely because Astrid started the target.

**Required LS-9 proof, on both a managed and an attached target:** admit A and
B with separate witnesses; cancel queued A while B is running, and cancel running A
while B is queued. Include A finishing exactly as B starts. B must still
produce its own valid output and Runtime record. Exercise poisoned-engine
cleanup followed by the next operation, stale-generation cancel, an unrelated
third-party prompt on the attached target, and a legacy server that ignores
`prompt_id` on `/interrupt`. Assert zero requests to global interrupt or queue
clear, no unload while a job is live, typed refusal/unknown where required,
and eventual owner-verified idle release. These are implementation obligations,
not tests executed by this documentation packet.

| Failure point | Recovery; what may happen next |
| --- | --- |
| Before Runtime admission | Reissue the same frozen admission only with the same idempotency key. No helper execution has authority yet. |
| Created but not claimed | Runtime queue remains authoritative; normal single claim may proceed. |
| Claimed, provably before submit | Recover the existing task under a valid attempt/fence and full preparation. Only explicit proof that POST never started permits submission; a missing acknowledgement does not supply it. |
| Definite typed rejection, before the one full-path replacement | Preserve the rejected Comfy attempt. Only its durable definite-rejection evidence with no prompt/acceptance permits §3's one new client, witness, journal and prefix. If that evidence is missing, or the replacement may already have submitted, reconcile conservatively and do not create another replacement. |
| Intent recorded, crash just before/during POST | Conservatively treat as possibly submitted unless a surviving supervisor can prove otherwise. Reconcile owned queue/history; no blind retry across this gap. |
| Accepted, acknowledgement or witness lost | Inspect retained evidence and known prompt identity under the same target evidence. If ownership/acceptance cannot be established, expose unknown outcome and the explicit recovery choice. Do not claim ownership of a guessed history entry. |
| Accepted, helper/socket dies while Comfy runs | Fence the old helper, retain the prompt mapping, reconcile with bounded queue/history reads and resume collection if attributable. A server restart may make the outcome irrecoverable. |
| Output exists, before Runtime settle | Revalidate attributed bytes/custody and retry the same settlement command under a still-valid lease. If the lease/epoch is stale, use only Runtime's supported recovery/refusal; never bypass a fence to publish. No new Comfy POST. |
| CAS published but DB commit failed | Existing publication journal reconciles exact objects against durable metadata. No succeeded task or caller success until settlement commits. |
| Settlement committed, acknowledgement/caller lost | Look up/replay the exact Runtime receipt and redeliver its stored result. Do not create a new task. Thumbnail intent remains durable. |
| Queue/history cleared, server restarted, or ownership/output cannot be recovered | Preserve the typed unknown/incomplete outcome with its known evidence and an explicit next action. Absence is not proof that nothing ran; automatic rerun is forbidden. |

Runtime epoch changes fence old executors even when their subprocesses remain
alive. The parent checks task/attempt/fence before forwarding every result and
Runtime checks it again when settling. If retiring one shared helper affects
two jobs, reconcile both individually; do not transfer one job's lease,
acceptance or output receipt to the other.

**Code to change:** [host run/cancel/settle][a-host], [worker validation][a-worker],
[new session modules described in §4](#4-resident-helper-lifetime-state-and-isolation),
[Comfy target][a-target], [managed `cancel` / `_contain` / `_cold_free` / `release`][a-managed-engine],
[attached artifact custody and cleanup][a-attached],
[VibeComfy acceptance/failure journal][v-session], [runtime run][v-run] and
[Runtime claim/settle][r-service] (LS-8/LS-9/LS-15; output recovery in LS-6/LS-7).
Retain existing typed exceptions/envelopes; labels in this table describe
states, not a replacement public error vocabulary.

## 7. Thin request and resident resolution

The request carries the authenticated caller/project context, stable request
key, entry/workflow selector and mode, requested placement/engine, original
values, explicit consent/repair choices, admitted input references (or bounded
new-input transfer), wait/deadline preferences and delivery preferences. It
contains neither compiled Python/graph authority nor a caller-created
execution binding, lease or verified-output receipt. A raw caller path is not
an admitted input and is never permission for an arbitrary resident file read.

Move catalogue/default/placement/schema discovery out of fresh CLI imports
into the admitted resident generation. Resolve only the named entry against
cached, versioned facts; preserve existing default precedence and the user's
requested values. Keep original values and resolved identities in provenance
so recovery cannot reselect a newer default or a different model.

### Concrete channel and authority (RS1.4)

Today's host [`_register_impl`][a-host] sends capability digests, readiness,
resources and source/dependency/epoch facts; it does **not** register entry,
default or placement definitions. The pinned [Runtime routes][r-server] have
no callback into a host. Registration cannot be treated as an existing resolver
channel. This design chooses **pure data resolution inside the already-resident
Runtime**, from an explicit registration extension, with no per-job reverse RPC.

| Step and channel | Authority and data | Commit cost |
| --- | --- | --- |
| Pack helper → parent host over the LS-8 private, bounded, generation-bound pipe | At preparation/change time the pack supplies an immutable, versioned declarative descriptor for supported entries: bounded field/default mappings, named placements, admitted input requirements, prerequisite/refusal data and exact capability/source/settings identities. The parent checks it against the captured admitted source. No Python, import path, callback address or arbitrary expression is accepted as resolver code. | No new Runtime commit; this is preparation, not task execution. |
| Parent host → Runtime using **`POST /v1/executors`**, with a proposed validated `resolution_descriptors` field | Extend `register_executor`'s allowlist/schema explicitly. The existing `worker:register` credential, executor actor binding and local-admission checks remain. Bind each descriptor digest to the approved capability/source definition, authority scope, live executor, Runtime/source/settings/placement generations and descriptor format. A caller cannot register one or acquire a worker credential. Existing untyped extra capability keys are not authoritative descriptors. | Persist/invalidate descriptors with the existing registration transaction at startup or change. Count it in first-job/change measurements; do not re-register for each warm job. |
| Caller → Runtime using **`POST /v1/tasks`**, with a proposed negotiated thin-request variant | Keep `tasks:write`, original caller identity and the existing project/capability/input/effect checks. A bounded Runtime normalizer reads only admitted descriptors and current scoped settings; it cannot call the host, execute pack code, read arbitrary paths, install, claim or publish. Its output is the ordinary normalized `execution_request` and admission fields. | Pure lookup/normalization adds **0** commits; ordinary create still costs **1**. |
| Runtime → host through the existing task queue and ordinary claim | The host receives the fully admitted task under the existing immutable claim, lease and fence. Comfy preparation/compilation and execution occur only after this claim. | Claim **1**, settle **1**: **3** outer commits for the warm successful invocation. |

This extension keeps pack-specific selectors in **pack-authored data** and
the pack's actual execution adapter; Runtime interprets only a bounded,
versioned field/default mapping format for the first supported use. It does
not import a VibeComfy resolver or acquire Comfy node/model rules. Resolution
that requires executable hooks, fresh target I/O, arbitrary pack code or facts
not safely expressible in that descriptor uses today's full caller preparation
before admission. Descriptor absence, stale generation or version disagreement
cannot create an under-specified task. Unknown entries and missing prerequisites
that fail before admission today retain that order and their typed refusals.

**Admission and replay are one existing write boundary.** Extend the service
and store ingress so a thin request's authenticated scope, idempotency key and
canonical original-envelope hash are checked for an existing receipt **before
re-resolution**. On the first create, resolve once, freeze any generated seed,
the resolved source/settings/placement/descriptor identities and normalized
payload, and store them with the ordinary task and command result in that same
create transaction. Check descriptor liveness/generations again at commit and
claim. On replay, identical original bytes return that recorded result; changed
bytes under the key are refused. No new resolution ticket, command journal or
fourth commit is introduced. This is a required extension to the existing
idempotency path, not a claim that the current Runtime already understands an
unresolved key. If creation is uncertain, recover/replay the same frozen thin
request; do not resolve through the full path under a new key.

The adapter is part of LS-7's service/server/store and generated-client scope
and LS-10's caller integration. It retains separate create, claim and settle,
and adds no independent task registry or scheduler. The existing
`generation_intent` field describes output publication and is **not** silently
repurposed into this request format. Keep its versioned contract and
`execution_request` as the first-class admission field.

On the CLI, import argument parsing, the minimal authenticated Runtime client
and result/error presentation; load full preparation only for a cache miss or
negotiated fallback. The resident tool server calls the same request function
in-process instead of `_run` starting `astrid-tools`. The SDK and App use the
same Runtime admission/result authority; adding a thin adapter does not
invalidate the App's existing explicit task path. A capability/validation,
missing-model/node, readiness or transport refusal keeps its current type,
message, details and next action across all front doors. The fast lane changes
where those decisions are made, not their permission semantics. Bounded
protocol/slot checks remain even though duplicate graph validation moves off
the warm path.

**Code to change:** [console routing][a-console], [gateway dispatch][a-gateway],
[generation CLI][a-cli], [`GenerationFacade` resolution][a-generation],
[SDK admission/wait][a-invocation], [`mcp_server._run`/`call_tool`][a-mcp],
[pack entry resolution][a-entries]; host [`_register_impl`][a-host], Runtime
[`register_executor` / `create_task`][r-service], [store admission/replay][r-store],
[server routes][r-server] and [generated client templates][r-generator]
(LS-7/LS-10/LS-15). Add a minimal client module as needed; do not import all of
`astrid.sdk.generation` merely to serialize a request. Prove identical records
and refusal envelopes for CLI, SDK and tool-server cases, plus no task side
effects on pre-admission refusal and no per-call tool-server subprocess. Test
unauthorized descriptor registration, stale/forged descriptor digests, source
change between resolve and commit, missing descriptors, unsupported executable
resolution, and replay after a lost create response and a descriptor update.
Instrument exactly three warm lifecycle commits with no resolver write or
host callback; separately report startup/change registration costs.

## 8. Client/resident version agreement across updates

Negotiate once per authenticated connection and again after any reconnect:
Runtime realm/instance/epoch, request and result schema/protocol versions,
required features (wait, thin request/descriptor format, prepared template, verified transfer),
Agent source/install generation and relevant admitted pack/VibeComfy identity.
A package version string alone is insufficient. Exact schema/source agreement
is the initial fast-lane compatibility rule; an older supported client may use
the existing full protocol. Do not invent a broad compatibility window.

A mismatch before admission returns a clear typed explanation and selects the
existing full path once if it is supported. It does not silently update pins
or bootstrap a second daemon. If the fallback is incompatible too, refuse
with the existing update/reconnect guidance. If admission may already have
succeeded, recover that exact task/key first; version fallback cannot submit a
second job. After a lease/epoch change, even a protocol-compatible helper must
obtain current authority before any further publication.

For an update, stop new admissions to the old session, retire it as in §4,
retain source/attempt evidence for already-submitted prompts, and start new
work only after the new generation's handshake and full preparation. Do not
hot-swap imported code or route an old response into a new job. A compatible
recovery path may collect an already-owned prompt; otherwise report the
existing recoverable/unknown outcome. Updating Astrid does not authorize
interrupting the user's ComfyUI or losing the old Runtime result record.

**Code to change:** [minimal CLI/gateway][a-console], [SDK invocation][a-invocation],
[installer launcher][a-launcher], [host registration/source epoch][a-host], the
new LS-8 session protocol, [Runtime service/server][r-service] and its
[generated client templates][r-generator] (LS-7/LS-8/LS-10). Test old/new in
both directions, reconnect during admission, update with an accepted prompt,
stale settlement, and fallback without duplicate creation. D10 authorizes
only its exact VibeComfy pin; further pins remain owner decisions.

## Windows

The hosted Windows one-megapixel floor is **225.63–284.01 ms median**;
slowest-in-twenty is **592.06/546.03 ms**. Reaching 100 ms on those two measured
cells would require removing more than **125.63/184.01 ms** before allowing
for any additional Agent work. The one-caller settle phase alone has a
159.98 ms median. This falsifies the earlier 25–120 ms total estimate for
these runners, but does not establish a hardware-independent Windows lower
bound. It also does not turn two-caller contention into an attributed flush
cost. A native CLI cannot fix an already-connected caller's Runtime floor.

**The owner chooses among these options; this note chooses none.**

| Option | Engineering cost and consequence |
| --- | --- |
| Keep the 0.1 s target for a real Windows machine | Build the resident path and preserve it as an unpromised target. LS-13/LS-14 need an identified machine, default scanner enabled, ordinary filesystem/security configuration, complete stored-and-recorded caller path and twenty measured jobs per cell. If that floor also exceeds 100 ms, return to the owner; hosted CI cannot qualify the promise. A paid tester remains an owner gate. |
| Move the Windows target | Owner selects the new workload/hardware-qualified threshold from measurements, with the slowest sample still reported. The Lead updates D1 and acceptance criteria. It avoids treating a current failed target as green, but changes the product promise; the packet cannot choose a convenient value. Under-two-second stage one is unchanged unless the owner changes it. |
| Meet 0.1 s another way | Attribute admission/claim, publication, SQLite and filter-driver costs, then design and prove any combined admission or narrower publication path. Preserve durable bytes + record, Runtime authority and unknown-acceptance rules; retest crash and Windows sharing/reparse-point cases and obtain exact new pins. If the only viable route changes durability, requires a Comfy extension, bypasses Runtime, disables the normal scanner or introduces a native client, bring that separate decision to the owner rather than calling it an optimization. |

The Linux/native Windows application-sync mapping and a real-machine native
flush count are still unqualified. Neither disabling the virus scanner nor a
component microbenchmark is acceptance. Keep first-job Windows under 5 s as
the existing design target; measure the Windows CLI target before setting it.
Stage one can proceed while this choice remains open. The Lead must record
the owner's answer before LS-14 claims the Windows 100 ms target is met or
changed.

## Owner decisions and dependency gates after RS1

The [review][rs1] identifies these decisions. The packet records their state;
it does not grant an approval, re-pin a dependency or perform LS-7's second half.

| Decision | State and consequence |
| --- | --- |
| Windows 0.1 s choice | **Open.** The three options and their costs are in Windows above; preserve D1 until the owner chooses. |
| VibeComfy re-pin after LS-4 / LS-5 | **Open for any new candidate.** D10 authorizes only `7fde33e2523281f840121b93a8a865a7f5d847de`. Later template/transport changes need the owner's new exact pin before the Agent consumes them. |
| Runtime re-pin for LS-6 / LS-7 | **Open.** D11 authorizes bounded implementation scope, not a new Runtime dependency in the Agent. The owner must approve the exact Runtime candidate containing the output/wait/descriptor protocol changes. |
| D11 interpretation: caller hashing on verified transfer | **Settled by [D14][d14], 17 November 2026.** Keep the caller's independent hash. §5, the guarantee table and later proof obligations use that rule without a negotiated exception. |
| Any second half of LS-7 | **Open and conditional on attributed LS-1b/LS-2 evidence.** The Lead takes the concrete combined-admission/claim or narrower-custody proposal to the owner; the three-step first half proceeds without selecting that redesign. |

## Guarantees and the owner decisions that permit changes

The table is exhaustive for the behavioral changes proposed here. Rows marked
preserved must not be traded away to reach a timing allocation. The accepted
task card specifies implementation work; it does not grant an extra owner
decision or a new pin.

| Guarantee / previous behavior | Proposed behavior and limit | Decision that permits it |
| --- | --- | --- |
| Re-resolve and recheck workflow/target each job | Retain generation-scoped facts and prepare once; preserve immutable source identity, lookup/slot bounds and anti-forgery authority | D6; accepted statements 4–6; LS-4/LS-12 |
| Fresh-schema recovery after a definite pre-enqueue rejection | Preserve one full-path recovery using a new Comfy client, witness, journal and output prefix under the same Runtime task/attempt; no replacement for accepted/unknown submission | Existing full-path promise in plan.md; Lead ruling RS1.3; one POST per Comfy attempt preserved |
| Astrid graph/schema/model preflight on every job | Compile-time structural warnings; Comfy validates submissions. Unknown inputs that Comfy accepts are not newly refused; last-check age is recorded | D6 |
| Same-name model-content assurance | Remains unverified as accepted; do not claim a cached schema verifies model bytes | D6, preserved limitation |
| One Python process per action | Only declared, supported admitted actions use a supervised resident process; ordinary/arbitrary code retains disposable children | D8; accepted statement 2; pinned-source/environment/fence guarantees preserved |
| Per-job managed audits/restore/sync/doctor | Cache the existing `ManagedEnginePreparation.prepare`, native preparation/doctor and `VibeComfyEngine.prepare_session` results for their installation generations; repeat on changes/failure. Never run managed preparation on attached servers | D6 and accepted statement 5; D5 forbids imposed changes on a person's server; code owners in §1/§4 |
| Poll work, completion and result | Replace `claim_once` loop waits and SDK `_wait_for_kernel_task_loop` / `poll_seconds` plus managed-output visibility retry with event-driven waits and authoritative reads; bounded disconnect fallback remains separately counted | Accepted statement 3; D3 and LS-5/LS-7; state/idempotency guarantees preserved |
| Repeated output hashing and buffered transfers | Carry the producer digest; preserve Runtime checks and the caller's own received-byte hash on every transfer, including negotiated verified transfer | D11 bounded scope, clarified by D14 / RS1.5; D2 preserved |
| Thumbnail extraction before reply | Durable Runtime follow-up intent and ordinary thumbnail task after main result; recover after caller/host loss | D11; D2/D3 preserved; no worker authority expansion |
| Success means stored and recorded | Unchanged, including output custody, output associations/effects and terminal record before success | D2; no weaker durability option approved |
| Runtime is the execution door | Unchanged; authenticated worker registration supplies validated data-only descriptors, and Runtime resolves the thin request into existing create/claim/settle with no per-job host callback or extra commit | D3; LS-3 point 7 and RS1.4; no caller/worker authority expansion |
| Fresh CLI/tool subprocess resolution | Python minimal client; resident tool server calls in-process; full path on supported fallback | D4 and accepted statement 10; native client remains unapproved |
| Requirements on user ComfyUI / cancel | No required extension or install. Both managed and attached paths use the dedicated atomic job-cancel route for a witnessed ID; legacy missing support yields queued-only deletion or typed running-cancel refusal. Replace managed `cancel` / `_contain` global cleanup, and gate `_cold_free` / `release` on owned quiescence | D5 and plan.md's job-only guarantee; RS1.2; two-job managed and attached proof required |
| Lost caller/unknown acceptance | Continue admitted job independently of subscriptions; recover its stored result or return typed unknown/incomplete, never automatic rerun | LS-3 point 6 and LS-9; D2/D3/D5 preserved; no exactly-once server claim |
| Connected/CLI/first-job timing promises | Keep D1 stages and workload scope; 100 ms unpromised until measured; Windows choice remains open | D1; this packet makes no target change |
| GPU-gated design progress | Write LS-3 and hold RS1 on existing CPU/stand-in evidence; live qualification remains required later | D9 |
| Dependency and permission exceptions | D10 only the named VibeComfy pin; D11 only bounded output scope; D12 only its fixture repair/retry. None authorizes a new pin or permission bypass | D10–D12; packet makes no such mutations |
| Who merges or reconciles tasks | Packet submits this note only. D13's older progress exception is not used; current release authority assigns review/merge/tasks to the Lead | Packet authority at the pinned release board |

## Unmeasured assumptions and the required proof

No more measurement is performed by this packet. These are implementation and
qualification obligations, with unknown values left visible:

| Assumption or remaining number | How it is checked; consequence if false |
| --- | --- |
| Default workflows can be frozen with typed slots under 5 ms fill | LS-4's 1,000 varied values/default-workflow equivalence test, forged-handle and changed-shape/schema cases; LS-14 reports any full-path exclusions instead of silently treating them as fast. |
| Resident protocol preserves source, environment and task custody | LS-8/LS-15 two-job and two-caller proof, kill/source-change/fence tests; LS-14 runs the installed candidate, not an in-process substitute. |
| Hosted Linux's one/two-caller difference is contention rather than a new fundamental write cost | LS-2/LS-7 exclusive spans and separate timing/counter runs; LS-14 reports both caller counts and queue wait. No saving is inferred by subtracting medians. |
| Exact native flush vector, including Windows and SQLite, fits the allocation and timing | LS-2's forced-write counter verifies §5's assumed 3 FULL-mode WAL commit syncs, with checkpoints/reuse separately attributed; LS-7 names each cause against 3 commits and the application-write budget; LS-13 maps Windows operations; LS-14 requires complete attribution and regression gates. Missing native counts remain NO-RESULT. Necessary extra durability work returns to the Lead with a revised measured design, never a weakened assertion. |
| Verified streaming preserves both Runtime and caller verification | D14 keeps the caller's own hash. LS-6 mutation/equal-length corruption/truncation/final-framing, disconnected-caller and stale-fence cases must still fail safely; LS-14 counts producer, Runtime and caller passes separately across the installed path, with no negotiated omission. |
| Thin resolution stays within existing admission authority and 3 commits | LS-7/LS-10 descriptor-registration auth/source/generation tests, pre-admission refusals and frozen-envelope replay across updates; LS-2 counts warm transactions and separately records startup/change registration. A descriptor cannot run pack code or become a worker credential. |
| Moving preview off the reply does not lose it | Kill after settlement but before thumbnail admission, drop caller, restart host and verify one eventual Runtime-backed attachment. LS-14 checks valid primary output plus durable follow-up, not just low latency. |
| Actual first-job and Python CLI floors | LS-12/LS-10 measure real start-to-request and request-to-reply on each OS; LS-14 keeps cold/changed-source jobs separate from second jobs. Native-client timing is absent and does not change D4. |
| Real Windows machine can meet the owner's chosen target | LS-13 plus live LS-14 on declared hardware with the normal scanner. Apply the owner's Windows choice; report medians and slowest-in-twenty without hiding tails. |
| Warm-model image, video and new-input behavior | Live LS-14 on authorized GPU hardware, default image and default video, Linux and Windows, real stored outputs and task records. Large media and new input are separately attributed; the small-image target is not a size-independent bound. |
| Older/uncontrolled ComfyUI event/cancel support | LS-5/LS-9 cover cached/error/interrupted/lost-event/reconnect, retired Agent upload/download/cancel and missing dedicated atomic cancel; §6 requires two-job managed/attached cancellation and poisoned cleanup cases. LS-14 labels bounded fallback and unsupported cases. No install requirement is invented. |

**Acceptance matrix for the Lead's design review:** §1 answers the key and
first-job residue; §2 the paired target generation; §3 every fast-lane exit;
§4 helper lifetime and protections; §5 waits, output and write budget; §6
identity, concurrent callers, cancel and crash outcomes; §7 request/resolution
and typed refusals; §8 version agreement; Windows states the measured conflict
and all three owner options; the guarantee table links every change to its
authority. Each numbered section names the code that changes and the proof
its implementation must supply.

### RS1 rework index

| Finding | Change to inspect |
| --- | --- |
| RS1.1 and Paths | §4 names reuse/extension of the existing session, supervisor, warm-hold and process-custody modules and the exact host seams; Plan 13's map is on `release/14/main`. |
| RS1.2 | §6 scopes the managed backend, detects/uses dedicated per-job cancellation on attached targets and specifies both two-job proofs; the guarantee row agrees. |
| RS1.3 | §3 and §6 preserve one fresh Comfy attempt after definite typed no-prompt rejection, with new custody records and no uncertain-submit retry. |
| RS1.4 | §7 specifies private preparation frames, authenticated descriptor registration and Runtime-side data resolution; normalization shares create and adds no warm commit. |
| RS1.5 / D14 | §5 and both matrices retain the caller's independent hash without a negotiated exception. |
| RS1.6 | §5 states three assumed FULL-mode WAL commit syncs and separate checkpoint/reuse accounting, checked by LS-2. |
| RS1.7 | §1/§4 name managed/native/backend readiness code; §5 and the guarantee table name `claim_once`, SDK `poll_seconds` and managed-output waits. |
| RS1.8 | §2 carries the generation and retirement fence through every Agent upload, download and cancel, including late responses. |
| RS1.9 | PR #803 must begin with one `Project: plans/55-local-speed/plan.md` and one `Review request: implementation` line. Submission proof reports `review-intake` as well as documentation/consumer checks; a red check is not an overall CI success. |

The repository's documentation check validates this note's structure/links.
It does not consume another RS1 round, certify product performance or complete LS-1/LS-2.
Submit the exact document commit and check results in PR #803 and mailbox
#796; no `tasks.md` edit, product change or merge is part of this packet.

[authority]: https://github.com/banodoco/astrid-dev/blob/1c6b21f3e6fda84384871805719ebba6e03b626c/releases/14/run.md#authority
[handover]: https://github.com/banodoco/astrid-dev/blob/1c6b21f3e6fda84384871805719ebba6e03b626c/plans/55-local-speed/handover.md
[plan13]: https://github.com/banodoco/astrid-dev/blob/1c6b21f3e6fda84384871805719ebba6e03b626c/plans/13-execution-host-refactor/plan.md#release-14-scope
[d9]: https://github.com/banodoco/astrid-dev/pull/728
[rs1]: https://github.com/banodoco/astrid-dev/pull/803#issuecomment-6955108457
[d14]: https://github.com/banodoco/astrid-dev/issues/796#issuecomment-6955711095
[floor-pr]: https://github.com/banodoco/astrid-dev/pull/756
[floor]: ../../releases/14/evidence/ls1/real-cpu-20261116.json
[linux-meter]: evidence/continuation-20261116/linux-meter-43918996289.json
[later]: evidence/continuation-20261116/approved-implementation-followup.md#e5--newest-completed-attached-meter-run-and-bounded-memory-windows-replay
[a-host]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/generic_host.py
[a-worker]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/generic_host_worker.py
[a-managed-session]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/managed_tool_session.py
[a-persistent-supervisor]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/persistent_supervisor.py
[a-warm-hold]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/warm_hold.py
[a-task-scope]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/task_scope.py
[a-custody-broker]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/custody_broker.py
[a-process-group]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/process_group.py
[a-managed-preparation]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/managed_preparation.py
[a-native-preparation]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/packs/vibecomfy/native_preparation.py
[a-managed-engine]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/backends/vibecomfy.py
[a-local]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/packs/vibecomfy/local_server_engine.py
[a-local-job]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/packs/vibecomfy/local_job.py
[a-action]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/packs/vibecomfy/actions/run/run.py
[a-target]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/backends/comfy_target.py
[a-attached]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/backends/vibecomfy_local_server.py
[a-discovery]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/pack/discovery.py
[a-imports]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/pack/imports.py
[a-source]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/pack/source_setup.py
[a-schema]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/pack/schemas/v3/pack.json
[a-manifest]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/packs/vibecomfy/pack.yaml
[a-entries]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/entries.py
[a-generation]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/sdk/generation.py
[a-invocation]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/sdk/invocation.py
[a-delivery]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/delivery.py
[a-thumbnail]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/thumbnail_backfill.py
[a-console]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/console.py
[a-gateway]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/gateway/dispatch.py
[a-cli]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/generation/cli.py
[a-mcp]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/mcp_server.py
[a-launcher]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/installer/launcher.py
[v-bundle]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/workflow_bundle.py
[v-workflow]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/workflow.py
[v-validate]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/schema/validate.py
[v-execution]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/runtime/execution.py
[v-transport]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/runtime/transport.py
[v-session]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/runtime/session.py
[v-run]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/runtime/run.py
[v-attempt]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/runtime/attempt.py
[v-journal]: https://github.com/banodoco/VibeComfy/blob/7fde33e2523281f840121b93a8a865a7f5d847de/vibecomfy/comfy_nodes/agent/_session_transaction_journal.py
[r-service]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/service.py
[r-store]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/store.py
[r-server]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/server.py
[r-cas]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/cas.py
[r-dirfd]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/dirfd.py
[r-platform]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/runtime_protocol/platform.py
[r-generator]: https://github.com/banodoco/astrid-runtime/blob/6855dfa8df65cf8ae4c002b57134d6505493c17c/generators/python_client_template.py
[comfy-server]: https://github.com/Comfy-Org/ComfyUI/blob/6bfaacc67c2103481e5f0c84d75257cd0581d86a/server.py
[comfy-execution]: https://github.com/Comfy-Org/ComfyUI/blob/6bfaacc67c2103481e5f0c84d75257cd0581d86a/execution.py
[comfy-features]: https://github.com/Comfy-Org/ComfyUI/blob/6bfaacc67c2103481e5f0c84d75257cd0581d86a/comfy_api/feature_flags.py
[sqlite-sync]: https://www.sqlite.org/pragma.html#pragma_synchronous
