# REV-01 — independent integration re-review 03

**Run:** `r16-scoping` · **Session:** `REV-01-01` · **Date:** 26 November 2026 (Europe/Berlin; source observations below use UTC)  
**Exact integration base:** `a097f1c5c9de593ea524d20b88f75cfa217f389a`  
**Exact integration head:** `6f20e4ee4f60dd477ae461d16bd24c03976656c3`  
**Verdict: SOUND — for this planning integration only.**

The [actual integration][integration] preserves the previously reviewed substantive scope, its repaired findings, newer main progress and delivery authority. The P31 overlap is reconciled to main's current tester documents without losing its safety or qualification requirements. Plan 73's completed cutover remains in place; P91's STOP is explicit and controlling. I found **no new BLOCKING defect, no required integration amendment, and no missing source that makes this assessment BLOCKED**.

This is a judgment of the integration into the specified main base. It does not turn the earlier proposal into a different assessed head or close its execution obligations. [SC-FINAL][scfinal] remains **SOUND WITH FOLLOW-UPS on substantive proposal `2662280f597413471c12e46040bae08803f04441`**. Its feasibility, allocation and predecessor-reconciliation follow-ups remain applicable as described below. The owner's instruction authorizes this planning integration; it does not itself choose a pending technical option, resume a held delivery lane, establish product proof or authorize publication. The integrated [handoff][index] states that distinction explicitly.

## 1. Identities and preserved review chain

| Role | Exact identity and meaning |
| --- | --- |
| Integration under review | [PR #2021][integration-pr], `a097f1c5c9de593ea524d20b88f75cfa217f389a` → **`6f20e4ee4f60dd477ae461d16bd24c03976656c3`** |
| Integration ancestry | One commit; its sole parent is `a097f1c5c9de593ea524d20b88f75cfa217f389a`. This is the actual specified main base, not the older proposal base. |
| Previously reviewed substantive proposal | `2662280f597413471c12e46040bae08803f04441`; continuity reference, not the present verdict target |
| Original review, preserved | [REV-01][original] at `53a9e33175ad907aea3febf60bf5105cdc7f054e`, assessed `ed87d2ef0a437b5ec03818d502e1d7b8540aa65a` → `4e355ca5095843612496a1dc84cf305b0c0fe5ce`, **REWORK** |
| First re-review, preserved | [REV-01-re-review-01][r1] at `af0684f992190f94c44add1953724631bcd0e86d`, assessed `338b5014e839ae86364f4505c26d99d164602056`, **SOUND WITH FOLLOW-UPS** |
| Second re-review, preserved | [REV-01-re-review-02][r2] at `812d03eb15c824f2f411d9fc63736ed6feb0e3dd`, assessed the focused F05 repair at `2662280f597413471c12e46040bae08803f04441`, **SOUND for that repair** |
| Subsequent whole-release review | [SC-FINAL][scfinal] at `ace5b96edb5c70d3e2e8023be9ab1acb83bdfc14`, **SOUND WITH FOLLOW-UPS on 2662280…**, not on this integration |
| Parent of this separate evidence addition | `812d03eb15c824f2f411d9fc63736ed6feb0e3dd`; the evidence branch still descends from original dispatch base `9b42590fbe69b68cac07f81abc5d9f2037bc7ba8` |
| Authorized destination | Existing `evidence/r16-scoping-rev-01-01`, existing draft [PR #2011][evidence-pr] into `scope/release-16-scoping-record` |
| Only new repository path | `releases/16/evidence/scoping/REV-01-re-review-03.md` |

The original findings and earlier verdicts remain valid for their own assessed identities. This new record neither edits those reports nor retroactively changes their scope. The coordinator's [resolution][resolution] and integration explanation were checked as claims against source, not accepted as independent evidence of correctness.

## 2. Actual comparison and material-change inventory

Complete recursive Git trees were retrieved at all three identities: 4,512 entries at the integration base, 4,545 at the integration head and 4,482 at the prior substantive proposal; none was truncated. Comparing path, mode, type and object identity establishes **100 changed files: 67 modified, 33 added, zero removed**, all Markdown. No mode-only change or non-document change is hidden in that count. The specified base is also the comparison's merge base. [Base tree][base-tree] · [Integration tree][head-tree] · [Prior tree][prior-tree] · [Actual diff][integration]

Of those 100 integration paths, **95 head blobs are byte-identical to the corresponding files at 2662280…**. The remaining five are the complete three-way reconciliation surface:

| File | Difference from the previously reviewed substantive proposal | Integration finding |
| --- | --- | --- |
| [P31 plan][p31-plan] | Line 25 uses main's platform-neutral tester filenames and wording. | Preserves the full tentative-build outcome and consent/reporting safeguards. |
| [P31 tasks][p31-tasks] | Line 85 uses the same current filenames and current relative preparation/frontend references. | Preserves the full RL-1e contract and main's actual document targets. |
| [Scoping evidence index][index] | Adds the second re-review receipt, SC-FINAL receipt and handoff, and an explicit main-integration explanation. | Preserves exact reviewed/report identities, pending choices, limits and independent-review boundaries. |
| [SC-FINAL dispatch][final-dispatch] | Additional historical report-only assignment, absent at 2662280… and at integration base. | Explicitly assesses 2662280…; does not purport to review 6f20e4ee… or authorize a new product run. |
| [R16 run board][run] | Historical P91 launch line 88 keeps main's `agent/roles/orchestrator/multi-manager-dispatch.md` path. | Preserves Plan 73's path migration; does not change the STOP, target or authority. |

These five complete head files contain 135,207 UTF-8 bytes and 663 lines. Their head Git blobs, in table order, are `79fc5da3d2dda186a5f6f46ef4ff23f3e15a3639`, `9c54cd257e7c521c5ebd601a49969740f9e2e9c4`, `03a83b0f721680d78ef5f2e89413f3e788af891a`, `c76f4d9d5b1d1a13327c0b28f2b099c1fd477177` and `9dc9196c926af8ac6148f5cc20ecf579590abab3`.

Equality with the prior proposal alone would not prove preservation of newer main facts. Every actual base-to-integration hunk was therefore read, including the removed/replaced side, and newer-main status changes were checked in the full receiving records. Conversely, a diverged three-dot comparison from 2662280… would mix inherited main history into the scope delta and can hit GitHub's file-list cap. The verdict uses complete trees and exact file bytes, not that capped comparison.

### INT-01 — NOTE — P31's conflict resolution preserves both current main and the reviewed gate

The changed paragraphs are exactly the current-main versions in [base plan line 25][base-p31-plan] and [base tasks line 85][base-p31-tasks]. The integrated tree contains `tester-brief.md`, `test-matrix.md`, `prepare-build.md` and `frontend-testing.md` at the referenced Release 15 tester-run paths. The obsolete Windows-specific names are not restored. The current document targets, and the entire Release 15 subtree, are unchanged from the integration base. [Tester documents][tester-docs]

RL-1e still requires read-only discovery of the active or explicitly selected testing release, coherent immutable sources derived from owning pins, exact artifact receipts/hashes, replay versus fresh resolution, two same-number snapshot updates, and real Windows/Linux installed and local-App journeys. Consent, first creation, connection, edit/save/reopen, setup/chat, cleanup and rollback remain. Served-App observations remain distinct from native full-stack evidence. Nothing makes a tentative build a production publication. [P31 plan, line 25 and completion][p31-plan] · [P31 tasks, RL-1e][p31-tasks]

The previously repaired protection and sequencing also survive: current Lead-approved branches and the specific P29 status/manifest landing join; RL-3 before RL-R and the first Final; early nonpublishing rehearsal; a protected generated-only writer satisfying every effective required check; exact owner approval; old writer/guard retention until replacement enforcement works; safe deployment interval and complete served readback. RL-2c explicitly supersedes historical direct-push/self-check wording. The older broad plan text is retained history under the existing proposed task precedence, not a newly introduced bypass. Build, review and go remain unchecked. [P31 tasks, lines 7–9, 17, 28–36, 118–120 and 132–153][p31-tasks]

**Action/verification:** no further P31 integration amendment is required. At affected implementation, the existing P31 custodian and owner still owe effective-control and exact-writer evidence; this static review did not inspect effective settings or execute the gate.

### INT-02 — NOTE — Plan 73, P91 STOP and held authority are preserved

The following complete subtrees have identical base/head tree objects:

| Preserved surface | Common Git tree |
| --- | --- |
| `agent/` | `ae202e2bf5fbf46648712c80168eec321441e514` |
| `plans/73-markdown-first-agent-skills/` | `dd6468789c07fe26a65c1956963106f54fbd3392` |
| `plans/91-agent-main-green/` | `a045241eb5ddad2627eaf52aa22bfdcb51a87960` |
| `plans/82-reuse-across-commands/` | `c404ecfc917cea17a3fafd9806c3cfee8bd9d759` |
| `plans/95-composable-agentic-workspaces/` | `6efecf81cf2a15120194c457c2cf61bb1d43ed8a` |
| `releases/15/` | `a78587f3f5d6da9b61db145bf4c9c053fae8af47` |
| `.github/` | `5663d815589b4214519102849ff73a858247a1c9` |

The authored `skills/` tree is absent at both base and head; it is not recreated. P73's [plan][p73-plan] still says **done**, and its [completion-run table][p73-tasks] remains the controlling completed list, with original task records explicitly historical. The integration leaves main's canonical roles/workstreams in place. Immutable links into earlier instruction revisions and historical task text are provenance, not a rollback of the installed or authored instruction tree. This is source preservation, not a new installed-skill attestation.

P91's original lane, branch, accepted decisions, AG-0 completion and remaining unchecked tasks are preserved. The [run board, lines 7–9][run] forbids landing the broad programme into `release/16/main`, requires a coordinated R17 target/base/proof handoff and explicitly makes the later STOP controlling over older bounded-authority and launch text. Its historical `agent/` path correction conveys no fresh dispatch permission. [P91 tasks][p91-tasks]

The environment reader freshly read all six P91 mailbox comments at **23:24:59 UTC, 25 November**; [STOP 7129888302][stop] and [acknowledgement 7130215692][stop-ack] were still the last two, with no resume. I independently read both exact bodies. The acknowledgement reports no started packet, branch, PR or hosted CI and stopped monitoring. P82's [handoff][p82-handoff] remains unchanged; its [23:06:37 UTC manager status][p82-status] still holds Stage 2, the three open draft PRs and packets 04/05/07. The later comparison testimony retains its [log-tail limitation][p82-comparison]; I did not turn it into exhaustive proof.

**Action/verification:** no authority-repair amendment is required. Only the existing later owner/orchestrator decision can resume P91, and only an actual authorized handoff can bind new execution targets. This integration and this report do neither.

### INT-03 — NOTE — Newer main progress and unfinished work survive

| Record | Concrete preservation checked at the integrated head | Remaining meaning |
| --- | --- | --- |
| [P52][p52-tasks] | Existing custodian and waiting-on reconciliation; II-8/9 reopened, II-10/11/13 unchecked; warning against the obsolete Agent branch; all seven D14 states including Claimed. | Old six-search evidence remains partial. Owner transfers, browser proof and actual custodian confirmation are not completed by integration. |
| [P53][p53-tasks] | Still-unticked VA/R cards, source-present App #257 history, independent/owner acceptance and existing Lead custody; VA-11 remains post-live. | Source presence does not become acceptance or a reason to rebuild already merged work. |
| [P56][p56-tasks] | WS-0g and LE-2b checked; RS1's failure/fix/RS1B/RS1C/final delta history; all remaining Release 16 cells and owner-run WS-L after R. | Stage 1 is not reset; Stage 2 and whole-plan completion are not claimed. The exact P90 receiver/alias map and useful-delta warning remain. |
| [P38][p38-tasks] | W0 remains checked and subsequent tasks remain unchecked. Proposed D-SYN-4 and native/security proof limitations remain. | Internal Pub is not a public release; native role/custody acceptance remains necessary. |
| [P87][p87-tasks] | Later P87-09 Agent #661/`dc45d97c` installed-pack receipt, including the distinction from projected-pack proof; RN-0/R waiting-on and RN-10/11/14/15 limitations. | One installed-pack fix does not establish all render, wheel, recovery or heavy acceptance. |
| [P89][p89-tasks] | Open-residual waiting-on, SV-L11 no-gain history, unfunded SV-L12, historical measurements and unmet gate. | The comparable 300-clip 2 s median / 4 s maximum is retained; moving broader performance work later is not a waiver. |

P35/P36/P90/P93/P94 remain queued or draft/unassigned as recorded, and their proposed receiving rows remain unfinished. Current grants, revocation, credential references, reachability, target revalidation, local/paid separation and native acceptance retain their original meanings. No integration hunk converts an unchecked task, UNKNOWN result, source observation, deferred item, rejected approach or post-live obligation into completion. P09/P10/P29/P30 retain their existing progress, literal task suffixes, moved publisher history, native-engine gap and actual route proof. [P35 tasks][p35-tasks] · [P90 tasks][p90-tasks] · [P94 tasks][p94-tasks] · [Actual diff][integration]

**Action/verification:** no status-preservation correction is required. Existing custodians must still reconcile live donor containment, retained product residuals and owner evidence at authorized dispatch; a proposal row is not a new lane assignment.

### INT-04 — NOTE — F01–F06 remain closed as document findings; no material repaired claim is omitted

| Original finding | Preserved repair at 6f20e4ee… |
| --- | --- |
| F01 | P94 ER-P1 retains an actual receiving task, existing paid-lifecycle custodian to be designated, current reachability/credential/custody analysis, no-spend negatives, independent cost bound, retained-route final join and separate paid permission. Ordinary local ER-L/R is independent of paid proof. |
| F02 | The brief still normatively incorporates the immutable SYN support/negative/preservation matrix and maps every family to canonical tasks and proof joins. P38 retains #682's native allowed/denied asynchronous-guard witness as an unverified question, and P94 retains two accepted cold/recovery rounds before go. |
| F03 | Minimal ET-5→CC-4b, needed burst work→CC-5c and measured save/undo/reopen→CC-17 remain, with conditional watermark and ET-1/ET-4b coupled under pending D17 timing. |
| F04 | P52's all-seven-state obligation and explicit older six-search limitation remain. |
| F05 | P79 LM-4 retains App drop/capture → verified selection/`clip.add-media` → P63 CC-6/13. LM-5 independently joins D4/CC-10/P29. P88/P87/qualification verifies #1916 only when that fixture is selected for heavy qualification. No generic P77-builder landing dependency returns. |
| F06 | P90 current grant plus independently revalidated target/dependencies, P38 observation versus permitted owned-child signal, and P31 protected exact generated writer examples remain. |

These are continuations of the [first re-review][r1] and [focused second re-review][r2], checked against exact head blobs and actual current-main differences. Current canonical evidence is [P94 ER-P1][p94-tasks], [the brief's acceptance matrix][brief], [P38 E1/P1][p38-tasks], [P63 receiving tasks][p63-tasks], [P76's bounded transfer][p76-tasks], [P52's seven-state proof][p52-tasks], [P79 LM-4/5/6][p79-tasks], [P90 UP-1][p90-tasks] and [P31 RL-2c][p31-tasks]. The receiving files are unchanged from the repaired substantive proposal except the safe P31 references described above. The [coordinator resolution][resolution] itself is byte-identical to 2662280…. F07's HOR coverage and authority limits remain explicitly preserved in the [index][index]. This finding closes no product bug or proof obligation by inference.

## 3. Owner direction: practical parallel lanes remain the chosen strategy

The [brief, lines 20–30][brief] and [existing run board, lines 13–27][run] still support simultaneous source/origin inventories, native Pinokio feasibility, old-systemd/local adapters, records/protection work, provider/closure work, target discovery, managed-route work, exact-plan donor analysis, state/grant census, save model/corpus/capture, streaming media, pack/output repair and no-spend paid-safety analysis. There is no newly imposed whole-P35/P38 foundation gate or major refactor solely for parallelism.

The operative reservations remain narrow: one semantics owner for a shared function, schema, case table or pin hunk, with useful disjoint work in the same file permitted. A provider or schema blocks its affected consumer landing; current authorization blocks privileged apply; verified migration blocks retirement; an individual inverse blocks batching that relies on it; actual native engine authority blocks a valid lifecycle witness. These constraints protect real contracts rather than merely ordering plan numbers.

The two early vertical checkpoints remain independent: existing-environment selection/decline/approved first result, and substantial import/edit/lost-ACK/undo/reopen/short-render/recovery. They are internal integration evidence, not separate shipments. One pin integrator, relevant proof invalidation, exact final-tuple qualification, final independent review and one protected owner Final remain. Quiet GPU/native/heavy proof capacity is a reservation issue, not a reason to stop unrelated coding.

A whole-foundation-first sequence would delay scope-changing observations without removing the eventual native, migration or save joins. Starting every plan as an independent implementation would duplicate shared writers and defer conflicts. The retained dependency-led sequence is the better practical choice here. Its remaining operational requirement is to fill actual holders and venues when authorized, not invent capacity, create another tracker or expand architecture. This agrees with [SC-FINAL's alternatives and SCF-01/02][scfinal] for reasons verified in the integrated records.

## 4. Carried follow-ups and decisions — open, not integration defects

No item below requires changing the assessed integration before its planning-only landing. These are existing obligations already retained in [index lines 167–171][index], the brief and canonical tasks. **SOUND for integration does not close them.**

| Carried obligation | Concrete next action and accountable owner | Evidence needed at its actual gate |
| --- | --- | --- |
| SCF-01: early feasibility | Existing Lead prioritizes native P10 Stop/Quit, P63 individual inverse/batching and comparable save, P94 managed Windows/compute and no-spend independent paid bound, and P31 effective controls/comparator work within the existing lanes. | Exact interim source/fixture/venue, observed result, limit and triggered action. A miss leads to bounded repair or an explicit owner scope decision. Other ready work need not wait globally. |
| SCF-02: real allocation | Lead records actual branch/function/schema holders, next landing contracts, one pin integrator and native/GPU/quiet-heavy venues in the existing run board. Keep P04 acceptance with P63 implementation unless a specific isolated repair warrants a branch. | A conflict-free authorized package and a real venue or explicit wait. No dates, free sessions, eight simultaneous GPUs or paid-machine permission inferred from historical estimates. |
| SCF-03: source/handoff reconciliation | Coordinator/Lead with P56/P90, P31, P52/P53 and qualification custodians refreshes current served/source/installed identities and useful donor deltas before affected execution branches and final freeze. | Actual containment and receiver receipt; truthful R14 historical origins and current comparator; consumed pins rather than floating names; owner/post-live closure distinguished. P31's filename part is now resolved, not the whole follow-up. |
| Scope decisions | Owner and existing Lead record the effective strict-check policy, any individually justified nonrequired inherited-red exception, P89 gate/miss response, ET-1/ET-4b timing, Windows route, Linux arm64 support/refusal, P38 role scope, grant revoke/restore, paid custodian/bound/capability and P52/P53 custody/closure. | Explicit decisions in existing homes. Current required checks and safety rules remain binding until a valid decision; integration is not acceptance by implication. |
| Qualification and publication | Existing qualifier and plan custodians establish accepted route/negative/heavy/native/installed receipts and effective protections on the actual final tuple; owner gives the exact publication go. | PASS/FAIL/UNKNOWN/NOT RUN/justified NOT APPLICABLE remain distinct. Changed relevant inputs invalidate affected proof. Retained paid capability needs separately authorized proof or explicit restriction. |

SCF-03's current-main documentation part is substantially addressed: the tester names are reconciled and the completed Plan 73 tree plus current release machinery remain. The [Release 15 publication lessons][lessons] are unchanged at base/head, as is the canonical [release workstream][release-workstream]. Its relevant clauses still require distinct failure IDs (line 34), stock manifest-pinned installed packs (line 36), consumed pins and a settled required floor before update journeys (line 156). Their preservation does not mean those witnesses have been performed for R16.

The original qualifier/issue's unresolved #2002 causes and the later Lead's test-only classification must retain their separate attribution, as [SC-FINAL §7][scfinal] does. R15 acceptance is not a blanket R16 exception. The integrated index also retains HOR's broader source-coverage blocker and separately attributed follow-up. Neither a complete scoping-report read nor a successful documentation integration establishes an exhaustive issue census or fresh installed/native/paid qualification.

## 5. Reading, verification and limits

This is an independent continuation of REV-01, not a new commissioned whole-release reviewer. I retained the integration verdict and report authorship. Three internal read-only readers assisted with the release/qualification, environment/authority and editing/media/status comparisons; their results and precise ledgers were read and checked against the central records and exact trees. They did not write remotely or change the assessed proposal.

All **100 actual base-to-head patches** were freshly read within this division, including removed sides, context and exact changed link destinations. The complete 100 head files were obtained and verified against their Git blobs: **1,466,449 UTF-8 bytes and 8,537 lines**. Complete full-file semantic coverage consists of fresh reads and explicitly identified prior full reads carried only by byte identity:

| Review slice | Files | Fresh full-head reading versus verified previous full reading |
| --- | ---: | --- |
| P09/P10/P29/P30/P31 | 15 | Full P31 plan/tasks at all three identities; 13 other full-head reads carried from the earlier review after exact blob verification; all current integration hunks freshly read. |
| P35/P36/P38/P90/P93/P94 | 17 | All 17 full heads freshly read; every integration hunk read; base/head/prior blobs checked. |
| P04/P32/P52/P53/P56/P63/P75/P76/P79/P85/P87/P89 | 32 | Fourteen full heads freshly read: P52/P53/P56/P85's complete triples and P79 plan/tasks. Eighteen earlier full reads carried by exact identity; all 958 lines of the integration diff read. |
| Central brief, run, index, CTX-01, resolution | 5 | All full heads and integration hunks freshly read by the verdict author. |
| Imported dispatch wrappers | 31 | All 31 full files and all addition hunks freshly read; 30 equal prior proposal, SC-FINAL is additional. |

Thus 69 complete head files were freshly reread and 31 reused verified prior full semantic coverage; this is not a claim that I personally reread every line of all 100 files during this pass. Every one of the five exceptions from substantive 2662280… was freshly read in full, together with its exact direct differences. The original evidence, SYN and earlier review coverage remain traceable in [REV-01 §8][original] and the [two][r1] [re-reviews][r2]; they were not all rerun for a preservation review.

The new SC-FINAL original was fetched at its exact report commit, verified as blob `0647f6c0f8d8bff06c44943958ded93236e0133a`, 100,543 bytes and 561 lines, and read through EOF by both the release reader and me. P73/P91/P82 plan/inputs/tasks and P82's handoff were freshly read in full. The live authority observations are bounded as stated above; P82's relevant decisions/latest comments were read, not every historical packet message. Supplemental publication-lesson and workstream reads establish retained policy text, not executed proof.

No required integration source was inaccessible. No new exhaustive product-source audit, installed-skill verification, hardware/native engine observation, effective-settings inspection or served-product refresh is claimed in this third review. SC-FINAL's served R15 observation remains its timestamped observation. Source presence, recorded receipts and static equality do not establish current machine state. These limits do not hide an integration defect; they bound the claims this review can make.

No tests, builds, repository validators, CI dispatches/reruns, product execution, paid actions, proposal/product edits, merge or publication were performed. Source retrieval, file comparison, Git-object verification and this report-only submission are the work of this pass.

## 6. Submission boundary

Add only this separate linked report to existing evidence branch head `812d03eb15c824f2f411d9fc63736ed6feb0e3dd`. Preserve the original and both prior re-reviews byte-for-byte; do not import the assessed integration into the report branch or retarget the evidence PR. The READY-REPORT-CORRECTION receipt must identify the resulting full report commit, this path, exact assessed head `6f20e4ee4f60dd477ae461d16bd24c03976656c3`, integration base and prior substantive/report references. Verify the remote report, sole added path, parent, branch head, existing draft PR and posted receipt.

The final disposition is **SOUND for integrating this exact planning diff onto its specified main base, with no new actionable integration defect**. The separate whole-release follow-ups, pending owner choices and proof requirements remain open exactly as described.

## Sources

[integration]: https://github.com/banodoco/astrid-dev/compare/a097f1c5c9de593ea524d20b88f75cfa217f389a...6f20e4ee4f60dd477ae461d16bd24c03976656c3
[integration-pr]: https://github.com/banodoco/astrid-dev/pull/2021
[base-tree]: https://api.github.com/repos/banodoco/astrid-dev/git/trees/a097f1c5c9de593ea524d20b88f75cfa217f389a?recursive=1
[head-tree]: https://api.github.com/repos/banodoco/astrid-dev/git/trees/6f20e4ee4f60dd477ae461d16bd24c03976656c3?recursive=1
[prior-tree]: https://api.github.com/repos/banodoco/astrid-dev/git/trees/2662280f597413471c12e46040bae08803f04441?recursive=1
[original]: https://github.com/banodoco/astrid-dev/blob/53a9e33175ad907aea3febf60bf5105cdc7f054e/releases/16/evidence/scoping/REV-01.md
[r1]: https://github.com/banodoco/astrid-dev/blob/af0684f992190f94c44add1953724631bcd0e86d/releases/16/evidence/scoping/REV-01-re-review-01.md
[r2]: https://github.com/banodoco/astrid-dev/blob/812d03eb15c824f2f411d9fc63736ed6feb0e3dd/releases/16/evidence/scoping/REV-01-re-review-02.md
[scfinal]: https://github.com/banodoco/astrid-dev/blob/ace5b96edb5c70d3e2e8023be9ab1acb83bdfc14/releases/16/evidence/scoping/SC-FINAL.md
[evidence-pr]: https://github.com/banodoco/astrid-dev/pull/2011
[brief]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/releases/16.md
[run]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/releases/16/run.md
[index]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/releases/16/evidence/scoping/README.md
[resolution]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/releases/16/evidence/scoping/REV-01-resolution-01.md
[final-dispatch]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/releases/16/evidence/scoping/dispatch-v2/SC-FINAL-dispatch.md
[p31-plan]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/31-releases-from-astrid-dev/plan.md
[p31-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/31-releases-from-astrid-dev/tasks.md
[base-p31-plan]: https://github.com/banodoco/astrid-dev/blob/a097f1c5c9de593ea524d20b88f75cfa217f389a/plans/31-releases-from-astrid-dev/plan.md
[base-p31-tasks]: https://github.com/banodoco/astrid-dev/blob/a097f1c5c9de593ea524d20b88f75cfa217f389a/plans/31-releases-from-astrid-dev/tasks.md
[tester-docs]: https://github.com/banodoco/astrid-dev/tree/6f20e4ee4f60dd477ae461d16bd24c03976656c3/releases/15/tester-run
[p73-plan]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/73-markdown-first-agent-skills/plan.md
[p73-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/73-markdown-first-agent-skills/tasks.md
[p91-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/91-agent-main-green/tasks.md
[p82-handoff]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/82-reuse-across-commands/release-16-handoff.md
[stop]: https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7129888302
[stop-ack]: https://github.com/banodoco/astrid-dev/issues/1826#issuecomment-7130215692
[p82-status]: https://github.com/banodoco/astrid-dev/issues/1824#issuecomment-7177157418
[p82-comparison]: https://github.com/banodoco/astrid-dev/issues/1824#issuecomment-7176912460
[p52-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/52-issue-intake/tasks.md
[p53-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/53-vision-aspirations/tasks.md
[p56-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/56-workflow-setup/tasks.md
[p38-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/38-one-process-identity/tasks.md
[p87-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/87-render-works/tasks.md
[p89-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/89-heavy-saves-in-seconds/tasks.md
[p35-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/35-one-home-for-user-state/tasks.md
[p90-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/90-workflow-setup-exact-plan/tasks.md
[p94-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/94-dependable-environment-setup-and-recovery/tasks.md
[p63-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/63-dependable-saving/tasks.md
[p76-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/76-editing-together/tasks.md
[p79-tasks]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/plans/79-local-media-any-size/tasks.md
[lessons]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/docs/ledger/2026-11-25-release-15-publish-lessons.md
[release-workstream]: https://github.com/banodoco/astrid-dev/blob/6f20e4ee4f60dd477ae461d16bd24c03976656c3/agent/shared/workstreams/release.md
