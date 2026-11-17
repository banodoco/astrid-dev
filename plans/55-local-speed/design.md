# Local speed: the fast lane

[Plan](plan.md) · [Inputs](inputs.md) · [Decisions](decisions.md) · [LS-3 card](tasks.md)

**LS-3 / R14-P55-01 — design submitted for the Lead's RS1.** This note
specifies the implementation; it does not claim that the fast lane exists or
that a latency target has passed. The packet changes this file only. The Lead
owns review, integration and the task record.

## Basis, scope and evidence

The packet and [authority][authority] are pinned at astrid-dev
`1c6b21f3e6fda84384871805719ebba6e03b626c`. The PR base is
`4b774b114dcc97b11cfe50ad69eeac18b0308711` on `release/14/plan-55`, including
the floor table merged from [#756][floor-pr]. Read together: the
[handover][handover], [developer handoff](developer-handoff.md),
[time ledger](inputs.md#the-time-ledger), [keep list](inputs.md#the-keep-list),
[D1–D8](inputs.md#owner-decisions), [D9][d9] and
[D10–D13](decisions.md). Older claims that the floor is unmerged, that the
LS-5 pin or LS-6 scope still awaits approval, or that this packet must finish
LS-1/LS-2 first are superseded by those decisions and this packet. They are
not rewritten here.

Code references below are immutable source readings:

| Source | Revision and meaning |
| --- | --- |
| Agent | `cb1a590e0008dde7e3fc2d3fbf341ef98401b32a`, observed Plan 55 branch; still pins the older VibeComfy below |
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
Keep one attempted POST per attempt and a separate witnessed-prompt set.

## 3. Leaving the fast lane and reaching the full path

Full path means fresh resolution/preparation under existing permissions and
typed refusals. It is not permission to rerun an accepted or uncertain job.
Use one explicit fallback flag per logical invocation, not recursive retry.

| Case | Action and submission rule |
| --- | --- |
| First job, evicted entry, new variant/shape, unfreezable builder | Full preparation; allocate/retain this invocation's identity. Submit only after a valid prepared/full approval exists. Unfreezable builders stay on the ordinary process path. |
| Workflow, companion, admitted pack or effective settings change | Stop using the old key; atomically select a newly verified snapshot and full preparation. Never reread mutable code through an old handle. |
| Astrid/source/environment update | Retire the resident generation as in §4/§8; re-handshake and use full preparation. |
| Either target transport drops, restart or listener continuity is uncertain | Retire the pair and reconcile all old attempts as in §2/§6. New jobs prepare against a new generation. Old accepted/unknown jobs are not submitted again. |
| Node/model removed and ComfyUI definitively refuses before enqueue | Invalidate target facts; refresh and run full-path diagnosis once. Preserve the same typed missing-node/model/precondition refusal and repair choices. If preparation now succeeds, any new POST needs a new single-submit attempt object plus explicit evidence that the previous POST was rejected; never reset its attempted flag. |
| Failure after enqueue, including a model disappearing during execution | Record the typed terminal failure. Invalidate readiness for the next request; do not regenerate this job automatically. |
| Timeout, malformed/empty acknowledgement, disconnect during POST, or failure to persist acceptance | Mark acceptance unknown, reconcile if owned evidence permits, otherwise return the existing recoverable unknown outcome. A second POST is forbidden. |
| Cached uploaded input absent or the wrong size | Invalidate the presence fact and use LS-11's private per-task upload name. Never repair/overwrite a shared content-named file. |
| Changed authorization, expired lease/fence, revoked capability or scope mismatch | Refuse through Runtime. A full path cannot bypass the refusal. |
| Output truncated, mutated, unattributed or missing | Refuse publication/delivery; retain the original prompt identity for retrieval recovery. Full preparation can serve a later explicit request but cannot conceal this failure by regenerating. |

A definite rejection is established by the existing typed protocol response,
not merely any HTTP error. After one refresh, another refusal is returned;
there is no infinite refresh/submit loop. A user-requested retry after an
unknown outcome is a new invocation with explicit provenance, not automatic
recovery. Internal preparation retries that never attempted submission still
keep one visible request identity.

**Code to change:** [local preparation/approval][a-local],
[pack action dispatch][a-local-job], [target submission/cancel][a-target],
[VibeComfy queue and failure evidence][v-run], [session failure state][v-session]
and LS-8's new session supervisor (LS-9/LS-15). LS-9's proof is one case per
row with the current typed result, plus no duplicate POST, no unrelated cancel
and no unexpected source/installation mutation.

## 4. Resident helper: lifetime, state and isolation

LS-8 adds a module such as `astrid/core/execution/resident_sessions.py` and a
worker entry beside `generic_host_worker.py`; these names are proposed, not
existing APIs. In accordance with [Plan 13][plan13], supervision/state/protocol
live in those modules. `generic_host.py` gets only narrow wiring at its existing
registration, claim, task-dispatch and shutdown seams. This is not the host
extraction assigned to Release 15.

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
| Crash, broken fence or protocol violation | Fence all affected in-flight jobs, kill the owned process scope, start a fresh helper for subsequent work, and reconcile affected prompts without replay. One failure may retire a shared helper, but never implies a global Comfy interrupt. |
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

**Code to change:** [host source custody, child environment and dispatch][a-host],
[`generic_host_worker.run`][a-worker], [pack imports][a-imports],
[manifest schema v3][a-schema] and [VibeComfy manifest][a-manifest] (LS-8);
[local job runner][a-local-job], [local server runner][a-local] and
[run action][a-action] (LS-15). Reuse the existing process-scope implementation,
including [Windows Job Objects][r-platform]; it is not a claim of a complete
OS sandbox. Proof must cover source/install change, kill, cross-job fence
refusal, ordinary per-job actions and two concurrent isolated contexts.

## 5. Runtime hand-off, output and write budget

### Work and result notifications

The pinned Runtime offers cursor-paged event reads through
[`events_page`][r-service] and [GET routes][r-server]; it has no wait endpoint.
LS-7 adds bounded authenticated waiting for eligible work and for a selected
task's result on top of those durable states. Notifications contain IDs/cursors
and cause a state read; they are not a second source of truth or a claim grant.

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

D11 permits a bounded streaming improvement over existing object routes. The
reviewed design for full-object export is: Runtime reads and hashes the actual
chunks it transmits, checks length/digest, and sends the protocol's successful
end-of-message marker only after those checks pass. The negotiated client
requires that marker as well as the expected object identity and length before
renaming its temporary file. A header, an earlier verified file descriptor, or
receiving the expected byte count alone does not establish success: the
underlying file can change. Keep caller hashing on the old protocol and for
ranges/other producers. Remove it only on this negotiated, tested transfer;
otherwise the one-Agent-hash target remains unqualified rather than weakening
verification. Tests must corrupt equal-length data and truncate after all
payload bytes but before the completion marker, as well as mutate mid-stream.

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
plus the optional caller call, plus SQLite's internal syncs**. Three commits
are not three native flushes. SQLite/WAL checkpoints, Windows write-through
operations and unrelated maintenance are not numerically attributed by the
existing evidence; their native ceiling is **NO-RESULT**, not zero. LS-7 must
instrument these named boundaries, explain any necessary difference, and
retain durability. LS-14 must enforce the resulting platform-specific native
vector with zero observer gaps; the qualification cannot pass while it is
missing. Do not copy 166/162 from the instrumented baseline into the budget or
relax a check to absorb excess writes. This explicit allocation lets LS-7
proceed without another LS-1 run in this packet.

**Deeper Runtime change is conditional.** The observed Windows one-caller
medians were create 22.29 ms, claim 16.79 ms and settle 159.98 ms; these are
separate phase medians and must not be summed as a total median. Stage one
retains those operations. LS-1b plus attributed LS-2/LS-7 evidence may justify
combined local admission/claim or a narrowly scoped one-pass custody path for
the tighter target. Such a proposal must preserve D2/D3, stale-worker and
duplicate-settle refusal and crash ordering, go through the Lead's review and
obtain any new exact dependency pin. There is no general `synchronous=OFF`,
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
and fence; admitted source/session generation; target generation; exact bound
prompt digest; accepted prompt ID if known; and private output prefix. A
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
fence. Queued cancellation deletes only that prompt. Running cancellation
requires the server's atomic per-job operation; without it, return the existing
typed unsupported/refused cancel. A queue read followed by global `/interrupt`
is unsafe. Killing the resident process is not a substitute for job cancel.

| Failure point | Recovery; what may happen next |
| --- | --- |
| Before Runtime admission | Reissue the same frozen admission only with the same idempotency key. No helper execution has authority yet. |
| Created but not claimed | Runtime queue remains authoritative; normal single claim may proceed. |
| Claimed, provably before submit | Recover the existing task under a valid attempt/fence and full preparation. Only explicit proof that POST never started permits submission; a missing acknowledgement does not supply it. |
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
[Comfy target][a-target], [attached artifact custody][a-attached],
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

Move catalogue/default/placement/schema resolution out of fresh CLI imports
into the admitted resident generation. Resolve only the named entry against
cached, versioned facts; preserve existing default precedence and the user's
requested values. Freeze any generated seed and the normalized admission
payload once, before sending a retriable Runtime create. Keep original values
and resolved identities in provenance so recovery cannot reselect a newer
default or a different model.

**Admission order is unchanged.** Introduce the thin request as an
optional authenticated adapter at the Runtime boundary, using the host's
registered, admitted descriptors for resident resolution. Resolution is a
bounded preparation/query operation; it cannot execute a workflow, claim work,
install dependencies or publish output. Its result supplies the same
capability, input and execution-request fields to the existing `create_task`
under the original caller's authority. Runtime validates source binding,
permissions, resources and effects itself. There is one ordinary task and no
post-hoc record or worker bypass. Unknown entries and missing prerequisites
that currently fail before admission still do so. If a safe descriptor is not
available, use today's full caller preparation path rather than create an
under-specified task or widen the helper's permissions.

Freeze the resolved source, settings and placement generations in the admission
description and revalidate them at create and claim. A change between lookup
and create invalidates the lookup; it cannot bind new code to an old handle.
An uncertain create response is recovered by its key before resolving again.

The adapter is part of LS-7's existing service/server route scope and LS-10's
caller integration, not a combined admission-and-claim redesign. It adds no
independent task registry or scheduler. Core carries generic bounded
preparation messages; the VibeComfy pack owns selector semantics. The existing
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
[pack entry resolution][a-entries] and the LS-7 [Runtime route/service][r-server]
(LS-10/LS-15). Add a minimal client module as needed; do not import all of
`astrid.sdk.generation` merely to serialize a request. Prove identical records
and refusal envelopes for CLI, SDK and tool-server cases, plus no task side
effects on pre-admission refusal and no per-call tool-server subprocess.

## 8. Client/resident version agreement across updates

Negotiate once per authenticated connection and again after any reconnect:
Runtime realm/instance/epoch, request and result schema/protocol versions,
required features (wait, thin request, prepared template, verified transfer),
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

## Guarantees and the owner decisions that permit changes

The table is exhaustive for the behavioral changes proposed here. Rows marked
preserved must not be traded away to reach a timing allocation. The accepted
task card specifies implementation work; it does not grant an extra owner
decision or a new pin.

| Guarantee / previous behavior | Proposed behavior and limit | Decision that permits it |
| --- | --- | --- |
| Re-resolve and recheck workflow/target each job | Retain generation-scoped facts and prepare once; preserve immutable source identity, lookup/slot bounds and anti-forgery authority | D6; accepted statements 4–6; LS-4/LS-12 |
| Astrid graph/schema/model preflight on every job | Compile-time structural warnings; Comfy validates submissions. Unknown inputs that Comfy accepts are not newly refused; last-check age is recorded | D6 |
| Same-name model-content assurance | Remains unverified as accepted; do not claim a cached schema verifies model bytes | D6, preserved limitation |
| One Python process per action | Only declared, supported admitted actions use a supervised resident process; ordinary/arbitrary code retains disposable children | D8; accepted statement 2; pinned-source/environment/fence guarantees preserved |
| Per-job managed audits/restore/sync/doctor | Cache for managed installation generation; repeat on changes/failure. Never run managed preparation on attached servers | D6 and accepted statement 5; D5 forbids imposed changes on a person's server |
| Poll work, completion and result | Event-driven waits plus authoritative reads; bounded disconnect fallback is separate and unqualified for zero-poll budget | Accepted statement 3; D3 and LS-5/LS-7; state/idempotency guarantees preserved |
| Repeated output hashing and buffered transfers | Carry original digest; retain Runtime checks and caller verification until negotiated verified transfer passes | D11's bounded scope; D2 preserved |
| Thumbnail extraction before reply | Durable Runtime follow-up intent and ordinary thumbnail task after main result; recover after caller/host loss | D11; D2/D3 preserved; no worker authority expansion |
| Success means stored and recorded | Unchanged, including output custody, output associations/effects and terminal record before success | D2; no weaker durability option approved |
| Runtime is the execution door | Unchanged; thin resolution feeds existing create/claim/settle, no direct worker execution | D3 |
| Fresh CLI/tool subprocess resolution | Python minimal client; resident tool server calls in-process; full path on supported fallback | D4 and accepted statement 10; native client remains unapproved |
| Requirements on user ComfyUI / cancel | No required extension or install; atomic owned-job cancel only, otherwise typed refusal; never global interrupt | D5 |
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
| Exact native flush vector, including Windows and SQLite, fits the allocation and timing | LS-7 names each cause against §5's 3 commits and application-write budget; LS-13 maps Windows operations; LS-14 requires complete attribution and regression gates. Missing native counts remain NO-RESULT. Necessary extra durability work returns to the Lead with a revised measured design, never a weakened assertion. |
| Full-object completion proof can replace redundant caller hashing safely | LS-6 mutation/equal-length corruption/truncation/final-framing, disconnected caller and stale-fence cases; LS-14 counts hashes across the installed path. Keep verification and leave the one-hash target open until proven. |
| Moving preview off the reply does not lose it | Kill after settlement but before thumbnail admission, drop caller, restart host and verify one eventual Runtime-backed attachment. LS-14 checks valid primary output plus durable follow-up, not just low latency. |
| Actual first-job and Python CLI floors | LS-12/LS-10 measure real start-to-request and request-to-reply on each OS; LS-14 keeps cold/changed-source jobs separate from second jobs. Native-client timing is absent and does not change D4. |
| Real Windows machine can meet the owner's chosen target | LS-13 plus live LS-14 on declared hardware with the normal scanner. Apply the owner's Windows choice; report medians and slowest-in-twenty without hiding tails. |
| Warm-model image, video and new-input behavior | Live LS-14 on authorized GPU hardware, default image and default video, Linux and Windows, real stored outputs and task records. Large media and new input are separately attributed; the small-image target is not a size-independent bound. |
| Older/uncontrolled ComfyUI event/cancel support | LS-5/LS-9 cover cached/error/interrupted/lost-event/reconnect and missing atomic cancel; LS-14 labels bounded fallback and unsupported cases. No install requirement is invented. |

**Acceptance matrix for the Lead's design review:** §1 answers the key and
first-job residue; §2 the paired target generation; §3 every fast-lane exit;
§4 helper lifetime and protections; §5 waits, output and write budget; §6
identity, concurrent callers, cancel and crash outcomes; §7 request/resolution
and typed refusals; §8 version agreement; Windows states the measured conflict
and all three owner options; the guarantee table links every change to its
authority. Each numbered section names the code that changes and the proof
its implementation must supply.

The repository's documentation check validates this note's structure/links.
It does not consume RS1, certify product performance or complete LS-1/LS-2.
Submit the exact document commit and check results in PR #803 and mailbox
#796; no `tasks.md` edit, product change or merge is part of this packet.

[authority]: https://github.com/banodoco/astrid-dev/blob/1c6b21f3e6fda84384871805719ebba6e03b626c/releases/14/run.md#authority
[handover]: https://github.com/banodoco/astrid-dev/blob/1c6b21f3e6fda84384871805719ebba6e03b626c/plans/55-local-speed/handover.md
[plan13]: https://github.com/banodoco/astrid-dev/blob/1c6b21f3e6fda84384871805719ebba6e03b626c/plans/13-execution-host-refactor/plan.md#release-14-scope
[d9]: https://github.com/banodoco/astrid-dev/pull/728
[floor-pr]: https://github.com/banodoco/astrid-dev/pull/756
[floor]: ../../releases/14/evidence/ls1/real-cpu-20261116.json
[linux-meter]: evidence/continuation-20261116/linux-meter-43918996289.json
[later]: evidence/continuation-20261116/approved-implementation-followup.md#e5--newest-completed-attached-meter-run-and-bounded-memory-windows-replay
[a-host]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/generic_host.py
[a-worker]: https://github.com/banodoco/astrid-agent/blob/cb1a590e0008dde7e3fc2d3fbf341ef98401b32a/astrid/core/execution/generic_host_worker.py
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
