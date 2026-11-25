# SYN-01 — Release 16: parallel delivery with explicit landing and proof gates

**Run:** `r16-scoping` · **Author/session:** `SYN-01` / `SYN-01-01` · **Date:** 25 November 2026 (timestamps below are UTC).  
**Verdict:** **REWORK the proposal before scope acceptance.** Retain the fifteen selected product outcomes and the P56 residual handoff. Replace the provisional foundation-first sequence with independent work packages, a few reviewed interfaces, two early vertical checkpoints, and one integrated shipment. A major refactor is not a prerequisite for concurrency.  
**Exact reviewed proposal and mandatory report parent:** `f8721766ba2fcb7762ca42767749409d00aa2dbc`.  
**Report-only destination:** `releases/16/evidence/scoping/SYN-01.md`, branch `evidence/r16-scoping-syn-01-01`, draft evidence PR to `scope/release-16-scoping-record` / [proposal #1964](https://github.com/banodoco/astrid-dev/pull/1964). The eventual evidence commit is a submission identity, not a reviewed proposal or product identity.

This report proposes actual replacement brief text and path/task amendments. It does not apply them, change progress, authorize implementation, qualify a product, or accept the release. All 28 Wave A/B originals, both corrections, and the **completed** AUD-01 were read through their ends; their immutable identities are in §10. Read-only source checks and supporting cross-checks are distinguished from reported tests and source-supported inferences. No tests, builds, CI dispatch, installation, clone, spending, product/proposal edits, merge, publication, or issue mutation outside the authorized #1963 mailbox were performed by this synthesis. Internal read-only cross-checks supplemented, rather than replaced, the author's reading of every original.

The governing [dispatch](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/dispatch-v2/SYN-01-dispatch.md), [packet](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/dispatch-v2/packets/SYN-01.md), procedure/context, CTX-00/01, evidence index, and the four workstreams at `7060b764ec16a638b0e6774f814eabf6d7b70c04` were read. This verifies source instructions, not a locally installed skill revision or a Chat UI model setting. Initial STATUS [7172355698](https://github.com/banodoco/astrid-dev/issues/1963#issuecomment-7172355698) was acknowledged by the coordinator in [7172729103](https://github.com/banodoco/astrid-dev/issues/1963#issuecomment-7172729103).

## 1. Decision and numbered findings

“BLOCKING” below means an unresolved canonical scope/acceptance or eventual release gate. It does not mean the report is undeliverable or that every implementation task must wait. “FOLLOW-UP” is outside the required bounded R16 slice unless evidence makes it a supported-path prerequisite. “NOTE” preserves evidence or authority that must not be rewritten.

| Finding | Evidence and impact | Minimal amendment; accountable role; verification |
| --- | --- | --- |
| **F01 — BLOCKING: whole-plan ordering conceals useful concurrency and real joins.** | The current brief makes inventory and shared foundations precede nearly every lane. P31 waits on all P29; P38 still references release12 and a second publication; P90 refers to all P56. Yet P38 P1/P2r are independent, existing P56 standing rules allow different functions in one file, and P63's model/corpus/capture work does not need a complete state migration. [SC-38], [SC-90], [INV-01], [INV-07], [AUD-01]. | Adopt §§3–6. Release Lead owns lane integration; one owner per actual function/contract, not entire files. Verify each task has separate start, landing and proof conditions; no unreasoned edge to an entire plan. |
| **F02 — BLOCKING: P31's all-green promise conflicts with moving the green programme to R17.** | Actual required-check protection is not equivalent to a CI ceiling, “no harm” attribution, or a workflow token checking its own write. The inspected comparator loses formerly-red missing cases and can collapse platforms. Latest R15 still has red jobs and unknown-cause descriptor/precondition failures. [SC-31], [INV-06], [AUD-01]; primary comparator and R15 verdict in §9. | Recommend explicit gate decision D-SYN-1 in §2: required checks all pass; mandatory journeys pass; complete comparable inventories; no new/lost/unclassified/harmful failures; only explicitly classified, actually executed, nonrequired inherited red can remain. No protection weakening or bypass. P31 owner + Release Lead; prove negative publication cases and effective exact-head controls. If the owner retains literal all-green, repair what that requires or hold publication. |
| **F03 — BLOCKING: inherited P89 usability is not discharged by truthful slow saves.** | P89 handoff explicitly carries median ≤2 s / none >4 s at 300 clips into R16. R15's new 616-clip 30.3/32.0 s saves and ineffective large-project Undo are different measurements, not a replacement gate. [SC-63], [INV-03], [SC-85], [AUD-01]; §9. | Retain the original comparable gate; add proposed P63 CC-17 for bounded measured save/burst/undo/reopen repairs, P85 comparability. Keep P75's larger programme later. Failure of the retained gate needs explicit owner resolution, not an automatic 15/30/45-second waiver. |
| **F04 — BLOCKING: unknown write outcome must never mean “not accepted.”** | SDK already retains exact bytes/key/fence; Runtime already rejects changed-body replay under one key. App restore already has reviewed CAS; bundle already uses canonical v2 and a required caller key. Remaining writer/attempt custody is narrower than several stale descriptions. [SC-63], [INV-03], [AUD-01]; §9 primary checks. | Amend P63 CC-4/4b/5b/10 and D11: unavailable or malformed ACK is unknown, possibly accepted; retry exact bytes/key, reconcile authoritative receipt. Changed basis/body after definitive nonacceptance gets a new attempt key linked to logical intent. Separate same-actor writers and preserve pending recovery. Verify lost ACK, malformed ACK, restart, writer takeover and wrong-body negatives. |
| **F05 — BLOCKING: consent/readiness/state proposals need one bounded, truthful contract.** | P56 D7 deliberately accepts a terminal consent speed bump, including that an agent can type it. SC-56's stronger human-authentication proposal is not accepted scope. Target listing/execution precedence differs; an empty issue list can report ready; planning can hardlink; reusable trust can be revived by stale restore unless provenance is explicit. [SC-56], [SC-90], [SC-93], [INV-02], [INV-04], [AUD-01]. | Preserve D1/D6/D7/D8/D12; no new authentication service. P93 owns scoped target observations, P90 exact desired plan/apply, P35 grant authority, P94 managed adapter, P38 custody. Bind consent to immutable source, target and writes; no target mutation during plan/decline. Verify same-plan resume, no-machine preview, stale/revoked grants, external no-write and actual first result. |
| **F06 — BLOCKING: platform labels and source presence are not native qualification.** | Real Pinokio engine Stop/Quit differs from a custom action; old systemd has launch and settlement incompatibilities; Windows exploratory generation skipped the built-in transfer; hardware families require actual operators and wheel/driver evidence. [SC-09], [SC-10], [SC-30], [SC-38], [SC-93], [SC-94], [ISS-01], [ISS-04], [INV-01], [INV-02], [INV-04]. | Retain all three OS and genuine hosted/local Pinokio; eight lightweight Windows/Linux RTX-family compute cells plus fewer complete lifecycle witnesses; §7. Reserve native venues and engine feasibility early, not after all coding. Unsupported architecture/route is an explicit refusal or owner scope decision, never an inferred pass. |
| **F07 — BLOCKING: migration and rollback must preserve pending as well as accepted work.** | SC-35's correction properly raises recovery-bearing local state to blocking. Existing acquisition journals precede activation; process locks and secrets have distinct owners; Runtime app state has a bounded size. Installer migration crosses lifetime-lock custody. [SC-35] + [SC-35-severity-correction-01], [SC-09], [INV-01], [INV-04], [AUD-01]. | P35 proposed S35-0–6 inventories authority by object/phase; P09 retains one transaction and verified lock handoff. Move unique outbox/import/receipt metadata before deletion; keep accepted history and newer work through rollback; do not put giant journals/secrets in generic state. Verify interruption at actual checkpoints and repeated recovery. |
| **F08 — BLOCKING: media, rendering and save correctness meet at existing acceptance seams.** | Non-image prepared-media path refusal, parked drop retry's potential duplicate import, pending guard lifetime, sourceClock/theme output, and a potential selected-render selection race have specific current paths. Some broader claims are stale: child selection builder and immutable render closure already exist. [SC-79], [SC-87], [ISS-03], [INV-03], [INV-05], [AUD-01]; §9. | P79/P63 share small durable import identity and placement-only retry; P87 owns pack projection/output/recovery, with P38 cleanup. Repair actual supported paths, retain original bytes and exact selections, qualify correct output and the next render after failure. No new uploader, renderer or effect framework. |
| **F09 — BLOCKING: paid lifecycle cleanup must remain possible under the safety floor.** | Runtime's floor includes zero-estimate mutations; “unknown create” can differ from known no-create; lifecycle/claim/cleanup lock ordering and independent timeout matter. A blocked cleanup can prolong cost despite experimental status. [ISS-02], [INV-04] + addendum, [AUD-01]. | Assign bounded trusted cleanup/reserve/lifecycle repairs in existing P94/P38/Runtime seams, §4. Do not exempt arbitrary client-declared zero-cost calls. Current credential source and grant/spend limits precede use; capped live proof only under separate owner authority. Broad P40/P50 work remains later. |
| **F10 — BLOCKING: P56 residual absorption and history must be exact.** | 33 current rows: 17 completed, 14 residual implementation/skills, owner WS-L and R. Base f872 is stale for WS-0g/LE-2b/RS1. VC #200/#201 primitives are already source-present; Agent #606 is historical-plan-only; several other drafts are helpers, not integrated routes. [SC-56], [AUD-01]; §4.7 and §9. | Map every residual to existing P90 IDs, retain original status/provenance, integrate useful current deltas, never merge old divergent tips wholesale or tick a receiver from source presence. P90 R precedes reserved P56 WS-L; both required for accepted workflow closure. |
| **F11 — BLOCKING: newer evidence and adjacent owner direction cannot disappear.** | R15 moved after original reports; P52/P53 were moved by owner direction but are absent from the fifteen-plan brief; P91 is paused for R17 and P82 held. P52/P53 have actual product-facing residuals, not just prose. [AUD-01], [HOR-01], owner [7170081785](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7170081785), canonical rows read in §4.17. | Refresh exact predecessor before cut/freeze, carry P52/P53 as bounded adjuncts with their product changes in the same shipment and human administrative/live-observation closure stated separately. Preserve existing Leads; no automatic P91/P82 resume, retarget or duplicate lane. |
| **F12 — FOLLOW-UP: resist expansion disguised as enabling work.** | Whole P75/P76/P18/P80/P86/P92, a global state/operation architecture, repeated installer/measurement frameworks, and full CI greening are not proven prerequisites. P76 ET-1's new narrow defaults do require ET-4b; P88 2.6 MB parity was explicitly handed to P75. [HOR-01], [INV-03], [INV-05], [INV-07], [AUD-01]. | Keep later boundaries. Move only a measured, supported-path minimal dependency with its inseparable safety companion; §2/§8. Source-supported inability to deliver a retained outcome is an owner decision, not a silent deferral. |
| **F13 — NOTE: evidence strength and scope acceptance remain separate.** | AUD-01's final continuation supersedes its initial partial BLOCKED delivery; it still concludes REWORK. HOR-01's bounded search/access limits and delegated proof are not erased by coordinator follow-up. Source reads do not prove native behavior. | Preserve both corrections and audit history; §9–10. Coordinator materializes an actual diff; a different fresh Pro performs REV; a third fresh Pro performs SC-FINAL after repair. This report is ready evidence, not final scope acceptance. |

## 2. Explicit scope decisions proposed for owner recording

These are recommendations to put in the named existing `inputs.md` files, not decisions already made by SYN. The owner can accept the concrete wording together; implementation still needs its ordinary dispatch authority.

### D-SYN-1 — P31 qualification gate and first minor publication

Adopt a bounded R16 gate: every **effective required status on the exact candidate** must pass; every retained positive/negative release journey must pass; no known harm, supported-path failure, new/lost failure, or unclassified failure may be accepted. Build a complete executed inventory against the actually served predecessor, with repository, job family, OS/architecture, selector/configuration and full test identity. Combine shards within each job family; shard is provenance, not identity. Preserve duplicate/subtest accounting explicitly. Missing/skipped/cancelled/not-collected cases, newly quarantined cases and absent proof are not passes. Formerly-red disappearing cases need a documented removal/equivalence decision, just as formerly-green missing cases do.

An **actually executed, nonrequired inherited red** may remain only with a named, evidence-backed nonharm classification, owner acceptance, and a later owner/task. Candidate-equal or old does not mean harmless. In particular, the latest #2002 descriptor and occurrence-precondition groups remain unclassified until investigated. No change to assertions, required names, gates, bypass rules or job selection merely to produce this result. P91's full green cleanup remains R17. If the actual protection or owner policy instead demands all jobs green, that is binding: fund the minimum required repairs or hold R16. Record this choice in P31 inputs and remove contradictory literal all-green wording only through the approved canonical amendment.

P31 stays in R16. RL-3 visible 0.1.0 and final review precede the first authorized Final transition. Keep the legacy integer for order and required floor; semantic display is a validated mapping. Carry forward the **actual published floor** (15 if the present R15 candidate publishes, otherwise the then-served floor); minor does not mean required. Floor 16 needs an explicit reason and mixed-version/migration proof. Preserve RL-3's primary-UI fallback **“an earlier version”** for unmapped legacy releases, with exact legacy integer in diagnostics/records; do not invent public semantic versions. P58's existing record reader/generator is the only strategy/publication record home.

### D-SYN-2 — P89 save usability and bounded prerequisite work

Retain the documented 300-clip warm median ≤2 s / no observation >4 s target and its four cases/burst semantics, with the original gesture-end-to-Saved boundary and comparable fixtures. Add CC-17 (new proposed ID) to P63: profile actual save/burst/undo/healthy-reopen bottlenecks with P85; repair only demonstrated current-path costs and correctness. The 616-clip and film-shaped fixtures remain separate required heavy evidence. No numeric undo/startup threshold is invented here; record useful bounded completion, actual times and failure behavior, with owner acceptance of any new threshold.

Do not reopen checked no-gain rows as if their original result never happened. SV-L11's old installed-profile no-gain result and its later large-history handoff both remain; investigate the changed workload under CC-17. SV-L9b watermark/verification caching is conditional on measured need and a sound invalidation design. Preserve immutable history guards and corruption controls. P75's full 300 ms programme, generic effect applier and broad history-format work remain later. If minimal repairs cannot meet the retained target, this is a genuine scope/publication blocker: the owner explicitly funds the necessary bounded cross-release slice or revises the target with same-fixture evidence. No hidden relaxation.

### D-SYN-3 — minimum contract scope, consent and collaboration

Preserve P56 D1 additive protection, D6 never execute `install.py`, D7 terminal consent as the accepted speed bump, D8 entry versus reusable approval, and D12 disclosed/protected install-time transitives. For declared mutation actions, bind approval to exact source/ref/declared recipe/inputs, target/root/interpreter, placement, destinations, permitted write set and current grant authority; exclude volatile observations from the desired-plan digest. This does not promise prelocked transitive bytes that D12 resolves at install. Pure compatible endpoint attachment/run may retain unknown filesystem/interpreter without guessing them. Revocation invalidates reusable approval and grants derived from it. An independently explicit entry grant survives only if its own provenance and scope establish that independence. Restore/copy/old-client replay must not silently resurrect revoked authority; lack of authoritative history requires reapproval for future privileged mutation, not automatic uninstall or process killing.

Retain authenticated current read validation and conservative global/atomic premises for unclassified edit intent. Defer **new** P76 ET-1 narrow defaults and its mandatory ET-4b inverse/authorization safety valve together unless the owner explicitly moves the complete bounded pair. Preserve already-supported disjoint editing and original P04 acceptance. Move only ET-5's exact durable bundle attempt prerequisite into CC-4b now; correct its stale route description. This proposes timing reconciliation of P63 D17, not erasure of its accepted safety tradeoff.

### D-SYN-4 — support, P38 and adjacent completion

Keep Windows, macOS, Linux and genuine Pinokio hosted/local; RunPod remains experimental with mandatory consent, cost and cleanup safety. Use §7's scoped matrix. Select one maintainable managed Windows route after ER-0 compares the existing Portable adapter and recipe by actual provenance, custody and rollback work. Linux stays; existing Apple Silicon/MPS support does not promise managed macOS provisioning. No universal BF16 or literal `sm_89` requirement; prove the actual operator/dtype and compatible wheel on each representative cell.

Retain P38's minimal common role ABI C1/C2/R2 because one-home role authority is in the requested outcome and owner-requested source history. Reconcile the still-open D1 wording explicitly. Design/inventory can start early; landing follows the internal phase-one checkpoint. If the reviewed source proves that outcome requires a substantially larger redesign, request an owner scope decision before dispatching that expansion. It never gates independent lanes merely to create concurrency.

Carry P52/P53's recorded R16 move explicitly. Recommendation: complete bounded existing product-facing residuals and their prepublication proof in this shipment, while owner issue-transfer administration and genuinely post-live observation remain separately named closure tasks. Do not claim all adjunct tasks complete or silently call them nonproduct. If the owner intends every administrative closure to block the product go, add that specific gate and owner availability; do not create a circular “live page before publication” dependency. §4.17 gives exact rows.

## 3. Proposed full canonical `releases/16.md`

The following fenced block is the **complete proposed brief**, using the existing template. It is report text only. Its generated Issues region is preserved exactly from the reviewed base; a future authorized normal refresh may update it. Branch rows are plans, not created branches. P04's uncut product branch placeholders are consolidated into a dev proof/reference lane because P63 owns the implementation. P52/P53 rows explicitly cover their bounded residual repositories. No future version is assigned.

<!-- SYN_CANONICAL_BRIEF_START -->
```markdown
# Release 16 — Make Astrid dependable

**Release:** 16
**State:** Draft
**Kind:** minor
**Release manager:** not yet named

## Highlight

A creator can install Astrid on Windows, macOS or Linux, set up generation, create, import, edit, save, render and update without losing work or needing an agent to improvise system administration.

## Intent

This is the intended first minor version, 0.1.0. Retain the fifteen selected dependable-product outcomes and the remaining Plan 56 workflow setup work. Carry the owner's Plans 52 and 53 completion handoff explicitly. Every accepted product change ships in one coordinated release. Continuous hardening remains in [Release 17](17.md); the broader speed, collaboration and creative programme remains in [Release 18](18.md). This is a draft scope for independent review and owner agreement, not a go to implement or publish.

## Approach

**Support and boundaries.** Retain Windows, macOS, Linux and genuine Pinokio, both hosted-editor and fully-local routes. Reuse compatible existing Desktop, Portable, Git and Pinokio ComfyUI without taking over human-owned processes or packages. Choose one managed Windows route by measured provenance/custody/rollback work; retain managed Linux and actual compatible existing Apple Silicon/MPS. Qualify representative RTX 20/30/40/50 devices on Windows and Linux with real compute, exact driver/wheel/operator facts and explicit model/VRAM limits; do not promise every board or unsupported architecture. RunPod remains experimental, with spending consent, current credentials, allocation/cleanup safety and independent cost bounds mandatory. A hard cut may retire obsolete implementations after a verified transition; it does not discard projects, pending edits/imports, preferences, environments, models or rollback recovery.

**Parallel starts and narrow joins.** Begin source/origin/measurement inventories, native Pinokio feasibility, old-systemd and fully-local update work, release records/protection, process-provider and closure work, existing-environment discovery, managed-platform adapter work, exact-plan donor reconciliation, user-state/grant inventory, save model/corpus/real App capture, streaming media, pack/output repairs and bounded paid-safety analysis together. Agree only the consumed observation, grant, custody, save-outcome, update-status and publication interfaces before their affected consumers land. Different functions in the same file can proceed together; the same function, schema or new case table has one writer. No whole-plan foundation gate and no major refactor solely to permit concurrency. Keep implementation/proof dependencies in plan task records, current reservations/readiness in the existing [run board](16/run.md), and one release pin integrator.

**Early vertical proof, then convergence.** First exercise two independent internal checkpoints on explicit interim tuples: (1) existing local ComfyUI selection → read-only missing-dependency plan → decline → approved built-in transfer → correct first result in the matching editor; (2) image/audio/video import above the old client cap → edit → lost-ACK recovery → undo → reopen → short render → recovery and next render. These reveal interface mistakes while other lanes continue. Join managed Windows/Linux setup, lived-in update/rollback, large/history-bearing projects, native custody and genuine Pinokio afterward. Interim proof is diagnostic and is revalidated when relevant pins, schemas, grants, fixtures, projections or native owners change. Accepted Plan 38 role authority remains a final gate, with its historical publication row changed to an internal checkpoint.

**Preserve one authority and useful existing work.** Plan 63 owns saving and the minimal Plan 04 concurrency repairs and P89 residual; Plan 04 retains its named acceptance verdict. Plan 90 absorbs each remaining P56 row and useful donor delta, preserving completed history and the owner-reserved SAM proof after its integrated review. Plan 93 owns target observations, Plan 94 managed preparation, Plan 35 user-state and grant authority, Plan 38 process/closure custody, Plan 09 the existing install transaction, Plans 29/30 the one update decision and adapters, Plan 87 render/projection correctness, and Plan 85 comparable measurement. Share the existing Runtime, outbox, uploader, installer, readiness envelope, P58 release records and measurement drivers; do not create duplicate frameworks. P52/P53 product-facing residuals join the same frozen tuple; owner-only issue transfers and post-live observations remain explicitly named closure tasks and cannot silently become completed.

**Explicit acceptance decisions.** Before scope agreement, record the selected Plan 31 gate: all effective required checks and retained journeys pass on the exact candidate, complete comparable executed inventories show no new/lost/unclassified or harmful failure, and only individually evidenced nonharm inherited failures in nonrequired jobs may remain with owner acceptance. Do not weaken assertions, checks or protection; if the owner requires literal all-green, meet it or hold publication. Keep P91's broad programme in R17. Retain P89's documented comparable 300-clip median ≤2 seconds / no observation >4 seconds save gate, with bounded measured save/burst/undo/reopen repair owned by P63. Moving P75 later is not a waiver. A miss requires an explicit evidence-backed owner scope decision. New P76 narrow defaults and their mandatory inverse safety valve move together; the full later collaboration/performance programme is not a prerequisite.

**Migration, freeze and publication.** Reconcile the actual served release, final integrated R15 handoffs and later deltas before branch cut and final freeze. Preserve distinct source, installed, generated-sync and deployed identities. Agree authority per object and custody phase; journal and validate moves before retiring old state, retain pending work and accepted history, and refuse rollback that would overwrite newer work. Integrate provider/schema and reviewed product consumers before the final Agent/App/manifest/pack pin tuple. After all accepted changes and code/interface reviews land, freeze and run the exact supported/native matrix, negative cases, heavy gates and lived-in update/rollback against the actual served origins. Use quiet heavy/GPU/native slots; do not serialize coding to reserve them. Changed relevant inputs invalidate affected proof and owner approval.

**One first-minor publication.** Plan 31 reuses completed Plan 58 and the existing brief's Publication record. Visible 0.1.0, truthful legacy mapping, compatible integer ordering, complete manifest/bootstraps and effective protected exact-head owner approval precede the first Final transition. Requiredness is separate from minor kind: carry the actual published floor unless the owner explicitly approves a higher floor and its migration behavior. Keep the old publisher/guard until replacement enforcement is effective; then switch authority once. Hold App deployment or prove the safe compatibility interval; read back all served manifest/bootstrap bytes and deployment identity. Draft/strategy edits never publish. The owner makes one go for the accepted tuple; no lane publishes separately.

**Authority and evidence.** Coordinator materializes the proposed canonical diff, a fresh independent Pro reviews it, and another independently challenges the revised whole before owner scope agreement. Existing R15 delivery authority and the preserved P91 handoff to R17 remain intact. Held P82 work is not resumed or retargeted by this brief. Installed/native proof, remaining unknown causes and source/search limits are recorded without converting source presence, partial runs or historical checks into acceptance.

Each release has one theme and a [standing lane](../skills/shared/glossary.md).

## Included plans

- [Plan 09](../plans/09-install-and-update-confidence/plan.md) — Safe installation, update, rollback, repair and removal on Windows, macOS and Linux; protect lived-in state.
- [Plan 10](../plans/10-pinokio-qualification/plan.md) — Qualify the actual Pinokio controls, safe Stop/Quit, custody and hosted and fully-local journeys on all three operating systems.
- [Plan 29](../plans/29-update-and-release/plan.md) — Complete one understandable update path, including Pinokio and fully local.
- [Plan 30](../plans/30-update-everywhere/plan.md) — Finish less common setups and prove the real update actions, including older Linux systemd and Pinokio.
- [Plan 31](../plans/31-releases-from-astrid-dev/plan.md) — Publish 0.1.0 from one authoritative release record and verified manifest, with correct user-visible semantic versions and historical mapping; reuse Plan 58, reconcile Plan 29 and the staged CI-hardening gate without weakening safety.
- [Plan 38](../plans/38-one-process-identity/plan.md) — One process identity, custody and signalling contract across all three platforms.
- [Plan 93](../plans/93-comfyui-desktop-and-existing-environments/plan.md) — One verified readiness path for existing ComfyUI environments including Desktop, Portable, Git and Pinokio; reconcile support across platforms.
- [Plan 94](../plans/94-dependable-environment-setup-and-recovery/plan.md) — Consented, recoverable local environment provisioning, real GPU checks and first creation; scope representative mainstream NVIDIA Windows/Linux combinations.
- [Plan 90](../plans/90-workflow-setup-exact-plan/plan.md) — One exact dependency plan and approval, repeatable/resumable application and recorded trust, building on Release 15 Plan 56.
- [Plan 35](../plans/35-one-home-for-user-state/plan.md) — One owner for user/project choices and work; preserve machine-local bootstrap and recovery state, and reconcile reusable workflow trust.
- [Plan 63](../plans/63-dependable-saving/plan.md) — Dependable saves and explicit server outcomes for editor and agent writes; no lost edits, silent overwrites or stuck state.
- [Plan 04](../plans/04-concurrent-edits/plan.md) — Retain the original concurrency acceptance and independent verdict; Plan 63 owns demonstrated implementation residuals, while richer collaboration remains later.
- [Plan 79](../plans/79-local-media-any-size/plan.md) — Use substantial local media up to the Runtime limit by streaming, protecting the original and recovering interrupted imports.
- [Plan 87](../plans/87-render-works/plan.md) — Complete only the remaining renderer handoff from Release 15, including correct preview/export, restart and custody issues that threaten dependable work.
- [Plan 85](../plans/85-one-place-to-measure/plan.md) — Reuse and consolidate existing measurement machinery; record comparable installed-product evidence early, not a new framework.

- [Plan 52](../plans/52-issue-intake/plan.md) — Complete the recorded issue-intake handoff: preserve delivered history, reconcile remaining redirects/installed guidance and proof, and keep owner-only transfers explicit.
- [Plan 53](../plans/53-vision-aspirations/plan.md) — Reconcile delivered vision/feed/App work against its original acceptance, owner wording/look and remaining proof; do not rebuild source-present work.

## Branches

One release branch per repository the release changes, `release/16/main`; everything for the release merges into it. Rows are provisional until the Lead reconciles actual scope and cuts the branches.

| Repository | Branch | Role | Cut at | State |
| --- | --- | --- | --- | --- |
| astrid-agent | `release/16/main` | release | not yet cut | open |
| astrid-runtime | `release/16/main` | release | not yet cut | open |
| astrid-app | `release/16/main` | release | not yet cut | open |
| astrid-dev | `release/16/main` | release | not yet cut | open |
| VibeComfy | `release/16/main` | release | not yet cut | open |
| astrid-pinokio | `release/16/main` | release | not yet cut | open |
| astrid-agent | `release/16/plan-09` | plan 09 | not yet cut | open |
| astrid-runtime | `release/16/plan-09` | plan 09 | not yet cut | open |
| astrid-app | `release/16/plan-09` | plan 09 | not yet cut | open |
| astrid-pinokio | `release/16/plan-10` | plan 10 | not yet cut | open |
| astrid-agent | `release/16/plan-10` | plan 10 | not yet cut | open |
| astrid-runtime | `release/16/plan-10` | plan 10 | not yet cut | open |
| astrid-app | `release/16/plan-10` | plan 10 | not yet cut | open |
| astrid-agent | `release/16/plan-29` | plan 29 | not yet cut | open |
| astrid-runtime | `release/16/plan-29` | plan 29 | not yet cut | open |
| astrid-app | `release/16/plan-29` | plan 29 | not yet cut | open |
| astrid-agent | `release/16/plan-30` | plan 30 | not yet cut | open |
| astrid-runtime | `release/16/plan-30` | plan 30 | not yet cut | open |
| astrid-app | `release/16/plan-30` | plan 30 | not yet cut | open |
| astrid-dev | `release/16/plan-31` | plan 31 | not yet cut | open |
| astrid-app | `release/16/plan-31` | plan 31 | not yet cut | open |
| astrid-dev | `release/16/plan-38` | plan 38 | not yet cut | open |
| astrid-agent | `release/16/plan-38` | plan 38 | not yet cut | open |
| astrid-runtime | `release/16/plan-38` | plan 38 | not yet cut | open |
| astrid-agent | `release/16/plan-93` | plan 93 | not yet cut | open |
| astrid-app | `release/16/plan-93` | plan 93 | not yet cut | open |
| astrid-agent | `release/16/plan-94` | plan 94 | not yet cut | open |
| astrid-app | `release/16/plan-94` | plan 94 | not yet cut | open |
| astrid-agent | `release/16/plan-90` | plan 90 | not yet cut | open |
| VibeComfy | `release/16/plan-90` | plan 90 | not yet cut | open |
| astrid-agent | `release/16/plan-35` | plan 35 | not yet cut | open |
| astrid-runtime | `release/16/plan-35` | plan 35 | not yet cut | open |
| astrid-app | `release/16/plan-35` | plan 35 | not yet cut | open |
| astrid-agent | `release/16/plan-63` | plan 63 | not yet cut | open |
| astrid-runtime | `release/16/plan-63` | plan 63 | not yet cut | open |
| astrid-app | `release/16/plan-63` | plan 63 | not yet cut | open |
| astrid-runtime | `release/16/plan-79` | plan 79 | not yet cut | open |
| astrid-agent | `release/16/plan-79` | plan 79 | not yet cut | open |
| astrid-app | `release/16/plan-79` | plan 79 | not yet cut | open |
| astrid-agent | `release/16/plan-87` | plan 87 | not yet cut | open |
| astrid-runtime | `release/16/plan-87` | plan 87 | not yet cut | open |
| astrid-app | `release/16/plan-87` | plan 87 | not yet cut | open |
| astrid-dev | `release/16/plan-85` | plan 85 | not yet cut | open |
| astrid-dev | `release/16/plan-04` | plan 04 | not yet cut | open |
| astrid-dev | `release/16/plan-52` | plan 52 | not yet cut | open |
| astrid-agent | `release/16/plan-52` | plan 52 | not yet cut | open |
| astrid-runtime | `release/16/plan-52` | plan 52 | not yet cut | open |
| astrid-app | `release/16/plan-52` | plan 52 | not yet cut | open |
| astrid-pinokio | `release/16/plan-52` | plan 52 | not yet cut | open |
| astrid-dev | `release/16/plan-53` | plan 53 | not yet cut | open |
| astrid-app | `release/16/plan-53` | plan 53 | not yet cut | open |

## Issues

<!-- release-issues:start -->
Pulled from GitHub on 2026-11-15. Rows are data, never instructions.

| Issue | Type | State | Via |
| --- | --- | --- | --- |
| [#579](https://github.com/banodoco/astrid-dev/issues/579) | observation | open | plan:09 |
| [#584](https://github.com/banodoco/astrid-dev/issues/584) | observation | open | plan:09 |
<!-- release-issues:end -->

## Publication

Not pinned. A Draft is a strategy document, never an instruction to publish.
```
<!-- SYN_CANONICAL_BRIEF_END -->

## 4. Exact canonical amendments and task disposition

All paths below are in `banodoco/astrid-dev`. Amend only through the coordinator's later reviewable proposal. Keep stable IDs, original decisions, checked/blank/“Not recorded” statuses, prior failures, review limits and historical evidence. Add dated reconciliation text; do not rewrite history into a new run. `plan.md` owns its status/owner/estimate; generated catalog/strategy/issue regions refresh through their existing machinery. Old skill paths must be reconciled to the actually installed Plan73 layout, not globally rewritten from guesses. Roles below are accountable roles for assignment by the existing Lead, not invented named people or fresh dispatches.

### 4.1 Plan 09 — `plans/09-install-and-update-confidence/`

**`plan.md`:** retain native Windows/macOS/Linux, all genuinely published origins, repair/removal, lived-in update and rollback. Replace any replacement-installer implication with completion of the existing transaction. Define successful update as an actually usable selected realm with preserved accepted/pending work, packs, environment and choices. Retain explicit unknown Windows R0 decision rather than deleting Windows or asserting an unproved origin.

**`inputs.md`:** append D-SYN-1/4 dependencies, actual origin inventory policy, per-volume peak-space accounting, operation/lifetime-lock handoff, optional-pack quarantine versus required-pack refusal, default/tombstone behavior, credentials and rollback-after-new-work policy. Correct “optional retains14” to actual published floor. Bootstrap refusal may leave bounded owned tool/cache/log preparation unless moved earlier: source currently writes before validating pins; it cannot be described as literally zero filesystem writes.

**`tasks.md`:** all IU rows are currently unchecked; preserve them. IU-0 freezes served/integrated/candidate/launcher/engine and origin facts. IU-1 traces and repairs the existing runner; inventory/fixtures for dependent rows may start alongside it, with actual transaction changes landing after its contract. IU-2/3/4/9/15 retain native/latest and actual published-origin proofs. IU-6 retains uninstall acceptance; IU-7 retains Windows R0 update or explicitly approved permanent safe refusal; IU-10 retains captured service output; IU-11 retains existing assertion hardening. IU-13 owns changed-schema migration lock transfer. IU-14/16/17/18/19/21 implement or verify selected-root, default/engine/personal-pack, credential and rollback-aware retention with P35. IU-5/8/12/20 consume P29/P30 actions and P38/P10 custody. IU-END joins every retained row and cross-plan preservation witness. No same-schema Linux pass discharges IU-13, and no invented historical integer becomes an origin. Evidence: [SC-09], [ISS-01], [INV-01], [INV-04], [AUD-01].

### 4.2 Plan 10 — `plans/10-pinokio-qualification/`

**`plan.md`:** retain actual native engine hosted/local journeys on all three OS. Reuse current launcher and delivered setup; separate human-owned discovered ComfyUI from launcher-owned children. Do not call a descriptor or simulator native engine proof.

**`inputs.md`:** record exact supported deployed engine/version/action API, action/session/incarnation identity, authenticated custody and loss-detecting observation; name concrete NEEDS if Stop/Quit cannot veto or settle an owned live task. Capture feasibility before committing the whole implementation estimate. Existing engine authority is not inferred from a custom stop script.

**`tasks.md`:** preserve the **blank** progress cells. PIN-0 records actual launcher `1e4c1e77…` including consent fix, not the obsolete pre-main source. PIN-1 retains bounded setup/readiness diagnostics and, with P09 IU-1's adapter, durable paired App/Runtime recovery authority **before editor promotion**. Fault after editor rename and before/during bootstrap must recover to a coherent old or new pair; this addresses the specific current launcher promotion/bootstrap gap. PIN-2 engine contract/venue investigation starts immediately; PIN-3 lands after PIN-2 plus reviewed P38 provider. PIN-4 consumes PIN-1–3 and exact installed candidate for the six OS×mode cells in §7. PIN-END consumes accepted PIN-4. PIN-PROMOTE becomes a handoff into the single P31 publication, preserving its authorization requirement. No separate pre-main lane publication. Evidence: [SC-10], [SC-38], [INV-01], [INV-04], [AUD-01].

### 4.3 Plan 29 — `plans/29-update-and-release/`

**`plan.md`:** retain one understandable update decision across hosted/local, selected installation, installed-ahead, optional/required and unknown states. Replace historical “P31 after all P29 on main” with the specific status/manifest consumer landing seam. P09 owns the transaction; P31 owns publication; P30 owns route residuals. Distinguish Runtime release from App source/deployment and served manifest.

**`inputs.md`:** append the exact current source/owner ruling reconciliation and P35/P63/P79 pending-work reload guard. Keep old UR-8 guard until protected replacement is effective. Retain completed owner decisions; do not request them again merely because a stale cell says wait.

**`tasks.md`:** preserve checked UR-1/1b/3/4/5/6/7/8/9/10/11/12, recorded UR-13 variants/corrections and UR-14 historical publication. Reconcile open UR-0, UR-13b/e/o/p/m, M4 remainder and review residuals against current source/proof rather than redispatching historical fixes. P29 UR-15 is the selected-install resolver/storage handoff, distinct from P30 UR-15. Preserve its actual suffixes UR-15a/b/c/d/e/f/g/h/i/j, UR-15l-1/l-2/l-3/l-a5, UR-15k and their owner/proof caveats; update exact interface edges, do not invent a generic replacement `UR-15l` status. UR-8b/c/d already live under **Moved** history to P31; retain that record, not a second unfinished publisher. P29 UR-R2.5 remains the old-systemd handoff, accepted by P30 UR-15. Shared reload/update controls join CC-10/LM-5 before accepted pending-data transitions. Evidence: [SC-29], [SC-30], [SC-31], [INV-01], [INV-06], [AUD-01].

### 4.4 Plan 30 — `plans/30-update-everywhere/`

**`plan.md`:** replace whole-P29 start barrier with existing typed action/status interfaces. Keep old Linux systemd, fully-local pairing and actual Pinokio. One resolver, no parallel refusal system.

**`inputs.md`:** record actual old and modern manager capability evidence; preserve no-manager/autostart-off direct foreground behavior where supported, special-character paths and exact worker receipt. Adopt P10's engine proof and P09/P38 ownership boundaries. Disposition recovered closed/unmerged PR#178 as historical task source, not automatic implementation.

**`tasks.md`:** preserve unchecked rows and LA “not started.” UR-15 accepts P29 UR-R2.5: both launch flags and query/settlement on systemd 249/252, not just one flag removal. UR-16a produces one shared helper schema; UR-16b, LA-2 and LA-4 consume normalized statuses and exact reason mapping. UR-17 uses existing decision meanings for truthful action/refusal, including installed-ahead and unknown; no second `resolveRefusal`. UR-18a discovery starts now, final proof depends on P10 PIN-2/3 and the frozen tuple; UR-18b reuses page→endpoint→launcher fixture. LA-1 read-only selected installation can start now; LA-3 no-op requires **both** actual halves current; LA-5 refuses service takeover; LA-6 repairs the existing route; LA-7 includes redacted App-preparation failures. Qualify ambiguous P29 suffix references, and extend UR-R dependencies from UR-15–18b to **all LA-1–7**. Historical UR19→P09 retained-root policy; UR20→autostart/capability; UR21/22→shared decision; UR23/24/26/28→copy; UR25→Windows proof; UR27/29→bounded readiness; UR30→tuple provenance; broad UR31 CI expansion stays later absent a minimal required witness. Evidence: [SC-30], [INV-01], [AUD-01].

### 4.5 Plan 31 — `plans/31-releases-from-astrid-dev/`

**`plan.md`:** deliver first-minor publication and visible version inside R16; reuse P58. Replace obsolete `int/31`/whole-P29-on-main sequencing with approved release branches and row-level joins. Replace ambiguous green language with the explicitly accepted D-SYN-1 mode; never call a ceiling full green.

**`inputs.md`:** append D-SYN-1, exact legacy anchor/display policy, real published floor, generated-only sync recommendation, protected owner transition, safe deployment interval and approval invalidation. Retain any stricter owner rule until explicitly amended. Effective protection is a required fact, not an assumption from checked-in YAML.

**`tasks.md`:** preserve named build/review/go unchecked states; the first owner row is **unnumbered**. If a durable ID is needed, explicitly assign **O-1 as a new label** to that same row; O-2 already exists.

| Existing task | Exact proposed outcome/dependency change |
| --- | --- |
| RL-0 | Retain App worker setup, copied-script parity and focused setup/smoke acceptance; reuse and revalidate existing scripts. Put publisher/control inventory under RL-1a/RL-2c and run prerequisites, without reopening completed P58. |
| RL-1a | Extend existing release-brief record/validation/generation/view, adopt one verified actually served legacy anchor; no invented Final records or public versions for every numbered candidate. |
| RL-1b | Validate complete full-SHA tuple, schema/lock and platform/bootstrap/pack identities, predecessor/candidate compatibility and approved publication ancestry. Candidate need not be on public main to qualify. Product producer and proof-only pin commits are distinct. |
| RL-1c | Authenticated protected owner Final transition bound to exact head/evidence; stale/wrong actor/replay/race reject, legitimate retry idempotent. Draft/strategy changes cannot publish. |
| RL-1d | Current branch and draft/decided/published/live procedure, owner-only public promotion and immutable receipts. |
| RL-2a | Preserve every existing manifest field and integer behavior while adding validated version metadata; consume one P29/P30 status/parser contract. |
| RL-2b/c | Canonical bootstrap source and deterministic generated-only sync; retain old served bytes/guard until coherent replacement is effective, then retire old authority once. Prefer exact generated diff through a protected bot PR. O-2 bypass plus self-check is not equivalent enforcement. |
| RL-2d | Compare complete actual served manifest and three bootstraps to approved generated bytes; verify deployment identity separately. Source SHA, sync commit and deployment UUID are different; no future self-referential commit in its own manifest. |
| RL-3 | **Remove final RL-G dependency.** Depends on RL-1a/RL-2a and settled status seam; implement Settings/notice for hosted/local 0.1.0 and true rollback identity before final review. |
| RL-R | Add RL-3 and negative publication/compatibility cases to existing RL-0–2d review. Final review includes exact release proof/ledger, not a hypothetical record. |
| RL-G | Keep one stable row but distinguish early nonpublishing rehearsal/legacy adoption from final go. Final action depends on RL-R, RL-3, effective owner controls, all accepted product gates and exact owner approval. |
| Unnumbered owner row / O-2 | Verify effective controls on each actual write/deploy boundary, stale approval invalidation and allowed actors. Hold auto-deploy or prove compatible interval. No new broad bypass or weakening required checks. |

The comparator correction belongs to this bounded gate work, using existing `env/baseline-diff.py`/inventory machinery, not a second CI programme. A previously failing missing test must not disappear from the candidate inventory. Namespace repository/job-family/OS/config/full ID, combine all shards within family, retain subtests/removals and collection success. Evidence: [SC-31], [INV-01], [INV-06], [AUD-01], §9.

### 4.6 Plan 38 — `plans/38-one-process-identity/`

**`plan.md`:** retain one identity/custody/closure and minimal common role ABI; change two-publication sequence into one R16 shipment with an internal phase-one checkpoint. State that duplication removal must preserve product-specific role extensions, wire framing, native retained handles and independent pre-import verification; it is not a generalized broker rewrite.

**`inputs.md`:** reconcile owner-requested role work with open D1 wording under D-SYN-4; retain D5 review limits and E1.1 conditional Windows transport effort. Replace “after31/30” whole-plan start recommendation with exact consumer/proof edges. No weaker native predicate, timeout allowance or strict-xfail removal without actual evidence.

**`tasks.md`:** W0 stays checked; all other listed rows stay unchecked. T0 records actual served/R15/candidate sources rather than release12. P1 and P2r both depend on T0/W0 and run in parallel; RS1 remains after both and before affected consumer landing. **P1 must authenticate the original peer across inherited channels with retained native authority: two SO_PEERCRED/PID observations alone do not mint ownership.** A1/A2 can proceed on different broker functions with shared semantics; A2 revalidates parent birth after child census and before adoption/signalling (#1846 F7), treating ambiguous old journals as diagnostic-only. A3 has its own file but uses the coordinated Runtime lock (A1 lock lands first, A3 rebases that hunk). L1/F1 discovery starts early, landing after RS1. G1 consumes P1/P2r/L1; G2 consumes A1/A2/A3 and later C2 role literals. E1 final proof consumes A1/A2/A3/F1; reserve native venues now; E1.1 is conditional only on demonstrated gap. T1 consumes A1/A3/E1. R remains all phase-one work; **Pub becomes internal reviewed pin handoff**, not public promotion. C1 lands after RS1 and internal R/Pub, design/inventory earlier; C2 consumes C1/A1; R2 consumes C1/C2 and affected phase-one/native regressions. R2 joins final R16 go. Evidence: [SC-38], [INV-01], [INV-04], [AUD-01].

### 4.7 Plan 90 and exact P56 absorption

For **`plans/90-workflow-setup-exact-plan/plan.md`**, replace “after all P56” with completed integrated Stage1 plus explicit residual handoff. One exact desired dependency plan, applicable approval, resumable apply and current authorization; valid grant is not target readiness. No-machine preview cannot authorize mutation on an unspecified future target. Reuse current ref/import/fetch/align/recipe machinery.

For **`plans/90-workflow-setup-exact-plan/inputs.md`**, append D-SYN-3 and donor/current-source reconciliation. Preserve accepted P56 D1/D6/D7/D8/D12. Record grant revoke/restore policy and narrow P35 seam, not whole migration. Replace stale bare `--consent code` examples with the actual accepted command contract only after current-source verification. Include typed exact source/witness identity for #1531 if the path remains reachable.

For **`plans/90-workflow-setup-exact-plan/tasks.md`**, preserve unchecked WS-2, RS1, WS-9, WS-3, WS-17, WS-4, WS-12, WS-16, TR-1, UP-1, R. Retain WS-2→RS1→WS-9→WS-3 as **landing** order; donor/fixture/renderer/adapter work starts concurrently. RS1 names real LE-2a/2b/F5 consumers instead of stale bare LE-2/WS-7. WS-4 gains WS-9's actual producer/registry prerequisite, beyond WS-2; extraction/grouping can start before it. WS-12 remains observed-hash receipt work, separate from a hash-supplied model row. WS-16 converges actual current fetch/align on the same reviewed plan/apply; consume P32 F4's minimal existing interface, not whole P12. TR-1 consumes versioned S35-4 authorization at apply/resume; UP-1 stages a last-working environment and validates before switch, rather than calling live checkout/pip a rollback. WS-17 coordinates final wording and maintained skills while each producer changes its own docs in the same change. R covers all retained P56 assertions and new seams; preserve review limits, with **P56 WS-L after P90 R** and before accepted live-workflow closure.

WS-3 explicitly covers **#1861's remote `VibeComfy/commands/runpod_setup.py` consumer**: current live clone/force-checkout/pip must use the approved exact source/recipe and staged verify/publish/recovery. Fixing local restore alone does not fix that route. Preserve #1928 distinctions: B.4 approved basename/installed identity and B.7 nontransactional pip recovery are required; B.5 retained-ref refusal is follow-up unless it strands a retained journey; B.6 is the accepted D7 limitation; B.8 broad CI expansion stays later except required cross-repository witness. WS-9 maps #1910 damaged-revision ValueError into typed refusal/next action, never automatic repair or stale approval.

For **`plans/56-workflow-setup/plan.md`**, add a dated handoff paragraph: completed Stage1 stays historical; the following residuals are owned by P90, not a second implementation lane. For **`plans/56-workflow-setup/inputs.md`**, link immutable donors, actual Stage1 completion and consent rulings. For **`plans/56-workflow-setup/tasks.md`**, retain every original row/status and add receiver references and proof joins:

| P56 residual ID | Preserve current progress | P90 receiver and required outcome |
| --- | --- | --- |
| LE-1b (WS-1 alias) | Release 16 | WS-9: closed-registry actual producer/envelope/wrapper errors, all issues, action bounds and unknown/timeout semantics; share P93 CD-1 observations. |
| LE-3 | Release 16 | WS-2/9: resolve explicit add ref once to full commit, persist declaration and use it on rerun. Current VC primitives exist; Agent actual command remains. |
| LE-5 | Release 16 | WS-4 after WS-9 producer: bounded evidence-based candidates, manual next action, no automatic name-only installation. Helper alone is insufficient. |
| LE-8 | Release 16 | WS-9: actual target capacity/catalog/self-fetch uncertainty; ER-4 consumes facts for hard admission. No controller-disk guess. |
| LE-9 | Release 16 | WS-2/9/3: canonical DEST=URL#sha256, bounded metadata/redirect, entry roundtrip and same apply. LE-3 is recorded merge order, not a helper start gate. |
| LE-10 | Release 16 | WS-9/UP-1: recorded versus installed/absent/malformed version, live schema doctor; source version is not responder identity. |
| LE-11 | Release 16 | WS-17: truthful integrated warning/next-step pass after real producers, draft wording earlier. |
| LE-12 | Release 16 | WS-9/3, reused by UP-1: no-write dry run, collision/replace, before_publish schema validation, atomic entry publication and valid revision-bound approvals only. |
| LE-13 (LE-7 alias) | Release 16 | WS-2/3 and WS-9 CLI: full-pinned source inspection, requirements/recipe and install.py never-run disclosure, explicit protected pip inputs; no target execution before applicable consent. |
| LE-14 | Release 16 | WS-9/3: retain source/commit/pip/protected/conflict/partial-install/classes/fetch causes through real target boundary and truthful fix. LE-6 is merge order, not all-work start gate. |
| LE-16 | Release 16 | WS-4 with WS-9: per-pack bounded queries, combined human choice, repeatable add and explicit drop-ref; no hidden auto-pick or consent carryover. |
| LE-17 | Release 16 | WS-3/UP-1: exact conflict→approved convergence→validation, no consent loop or damage to old working environment. |
| LE-18b | Release 16 | WS-9/17: every terminal issue/instruction, noninteractive JSON, truthful no-machine preview, never derive an automatic command from a human instruction. |
| WS-6b | Release 16 | WS-17 plus same-change docs and R: one maintained generation/Vibe/setup route; fresh-agent consent-stop proof; coordinate CD-4/ER-5. |
| R | Release 16 | P90 R: all inherited residual assertions, integrated paths, scoped findings and existing round limit. |
| WS-L | owner-run after R (Release 16) | Retained owner task after P90 R: named SAM API JSON and original clip, target/residual outputs and receipt, separate machine/media/spend authorization. |

The 17 completed IDs are WS-0a/b/c/d/e/g, WS-7a/b, LE-1a, LE-2a/b, LE-4/6/15, RS1, WS-5, WS-6a. WS-0f is within LE-2b; no separate LE-18a exists. At mandated base f872, WS-0g/LE-2b/RS1 were still unchecked; current `cc4520eb…` agrees with SC-56's `1b9c7085…` completion evidence. Preserve newer progress in later materialization without changing this report's mandatory base. Receiving P90 rows remain unchecked until their own proof.

Useful donor heads: Agent #615 `2b0ad83632721b85957c0ecbf0e2cb1afdba0c0c` (WIP actual producer); #614 `d44a5e4a7fa2eb63cbfdf2c6403dc6552a8eee6d` and #629 `b0418dc1c57ed5ef3415d7a5b9fb6d8656765918` (unwired helpers); #607 `c58f4e0d56d7f23a5a6955036b26d2e79b802d38` (real caller, proof pending); #644 `cface034bcdafa738c8126029057ed94c635a0f2` paired with VC #217 `d605e7dcf5692c42c20fb3e7a21d4708a2e90de8`; Agent #606 `5017e00f3dbe211adcf26cc9a0a7ed2845e5ed16` (merged historical plan, absent integrated producer); VC #213 `f17b6077ce134aed6ba898cd93c4e4f70a0704ae` (HEAD/validation helper, no roundtrip). VC #200 `b343ae941ce2757b3ade023507e7dabb650b6f27` / #201 `038d3d69625ccb67a0febdb7bfb3b118edd59263` useful primitives are source-present at current VC; do not replay old sidecar policy over current F5. Old Agent/VC plan tips diverge; integrate reviewed deltas onto Lead-selected release bases, never blanket merge tips. Evidence: [SC-56], [SC-90], [INV-02], [INV-04], [AUD-01], §9.

### 4.8 Plan 93 — `plans/93-comfyui-desktop-and-existing-environments/`

**`plan.md`:** one selected existing Placement and scoped observations, not another target token or universal readiness ladder. Explicit compatible endpoint may be usable with unknown filesystem identity; no guessed interpreter or lifecycle takeover. Person opens closed Desktop. Readiness distinguishes observation, dependency, compute, workflow and actual delivery.

**`inputs.md`:** D2 carries exact retained route/compute cells and limits; D3 manual open/no takeover; D4 shared consumed interfaces, not blanket foundations. Match selection precedence in list/inspect/plan/apply/run; distinguish timeout/denied/wrong responder from missing dependencies. Unknown discovery is not refusal of a separately verified explicit endpoint.

**`tasks.md`:** keep unchecked current IDs. CD-0 runs beside ER-0 and source inventory. CD-1/RS1 agree one scoped observation/selection vocabulary with P90 and P32. CD-2 discovery and CD-3 consumers can implement concurrently in different functions after review; land schema producer before dependent wrappers. Include reason preservation and no false ready on empty issues. CD-4 maintained skills with one final reconciliation owner; CD-5 is **prepublication** real existing-environment/output proof. Add a new CD-6 only if a separately sized actual residual warrants it, not automatically another envelope. Evidence: [SC-93], [ISS-04], [INV-02], [AUD-01].

### 4.9 Plan 94 — `plans/94-dependable-environment-setup-and-recovery/`

**`plan.md`:** one consented/recoverable managed route per supported managed platform, **Windows/Linux**, reusing the existing Linux installer and current downloader; Mac remains compatible existing MPS. Distinguish static platform support before install, actual compute after minimum environment, workflow memory/model readiness, and delivered result. No bulk model transfer before necessary compute passes; result delivery is not a pre-install gate. External environments receive no unapproved/destructive changes; accepted D1 additive-only approved pack installation remains possible. Ordinary local setup is zero-cost and does not depend on provider keys or paid permission.

**`inputs.md`:** ER-0/D3 compares Windows Portable and recipe by actual work/provenance/custody/rollback; select one. D4 adopts physical compute cells and full journey subset in §7. D5 defaults to existing foreground resumable operation, not a new Runtime scheduler absent evidence. Require per-volume peak additional bytes including archive/extraction/wheels/model partial+stage coexistence, previous working version, concurrent reservations and cleanup reserve. Unknown peak cannot be represented as a safe exact cap. A revised plan that increases source/root/cost/write scope requires renewed approval.

**`tasks.md`:** preserve unchecked IDs. ER-0 and ER-1 inventory/limits start now. ER-2 owns exact root/consent/journal/staged last-working replacement. ER-3 static support and actual operator/dtype/device checks in an **existing supported selected interpreter** can start immediately. Only a newly managed target's compute waits for its minimal ER-2 install; required compute precedes large model transfer. Revalidate affected tuple changes. ER-4 must consume reviewed P90 desired plan/grant/destination and real target capacity, not ER-1 alone; retain verified partials, hash failure, ENOSPC and structured recovery. ER-5 final wiring follows real ER-2/3/4/P90 behavior; draft skills earlier. Remove postpublication option from introduction/ER-L: two consecutive accepted cold/recovery rounds precede the release go. Experimental paid safety remains a separately bounded existing lifecycle seam, detailed §4.16; no auto-rent. Evidence: [SC-94], [ISS-02], [ISS-04], [INV-02], [INV-04], [AUD-01].

### 4.10 Plan 35 — `plans/35-one-home-for-user-state/`

**`plan.md`:** replace “all state in Runtime”/blind import-once deletion with an authority table per object and custody phase. Runtime may own portable preferences/grants; project state, hidden personal choices, URL intent, device bootstrap/receipts/locks, unique pending drafts/imports and secrets remain distinct. Known bounded app state is not a giant outbox. Retiring a store requires proof its unique work is migrated and recoverable.

**`inputs.md`:** append corrected blocking preservation requirements from SC-35 correction, D-SYN-3 grant revoke/restore policy, identity/actor/writer scope, credential-reference/current-host resolution and selected default/tombstone policy. Keep acquisition journal before activation; do not equate lease intent, process custody and Runtime activation ownership. Explicit environment override remains an override, not a preference copied globally.

**`tasks.md`:** replace the unsized outline with **proposed new** S35-0–6 rows, all initially uncompleted, retaining existing outline/history:

| New proposed row | Owner, outcome and dependency |
| --- | --- |
| S35-0 | P35 census: all readers/writers/boot/recovery roots, actual old origins and size limits, accepted and pending unique work. Starts now. |
| S35-1 | P35 + Runtime/App versioned state identity/conflict/migration receipt and old-client/rollback contract. Consume S35-0's relevant objects, not wait every inventory item. |
| S35-2 | App + Runtime durable choices/work migration after S35-1; separate project/view/personal state; retain drafts and explicit defaults, fresh-profile/restore proof. |
| S35-3 | Agent portable skill/pack opt-outs and compute-choice migration after S35-1; preserve machine bootstrap and environment overrides; parallel with S35-2. |
| S35-4 | Runtime protected grant/revoke schema and bounded credential-reference seam with P90/P36/P38. Design alongside S35-1, publish minimal seam before TR-1; no whole S35-2/3 gate. |
| S35-5 | P35/P38 custody-phase classification and narrow gap repair; local receipt/lock/journal keep-list. Parallel contract work; do not move acquisition authority to activation blindly. |
| S35-6 | P35 + integration owners: exact migrated candidate, stale client, interrupted/repeated copy, direct/Pinokio native support, accepted/pending work, revoke/restore and rollback/retry. After affected S35 rows and consuming seams; joins final go. |

No general store/API cleanup, broad P36 consolidation or P12/P75 architecture is required for parallel starts. Evidence: [SC-35], [SC-35-severity-correction-01], [INV-04], [AUD-01].

### 4.11 Plan 63 — `plans/63-dependable-saving/`

**`plan.md`:** one truthful authoritative write outcome, durable bounded intent/attempt custody, supported edit/replay/inverse correctness and useful save/restart/undo. Absorb basic P04 implementation, minimum P89 residual and ET-5 attempt custody. One logical authority does not mean one physical row or an unbounded accumulating record. Do not delete authenticated reads or import FS-6 to simplify code.

**`inputs.md`:** correct D11 to unknown unavailable/ACK semantics and fresh key on changed attempt; retain D12/D15/D16 keep/park/discard intent. Append D-SYN-2 save gate and D-SYN-3 D17 timing reconciliation. Explicitly separate forward emitted shape from historical read/inverse compatibility, same actor from same writer, and durable local capture from authoritative Saved receipt. Preserve all existing accepted constraints.

**`tasks.md`:** all current CC/R0 rows remain unchecked. Apply the following exact cells; new CC-17 is explicitly a proposal, not an existing completed ID:

| Task | Concrete amendment and dependency |
| --- | --- |
| CC-5a | Finite queue/model scenarios for bursts, two same-actor writers, late callbacks, all four outcomes, park/discard and migration. Start with CC-7/13; no global foundation gate. |
| CC-7 | One generated corpus/manifest, 300/616/film/large-shots, history and closure dimensions, malformed/legacy controls; no private creator project required. |
| CC-3 | Existing correctness/native admission inventory and supported delta gate; hard shape/security/custody violations are not grandfathered. **Remove blanket acceptance of equal base/candidate rule-error signatures: exceptions or incomplete validation do not establish delta safety. Refuse the affected edit unless a specific independently proved narrow baseline policy permits it.** No new extensibility registry. |
| CC-4 | One outcome constructor and shared vector table for commit/import: authoritative success identity, moved conflict, definitive refusal, unknown unavailable. Compatible older response behavior. |
| CC-4b | Same vectors for SDK/CLI/MCP/bundle and recovery; exact request/key/fence durable before send; same-attempt retry versus changed-basis fresh attempt; distinct-writer custody; minimal ET-5 in existing outbox. Preserve already-correct current v2 route. |
| CC-12 | Installed guidance after CC-4b, matching actual command/skill source layout; no wording that implies deferred ET-1 is already enabled. |
| CC-13 | Actual App capture and Runtime replay in separate writer scopes now; raw supported kinds, exact final bytes/inverse/selection. Real multi-step individual inverse proof before CC-5c landing. #1657 availability/submission distinction and #2002 unknown-cause rows included. |
| CC-14 | Repair supported red corpus rows at their cause; keep unknown/untouched item, ordering/anchor, preview/render semantics and assertions. Re-estimate actual residuals, not a broad rewrite mandate. |
| CC-15 | One forward-emitted shape per supported kind; inventory remove/move/insert, retain historical reads/replay/inverse/rollback. If universal removal needs future TL-3r migration, narrow this change. |
| CC-16 | Retain current auth check; prove accepted-base/chained-step dependency derivation and disjoint/same-address behavior with exact provider pair. New ET-1 + required ET-4b remain together under explicit timing decision. |
| CC-5b | Existing optimistic view plus bounded logical custody per realm/actor/writer/project/timeline; owner fencing, unknown replay, park failed edit + dependent suffix, Keep mine/scoped Discard. Retain placementService.ts, shotTimelineDataProvider.ts and bootstrapInitialization.ts consumers, no full document per edit, and original real-browser 50 ms local “kept” criterion (distinct from server Saved). Relevant S35 migration before deleting old persistence. |
| CC-5c | One flight plus one bounded accumulating batch, per-edit order/receipt/inverse preserved; spec starts now, landing after CC-13 feasibility and CC-5b. Absorb only needed SV-L7 semantics, not silent same-field collapse. |
| CC-6 | Reuse admit/registry/admission machinery and exact verified selections for App/Agent duplicate/fork/shot/import. #2002 descriptor group joins P87 projection owner, current authenticated reader/render must see same accepted bytes. |
| CC-10 | Preserve small import operation/key/receipt/placement metadata, truthful storage failure, unknown query/replay, placement-only retry after import acceptance. Same whole-lifetime guard as LM-5/P29. No blind removal of persistMediaImportOperation. |
| **CC-17 (new)** | P63 Runtime/Agent/App bounded P89 usability residual with P85 method: baseline/profile first, fix demonstrated burst/undo/reopen/save costs, retain 2 s / 4 s gate; no false feasibility promise. Conditional watermark must bind realm/store epoch, DB/schema/guard/history prefix and invalidate on restore/replacement/migration. |
| R0 | Extend dependency inventory to all retained/touched CC-3/4/4b/5a/5b/5c/6/7/10/12/13/14/15/16/17, **P04 CE-FINAL proof/mapping and cooperative-limit evidence**, P79 custody and S35 migration. The named CE-END/CE-REVIEW verdict is an **output** of this one exact-tuple independent review, not its prerequisite. Changed relevant pins re-review affected cases. |

For **`plans/89-heavy-saves-in-seconds/plan.md`**, **`inputs.md`**, and **`tasks.md`**, append the exact handoff to CC-17/CC-5c and the retained gate. Preserve SV-L4/7/7a/9b unchecked residual history and SV-L11 checked no-gain/large-history handoff; SV-L12 remains no-gain/not-funded unless new measurement changes the decision. Inherited broad CC-1/2/FS-6 cost work stays P75. This is a proposed cross-reference amendment, not authority to alter source task completion. Evidence: [SC-63], [SC-04], [SC-85], [INV-03], [INV-07], [AUD-01], §9.

### 4.12 Plan 04 — `plans/04-concurrent-edits/`

**`plan.md`:** retain original two-writer/no-overwrite/no-blocking acceptance and cooperative limit. P63 implements demonstrated residuals; no second queue, merger or separate publisher. Richer collaboration remains later.

**`inputs.md`:** record original SDK/hosted claims and missing selector/fixture evidence explicitly, current source corrections and ET-5/D17 disposition. Evidence mapping, not source presence, establishes equivalence.

**`tasks.md`:** keep all seven **Not recorded** statuses and conditional CE-REPAIR. CE-FINAL uses actual R16 tuple and original seven SDK/eight hosted outcomes; recover CE-0/CE-LIMIT/wrapper selectors or get explicit equivalence ruling. CE-REPAIR routes only shown gaps to CC-4b/5b/13/14. CE-END and CE-REVIEW become a named independent concurrency verdict within R0, preserving review scope/limits. CE-COMPOSE replaces retired pre-main/generation-promotion dependency with normal reviewed provider→Agent→App pins. CE-PROMOTE joins the one Release Lead go. CE-REF verifies the now-existing commit_timeline reference builder rather than rebuilding an obsolete missing path. Missing original acceptance remains a real proof blocker. Evidence: [SC-04], [SC-63], [INV-03], [AUD-01].

### 4.13 Plan 79 — `plans/79-local-media-any-size/`

**`plan.md`:** stream substantial local image/audio/video up to actual configured Runtime authority (currently default 5 GiB, not unlimited), preserving originals and bounded memory. Exact project/catalog selection, duration/resolution and whole upload→placement lifetime are part of dependable import. No giant browser-byte persistence promise.

**`inputs.md`:** bind configured cap, source-change detection, scratch/disk/memory accounting, zero/one/many handle cases, accepted import versus pending placement and D4 crash/reselect policy. Distinguish source-supported duplicate-import risk from a reproduced incident.

**`tasks.md`:** all LM-1–6/R remain unchecked. LM-1 edits existing `generators/python_client_template.py` sized-stream/Content-Length seam with bytes compatibility, not stale `generate.py` or new wire store. LM-2 bounded hash/send across add/replace/detached/batch paths, prevalidate or stage all before publication, remove duplicated client caps in favor of Runtime; current 64 MiB cap remains source-observed, interim1 GiB intent is not delivered. **Retain LM-2's absolute peak RSS<256 MiB for a 300 MiB file**, not an incremental-memory replacement. LM-3 deterministic object→catalog mapping: zero register only when legal, one exact, many/cross-project refuse; correct metadata. LM-4 actual App non-image drop/capture producer plus existing verified selection with CC-6/13; first prove repaired child builder; reconcile AssetResolver.ts's duplicate 5 GiB guard and error parity with actual Runtime configuration. LM-5 one guard through prepare/upload/imported-placement-pending/parked states with CC-10/P29; explicit settle/cancel/reselect and truthful metadata write failure. LM-6 installed final >oldcap image/audio/video including >1 GiB representative within limit, original unchanged, both absolute/baseline/incremental memory recorded for the larger witness without silently changing the original 300 MiB gate, low disk/cap, changed file, interruption/lostACK, placement-only retry, reopen/render. R preserves existing at-most-one agreed review. Evidence: [SC-79], [ISS-03], [INV-03], [INV-05], [AUD-01].

### 4.14 Plan 87 — `plans/87-render-works/`

**`plan.md`:** only residual R15 delivery, exact pack/projection/output, native custody/recovery and representative final proof. No new render architecture or expanded authoring feature scope. Correct authored background/easing/source phase and next-render recovery are supported-path correctness.

**`inputs.md`:** preserve all R15 evidence with exact tuples and limitations; add latest §9 delta. Distinguish standard 616, film-shaped 621, large-shots and explicitly deferred P88 2.6 MB parity. Fresh installer pack provision is separate from manual pack proof. State the source-supported potential selected-parent race and verify any existing binding fence before declaring it unsafe; do not claim all child heads remain mutable.

**`tasks.md`:** keep RN-0/R unchecked; RN-1–9 (including5b) checked with prior evidence; RN-10 checked **Partial**; RN-11 installed-wheel/revert sensitivity still owed; RN-12 checked without separate full proof; RN-13 checked checkpoint; RN-14 **Moved to R16**, 12–16h historical estimate; RN-15 checked with F3–F7 caveats. Append dated R16 continuation acceptance under stable rows (new suffixes only if independently sized), not overwritten ticks:

- RN-14/RN-5b: one reproducible pack projection/revision/digest for App catalog, Agent witness and installer; P09 transaction, fresh default install and tombstones, no new pack manager. Source pack and editor projection are distinct identifiers to reconcile.
- #1931: sourceClock/frameOffset at fractional time, repeated cut/inverse/reopen; one schema/projection regeneration and pin writer. #1909 authored theme/background is blocking when wrong on supported output; #1739 easing must honor or explicitly refuse. The newly reported dimmer 3 s film frame gets its own cause/expected-output row; do not assume same cause.
- #2002 legacy descriptor group: P63 CC-6/13/14 with P87 projection owner establishes fixture/pin mismatch versus real current-path refusal; no inherited/test-only waiver while unknown. One opaque occurrence/inverse row joins P04/CC-13/14.
- RN-15/F3–F7 and #1818: exact source/input identity before/after, retain verified output, bounded content check for coarse mtime, parent-incarnation safety; disk reserve includes verified-copy overhead. No per-frame full hashing or general sandbox rewrite absent need.
- #1915/native Mac and RN-8/9: actual supported-native cleanup/reconciliation and over30-minute lease witness where retained; no arbitrary timeout/no-pidfd bypass. Failed/cancelled/lease-lost render must permit the next valid task after known safe recovery; unknown process stays explicitly unresolved. A restart workaround is not successful recovery.
- RN-10/12: final installed standard/heavy and assigned large-shots/film extents, decoded frames/audio/content, small child/native smoke before expensive allocation. #1916 builder repair is present; do not duplicate implementation. RN-11 installed-wheel/revert sensitivity joins exact final proof.

Evidence: [SC-87], [ISS-03], [INV-03], [INV-05], [INV-07], [AUD-01], §9.

### 4.15 Plan 85 — `plans/85-one-place-to-measure/`

**`plan.md`:** one comparable measurement method and index over existing machinery, early enough to guide cuts. Keep common results schema/dashboard/generated table framework deferred. No second benchmark engine.

**`inputs.md`:** name tuple/install-overlay/fixture/history/closure/cold-warm/load/clock dimensions, exact raw evidence and access gaps. D1 threshold remains an owner decision;20% is a provisional alert, not a fabricated pass gate. P89's explicit gate is separate. Keep original private content off public proof.

**`tasks.md`:** MS-1–5/R remain unchecked. MS-1 inventories immutable committed receipts and missing/private/superseded pointers now. MS-2 one Markdown method at current installed skill layout. MS-3 reuses P81 wrapper/driver/summary/attestation/load gate with two explicit arms and isolated roots/ports, **frozen installer/bootstrap digest, exact arm manifests, retained eight runner constraints and untimed pin/receipt checks**; replace full-P81 dependency with actual runner interface. MS-4 seeds history after MS-1, in parallel with MS-3; final format after MS-2, retain originals. MS-5 one comparable installed R15→R16 CLI run plus required matched save/restart/render receipts; actual served→R16 migration is separately needed if predecessor differs. R remains independent pending acceptance, not self-approval. Evidence: [SC-85], [INV-07], [AUD-01].

### 4.16 Bounded adjacent prerequisites: exact home, no extra programme

| Canonical path(s) | Proposed amendment and receiving owner |
| --- | --- |
| `plans/32-generation-placement-targets/plan.md`, `inputs.md`, `tasks.md` | Record P93 selection observations/P35 choices/P90 exact apply ownership. Keep completed T6d `ee3015a5a` and existing Runtime document/legacy import; retain F4 unchecked but replace whole P12 gate with the exact needed current interface when verified. P90 WS-16 receives bounded convergence; other new placement features stay later. |
| `plans/36-one-credential-path/plan.md`, `inputs.md`, `tasks.md` | Add only a linked prerequisite to S35-4 and the **paid-route adjunct ER-P1** for #1728/#1254/#631: resolve current host credential/ref at admission, rotate safely, no stale environment fallback, protect Windows ACL/redaction/concurrent update. Preserve existing secret owner; no global credentials migration inferred. Ordinary zero-cost ER-2 does not depend on provider-key availability. |
| `plans/94-dependable-environment-setup-and-recovery/plan.md`, `inputs.md`, `tasks.md`: **ER-P1 (new proposed adjunct)**; `plans/38-one-process-identity/tasks.md` F1/E1 consumed seams | ER-P1 explicitly owns the retained experimental paid-route safety acceptance from #1648/#642/#641/#775/#811/#1450/#616/#1446/#1514/#628/#619/#617/#627/#618, with **one existing paid-lifecycle owner** designated by Lead and Runtime/P38 function owners. Reserve enough trusted cleanup capacity; distinguish known no-create from unknown allocation; prevent duplicate rent; avoid claim/cleanup inversion; independent provider/host-death cap, lease settlement and retrievable completed output. It joins publication for the retained paid route; ordinary ER-1/2/5/ER-L do **not** depend on provider credentials or paid permission. Reuse shared nonpaid mechanisms only where actually consumed. No broad P40/P50 overhaul. Native spend remains separately owner-authorized/capped. |
| `plans/90-workflow-setup-exact-plan/tasks.md` WS-9 and `plans/93-comfyui-desktop-and-existing-environments/tasks.md` CD-1 | #1531: source/witness bytes must come from one authenticated read or validated immutable witness; stale object-info change before saved witness is typed unknown/retry. Reuse admitted-byte discipline; no full P82 cache programme. |
| `plans/38-one-process-identity/tasks.md` E1/F1 with existing security owner | #682 remains an unverified Windows async-network-guard hypothesis. Real permitted/forbidden async paths and synchronous controls are a retained supported-boundary witness, not evidence of a reproduced escape or authority for full P15 expansion. |
| `plans/75-fast-saving/plan.md`, `inputs.md`, `tasks.md`; `plans/76-editing-together/plan.md`, `inputs.md`, `tasks.md`; `plans/89-heavy-saves-in-seconds/plan.md`, `inputs.md`, `tasks.md` | Record only exact handoff/timing cross-references for CC-17, CC-5c, ET-5, and ET-1+ET-4b together; preserve later scope, checked no-gain history and original IDs. Do not mark donor or receiving tasks complete by this amendment. |

Any separately sizeable confirmed safety fix must be appended as a uniquely identified residual row in the **owning existing** task table, with route, writer, dependencies and negative proof; never hide it as “investigate later” while retaining the affected promise. The source-supported issue list does not establish every historical defect remains present. [ISS-02], [ISS-04], [INV-04] + addendum, [AUD-01].

### 4.17 P52/P53 owner handoff and preserved existing authority

The owner [moved52/53 to R16](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7170081785). Direct canonical reads show product-facing residuals; treating both as nonproduct planning would lose work. Proposed additions in the full brief preserve the original fifteen product outcomes and explicitly expose these adjuncts.

For **`plans/52-issue-intake/plan.md`**, **`inputs.md`**, **`tasks.md`**: append R16 handoff/current custodian confirmation, not a fresh run or reset. Preserve checked II-1–7/R/II-12 with their pending browser/duplicate limitations. II-8 was reopened: Agent half historically landed, App/Runtime/Pinokio patches were unmerged; reconcile actual heads before integrating only residual redirect changes. Do not merge old `r13/plan52-agent`, which deletes Windows notes. II-9 reopened skill patch needs existing owner wording approval and actual installed root-source identity, not duplicate roots. II-10 transfers are owner administration; II-11 both-door/redirect proof and II-13 six-search proof remain uncompleted. The recommended product gate is actual residual redirect/installed-guidance correctness and required prepublication proof; administrative transfer completion and post-live door observation remain explicit closure. Do not create/move issues in this scoping action.

For **`plans/53-vision-aspirations/plan.md`**, **`inputs.md`**, **`tasks.md`**: retain source-present-but-unchecked VA-1–9 and R, owner wording/table/look needs, VA-10/11 and execution follow-ups VA-12/R1.1–4. App#257 is already merged historically; verification against original acceptance, not rebuilding it, is the first work. Current feed/App contract plus remaining correction/owner-look/review are prepublication if changed in R16; VA-11 is explicitly a **post-live observation**, so cannot be a predecessor of publication. Replace obsolete release13 gate with the actual carried handoff/current source. Keep old Release14 Lead records; existing Leads must designate/acknowledge the R16 custodian before new dispatch. Owner input is a real resource, not an assumed calendar date.

For **`releases/16/run.md`**, insert §6's proposed current section immediately after “Scope change —25November2026” and before the historical Now. Preserve all P91 launch/queue/rulings/history verbatim. P91 destination R17 and P82 hold remain; no resumption/retarget/merge is authorized by this report. Existing Lead identity `session_011EzfW1C63rxLXsL6TkHHVV` is historical evidence, to be reconfirmed, not silently replaced by SYN or a new orchestrator.

## 5. Sequencing comparison, actual DAG and writer/resource map

### 5.1 Why a dependency-led hybrid wins

| Option | Useful property | Practical cost / critical path | Decision |
| --- | --- | --- | --- |
| Foundation-first: finish P35/P38/contracts before consumers start | Fewer early interface changes | Delays source discovery, native engine feasibility, corpus capture and independent fixes; broad extraction becomes speculative critical path. A late physical/native failure then invalidates assumptions. | Reject as the default. Retain narrow security/contract review stops before affected landing. |
| One early vertical lane, then expand | Fast discovery of real end-to-end mismatches | Serializes unrelated installers, record/protection, GPU feasibility and media/save work behind whichever path was chosen; encourages a smoke pass to stand in for final coverage. | Use **two independent checkpoints**, not the whole schedule. |
| Pure task parallelism with late integration | Many workers can code | Shared enum/function/manifest writers diverge; proof churn and unrecognized trust/state seams move risk to freeze. | Reject unowned shared writes and late contract discovery. |
| **Recommended hybrid: parallel inventories and bounded tasks; reviewed seam landings; early verticals; one freeze/proof/go** | Maximizes currently useful work while preserving ownership and exact evidence | Real serial paths remain provider→consumer, migration→retirement, accepted inverse→batching, native engine authority→lifecycle proof and final pins→release evidence. | Adopt. Reuse the current implementations; no refactor required merely to add workers. |

The task-table edges in §4 are canonical amendments. The temporary labels below explain the schedule; they are **not new permanent cards or another tracker**. `Start` is the minimum information needed for useful work, `Land` means integration requires a reviewed upstream artifact, and `Proof` means only an exact installed/native tuple can close the claim. Contract review may be satisfied for one consumed interface while unrelated inventory continues.

### 5.2 Immediately useful work packages after normal implementation authorization

| Package / canonical rows | Accountable role | Start without waiting for other whole plans | First landing or acceptance join |
| --- | --- | --- | --- |
| Evidence/comparator: MS-1/2/4, P31 RL-0/1b | Evidence owner + P31 gate owner | Reconcile receipts, job inventory, current source and fixtures; correct comparator design | Accepted inventory/clock schema; exact candidate later for MS-5/qualification |
| Release records/protection: RL-1a/c/d, RL-2b/c | P31 owner | P58/current publishers and effective-control probes; deterministic generation/rehearsal | Approved canonical fields, protection and one generated writer before cutover |
| Native transaction/origins: IU-0/1/13/14/17 | P09 owner | Actual origin inventory, per-volume model, migration lock trace, lived-in fixtures | P38 custody + S35 object/rollback contract for affected transaction changes |
| Native engine/old managers: PIN-0/2; P30 UR-15 | P10 engine owner and P30 Linux owner | Discover actual engine/version/veto; systemd 249/252 adapter and receipt work in distinct functions | Reviewed native custody/worker interfaces; final installed/native proof later |
| Status/local pairing: P29 UR-15 suffixes; P30 UR-16/17/LA | Update decision owner | Current resolver, selected install and local route inputs | Typed producers land before changed App consumer; same resolver writer |
| Provider + closure: P38 P1/P2r and E1 venue discovery | P38 Runtime provider and closure owners | Parallel after T0/W0 framing, actual host-only/native venue preparation | RS1 before new Agent consumer landing; no blanket stop on other lanes |
| State/grant: S35-0/1/4/5 | P35 authority owner | Per-object/phase census and bounded schema; current credentials | Minimal grant/selection seam before privileged consumer apply; bulk migration independent |
| Discovery + managed target: CD-0/2; ER-0/1/2/3 | P93 discovery and P94 platform owners | Existing target observation and physical compute now; compare Windows route; Linux adapter work | CD-1/RS1 for observations; approved route/plan/grant/custody for managed writes |
| Exact plan/donors: WS-2/9/4/17 | P90 owner plus scoped donor/renderer workers | Reconcile Stage1/donors, ref/model helpers, multi-issue renderer and wording drafts | WS-2/RS1→WS-9 producer; WS-4 wiring after registry; WS-3 after reviewed apply contract |
| Save model/corpus/capture: CC-5a/7/13/17 | P63 App model, Agent corpus and Runtime replay owners | Separate functions/files; capture real supported gestures; profile actual heavy cost | Shared outcome/session contracts for consumers; inverse feasibility before CC-5c |
| Media: LM-1/2/3/5 and CC-10 | P79 Runtime template, SDK and App lifetime owners | Existing stream seam, bounded all-path preparation, exact selection and lifetime contract | Reviewed client/provider pin for SDK; migration/guard contract before old persistence removal |
| Render/pack: RN-14, sourceClock/theme, RN-15 residuals | P87 projection/output owner + native custody consumer | Small actual pack/output witness, cause triage, fixture identity and recovery design | Shared projection/schema writer, current custody provider; final heavy/native proof later |
| Experimental paid/credential minimum | Paid lifecycle owner + Runtime/P38/S35 writers | CPU/source failure-path analysis, credential admission, known/unknown allocation contract | Trusted floor/cleanup/lease authority; separately approved capped live proof |
| P52/P53 residual review | Existing custodian acknowledged by Lead | Compare current source to retained acceptance, draft owner wording/look packet | Product residuals to same release, existing owner decisions and contract proof |

These are practical work packages, not a request to launch fourteen sessions or override a live cap. Assign available people to nonconflicting packages; keep an available worker on another ready package while a native/protection decision waits. The existing P91 five-packet cap and two shared Agent-CI-run ceiling are plan/live-authority constraints, not evidence that all R16 coding must wait. While R15 is unpublished, its landing gates retain priority in the shared CI budget. Native proof, heavy quiet measurement and owner review are separate resources from coding capacity.

### 5.3 Dependency edge list to put in task cells

| From → To | Type | Why / scope of the edge |
| --- | --- | --- |
| Current served + integrated predecessor + relevant source inventory → affected implementation baseline | Start | Needed to avoid replaying old work; not a wait for predecessor publication to investigate/design. Branch cut/landing uses Lead's reviewed ancestry. |
| CD-1/RS1 observation + existing Placement contract → CD-2/3 and WS-9/ER consumers | Land | Single precedence, scoped status/reason and responder identity; adapters/fixtures can start earlier. |
| WS-2 → P90 RS1 → WS-9 → WS-3 | Land/review | Actual exact plan/grant/schema and real producer path; helper/renderer/ref work independent. |
| WS-9 producer/registry → WS-4 actual candidate wiring | Land | Synthetic helper results alone cannot prove real unknown-class route. |
| Agreed scope/provenance/revoke semantics → privileged apply; S35-4 producer → TR-1/reusable-derived actions | Land, only for consumed authority | Current applicable approval at mutation/resume is mandatory. Explicit operation/entry grants may use existing reviewed authority; the new reusable-grant backend is not a prerequisite for every local apply. No whole S35 migration gate. |
| P90 accepted plan/grant + ER-1 capacity → ER-4 managed transfer | Land/proof | Exact destination/write/cost admission, no independent downloader policy. |
| Minimum ER-2 install → ER-3 compute → bulk model fetch | Proof, newly managed target only | Existing supported interpreter feasibility starts now; real compute before expensive work. |
| P38 P1 + P2r → RS1 → A1/A2/A3/L1/F1 | Review/land | Agreed process/closure authority. Different functions can be developed in parallel; one lock integrator for A1/A3. |
| P38 R → internal Pub → C1 → C2 → R2 | Land/review/proof | One bounded role ABI in same shipment; public release is not an intermediate dependency. |
| CC-4 semantic vectors → CC-4b/5b wire consumers | Land | One classification/replay contract; model/corpus/preparation starts early. |
| CC-13 real multi-step inverse feasibility + CC-5b contract → CC-5c | Land | Batching cannot erase individual intent/undo/receipt semantics. |
| Per-object migration/custody proof under S35-1/2/3 → CC-5b/10 retirement of that legacy state | Land | Unique pending data must be durably recoverable first; unrelated state migration not required. S35-6 is later integrated candidate/native/rollback proof, not a circular prerequisite for consumer landing. |
| LM-1 provider/template artifact → reviewed Agent client pin → LM-2 shipping | Land/proof | Existing stream method plus backward compatibility, no parallel generated writer. |
| CC-10/LM-5 lifetime contract → P29 guarded update/reload | Land/proof | Prepare/active/imported/parked states all protected before actual application switch. |
| P87 source/schema projection + generated artifact → App/Agent/installer consumers | Land | One projection identity; local work can use reviewed fixtures, not independent regeneration. |
| P10 PIN-2/3 + P38 installed provider → PIN-4/P30 UR-18a | Proof | Actual engine Stop/Quit/Update and child settlement cannot be proved with a simulator. |
| P09 transaction + S35 state + P38 custody + P63 accepted/pending history → lived-in migration/rollback | Proof | Changed-schema, post-update new edits, interruption and recovery all use the integrated pair. |
| P90 implementation/skills → P90 R → retained P56 WS-L | Review/proof | No review↔owner-live-proof cycle; owner SAM witness still needed for accepted closure. |
| RL-1a/2a + settled P29/P30 status → RL-3 → RL-R | Land/review | Visible first-minor identity before qualification/go. Final RL-G is removed as predecessor. |
| All accepted product changes + pre-freeze code/interface reviews → one pin freeze | Integration | Includes bounded P52/P53 product changes; no lane publishes. This does not require RL-R or other final qualification reviews before their evidence exists. |
| Frozen tuple → full support/negative evidence and effective required checks → RL-R/final qualification review → exact owner approval → final RL-G | Proof/review/publication | Classified ledger and one protected Final transition. Final evidence review follows freeze; physical/protection/spend access is not inferred from source. |
| Protected Final and coherent generated sync/deploy → complete served readback/owner live checks | Publication/proof | Not equivalent to GitHub main; post-live observations cannot circularly gate initial publication, but failed readback triggers approved stop/rollback process. |

No edge above permits replaying an unapproved action. “Land” includes any pair/pin review needed to avoid an incompatible intermediate integrated product. Small preparatory PRs may land without activating incomplete behavior; enabling the behavior requires its actual contract and negative acceptance.

### 5.4 Shared writers: reserve functions and artifacts, not broad files

| Shared surface | One accountable writer/integrator | Work that remains parallel / required handoff |
| --- | --- | --- |
| Runtime process/role ABI, framing and provider schemas | P38 provider owner | P2r closure definition and independent pre-import measurers; A1/A2 distinct broker functions. A3 lock hunk joins A1 under one lock integrator. |
| Agent installer `core.py`, `backend.py`, service/update helpers | P09 transaction owner per touched function; P30 owns its platform adapter functions | Native origin/disk fixtures, old-systemd functions and local status work proceed separately. Same transaction/lock function gets one active card, not concurrent rewrites. |
| App update resolver/status and guarded reload | P29/P30 decision owner; CC-10/LM-5 supplies lifetime predicate | P31 labels/record parser in distinct functions, independent UI fixture work; shared resolver/predicate changes sequenced together. |
| `target_schema`, `_workflow_command`, readiness envelope/error wrapper | P90 producer/CLI owner with P93 observation-contract owner | Ref/model helper, candidate grouping, terminal rendering and target discovery in distinct functions; real enum/new case table one writer. |
| VC `import_as_entry`, `before_publish`, revision approval and source refs | P90 import/publication owner | Current full-ref primitives retained; A644/V217 pair gets one reviewed contract. Different ref/diagnostic functions may proceed concurrently. |
| Runtime `store.py` grant/state, capacity/floor, lease mutation functions | P35 grant owner and paid/floor owner on disjoint functions; one integrator for shared transaction hunks | Shared filename is not a conflict. Exact same mutation/transaction function or schema must have one holder and an agreed landing order. |
| Runtime timeline acceptance/outcome/auth and App save-session constructor | P63 contract owner plus one App session writer | Runtime replay corpus, App capture, Agent fixtures, streaming client template and cost profiling proceed in their own functions/files. Shared semantic vector table one writer. |
| SDK `sync.py` outbox and bundle attempt; `commit_session` media sections | P63 attempt-custody owner, P79 media owner on distinct functions | Agree writer/key/replay semantics once; stage edits to common functions, not separate competing queues. |
| App drop/upload hooks, provider import metadata and reload guard | P79 lifetime owner with P63 CC-10 integration | Placement producer and guard work can be separate if functions differ; one import/placement attempt-state definition. |
| Pack component/schema/projection and generated copies | P87 projection owner | Output/phase investigations and fixture/media work parallel; exactly one deterministic regeneration and consumer pin update. |
| `runtime.lock`, Agent dependencies, App manifest, bootstrap/generated sync, release Final | Release pin integrator; P31 owns final record/generated writer | Plan branches record required inputs but do not independently bump shared pins. Product source, proof-only pin and deployed UUID remain separate. |
| Maintained setup/generation skills | Each producer owns its changed subsection; one final reconciliation owner | P56 precedent permits separate subsection work; final fresh-agent route uses actual installed source, not duplicate skill homes. |
| Shared proof selector/case table, baseline ledger and review receipt | Named evidence owner for each table | Different per-card fixtures and native recordings run concurrently when resource policy allows; no concurrent edits to same table or independent reinterpretation of a failing case. |

The [P56 standing rules](https://github.com/banodoco/astrid-dev/blob/cc4520eb67c90024547dd3f012479c1c6a6188eb/releases/15/run.md) explicitly distinguish same-function/same-new-test-table conflicts from different functions in one file, and require dependants to wait only for prerequisite cards. Use that existing rule. The run board should name the current task-branch holder and release the reservation on merge/handback; it need not invent a new scheduler or impose whole-file locks.

### 5.5 Critical path, estimate ranges and escalation

The critical path is conditional on the actual longest retained outcome, not automatically “P35 then P38 then everyone.” In work-unit terms:

`max(P38 native/role closure, P31 protected-publication preparation, P09/P10 native transaction+engine, P90/P94 exact setup+hardware, P63/P79 usable-save+media, P87 exact output/pack) → final join/pins → exact proof/review → owner go/served verification`.

| Estimate source or assumption | Range and how to use it |
| --- | --- |
| Historical P38 plan | 10–13 engineering days (7–9 phase 1, 3–4 phase 2); conditional Windows E1.1 adds 1–2. Re-estimate current residual, do not bill delivered work again. |
| Historical P31 plan | 9.5–18 days, 12.5 point estimate, about 1 for RL-3. P58 reuse helps; effective control/cutover work may dominate. Not a new SYN measured estimate. |
| Historical P30 plan | 7–9 days; old whole-P29 gate removed for independent work. |
| Historical P29 plan | 11–13 days for old scope, much delivered; unsuitable as a residual duration. |
| Historical RN-14 | 12–16 hours; assumes current pack/installer seams work. SourceClock/theme and native residuals are additional, separately sized after cause. |
| P09/P10 and newly bounded save/setup/state residuals | No trustworthy consolidated residual estimate yet. Origin count, engine authority, Windows route, real hardware availability and measured CC-17 cause are concrete unknowns; keep TBD instead of fabricated precision. |
| **New planning assumption: initial decision timebox** | 1–2 working days after authorization for source/contract/origin/engine/hardware/protection discovery, in parallel. Required output: chosen writers, actual outstanding acceptance, route decision, venue availability and revised task sizes. Not a claim all research can be resolved in that time. |
| **New planning assumption: join/rehearsal** | Reserve 1–3 working days after the last required landing for tuple/installer/rollback/publication rehearsal and affected correction, assuming no structural failure. |
| **New planning assumption: final evidence window** | Reserve 2–5 working days of coordinated native/quiet measurement and review capacity after freeze, plus the actual number of accepted repeats. Missing machines, engine authority, cost permission or new harm can extend this without a credible upper bound. |

For the three historical, independently startable P38/P31/P30 estimates alone, a naive serial sum is 26.5–40 engineering days before other work/proof; overlapping their independent work changes that component to the maximum, roughly 10–18, **not** a release completion promise. Shared landing joins and other unknown lanes can dominate. A second core implementer helps only where functions/contracts are disjoint; another simultaneous heavy render can make measurements invalid. Do not invent a delivery date or claim a speedup factor from these ranges.

Escalate concrete facts after the initial timebox: missing native Pinokio veto/settlement API; unavailable representative hardware; unbounded Windows route/role extraction; inaccessible actual origin; insufficient effective release protection; unknown accepted-history/descriptor cause; failure of the retained save gate. Continue unrelated ready work. Escalation must state the retained promise, smallest viable repair/refusal alternative, affected landing/proof and revised effort; owner decisions go in existing inputs/tasks/run board.

## 6. Proposed existing run-board section and integration protocol

Insert the following section in `releases/16/run.md` after the current Scope change heading's paragraph. The word “Proposed” stays until the owner accepts scope and the existing Lead commissions implementation. Preserve all older content below it.

```markdown
## Proposed R16 readiness — pending scope agreement and dispatch

The brief holds strategy; each plan's tasks hold work and progress. This section records current readiness, branch/function reservations, scarce proof slots and source/pin deltas. It does not start a run. Reconfirm the existing Lead and each carried custodian before dispatch; preserve R15 priority, the P91 R17 handoff and held P82 authority.

1. Establish the current served/predecessor/candidate register and actual old origins. Confirm narrow owner decisions: qualification mode, retained P89 gate, Windows route, P38 role scope, grant restore/revoke policy and P52/P53 closure boundary. Independent inventory, fixtures, native feasibility and bounded implementation preparation proceed together once authorized.
2. Fill every ready nonconflicting work package: records/protection; native update/Pinokio/systemd; provider/closure; state/grants; existing and managed environments/exact plan; save model/corpus/capture; streaming media; pack/output/recovery; bounded paid safety; evidence; carried P52/P53 residuals. For each, link canonical task IDs, current branch/function holder, exact predecessor, next landing contract and proof venue. A different function in the same file is not a blanket conflict.
3. Hold only real joins: provider/schema review before dependent consumer landing; exact authorization before privileged apply; verified migration before retirement; individual inverse feasibility before batching; actual native engine authority before lifecycle proof. Start fixtures, adapters and venue discovery before those joins where useful.
4. Record two interim vertical checkpoints independently: existing-environment first creation with decline/consent; substantial import/edit/recovery/undo/reopen/short-render/next-render. Record exact tuples and limits. These are internal integration evidence, not shipment or automatic final acceptance.
5. Converge all retained outcomes, P56 residuals and bounded adjunct product changes through one pin integrator. Rehearse changed-schema lived-in update/rollback, grant/state recovery, native custody and generated publication. Resolve unknown causes; preserve original task history. Name current resource reservations and actual waits, not a new task list.
6. Freeze exact product/Runtime/client/schema/pack/bootstrap/launcher/engine identities after required landings and code/interface reviews. Qualify the retained support/negative matrix, actual served origins, heavy and native journeys; require complete comparable inventories and effective required checks. Then complete RL-R and final qualification reviews on that evidence before the owner's go. Rerun only affected evidence when inputs move, with explicit impact rationale; do not silently carry old passes.
7. Owner approves one exact tuple and ledger. P31 performs one protected Final transition and coherent generated sync/deploy, then verifies complete served bytes and live identity. Plans do not publish separately. Retain named post-live owner observations/administrative closure without pretending they happened before publication.

At every check-in: read all current mailbox messages; reconcile predecessor moves, task receipts, exact writer conflicts and proof availability; start ready work within actual authorized capacity; report blocked contracts/resources with owner and next action. Agent CI remains capped by existing shared authority while R15 is unpublished; R15 gates have priority. P91's historical launch text is not new R16 authorization. No new permanent scheduler, strategy file or tracker is introduced.
```

**Pin/freeze order.** Review and integrate Runtime/provider/schema changes first where consumers require them; produce the one generated client/projection artifact; review exact Agent/VC consumers and dependency pins, then App/installer/manifest consumers with compatibility/readback. Disjoint additive work can land earlier, but incomplete behavior is not enabled by mismatched pins. The pin integrator records source producer, proof-only CI change, lock/schema/pack digest and installed identity separately. After phase-one P38 review and bounded C1/C2, rerun affected native/custody paths before R2/final qualification. Final freeze also contains RL-3 visible version and RN-14 default provision, not post-go follow-ups.

**Proof invalidation.** A changed source with no product effect can carry prior product evidence only with an explicit reviewed impact statement; required status still belongs to the actual head. Any changed ABI/schema/client, transaction/lock, grant/revoke policy, outbox/recovery, projection/media selection, bootstrap/install recipe, launcher/engine/native adapter, test inventory or relevant fixture/measurement boundary invalidates its affected proof. Reconstruct exact candidate installs for those cases, not overlay code and label it stock. Changed tuple or new material ledger invalidates owner approval. No blanket rerun of unrelated heavy campaigns, and no blanket transfer of old proof.

**Predecessor changes.** If R15 publishes or lands another fix, Lead records actual source/served delta, updates work bases by reviewed integration, reclassifies donor overlap and changes the actual-origin/floor comparison. A new floor or schema affects migration/compatibility; a render/pack fix affects projection proof; a proof-only document does not change product identity. Report branch ancestry remains the mandated f872 throughout this scoping submission.

## 7. Exact support, negative and preservation matrix

These are **proposed evidence-row labels**, to attach to existing task acceptance/proof cells, not new permanent task IDs. Every final receipt says PASS, FAIL, UNKNOWN/NOT RUN or explicitly justified NOT APPLICABLE. “Source exists,” aggregate workflow success, inherited red, simulated engine and skipped legs are never PASS for a different route. The matrix is the proposed scope to qualify, not a statement that any new R16 row has been run.

### 7.1 Native install/update/launcher routes

| Row | Required route / support cell | Required final positive witness | Owner |
| --- | --- | --- | --- |
| INST-W | Windows direct PowerShell, Windows 11 Home/nonadmin/Defender, actual scheduled task, supported x64 | Fresh install, chosen settings, owned healthy Runtime, matching editor and minimal creative result; same-release repair; remove program while retaining work | P09/P38 |
| INST-MA | macOS direct shell, actual Apple Silicon | Same lifecycle, native launch/identity and selected realm; real native custody, not Linux emulation | P09/P38 |
| INST-MI | macOS direct shell, actual Intel | Same retained macOS lifecycle; explicit installed architecture/tool facts | P09/P38 |
| INST-L | Linux direct shell, supported native x86_64/user manager | Same lifecycle; exact OS/service versions | P09/P30/P38 |
| INST-LA | Linux arm64 is an explicitly **unresolved admitted-platform cell**: the served manifest contains its Bun/Node/FFmpeg assets | Establish actual installer/runtime support and run the retained direct lifecycle on native hardware, or obtain an explicit truthful support/refusal decision before freeze; asset existence alone is not qualification | P09/P38/Lead |
| UPDATE-DIRECT | Each INST cell, official command and hosted Update now where actually available | **Two consecutive accepted update→forced rollback→update-again passes on the same exact tuple**, actual served origin; true 0.1.0/legacy display; busy/pending data guard | P09/P29/P31 |
| UPDATE-LOCAL | Each retained OS, terminal-owned/autostart-off and fully-local editor | Both halves current/no-op correctness; actual in-page/local update, coherent old/new pair and already-installed offline work; no foreign service takeover | P30/P09 |
| LINUX-OLD | Native systemd 249 and252, plus no user manager/autostart-off | Launch **and** query/settlement, predecessor worker recovery, special-character path, terminal receipt and safe direct fallback | P30 UR-15, P29 UR-R2.5 |
| PIN-W-H / PIN-W-L | Real supported Pinokio engine on Windows, hosted and fully-local respectively | Actual Install/Start/Stop/Quit/Update/recovery/remove controls; exact owned-child settlement, busy barrier, matching editor, coherent App/Runtime recovery | P10/P38/P30 |
| PIN-M-H / PIN-M-L | Real supported Pinokio engine on macOS, hosted/local | Same actual-engine proof, named native architecture/engine version; no descriptor-only substitute | P10/P38 |
| PIN-L-H / PIN-L-L | Real supported Pinokio engine on Linux, hosted/local | Same actual-engine proof and native owner/receipt; integrate old-manager behavior where that route supports it | P10/P30/P38 |
| ORIGIN-N | **Every verified published origin** on each originally supported OS/route, including servedR14 and R15 if published | Lived-in origin data, exact old artifact/pins/schema, direct update and forced rollback; old origin without a button uses its supported official command | P09 IU-15/P31 |
| ORIGIN-R0 | Actual R0/R1 boundary only where documented published/supported | Copy-only migration, retained old install/removal; Windows R0 gap explicitly decided as support or safe refusal preserving data/recovery path | P09 owner |
| SCHEMA-CHANGE | Latest actual served direct and real launcher, each different schema/ownership boundary | Genuine changed-schema migration plus same-schema control, interrupted/retried recovery, accepted history and pending work retained | P09/P35/P38/P63 |
| PAIR-MIX | Hosted/local old-old, new-new, oldApp/newRuntime, newApp/oldRuntime, stale browser/manifest | Correct optional/required/installed-ahead/unknown decision; no impossible downgrade; unsafe writes refuse before mutation; pending edit/import survives guarded switch | P29/P30/P31/P63/P79 |

Exact OS build, architecture, shell/tool, filesystem and service/engine version belong in each receipt. The matrix retains explicit Mac Intel and Apple Silicon from SC-09; Windows ARM64 currently has explicit bootstrap refusal and is not silently promised. Any additional architecture admitted by the final installer must be reconciled before freeze with an actual supported witness or an explicitly approved truthful refusal; the permissive POSIX OS dispatch alone does not establish support. Do not infer a published R2–R8 origin from its number or demand a nonexistent historical Pinokio route. Missing origin artifacts are a concrete P09/P31 gate gap. Reducing genuinely distinct origin/route proof requires an explicit equivalence argument and owner acceptance, not a blanket latest-only shortcut. [SC-09], [SC-10], [SC-30], [SC-38], [INV-01], [AUD-01].

### 7.2 Environments, hardware and exact setup

| Row | Required witness and limit | Owner |
| --- | --- | --- |
| ENV93-DESKTOP-RUN | Actual Windows Desktop reused, selected responder, first/warm output tied to its job and correct editor; unrelated queue survives | CD-2/5 |
| ENV93-DESKTOP-OPEN | Closed Desktop opened by person, re-probed, then correct output; no guessed executable or lifecycle takeover | CD-3/5 |
| ENV93-EXIST-W | Actual supported human-owned Windows Portable/Git installation, selected root/responder and first/warm output; no lifecycle takeover or mutation of preexisting packages/queue; only separately approved D1 additive writes | CD-2/5 |
| ENV93-EXIST-LINUX | Compatible selected Git/Portable/other existing Linux endpoint as actually supported, partial discovery truthful, explicit selection consistent | CD-2/5 |
| ENV93-EXIST-MPS | Actual Apple Silicon selected interpreter, synchronized MPS operator and compatible workflow; classify custom-node/CPU fallback/unsupported limits | CD-5/ER-3, reuse P34 |
| ENV93-PIN-H / ENV93-PIN-L | Existing environment discovery/connection/delivery in the genuine hosted/local Pinokio route, linked to native lifecycle row | P10/P93 |
| ENV94-MANAGED-W | Chosen Windows ER-0 route, clean isolated install, exact built-in transfer, first/warm image, interrupted recovery and last-working preservation | ER-2/3/4/5/ER-L |
| ENV94-MANAGED-L | Existing supported Linux mechanism, equivalent real managed journey | ER-2/3/4/5/ER-L |
| ENV90-REUSE | Saved entry→exact plan→decline→applicable approval→apply→readiness→real result→second run without new flags; immutable source/pin and exact destination | WS-2/9/3/16/TR-1 |
| ENV90-SAM | Named original SAM API JSON and film clip; target/residual results and receipt; separate owner machine/media/paid permission; **after P90 R** | Retained P56 WS-L |
| GPU-WIN-RTX20 / 30 / 40 / 50 | Four distinct physical Windows family cells, actual GPU/model/driver/interpreter/wheel/operator/dtype, synchronized result and relevant memory limit | ER-3/P34 witness |
| GPU-LINUX-RTX20 / 30 / 40 / 50 | Four distinct physical Linux family cells with the same precise facts | ER-3/P34 witness |

The eight physical NVIDIA cells use a **small real compute workload**; they do not each repeat a large model download. Full managed/existing/native journeys above cover lifecycle; reused evidence explicitly names which dimension it proves. Family representation does not claim every VRAM variant or custom kernel. INV-02 corrects the literal Ada `sm_89` demand: compatible8.6 cubin can be valid; prove actual execution, not a string. Current gpu_sanity already computes, so adapt actual backend/dtype/workload rather than build a second checker or demand BF16 universally. Static support precedes consented minimum install; newly managed compute precedes bulk models. Existing supported interpreters can be measured immediately. P94 keeps **two consecutive accepted cold/recovery rounds before publication**, with actual per-volume peak/time, not a guessed40 GB guarantee. [SC-93], [SC-94], [SC-90], [ISS-04], [INV-02], [AUD-01].

### 7.3 Editing, media, render and comparative evidence

| Row | Required positive/negative acceptance | Owner |
| --- | --- | --- |
| SAVE-OUTCOME | Actual App/SDK/CLI/MCP/bundle/restore routes: success receipt, moved, definitive refused, unavailable/unknown; lost/malformed ACK same attempt, changed body new attempt only after known nonacceptance | CC-4/4b/5b, P04 |
| SAVE-WRITER | Two tabs and two independent same-actor SDK writers, fenced handoff, late callback/restart/foreign pending data, same-address conflict versus disjoint allowed work; original7SDK/8hosted cases/cooperative limit mapped | CC-5a/b/13, CE-FINAL→R0 |
| SAVE-BURST | Model 1–20 edits/s×30 s with 0–10 s send, real 5/3s and 10/5s bursts, bounded flight/batch, final authoritative document and each inverse, failure parks the failed edit and its dependent suffix | CC-5a/c/13, CC-17 |
| SAVE-LOCAL | Real-browser original 50 ms locally “kept” boundary, all outbox consumers and no full document per edit; Saved only after authoritative receipt | CC-5b |
| SAVE-300 | Original four comparable warm cases and burst semantics, median≤2 s / no >4 s, frozen installed arms and original end-to-Saved clock; integrity/correctness gates independent | CC-17/P85/P89 handoff |
| SAVE-HEAVY | Standard616 and history-bearing representative project save/reload, useful Undo/redo/restart; exact records/content/history identity; known corruption refuses while healthy large history is not mislabeled corrupt | CC-13/14/17/P85 |
| IMPORT-STREAM | Image/audio/video over64 MiB, representative>1 GiB within configured cap; source unchanged, correct metadata;300 MiB import absolute peakRSS<256 MiB retained, larger witness baseline, absolute and incremental reported separately | LM-1/2/6 |
| IMPORT-CUSTODY | Source changes, cap/low disk, wrong/ambiguous/cross-project handle, batch partial failure, lost ACK, accepted import then failed placement/try-again, reload/update while active or parked; no duplicate catalog attempt or lost authored clip | LM-3/4/5, CC-6/10/13 |
| RENDER-SMALL | Fresh-installed motion pack/defaults, image-only and film 23-like useful short witness, exact source-time/cut/phase/theme/easing, decoded frames/audio/duration and preview agreement | RN-14/P87 |
| RENDER-HEAVY | Final installed standard 616 and assigned large-shots/film-shaped extent; retain inherited two accepted heavy rounds where required, actual frames/audio/content and accepted source/child closure; no pass from clip count alone | RN-10/11/12/R, P85 |
| RENDER-RECOVER | Fail/cancel/lease loss/known process stop→next valid job; unknown owner not force-cleared; exact parent birth/child closure, installed-wheel/revert sensitivity, native Mac custody and long lease where retained; verified output remains retrievable | RN-8/9/15, P38 |
| COMPARE | One matched installed predecessor/candidate CLI comparison plus linked required save/restart/render evidence, identical method/fixtures/load gates, frozen bootstraps/arm manifests, raw receipts and failed attempts retained | MS-3/5, P31 |

P88's 2.6 MB owner-profile parity is explicitly later P75 work; it is not silently restored as a new R16 criterion. That deferral does not erase standard 616/large-shots, history-depth, media/closure and content-versus-occurrence extent obligations. Padding JSON is not a representative workload. Heavy proof should use a quiet named reference host with load/CPU acceptance gates, while native correctness smoke covers each materially different platform mechanism. If the retained original acceptance requires more, preserve it or record an explicit equivalence decision. [SC-63], [SC-04], [SC-79], [SC-87], [SC-85], [INV-03], [INV-05], [INV-07], [AUD-01].

### 7.4 Shared negative cases and publication refusal

| Row | Must observe | Owner |
| --- | --- | --- |
| NEG-TARGET | Stale/wrong responder at same URL, denied/timeout/ambiguous/partial scan, explicit/default/env precedence; no false ready, guessed interpreter, unapproved target mutation or human queue disruption | CD-1/2/3, WS-9 |
| NEG-PLAN | Decline/dry-run/no-machine, changed workflow/root/interpreter/source/ref/recipe/destination; no target clone/execute/publish before applicable approval; install.py never runs; name-only candidate stays human choice | WS-2/3/4/9 |
| NEG-TRUST | Revoked reusable grant, independently explicit entry provenance, stale cache/copy/backup/old client; no resurrected derived authority; reapproval when current authority unknown | TR-1/S35-4 |
| NEG-ENV | Unsupported wheel/operator, enumerated-but-unusable device, insufficient workflow memory, foreign/ambiguous root, low capacity/space lost midway, stalled/incorrect-hash transfer, partial install/resume/repeat | ER-2/3/4, WS-16 |
| NEG-ENTRY | Collision/replace/schema error before publication, changed source witness #1531, copied stale approval; no output on no-write path, one new approval when plan actually changes, previous working version retained | WS-9/3/UP-1 |
| NEG-CUSTODY | Busy/unknown/foreign owner, inherited channel and original peer, PID/parent birth reuse, missing/altered/symlinked closure, ambiguous old journal, stop observation loss | P38/P10/P09 |
| NEG-TRANSACTION | Kill at actual staging/stopping/backup/migration/switch/verify checkpoints; locked files/ACL/long path; corrupted backup/receipt; exact repeated recovery; paired editor rename/bootstrap fault | IU-1/13, PIN-1/4 |
| NEG-STATE | Two writers/conflict/oversize/stale actor/old client, interrupted migration or local metadata write failure; no pending intent/default/tombstone/accepted-history loss | S35-1/2/3/6, CC-5b/10 |
| NEG-ROLLBACK | New accepted edits/imports after successful update, changed schema/grants, replayed old recovery token; never overwrite newer work; safe refusal with preserved copy/recovery when old product cannot read it | P09/P35/P63 |
| NEG-PAID | Known no-create versus unknown allocation, duplicate retry, nonACK/skew/host death, cleanup at/below reserve and under locks, stale credentials; no duplicate spend and bounded settlement | ER-P1/Runtime/P38/credential owner |
| NEG-WIN-GUARD | Real allowed/forbidden asynchronous requests with synchronous controls; #682 stays unknown until observed; no blanket allow or unverified security claim | Existing security owner/P38 |
| NEG-VALIDATION | Rule exception/incomplete check, actual immutable-history corruption, unsupported shape/selection, unauthorized inverse and unknown item; never “same exception as base, therefore safe” | CC-3/6/13/16 |
| PUB-DRAFT | Draft, strategy-only edit, missing/malformed Final, bad kind/version/floor, invalid/incomplete pins/digests/bootstraps, unqualified tuple | P31 rejects before public writer/deploy |
| PUB-AUTH | Wrong actor, stale/wrong head, missing/failed required check, unclassified ledger, approval before candidate change, competing transition/replayed approval | RL-1c/G effective control rejects; legitimate retry is idempotent |
| PUB-CUTOVER | Old writer still active, mixed generated manifest/bootstrap, source/sync/deployment identity confusion, App auto-deploy before coherent tuple | One authority, held deploy or proved safe interval, complete served-byte readback; no dual publishing |

Exercise each fault at every **materially distinct transaction/ownership/native mechanism**, rather than every arbitrary Cartesian permutation. Keep positive native route coverage and actual historical origins. If two cases share one mechanism, record the equivalence and retained native control; do not just delete a matrix row. Experimental status never exempts spend/consent/cleanup safety. Local zero-cost ER-L can complete without provider keys or paid permission; retained paid-route final acceptance separately needs its authorized evidence or an explicit owner support decision.

### 7.5 Migration and rollback contract by object

| Object / phase | Authority and minimum transition | Rollback / negative obligation |
| --- | --- | --- |
| Accepted projects, history, publications and media | Existing Runtime/project authority; validate source identity/integrity, migrate under exclusive operation/lifetime lock; receipt before switch | Old reader compatibility or explicit safe refusal/copy after newer writes; no overwrite of accepted post-update work; corrupted source control fails |
| App/SDK pending drafts, attempts, inverse and import placement | Existing owner-fenced outbox/operation metadata, scoped actor+writer+realm/project/timeline | Copy/receipt/verify before retiring legacy; lostACK remains unknown; storage failure visible; don't deduplicate similar documents or delete parked work |
| User/project choices, hidden personal defaults, pack opt-outs | Versioned P35 scope; retain explicit choice, URL intent not global preference; current P32 document reused | Restore/fresh profile/old client preserve selection; deleted default stays deleted; optional unknown pack quarantined without deleting user source |
| Reusable and entry trust | S35-4 authoritative grant/provenance/revoke; P90 checks current scope at apply/resume | Old backup/copy cannot revive derived authority; independently explicit entry grant only by established provenance; no retrospective uninstall/kill |
| Secrets and credential references | Current protected host/secret owner; resolve at admission, no generic app-state copy | Rotation/concurrent update/Windows ACL; stale env cannot override current secret; recovery references remain redacted |
| Bootstrap receipts, program roots, models, caches and foreign environments | P09/installer ownership receipts and selected-root policy; managed last-working stage, no foreign deletion | Repair/remove only proven program-owned artifacts by default; per-volume peak/reserve; locked or ambiguous files cause safe refusal, retained original data |
| Acquisition journal, lease, activation, native process handles | Distinct pre-activation local and Runtime phases; P38 authenticated transfer and exact incarnation | Crash/retry cannot lose unknown allocation or adopt a reused PID; terminal observation not EOF; paid cleanup reserve and independent cap remain reachable |
| Local editor + Runtime version pair | PIN-1/IU-1 durable transaction record before editor rename, then bootstrap/verify/switch | Crash on either side restores coherent old/new pair; mixed stale UI safely refuses and preserves pending work |
| Render scratch/output and immutable inputs | Exact admitted source/selection/parent/child closure; bounded content snapshot, owned scratch only | Parent birth rechecked; failed cleanup does not delete verified retrievable output; copy overhead reserved; no next render until known safe settlement |

**Receipt content:** reuse existing journey candidate config, process/operation identities, committed raw logs and measurement records. Include old/candidate source full SHAs, installed pair and tool/lock/schema/pack digests, actual manifest/bootstrap hashes, publication/deployment identity, OS/architecture/engine/hardware, target/selected roots sanitized, operation checkpoint/outcome, exact logical revision/selection/history identifiers, before/after data/write-set checks, clock/load/CPU/RSS/peak-space facts, negative trigger/recovery and evidence limitations. Never attach credentials or private creator media; use reproducible nonprivate lived-in fixtures. Source inspection and tests proposed here are not executed proof.

## 8. Significant issue ledger and adjacent-plan disposition

This ledger consolidates ownership, not issue history. **Every `dev#N` means `banodoco/astrid-dev#N`; `app#N`, `agent#N` and `pinokio#N` identify those product repositories.** Grouped numbers inherit the written repository prefix. Exact original issue links, historical open/closed/reopened states and search coverage remain in [ISS-01], [ISS-02], [ISS-03], [ISS-04], [HOR-01] and [AUD-01] §8; those full originals were read. No issue is created, closed, relabeled, transferred or declared currently reproduced by this synthesis. `Required` means retained-path acceptance/repair if needed; `Verify` means current cause/reachability remains open; `Later` means no broader feature programme enters R16.

### 8.1 Root causes with one receiving owner

| Repo-qualified significant issues | Disposition and exact receiving seam |
| --- | --- |
| dev#579/#584/#679/#1230/#1047; agent#104 | Required/verify native install/update/locked-root/realm preservation, P09 IU-2/3/4/13/15 with P38. Source-present historical fix such as command-length repair is a regression witness, not a duplicate implementation. |
| dev#1729/#723/#1413/#683/#935/#758/#1387 | Required disk/partial-cache and truthful supported-path errors under IU/P29; copy/harness-only cleanup later unless needed for safe diagnosis. Actual volumes/owners/capacity, no false success or secret disclosure. |
| dev#818/#825/#1611/#815/#1206/#739 | P29/P30 selected installation, capability/direction/mixed-pair and P38 ownership; P31 version/protection. No downgrade when installed ahead, no guessed service manager or wrong realm. |
| dev#1525/#1805/#1578/#1938 | P09 default/tombstone/atomic swap preservation and P87 RN-14 one projection; user-created concurrent files survive rollback. |
| pinokio#11; dev#1920 | P10 real native controls and pair recovery with P38/P30; missing-file/no-op/collision causes verified individually, simulator not acceptance. |
| dev#651/#652/#653/#581/#678/#681/#1848/#1952/#725/#816/#733/#1380 | P93/P94 actual selected environment/first result, P34 witness reuse. #1848 external transfer with skipped built-in route and mismatched editor is not complete first creation. Idle/cache optimization later unless readiness fails. |
| dev#721/#722/#823/#1213/#760 | P90/P94 existing TLS/transfer/receipt mechanism; preserve reopened#721 and partial#722 repair, verify peak/resume/hash before publish. #760 actual installed browser/render dependency via P87/P09. No TLS verification bypass. |
| dev#1861/#1910/#1928/#576/#767/#1531 | P90 WS-2/3/9/16/TR-1 with VC/P93/P35: exact source, target, consent, registry, live schema and authenticated witness. #1910 fail-closed may be safe until recovery required; #1531 stale parsed-bytes/witness identity has bounded fix/proof, not full cache work. |
| dev#682 | P38/existing security owner native Windows positive/negative proof. Hypothesis remains unverified; no invented exploit or broad P15 move. |
| dev#1728/#1254/#631 | S35-4/current credential owner + ER-P1 paid admission: resolve current secret by reference, missing/revoked/stale refuses, no fallback charge or log leak. Zero-cost local ER-L independent. |
| dev#1648/#642/#641/#775/#811/#1450/#616/#1446/#1514/#628/#619/#617/#627/#618 | Required retained experimental paid safety, ER-P1 owner with Runtime/P38: low-disk cleanup, claim/settlement locks, unknown create, expiry/skew/nonACK, queue/cancel versus stop and host-death cap. Distinct causes keep separate witnesses. |
| dev#587/#582/#589/#782/#580 | Verify paid-capacity/diagnostic effects under ER-P1 only if needed for truthful safe recovery/cost; broader lifecycle features stay P40/P50. |
| dev#1402/#1369/#1480/#1690/#1657 | P63 CC-4b/5b/13/14 with P04. Restore CAS and immutable-history guards already exist; retain regression proof. #1657 distinguishes Undo availability from actual inverse submission with exact accepted basis/key/actor/publication and seven honest recovery fixtures. |
| dev#1292/#720/#1246/#1793/#1932/#1561/#1908/#1939 | P63 CC-17/CC-5c with P38/P85: bounded command-cap/lock, healthy restart/history and useful Undo/save. #1939 handoff is not approval for all P75; retain original2 s / 4 s gate and distinct workloads. |
| app#252/#255; dev#1235/#1237/#1222/#1236/#1404/#1412/#1726/#769/#1247 | P79 LM-1–6 + CC-6/10/13; stream/cap/duration/selection/drop and active/parked lifetime. #1247 local FFmpeg protocol/root guard with P38: permit actual safe local file/pipe use, refuse wrong/network root as required; no blanket media de-support. |
| dev#1296/#1312/#1507 | Verify current supported writer/normalization under P63/P79/P87. Historic raw-SDK-only or unknown starter-track routes do not authorize broad provenance migration or new transition features; repair only actual supported mismatch. |
| dev#1931/#1909/#1739/#1500/#771/#851/#861 | P87 phase/theme/easing/source/range/output correctness with P63 canonical writes; trace #861 accepted transcript/visualization/word agreement if that route is supported, not new feature expansion. Each historic symptom needs current route evidence. |
| dev#1916/#1938/#1503/#1818/#1846/#1915 | P87 exact pack/input/output/native custody. #1916 repaired builder is integrated source, heavy proof still distinct. #1503 changed-library readiness is a lead until traced; parent reuse/coarse timestamps/copy/lease/Mac budget have separate bounded witnesses. |
| dev#1474/#1475/#1502/#1514/#1476/#1501/#1477/#1504/#1515 | P87/P38 required actual cancel/settlement/recovery/next-job/output-retention; #1515 general resumable render scheduling later unless a demonstrated core recovery prerequisite. |
| dev#1760/#1267/#1855/#866/#1384 | #1760 broad worker-versus-host isolation later; current caller-versus-host admitted-root/snapshot boundary still required. #1267 installed HyperFrames/CPU render proof if supported; 404 cause unknown. #1855/#866 exact receipt/admission witness, broader P82/P92 later. #1384 full H3 only if a retained promise actually requires it, no automatic P13 expansion. |
| dev#1768/#680/#739/#1920/#1941/#1929 | P31/P85 exact inventory/collection/attempt and proof authority. #1768 no unit collection is NO-RESULT; #1929 coordination policy, not product defect. Broad flakes/green programme P91/R17; minimal required witness repair stays R16. |
| **dev#2002** | Newer source: 15 unknown descriptor cases→CC-6/13/14 + P87 projection; one unknown occurrence retry/restart/inverse case →CC-13/14 + CE-FINAL.19 timeout-keyword fake-transport cases: make the narrow fixture repair in R16 where needed for retained conformance, otherwise broader cleanup remains R17. Do not call the two unknown groups harmless because they are inherited. |
| **R15 qualifier's3s dimmer-film-frame observation**, no distinct issue ID established here | Separate P87 output/projection cause row beside#1909/#1931. Preserve accepted document/frame/time/settings and intended output; no invented issue number or assumed common cause. |
| dev#1495/#1496/#1497/#1538/#1564/#1566/#1567/#1584/#1588/#1599/#1870/#1873/#1874/#1875/#1876/#1877 | Horizon/authoring/pack-registry leads. Only supported admitted-source/output/security defects join P87/P90; broader P18/P76/P92/element-authoring work later. Titles alone do not prove current bugs or closure. |
| dev#727/#754/#800/#885/#890/#1899/#1513/#1618/#1621/#1608/#1594 | Note/later factories, privacy diagnostics, H3/voice/new-product/cache/harness/watchdog/process work. Actual privacy loss or unsafe retained lifecycle is escalated to P35/P38/P31; no broad scope from keywords. |

This covers the audit's consolidated significant root causes plus the new qualifier delta; every original remains authoritative for its finer issue provenance. “Same symptom” never merges away a separate cause. Source inspection, report attribution and newly recorded current unknowns have deliberately different force.

Additional explicit case mapping retained from the complete originals: dev#1401 anchored/shot/reflow goes to CC-13/14/16 (an earlier unanchored witness is not equivalence); dev#1002 legacy shared-media unplace/restart/inverse to CC-13/CE-FINAL; dev#1347/#966 post-ACK cleanup/early false-Saved to CC-5a/b, preserving old proof; dev#1521 healthy-history admission to CC-17/P38/P09; dev#1253 installed browser launch context to P87/P09/P94. Dev#720/#1246's legitimate command/Three.js payload boundary is distinct from media capacity: bounded references or explicit support decision, not simply a larger global cap. Dev#771/#851 retain the existing P59/P63 source-offset contract while P87 verifies export/filmstrip/audio agreement. No broad change to those adjacent plans is implied.

For environment/paid cases, preserve these noninterchangeable outcomes: dev#1450 known-zero `capacity_retry_ready` may safely continue after reconciliation, while dev#616 unknown creation cannot blindly retry; dev#641 delayed/nonACK cancellation may remain only under the owner's conditional acceptance **with independently proved paid expiry bounding exposure**, otherwise repair/restrict that route. Dev#1213 must allow only the expected resumable partial, rejecting unrelated residue, rather than asserting no resume file at all. Dev#733/#1380 slow object_info retains cause; dev#581 no selected project offers the existing create/select action; dev#816 distinguishes Runtime health from render/generation capability; dev#1611 binds selected realm through actual admission rather than re-reading a changed choice. These clauses belong in the receiving task acceptance specified above, not another workstream.

### 8.2 Every selected/adjacent programme has an explicit home

The fifteen selected plans09/10/29/30/31/38/93/94/90/35/63/04/79/87/85 remain, with exact amendments in §4. P56 residuals are fully absorbed into P90 with WS-L retained. P52/P53 are explicit owner-directed adjuncts, not inferred new feature work.

| Adjacent canonical home | R16 disposition / later boundary |
| --- | --- |
| `plans/12-multiple-inference-routes/` | Do not require complete engine-protocol programme. P32 F4/P90 consume only a proven needed current interface. |
| `plans/13-execution-host-refactor/`, `plans/83-execution-host-in-modules/` | R17 architecture remains later; no umbrella refactor to permit parallelism. Required current custody/admitted-root correctness stays P38/P87. |
| `plans/15-openshell-safe-execution/` | Only retained native boundary proof/confirmed minimal#682 seam; full security architecture not imported. |
| `plans/16-streamlined-agent-experience/`, `plans/20-zero-to-first-image/` | Reuse current setup/choice/first-result journey and maintained skills. No new onboarding framework or redispatch of delivered primitives. |
| `plans/18-timeline-editing/`, `plans/19-first-principles-documentation/` | New vocabulary/authoring/documentation programme later; R16 fixes supported kinds and accurate installed guidance only. No superseded release milestone restored. |
| `plans/27-video-render-options/` | New export controls later; current output/range correctness remains P87. |
| `plans/32-generation-placement-targets/`, `plans/34-real-gpu-proof/` | Reuse selected Placement/T6d and real hardware method; bounded F4/P90 convergence and P93/P94 witnesses, not whole-plan gating. |
| `plans/36-one-credential-path/`, `plans/40-machine-lifetime-controls/`, `plans/50-recorded-boundaries/` | Narrow current credential/paid safety through S35-4/ER-P1/P38; full consolidation/lifecycle/boundary programmes remain separate. |
| `plans/37-generate-time-destination/` | New generation destination choices later; existing explicit/default selection must be truthful now. |
| `plans/58-strategy-from-releases/` | Completed shared record/generator reused by P31; no duplicate roadmap, generated region edit or reopening from scratch. |
| `plans/73-markdown-first-agent-skills/` | Reuse verified current source/layout and installed consumer; source cutover is not proof of local installation. |
| `plans/75-fast-saving/` | R18 broad speed programme, generic effect applier, larger history-format/payload work and explicitly deferred 2.6 MB parity. CC-17 owns only bounded retained P89 necessity. |
| `plans/76-editing-together/` | New ET-1 defaults + mandatory ET-4b stay together; ET-5 minimum exact attempt moves to CC-4b. Full collaboration UX/reattachment later. |
| `plans/77-saving-holds-on-a-heavy-timeline/`, `plans/78-live-custom-element-editing/`, `plans/88-timeline-edits-land/` | Preserve landed fixes/fixtures and unresolved acceptance limits. Reuse actual artifacts/cases once in final integrated save/media/render proof, do not rebuild whole plans. |
| `plans/80-use-media-in-place/` | Later live/source media programme; R16 still imports/copies preserving original and exact identity. |
| `plans/81-once-per-command/` | Existing runner/attestation constraints reused; only #1531 authenticated source/witness boundary if needed. No full optimization prerequisite. |
| `plans/82-reuse-across-commands/` | Stage1 evidence retained; RA-0b/RA-2 and remaining speed work held under existing Lead. No resume/retarget here. Existing Lead/orchestrator hands off actual branches/proof to later P92/R18 scoping. |
| `plans/86-the-timeline-feels-fast/`, `plans/92-generate-within-a-second/` | R18 broad playback/generation speed and cache programme; no silent3s/300 ms gate in P85. |
| `plans/89-heavy-saves-in-seconds/` | Completed fixes/no-gain history retained; explicit2 s / 4 s residual and usable Undo/reopen owned by CC-17/CC-5c/P85. No pending blanket P89 packet inferred. |
| `plans/91-agent-main-green/` | R17 destination; retained branch/evidence/ceiling/mailbox untouched. Existing Lead/orchestrator must reconcile in-flight work and rebind before any destination-dependent landing. No P91 landing to R16. |
| `plans/95-composable-agentic-workspaces/` | Dev infrastructure/parallel-workstream context, not a prerequisite for R16 product implementation or a reason to create a new scheduler. |

No future release semantic version is assigned. A minimal cross-boundary prerequisite must name its evidence, receiving task, inseparable safety conditions and owner decision; a plan label on an issue is not authority to move the whole plan.

## 9. Refreshed identities, primary-source adjudication and limits

### 9.1 Proposal, implementation, publication and transitive identities

The reviewed proposal/report parent remains **`f8721766ba2fcb7762ca42767749409d00aa2dbc`**, even though planning main and product evidence moved. The brief blob is `cdcc1c18db4f53bcadb15219436dfd21ec25a882`; run board blob `2bedb3da1eb6d3b91539a24c68e6c65eed0622c3`; release template blob `0fcda37d63a01dae9568c55bbdeff782e834a2a9`. The [template](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/TEMPLATE.md) keeps Final publication inside the same brief, not a second authoritative JSON file. Roadmap#1956's actual merged history is context; it does not replace this assigned report base.

Read-only ref refresh around 19:31–32 and again 19:50UTC found:

| Repository / identity | Integrated R15 candidate or pin | Public main / other distinct identity |
| --- | --- | --- |
| astrid-agent | `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5` | `c0ad6b54aadd21630d98bb5039613e37efe92a8f` |
| astrid-runtime | `686ca695469bda48cd40a70824c4ccef2a137284` | `5120462d67479dc4719406d0d34440edb616ace1` |
| astrid-app | `cc1d48f016fde55ad6b0609c619d8a4bcec56823` | `e0da794ac9d26a808ab4082b29f60408b66b3a4c` |
| VibeComfy | `55c3948212d23cf037fae8a4c6faad77d33e7279` | `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`; **served pin differs**, below |
| astrid-dev planning main | `cc4520eb67c90024547dd3f012479c1c6a6188eb` | Not the reviewed proposal/report base |
| astrid-pinokio launcher main | `1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb` | Actual deployed engine/version still needs separate qualification |
| runpod-lifecycle consumed pin | `9f88ef7640bc664f697112d966ecefa123d44340` | main `f2948817eeb94af8dee76be21f6d673724f1606e`, independently rechecked near 20:23 UTC, not interchangeable |
| motion pack source | `2379ab54aca522019ff4f869cfdf9375bdb56dfc` | Pinned digest `75234c10217e67ec0f111a4cb6be4a6252e172a9cd382506498d07ce1d241029`; editor projection begins `414a6fd1`, distinct identity requiring reconciliation |

R15 candidate manifest has release 15/required 15 and schema digest `2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2`. Its exact manifest SHA256 in the two independently inspected Linux update receipts is `3ccc767c11fa0d08551bce7e73f88e72877a9657fb8dec08dc20ac3a4739e4bb`. Both Agent and App runtime.lock.json source_commit equal `686ca695469bda48cd40a70824c4ccef2a137284`; producer_version is the distinct digest `sha256:69cdb4b75760f238114ec5032f4794e3d33bf5f8a090d41ade8b5b207593aed1`, not another product commit. The proposed later P38 proof-only tests/astrid-agent.pin commit is a separate identity; do not confuse it with these current lock fields. [Agent lock](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/runtime.lock.json); [App lock](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/runtime.lock.json).

### 9.2 Actual served bytes, independent read

Normal-TLS HTTPS GETs with `Cache-Control: no-cache` at **2026-11-25T19:50:27Z**, repeated from the earlier 19:32 snapshot, returned unchanged bytes:

| Actual URL | Bytes | SHA256 |
| --- | --- | --- |
| [install-manifest.json](https://astrid.haus/install-manifest.json) | 5155 | `8556f2183dfc5575508827ec449c23ea5bbc61792d8e85cfad309dff9d44dee7` |
| [install](https://astrid.haus/install) | 6302 | `c268a5fae7ff318414745cee7bfcec13b6d7a81434f7aaa10d218ffe28248fff` |
| [install.sh](https://astrid.haus/install.sh) | 162 | `591c4c51b148fccef2a7d1c45782d9ff949d5fd03d46cd82b5591e3a23d1b285` |
| [install.ps1](https://astrid.haus/install.ps1) | 18682 | `ea581d5d7c2d02f9f062dc15affabe1f7c3e38d641984cecf4797f13ac58b3a9` |
| [build.json](https://astrid.haus/build.json) | 60 | `9f5549ffac417d6b71557979ff82f342f7a447499f9f2253d6ae1612f5abe981` |

Served manifest **release 14/required 14**, Agent `c0ad6b54aadd21630d98bb5039613e37efe92a8f`, Runtime `5120462d67479dc4719406d0d34440edb616ace1`, schema `9c9e746eb5138f5e92baf5bcd87e8598c6aa92597c92083956b24517c4071923`, VC `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c`, lifecycle `9f88ef7640bc664f697112d966ecefa123d44340`, **no packs field**. Build bytes read `{"app":"7dedb819-d5b9-42a3-a9b3-b759373a6155","release":14}`; that UUID is not an App source commit. These are time-bounded network observations, not permanent assertions that R15 cannot subsequently publish. They establish the actual migration/regression baseline at this cut and why main/candidate/served cannot be conflated. Only the report path may be submitted, so hashes/fields/time are embedded here rather than adding raw-download files to the PR. A final author-run normal-TLS no-cache read at **20:22:22UTC** (manifest) and **20:22:25UTC** (build) returned the same byte lengths, SHA256 values and release14/floor14/deployment identity. The three bootstrap byte observations remain separately timestamped19:50:27UTC; no later refresh of those three is claimed.

### 9.3 R15 delta: qualification progressed, publication remained separate

The root read the full [19:45 qualifier verdict7172606069](https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7172606069), [lead-thread summary7172609349](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7172609349), [evidence-PR request7172689586](https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7172689586) and [Direct Journey status7172802576](https://github.com/banodoco/astrid-dev/issues/1834#issuecomment-7172802576). This supersedes earlier “qualifier pending” observations in original reports. Evidence PR#2004 is reported; this synthesis did not run it, merge it or independently reperform the entire corpus.

- **Reported verdict:** Tier1 met, no harm-class finding on paths run, fit subject to owner acceptance of the ledger. The earlier [Lead conditional go7170081785](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7170081785) accepted known nonharm items and conditioned publishing on the verdict; the newer ledger contains unexplained cases and again asks for owner acceptance. This report does not decide that new unknown causes are covered by the earlier acceptance.
- **Reported new proof:**616-clip save/reload twice, Saved 30.3s/32.0s with identical616records/content digest;616-clip whole render18m45,233s/6990frames/audio;621-clip film-shaped render16m11,195.967s/5879frames/audio at declared1280×720. These are useful scoped R15 evidence, not the original300clip2 s / 4 s gate or all large-shots proof. Its “P89 target 3 s” wording does not overwrite the canonical handoff.
- **Independently inspected narrow run evidence:** Linux user-service `update_rollback_only` runs [45669028971](https://github.com/banodoco/astrid-agent/actions/runs/45669028971) / [45669037506](https://github.com/banodoco/astrid-agent/actions/runs/45669037506), jobs139399026710/139399064746, attempt1, exact candidate/manifest bindings and “receipts pass,0problems.” Other legs skipped. This proves those selected update/rollback legs, not the whole matrix or native Pinokio.
- **Important limits:** installed App reported `7676df48f4104fb8ebe2b19de64dea25b9ec3dc7`, while final candidate is `cc1d48f0…`; the reported difference is required-floor-only. Preserve that explicit carryover rationale rather than call it an identical stock final App. Motion pack installed manually; RN-14 remains. Windows tester and Pinokio rows unrun; full journey matrix not run; large-shots success not established. GPU generation relies on owner-accepted witness, not the qualifier's own run. Heavy render summed process RSS ≥7.9 GB is a lower bound, not a universal memory requirement.
- **New unresolved evidence:** [#2002](https://github.com/banodoco/astrid-dev/issues/2002) full body directly read: 19 timeout-keyword test-double mismatches, 15 compiled-element-descriptor failures and one opaque occurrence retry/restart/inverse precondition failure; causes of the latter 16 unestablished. Inherited and candidate-equal does not establish harmlessness. Film frame at 3 s is dimmer than preview, cause unknown; separate from known theme background/phase findings until traced. #1932 Undo ineffective at 300–616 remains a real usability observation, even without demonstrated data loss.
- **Aggregate-only update:** Direct Journey [45686782170](https://github.com/banodoco/astrid-app/actions/runs/45686782170) reported success 19:48, explicitly not job-by-job inspected by that commenter. Do not widen its evidence to native/manual coverage.

At the root's **20:14UTC mailbox refresh**, #1836 still ended at7172609349 and #1963 at the coordinator ACK7172729103; no newer publication-completion or changed synthesis authority was observed. The raw served observation is19:50:27, separately timestamped. Before actual R16 branch cut/freeze, repeat the source/served/handoff delta procedure in §6. No live R15 task or owner's go is modified here.

### 9.4 Primary checks that adjudicate disputed/high-harm claims

These are source observations, not reproduced incidents. Exact source links below were read directly by the author or supporting read-only cross-check; the author read every mandatory original independently. An inference names its narrower path and does not claim global coverage.

| Primary source | Observed fact / resulting judgment |
| --- | --- |
| [P56 inputs at current planning source](https://github.com/banodoco/astrid-dev/blob/cc4520eb67c90024547dd3f012479c1c6a6188eb/plans/56-workflow-setup/inputs.md) D1–D12 | Terminal consent is an accepted speed bump an agent can type; additive protection/install.py/transitive policy is explicit. Reject a new human-authentication prerequisite. |
| [baseline-diff.py](https://github.com/banodoco/astrid-dev/blob/cc4520eb67c90024547dd3f012479c1c6a6188eb/env/baseline-diff.py)155–240 | Missing inventory uses passed-somewhere minus candidate keys, so an always-failed case can disappear undetected; flat IDs can mask platform differences. Bounded comparator/complete-collection correction is required for the proposed gate; preserve whole-family shard aggregation. |
| [SDK timeline sync](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/sdk/timeline/sync.py)452–492 and1080–1146 | Default scope omits independent writer; exact bytes/key/fence retention and new key after changed conflict basis already exist. Fix writer/caller custody, do not discard those protections or conflate unknown with nonacceptance. |
| [Runtime commit store](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/timeline_commit_store.py)868–878,2260–2315 | Same key with changed request hash is rejected; reviewed CAS is checked under authority. Preserve; universal “same logical operation, same key after body changes” is wrong. |
| [App data provider](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/src/integrations/runtime/dataProvider.ts)244–273,1416–1470,1753–1770 | Restore already sends reviewed pair; fresh UUID per invocation leaves attempt-custody tracing. Import operation generation/persistence exists, with swallowed persistence failure. Retain/migrate metadata; source presence alone is not durable acceptance. |
| [Agent asset planner](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/core/generation/asset_gaps.py)410–485 | Planning can hardlink/probe, so target no-write promise needs exact separation; stable desired present+missing model representation is useful existing work to keep. |
| [VC remote setup](https://github.com/banodoco/VibeComfy/blob/55c3948212d23cf037fae8a4c6faad77d33e7279/vibecomfy/commands/runpod_setup.py)315–375 | Live clone/check=False fetch/force-checkout/pip consumer remains. Approving a local planner does not repair this distinct mutation path; WS-3 owns the bounded correction. |
| [VC entries](https://github.com/banodoco/VibeComfy/blob/55c3948212d23cf037fae8a4c6faad77d33e7279/vibecomfy/entries.py)123–253; [custom_node_refs](https://github.com/banodoco/VibeComfy/blob/55c3948212d23cf037fae8a4c6faad77d33e7279/vibecomfy/custom_node_refs.py)21–142 | Full immutable refs, retained declarations, before_publish and atomic publication already exist. Old donors are not wholesale missing; old sidecar retention must not replace current F5. Current Agent lacks donor frozen TargetSchemaResult/actual add-model surface. |
| [Runtime store](https://github.com/banodoco/astrid-runtime/blob/686ca695469bda48cd40a70824c4ccef2a137284/runtime_protocol/store.py)4504–4519,4550–4583 | Floor includes zero estimates and recovery; a client saying zero is not a safe cleanup exemption. Use trusted bounded cleanup authority/reserve, distinguish ordinary mutation and settlement. |
| [App POSIX bootstrap](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install)1–92 | mkdir/log/uv/Python preparation occurs before manifest pin mismatch check; zero program/realm/service mutation and literally zero filesystem writes are different promises. Windows also creates directories; its ARM64 refusal remains separate. |
| [Current launcher](https://github.com/banodoco/astrid-pinokio/blob/1e4c1e77f0d2b1ed322d0112d5f40103c998c5eb/pinokio/lib.js)455–498 | Editor promotion precedes bootstrap; paired durable recovery before promotion must be explicit. Actual deployed engine behavior remains unproved by this source read. |
| [Managed render](https://github.com/banodoco/astrid-agent/blob/dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5/astrid/packs/rendering/actions/render/managed_timeline.py) | Source cross-check observes separate list/expected-version and current-head reads, a potential selected-parent race; subsequent closure construction freezes parent/children. Establish the current upstream/later binding fence and repair only if reproduced or proved unsafe; do not invent a continuously mutable render. |
| [#1531](https://github.com/banodoco/astrid-dev/issues/1531), [#1657](https://github.com/banodoco/astrid-dev/issues/1657), [#2002](https://github.com/banodoco/astrid-dev/issues/2002) full bodies | Exact source-witness race, Undo availability/submission versus honest fixtures, and unresolved descriptor/opaque-precondition failure groups are explicit current handoffs. Old/synthetic context does not itself close their retained-path acceptance. |

The managed-render windows are 1020–1094 for the selection sequence and 860–1245 for closure. Parked-drop duplicate import is a **source-supported inference** from retrying the whole upload callback plus fresh import UUID; no duplicate incident was reproduced. Non-image handoff refusal is path-specific, not evidence every App media add is broken. #1916's child builder now passes verified_selection/capture; successful large-shots proof remains separate. These corrections constrain the actual work instead of expanding it.

### 9.5 Protection, coverage and unresolved access/proof

Read-only [dev ruleset27040267](https://api.github.com/repos/banodoco/astrid-dev/rulesets/27040267) showed active default targeting, PR approval count0, no code-owner requirement/stale dismissal, `documentation` and `vision-consumer-contract` integration15368 contexts, strict=false, and integration5728294 always bypass. App repository ruleset listing returned[]; that does not prove no inherited/classic/effective protection. A supporting effective-endpoint attempt was denied400; coordinator's earlier [#1963 comment7171826910](https://github.com/banodoco/astrid-dev/issues/1963#issuecomment-7171826910) reports its dev-effective read, separately attributed. Effective controls across every actual public write/deploy boundary and owner-specific permissions remain **unverified**, to be established before P31 authority cutover. No account/secret/admin access or configuration was changed. Source rules and required-status configuration are facts to verify, not authority to bypass them.

Coverage limits retained:

- Mandatory originals/corrections/final audit were all read; not every incidental linked historical issue comment, entire product file, proof artifact or recursive hyperlink was independently reread. Targeted primary windows cover disputed/high-harm decisions; original report provenance remains explicit.
- HOR-01's rate-limited GPU/unassigned searches and unavailable P88 direct path were genuine original limits. Coordinator supplied a later P88 handoff and bounded32-hit searches; final AUD extended the issue census but its recent-date slice read 100 of 216 results. These are bounded discovery, not an exhaustive no-other-defects claim. P88 final proof was delegated, not made true by finding the handoff.
- No native installation, original-peer/retained-handle behavior, deployed Pinokio engine, Windows TLS/async guard, physical GPU matrix, paid expiry/host-death cap or large-memory native measurement was performed in this synthesis. Their gates are concrete future evidence, not observed passing behavior.
- Exact historical published-origin artifacts, Linux arm64 support disposition, current native venues, final Windows managed route, effective release controls and residual estimates remain named work/owner decisions. None prevents submitting this complete report; each can block its affected implementation claim or publication.
- Internal read-only reviews found and corrected actual draft mistakes: RL-0 setup acceptance, PIN-END identity and pair-recovery gap; P38 original-peer/parent-birth predicate; legacy UI wording; existing-GPU independence; local versus paid-route gates; CC-3 exception-equality bypass; R0/P04 review cycle; absolute versus incremental memory; and retained outbox/measurement consumers. They are quality checks on this report, **not** the later independent REV or SC-FINAL acceptance.

The synthesis therefore recommends **REWORK with a concrete path to scope agreement**, not a new research blockade and not a ready-to-ship verdict. Materialize the actual brief/plan/input/task/run-board amendments, preserve history/status, obtain explicit decisions, then commission the independent actual-diff review and final whole-scope challenge required by the packet.

## 10. Complete original-reading and instruction register

The following 31 immutable originals were retrieved and semantically read through EOF in bounded chunks, including tables and caveats. URL compaction used while reading reduced repeated long links without dropping prose; raw full contents/identities were retained for source lookup. SHA is the original **blob**, distinct from its commit, the reviewed proposal and the eventual SYN evidence commit. AUD-01's completed continuation at 43e3 supersedes only its earlier incomplete-delivery status; initial observations and substantive REWORK findings remain preserved. No original is replaced by this synthesis.

| Original | Original commit | Blob SHA | Reading |
| --- | --- | --- | --- |
| [SC-09](https://github.com/banodoco/astrid-dev/blob/52c40028c067047533e222a017c92ac17f8cf5ba/plans/09-install-and-update-confidence/evidence/release-16-scoping/SC-09.md) | `52c40028c067047533e222a017c92ac17f8cf5ba` | `b129483fbd7c8ede8062f0a23800f5be8c66b77b` | Full, EOF |
| [SC-10](https://github.com/banodoco/astrid-dev/blob/d358b3b9de02c156d8a5576495256d6dea73c577/plans/10-pinokio-qualification/evidence/release-16-scoping/SC-10.md) | `d358b3b9de02c156d8a5576495256d6dea73c577` | `3b1ab93f58f69036ec19763b4e432a19ed446507` | Full, EOF |
| [SC-29](https://github.com/banodoco/astrid-dev/blob/68849637ddb2fb007289983727bc66e303328580/plans/29-update-and-release/evidence/release-16-scoping/SC-29.md) | `68849637ddb2fb007289983727bc66e303328580` | `91073d2b8a93ff9c44a03ce77e094d8ab3cb6133` | Full, EOF |
| [SC-30](https://github.com/banodoco/astrid-dev/blob/75d69e848eaa0760993e7be3a7c13c5fa7a0f19c/plans/30-update-everywhere/evidence/release-16-scoping/SC-30.md) | `75d69e848eaa0760993e7be3a7c13c5fa7a0f19c` | `2be7ebed40abcb6b66a32cee76e0005b8d7b323d` | Full, EOF |
| [SC-31](https://github.com/banodoco/astrid-dev/blob/25ced2a35b4677532911aaa61127fc9452be59b7/plans/31-releases-from-astrid-dev/evidence/release-16-scoping/SC-31.md) | `25ced2a35b4677532911aaa61127fc9452be59b7` | `df0d4c8fab68a86692e3fd30f62dfb12be1a368f` | Full, EOF |
| [SC-38](https://github.com/banodoco/astrid-dev/blob/7687ef518c86998f610ff4cf963e58b0565f38a1/plans/38-one-process-identity/evidence/release-16-scoping/SC-38.md) | `7687ef518c86998f610ff4cf963e58b0565f38a1` | `402b1fa7885cbf9ae51cc0f0b5cecba00765be80` | Full, EOF |
| [SC-93](https://github.com/banodoco/astrid-dev/blob/ace8e01a9455b97971691209682f65f568efcfda/plans/93-comfyui-desktop-and-existing-environments/evidence/release-16-scoping/SC-93.md) | `ace8e01a9455b97971691209682f65f568efcfda` | `7b3eb37cd49e0106776970467be9c4e719d2c136` | Full, EOF |
| [SC-94](https://github.com/banodoco/astrid-dev/blob/81105a08717746d0393ccf3bb126f8c71bbe2471/plans/94-dependable-environment-setup-and-recovery/evidence/release-16-scoping/SC-94.md) | `81105a08717746d0393ccf3bb126f8c71bbe2471` | `1767399f0ebfcfc55b18f90146f3db67d05d3909` | Full, EOF |
| [SC-90](https://github.com/banodoco/astrid-dev/blob/1bd93cf70f169e0db52f95ced5b8f9d189865539/plans/90-workflow-setup-exact-plan/evidence/release-16-scoping/SC-90.md) | `1bd93cf70f169e0db52f95ced5b8f9d189865539` | `34f5e6e5a88953c3806e9e7fcefe280a85ff9558` | Full, EOF |
| [SC-35](https://github.com/banodoco/astrid-dev/blob/44d813650b7e8b3726bd41699e80c182db8f79a1/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35.md) | `44d813650b7e8b3726bd41699e80c182db8f79a1` | `e18d1cba6376f5a02fdf62ba3e55717b5d300cf5` | Full, EOF |
| [SC-63](https://github.com/banodoco/astrid-dev/blob/6cf0dda31179711582a6ed0d8fcf76d3456c4de9/plans/63-dependable-saving/evidence/release-16-scoping/SC-63.md) | `6cf0dda31179711582a6ed0d8fcf76d3456c4de9` | `24e88f1fd77f92f8470b570ab4cbdc7fc6710e37` | Full, EOF |
| [SC-04](https://github.com/banodoco/astrid-dev/blob/cbd951924424ecbad213d3ad999a75ade2aabb51/plans/04-concurrent-edits/evidence/release-16-scoping/SC-04.md) | `cbd951924424ecbad213d3ad999a75ade2aabb51` | `6c30a5017ca9ad1c5e8a8c8ceefea69478d38b30` | Full, EOF |
| [SC-79](https://github.com/banodoco/astrid-dev/blob/ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1/plans/79-local-media-any-size/evidence/release-16-scoping/SC-79.md) | `ede2640e3a1b0ff2f1d5136abf289ff5a70d53f1` | `b5a6b0ceee61552fb12673d418310d2c42bfb217` | Full, EOF |
| [SC-87](https://github.com/banodoco/astrid-dev/blob/27212e5767406da192e6e822b2a56e59aa284a13/plans/87-render-works/evidence/release-16-scoping/SC-87.md) | `27212e5767406da192e6e822b2a56e59aa284a13` | `79b49761ce429cb95d823119684d384ad4d5054c` | Full, EOF |
| [SC-85](https://github.com/banodoco/astrid-dev/blob/799938e9ebcb2d8d97d078a27d448635ed7f7b5c/plans/85-one-place-to-measure/evidence/release-16-scoping/SC-85.md) | `799938e9ebcb2d8d97d078a27d448635ed7f7b5c` | `3f0415a04b1a5205d67022730fe20a65b05efc3e` | Full, EOF |
| [SC-56](https://github.com/banodoco/astrid-dev/blob/74eb2950b33233b076536f3178b1daaa86f675b1/plans/56-workflow-setup/evidence/release-16-scoping/SC-56.md) | `74eb2950b33233b076536f3178b1daaa86f675b1` | `89ac54c3faba9a508eccb54c7d9057551d34494b` | Full, EOF |
| [ISS-01](https://github.com/banodoco/astrid-dev/blob/1d8323ccf295f355628d5421701b1b0a0a40a8d0/releases/16/evidence/scoping/ISS-01.md) | `1d8323ccf295f355628d5421701b1b0a0a40a8d0` | `60959365c7fdfca78746dbe0f00ad0a4479aef61` | Full, EOF |
| [ISS-02](https://github.com/banodoco/astrid-dev/blob/9e34444b3c9269d42293ab30558561495d678e3b/releases/16/evidence/scoping/ISS-02.md) | `9e34444b3c9269d42293ab30558561495d678e3b` | `4242fc5b81e3d6b8e1d514bbf27734a8d1aa0bba` | Full, EOF |
| [ISS-03](https://github.com/banodoco/astrid-dev/blob/496ab219fff68b2ad85d762ec995da8d78a1d93a/releases/16/evidence/scoping/ISS-03.md) | `496ab219fff68b2ad85d762ec995da8d78a1d93a` | `64f588bb52b05f237c1674034305c14d3ba04a98` | Full, EOF |
| [ISS-04](https://github.com/banodoco/astrid-dev/blob/e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00/releases/16/evidence/scoping/ISS-04.md) | `e40e25ac21e7a3cc1e1bfeafdff3d8fa8d4b1f00` | `154d3b6a1f3d857a4cdd8a0f22e7c2366cf8ef65` | Full, EOF |
| [HOR-01](https://github.com/banodoco/astrid-dev/blob/736712b914dc2b46e6fd66dad2206d573ecf1510/releases/16/evidence/scoping/HOR-01.md) | `736712b914dc2b46e6fd66dad2206d573ecf1510` | `eb8957316c76e1552248ca76dcc67f8a7c850741` | Full, EOF |
| [INV-01](https://github.com/banodoco/astrid-dev/blob/17617b57cc0b4d0485ea68211b84b675f9b6c053/releases/16/evidence/scoping/INV-01.md) | `17617b57cc0b4d0485ea68211b84b675f9b6c053` | `9cce6af58063e83f1f3a518e6109fe43bed224c3` | Full, EOF |
| [INV-02](https://github.com/banodoco/astrid-dev/blob/f73732fbf825241f7be3f6204840e166a5f62c86/releases/16/evidence/scoping/INV-02.md) | `f73732fbf825241f7be3f6204840e166a5f62c86` | `692517ba245ac2b70cd11f9c83a7e0579869919b` | Full, EOF |
| [INV-03](https://github.com/banodoco/astrid-dev/blob/5d924e96aee1a2afdaeeb86131f698f5a57a5daf/releases/16/evidence/scoping/INV-03.md) | `5d924e96aee1a2afdaeeb86131f698f5a57a5daf` | `d5bd845d13805b1985077162b3416296b00e65f0` | Full, EOF |
| [INV-04](https://github.com/banodoco/astrid-dev/blob/9e8411372fc9a0257175d0f49da65ba7bee77bbb/releases/16/evidence/scoping/INV-04.md) | `9e8411372fc9a0257175d0f49da65ba7bee77bbb` | `9c63d2e3d4a2e785899a7a571da20c355752f559` | Full, EOF |
| [INV-05](https://github.com/banodoco/astrid-dev/blob/22d9be23d3001ca7dabb4b2e90fc38b8b59657bf/releases/16/evidence/scoping/INV-05.md) | `22d9be23d3001ca7dabb4b2e90fc38b8b59657bf` | `3a973a4e90fa8e3191a31263fe90413b6fd98e01` | Full, EOF |
| [INV-06](https://github.com/banodoco/astrid-dev/blob/f530e9b60391de8f60f8e38983038cf4615fa7e3/releases/16/evidence/scoping/INV-06.md) | `f530e9b60391de8f60f8e38983038cf4615fa7e3` | `dd08d1765b04638f194a337788e7ac24fce2ad5f` | Full, EOF |
| [INV-07](https://github.com/banodoco/astrid-dev/blob/ca85e04c05968ad8cb5d4b562e17045283018ce9/releases/16/evidence/scoping/INV-07.md) | `ca85e04c05968ad8cb5d4b562e17045283018ce9` | `49619dd01f68d75cb1ff11c50833b356f2b757b8` | Full, EOF |
| [SC-35-severity-correction-01](https://github.com/banodoco/astrid-dev/blob/ebe295571bb58028fe72d98c3da2cbe7fd40eaa5/plans/35-one-home-for-user-state/evidence/release-16-scoping/SC-35-severity-correction-01.md) | `ebe295571bb58028fe72d98c3da2cbe7fd40eaa5` | `53a024ba18e09bde3e44c1f7eb0b83a61f77d98e` | Full, EOF |
| [INV-04-coverage-addendum-01](https://github.com/banodoco/astrid-dev/blob/1e38786e3560d979b246a0ad0526920f4e3aa2ce/releases/16/evidence/scoping/INV-04-coverage-addendum-01.md) | `1e38786e3560d979b246a0ad0526920f4e3aa2ce` | `a9fe797b794f2ca9314108fb1c5104d39ba322d1` | Full, EOF |
| [AUD-01](https://github.com/banodoco/astrid-dev/blob/43e3e390d6ffe026e6f2a61f0c866b0ac94daf9b/releases/16/evidence/scoping/AUD-01.md) | `43e3e390d6ffe026e6f2a61f0c866b0ac94daf9b` | `25e688ff9492c326676d14fc72d5aca9ba675742` | Full, EOF |

Pinned governing workstreams, each read in full at **7060b764ec16a638b0e6774f814eabf6d7b70c04**:

- [scope-release](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/scope-release.md)
- [sense-check](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/shared/workstreams/sense-check.md)
- [chatgpt-packet](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/manager/chatgpt-packet.md)
- [multi-manager-dispatch](https://github.com/banodoco/astrid-dev/blob/7060b764ec16a638b0e6774f814eabf6d7b70c04/agent/roles/orchestrator/multi-manager-dispatch.md)

Shared [procedure](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/dispatch-v2/README.md), [context](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/dispatch-v2/context.md), [evidence index](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/README.md), [CTX-00](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/CTX-00.md), [CTX-01](https://github.com/banodoco/astrid-dev/blob/f8721766ba2fcb7762ca42767749409d00aa2dbc/releases/16/evidence/scoping/CTX-01.md), and [owner parallel-delivery direction](https://github.com/banodoco/astrid-dev/blob/6def0198c7a9a89f0e85b97582ef287274ef73a9/releases/16/evidence/scoping/README.md#owner-direction--parallel-delivery) are the procedure/context sources. Root AGENTS at the pinned proposal was unavailable; no installed revision is invented. The user's report-only authority and exact branch base govern submission.

**Intake and remaining acceptance:** coordinator verifies the exact report-only commit/diff and records the immutable original receipt. Coordinator then materializes the proposed canonical changes on its proposal, records actual base/head, and sends that concrete diff plus originals to a different fresh Pro for REV. After material repair, a third fresh Pro performs SC-FINAL on the revised whole. This report cannot substitute for either review or the owner's scope, implementation or publication decisions.

<!-- Original source reference definitions -->
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


