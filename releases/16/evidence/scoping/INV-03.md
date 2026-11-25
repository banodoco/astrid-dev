# INV-03 — Dependable editing and persistence across the R16/R18 cut

**Run:** r16-scoping  
**Session:** INV-03-01  
**Date:** 25 November 2026  
**Disposition:** **REWORK the R16 scope and shared contracts; retain the R16/R18 boundary.**  
**Reviewed proposal / mandatory evidence-branch base:** a7ea0a52d641bbb7799ea141934833285a77ab03  
**Submission branch:** evidence/r16-scoping-inv-03-01  
**Only authorized report:** releases/16/evidence/scoping/INV-03.md  
**Draft destination:** scope/release-16-scoping-record, proposal [#1964][proposal].

This is an original cross-project scoping judgment. It does not qualify a product release, accept a scope amendment, or authorize implementation. I read the seven complete original prerequisite reports and the separate SC-35 correction, then checked disputed claims against pinned plans, current integrated source and original handoff evidence. Read-only supporting source investigations were delegated within this session; they were not prerequisite authors or additional dispatched investigators. This session owns the conclusions below.

The smallest coherent R16 is one dependable editing path with isolated writers, recoverable exact attempts, honest acknowledgement, bounded useful save/undo/restart, retained import-to-placement custody, and render/restore bound to the work the user selected. It does not require the whole fast acceptor, every collaboration feature, or the extensible editing rewrite. Conversely, postponing those programmes does not justify postponing recovery for a currently supported bundle, allowing two sessions to consume each other's work, or calling a practically blocked heavy timeline dependable.

## 1. Reviewed identities, authority and limits

### 1.1 Source register

The reviewed proposal identity, product source identities, historical served observation and eventual evidence commit are different things.

| Source | Exact reviewed identity / observation | Meaning |
|---|---|---|
| Dispatch, packet, procedure, context, evidence index, CTX-00 and CTX-01 | [a7ea0a52d641bbb7799ea141934833285a77ab03][dispatch-root] | Immutable assignment and evidence-branch parent. |
| Scoping proposal #1964 | Open draft; head a7ea0a52d641bbb7799ea141934833285a77ab03; base main at 41350e4e778a18593264da59114911e59ee8ec53 | Proposal reviewed here, not an implementation candidate. Refreshed during investigation. |
| Planning main | [1b9c7085beddc220de4c87e628f4112cb6df33e9][planning] | Canonical plan/task/handover reads unless otherwise linked. |
| Roadmap #1956 | [Merged][roadmap]; head fd4f68eb698ffd5544215920f9c4549219cc4bbd; merge 41350e4e778a18593264da59114911e59ee8ec53 | The dispatch context's earlier “unmerged” observation is historical. The merged roadmap is planning authority, not product publication. |
| Agent release/15/main | [dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5][agent-head] | Inspected implementation baseline. |
| Runtime release/15/main | [686ca695469bda48cd40a70824c4ccef2a137284][runtime-head] | Inspected implementation baseline. |
| App release/15/main | [cc1d48f016fde55ad6b0609c619d8a4bcec56823][app-head] | Newer than the 7676df48f4104fb8ebe2b19de64dea25b9ec3dc7 snapshot in several prerequisites. |
| VibeComfy release/15/main | [55c3948212d23cf037fae8a4c6faad77d33e7279][vc-head] | Candidate transitive pin; no new execution investigation here. |
| Pinned workstreams | [7060b764ec16a638b0e6774f814eabf6d7b70c04][scope-workstream] | Scope a release, Sense check, evidence-only ChatGPT packet, and multi-manager dispatch were read directly at this identity. |
| Candidate install manifest | App cc1d48f0: release 15, required floor 15; Agent/Runtime/VibeComfy pins above | Repository manifest, not independently observed installed or served state. |
| Additional manifest pins | Runtime schema sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2; runpod-lifecycle 9f88ef7640bc664f697112d966ecefa123d44340 | Compatibility inputs from candidate manifest. |
| Motion pack | 2379ab54aca522019ff4f869cfdf9375bdb56dfc; pack-tree-v1 digest 75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029 | Pin presence is not proof that the installed pack works. |
| Historical served baseline | [CTX-00][ctx00]: R14 manifest digest 8556f2183dfc5575508827ec449c23ea5bbc61792d8e85cfad309dff9d44dee7 | Preserve as a dated regression/migration origin. Fresh independent HTTP retrieval of the served manifest failed in this session. |

Candidate pins above are read from the [App manifest][candidate-manifest]. The other pinned instructions are [Sense check][sense-workstream], [the evidence-only ChatGPT packet][packet-workstream] and [multi-manager dispatch][dispatch-workstream].

The App delta from 7676df48 to cc1d48f0 is the required-release floor change. The [Release Lead's q-0016 direction to the Qualifier][q16] expressly permits save/render/test carryover across that floor-only change, while requiring fresh update and rollback proof. [Candidate status][candidate-status] confirms the new App. The [18:03 UTC qualification-manager status][qualifier-status] does not establish a final qualifier verdict. Neither the floor change nor this investigation supplies one.

The coordinator's [Wave B dispatch status][waveb] attests INV-03's fresh Pro route. I did not independently inspect the Chat UI model selector or a supported local astrid-dev skill installation. I followed the exact pinned authored instructions instead. No product source was changed, no test/build/CI or live journey was run, and no spending, migration, rollback or publication was attempted. Historical measurements and executions below are attributed to their original evidence.

**Evidence terms:** “Observed” means read in the specified source or original record. “Inference” identifies a consequence of inspected code that was not reproduced here. “Unverified” is an outstanding proof obligation. A **BLOCKING** finding blocks accepting a scope or qualification claim that omits the stated correction; it is not automatically a newly reproduced product incident.

### 1.2 Complete prerequisite originals and independent adjudication

All originals remain authoritative as records of what their authors actually examined. This report does not edit them or erase disagreement.

| Original read in full | Judgment after source checks |
|---|---|
| [SC-63, 6cf0dda3][sc63] | Retain its central queue, contract, writer, heavy-history and recovery concerns. Narrow its architectural prescription: a completed generic effect applier is not automatically a prerequisite to safe current edits. Its proposed 15/30/45-second replacement limits are recommendations, not an accepted repeal of P89's 2s/4s gate. |
| [SC-04, cbd95192][sc04] | Agree with absorption into P63 and a single implementation/review lane. Retain each concurrency guarantee, historical incident and independent proof obligation. “Absorb” must not mean closing P04 because P63 has a vaguely similar goal. |
| [SC-79, ede2640e][sc79] | The Agent's artificial 64 MiB cap, whole-file handling and App's ordinary non-image prepared-media refusal remain real in inspected code. Its old large-shots fixture failure has a later source fix; verify that fix instead of reimplementing it. Retain the warning/reselection limit for browser-owned File bytes, but preserve operation metadata and acknowledged import identity. |
| [SC-35, 44d81365][sc35] plus [severity correction, ebe29557][sc35-correction] | Apply the correction: the original F1–F5 are BLOCKING, not mild follow-ups. Agree on state classification, fencing, migration and rollback. Disagree with treating the old stale-restore omission as current source: App now sends the reviewed pair and Runtime rechecks it. This correction does not establish restore crash/unknown-ACK recovery. |
| [SC-87, 27212e57][sc87] | Retain exact installed render/output evidence and heavy-fixture limits; its newer verified-child fixture disposition is supported. Reconcile its proposed 2.6 MB blocker with the actual Lead handoff to P75. Do not confuse final qualifier-owned proof with completed P88/P87 work. |
| [ISS-03, 496ab219][iss03] | Retain the issue-first recovery, heavy undo and custody inventory. Its “old guard gone” description must be path-specific: the current prepared-media path still refuses ordinary video/audio. Historical issues are evidence leads, not proof that every old defect survives. |
| [HOR-01, 736712b9][hor01] | Preserve its original source-coverage BLOCKED disposition. I independently read the linked P88 handover/mailbox and #1952/#1384, resolving those targeted access gaps. Neither those reads nor the coordinator's bounded searches establish an exhaustive issue/horizon census. |

The [P88 final mailbox][p88-mail] is decisive on two disagreements: App #397 supplies the verified-child fixture path; final 616-clip and large-shots proof was delegated to the Qualifier, not established by P88. It also records the Lead's explicit move of **2.6 MB parity into P75 follow-up**, via #1867 / 83ab5c0e. Moving P75 to R18 does not silently move the separate P89 speed commitment, but neither does it silently bring the 2.6 MB fixture back into R16.

## 2. The actual editing and persistence path

This is a reconstruction of inspected current source, not the desired future P18 architecture.

| Surface / stage | Actual path and existing protection | R16 seam that remains |
|---|---|---|
| App read, local edit and preview | The editor hands captured changes to [localSaveSession][app-session]. While draining, an acceptance moves the durable base without replacing the person's queued visible work; head adoption is constrained to the empty case. [commitOutbox][app-outbox] stores scoped ownership/generation and the exact request before transmission, then settles under a fence. | Prove every shipped gesture uses this path, including placement continuations and shot/raw edits; preserve the protections during row consolidation and batching. |
| SDK / CLI session | [sync.py][sdk-sync] retains a flight with body bytes, key and fence before the commit call. It distinguishes a logical retry identity from a fresh wire key for a recomputed conflict retry. Native-backed edits and CLI callers converge on the guarded commit machinery. | The default outbox name includes realm, actor, project and timeline, but no independent writer/session identity. Two sessions for one actor can share custody. |
| Raw/document and pack edits | [commit_session.py][sdk-session] captures free document edits through the emitter, validates occurrence closure and media selections, and refuses unsupported mixed changes. [timeline_elements.py][sdk-elements-src] settles only the captured held flight. [P78][p78] delivered mixed commits and pack work, with separately retained proof/deferred limits. | Enumerate the actual supported edit/target pairs, accepted result and inverse. Do not advertise arbitrary raw documents or unsupported pack mutations as safe merely because the wire route is shared. |
| Bundle read / preview / commit | [authoring_remote.py][bundle-remote] opens exact parent/shot/internal pins. [authoring_render_preview.py][bundle-preview] binds an unpublished candidate to its base. [authoring_bundle.py][bundle-publish-src] compiles a canonical v2 request and uses a required caller key. The Runtime old publish route is not the current writer. | The inspected bundle publication path reconstructs and sends the request without durable frozen custody. A caller key alone does not ensure crash replay uses identical bytes. |
| Runtime accept / replay / history | [timeline_commit_store.py][runtime-store] authenticates replay identity/hash, returns an existing accepted receipt before treating the retry as a new head check, verifies history, and accepts under a transaction. [timeline_commit_auth.py][runtime-auth] authenticates declared read values against their input boundaries. | Unify the outcome envelope without weakening existing validation. Bound the cost of legitimate heavy history and recovery; incomplete future CC-16 is not evidence of an unauthenticated overwrite today. |
| Import then placement | App [prepareMediaImport][app-provider] attempts local metadata persistence of an operation key before POST and performs same-key lost-ACK lookup/replay within that call. The returned exact selection is then used for a separate timeline edit. Runtime imports can stream staged bytes into its existing CAS/catalog path. | Retain the import result and dependent placement identity across retries/reload; remove false limits and the ordinary video/audio placement refusal. “Imported” and “timeline saved” are different receipts. |
| Undo / restore | SDK publication inverse goes through the session. App [restoreHistory][app-restore] sends the reviewed revision/publication pair; Runtime's restore check uses the same exact base and a transaction-time recheck. | Preserve per-step inverse and stale-restore refusal. Prove unknown-ACK recovery for restore and usable heavy undo; no fresh restore should replace an unresolved prior attempt. |
| Render / output | [managed_timeline.py][managed-render] selects one parent then follows its pinned closure; [snapshot_refs.py][snapshot-refs] binds revision/digest and stores exact projected bytes. [verified_source.py][verified-source] binds execution files; [project_render.py][render-output] verifies retained output identity/digest/size. | Bind the user's chosen accepted revision through admission, including an intervening foreign commit. Do not conflate coherent closure after selection with proof that an earlier expected-version check selects that exact revision. |

P77/P89's save and history work, P78's atomic mixed edits, and P88's canonical edit/ripple and fixture fixes form the starting point. The [P89 handover][p89-handover], [P78 handover][p78] and [P88 handover][p88] distinguish landed code, scoped decision closures and outstanding integrated proof. Their old manager completion statements do not substitute for the current installed release tuple.

## 3. Minimum shared contract

The contract should be stable enough for R18 to extend. Its meaning must not depend on which client emitted the request.

1. **Identity and authority.** Authenticate realm, actor and project/timeline scope separately from a recoverable writer identity. A writer identity is queue custody and a fencing boundary, not a new privilege. Each logical edit has an ordered identity; each wire attempt has immutable canonical bytes, expected base and idempotency key. Receipts correlate the exact attempt and accepted publication/revision/digest. Scope switching never transfers authority or consumes another writer's pending state.

2. **Reads, effects and inverses.** Preserve the exact supported effect vocabulary, resource/media identity, authenticated base and sequential capture boundaries. Record the addresses and order needed for safe conflict detection and inverse; a writer's earlier queued step is not a foreign edit. A global-premise operation must keep a whole-timeline dependency until explicitly classified otherwise. A detached preview is neither an accepted publication nor permission to overwrite a different head.

3. **Outcomes describe knowledge, not just HTTP status.**

   | Outcome | Required meaning and client action |
   |---|---|
   | accepted | A verified durable receipt identifies the exact attempt. Settle that attempt once. Advance the accepted base without replacing newer optimistic work or regressing a newer cache. |
   | moved | The attempt is known not to have landed because the relevant base/dependency changed. A proven disjoint re-evaluation may form a new attempt; an actual human clash parks the change and its dependent suffix. |
   | refused | A definitive, authoritative refusal proves no effect for that exact attempt. Preserve recoverable intent and explain the reason; do not discard later dependent work. |
   | unavailable | The outcome cannot yet be confirmed or the operation is temporarily unavailable. Keep exact attempt custody and reconcile/retry. This **does not mean “nothing was decided.”** A server may have accepted before the reply was lost or unreadable. |

4. **Keys.** After timeout, disconnect, unreadable success or uncertain response, replay/lookup the same key and exact bytes. After definitive nonacceptance, re-evaluation with another base/body is a **new wire attempt key**, linked to the same logical edit. Never mutate an unresolved flight under its existing key. Idempotency mismatch is not permission to invent a replacement while the first result remains unknown.

5. **Resolution and undo.** Keep mine is a new explicit attempt on an inspected current base, still subject to authorization, media validity and structural rules; it cannot guarantee acceptance. Discard settles only the intended local/parked scope, without deleting another writer's row or an already accepted publication. Undo of queued, in-flight and accepted edits have distinct states; accepted undo is a new guarded inverse, not rewriting immutable history. Cross-actor inverse must be authorized and must park on a subsequent same-address change.

6. **Durability and capacity.** An edit is locally retained only after its custody write succeeds; Saved requires the accepted receipt. Quota failure before capture is an explicit local capture failure, not a server refusal and not saved work. A bounded batch must respect the real body limit, step ordering and inverses. One waiting batch cannot contain an unbounded burst while also promising bounded bytes and time: define a finite supported workload and preserve/explain backpressure at the capacity boundary.

7. **Import and render.** An import key/result, a timeline placement attempt and a render snapshot/output receipt are separate durable identities with explicit dependencies. Content deduplication alone does not establish catalog or placement idempotence. Preserve exact selected media and accepted parent/shot/internal/pack identities. Future P80 clone transport can reuse these content identities; true links require a later negotiated identity/authority contract.

These are proposed amendments, not a claim that the full contract already exists. They retain useful current safeguards and remove contradictions that would otherwise make separate implementation tracks incompatible.

## 4. Numbered findings and minimum amendments

### F1 — BLOCKING: contradictory outcomes and key rules can turn uncertainty into lost work

**Evidence.** [P63 CC-4][p63-tasks] says an unreadable reply is refused; the [plan][p63-plan] describes unavailable as nothing decided. Both are unsafe descriptions of a lost or malformed acceptance. [D11][p63-inputs] says to change expected head while retaining the same key, whereas Runtime [replay lookup][runtime-replay-src] authenticates request hash. Current SDK [flight creation][sdk-flight-src] already distinguishes a new conflict attempt key from its logical identity. CC-4 and CC-4b also disagree over one reason mapping versus mandatory constructor outcomes. Current [App failure classification][app-client] and Runtime response paths are not already one four-outcome protocol.

**Impact.** A client could park/discard an accepted edit as refused, rewrite an unknown flight, or run another operation under a key bound to different bytes. A four-word enum without consistent knowledge semantics would make recovery less safe.

**Minimum change.** Amend CC-4/4b, D11, statements and the existing commit-v2 contract to section 3. Preserve the old-Runtime decoder until the actual minimum-version policy excludes it. Unknown/malformed responses stay unresolved unless a receipt or definitive authenticated refusal settles the exact operation. Specify whether each 401/403/408/429, generic 409, 413, 5xx and integrity error is definitive or uncertain in the actual route; HTTP status alone is insufficient for an uncorrelated proxy reply. Keep one owner for semantic mapping/fixtures, while allowing constructors and transport adapters to implement that same contract. Do not add a universal all-route outcome migration.

**Owner.** P63 Runtime/Agent contract owner; App decoder consumer; P31/P29 own the supported version boundary.

**Verification.** One pinned canned-reply corpus decoded by Agent and App, including old envelopes, malformed 2xx, unknown 409, pre-accept refusal, accepted-then-disconnect and late duplicate ACK. Assert receipt identity, retained bytes/key, no duplicate effect, no loss and no stale-cache regression. This is a proposed proof, not executed here.

### F2 — BLOCKING: isolate same-actor writers and absorb P04 without deleting its guarantees

**Evidence.** [sync.py's default outbox scope][sdk-scope-src] hashes realm, actor, project and timeline. It does not distinguish concurrent writers for the same actor. The [original #1402][shared-actor-issue] and [SC-04][sc04] describe the relevant ownership class; current flight fencing is useful but does not itself create distinct queue homes. App [owner/generation transactions][app-owner-src] already provide important separate safeguards. P04's old CE tasks and P63 touch the same commit/queue authorities.

**Impact.** A second session can find foreign pending/flight state under its own actor scope, block behind it or settle/replay work it did not create. Actor isolation alone misses the two-agent or SDK-plus-CLI case. Editor-plus-agent remains a separate cross-writer acceptance case. Two parallel implementations would create conflicting ownership policies.

**Minimum change.** Give each independent writer a recoverable identity and explicit acquisition/transfer/fence rules inside the existing durable mechanism. Recovery may reacquire its own stored writer state; a fresh session must not silently adopt a stranger's queue. Document expiration/orphan recovery and actor/realm changes without granting new authorization. Absorb P04 delivery into P63's owner lane, mapping every CE requirement to an active task/proof; preserve the old plan/history and its independent concurrency review. Do not revive obsolete implementation branches or add a third queue/merge service.

**Owner.** P63 Agent session/outbox owner, with the P04 safety reviewer and P35 migration owner; App's existing per-owner fencing stays in scope.

**Verification.** Same actor/same timeline with two SDK processes, SDK+App, two tabs and a restarted writer: A's accepted, unresolved and parked requests cannot be replayed, cleared or blocked indefinitely by B. Include a late ACK after transfer/discard, authority changes, disjoint writes, same-address clashes and an abandoned writer. Assert each ledger and exact publication history, not merely that both commands return.

### F3 — BLOCKING: the queue simplification must preserve custody, visible intent and a finite capacity promise

**Evidence.** [localSaveSession][app-session] already retains optimistic work while a save drains. [commitOutbox][app-outbox] persists the exact request and settles atomically under ownership/generation checks. [CC-5a][p63-tasks] proposes a broad burst property with one flight and one waiting batch, but includes a foreign commit without distinguishing a genuine clash; D16 explicitly requires that clash to park. Current task prose also treats row consolidation/deletions as if every older home were redundant.

**Impact.** Replacing proven fences with a simpler-looking row can reintroduce stale completion, cross-tab deletion or reversion. Unlimited accumulated bytes cannot fit a fixed request cap. “No edit is ever refused” is impossible for invalid edits or the owner's required conflict rule.

**Minimum change.** Define one logical custody authority per realm/actor/writer/project/timeline, not one physical row shared by all writers. Preserve capture-before-send, immutable flight, transactional settlement and dependent suffixes. Freeze one batch while it sends, retain later intent separately, and keep each step's inverse. Qualify CC-5a's positive burst property to valid supported edits and disjoint foreign changes; give real clashes their required parked behavior. State a finite fixture/rate/latency/body-size envelope and explicit capacity/backpressure behavior, including a failed local write. Trace empty-queue foreign-head adoption and every real outbox user before deletion.

**Owner.** P63 App queue/model owner; P35 owns old browser-state migration; P85 supplies existing measurement attribution.

**Verification.** Extend the existing model before destructive simplification: interleave edits at every accept/drain point, refusal in the middle, edits during import, local quota/storage failure, abrupt close, two tabs and late callbacks. After each step the accepted receipt, visible document and retained suffix have one explained relationship. Verify migration from actual prior owner/draft shapes and one staged real-stack burst with actual request-size limits. No batch may erase a step or make its inverse unknowable.

### F4 — BLOCKING: bundle and restore recovery cannot wait for P18's general editing verb

**Evidence.** [Bundle publication][bundle-publish-src] requires a caller-supplied key and reaches the guarded v2 commit; the “random key / retired publish route” shorthand in CC-4b/ET-5 is stale. However the inspected path constructs a request from the current bundle and does not retain immutable bytes durably before sending. [P76 ET-5][p76-tasks] already proposes reuse of the pending-record mechanism. App [restoreHistory][app-restore] now forwards the reviewed pair and Runtime [accept/restore][runtime-accept-src] rechecks it; SC-35's older stale-overwrite description is not current. That App method generates a fresh UUID per invocation without visible durable restore custody.

**Impact.** After a lost acknowledgement or restart, reconstructing a bundle can produce different bytes under an existing key; repeating restore with a fresh key can create a new operation before the old one is resolved. These are inspected recovery gaps/inferences, not live reproduced duplicate publications.

**Minimum change.** Pull only ET-5's immutable attempt/result custody into P63 CC-4b, using the existing SDK pending/outbox mechanism. Record detached candidate/base/approval binding and exact serialized request before send. On definitive moved, reattach only when proven safe; no regeneration or silent overwrite. Apply the same exact-attempt rule to supported restore, or prove an existing upstream durable owner supplies it. Keep the existing two-stage restore compare-and-swap. P18 TL-13b remains the later common verb; do not create a separate bundle queue.

**Owner.** P63 Agent bundle/session owner and App history/restore owner, coordinated with P35 recovery.

**Verification.** Bundle/restore accepted then reply lost, client exit before receipt, repeated invocation, current head advanced during review, and a late result after explicit resolution. Reopen must recover the original receipt or safely replay identical bytes/key once. Changed candidate/body under the old key must be rejected. Demonstrate no new generation work or unintended second restore.

### F5 — BLOCKING: preserve authenticated current edits; separate narrow correctness fixes from future acceptance architecture

**Evidence.** Runtime [validate_read][runtime-read-src] checks declared values against their actual input boundary; the Agent also validates capture. [CC-16][p63-tasks] is a proposed address-derived replacement, not a description of a missing present-day authenticity check. [P63's end-state][p63-plan] simultaneously requires the acceptor to apply effects without recomparing the Agent's answer, which is [P75 FS-6][p75-tasks] work. [P76 ET-1][p76-tasks] still has an uncompleted survey of global-premise intents. [D17][p63-inputs] accepts narrow-read stale-premise risk specifically with ET-4b's one-click agent undo safety valve; that task still calls cross-actor inverse authorization unverified.

**Impact.** Removing validation to satisfy a future architecture can accept malformed or unauthenticated edits. Conversely, making all P75/P18 work a dependency inflates R16. Shipping new narrow defaults while deferring their stated safety valve would silently change the accepted tradeoff.

**Minimum change.** Keep the existing validated acceptance path for R16, repairing concrete mismatches/collateral edits through CC-13 and the minimum CC-16 slice actually needed. Before changing read representation, specify sequential bases and prove base-to-current dependency comparisons preserve conflicts; do not simply delete state checks. Scope the effect/inverse vocabulary to shipped operations and refuse unsupported raw mutations honestly.

Keep existing supported disjoint behavior. For new function/document narrow defaults, obtain an explicit owner disposition: either retain conservative current atomic/global semantics for unclassified operations in R16, or bring the intent survey and required ET-4b safety/authorization/proof with the narrowed default. This report recommends the conservative option until evidence justifies the broader one; it does not overwrite D17 by assertion. Full shadow-applier equivalence and FS-6 retirement of validation belong to R18 unless a measured R16 blocker proves the specific slice necessary.

**Owner.** P63 Agent/Runtime semantic owner; P76 owner for D17/ET-1/ET-4b ruling; P18 owns future extensibility. Release synthesis records the actual owner decision.

**Verification.** Use CC-13's gesture-by-target matrix through the actual App handoff and pinned provider: accepted document equals intended document, unrelated fields unchanged, inverse restores the prior state. Include raw/document, occurrence, shot, element/text, pack, media selection and chained records; forge identities/reads/effects/inverses as negatives. Put a foreign write between base and head. Any new default needs a global-premise counterexample and authorized cross-actor undo that parks after a later same-address edit.

### F6 — BLOCKING: retain import-to-placement identity and protect the entire upload lifetime

**Evidence.** Agent [authoring_media.py][author-media-src] enforces 64 MiB and reads the whole source; [media_add.py][media-add-src] reads/validates again. Runtime [server streaming][runtime-stream] and [CAS staging][runtime-cas] already support bounded sized ingestion; the canonical [Python client template][runtime-client-template] has sized object streaming but catalog import coerces bytes. App [timelineLocalSaveHandoff][app-media-guard] still refuses ordinary nonduplicate prepared video/audio. These are bounded P79 seams.

A further source-supported inference is that a parked App retry starts another import even after the earlier import succeeded. [external-drop-utils][app-drop] puts upload inside each attempt and stores tryAgain as the whole run; [useAssetManagement][app-asset-upload] calls prepareMediaImport afresh; [dataProvider][app-import] unconditionally creates a UUID. The within-call [lost-ACK recovery][app-import-recovery] correctly keeps its key, but a later retry does not retain that successful prepared result. The metadata helper catches storage errors, so calling it is not itself proof of durable capture; that failure must be exposed by the revised custody contract. Runtime [catalog operation identity][runtime-import] is keyed separately from CAS content deduplication. No duplicate-catalog incident was executed here.

The placeholder is created with save disabled. [useTimelineCommit][app-timeline-commit] invalidates the reload witness only when shouldSave is true, meaning the edit requests saving; the inspected [persistence pending predicate][app-pending] does not consume active/parked upload lifetime. Parked Files live in React/closure state, and the pending counter is decremented even while parked. This is a missing guard input in the inspected chain; end-to-end behavior remains to be proven.

**Impact.** Removing operation metadata or retrying the whole workflow can orphan or duplicate catalog work, mislabel an import as a saved placement, or lose recoverable dependency information. An update can regard the timeline as safe while a browser-owned File is still needed.

**Minimum change.** P79 LM-4/5 and P63 CC-10 must share one operation key/result, exact prepared selection and dependent placement identity. Reuse the key until import outcome is known; after successful import, retry only the placement. Extend existing transport streaming, not the API/store topology. Remove the artificial limit and complete supported video/audio placement with exact validated selection.

Do **not** implement CC-10's deletion of persistMediaImportOperation without an equivalent durable recovery home and migration. Preserve small metadata/receipts across reload. Do not persist multi-gigabyte File bytes in a new browser spool: retain P79's warning/reselect decision. Supply one lifecycle signal to the existing save/update guard from preparation through acknowledged placement or explicit discard, including parked work. A forced reload/crash may require source reselection; an acknowledged import should not be repeated merely because its placement needs recovery.

**Owner.** P79 media/transport owner, P63 App queue/outcome owner, P35 metadata migration owner and P29 update guard consumer.

**Verification.** Real substantial image/video/audio via App and SDK/CLI; configured server limit, bounded memory, truncation/changed-file refusal. Force import success then placement refusal; repeated Try again must retain one import/catalog selection and one eventual placement. Include lost POST reply plus failed lookup, reconnect, update/reload while active and parked, forced browser reload, reselection, duplicate click and explicit placement discard. A discarded placement must not silently delete an already accepted import.

### F7 — BLOCKING: usable save, undo and restart remain R16 obligations; reconcile the 2s/4s gate explicitly

**Evidence.** The [P89 handover][p89-handover] explicitly says the 2-second median / none over 4 seconds gate moved to R16 with P75 and was **not met**. Current [P89 tasks][p89-tasks], [handoff #1939][p89-issue] and [SC-63][sc63] record materially different workloads: the 300-clip harness result around 6.23 seconds is not the same population as qualifier 13.2/14.2-second evidence or the 616-clip 35/17-second samples. They cannot be averaged into a release claim. [Heavy undo #1932][undo-issue] records an unusable recovery path on its named older tuple, not data loss or a fresh reproduction on today's candidate.

Runtime [history guards][history-guards-src] already make accepted history immutable and classify rollback compatibility. [Deferred verification][history-verification-src] permits only a tightly classified read-only owner while incomplete history verification proceeds; it is not a blanket timeout bypass. P89's large-history owned-copy card SV-L11 and history/startup work remain separate causal investigations.

**Impact.** Moving all speed work to R18 without a gate disposition leaves a prior accepted promise unresolved. An honest Saving/verification message does not make a supported editing or undo journey usable. Conversely, importing the entire 300 ms programme is not justified by one slow stage.

**Minimum change.** Preserve the inherited 2s/4s commitment in the release decision record until its owner explicitly retains or revises it on comparable evidence. Do not accept SC-63's suggested 15/30/45-second limits as a de facto ruling. Define the fixture, history depth, closure/media complexity, cold/warm state, concurrency and end-to-end measurement boundaries before choosing implementation.

Carry the smallest measured work needed for a bounded useful R16 journey: check SV-L11 on the appropriate large-history builder realm; a no-gain small-300 result does not disprove that card. Profile authoritative history lookup/inverse and startup separately. A targeted lookup or resumable verification/checkpoint is justified only by that measurement and an authenticated invalidation design covering realm/store identity, schema/guard version, history prefix and restore/rollback. Do not add a general history-format rewrite or FS-6 by default. Preserve immutable history and fail closed on corruption. Measure import waiting behind a commit as part of the same user journey.

**Owner.** R16 Lead/owner for the gate disposition; assigned R16 P63/Runtime owner for the P89 acceptance/recovery handoff; P85 comparable runner/metrics; Runtime history owner and installer owner for any checkpoint/rollback seam.

**Verification.** One normalized heavy fixture plus explicit history-growth and closure dimensions, before/after on the same exact installed tuple and machine. Record gesture end, dispatch, authoritative acceptance, badge, queued burst tail, undo completion, restart to safe writable state and import delay. Read back actual accepted edits and inverses. Include cold restart, corrupt history and a valid long history; none may be hidden by a warm cache or a looser substitute fixture. The owner must see both retained gate and observed result.

### F8 — BLOCKING: migration and rollback must include pending intent and receipt custody

**Evidence.** [SC-35 and its correction][sc35-correction] identify blocking state-home/migration/authority seams. P63 CC-5/CC-10 changes local owners, drafts and import recovery; the present [outbox][app-outbox] and [SDK flights][sdk-flight-src] contain work not yet represented in accepted Runtime history. [history_guards.py][history-guards-src] explicitly warns that a previous Runtime may require an unguarded backup or stopped-realm rollback preparation. The [q-0016 ruling][q16] requires fresh update/rollback proof for the new required floor.

**Impact.** Treating every local row as a redundant cache can delete the only copy of a user's intent or forget an accepted-but-unacknowledged operation. A rollback of Runtime alone can leave a newer browser/SDK writer interpreting old receipts or replaying into the wrong realm/schema.

**Minimum change.** P35 owns the state classification: preferences, credentials/trust, machine bootstrap, regenerable caches, accepted authority, pending intent, frozen requests and receipts have different custody. Specify migration from actual supported old App/SDK shapes, stop/fence old writers, preserve unknown flights byte-for-byte, and resume only after validating realm/actor/writer and version. Move metadata atomically or leave a recoverable original; no blanket old-store deletion. Pair editor/SDK migration with Runtime backup/schema/guard changes and installer rollback. If an old client cannot safely interpret new state, enforce the existing version/update boundary with a recoverable explanation.

**Owner.** P35 with P63; P09/P29/P31 own installation, version admission and rollback orchestration. INV-04/INV-01 reconcile broader custody/version questions, without moving delivery authority.

**Verification.** Upgrade and rollback with an empty queue, queued edit, unresolved accepted request, parked clash, imported-but-unplaced media and an abandoned writer. Include interrupted migration, restored backup, different realm and stale tab reopening. Assert no cross-scope replay, no lost intent, one accepted effect and an actionable recovery path. Current source heads alone do not prove any of these native transitions.

### F9 — BLOCKING: bind selected work through render and require the missing representative proof

**Evidence.** [managed_timeline.py][managed-render] follows one immutable parent/shot/internal closure after selecting a head. The list/expected-version check and subsequent current-head inspection are separate reads; I did not establish a later/upstream fence that binds them to the user's exact selected accepted revision. [Runtime snapshot binding][snapshot-refs] and [output retrieval][render-output] already provide substantial identity/digest checks. The source does **not** support a blanket claim that rendering freely mixes current child heads.

[P88's final mailbox][p88-mail] and [fixture source][fixture-src] establish the verified-child builder fix and the unproven qualifier-owned heavy rows. Its 250-change edit/readback result does not by itself prove exact-frame/render parity. [SC-87][sc87] preserves the wider installed render obligations and uncertainty.

**Impact.** A coherent snapshot can still be the wrong selected revision if a concurrent edit wins between selection reads. Source repairs and readback-only tests can be mistaken for final proof that heavy saved work renders correctly.

**Minimum change.** Make “render this accepted revision” bind an explicit revision/digest/closure through admission, or explicitly refuse if it cannot be honored. Verify the specific list-to-inspect race before declaring a defect or choosing a fix. Reuse the existing snapshot and output authority instead of adding a new renderer store. Include pack identity and media selection in the retained evidence.

Rerun/retain the repaired 616-clip and large-shots workload as the qualifier's actual disposition requires. Explicitly choose a representative R16 editing/render envelope, with history and closure complexity recorded. Respect the existing 2.6 MB-to-P75 ruling; do not make parity an automatic new R16 prerequisite. Preserve P88's interim ripple path until the P18 TL-3r replacement actually supplies equivalent accepted/inverse behavior.

**Owner.** P87 rendering owner with P63 selection/commit owner; P85/Qualifier own the installed proof lane. The Lead resolves inherited workload gates; INV-05/06 integrate adjacent rendering/qualification concerns.

**Verification.** Capture an accepted parent and exact child/media/pack pins, advance the current head concurrently, then render the chosen revision or receive an explicit stale-selection refusal. Verify output content and managed receipt/digest after restart and retrieval. Also exercise unpublished bundle preview, refused/stale candidate, ordinary media import and heavy edit→save→reopen→render. Keep final qualifier evidence separate from manager handover claims.

### F10 — BLOCKING: current task dependencies do not describe the real shared-file critical path

**Evidence.** [P63 plan/tasks][p63-plan] still describe tracks as independent, while CC-4/4b change shared reply semantics, CC-5 changes custody, CC-10 crosses P79/P35, CC-13 relies on the real provider and CC-16 changes read authentication. [P75 FS-2][p75-tasks] explicitly depends on CC-4/5b's reply and accept branch. [P76 ET-5][p76-tasks] overlaps CC-4b's authoring files. P04's safety work and R15 fixes touch the same authorities.

**Impact.** A nominally parallel schedule can overwrite shared source, require repeated pin churn, or postpone the first useful cross-repository check until all designs are entrenched. A foundation-first rewrite can consume the release before showing the user journey works.

**Minimum change.** Use the contract-first, early-vertical sequence in section 6. One owner reserves shared files at a time. Start the reply corpus, queue model and gesture/readback/inverse corpus early; they define acceptance boundaries before deletions. Do not make every corpus/task wait for every other one, and do not claim independent landing where the protocol or pins are shared. Amend the existing release brief, run board and task dependencies only through the coordinator's later authorized proposal workflow; this report creates no competing delivery plan or tracker.

**Owner.** R16 coordinator/Lead, P63 integration owner and each named interface owner.

**Verification.** Before implementation dispatch, each task has a start dependency, landing dependency, proof dependency and file owner. An early installed vertical must expose writer isolation, lost ACK, undo, import recovery and snapshot render before the full workload matrix. The final freeze records one compatible tuple and remaining owner rulings.

### F11 — FOLLOW-UP: retain compatible R18 growth without shipping its whole programme in R16

**Evidence.** [P75][p75-tasks] owns generic fast saving and effect-application work, [P76][p76-tasks] owns broader collaborative behavior, and [P18][p18-tasks] owns the extensible command/gesture transition. [P80][p80-plan] deliberately puts clone after P79 and makes true links conditional on a later owner decision and contract review. Its proposed “temporarily unavailable” and “stale selection” additions are not yet a negotiated outcome version. The [R18 brief][r18-brief] commissions P18 Phase A only; later editor gestures require a separate scope decision.

**Impact.** A throwaway R16 wire contract would make R18 migration expensive; completing every later mechanism now would expand the authorized release.

**Minimum change.** Preserve extensible reason codes, exact content/selection identities, step/inverse semantics, receipt correlation and versioned compatibility. Keep P75's full 300 ms/FS-6 architecture and P76's richer adoption/presence UX in R18. P18 Phase A's registry/general agent-and-pack verb remains R18; Phase B editor conversion remains subject to its separate later scope decision. P80's clone belongs to R18, while true links remain conditional on their recorded later scope/authority review. Borrow only the specifically justified recovery/correctness slices in F4/F5/F7. Classify future P80 states within the agreed outcome semantics or negotiate a later version; do not add two incompatible fifth/sixth outcomes casually.

**Owner.** P63 contract owner with P18/P75/P76/P80 owners at their authorized starts.

**Verification.** A contract review demonstrates that a new supported operation or clone transport can preserve existing receipts, old-client refusal and immutable media identity. True-link authority, missing/changed source and export portability need their own later review; no R16 live proof is claimed for them.

### F12 — NOTE: targeted source gaps were closed; exhaustive coverage and final qualification were not

**Evidence.** The dispatch explicitly preserves [HOR-01's original blocker][hor01]. I read the missing [P88 handover][p88], [final mailbox][p88-mail], [GPU witness #1952][gpu1952] and [#1384][gpu1384]. #1952 is a proposed witness, not a completed build/run; #1384 retains a final-tuple GPU case-C gap. The served-manifest fetch was unavailable, and [latest qualification status][qualifier-status] did not supply final acceptance.

**Impact.** Calling this an exhaustive safety census or a final installed proof would overstate the work. It would also incorrectly pull a complete GPU/environment programme into an editing investigation.

**Minimum change.** Preserve the original coverage limitation in intake and AUD-01. Route the GPU/environment witness and consent/cost authority to INV-02/Qualifier, and the actual final-tuple/gate reconciliation to INV-06/07. Record which bounded reads resolved which gaps; no implication that the original report has been amended.

**Owner.** Scoping coordinator/AUD-01, with the existing environment and qualification owners.

**Verification.** Independent source index and original immutable links remain available; final acceptance names actual executed evidence and its exact tuple. This note does not prevent submitting this complete original report.

## 5. R16 must ship versus R18 enhancement

| Area | Minimum R16 result | Deferred work and dependency condition |
|---|---|---|
| Multiple writers | Distinct writer custody; safe disjoint supported edits; actual clashes park; no foreign replay or indefinite shared-actor block. Absorb P04 delivery into P63. | Broader collaboration UX/default narrowing is P76; D17's required safety valve travels with any newly enabled narrow default. |
| Save contract / App queue | Exact recoverable attempts, truthful four outcomes, no optimistic reversion, bounded supported bursts, per-step undo, real old-state migration. | P18 Phase A's registry/general agent-and-pack verb remains R18; later editor gesture conversion needs its separate scope decision. |
| Bundle / restore | Preserve current canonical writer and stale-base checks; durable original request/receipt across lost ACK/restart. | General one-verb conversion, not basic recovery, can wait for P18. |
| Reads / effects | Correct supported operations, authenticated capture, preserved base-to-current clash checks and inverse; precise refusals for unsupported writes. | Full FS-6/shadow-applier replacement waits for equivalence and actual need. |
| Heavy acceptance / recovery | Explicitly resolved P89 gate plus measured useful save, queue tail, undo and restart on a representative history/closure workload. | Broad 300 ms programme, unneeded structural optimization and 2.6 MB parity remain with P75 in R18 under the existing ruling. |
| Media | Sized streaming managed copy, ordinary supported video/audio placement, stable import/result/placement identities, guard integration and honest reselection. | P80 clone and true links; multi-GiB browser-byte persistence; full P18 TL-10 conversion. |
| Render | Exact selected accepted snapshot, verified output receipt, representative installed import/edit/save/reopen/render proof. | Broad renderer expansion, whole hardware fleet sweeps and new storage/custody frameworks. |
| Update / state | Pending work and unknown receipts survive supported migration/rollback, with proper fencing and version admission. | Unrelated state/UI redesign. R17's continuous hardening split does not repeal targeted R16 negatives. |

### Concrete canonical amendments for the coordinator

These are instructions for later proposal materialization, **not edits made by INV-03**.

- **P63 plan/statements/inputs/tasks:** reconcile unavailable/refused/moved and D11/D16; remove the unconditional FS-6 implementation premise from R16; state the D17 disposition and P89 gate decision explicitly. Correct the obsolete bundle random-key claim and stale “independent tracks” wording.
- **CC-4/4b:** own one outcome/receipt/version corpus; freeze bundle/restore attempt custody; use existing session storage. **CC-5a/5b/5c:** model before deletions, real owner/fence migration, finite burst/body limits and genuine-clash cases. **CC-7/13:** one reusable long-lived corpus and real gesture/target/accepted/inverse inventory, not another measurement platform. **CC-16:** replace authentication only with proved base-to-current semantics and only where required.
- **CC-10 with P79 LM-4/5:** retain small import metadata and exact successful result; separate import retry from placement retry; wire active/parked upload lifetime into existing update/reload protection. Keep the browser File warning/reselection limit.
- **P04 tasks:** map all historical CE safety obligations into P63, retire duplicate delivery dependency only after owner acceptance, retain read-only concurrency review/proof.
- **P76 ET-5:** hand the narrow recovery slice to P63; leave broader behavior later. **ET-1/ET-4b:** record the accepted-risk dependency; do not enable one while silently deferring the other.
- **P75/P89:** record the owner's exact gate disposition, the smallest cause-driven R16 cards and comparable proof. FS-2 receipt slimming is optional unless measured necessary and depends on the outcome/queue contract. Do not import FS-6 or the full 300 ms goal by implication.
- **P35 and update plans:** classify pending rows/receipts as unique user work, specify migration/rollback/version edges, coordinate one update guard.
- **P87/P85 and R16 qualification:** use the repaired fixture and retained output/snapshot proof; record the 2.6 MB ruling separately from 616-clip/large-shots and history-depth obligations.
- **Release 16 brief/run/decisions:** place the sequence, file reservations, gate rulings and freeze in the existing canonical homes. Preserve active R15/Plan 91 delivery authority and the R17/R18 scope boundaries.

## 6. Recommended sequence, shared files and proof dependencies

Three sequences are credible. An all-foundations-first sequence maximizes architectural uniformity but delays evidence and imports too much P75/P18 work. Fully parallel plan execution starts fast but collides on commit semantics, outbox ownership and pins. **Recommend a short contract/model foundation, one early integrated vertical, then bounded parallel lanes.** This is sequencing advice for the existing run board, not a new implementation dispatch.

| Stage | Start dependency | Work / shared-file reservation | Landing and proof dependency |
|---|---|---|---|
| A. Freeze semantics and workload | Accepted R16 boundary; original evidence available | P63 owns outcome/key/writer/read/inverse contract and canned replies; P35 co-owns custody inventory. Define representative fixtures and resolve P89/D17 rulings. Start CC-5a and CC-7/13 from current supported paths. | The semantics must be reviewed before incompatible deletions or protocol changes land. No need to await a complete future effect engine. |
| B1. Commit/session safety | Stage A interface agreed | Reserve Runtime timeline_commit_store.py, timeline_commit_port.py, timeline_commit_auth.py and errors/server route changes; Agent sync.py, _commit_errors.py, _commit_patch.py and bundle/remote/commit files. P04 safety joins this lane. | Runtime schema/contract and provider must agree; legacy decoder and negative vectors remain compatible. Bundle/restore use the same custody rules. |
| B2. App queue and migration | Stage A fixture and custody contract | Reserve localSaveSession.ts, commitOutbox.ts, runtime client.ts and timelineLocalSaveHandoff.ts. P35 migration reviewed with CC-5/10, not after deletion. | Land against the agreed provider/reply version. Queue model and real accepted-document/inverse rows must stay coherent. |
| B3. Media and targeted usability | Stage A operation identities and workload; source profiling may begin sooner | P79 owns authoring_media.py, media_add.py and sized client import seam; coordinate dataProvider.ts, useAssetManagement.ts and drop/save hooks with B2. The assigned R16 P63/Runtime owner receives the explicit P89 residual handoff and owns cause-driven history/copy/startup work under a Runtime reservation. | Import→placement needs B1/B2 semantics. History changes need guard/backup/rollback agreement. A profile may justify a smaller card or no code; no assumed savings. |
| C. Early installed vertical | Minimal B1+B2+B3 compatible candidate | Two independent writers; one ordinary media import; edit/preview/save; lost reply and recovery; inverse; reopen; exact snapshot render. Use existing direct journey/save-loop and measurement tools. | Fail early on contract/pin/custody seams before full workload expansion. This does not replace later negatives or final qualification. |
| D. Complete retained matrix | Early vertical explained; owners' actual gates settled | Extend supported edit/target combinations, long history, repaired heavy closure, raw/pack writes, migration/rollback and render/output negatives. One reserved fixture/runtime owner and render resource slot avoid interference. | Exact Runtime/schema → Agent/generated client/provider → App pins, manifest/pack/lifecycle identities recorded. Changed claims get targeted reproof; use explicit carryover rulings only. |
| E. Freeze and independent review | One compatible installed tuple; unresolved blockers closed or explicitly ruled | P63 R0 includes absorbed P04 concurrency coverage. P87/P85/Qualifier retain workload and output proof. Installer/state owners supply update/rollback witness. | Freeze the actual tuple and evidence; one R16 publication gate under existing authority. No merge/publication by this report session. |

The high-contention files are not independent team lanes: Agent sync.py and authoring files; Runtime commit store/auth/port, history and server import/reply code; App client.ts, dataProvider.ts, outbox/session/handoff and upload hooks. Assign one integrator per file family and use small reviewed handoffs. Runtime server.py is shared by outcome and media work; dataProvider.ts is shared by import, restore and update/recovery. Explicitly reserve those seams rather than assuming separate plan numbers prevent conflicts.

No calendar duration is asserted: the old effort estimates predate the actual R16/R18 cut and the unresolved workload/default-read decisions. The bottleneck is compatible semantics plus scarce installed heavy/render proof, not the number of nominal projects. Final order must preserve the live R15/Plan 91 authority and use the existing run-board freeze/landing rules.

## 7. Acceptance evidence required — not executed by this investigation

Each row needs the exact installed tuple, fixture identity, request/receipt identifiers and authoritative readback. A screenshot saying Saved or a successful HTTP status is insufficient.

| Journey / negative | Required observable result | Primary owner |
|---|---|---|
| Valid supported gestures on fresh, loaded and just-imported documents | Real App handoff accepted; canonical document equals intended after-state; unrelated state unchanged; accepted inverse restores the start. Include parent, shot, occurrence, track, text/element, raw/document and supported pack edits. | P63 CC-13 / P78 handoff |
| Burst plus foreign writer | Within the agreed finite envelope, visible local intent stays ordered; disjoint foreign work survives; actual clash parks its dependent suffix. One flight, bounded requests and no lost inverse. | P63 CC-5 / absorbed P04 |
| Same actor, independent writers | No queue/key adoption across writers; restart recovers the intended writer; stale callbacks cannot clear another row. No permanent block by abandoned work. | P63 Agent/App |
| Accepted then lost/unreadable ACK | Same bytes/key recover one exact receipt; no duplicate effect, no false definitive refusal, no replacement request while unresolved. Include late ACK and newer head/cache. | P63 CC-4/4b |
| Definitive refusal / local storage failure / quota / invalid request | Known refusal remains distinct from unknown result and failed local capture; parked work and later suffix remain recoverable. Discard/Keep mine acts only on the named scope. | P63 / P35 |
| Bundle and restore across interruption | Candidate/base binding survives; stale restore refuses; restart replays or resolves the original attempt. No regeneration or unintended second publication. | P63 bundle/history |
| Real media, then failed placement | Bounded sized transfer; exact accepted import and selection retained; retry creates no duplicate catalog pair or placement. Forced close explains reselection only where bytes were never retained. | P79 / P63 |
| Active or parked upload during update/reload | Existing guard sees the whole lifecycle; App-controlled navigation/update waits or requires explicit disposition; accepted import survives even if placement is discarded. | P79 / P29 / P35 |
| Heavy history, inverse and restart | Comparable save/tail/undo/startup timings meet the explicitly recorded gate; correct accepted readback; corruption refuses without bypass. Cold/warm and history/closure dimensions recorded separately. | P63/Runtime (P89 handoff) / P85 |
| Selected snapshot under concurrent edit | Exact selected parent/child/media/pack closure renders or explicitly refuses; current-head advance cannot silently retarget. Output receipt/digest survives retrieval/restart. | P87 / Qualifier |
| Upgrade and rollback with unresolved work | One authority, correct realm/actor/writer, exact original attempt retained, no duplicate effect or lost suffix; old history/schema/guard compatibility proved. | P35 / P09/29/31 |
| Final workload and evidence carryover | Repaired 616/large-shots obligations have explicit executed evidence or owner disposition; 2.6 MB ruling remains accurately recorded; final tuple and allowed carryover named. | Lead / Qualifier / P85 |

The existing model, corpus, direct-journey, save-loop, Runtime/provider conformance and P85 measurement surfaces should carry these rows. Do not create parallel infrastructure because multiple plans need the same witness. Invalid, stale-authority, same-size media rewrite, missing/corrupt accepted history, changed pack identity and unsupported old-client cases are essential negatives where they exercise the promised path; broad unrelated test-green work remains with the release's separate hardening policy.

## 8. Decisions and submission disposition

The coordinator can intake this report now. Scope acceptance still needs:

1. An explicit disposition of P89's inherited 2s median / none over 4s gate, with a comparable workload and the smallest justified R16 work.
2. An explicit D17/ET-1/ET-4b decision: conservative current dependencies for unclassified global operations, or the complete narrow-default safety prerequisite, rather than half the accepted tradeoff.
3. A representative heavy history/closure/render envelope and disposition of actual inherited proof rows, respecting the already recorded 2.6 MB handoff.
4. Materialization of the outcome/key/writer/custody and migration/rollback amendments in the actual proposal, followed by the required independent exact-head reviews.
5. Final predecessor/candidate qualification and served/installed identity reconciliation by their existing owners.

These are concrete scope/proof decisions, not requests for this investigator to implement, run tests or mutate the proposal. **Report verdict: REWORK. Report submission readiness is separate from product readiness.** Only this original report is to be committed on the assigned branch; the evidence commit, draft PR, exact remote readback and READY-REPORT receipt belong in the authorized mailbox submission.

## Source links

All code links below are immutable at the reviewed source identity. Mutable issue/PR links identify original claims, decisions and observation history; they are not claims of a newly executed test.

[proposal]: https://github.com/banodoco/astrid-dev/pull/1964
[dispatch-root]: https://github.com/banodoco/astrid-dev/tree/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping
[planning]: https://github.com/banodoco/astrid-dev/tree/1b9c7085beddc220de4c87e628f4112cb6df33e9
[roadmap]: https://github.com/banodoco/astrid-dev/pull/1956
[agent-head]: https://github.com/banodoco/astrid-agent/commit/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5
[runtime-head]: https://github.com/banodoco/astrid-runtime/commit/686ca695469bda48cd40a70824c4ccef2a137284
[app-head]: https://github.com/banodoco/astrid-app/commit/cc1d48f016fde55ad6b0609c619d8a4bcec56823
[vc-head]: https://github.com/banodoco/VibeComfy/commit/55c3948212d23cf037fae8a4c6faad77d33e7279
[scope-workstream]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/scope-release.md
[ctx00]: https://github.com/banodoco/astrid-dev/blob/a7ea0a52d641bbb7799ea141934833285a77ab03/releases/16/evidence/scoping/CTX-00.md
[candidate-manifest]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install-manifest.json
[sense-workstream]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/sense-check.md
[packet-workstream]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/manager/chatgpt-packet.md
[dispatch-workstream]: https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/orchestrator/multi-manager-dispatch.md
[q16]: https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7169735581
[candidate-status]: https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7170071520
[qualifier-status]: https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7170400083
[waveb]: https://github.com/banodoco/astrid-dev/issues/1963#issuecomment-7170537114
[sc63]: https://github.com/banodoco/astrid-dev/blob/6cf0dda31179711582a6ed0d8fcf76d3456c4de9/plans/63-dependable-saving/evidence/release-16-scoping/SC-63.md
[sc04]: https://github.com/banodoco/astrid-dev/blob/cbd951924424ecbad213d3ad999a75ade2aabb51/plans/04-concurrent-edits/evidence/release-16-scoping/SC-04.md
[sc79]: https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md
[sc35]: https://github.com/banodoco/astrid-dev/blob/44d813650b7e8b3726bd41699e80c182db8f79a1/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35.md
[sc35-correction]: https://github.com/banodoco/astrid-dev/blob/ebe295571bb58028fe72d98c3da2cbe7fd40eaa5/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35-severity-correction-01.md
[sc87]: https://github.com/banodoco/astrid-dev/blob/27212e5767406da192e6e822b2a56e59aa284a13/plans/87-render-works/evidence/release-16-scoping/SC-87.md
[iss03]: https://github.com/banodoco/astrid-dev/blob/496ab219fff68b2ad85d762ec995da8d78a1d93a/releases/16/evidence/scoping/ISS-03.md
[hor01]: https://github.com/banodoco/astrid-dev/blob/736712b914dc2b46e6fd66dad2206d573ecf1510/releases/16/evidence/scoping/HOR-01.md
[p88-mail]: https://github.com/banodoco/astrid-dev/issues/1849#issuecomment-7142352430
[app-session]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/commands/localSaveSession.ts#L190-L405
[app-outbox]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/commands/commitOutbox.ts
[sdk-sync]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/sync.py
[sdk-session]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/commit_session.py#L639-L719
[sdk-elements-src]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline_elements.py#L137-L159
[p78]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/78-live-custom-element-editing/handover.md
[bundle-remote]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/authoring_remote.py#L146-L303
[bundle-preview]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/authoring_render_preview.py#L85-L218
[bundle-publish-src]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/timeline/authoring_bundle.py#L1865-L1945
[runtime-store]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_store.py
[runtime-auth]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_auth.py
[app-provider]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts
[app-restore]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L230-L290
[managed-render]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/rendering/actions/render/managed_timeline.py#L696-L1094
[snapshot-refs]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/snapshot_refs.py#L114-L191
[verified-source]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/rendering/verified_source.py#L150-L249
[render-output]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/project_render.py#L394-L914
[p89-handover]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/89-heavy-saves-in-seconds/handover.md
[p88]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/88-timeline-edits-land/evidence/completion-handover.md
[p63-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/63-dependable-saving/tasks.md
[p63-plan]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/63-dependable-saving/plan.md
[p63-inputs]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/63-dependable-saving/inputs.md
[runtime-replay-src]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_store.py#L846-L903
[sdk-flight-src]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/sync.py#L1060-L1154
[app-client]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/client.ts#L290-L394
[sdk-scope-src]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/sync.py#L440-L500
[shared-actor-issue]: https://github.com/banodoco/astrid-dev/issues/1402
[app-owner-src]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/commands/commitOutbox.ts#L289-L361
[p76-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/76-editing-together/tasks.md
[runtime-accept-src]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_store.py#L2210-L2350
[runtime-read-src]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_auth.py#L310-L367
[p75-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/75-fast-saving/tasks.md
[author-media-src]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/authoring_media.py#L20-L145
[media-add-src]: https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/media_add.py#L48-L185
[runtime-stream]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/server.py#L336-L395
[runtime-cas]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/cas.py#L55-L90
[runtime-client-template]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/generators/python_client_template.py#L1185-L1212
[app-media-guard]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts#L731-L779
[app-drop]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/lib/external-drop-utils.ts#L454-L578
[app-asset-upload]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/hooks/useAssetManagement.ts#L480-L547
[app-import]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L1390-L1470
[app-import-recovery]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts#L1740-L1805
[runtime-import]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/service.py#L5667-L6020
[app-timeline-commit]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/hooks/useTimelineCommit.ts#L367-L435
[app-pending]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/hooks/useTimelinePersistence.ts#L1603-L1622
[p89-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/89-heavy-saves-in-seconds/tasks.md
[p89-issue]: https://github.com/banodoco/astrid-dev/issues/1939
[undo-issue]: https://github.com/banodoco/astrid-dev/issues/1932
[history-guards-src]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/history_guards.py#L1-L106
[history-verification-src]: https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/history_verification.py#L1-L110
[fixture-src]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/scripts/save-loop/build-fixture.mjs#L427-L532
[p18-tasks]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/18-timeline-editing/tasks.md
[p80-plan]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/plans/80-use-media-in-place/plan.md
[gpu1952]: https://github.com/banodoco/astrid-dev/issues/1952
[gpu1384]: https://github.com/banodoco/astrid-dev/issues/1384
[r18-brief]: https://github.com/banodoco/astrid-dev/blob/1b9c7085beddc220de4c87e628f4112cb6df33e9/releases/18.md
