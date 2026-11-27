# 63 — Dependable saving

**Project:** Dependable saving

**Goal:** A creator can edit, save, recover and undo work on a long-lived timeline while other writers work, without lost edits, silent overwrites or a stuck saving state.

**Status:** queued

**Owner:** Unassigned

**Estimate:** 17–27 engineering days implementation, including focused regression work; 4–6 days shared integration, installed qualification and review. P04 adds 1–2 days of independent acceptance, with no separate implementation lane.

**Waiting on:** Review of this reconciliation and normal R16 dispatch; the existing P77/P88/P89 implementation is the baseline. The burst-contract decision and missing P04 historical acceptance evidence are explicit in [inputs](inputs.md#decisions-needed); neither is a reason to repeat delivered work.

**Start:** [Astrid agent start](../../agent/start.md), [task dispositions](tasks.md#task-disposition-and-delivery) and [source register](inputs.md#source-identities).

**Vision gaps:** [F-001 — Platform reliability](../../vision/gaps/F-001-platform-reliability.md) (primary).

> **Planning revision, 27 November 2026 — proposed for review.** This is the single proposed R16 contract, replacing the conflicting historical instructions and appended amendments. It authorizes no implementation. Accepted owner decisions remain recorded in inputs; consequential changes are expressly pending. The [previous complete pack](https://github.com/banodoco/astrid-dev/tree/2b43946a85f63a0a114023e271baf4952ed209c2/plans/63-dependable-saving) remains the historical record.

## Outcome and scope

P63 owns one residual implementation lane for saving, the minimum P04 concurrency repairs and the bounded P89 save/undo/reopen work. P04 supplies a separately judged concurrency result. P79 supplies media imports to the same save path. Product changes land through the Lead-selected R16 plan/integration branches; P04 creates no competing implementation or publisher.

Retain the existing Runtime commit authority, accepted history, authenticated provider records, App and SDK outboxes, optimistic editor view, media admission and inverse operations. Repair demonstrated failures at those seams. Do not build a generic rule registry, effect applier, command registry, second recovery store or history engine. Full P75 performance architecture, P76 collaboration features and P18 extensibility remain later work.

### Save and recovery contract

1. **Separate logical edit from transmission attempt.** A logical intent survives retries. Before sending a real write, its owner durably retains the exact request bytes, key, basis and fence. An unknown or malformed acknowledgement may hide an accepted write: query/replay that same attempt, never regenerate it. A definitive moved/refused result may permit a newly reviewed/re-evaluated attempt with a new key; changing a request under the old key is forbidden.
2. **One meaning for each attempt outcome.** `accepted` includes an authoritative revision/publication receipt; `moved` is a definitive conflict with the current head; `refused` is definitive nonacceptance of those bytes; `unavailable` means the result is not established. Shared vectors cover Runtime/provider, App, SDK, CLI/MCP, bundle, restore and the supported import boundary. Reasons remain diagnostic. Compatible old replies are interpreted at one client boundary; authorization/verification waits have a next action and bounded retry, not false refusal or an endless spinner.
3. **One logical home per writer's pending work.** Scope custody by realm, actor, recoverable writer, project and timeline. The browser and SDK retain their existing implementations of one contract. A shared actor is not a shared writer. Preserve lock/generation fencing and explicit recovery claims; do not let a sibling process, stale callback or another tab replay or discard someone else's pending attempt. Legacy unresolved work remains recoverable.
4. **Preserve accepted conflict behavior.** D15/D16 park the refused/clashing edit and its entire already-queued suffix together. Keep mine requests overwrite against the current head, subject to normal authentication and invariants; an invalid edit may still refuse. Discard always offers a nondestructive local exit: cancel this writer's unsent work and leave its pending view, while retaining any unknown sent-attempt evidence for authoritative reconciliation. It cannot claim remote cancellation, erase accepted shared work or automatically resend discarded work that might newly commit. Resolve the unknown result before claiming no effect or issuing an accepted inverse. An agent intention/function may be reevaluated after definitive moved at most three times, then reports; fixed decisions and genuine overlap park. Unknown-attempt replay is not reevaluation. Do not add per-clip dependency analysis to bypass the parked suffix. New edits use validated capture from the visible basis without silently replaying parked work.
5. **Locally kept and Saved are different.** A new edit is locally kept only after durable capture succeeds; Saved requires the matching authoritative receipt. Keep the optimistic document while its queue drains. Bound serialized pending bytes and per-turn work, not merely the number of rows or batches. On quota or capture failure, report that the edit was not durably kept. Never silently drop work, overwrite a foreign edit or report a storage failure as Saved.
6. **Ordinary undo is part of dependable saving.** Unsent own work can be cancelled only with its suffix kept valid or parked. An in-flight attempt settles before an accepted inverse is issued. Accepted undo/redo uses the existing keyed, step-targeted inverse through the same custody path, preserves later disjoint work and parks a real overlap. The own-action stack survives foreign-head adoption; actor identity alone cannot select another writer's action. No stale-snapshot overwrite.
7. **Preserve the trust boundary.** Retain Runtime authentication, binding, order, selection, immutable history and corruption checks. Reuse P88's specific non-worsening legacy rules and P89's success-only validation memo. Equal exceptions or incomplete validation are not evidence that a change is safe. Narrow supported record/admission repairs must retain old accepted-history replay, inverse and rollback compatibility.

### Burst acceptance requiring a decision

Retain the original stress workload: 1–20 mixed edits/second for 30 seconds, 0–10 second responses, lost acknowledgements and foreign writes, in the model and a real editor. Valid nonconflicting captured edits must stay ordered, visible, recoverable and eventually match the authoritative document; real overlap must follow D15/D16.

The historical promise of exactly one waiting batch, an unconditional two-save-time drain and no refused edit cannot hold for arbitrary payload sizes under the existing serialized request cap, or for arbitrary conflicting foreign writes. **Recommendation for approval:** use one in-flight attempt, byte-bounded ordered batches only after individual inverse proof, explicit backpressure before failed capture, and measured drain time/commit counts. Do not make unsafe coalescing a prerequisite. If batching is not safe, smaller commits remain the safe fallback, but do not claim the original burst gate passed. [R16-S1](inputs.md#decisions-needed) records the alternative and the decision needed before accepting a changed gate.

## Existing work and decision

[The source/evidence table](inputs.md#implemented-baseline-and-active-donors) credits P77 verified opening/checkpoint tolerance, P89 immutable history/progress-aware timeout/validation memo and P88 admitted media swaps/legacy timing. Current App `pump` already retains the optimistic document while queued work drains; current SDK already persists exact flights and fences late acknowledgements. These are retained mechanisms, not new CC tasks.

App [#363](https://github.com/banodoco/astrid-app/pull/363) already proposes draft-owner-bound recovery cleanup and mounted reload proof. CC-5b must reconcile that existing donor with its current custodian and reuse the compatible delta or explicitly supersede it; no competing fix is assigned here. Its open status is not delivery evidence.

## Shared import and placement contract

This is the shared P63/P79 boundary. Import state and commit outcomes are distinct; they reuse existing receipts and custody rather than a combined new protocol.

| Phase | Accountable implementation | Retained identity and recovery behavior |
| --- | --- | --- |
| Prepare / transfer | P79 LM-2/4 | Before transfer, retain a small operation record: original import key, project/actor scope, filename, declared type/size and exact request options, including an expected digest when already available. Agent retains its computed digest; browser imports may learn content identity from Runtime's receipt. Retain that receipt when available. Filename/size/time alone are not content identity. Report persistence failure before claiming recoverability; no browser `File` spool or mandatory prehash. |
| Unknown import acknowledgement | P79 LM-2/4/5 | Query the existing receipt first; completed imports need no upload. For accepted-object/catalog-pending recovery, retain its digest and replay the original key/options unchanged. Runtime's staged digest/idempotency check must refuse different bytes before catalog settlement. Do not add a newly learned expected-digest header to an old attempt. After forced close without a content-bound receipt or original bytes, retain the evidence and resolve possible acceptance; do not silently call a reselected file the same operation. Local staging alone is not acceptance. |
| Accepted catalog / placement pending | P79 supplies exact verified selection; P63 CC-6/10 captures placement | Keep the completed import receipt and the captured placement intent. Retry only placement, through the existing outbox. If the target disappeared, expose the imported media and ask for a new location; do not invent a new clip or import. |
| Placement in flight / accepted | P63 CC-4/4b/5b/10 | Retain exact commit bytes/key and resolve unknown acknowledgement before another attempt. Only the matching accepted commit makes the timeline Saved. Undo uses the same save contract. |
| Reload / update / restart / discard | P79 LM-5 and P63 CC-10, using P29's existing guard | Guard the whole prepare → transfer → receipt → queued/parked placement lifetime. App-triggered reload/update waits for safe custody; native browser warning remains overridable. After forced close, recover completed receipts or truthfully request exact reselect/discard. Keep unknown-attempt evidence, accepted shared objects and other writers' work. |

P35 owns state-location and migration policy. Its later broad App relocation is not a gate on keeping recovery state in the existing owner store. If this plan changes a stored shape, its writer must prove lossless, repeatable migration and rollback-compatible recovery before deleting the old representation. Do not reopen deferred P35 work merely to move this metadata.

P79 owns input metadata and transfer; P63 owns shared capture/outbox/commit semantics; P87 owns projection and rendered output. Reserve the affected function and next landing contract, not a whole file. CC-10 is the integration of these owners, not another uploader or recovery queue.

## Sequence and readiness

On authorized dispatch, start CC-5a, the consolidated CC-7/13 corpus/capture work, CC-4/4b custody inventory and CC-17 baseline in parallel. P04 reconstructs original acceptance now; P79 can prepare its client, import and guard work independently. Record exact source/pin identities before changes.

Land the shared attempt contract before dependent client changes. CC-5b consumes its vectors and model; the existing admission owner closes only supported red rows from CC-13. CC-15/16 are conditional repairs within those rows, not mandatory architectural cleanup. CC-5c lands only after per-step inverse, serialized-cap and suffix semantics are demonstrated. The existing interim P88 timing/ripple route stays until a reviewed equivalent replaces it; moving P18 to R18 is not permission to remove it now.

Join P79's verified selection and import receipt with CC-10, then run the early import/edit/recovery/undo/reopen/short-render witness. P85 provides the existing comparable measurement method. One pin integrator joins reviewed providers and clients; shared R0 returns **separate P63 saving and P04 concurrency verdicts** on the same final installed tuple.

## Interfaces and handoff

Consume the actual R16 source tuple selected by the Lead, retaining R15 predecessor identities separately. Produce compatible attempt outcomes/vectors, writer-isolated durable recovery, supported public edit/inverse proof and a measured usable save path. A source PR, generated client sync, plan-branch merge and installed/served qualification are separate claims.

The [tasks](tasks.md) retain every original CC ID and its disposition. They do not require P75, full P35 relocation, P18 or full P76 to finish first. P04 original acceptance and relevant P79 custody evidence are inputs to R0; CE-END/CE-REVIEW are outputs, not circular prerequisites.

## Completion

The [P0-1–P0-7 acceptance map](tasks.md#end-state-checks) remains explicit. The exact compiled/installed candidate must demonstrate saving, repeated mixed edits, known refusal versus unknown acknowledgement, restart/reopen, ordinary undo/redo, import placement and correct short render, with per-ID content and accepted revision/publication readback.

Retain the original 50 ms real-browser local-kept criterion and the R16 brief's comparable 300-clip median ≤2 seconds / no observation >4 seconds save gate. Deterministic unit tests keep structural assertions; elapsed measurements belong to qualification, consistent with D12. Record 616-clip/history-bearing and film-shaped evidence separately; clip count alone is not fixture equivalence. Use the documented fixture/profile limits and do not lower the workload or silently waive a missed gate. No invented numeric restart/undo threshold: record completion and bring an unusable or unbounded result to the owner.

Required negatives include real browser storage failure/reload, old draft migration, same-actor independent writers, stale owner/late ACK, lost/malformed ACK, actual overlap, cap-limited/failed batches, source/import interruption and legacy/corruption refusals. Reuse existing harnesses and run only affected checks when relevant pins change. Historical unit passes and a Done-or-Parked CPU queue do not establish installed acceptance.

The owner's week on Almost Ready remains separately recorded lived-use evidence, not fabricated by a synthetic fixture and not permission to access private media. This plan does not publish independently; final release qualification and owner review remain required.
