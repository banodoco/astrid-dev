# REV-01 — Independent review of the actual Release 16 proposal

**Run:** `r16-scoping` · **Session:** `REV-01-01` · **Verdict: REWORK**  
**Review date:** 25 November 2026. Live observations below carry their own timestamps.  
**Question:** Is the actual materialised proposal complete, coherent, independently shippable as the intended first minor release, and arranged to maximize practical parallel delivery without a major refactor solely for parallelism?

## 1. Verdict, exact identities and limits

**The assessed diff needs bounded amendments before scope acceptance.** It correctly materialises much of the original evidence: narrow producer/consumer joins, two early vertical checkpoints, one publication, preserved P56 and P91 authority, save/undo/recovery constraints, and honest final-tuple proof requirements. The remaining two blocking findings are an undefined retained paid-safety receiver and incomplete adoption of the exact support/negative acceptance set, including the Windows asynchronous-guard witness. Neither finding requires a new architecture or pulling the broad R17/R18 programmes into R16. Findings F03–F06 are concrete follow-ups before affected dispatch, rather than claims that the current proposal authorizes unsafe behavior.

| Identity | Exact value and role |
| --- | --- |
| Assessed proposal base | `ed87d2ef0a437b5ec03818d502e1d7b8540aa65a` |
| Assessed proposal head | **`4e355ca5095843612496a1dc84cf305b0c0fe5ce`** |
| Actual comparison | [Two-commit, 67-file proposal diff][assessed-diff]; commits `5f9266806a72d063848f8e0cf8d5464d38042d51` and `4e355ca5095843612496a1dc84cf305b0c0fe5ce`; base is the merge base |
| Materialisation source reconciliation | Planning main `257a80bab15f753f1164994ca024efd01a4205e0`; this is neither the reviewed head nor the report parent |
| SYN original | `4259785be40565ba940ecb076ca8c9889742d7cf`; SYN assessed the earlier proposal `f8721766ba2fcb7762ca42767749409d00aa2dbc` |
| Required report-only parent | **`9b42590fbe69b68cac07f81abc5d9f2037bc7ba8`**, the distinct dispatch wrapper |
| Assigned report branch and path | `evidence/r16-scoping-rev-01-01`; `releases/16/evidence/scoping/REV-01.md` |
| Draft evidence PR destination | `scope/release-16-scoping-record`, associated proposal [#1964][proposal-pr] |

This is the independent technical/evidence judgment requested by the [pinned dispatch][dispatch], not a rewrite of SYN, scope approval, a product qualification, or permission to execute. The report's eventual Git commit is an evidence identity only; it does not change the immutable assessed pair. Material repairs require a traceable change manifest and independent targeted review of the exact new diff/head. The separate fresh SC-FINAL whole-release judgment and owner scope decision remain outstanding.

### Reading and verification method

The review read all **28 Wave A/B original reports**, both corrections, final AUD-01, SYN-01, the preserved earlier AUD, the owner parallel-direction index, pinned instructions/context, **every full changed head file**, and every old/new diff hunk. The complete source ledger is in §8. Reading was divided among three internal read-only domain readers and the accountable REV-01 reviewer; these are contributions to this one independent packet, not additional external review verdicts. The accountable reviewer read the complete actual diff, full release brief/run/evidence index, full SYN and final AUD, then checked the material findings directly against their original evidence and actual changed locations. No SYN summary or receipt replaced an assigned original.

All 67 head files and their 67 base versions were retrieved completely. All 168 cached original/proposal blobs were reconciled to their GitHub blob identities; a local transport-added terminal newline was removed from the caches without changing source content. Full head plus all diff deletions/context supplied the base semantics; this is not a claim that each reader independently reread every unchanged base line. The release's generated `release-issues` block is byte-identical across the assessed pair, with SHA256 `1746b4767d283a2c9a374339c5a1baf980915f92309dc28e9344a967b19d9f9b`. No generated roadmap or product file is in the changed set.

**No dispatch-required original or assessed file was inaccessible.** The review has narrower limits elsewhere: it did not rerun product behavior, exhaustively retrace all code and every historical issue comment cited by the originals, or independently inspect every raw qualifier image/clip/resource sample. Effective branch protection could not be fully read, and native/hardware/installed acceptance remains future work. Those limits are explicit in §§6–7; the report does not claim complete product or effective-control clearance. Pinned workstreams were read directly; installed skill revision and UI model settings were not independently verified.

No tests, builds, CI dispatch, product execution, paid calls, implementation, proposal edits, task completion, merge, publication, or unrelated issue mutation were performed. Review activity was source/record reading, static document/diff inspection, ordinary TLS reads of public served artifacts, and this report-only submission.

## 2. Numbered findings

### F01 — BLOCKING: the retained paid route names ER-P1 without defining its work or acceptance

**Actual locations:** [P94 tasks][P94-tasks], lines 38–46, and [P36 tasks][P36-tasks], line 28. P94 says experimental paid safety is “detailed §4.16”, but that file has no such section. Its second proposed-reconciliation table repeats the P36 credential prerequisite instead of defining ER-P1. The only `ER-P1` occurrences in the changed canonical proposal are those two credential cells. They do not give an accountable paid owner, bounded outcome, dependencies, proof, or publication join.

**Evidence and consequence:** [ISS-02 F01–F03][ISS-02], [INV-04 addendum §2.6][INV-04-coverage-addendum-01], and [AUD-01 F07/paid coverage][AUD-01] identify distinct obligations: trusted release/cleanup under low disk; known no-create versus ambiguous allocation; duplicate-rent prevention; binding/lease lock ordering; a producer that never acknowledges cancellation; independent expiry under clock skew or host death; exact machine binding; retrievable completed output and settled custody. [SYN §4.16, lines 413–422][SYN-01] proposed an actual ER-P1 receiver and deliberately kept ordinary local setup independent of paid keys and permission. A header saying “Source: SYN-01 original” provides provenance; it does not explicitly adopt this absent task as canonical work.

These are scope/acceptance gaps, not a claim that every historical defect still reproduces. In particular, #1648's recorded incident preserved the clip and the fallback stopped the pod; it does not establish an orphan in that incident. The [#641 owner ruling][issue641-ruling] permits deferral only if paid expiry actually bounds exposure. The direct current issue read still describes #641 as open. Current source or a newer lifecycle main does not prove that the consumed lifecycle pin meets the cap. A dispatcher could complete all defined P94 tasks while leaving this retained experimental route's distinctive money/cleanup safety unowned.

**Minimum amendment:** Add an unchecked, explicitly proposed ER-P1 row in the existing P94 record, or explicitly link an equally complete existing paid-lifecycle receiver. Name one existing paid-lifecycle owner designated by the Lead, with Runtime admission/settlement and P38 function owners. Map the distinct issue/negative cases, first verify current reachability, specify the retained route's publication gate, and keep ER-1/2/5/ER-L independent of paid credentials or spend authorization. Reuse current journal, custody and cleanup machinery; do not import the broad P40/P50 programme. Retain separate owner permission and bounds for any eventual paid witness. If an independent spend bound cannot be established, return an explicit restriction/owner decision for the affected route.

**Accountable owner:** Scoping coordinator for the canonical amendment; Release Lead for the existing paid-lifecycle custodian, with Runtime/P38 consumed interfaces. **Verification:** Exact-new-head readback must resolve every retained paid obligation to one row, owner, dependency and proof, preserve ordinary admission guards, and show no dependency of local implementation or ER-L completion on paid proof. Later authorized no-spend negatives and the bounded provider witness are product verification, not work performed by REV-01.

### F02 — BLOCKING: resolve the complete support and negative-proof contract, including the missing Windows async guard witness

**Actual locations:** [P94 inputs][P94-inputs], line 89, says D4 adopts physical compute cells and the full-journey subset “in §7”; [P38 inputs][P38-inputs], line 152, and [P09 inputs][P09-inputs], line 56, use similar unresolved shorthand. [P93 inputs][P93-inputs], line 77, refers to exact retained cells without naming the accepted set. [Run readiness][R16-run], line 18, requires the retained support/negative matrix but does not bind its full row set. In contrast, [P10 PIN-4][P10-tasks], line 71, explicitly links SYN's immutable support matrix for its six OS×mode cells; that specific adoption is valid and should be retained.

The problem is not simply that historical narrow Windows proof remains in the files: the new precedence clauses correctly supersede conflicting historical scope. The problem is that parts of the replacement acceptance set are left as unresolved section references. In particular, [P38 E1/F1 and its reconciliation][P38-tasks], lines 96–106, do not carry the distinct allowed/forbidden asynchronous network-policy witness. Neither `#682` nor `NEG-WIN-GUARD` appears in any changed canonical file. A native host-spawn/custody pass is not automatically an async-network-denial pass.

**Evidence and consequence:** [ISS-02 F05/F08][ISS-02], [INV-02][INV-02], [INV-04 addendum §2.7][INV-04-coverage-addendum-01], and [SYN §§4.16 and 7][SYN-01] require supported-boundary proof with explicit limits. #682 remains an **unverified hypothesis**, including in the fresh issue read; this review does not report a demonstrated Windows escape. Its bounded resolution is nevertheless necessary before claiming that the affected guard is supported. Likewise, the proposed Windows/Linux RTX-family compute cells, existing Desktop/Portable/Git/Pinokio/MPS journeys, managed Windows/Linux routes, preservation negatives and final exact tuple must have a resolvable owner/task home. A single old Windows/5070Ti witness cannot stand for them all. Eight small physical Win/Linux × RTX20/30/40/50 compute cells are not eight full heavy-model downloads.

**Minimum amendment:** Explicitly propose/adopt the retained matrix in existing task acceptance records, or normatively link its immutable rows with an exact owner/task mapping and limits. No duplicate matrix framework is needed. Replace bare §7/§4.16 references. Carry the Windows native guard witness to P38 E1/F1 or a linked existing security-owner acceptance row: actual installed guard, permitted and forbidden async loopback paths, synchronous controls, exact Windows interpreter/event loop, and truthful disposition. Diagnose first; fix a confirmed gap or explicitly restrict the affected capability. Do not infer a vulnerability, weaken policy, or import a general P15 sandbox rewrite. Keep the two accepted P94 cold/recovery rounds before publication and existing-interpreter feasibility immediately startable.

**Accountable owner:** Release Lead and scoping coordinator, with P09/P10/P38/P93/P94/P34 proof owners and the existing security owner for the guard. **Verification:** Read the new exact proposal and follow every retained support/negative row to a canonical task, accountable owner, required receipt and release join. Owner-selected support limits must be explicit pending decisions until accepted. Native proof itself remains unexecuted; an unknown result must remain unknown rather than becoming a pass or automatic unsupported label.

### F03 — FOLLOW-UP: finish donor handoffs and the promised D17 timing decision record

**Actual locations:** [P75 tasks][P75-tasks], lines 118–124; [P76 tasks][P76-tasks], lines 68–74; [P89 tasks][P89-tasks], lines 32–38, repeat an instruction to record exact handoff/timing cross-references instead of making those mappings. [P63 inputs][P63-inputs], lines 218–224, requests D-SYN-3 for D17 timing, but materialises only D-SYN-2. P76 still describes ET-5 as another implementation after CC-4b, and donor P75/P89 plan/task text retains older R16 ownership labels.

**Why this is a follow-up:** The [actual release brief][R16-brief], lines 24–28, and [P63 receiving rows][P63-tasks], lines 137–150, already establish P63 ownership of minimal ET-5 and the bounded P89 residual, retain the comparable 300-clip 2 s/4 s gate, and keep new ET-1 narrow defaults paired with mandatory ET-4b inverse safety. This is not permission to move all P75/P76 into R16 or to implement the unsafe half of a pair. It is an avoidable ambiguity for a dispatcher working from an individual donor record.

**Minimum amendment:** Record minimal ET-5 → CC-4b; needed SV-L7 semantics → CC-5c; measured save/burst/undo/reopen residual and conditional watermark → CC-17; retain original IDs/status and later residuals. Add the promised pending D17 timing decision, preserving the accepted risk/inverse coupling without pretending the owner has decided. Point the actual donor dispatch/dependency lines to the mapping and preserve SV-L11's checked no-gain history; SV-L12 is not automatically funded.

**Accountable owner:** Coordinator with P63/P75/P76/P89 custodians. **Verification:** One implementation owner and receiving proof per retained donor row, explicit release/timing disposition, unchanged historical completion, no waived save gate, and no ET-1/ET-4b split dispatch. Evidence: [SC-63][SC-63], [INV-03][INV-03], [INV-07][INV-07], [SYN §4.16][SYN-01].

### F04 — FOLLOW-UP: retain the seventh P52 state/search, Claimed

**Actual locations:** [P52 tasks][P52-tasks], new line 209 says “six searches”; retained II-13 at line 26 requires seven. [P52 inputs D14][P52-inputs], line 285, preserves the owner's 17 November addition of **Claimed**, evidenced by a branch, PR or dispatched packet. The older six-search receipt is partial proof, not a removal of the seventh obligation. The new proposal banner otherwise gives the appended wording precedence.

**Impact and minimum amendment:** Change the amendment to “all seven D14 states/searches, including Claimed,” and retain the older receipt's limit. This avoids losing visibility of actual claimed work. It does not require reopening completed implementation, new bots, or issue mutation.

**Accountable owner:** Existing P52 custodian under the recorded Release 14 Lead, with the R15/R16 handoff to be confirmed before dispatch; coordinator corrects the proposed text. **Verification:** Task/input readback retains seven states and the missing witness, original progress, browser/duplicate limits and owner-only transfers. This is a correction the independent review found in the actual materialisation and its compressed SYN wording, not an assumption that SYN was authoritative.

### F05 — FOLLOW-UP: make local start/landing edges and the run-board critical path operational

**Actual locations:** [P79 tasks][P79-tasks], lines 13–21, retain LM-3 after all LM-2 and a fully serial Runtime→pin→LM-2→LM-3 order; [P79 plan][P79-plan], lines 43–49, retains a whole-P77 start/branch barrier based on shared files. [P32 tasks][P32-tasks], lines 845–851, says to replace F4's whole-P12 dependency once the needed interface is verified, but does not yet identify that consumed seam. [Run readiness][R16-run], lines 11–22, tells the coordinator to fill writer/resource reservations rather than showing the linked critical path and current reservations.

The [brief's parallel-start rule][R16-brief], line 20, already forbids whole-plan foundation gates and permits different functions in the same file. The proposal has not dispatched these tasks, so the missing operational resolution is not itself an unsafe execution. However, leaving the old local rows unlabelled can unnecessarily serialize catalog work, distinct-function media handling and native feasibility, or conceal an actual same-function conflict.

**Minimum amendment:** Label the relevant old edges as start, landing or proof. Start LM-3 catalog inventory against already ingested objects, LM-4/5 producer/guard inventory and P32 interface investigation independently; gate only affected consumer landings on the actual contract/pin/shared-function integration. Put a short conditional critical path and links to canonical row groups on the existing run board. Populate real holder, branch/function, next landing contract and scarce proof venue when existing authority makes the lane ready; do not invent sessions, dates or capacity. §4 below provides the review's sequence comparison and conditional path.

**Accountable owner:** Coordinator/Release Lead with P79/P32 and affected consumer custodians. **Verification:** A read-only dispatch review can identify ready work, exact consumed contracts, one writer per actual shared seam, and final proof joins without a new tracker or major refactor. No tests are needed for this planning correction.

### F06 — FOLLOW-UP: align a few retained proof examples with the new governing contracts

| Actual location | Narrow correction, impact and owner |
| --- | --- |
| [P90 UP-1][P90-tasks], line 20, still says rollback to an approved commit plans `ready` | Say that a currently valid grant **and revalidated selected target/dependencies** permit readiness; revoke/restore cannot be bypassed by calling an action rollback. P90/P35 own it. New TR-1 and the plan already distinguish authorization from readiness, so this is not a separate safety blocker. |
| [P38 P1][P38-tasks], line 26, still uses successful `signal(words, 0)` as proof | Distinguish nondestructive identity/liveness observation from an allowed signal to an owned disposable child. [SC-38][SC-38] records current TERM/KILL/USR1 admission; do not broaden signal authority to satisfy an old example. P38 owns it. |
| [P31 RL-2c detail][P31-tasks], lines 123–125, retains direct-push/no-PR/copy-guard prose | Reconcile it with changed O-2 and RL-2b/c at lines 151–156: effective required checks and a generated-only protected writer, preferably the exact generated bot PR. Update the guard's positive/negative examples for the chosen writer. P31 owns it. The actual proposal does **not** authorize blanket bypass; its new explicit rule supersedes this old option. |

**Verification for all three:** Read the revised concrete proof cells against the governing contract; retain current safety and authority. These are documentation/acceptance corrections, not requests to run the proof or rewrite the mechanisms during scoping.

### F07 — NOTE: retain the unresolved horizon/source-coverage blocker and preserve live authority

[HOR-01][HOR-01] reports a secondary-rate-limit interruption, title/truncated search returns, missing P88 direct handoff and incomplete broader GPU/issue/horizon coverage. The [assessed evidence index][R16-index] preserves that original limitation and separately attributes later coordinator P88/GPU follow-up. This review read those records; it does not transform them into exhaustive enumeration. The newer qualification receipts in §6 narrow specific proof gaps, not every horizon gap. In particular, historical delegation of P88's 616 proof was not itself proof, and P88's explicitly deferred 2.6 MB parity remains distinct from the later standard-616 receipt.

**Impact/action/owner:** The coordinator retains the broader source-coverage blocker and its bounded unexamined areas in the existing index until resolved or explicitly dispositioned for scope. Do not erase HOR's original or re-run all discovery without a targeted gap. Preserve existing P56/P52/P53 authority and P91's actual STOP; a proposal saying “already-authorized work” does not revive work stopped by its owner. **Verification:** Exact source-linked resolution and current mailbox/branch readback, with no new competing lane. This note is not a new product-defect claim or clearance of the inherited coverage blocker.

## 3. Every selected outcome and bounded prerequisite

The following is the actual-head disposition, applying the explicit dated-proposal precedence clauses. Historical checked, unchecked, Not recorded, Partial, rejected, moved and post-live states remain historical; appended recommendations are not accepted owner decisions.

| Outcome/home | Actual proposed behavior and review disposition |
| --- | --- |
| [P09 install/update][P09-tasks] | Reuses the existing transaction; actual published origins, changed-schema/lived-in updates, preserved credentials/defaults/tombstones/pending work, per-volume peak space and rollback after new accepted work remain necessary. Old R0 behavior needs an explicit supported transition or truthful refusal/copy-export decision. No invented R2–R8 origin. Exact support adoption needs F02. |
| [P10 Pinokio][P10-tasks] | PIN-2 engine/venue investigation can start now; PIN-3 consumes actual engine authority and reviewed P38 provider. Durable paired App/Runtime recovery precedes editor promotion. Six native OS×hosted/local cells, safe Stop/Quit, and one final publication handoff remain. Blank progress is preserved. |
| [P29 update path][P29-tasks] | One understandable decision, whole pending-work reload guard and exact typed outcomes; current suffixes and historical progress survive. P31 waits on its actual consumed status/manifest seam, not completion of all P29. |
| [P30 everywhere][P30-tasks] | One install-selection/refusal path; actual old-systemd 249/252 launch/result behavior, direct and fully local routes, no foreign-service management. LA-1–7 feed final review. Discovery/adapters need not wait for all update implementation. |
| [P31 first minor][P31-tasks] | Correctly reuses P58, places RL-3 before RL-R/RL-G, retains RL-1e tentative builds, one protected Final and coherent deployment. Required checks versus nonrequired inherited-red proposal remains an owner decision. Effective controls remain unverified, not waived. See §§5–6 and F06. |
| [P38 custody][P38-tasks] | Original-peer native authority, installed-pair closure, parent-incarnation safety, shared lock integration and role migration remain. P1/P2r start together; R/Pub is internal and C1/C2/R2 remain final retained scope, subject to the owner. G2's “later C2” is staged revalidation, not a proved cycle. Missing guard acceptance is F02. |
| [P93 existing environments][P93-tasks] | One selected Placement/observation vocabulary; compatible explicit endpoint can work with unknown filesystem identity; person opens Desktop; no guessed interpreter or lifecycle takeover. CD-5 is explicitly prepublication. Full retained cells need F02. |
| [P94 managed recovery][P94-tasks] | Windows/Linux managed routes, existing Mac/MPS, exact consent/root/journal/last-working recovery, real operator/dtype checks before bulk models, actual peak disk and two cold/recovery rounds. Existing-interpreter compute can start independently. Paid adjunct is missing: F01. |
| [P90 exact workflow][P90-tasks] | WS-2→RS1→WS-9→WS-3 is a real landing chain; donor inspection, fixtures, renderer/adapters start earlier. Approval is separate from target readiness; no-machine preview cannot authorize future mutation. Remote #1861, typed #1910, current witness #1531, revoke/restore and staged rollback are retained. Preserve P56 D1/D6/D7/D8/D12, including the admitted terminal-consent limitation. |
| [P35 state/grants][P35-tasks] | Versioned authority per object/custody phase, pending work and machine bootstrap/receipts/locks stay distinct. S35-4 grant seam can land before bulk S35-2/3 migration; relevant migration precedes old-store retirement. S35-6 joins interrupted copy, stale clients and revoke/restore/rollback proof. No blanket “all state in Runtime” cleanup. |
| [P63 dependable save][P63-tasks] | Exact unknown-ACK request/key/fence custody, distinct writers, authoritative outcome, park/Keep mine/scoped Discard, historical read/inverse compatibility and no blanket equal-rule-error acceptance. CC-13 inverse feasibility precedes CC-5c landing. CC-17 is bounded and measured, not a promise the target is already feasible. |
| [P04 basic concurrency][P04-tasks] | P63 supplies shared implementation; P04 retains its named acceptance, seven SDK/eight hosted outcomes, missing selector/equivalence recovery and cooperative limits. CE-FINAL proof/mapping feeds R0; CE-END/CE-REVIEW is an output of that review, avoiding a circular prerequisite. Not recorded states remain. |
| [P79 local media][P79-tasks] | Actual sized-stream generator seam, add/replace/detached/batch custody, Runtime configured cap (default 5 GiB, not unlimited), deterministic zero/one/many catalog mapping and upload-to-placement lifetime. Original 300 MiB absolute RSS <256 MiB remains. Accepted import retries placement without blind re-upload; D4 reselect/crash limits survive. F05 tightens local start edges. |
| [P87 render/output][P87-tasks] | Retains staged/partial RN history, fresh default pack provision, exact projection/source-clock/background/easing, unknown #2002 cause, separate dimmer-frame cause, native cleanup/lease/next-render recovery and RN-11 proof. #1916 source repair is recognized rather than duplicated. Standard, film, large-shots and deferred P88 parity are distinct. |
| [P85 measurement][P85-tasks] | Existing P81 machinery, frozen arms/bootstrap identities, untimed integrity/load gates and one method/index. MS-4 history can proceed beside runner work. No second benchmark engine, generated dashboard or fabricated 20% pass threshold. |
| [P56 retained residuals][P56-tasks] | Full dated mapping of 14 implementation/skills residuals plus R and WS-L into P90; WS-0f stays within LE-2b, no invented LE-18a. Stage 1 statuses and source-present versus unwired donor distinctions survive. P90 R precedes separately owner-authorized WS-L; no competing P56 delivery lane or blanket divergent-tip merge. |
| [P52 carried intake][P52-tasks] | II-8/9 reopened history, ban on obsolete divergent Agent donor, installed skill-root/text approval and II-12 duplicate/browser limits retained. II-10 remains owner administration. Correct seventh search under F04; confirm existing custodian rather than inventing one. |
| [P53 carried vision][P53-tasks] | Reconcile already-merged App #257/feed work, unticked acceptance, owner wording/table/device look and independent review. VA-11 remains post-live, preventing a publication cycle. No rebuild or reset. |
| [P32][P32-tasks] / [P36][P36-tasks] | Bounded selection/fetch and current credential-reference seams only; keep completed T6d and existing Runtime ownership. Identify actual F4 interface, retain secrets' owner and Windows ACL/redaction/rotation constraints. No wholesale placement or credentials migration. |
| [P75][P75-tasks] / [P76][P76-tasks] / [P89][P89-tasks] | Broader performance/collaboration stays later; minimal ET-5 and measured save residual have P63 receivers. Retained P89 gate is not waived by moving a plan title. Complete donor/timing records under F03. |

## 4. Explicit assessment of the owner's parallel-delivery direction

**Judgment: the proposed hybrid is technically preferable and substantially follows the owner's direction.** [The exact direction][parallel-direction] requires independent starts, real start/landing/proof edges, shared writers, critical path and a comparison of practical sequences, without a major refactor merely to increase parallelism. The actual [Approach][R16-brief] and [run readiness][R16-run] implement the essential policy. Their remaining operational precision is F05. This is not a claim that every named lane already has a free worker or proof venue.

### Workable sequence comparison

| Option | Real benefit | Cost/risk | Review judgment |
| --- | --- | --- | --- |
| Finish all state/custody/foundation plans first | Fewer provisional interfaces to track | Needlessly holds source inventories, fixtures, adapters, catalog work, renderer fixes and native feasibility; discovers cross-product usability late | Reject as the default. A whole-plan gate is justified only by a demonstrated consumed boundary that cannot be isolated. |
| Finish one complete vertical before broad work starts | Early concrete user feedback | Idles unrelated lanes; one GPU/native venue or save problem can delay everything | Use verticals as checkpoints while other work continues, not as a global start barrier. |
| Parallel preparation/implementation with narrow reviewed landings and two early verticals | Finds interface errors early while keeping distinct owners productive | Requires actual shared-function reservations, exact interim tuples and disciplined revalidation | Recommended. It matches the actual proposal, with F01/F02 completeness and F05 operational amendments. |

### Ready work versus genuine joins

| Lane group | Useful independent starts once authorized | Actual landing/proof join |
| --- | --- | --- |
| Release/evidence | P31 record/control inventory, RL-1e design, P85 method/history, source/origin register | Exact required-check policy and coherent consumer/artifact contract; final candidate evidence before RL-R/go |
| Install/update/native | P09 origin fixtures and disk/rollback cases; P10 engine feasibility; P30 selected-install/systemd adapters | Existing transaction/paired recovery and P38 native provider where consumed; genuine supported-route proof |
| State/grants | S35-0 census, S35-1 relevant object contracts, S35-4 grants, S35-5 custody | App and Agent migrations after their actual object contract; current grant before privileged apply; migration before retirement |
| Process/closure | P38 P1 and P2r in parallel after T0/W0; L1/F1 venue discovery | RS1 before affected consumers; shared A1/A3 lock hunk integrated once; C1/C2/R2 and native proof for retained role scope |
| Environment/workflow | CD-0, ER-0/1, existing-interpreter compute, donor/fixture/renderer work | Reviewed observation vocabulary and WS-2/RS1; actual WS-9 producer before apply consumers; newly managed compute after minimum ER-2 install and before bulk transfer |
| Save/concurrency | CC-5a model, CC-7 corpus, CC-13 real capture/inverse feasibility, P04 selector mapping, profiling | Shared outcome/vectors; CC-4b attempt custody; CC-5b writer fencing; CC-5c after individual inverse feasibility; receiving state migration before deletion |
| Media/output | Streaming caller/generator inventory, independent catalog work, drop/guard inventory, pack/theme/source-clock/easing diagnosis | Exact consumed stream/pin and shared media function; import accepted versus placement retry; projection/regeneration writer; known-safe custody before next render |
| Paid safety | Source/reachability, no-spend fixture and lifecycle-cap analysis | Defined ER-P1, current credentials/admission, independent bound and separately authorized retained-route proof; not a start gate for ordinary local work |
| Carried work | P52/P53 current-source/acceptance reconciliation with existing custodians | Exact bounded product residuals join frozen tuple; owner transfers and named post-live observations remain distinct |

**Writer reservations should be at the real conflict.** P38's shared Runtime lock, P90/P56 `_workflow_command` and `target_schema`, the shared readiness/error case table, P63 outcome/vector/queue mutation, shared media add/placement functions, the pack/schema generator, and release pins/generated publication each need one current integration writer. Distinct functions in the same file can be separate assignments. Plan branches record their required inputs; one release integrator orders Runtime/client/Agent/App/manifest/pack pin changes. The proposal's shared existing outbox, installer, uploader, readiness envelope, provider and P58 mechanism are sufficient; no new scheduler, queue, registry or major module split is justified solely for concurrency. [SYN §§5–6][SYN-01] and the concrete task rows above support these inferred reservations.

**Conditional critical path:** relevant producer/identity/schema/grant contracts and their reviews → the slowest retained consumer stream (native custody/roles, managed/exact workflow, save/inverse/migration, media/output, or supported install/update) → one coherent pin convergence → final changed-schema/lived-in/native/support/negative/heavy proof → RL-R and required final qualification reviews → exact-head owner go → one protected Final/generated deployment → served readback and named post-live observations. The maximum changes with measured residuals and venue availability; there is no evidence for a fixed elapsed date. P38 role scope, native engine feasibility, real GPU/OS witnesses, save target feasibility and unknown output/descriptor causes are plausible critical resources, not proven duration estimates.

**Two early checkpoints are useful and independent.** Existing local ComfyUI → read-only plan → decline → approved built-in transfer → correct result tests the setup seam. Above-old-cap media → edit → lost ACK → undo → reopen → short render → safe next render tests the custody seam. Neither needs all managed provisioning or all native-role work to begin, and neither qualifies those later dimensions. Changed pins, schemas, grant/revoke policy, state/outbox recovery, projection, fixture, installer/engine/native owner or measurement boundary invalidate the affected proof. A reviewed no-product-effect statement may retain unrelated evidence; it cannot transfer required status or owner approval to a changed head.

Heavy CPU/disk/GPU/native runs need quiet, named reservations and raw resource records. Reserve proof venues early without holding all coding. Use actual authorized capacity; the scoping session ceiling is not evidence of an eventual product worker count. R15 has now published (§6), but that observation does not silently grant another session's CI or machine allocation. No shared limit or existing authority was changed by this review.

## 5. First-minor publication, usability and pending owner choices

The actual P31 table repairs the important order: RL-3 version display precedes the first R16 Final; RL-R depends on RL-3 and evidence; RL-G is the one final owner action. P58 remains the record/generator authority. The generated issues block is preserved. Draft/strategy edits, tentative RL-1e builds and internal P38 Pub do not publish. The old publisher/guard stays until coherent replacement enforcement is effective, and App deployment is held or its mixed-version interval is proved. Full SHA/digest/platform/bootstrap/pack identities, source ancestry, served bytes and deployment identity remain different evidence dimensions. [P31][P31-tasks], [P31 inputs][P31-inputs], [INV-01][INV-01], [INV-06][INV-06].

R16 can be scoped independently of P91's R17 green programme only under an explicit gate. The proposed mode requires **every effective required check** and retained journey on the exact candidate, complete comparable executed inventories, and no new/lost/unclassified or harmful failure. An individually evidenced nonharm inherited failure in a nonrequired job is a proposed owner exception, not a blanket waiver based on age or equal counts. The current unknown #2002 causes and unsupported execution gaps cannot be called harmless by label. Preserve full ID/job/OS/configuration accounting, shard and duplicate/subtest boundaries, and explain missing results. If the owner retains literal all-green, meet it or hold. No protection change or assertion weakening is authorized here.

The P89 comparable **300-clip median ≤2 s and no observation >4 s** gate remains a proposed carried acceptance obligation, with CC-17 baseline/profile and bounded repair. The two new 616-clip 30.315/32.046 s observations are a different fixture/measurement and neither demonstrate nor mechanically adjudicate that 300-clip gate. P75's broad 300 ms programme stays later. Missed feasibility returns to an evidence-backed owner decision; moving scope labels cannot waive usable save/undo/reopen. P85's provisional 20% alert is not a replacement pass threshold. [P63][P63-tasks], [P89][P89-tasks], [P85 inputs][P85-inputs], [INV-03][INV-03], [INV-06][INV-06].

The following decisions remain pending in the actual proposal; none is manufactured by this review:

- Qualification mode and any individually justified nonrequired-red exception; effective enforcement and owner approval identity.
- Exact retained save gate and a response if bounded measured repair cannot meet it.
- Managed Windows route and supported hardware/architecture/journey limits, with exact owned acceptance under F02.
- P38 retained role scope, rather than assuming role conversion is a necessary concurrency refactor.
- Grant revoke/restore semantics and D17 timing, preserving existing P56 consent decisions and the ET-1/ET-4b coupling.
- P52/P53 current custodian/closure boundary, R0 legacy handling where needed, and separately authorized machine/media/spend for reserved live proof.

The actual served anchor is now R15/floor15. P31 must carry the real floor unless the owner explicitly approves a higher one and its behavior; intended 0.1.0 does not itself make R16 mandatory. Preserve truthful legacy fallback rather than inventing semantic releases or Final records for unpublished integer candidates. A hard cut may retire obsolete implementations only after verified transition; it cannot discard accepted history, pending edits/imports, choices, environments or recoverable newer work.

## 6. Refreshed source, served state and handoff drift

These observations update the evidence register without substituting a moving main for the assessed head. Public/source/installed/deployed identities are deliberately distinct.

### Source observations

| Repository/ref | Observed full identity | Meaning |
| --- | --- | --- |
| astrid-dev main | `a9da325e274a70a249239d1f95913495797780ee` | Four commits beyond reconciliation source `257a80bab15f753f1164994ca024efd01a4205e0`; qualification receipts, tester-path updates and other planning work |
| astrid-agent main and release/15/main | `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` | Observed equal; also served Agent pin |
| astrid-runtime main and release/15/main | `686ca695469bda48cd40a70824c4ccef2a137284` | Observed equal; also served Runtime pin |
| astrid-app main and release/15/main | `cc1d48f016fde55ad6b0609c619d8a4bcec56823` | Observed equal; contains the matching public manifest/bootstraps |
| VibeComfy main and release/15/main | `55c3948212d23cf037fae8a4c6faad77d33e7279` | Observed equal; served pin is not an installed-machine attestation |
| astrid-pinokio main | `1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb` | Launcher source identity; not a native engine witness |
| runpod-lifecycle main | `f2948817eeb94af8dee76be21f6d673724f1606e` | Distinct from consumed pin `9f88ef7640bc664f697112d966ecefa123d44340` |
| Agent retained release/16/plan-91 | `514499debc902643a03aee3f0ed68b710c5d3ead` | Preserved stopped lane; no retarget, rename, deletion or new dispatch |

The branch GETs and [planning-main comparison][main-drift] were read during this review. The touched P31 plan/tasks drift is the platform-neutral `tester-brief.md` / `test-matrix.md` reference change; the assessed head retains its earlier filenames and must be reconciled before future execution. No wholesale merge or retarget was performed. Source snapshots: [Agent][agent-source], [Runtime][runtime-source], [App][app-source], [VibeComfy][vibe-source], [launcher][launcher-source], [lifecycle main][lifecycle-source], [consumed lifecycle][lifecycle-pin], and [retained P91][p91-source].

### Actual served bytes

A normal-TLS, no-cache-request read returned HTTP 200 for all five resources at **25 November 2026 21:59:49 CET (20:59:49 UTC)**. An earlier manifest read at 21:51:15 CET (20:51:15 UTC) already showed the same R15 bytes. The public page extraction endpoint could not parse the manifest; the direct ordinary HTTPS read succeeded without bypass or escalation.

| Resource | Bytes | SHA256 |
| --- | ---: | --- |
| [install-manifest.json](https://astrid.haus/install-manifest.json) | 5469 | `3ccc767c11fa0d08551bce7e73f88e72877a9657fb8dec08dc20ac3a4739e4bb` |
| [install](https://astrid.haus/install) | 6302 | `c268a5fae7ff318414745cee7bfcec13b6d7a81434f7aaa10d218ffe28248fff` |
| [install.sh](https://astrid.haus/install.sh) | 162 | `591c4c51b148fccef2a7d1c45782d9ff949d5fd03d46cd82b5591e3a23d1b285` |
| [install.ps1](https://astrid.haus/install.ps1) | 18682 | `ea581d5d7c2d02f9f062dc15affabe1f7c3e38d641984cecf4797f13ac58b3a9` |
| [build.json](https://astrid.haus/build.json) | 60 | `ec989a1ae95599b4eea27dfe1d547ec41a443d841569954c666d1d010b3253fa` |

Manifest **release15/required.release15** names the Agent/Runtime/Vibe pins above, Runtime schema `sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2`, lifecycle `9f88ef7640bc664f697112d966ecefa123d44340` version `0.3.1.dev0`, and motion pack `2379ab54aca522019ff4f869cfdf9375bdb56dfc` / digest `75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029`. Tools are uv0.11.32, Python3.11.13, Bun1.3.14, Node20.19.4, ffmpeg7.0.2, OMP `78f0e0960f471c2c62b943272a48c33366f239fe`; the complete served manifest includes platform asset hashes.

Git blob hashes of the served manifest and all three bootstraps exactly match [App cc1d48f0 public sources][app-public]: manifest `a6112a518dd34baf3bf66fffc94ad4c05f577f73`, install `ea31b6ddce7bfa7cddd9701b66db650568fb01e7`, shell shim `d8b02a727072f833586b61606177c226d243880e`, PowerShell `60f63e0a5564861b387532e97e404d9a3085f420`. `build.json` reads `{"app":"908735e4-bfcf-4177-b984-1e1f60553e67","release":15}`. The UUID is a deployment identity, not an App commit; matching public static bytes does not prove every running backend or installed machine matches source. SYN's earlier R14/floor14/other UUID observation remains accurate at its own timestamp and should not be rewritten.

### Qualification evidence changed, with specific limits

The new [R15 qualification README][qualification] and direct raw summaries/receipts at planning main `a9da325e…` establish more than the original historical delegation alone:

- [Standard-616 verification][standard616] records complete decode, 1920×1080/30fps, audio and selected colors, 233 s and 6,990 frames. “Standard616 was never observed” would now be stale.
- [Film declared verification][film-declared] records 1280×720/30fps, 195.967 s and 5,879 frames. The failed 1920 expectation was a qualifier expectation error. This does not establish every original film/heavy extent. The [same-source frame comparison][film-comparison] still has an unexplained dimmer 3 s result; do not invent a shared cause with #1931 or #1909.
- [Two-save receipt][two-saves] has attributable 30,315 ms and 32,046 ms Saved marks, actual edits, 616 clips, fresh-reload equality and equal nonempty digests. Its timing/identity/reload fields were inspected; not every large clip array/resource sample was semantically reread. It is not the comparable 300-clip gate.
- The installed save/render App is `7676df48f4104fb8ebe2b19de64dea25b9ec3dc7`; CI by-ID App is `cc1d48f016fde55ad6b0609c619d8a4bcec56823`. The README explicitly does not assert identical trees. The [R15 owner decision][r15-owner] describes the required-floor-only candidate change, but that is not permission to transfer all future R16 evidence. VibeComfy installation is unverified in these receipts; motion pack was manually installed/pin-checked. Standard render RSS ≥7.9 GB is a sampling lower bound and load overlapped comparisons.
- Full by-ID summaries retain new/previously absent Agent cases, including 15 descriptor causes not established and other timeout/shim impact groups. App E2E's 85 failed results represent 80 distinct IDs. Historical matching does not classify harm. Latest [qualifier comment][qualifier-latest] reports unchanged verdict and aggregate Direct Journey success; this review did not independently reread every job of that run.

No enumerated large-shots receipt, complete native Mac custody, over-30-minute lease witness, all assigned repeated RN-10 extents, RN-11 installed-wheel/revert sensitivity, or P88 deferred 2.6 MB parity is established by this bounded refresh. These receipts do not qualify an R16 product candidate. Preserve exact predecessor receipts and require affected final proof later.

### Live custodians and controls

The [P56 DONE handoff][p56-done] reports Stage1 shipped with R15, while Stage2 donors and #1861/#1910/#1928 remain R16 and untouched; WS-L and the owner's installation remain reserved, and `p56/*` deletion is not authorized. The latest two relevant comments were read in full, not all 571 historical comments. The proposal's residual mapping agrees with this handoff.

P52/P53 current headers retain the Release 14 Lead `session_011EzfW3Zy19ncNecpQnKb7D` and require an explicit handoff/disposition. [Owner comment][r15-owner] places their bounded residual in R16. App [#257][app257] was already merged on 13 November at `8938caa82f4c3e805d8f03e9983b20b260f778a2`. The proposal correctly does not claim new completion or authority.

All six P91 mailbox comments were read. The [owner STOP][p91-stop] and [manager acknowledgement][p91-ack] remain the latest actual instructions; no resume was observed. The retained branch is unchanged. R17 is the intended destination, but the existing Lead/orchestrator must coordinate its destination/proof handoff. Historical launch text is not fresh authorization.

Read-only [dev ruleset27040267][dev-ruleset] remains active on the default branch, with approval count0, no code-owner requirement/stale dismissal, `documentation` and `vision-consumer-contract` contexts, strict=false and an always-bypass integration. The App ruleset list returned `[]`; that cannot prove absence of inherited/classic/effective protection. Effective branch-rule endpoints were rejected by the connector, and classic `branches/main/protection` reads for dev and App returned **403 Resource not accessible by integration**. No settings were changed or access boundary bypassed. Effective checks/permissions at every actual public write/deploy boundary therefore remain **unverified**. P31's proposed proof gate is correct to demand them before cutover; this review cannot mark that implementation gate satisfied.

## 7. Repair and acceptance handoff

1. Coordinator materialises F01 and F02 in the existing canonical records, preserving exact source/status history and pending owner choices. Resolve F03–F06 before the affected dispatch; do not silently implement donor instructions as a second lane.
2. Publish an exact old/new change manifest and new proposal head. An independent targeted review checks those amendments plus their affected interfaces/matrix/critical path. This report's judgment remains about `4e355ca5095843612496a1dc84cf305b0c0fe5ce`; it does not pre-approve a hypothetical repair.
3. Carry forward HOR's broader coverage blocker, current served R15 baseline, incomplete native/effective-control evidence and unclassified causes with explicit owners. Fresh SC-FINAL challenges the revised whole release and practical sequence.
4. Owner accepts scope and pending decisions separately. Only the existing delivery authorities subsequently authorize implementation/proof/publication. Final owner approval must identify the actual frozen tuple and ledger, invalidate on material change, and precede one protected publication with complete served readback.

**Report delivery may be READY-REPORT while its review verdict is REWORK.** This original review is the sole authorized repository addition. No product or assessed-proposal changes, tests/CI, merges, issue-state mutations, branch retargeting or publication accompany it.

## 8. Full-read coverage ledger

The following tables are a ledger of files actually read through EOF, not merely retrieved. `E` = environment/state/custody reader; `Q` = release/qualification reader; `M` = editing/media reader; `R` = accountable REV-01 reviewer. Exact immutable source links resolve the full originals. Line totals count physical source lines, including internal blank lines, without counting a fictitious line after the final newline. Earlier reader logs included that terminal empty display line; no prose was omitted.

### Original reports and corrections

| Complete original | Immutable commit | Lines | Full readers |
| --- | --- | ---: | --- |
| [SYN-01][SYN-01] | `4259785be40565ba940ecb076ca8c9889742d7cf` | 903 | R, E, Q, M |
| [SC-09][SC-09] | `52c40028c067047533e222a017c92ac17f8cf5ba` | 225 | Q |
| [SC-10][SC-10] | `d358b3b9de02c156d8a5576495256d6dea73c577` | 156 | Q |
| [SC-29][SC-29] | `68849637ddb2fb007289983727bc66e303328580` | 111 | Q |
| [SC-30][SC-30] | `75d69e848eaa0760993e7be3a7c13c5fa7a0f19c` | 106 | Q |
| [SC-31][SC-31] | `25ced2a35b4677532911aaa61127fc9452be59b7` | 161 | Q |
| [SC-38][SC-38] | `7687ef518c86998f610ff4cf963e58b0565f38a1` | 102 | E |
| [SC-93][SC-93] | `ace8e01a9455b97971691209682f65f568efcfda` | 126 | E |
| [SC-94][SC-94] | `81105a08717746d0393ccf3bb126f8c71bbe2471` | 116 | E |
| [SC-90][SC-90] | `1bd93cf70f169e0db52f95ced5b8f9d189865539` | 153 | E |
| [SC-35][SC-35] | `44d813650b7e8b3726bd41699e80c182db8f79a1` | 119 | E |
| [SC-63][SC-63] | `6cf0dda31179711582a6ed0d8fcf76d3456c4de9` | 144 | M |
| [SC-04][SC-04] | `cbd951924424ecbad213d3ad999a75ade2aabb51` | 58 | M |
| [SC-79][SC-79] | `ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1` | 81 | M |
| [SC-87][SC-87] | `27212e5767406da192e6e822b2a56e59aa284a13` | 129 | M |
| [SC-85][SC-85] | `799938e9ebcb2d8d97d078a27d448635ed7f7b5c` | 85 | Q |
| [SC-56][SC-56] | `74eb2950b33233b076536f3178b1daaa86f675b1` | 96 | E |
| [ISS-01][ISS-01] | `1d8323ccf295f355628d5421701b1b0a0a40a8d0` | 54 | Q |
| [ISS-02][ISS-02] | `9e34444b3c9269d42293ab30558561495d678e3b` | 115 | E |
| [ISS-03][ISS-03] | `496ab219fff68b2ad85d762ec995da8d78a1d93a` | 91 | M |
| [ISS-04][ISS-04] | `e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00` | 170 | Q |
| [HOR-01][HOR-01] | `736712b914dc2b46e6fd66dad2206d573ecf1510` | 157 | M |
| [INV-01][INV-01] | `17617b57cc0b4d0485ea68211b84b675f9b6c053` | 263 | Q |
| [INV-02][INV-02] | `f73732fbf825241f7be3f6204840e166a5f62c86` | 449 | E |
| [INV-03][INV-03] | `5d924e96aee1a2afdaeeb86131f698f5a57a5daf` | 432 | M |
| [INV-04][INV-04] | `9e8411372fc9a0257175d0f49da65ba7bee77bbb` | 137 | E |
| [INV-05][INV-05] | `22d9be23d3001ca7dabb4b2e90fc38b8b59657bf` | 90 | M |
| [INV-06][INV-06] | `f530e9b60391de8f60f8e38983038cf4615fa7e3` | 142 | Q |
| [INV-07][INV-07] | `ca85e04c05968ad8cb5d4b562e17045283018ce9` | 146 | Q |
| [SC-35-severity-correction-01][SC-35-severity-correction-01] | `ebe295571bb58028fe72d98c3da2cbe7fd40eaa5` | 17 | E |
| [INV-04-coverage-addendum-01][INV-04-coverage-addendum-01] | `1e38786e3560d979b246a0ad0526920f4e3aa2ce` | 78 | E |
| [AUD-01][AUD-01] | `43e3e390d6ffe026e6f2a61f0c866b0ac94daf9b` | 328 | R, E, Q |
| [AUD-01-earlier][AUD-01-earlier] | `c9a3ec2b275a3e0d4bf9013255237d41ce2355f1` | 129 | R |
| [parallel-direction][parallel-direction] | `6def0198c7a9a89f0e85b97582ef287274ef73a9` | 139 | R |

The earlier AUD is an exact byte-prefix of the completed AUD. Its preserved partial/limited verdict was not substituted for the final continuation. The owner direction was read both in the pinned original index and in the complete assessed evidence index. Original source/search/qualification limits remain attached to their claims.

### Full changed files and all assessed diff hunks

All files below are at the fixed assessed head; corresponding base content and every diff hunk were read. R additionally read the whole 67-file diff. `—` means that file was not changed, not an unread changed file.

| Directory under plans/ | Full plan.md | Full inputs.md | Full tasks.md | Full reader |
| --- | --- | --- | --- | --- |
| `04-concurrent-edits/` | [plan (47 lines)][P04-plan] | [inputs (37 lines)][P04-inputs] | [tasks (96 lines)][P04-tasks] | M |
| `09-install-and-update-confidence/` | [plan (77 lines)][P09-plan] | [inputs (62 lines)][P09-inputs] | [tasks (313 lines)][P09-tasks] | Q |
| `10-pinokio-qualification/` | [plan (72 lines)][P10-plan] | [inputs (33 lines)][P10-inputs] | [tasks (71 lines)][P10-tasks] | Q |
| `29-update-and-release/` | [plan (118 lines)][P29-plan] | [inputs (117 lines)][P29-inputs] | [tasks (558 lines)][P29-tasks] | Q |
| `30-update-everywhere/` | [plan (62 lines)][P30-plan] | [inputs (30 lines)][P30-inputs] | [tasks (41 lines)][P30-tasks] | Q |
| `31-releases-from-astrid-dev/` | [plan (95 lines)][P31-plan] | [inputs (78 lines)][P31-inputs] | [tasks (158 lines)][P31-tasks] | Q |
| `32-generation-placement-targets/` | [plan (132 lines)][P32-plan] | — | [tasks (851 lines)][P32-tasks] | M |
| `35-one-home-for-user-state/` | [plan (63 lines)][P35-plan] | [inputs (32 lines)][P35-inputs] | [tasks (42 lines)][P35-tasks] | E |
| `36-one-credential-path/` | [plan (36 lines)][P36-plan] | — | [tasks (28 lines)][P36-tasks] | E |
| `38-one-process-identity/` | [plan (121 lines)][P38-plan] | [inputs (158 lines)][P38-inputs] | [tasks (106 lines)][P38-tasks] | E |
| `52-issue-intake/` | [plan (123 lines)][P52-plan] | [inputs (306 lines)][P52-inputs] | [tasks (209 lines)][P52-tasks] | Q |
| `53-vision-aspirations/` | [plan (122 lines)][P53-plan] | [inputs (301 lines)][P53-inputs] | [tasks (148 lines)][P53-tasks] | Q |
| `56-workflow-setup/` | [plan (58 lines)][P56-plan] | [inputs (95 lines)][P56-inputs] | [tasks (76 lines)][P56-tasks] | E |
| `63-dependable-saving/` | [plan (134 lines)][P63-plan] | [inputs (224 lines)][P63-inputs] | [tasks (150 lines)][P63-tasks] | M |
| `75-fast-saving/` | [plan (71 lines)][P75-plan] | — | [tasks (124 lines)][P75-tasks] | M |
| `76-editing-together/` | [plan (65 lines)][P76-plan] | — | [tasks (74 lines)][P76-tasks] | M |
| `79-local-media-any-size/` | [plan (74 lines)][P79-plan] | [inputs (76 lines)][P79-inputs] | [tasks (27 lines)][P79-tasks] | M |
| `85-one-place-to-measure/` | [plan (70 lines)][P85-plan] | [inputs (85 lines)][P85-inputs] | [tasks (26 lines)][P85-tasks] | Q |
| `87-render-works/` | [plan (137 lines)][P87-plan] | [inputs (167 lines)][P87-inputs] | [tasks (109 lines)][P87-tasks] | M |
| `89-heavy-saves-in-seconds/` | [plan (48 lines)][P89-plan] | — | [tasks (38 lines)][P89-tasks] | M |
| `90-workflow-setup-exact-plan/` | [plan (59 lines)][P90-plan] | [inputs (43 lines)][P90-inputs] | [tasks (31 lines)][P90-tasks] | E |
| `93-comfyui-desktop-and-existing-environments/` | [plan (125 lines)][P93-plan] | [inputs (77 lines)][P93-inputs] | [tasks (36 lines)][P93-tasks] | E |
| `94-dependable-environment-setup-and-recovery/` | [plan (148 lines)][P94-plan] | [inputs (89 lines)][P94-inputs] | [tasks (46 lines)][P94-tasks] | E |

| Full release file | Lines | Full reader |
| --- | ---: | --- |
| [releases/16.md][R16-brief] | 129 | R |
| [releases/16/evidence/scoping/README.md][R16-index] | 153 | R |
| [releases/16/run.md][R16-run] | 90 | R |

Also read: full dispatch/REV packet/shared procedure/context/CTX-00/CTX-01 at the wrapper; the four pinned workstreams at `7060b764ec16a638b0e6774f814eabf6d7b70c04`; the complete unchanged R18 brief at the assessed head; targeted current source/handoff records described in §6. Supplemental current raw receipts were read to the exact extent stated there. This is not an exhaustive new issue search, all historical comments, all private tester artifacts, a native experiment, or a test-suite pass.

## 9. Source links

Reference definitions below pin assessed files and original evidence separately. Live service/issue/ruleset links are explicitly timestamped observations in the text; immutable report/source links preserve their content basis.

[SYN-01]: https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md
[SC-09]: https://github.com/banodoco/astrid-dev/blob/52c40028c067047533e222a017c92ac17f8cf5ba/plans/09-install-and-update-confidence/evidence/release-16-scoping/SC-09.md
[SC-10]: https://github.com/banodoco/astrid-dev/blob/d358b3b9de02c156d8a5576495256d6dea73c577/plans/10-pinokio-qualification/evidence/release-16-scoping/SC-10.md
[SC-29]: https://github.com/banodoco/astrid-dev/blob/68849637ddb2fb007289983727bc66e303328580/plans/29-update-and-release/evidence/release-16-scoping/SC-29.md
[SC-30]: https://github.com/banodoco/astrid-dev/blob/75d69e848eaa0760993e7be3a7c13c5fa7a0f19c/plans/30-update-everywhere/evidence/release-16-scoping/SC-30.md
[SC-31]: https://github.com/banodoco/astrid-dev/blob/25ced2a35b4677532911aaa61127fc9452be59b7/plans/31-releases-from-astrid-dev/evidence/release-16-scoping/SC-31.md
[SC-38]: https://github.com/banodoco/astrid-dev/blob/7687ef518c86998f610ff4cf963e58b0565f38a1/plans/38-one-process-identity/evidence/release-16-scoping/SC-38.md
[SC-93]: https://github.com/banodoco/astrid-dev/blob/ace8e01a9455b97971691209682f65f568efcfda/plans/93-comfyui-desktop-and-existing-environments/evidence/release-16-scoping/SC-93.md
[SC-94]: https://github.com/banodoco/astrid-dev/blob/81105a08717746d0393ccf3bb126f8c71bbe2471/plans/94-dependable-environment-setup-and-recovery/evidence/release-16-scoping/SC-94.md
[SC-90]: https://github.com/banodoco/astrid-dev/blob/1bd93cf70f169e0db52f95ced5b8f9d189865539/plans/90-workflow-setup-exact-plan/evidence/release-16-scoping/SC-90.md
[SC-35]: https://github.com/banodoco/astrid-dev/blob/44d813650b7e8b3726bd41699e80c182db8f79a1/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35.md
[SC-63]: https://github.com/banodoco/astrid-dev/blob/6cf0dda31179711582a6ed0d8fcf76d3456c4de9/plans/63-dependable-saving/evidence/release-16-scoping/SC-63.md
[SC-04]: https://github.com/banodoco/astrid-dev/blob/cbd951924424ecbad213d3ad999a75ade2aabb51/plans/04-concurrent-edits/evidence/release-16-scoping/SC-04.md
[SC-79]: https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md
[SC-87]: https://github.com/banodoco/astrid-dev/blob/27212e5767406da192e6e822b2a56e59aa284a13/plans/87-render-works/evidence/release-16-scoping/SC-87.md
[SC-85]: https://github.com/banodoco/astrid-dev/blob/799938e9ebcb2d8d97d078a27d448635ed7f7b5c/plans/85-one-place-to-measure/evidence/release-16-scoping/SC-85.md
[SC-56]: https://github.com/banodoco/astrid-dev/blob/74eb2950b33233b076536f3178b1daaa86f675b1/plans/56-workflow-setup/evidence/release-16-scoping/SC-56.md
[ISS-01]: https://github.com/banodoco/astrid-dev/blob/1d8323ccf295f355628d5421701b1b0a0a40a8d0/releases/16/evidence/scoping/ISS-01.md
[ISS-02]: https://github.com/banodoco/astrid-dev/blob/9e34444b3c9269d42293ab30558561495d678e3b/releases/16/evidence/scoping/ISS-02.md
[ISS-03]: https://github.com/banodoco/astrid-dev/blob/496ab219fff68b2ad85d762ec995da8d78a1d93a/releases/16/evidence/scoping/ISS-03.md
[ISS-04]: https://github.com/banodoco/astrid-dev/blob/e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00/releases/16/evidence/scoping/ISS-04.md
[HOR-01]: https://github.com/banodoco/astrid-dev/blob/736712b914dc2b46e6fd66dad2206d573ecf1510/releases/16/evidence/scoping/HOR-01.md
[INV-01]: https://github.com/banodoco/astrid-dev/blob/17617b57cc0b4d0485ea68211b84b675f9b6c053/releases/16/evidence/scoping/INV-01.md
[INV-02]: https://github.com/banodoco/astrid-dev/blob/f73732fbf825241f7be3f6204840e166a5f62c86/releases/16/evidence/scoping/INV-02.md
[INV-03]: https://github.com/banodoco/astrid-dev/blob/5d924e96aee1a2afdaeeb86131f698f5a57a5daf/releases/16/evidence/scoping/INV-03.md
[INV-04]: https://github.com/banodoco/astrid-dev/blob/9e8411372fc9a0257175d0f49da65ba7bee77bbb/releases/16/evidence/scoping/INV-04.md
[INV-05]: https://github.com/banodoco/astrid-dev/blob/22d9be23d3001ca7dabb4b2e90fc38b8b59657bf/releases/16/evidence/scoping/INV-05.md
[INV-06]: https://github.com/banodoco/astrid-dev/blob/f530e9b60391de8f60f8e38983038cf4615fa7e3/releases/16/evidence/scoping/INV-06.md
[INV-07]: https://github.com/banodoco/astrid-dev/blob/ca85e04c05968ad8cb5d4b562e17045283018ce9/releases/16/evidence/scoping/INV-07.md
[SC-35-severity-correction-01]: https://github.com/banodoco/astrid-dev/blob/ebe295571bb58028fe72d98c3da2cbe7fd40eaa5/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35-severity-correction-01.md
[INV-04-coverage-addendum-01]: https://github.com/banodoco/astrid-dev/blob/1e38786e3560d979b246a0ad0526920f4e3aa2ce/releases/16/evidence/scoping/INV-04-coverage-addendum-01.md
[AUD-01]: https://github.com/banodoco/astrid-dev/blob/43e3e390d6ffe026e6f2a61f0c866b0ac94daf9b/releases/16/evidence/scoping/AUD-01.md
[AUD-01-earlier]: https://github.com/banodoco/astrid-dev/blob/c9a3ec2b275a3e0d4bf9013255237d41ce2355f1/releases/16/evidence/scoping/AUD-01.md
[parallel-direction]: https://github.com/banodoco/astrid-dev/blob/6def0198c7a9a89f0e85b97582ef287274ef73a9/releases/16/evidence/scoping/README.md
[P04-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/04-concurrent-edits/inputs.md
[P04-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/04-concurrent-edits/plan.md
[P04-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/04-concurrent-edits/tasks.md
[P09-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/09-install-and-update-confidence/inputs.md
[P09-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/09-install-and-update-confidence/plan.md
[P09-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/09-install-and-update-confidence/tasks.md
[P10-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/10-pinokio-qualification/inputs.md
[P10-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/10-pinokio-qualification/plan.md
[P10-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/10-pinokio-qualification/tasks.md
[P29-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/29-update-and-release/inputs.md
[P29-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/29-update-and-release/plan.md
[P29-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/29-update-and-release/tasks.md
[P30-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/30-update-everywhere/inputs.md
[P30-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/30-update-everywhere/plan.md
[P30-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/30-update-everywhere/tasks.md
[P31-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/31-releases-from-astrid-dev/inputs.md
[P31-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/31-releases-from-astrid-dev/plan.md
[P31-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/31-releases-from-astrid-dev/tasks.md
[P32-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/32-generation-placement-targets/plan.md
[P32-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/32-generation-placement-targets/tasks.md
[P35-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/35-one-home-for-user-state/inputs.md
[P35-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/35-one-home-for-user-state/plan.md
[P35-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/35-one-home-for-user-state/tasks.md
[P36-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/36-one-credential-path/plan.md
[P36-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/36-one-credential-path/tasks.md
[P38-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/38-one-process-identity/inputs.md
[P38-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/38-one-process-identity/plan.md
[P38-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/38-one-process-identity/tasks.md
[P52-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/52-issue-intake/inputs.md
[P52-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/52-issue-intake/plan.md
[P52-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/52-issue-intake/tasks.md
[P53-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/53-vision-aspirations/inputs.md
[P53-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/53-vision-aspirations/plan.md
[P53-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/53-vision-aspirations/tasks.md
[P56-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/56-workflow-setup/inputs.md
[P56-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/56-workflow-setup/plan.md
[P56-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/56-workflow-setup/tasks.md
[P63-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/63-dependable-saving/inputs.md
[P63-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/63-dependable-saving/plan.md
[P63-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/63-dependable-saving/tasks.md
[P75-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/75-fast-saving/plan.md
[P75-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/75-fast-saving/tasks.md
[P76-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/76-editing-together/plan.md
[P76-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/76-editing-together/tasks.md
[P79-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/79-local-media-any-size/inputs.md
[P79-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/79-local-media-any-size/plan.md
[P79-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/79-local-media-any-size/tasks.md
[P85-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/85-one-place-to-measure/inputs.md
[P85-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/85-one-place-to-measure/plan.md
[P85-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/85-one-place-to-measure/tasks.md
[P87-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/87-render-works/inputs.md
[P87-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/87-render-works/plan.md
[P87-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/87-render-works/tasks.md
[P89-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/89-heavy-saves-in-seconds/plan.md
[P89-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/89-heavy-saves-in-seconds/tasks.md
[P90-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/90-workflow-setup-exact-plan/inputs.md
[P90-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/90-workflow-setup-exact-plan/plan.md
[P90-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/90-workflow-setup-exact-plan/tasks.md
[P93-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/93-comfyui-desktop-and-existing-environments/inputs.md
[P93-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/93-comfyui-desktop-and-existing-environments/plan.md
[P93-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/93-comfyui-desktop-and-existing-environments/tasks.md
[P94-inputs]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/94-dependable-environment-setup-and-recovery/inputs.md
[P94-plan]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/94-dependable-environment-setup-and-recovery/plan.md
[P94-tasks]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/plans/94-dependable-environment-setup-and-recovery/tasks.md
[R16-brief]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/releases/16.md
[R16-index]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/releases/16/evidence/scoping/README.md
[R16-run]: https://github.com/banodoco/astrid-dev/blob/4e355ca5095843612496a1dc84cf305b0c0fe5ce/releases/16/run.md
[assessed-diff]: https://github.com/banodoco/astrid-dev/compare/ed87d2ef0a437b5ec03818d502e1d7b8540aa65a...4e355ca5095843612496a1dc84cf305b0c0fe5ce
[dispatch]: https://github.com/banodoco/astrid-dev/blob/9b42590fbe69b68cac07f81abc5d9f2037bc7ba8/releases/16/evidence/scoping/dispatch-v2/REV-01-dispatch.md
[proposal-pr]: https://github.com/banodoco/astrid-dev/pull/1964
[issue641-ruling]: https://github.com/banodoco/astrid-dev/issues/641#issuecomment-7069355239
[main-drift]: https://github.com/banodoco/astrid-dev/compare/257a80bab15f753f1164994ca024efd01a4205e0...a9da325e274a70a249239d1f95913495797780ee
[app-public]: https://github.com/banodoco/astrid-app/tree/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public
[qualification]: https://github.com/banodoco/astrid-dev/blob/a9da325e274a70a249239d1f95913495797780ee/releases/15/evidence/qualification-cc1d48f0/README.md
[standard616]: https://github.com/banodoco/astrid-dev/blob/a9da325e274a70a249239d1f95913495797780ee/releases/15/evidence/qualification-cc1d48f0/renders/standard-616-verify.json
[film-declared]: https://github.com/banodoco/astrid-dev/blob/a9da325e274a70a249239d1f95913495797780ee/releases/15/evidence/qualification-cc1d48f0/renders/film-shaped-verify-declared.json
[film-comparison]: https://github.com/banodoco/astrid-dev/blob/a9da325e274a70a249239d1f95913495797780ee/releases/15/evidence/qualification-cc1d48f0/renders/film-editor-comparison-report.txt
[two-saves]: https://github.com/banodoco/astrid-dev/blob/a9da325e274a70a249239d1f95913495797780ee/releases/15/evidence/qualification-cc1d48f0/saves/two-save-evidence-clean-pair.jsonl
[r15-owner]: https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7170081785
[qualifier-latest]: https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7173917245
[p56-done]: https://github.com/banodoco/astrid-dev/issues/1757#issuecomment-7174111913
[app257]: https://github.com/banodoco/astrid-app/pull/257
[p91-stop]: https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7129888302
[p91-ack]: https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7130215692
[dev-ruleset]: https://api.github.com/repos/banodoco/astrid-dev/rulesets/27040267
[agent-source]: https://github.com/banodoco/astrid-agent/tree/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5
[runtime-source]: https://github.com/banodoco/astrid-runtime/tree/686ca695469bda48cd40a70824c4ccef2a137284
[app-source]: https://github.com/banodoco/astrid-app/tree/cc1d48f016fde55ad6b0609c619d8a4bcec56823
[vibe-source]: https://github.com/banodoco/VibeComfy/tree/55c3948212d23cf037fae8a4c6faad77d33e7279
[launcher-source]: https://github.com/banodoco/astrid-pinokio/tree/1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb
[lifecycle-source]: https://github.com/banodoco/runpod-lifecycle/tree/f2948817eeb94af8dee76be21f6d673724f1606e
[lifecycle-pin]: https://github.com/banodoco/runpod-lifecycle/tree/9f88ef7640bc664f697112d966ecefa123d44340
[p91-source]: https://github.com/banodoco/astrid-agent/tree/514499debc902643a03aee3f0ed68b710c5d3ead
