# Inputs — Dependable saving

[Plan](plan.md) · [Task dispositions](tasks.md) · [Owner summary](statements.md)

## Planning evidence

**Scope decision:** Pending — on 27 November 2026 the owner authorized reconciliation of P63/P04, P90 and P79 after observations [#2057](https://github.com/banodoco/astrid-dev/issues/2057), [#2058](https://github.com/banodoco/astrid-dev/issues/2058) and [#2059](https://github.com/banodoco/astrid-dev/issues/2059), one documentation PR and concise replies. This authorizes planning-record corrections only. Next: review the proposed canonical diff and resolve the explicit acceptance/scope decisions; no product implementation, new assignments or merge before review.

**Prior art:** The linked scoping/predecessor records below and [verified source table](#implemented-baseline-and-active-donors) distinguish existing mechanisms, delivered repairs and residuals.

**Approach:** One P63 implementation lane, existing custody mechanisms, P04's separate verdict and P79's shared import/placement contract; repair demonstrated causes rather than replace working architecture.

**Challenge:** Reviewed — the three observation issues were independently checked against source, owner decisions and active work; [assessment corrections](#what-changed-after-independent-assessment) reject duplicate mechanisms and unapproved acceptance changes.

**Run start:** no new P63 product run is authorized by this revision. Existing R16 source and independent evidence are retained. A future Lead records actual custodian, branch, allowed work and proof venue at dispatch.

**Proof and limits:** Read the three complete observations and comments (none at the initial or final 27 November check), current project records, R16 scope/run controls, predecessor handoffs and immutable scoping reports. Rechecked consequential source paths, merge/open states and active ownership. No product test or installed journey was executed. Source-supported risks remain distinct from reproduced failures and historical measurements.

| Existing investigation | Use in this reconciliation |
| --- | --- |
| [SC-63](https://github.com/banodoco/astrid-dev/blob/6cf0dda31179711582a6ed0d8fcf76d3456c4de9/plans/63-dependable-saving/evidence/release-16-scoping/SC-63.md) | Residual outcome/capture/writer/validation/inverse work; existing fixes credited, not redispatched. |
| [SC-04](https://github.com/banodoco/astrid-dev/blob/cbd951924424ecbad213d3ad999a75ade2aabb51/plans/04-concurrent-edits/evidence/release-16-scoping/SC-04.md) | One implementation lane and separate concurrency verdict; exact old evidence requires mapping. |
| [SC-79](https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md) | Import identity/selection and shared guard/placement boundary. |
| [SYN-01 §§2, 4.11–4.13, 7.3](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md) | Already proposed most consolidation, CC-17, safety boundaries and exact-tuple proof. These are not newly discovered work. |
| [P89 handoff #1939](https://github.com/banodoco/astrid-dev/issues/1939), [P77 rounds](../77-saving-holds-on-a-heavy-timeline/rounds.md), [P88 completion](../88-timeline-edits-land/evidence/completion-handover.md) | Retain measured failures, bounded successful cases and fixture limitations. Do not equate different workloads or source and installed tuples. |

### What changed after independent assessment

The findings support narrow repairs, not the original complete architecture rewrite. In particular:

- Current SDK exact-attempt persistence and App optimistic draining already exist. The remaining ownership/capture problem is not permission to replace them.
- D15 parks the whole already-queued suffix. The observation's possible dependency-based escape must not become a new per-clip dependency engine. New edits may start from the explicit visible basis while the parked suffix stays recoverable.
- The observation correctly identifies impossible unconditional burst formulas. That requires a visible acceptance decision, not a quiet weakening of the original gate.
- Removing Runtime authentication, accepting equal rule exceptions, rejecting old historical record shapes and deleting owner/draft data unconditionally are unsafe historical prescriptions. Retain the safety outcomes through current mechanisms instead.
- The original seven SDK test definitions were recovered from the retained donor; [P04 inputs](../04-concurrent-edits/inputs.md) now maps them. The eight hosted wrapper, CE-0/CE-LIMIT and equivalence proof are still missing. Do not rebuild a retired lease just to restore old selector names.
- P79's exact import receipt must survive placement retries. The old CC-10 instruction to delete import persistence contradicts this custody requirement and is removed. Preserve D4 warning/reselect; no browser-byte resume framework.
- P35's [later-work decision](../35-one-home-for-user-state/tasks.md#later-real-hardware-qualification-not-in-release-16) does not authorize broad App relocation now. Keep the existing local recovery owner and prove only migrations this plan actually introduces.

## Source identities

Source snapshot read on 27 November 2026; refresh at dispatch and final integration. These are source facts, not the final installed candidate.

| Repository / role | Exact inspected identity |
| --- | --- |
| astrid-dev main / previous canonical records | `2b43946a85f63a0a114023e271baf4952ed209c2` |
| astrid-app main / R15 integrated App | `cc1d48f016fde55ad6b0609c619d8a4bcec56823` |
| astrid-agent R16 integration | `4a2bad187f12e7b0d1ba5bd1164b4a076787516a` |
| astrid-runtime R16 integration | `55a541a7ab904873e63510e581a60742e1b83fb8` |
| App manifest's Agent / Runtime pins | `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` / `686ca695469bda48cd40a70824c4ccef2a137284` |

App's [manifest](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install-manifest.json) does not establish that the R16 Agent/Runtime source is served. Branch destinations are the Lead's actual R16 plan and integration refs, not the historical R15 or `pre-main` instructions. This document cuts or moves no product branch.

## Implemented baseline and active donors

| Work | Evidence and disposition | Still required |
| --- | --- | --- |
| P77 checkpoint-safe verification and verified-head opening | Merged [Runtime #81](https://github.com/banodoco/astrid-runtime/pull/81), [App #375](https://github.com/banodoco/astrid-app/pull/375), with Runtime #102 / Agent #555. Keep existing implementation. | External-write/replacement/shrink/corruption negatives; heavy startup and ordinary undo remain separately measured. |
| Optimistic view while queue drains | Current [App pump](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/commands/localSaveSession.ts#L294-L397). Remove duplicate build instruction. | Capture costs, reload, parked state and other consumers under CC-5b. |
| Exact flight, key/body/fence and late ACK settlement | Current [SDK sync](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/sdk/timeline/sync.py#L1070-L1306). Keep. | [Default scope](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/sdk/timeline/sync.py#L459-L510) has no writer identity; close sibling custody and trace bundle/restore durable callers. |
| P89 history guards, index, deferred verification, successful validation memo and rollback compatibility | Merged [Runtime #123](https://github.com/banodoco/astrid-runtime/pull/123) (`336c9af3`), [#120](https://github.com/banodoco/astrid-runtime/pull/120), [Agent #648](https://github.com/banodoco/astrid-agent/pull/648) (`23ace564`). No second implementation. | Exact integrated corruption/replay/restart/rollback evidence and measured CC-17 residual. |
| P89 progress-aware timeout and save timing marks | Merged [App #400](https://github.com/banodoco/astrid-app/pull/400) (`2a842fc7`). | Keep live progress/timeout distinction; a 120-second ceiling is not a usable-save pass. |
| P88 media swap and bounded legacy timing | Merged [Agent #612](https://github.com/banodoco/astrid-agent/pull/612) (`514499de`), App [#393](https://github.com/banodoco/astrid-app/pull/393) / [#397](https://github.com/banodoco/astrid-app/pull/397) fixture work. | Broader concurrent and public edit/inverse/renderer journeys were not all established. Keep interim ripple until P18 replacement is proved. |
| Stale-restore compare-and-swap | Current [App restore](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L246-L274) sends reviewed head; Runtime rejects stale restore. | Durable exact restore retry and no second restore after lost ACK; CAS is not client custody. |
| CE-REF builder on canonical commit | Current [reference builder](https://github.com/banodoco/astrid-agent/blob/4a2bad187f12e7b0d1ba5bd1164b4a076787516a/astrid/core/dev/reference_realm.py#L96-L137). Implementation credited under P04. | Current two journey files and App quick-journey proof, not the old rebuild recipe. |
| App #363 accepted-save/draft cleanup | [Open donor](https://github.com/banodoco/astrid-app/pull/363), head `4be44de85511889539fbf4c1f1e1ba455e322317`; not merged. | Coordinate/reuse compatible source and mounted reload regression in CC-5b; do not claim delivered or assign a second fix. |
| Other historical donors | App [#370](https://github.com/banodoco/astrid-app/pull/370), Agent [#467](https://github.com/banodoco/astrid-agent/pull/467) / [#526](https://github.com/banodoco/astrid-agent/pull/526), Runtime [#121](https://github.com/banodoco/astrid-runtime/pull/121) remain unmerged at review. #121 is measurement-only. | Compare exact residuals to landed work before any adoption; no blanket merge or duplicate swap/optimization credit. |

No whole unchecked P63 task becomes complete from these component credits. Historical measurement examples (6.23 s harness versus 13.2/14.2 s installed, heavy undo/history stalls) identify work; they are not interchangeable gate results or newly reproduced here.

## Owner decisions

The complete original decision text and private-review provenance are preserved at [18 November decisions as recorded on 2b43946a](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/63-dependable-saving/inputs.md#owner-decisions). IDs are unchanged; this table states their current application without inventing a later approval.

| ID | Original status / decision | R16 treatment |
| --- | --- | --- |
| D9 | Owner accepted R15 placement of the four original plans on 18 November. | Historical; current R16 brief carries P63/P04, while P75/P76/P18 broader work is later. No historical R15 branch dispatch. |
| D10 | Open: synthetic corpus recommended; optional owner-supplied anonymized example. | Use synthetic existing shapes/counts. No private export is needed or authorized by this assignment. |
| D11 | Main-session ruling, to confirm: changed-head intent versus raw patch behavior; old text reused a key with changed basis. | Proposed correction: unknown retains exact key/bytes; only definitive nonacceptance allows a fresh attempt/key, with stable logical intent. D16 forbids automatic overwrite. Existing request binding is preserved. |
| D12 | Main-session ruling: deterministic tests use counts rather than clock deadlines. | Preserve unit-test policy. Record installed timing separately under existing P85/P89 qualification; no hidden change to a timing gate. |
| D13 | Session ruling: one rule home and one extension door. | Reuse current predicates/admission for R16; remove a new registry mandate and never grandfather an exception. P18 owns later extensibility; no second rule policy. |
| D15 | **Owner accepted:** refused edit plus entire queued suffix park together; Keep mine and Discard in every state; one stepwise retry of a definitively refused batch. | Preserve the local way out while offline: cancel own unsent work/leave its view, retain unknown sent-attempt evidence and prevent automatic resend after discard. This is not remote cancellation or proof of no effect. No per-clip suffix salvage; new work uses the current validated basis. |
| D16 | **Owner accepted:** clash follows refusal; never automatically reapply a person's clash; Keep mine explicitly overwrites; agent retries at most three times. | Preserve, including stale delete and inverse overlap. |
| D17 | **Owner accepted:** narrow reads/writes with whole-timeline opt-in, accepting stale-premise risk only with ET-4b inverse/authorization safety. | Timing remains a decision: recommend keeping new ET-1 defaults and mandatory ET-4b together in later P76; preserve current conservative defaults and already-supported disjoint edits now. |
| D18 | **Owner accepted:** P18 agents/packs before gestures, gestures after R0 and lived-use evidence. | Historical order retained for that later project; not a prerequisite to P63 implementation. |
| D19 | **Owner accepted:** P75 300 ms goal, no conditional architectural stage. | Broader P75 stays later; this is not a waiver of retained R16/P89 usable-save acceptance. |
| D5 (P18) | **Owner accepted:** alternate view deferred in favor of pack-op proof. | Remains outside this plan. |
| D-SYN-2 | 25 November proposal: retain comparable 300-clip ≤2 s median / ≤4 s maximum under bounded CC-17. | R16 brief retains this target; do not mark it met or silently lower it. A miss needs evidence and owner disposition. |

## Decisions needed

| Decision | Recommendation | Alternative and execution boundary |
| --- | --- | --- |
| **R16-S1: finite burst contract** | Approve the [byte-bounded contract](plan.md#burst-acceptance-requiring-a-decision), retaining original stress workload, all captured work, D15/D16, explicit pre-capture backpressure and measured drain. | Retain the literal original two-save-time/one-waiting-batch promise: keep that gate unmet and size the additional design explicitly. Do not weaken safety or claim equivalence without approval. Independent corpus/custody/profile work can still be prepared. |
| **D17 timing** | Keep new narrow defaults and ET-4b together in P76 later; do not rebuild them under CC-16. | Owner explicitly brings the complete bounded pair into R16 and accepts its additional scope. Current supported disjoint behavior remains mandatory either way. |
| **P04 evidence / qualification route** | Lead recovers hosted wrapper, CE-0 and CE-LIMIT and records outcome equivalence against current routes; then one exact-tuple witness with separate verdicts. Use existing R16 venues. | If original acceptance cannot be recovered or is replaced, return a concrete equivalence decision for owner review. CPU-only packet completion cannot silently substitute. No new review programme. |

The 2 s/4 s gate is retained in the estimate, not waived. If CC-17's bounded measured repair cannot meet it, return actual same-fixture evidence, smallest repair and revised cost before requesting any changed target. No new numerical undo/restart criterion is invented here.

## What gets deleted

From the **implementation instructions**, remove rebuilding delivered verified opening, checkpoint tolerance, immutable history, memoization, optimistic pump, timeout marks, P88 swap and CE reference builder. Remove mandatory generic rule/ratchet/nightly infrastructure, blanket owner/draft deletion, one-row storage mandate, universal history-shape migration, deletion of Runtime authentication, separate P04 promotion and independent CC-10 upload machinery.

This is not permission to delete product code or safety tests. Any actual retirement requires proved replacement, preserved stored work/history and compatible consumers. App #363 and other donors remain their existing writers' work until coordinated.

## Deferred

Full P75 O(change)/300 ms architecture, P18 operation/rule registry and all-gesture conversion, P76 presence/attribution/live-adopt, broad history-range restore and generic migration infrastructure. New narrow defaults with ET-4b are recommended together for later scope, pending the D17 timing decision. Browser file-byte persistence/offset resume and P80 external-path/clone storage remain outside P63/P79. Supported current-route safety, exact attempt custody, ordinary undo, truthful recovery and useful save/reopen are not deferred.

## Issue ledger and history

Existing incidents remain their existing issues; this reconciliation creates no duplicate bug or observation. #2057 receives a concise proposed-resolution/PR link. Prior incident tables, N1–N12 history, rejected alternatives and donor identities remain in the [immutable previous inputs](https://github.com/banodoco/astrid-dev/blob/2b43946a85f63a0a114023e271baf4952ed209c2/plans/63-dependable-saving/inputs.md). No issue is reopened/closed or implementation task checked merely by merging a planning correction.

## Review and evidence limits

One existing integrated R0, with separate P63/P04 judgments and retained review limits. This documentation review adds no product review stage and no authority to claim installed PASS. Estimated work is bottom-up residual judgment; measured cause, unknown historical equivalence and qualification venue can change it. The owner's week of editing remains separate evidence, never a fabricated test result.
