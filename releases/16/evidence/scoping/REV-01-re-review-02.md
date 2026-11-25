# REV-01 — independent targeted re-review 02

**Run:** `r16-scoping` · **Session:** `REV-01-01` · **Date:** 25 November 2026  
**Assessed proposal head:** `2662280f597413471c12e46040bae08803f04441`  
**Focused repair base:** `338b5014e839ae86364f4505c26d99d164602056`  
**Finding F05: RESOLVED. Exact-head verdict: SOUND for this focused repair.**

The actual committed clarification resolves the remaining LM-4 owner/interface/phase ambiguity. All three locations identified in the first re-review now agree: the P79 sequence, LM-4 task and dated reconciliation identify the App drop/capture → verified media selection/`clip.add-media` → P63 save-handoff contract; they keep LM-5's custody guard separate and place #1916 fixture verification with P88/P87/qualification only when that fixture is selected for heavy qualification. No residual F05 amendment is required. This is an independent judgment of the [actual focused diff][diff] and complete changed records, not acceptance of the coordinator's resolution claim alone.

This separate record preserves the [original REV-01 at `53a9e33175ad907aea3febf60bf5105cdc7f054e`][original] and [first re-review at `af0684f992190f94c44add1953724631bcd0e86d`][prior]. Their REWORK and SOUND WITH FOLLOW-UPS judgments remain valid for their respective older assessed heads. This targeted closure does not provide owner scope agreement, implementation/dispatch authority, product qualification, publication authority or the separately required SC-FINAL whole-release judgment.

## 1. Exact evidence chain

| Role | Exact identity and record |
| --- | --- |
| Original assessed proposal | `ed87d2ef0a437b5ec03818d502e1d7b8540aa65a` → `4e355ca5095843612496a1dc84cf305b0c0fe5ce` |
| Original review, preserved | `53a9e33175ad907aea3febf60bf5105cdc7f054e`, `releases/16/evidence/scoping/REV-01.md` |
| First re-review, preserved | `af0684f992190f94c44add1953724631bcd0e86d`, `releases/16/evidence/scoping/REV-01-re-review-01.md`; assessed `338b5014e839ae86364f4505c26d99d164602056` |
| Focused repair assessed here | `338b5014e839ae86364f4505c26d99d164602056` → **`2662280f597413471c12e46040bae08803f04441`** |
| Original SC-79 evidence | `ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1`, `plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md` |
| Report-only branch and existing draft PR | `evidence/r16-scoping-rev-01-01`, [#2011][pr], targeting `scope/release-16-scoping-record` |
| Parent of this report addition | `af0684f992190f94c44add1953724631bcd0e86d`; the evidence branch remains descended from dispatch base `9b42590fbe69b68cac07f81abc5d9f2037bc7ba8` |
| Sole authorized new repository path | `releases/16/evidence/scoping/REV-01-re-review-02.md` |

The GitHub comparison is **one commit ahead, zero behind**, with merge base equal to `338b5014…`. It changes four Markdown files: P79 `plan.md`, P79 `tasks.md`, the evidence index and the coordinator resolution record. The comparison reports ten added and four removed lines. Full new contents were retrieved at the exact head, matched to Git blob identities, and compared with the previously verified exact base contents. No moving proposal head or hypothetical synthesis was substituted. [Focused comparison][diff]

## 2. F05 — independent closure reasoning

### The original finding and its remaining part

Original F05 required useful independent starts, actual consumed-contract landing gates and final proof joins, with a conditional critical path and shared-function reservations instead of whole-plan or whole-file barriers. The first re-review already credited the LM-3/4/5 start/landing split, P32 F4 interface clarification and run-board amendments. It retained only the newly named **“verified P77 child builder”** as an unidentified LM-4 landing prerequisite. The specific LM-5 task already had its correct custody-only dependency; the first re-review expressly did not claim a demonstrated blanket LM-5-to-fixture wait. [Original F05][original] [First re-review F05][prior]

The required correction was therefore small: identify the actual LM-4 App producer/verified-selection/P63 handoff and responsible existing owners; retain LM-5's separate D4/CC-10/P29 guard; and keep the P88-owned #1916 fixture on its selected qualification path. No product rewrite, additional fixture programme or cosmetic rewriting of historical evidence was required.

### All three disputed locations now identify the correct dependencies

| Exact repaired location | What the actual text establishes | Independent disposition |
| --- | --- | --- |
| [P79 plan:46][plan46] | LM-4 consumes App drop/capture → verified media selection/`clip.add-media` → P63 save handoff, coordinated by the P79 App owner with P63. LM-5 separately consumes the D4/CC-10/P29 custody guard. Inventory starts independently; shared functions are reserved only where they actually conflict. | The grouped editor sentence no longer conflates the two landings or makes an unnamed builder their shared gate. |
| [P79 tasks:16][task16] | LM-4 traces the current App drop/capture producer and verified-selection/`clip.add-media` save handoff on the Lead-selected integrated candidate. It repairs an actual ordinary-video/audio refusal with P63 where necessary. Its landing depends on that reviewed contract and only the shared functions it consumes. Existing App scope paths and real-transfer/save/reopen proof remain. | The new dependency is identifiable by product flow, owning roles and affected code locations. The “verified P77 child builder” prerequisite is removed. |
| [P79 tasks:27][task27] | The dated reconciliation names the P79 App owner and P63 CC-6/13 for the LM-4 handoff, preserves LM-5's whole-lifetime CC-10/P29 guard, and places P88/P87/qualification-owned #1916 large-shots fixture verification in LM-6's proof description only when that fixture is selected for heavy qualification. | The controlling reconciliation no longer says to prove an unspecified child builder before LM-4. Product landing and selected-fixture qualification are distinct. |

This satisfies the prior read-only verification criterion: a dispatcher can now identify the actual consumer interface and accountable roles for LM-4, the separate LM-5 guard, and the conditional fixture-proof join. A concrete person/session, current branch and function reservation still need to be supplied by the existing Lead when authorizing work. The absence of those future dispatch facts is not an unresolved wording defect; neither previous F05 nor this review requires inventing them. [P79 plan:46–49][plan] [P79 tasks:15–27][tasks]

### The repair agrees with original SC-79 evidence

The full [SC-79 original][sc79] was reread. Its F5 and LM-4 mapping at lines 33 and 59 identify native verified media placement, the App handoff and P63 coordination; they require real ordinary-video/audio transfer, persistence and reopening, not a tiny payload with a fake size. Its F6 and LM-5 mapping at lines 37 and 60 concern the existing guard across preparation, upload, acknowledged import, pending placement and parked work. These are different product responsibilities, correctly separated by the repaired plan and task cells.

SC-79 F7 and the task mapping at lines 41 and 66 assign #1916's large-shots fixture to P88, with P87/qualification responsible for the selected proof. They explicitly distinguish that fixture from basic P79 transfer implementation. The new LM-6 sentence follows that distinction: it neither declares the fixture repaired/proved nor waives required heavy evidence. If that fixture is selected, its verification remains required; selection of another representative workload remains subject to the retained qualification contract. [SC-79:39–41][sc79-fixture] [SC-79 task mapping][sc79-map]

As a bounded source cross-check of the resolution's new App link, I also read `timelineLocalSaveHandoff.ts` lines 700–855 at immutable App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`. That window contains prepared-media selection validation, the path-specific non-image refusal and the `clip.add-media` command construction. It supports the existence and identity of the named handoff to investigate. It is a source observation at that App commit, not an installed reproduction, a claim that every App add path fails, or proof that the future integrated candidate already passes. The repaired LM-4 correctly requires rechecking the actual Lead-selected candidate. [App handoff source][app-source]

### Full-file consistency and parallelism

Reading the complete P79 records confirms that LM-3 inventory on existing objects and LM-4/5 producer/guard inventory remain independently startable. Tasks:21 still allows LM-4 and LM-5 to land in either order where their actual functions do not conflict, and LM-6 still proves the frozen integrated tuple. Plan:49 explicitly labels the old P77 branch conflict historical rather than a whole-plan start gate. The retained catalog waiting label at plan:15 points to that sequence; the new specific task and dated reconciliation provide the operative narrow interpretation. This focused patch does not restore the blanket barrier removed in the previous repair. [P79 plan][plan] [P79 tasks][tasks]

The owner direction to maximize practical parallel lanes is therefore preserved and made more precise. The real landing join is the consumed App/P63 contract; the real LM-5 join is its custody guard; a selected heavy fixture gates its qualification rather than unrelated implementation. Same-function conflicts still need one coordinated writer. No major refactor, new scheduler, new queue or new fixture platform is introduced solely for parallelism.

All LM-1–6/R progress remains unchecked. The original 300 MiB import absolute RSS gate, larger installed media witnesses, original-file preservation, interruption/lost-ACK and placement-only retry, reopen/render and one agreed review remain in the full task record. The correction changes who/what must join and at which phase; it does not claim execution or reduce those acceptance obligations. [P79 tasks:13–27][tasks]

**F05 result: RESOLVED.** There is no residual F05 owner/interface/phase contradiction requiring another canonical amendment at this exact head. The accountable implementation roles remain P79 App and P63 for LM-4, the existing custody-guard owners for LM-5, and P88/P87/qualification for the selected #1916 witness. Their actual implementation and proof are future work, not conditions for declaring this planning-text repair complete.

## 3. Effect on the prior review chain and limits

F01, F02, F03, F04 and F06 were resolved in the first re-review. This four-file focused diff does not alter their receiving task/acceptance repairs. With F05 now closed, **F01–F06 are resolved as scoping-text findings across this review chain**. This pass freshly adjudicates F05 only; it is not a new full release audit. The original verdict and first re-review are preserved rather than overwritten to appear as though they had assessed `2662280f…`.

The full revised [evidence index:152][index] accurately links the original and first re-review to their respective assessed heads. The [coordinator resolution:19–23][resolution] accurately describes the focused clarification, while leaving its independent check pending. Those receipts are provenance, not a substitute for the actual P79 changes examined here.

F07's broader HOR/source-coverage limitation, pending owner choices, existing delivery authority, P91 STOP, exact support/native/paid evidence, effective publication controls and final qualification obligations remain as recorded in the prior review and canonical records. No moving product baseline, served manifest, current protection setting or live qualification was refreshed by this focused pass. The bounded App source observation above is not a refresh of the installed product. SC-FINAL still needs its independent judgment of the revised whole, and the owner retains scope/go authority. [Prior re-review limits][prior] [Evidence index][index]

**Handoff:** the coordinator can index this exact-head F05 closure and pass the revised proposal plus both preserved prior reviews and this record to SC-FINAL. There is no further F05 repair request. READY-REPORT-CORRECTION reports delivery of the independent review; it does not mark an implementation task, fixture witness or release gate complete.

## 4. Coverage and preservation

Root read all four changed files completely through EOF and every focused old/new diff hunk. Total changed-file content: **71,706 UTF-8 bytes, 280 physical lines**. A separate internal qualification reader independently read both full P79 records, every focused hunk and the full resolution, checked the original F05/prior residual against SC-79, and reached RESOLVED without editing the proposal. The final decision is this session's independent review.

| Complete changed file at `2662280f…` | EOF | Verified Git blob |
| --- | ---: | --- |
| [plans/79-local-media-any-size/plan.md][plan] | 74 | `fdee8d2971733de0ee2314f8683aec5885f3eb04` |
| [plans/79-local-media-any-size/tasks.md][tasks] | 27 | `72b0871a0e11132718b498315854376e173d01d2` |
| [releases/16/evidence/scoping/README.md][index] | 156 | `9d6b3aa13c927eb808ddb815d10114ece562e14e` |
| [releases/16/evidence/scoping/REV-01-resolution-01.md][resolution] | 23 | `81a6e4eb8ae843132ffeffc8367071dab99f249f` |

Additional fresh semantic reads: complete SC-79 through its 82-line EOF; original REV-01 F05; first re-review F05 and its relevant limits; bounded App source lines 700–855 at the exact commit above. The earlier full original-report and wider changed-file coverage remains in the preserved prior ledgers. All sources required for this focused judgment were accessible. Source retrieval, blob/content comparison and document inspection are not tests or product execution.

Before this addition, both original reports were fetched at evidence-branch head `af0684f…` and verified against their established blobs: original `REV-01.md` = `dc2cf7ad2d7afa7872200536da98a733878607e3`; first re-review = `d0bc01aef1a11142bea78818cc9ad2ecb2be6cd6`. This second record alone is added on that existing branch. No proposal head is merged, rebased or imported into the evidence branch. After push, the authorized mailbox correction supplies this new record's exact commit/path and assessed head, plus readback verification of the one-file addition and preservation of both prior reports.

**Actions:** source/document reads, this separate independent report, its evidence-branch push and authorized mailbox receipt only. No proposal/product edits, tests, builds, CI invocation, paid work, merge, issue-state mutation, protection changes or publication.

[diff]: https://github.com/banodoco/astrid-dev/compare/338b5014e839ae86364f4505c26d99d164602056...2662280f597413471c12e46040bae08803f04441
[original]: https://github.com/banodoco/astrid-dev/blob/53a9e33175ad907aea3febf60bf5105cdc7f054e/releases/16/evidence/scoping/REV-01.md
[prior]: https://github.com/banodoco/astrid-dev/blob/af0684f992190f94c44add1953724631bcd0e86d/releases/16/evidence/scoping/REV-01-re-review-01.md
[pr]: https://github.com/banodoco/astrid-dev/pull/2011
[plan]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/plans/79-local-media-any-size/plan.md
[plan46]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/plans/79-local-media-any-size/plan.md#L46
[tasks]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/plans/79-local-media-any-size/tasks.md
[task16]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/plans/79-local-media-any-size/tasks.md#L16
[task27]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/plans/79-local-media-any-size/tasks.md#L27
[index]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/releases/16/evidence/scoping/README.md
[resolution]: https://github.com/banodoco/astrid-dev/blob/2662280f597413471c12e46040bae08803f04441/releases/16/evidence/scoping/REV-01-resolution-01.md
[sc79]: https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md
[sc79-fixture]: https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md#L39-L41
[sc79-map]: https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md#L51-L66
[app-source]: https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts#L700-L855
