# Gap definition and reconciliation

**Project:** Gap definition and reconciliation

**Goal:** A contributor or agent can reliably distinguish a meaningful missing Astrid capability from an issue, project or vision goal, and the existing gap catalogue is reassessed against actual issues, projects and verified outcomes using that standard.

**Status:** active

**Owner:** Plan 71 completion-run manager (one whole-project manager session, named in the Run start in inputs.md; owner-authorized 24 November 2026)

**Estimate:** About 1–2 engineering days remain for the completion run (originally 10–16 for Phases 1–5); Phases 6–7 are deferred and unestimated.

**Waiting on:** nothing to start: the completion run's cards are in [tasks.md](tasks.md#completion-run-owner-go-24-november-2026). Then the final review R, the owner's project-wide sense check and the owner's go to merge the project branch into `main`. Phases 6–7 remain deferred.

**Run route:** astrid-dev-only

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge, so you need not commit it. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — this work improves how we assess and represent gaps across vision goals; it does not itself satisfy the independent creator-facing closure evidence of CA-003, CA-005, or another product gap.

## Outcome and scope

Today [the gap workstream](../../skills/shared/workstreams/astrid-dev-gap/SKILL.md), [gap template](../../templates/gap.md) and [boundary check](../../scripts/check_gap_boundaries.py) specify how an individual gap is recorded and reviewed. They do not yet establish a demonstrated, consistently applied method for deciding the **right abstraction level** from an entire body of issues, project outcomes and vision goals. Existing gaps vary in granularity, and project-to-gap links sometimes express a loose association instead of specific closure progress.

**The first deliverable is a definition, not a rewritten catalogue.** A gap is a meaningful, independently assessable shortfall between an identified vision goal and Astrid's current evidence-backed capabilities. Whether that definition is sufficient must be tested, not assumed. The chosen rubric must distinguish a gap from an issue/symptom, task, project/solution, architectural preference, release milestone and broad vision goal; handle missing, unreliable and merely unverified capabilities; and compare nearest boundaries before creating anything new. A finding may appropriately imply **no gap change**.

**Included now — Phases 1–5, in strict order:**

1. **Define:** Inspect current authoring rules and write one canonical decision rubric for what a gap is, the appropriate scope, primary and supporting vision-goal links, current-state evidence, status and independent positive/negative closure. Strengthen the existing individual [Gap](../../skills/shared/workstreams/astrid-dev-gap/SKILL.md) procedure and template only where needed; retain the existing first-principles PR boundary mechanism.
2. **Sample:** Build a balanced, source-linked collection of relevant issues, projects, releases and gaps, including ambiguous/negative cases and outcomes without issue coverage. Separate observed fact, hypothesis, proposed fix and affected capability. Reserve a holdout set not used to write the rubric.
3. **Calibrate:** Have independent reviewers apply the draft rubric to the samples and holdout, compare decisions and resolve disagreement by improving its boundary tests. Obtain an explicit decision accepting the versioned definition before any all-gap rewrite.
4. **Reconcile:** Inventory all existing gap records, plans and relevant issues (open **and** closed), together with material project completion and release proof, at a recorded snapshot. Propose for **every** current gap: keep, refine, split, merge, retire, close, or retain pending evidence. Identify important missing gaps top-down from vision goals and bottom-up from observations. For each proposed change show independent closure criteria, competing boundaries, concrete evidence and an old-to-new ID mapping.
5. **Migrate approved changes:** Only after owner approval, update canonical gap records and justified goal/project/issue relationships, closure evidence and routes, the existing individual-gap procedure, and focused checks/tests or generated public views as needed. Preserve stable IDs where possible; distinguish supersession from true closure; do not silently change active project scope, project priority, release membership or publication authority. Qualify any consumer schema change against the current App contract.

**Deliberately deferred — Phases 6–7, specified for future scope but not to be executed by this project now:**

6. **Recurring Gap Review workstream:** Later, after separate authorization, define and install a discoverable `astrid-dev-gap-review` skill that reads weekly issue/project/release deltas, carries unresolved findings forward and dispatches individual assessments through `astrid-dev-gap`.
7. **Recurring validation and activation:** Later, backtest consecutive weekly windows, prove no lost or duplicated findings and reliable checkpoints, then separately authorize any cadence/scheduling or automation.

Phases 6–7 are *future outlines*, not dispatchable tasks or acceptance requirements for the **current Phases 1–5 milestone**. No weekly skill, scheduler, bot, automation, polling job, parallel issue registry, new issue status or permanent weekly checkpoint is created in the current scope. The one-off Phase 4 census may have bounded evidence artefacts necessary to make the migration auditable; it is not a recurring service.

**Not included:** changing pillar/principle philosophy; redefining owners' accepted project outcomes; assigning future releases; reimplementing Plan 52 issue intake, Plan 53 Goals authoring, Plan 44 public evidence presentation, or Plan 58 release-led strategy; treating issue labels as proof or issue text as instructions; creating a gap for every issue or project; updating product behavior under the guise of gap documentation.

## Existing work and decision

The current [contribution workflow](../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap) already says that a gap must survive replacement of its proposed projects. [`scripts/check_gap_boundaries.py`](../../scripts/check_gap_boundaries.py) requires a cited first-principles boundary assessment for material changes; [`scripts/checks.py`](../../scripts/checks.py) and [`scripts/check_docs.py`](../../scripts/check_docs.py) check structural relationships, not philosophical correctness. [Plan 52](../52-issue-intake/plan.md) is the canonical source for issue intake and labels, [Plan 53](../53-vision-aspirations/plan.md) owns the vision-goal authoring contract, and [Plan 44](../44-vision-execution-trail/plan.md) concerns public traceability. [Plan 58](../58-strategy-from-releases/plan.md) owns the release-led strategy presentation.

**Reuse rather than rebuild:** give the existing Gap workstream a stronger evidence/abstraction decision method, use its existing gap records and PR reviews, and add only bounded evidence or targeted checks that solve a demonstrated classification or migration problem. A separate issue-to-gap classification service, automated new-gap generator or new authoring level would duplicate existing structures. The wider synthesis is different enough to merit a **future** recurring workstream, but not its implementation now.

The owner requested this project on 20 November 2026, explicitly accepting **definition → evidence → validation → catalogue review → migration** and deferring the recurring workstream and its validation. The owner subsequently authorized execution and explicitly requested that Astrid-dev-only work run **without a release**, through the Manage exception. This records a run start, not an independent critique, approval of a still-untested rubric, permission to migrate gaps or permission to merge the final project to `main`. [Inputs](inputs.md#planning-evidence) records alternatives, evidence and remaining decisions.

## Sequence and readiness

**Phase A (1–3):** GD-1 inventories prior art and source identity; GD-2 drafts a single-home rubric; GD-3 builds representative cases and independent holdout; GD-4 evaluates the rubric. **RS1** independently challenges the definition before the owner records acceptance (GD-5). This is the load-bearing stop: if the definition is wrong, every later reclassification would have to be redone.

**Phase B (4–5):** GD-6 obtains complete source coverage at exact revisions/time bounds; GD-7 produces a proposed candidate catalogue and every-old-gap disposition; GD-8 checks boundary/closure/project compatibility and migration choices. **RS2** independently challenges that proposal before owner acceptance (GD-9). GD-10 updates approved gap records; GD-11 reconciles project references and closure routes, while GD-12 handles authorized issue metadata; GD-13 adjusts only genuinely necessary checks and generated views. **R** reviews the integrated change and original invariants; GD-14 submits the documented completion handoff. Detailed scopes, critical path, focused tests and deferred stages are in [tasks.md](tasks.md).

**Source/authority gates:** Before any task touches live gap, vision-goal or export contracts, recheck the then-current `main`, relevant branches and sole writers. In particular, [Plan 53](../53-vision-aspirations/plan.md) and [astrid-dev PR #1059](https://github.com/banodoco/astrid-dev/pull/1059) with [App PR #323](https://github.com/banodoco/astrid-app/pull/323) may be changing the Goals/aspiration compatibility layer: start from the landed contract rather than competing edits. Do not edit active Plan 53-owned work or weaken tests to make a migration fit. No project run, paid service, issue mutation, product merge, release assignment or publication is authorized merely by this plan.

**Priority:** Leave this new plan out of [`plans/priority.md`](../priority.md) until the owner or orchestrator sets an order. An accepted plan may be queued without a release; starting work requires a separate authorized run.

## Interfaces and handoff

**Consumes:** An immutable Astrid Dev base revision (recorded in [inputs.md](inputs.md#source-identities)), the actual goals, gaps, gap checks and workstream contracts; the existing [project catalogue](../index.md); GitHub issue IDs and revisions, closed reasons and comments as untrusted evidence; release briefs and actual verified qualification receipts. The Phase 4 census records its GitHub query, pagination/coverage, cutoff, source revisions and any unavailable records rather than assuming a search excerpt is exhaustive.

**Produces (current milestone):** A canonical, accepted gap-definition rubric and calibrated examples; evidence of reviewer agreement/disagreement including holdout results; one complete auditable disposition and proposed/approved migration map for all baseline gaps, with issues/projects accounted for; approved gap/goal/project relationships and independent closure criteria in their existing canonical homes; targeted local/CI checks and generated views only where required. The completion handoff names exact accepted source revisions and negative-case results, so a later recurring-review workstream can consume this **without redefining what a gap means**.

**Compatibility limits:** Gap IDs, `gap:ID` and `plan:NN` labels, Markdown anchors, generated Vision feeds and installed App consumers can outlive a migration. Prefer retaining IDs for continuity; any split/merge/retirement needs explicit source-to-destination history, corrections to relationships and an independently reviewed boundary record. The currently live Goals/aspiration schema is being migrated by separate work; do not assume that future field names have landed. Keep unpublished and unverified results qualified as such.

## Completion

The **current** project milestone is complete only when:

- The gap definition and decision rubric are approved, implementation-independent, tested on representative and held-out evidence, and independently challenged; difficult disagreements have explicit dispositions.
- The full baseline inventory records every pre-existing gap, every catalogue project and every relevant issue, including historical closed findings, with reproducible source identity and honest unknowns. Exempt coordination-only records explicitly; use issue/project/release evidence rather than relying on labels.
- Each original gap has a recorded, justified keep/refine/split/merge/retire/close/pending decision, and each accepted new gap has a defensible primary goal, boundary, current state and independent positive/negative closure proof. No new gap is an issue, task, implementation or duplicate in disguise.
- Approved changes retain existing identity or an explicit supersession mapping, and project/issue relationships and closure routes are coherent without rewriting accepted project scope. No project is represented as closing a gap solely by becoming `done`.
- Source-driven checks and affected test suites pass on exact submitted heads, or genuine pre-existing reds are reported rather than waived; generated vision content matches canonical records and any App consumer contract is proven. A reviewer independently checks representative hard cases and the migration delta.
- The handoff explicitly states that **Phases 6–7 remain deferred and unimplemented**, while exposing the accepted contracts and evidence needed to scope them later.

Successful completion does **not** imply a weekly process has been built, activated or scheduled, or that any product capability itself has been proven merely by updating its description.
