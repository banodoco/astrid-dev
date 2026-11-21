# Inputs — Gap definition and reconciliation

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — the owner requested this complete planning pack and on 20 November 2026 explicitly instructed its merge to `main`. This authorizes recording the plan but does **not** start work, accept the still-untested rubric, authorize catalogue migration or activate recurring reviews. The owner explicitly deferred the weekly workstream and its validation to future Phases 6–7. **Next:** independent scope critique and recorded approval of the implementation scope before any project run; revise the plan if the critique finds substantive problems.

**Prior art:** Read against Astrid Dev `main` at `6d174521e6f3996349044e393d51b9fa06dbc625`, 20 November 2026. [`docs/contribution-workflow.md`](../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap), [`templates/gap.md`](../../templates/gap.md), and [`astrid-dev-gap`](../../agent/shared/workstreams/gap.md) already define per-gap records, independent closure and project back-links. [`scripts/check_gap_boundaries.py`](../../scripts/check_gap_boundaries.py) and [focused tests](../../scripts/test_check_gap_boundaries.py) already gate material changes with a first-principles PR rationale; [`scripts/checks.py`](../../scripts/checks.py) and [`scripts/check_docs.py`](../../scripts/check_docs.py) check syntax/linkage but not strategic correctness. [Plan 52](../52-issue-intake/plan.md) owns issue intake and labels, [Plan 53](../53-vision-aspirations/plan.md) owns vision-goal authoring, [Plan 44](../44-vision-execution-trail/plan.md) owns public evidence presentation, and [Plan 58](../58-strategy-from-releases/plan.md) owns release-led strategy. Open [Dev PR #1059](https://github.com/banodoco/astrid-dev/pull/1059) and [App PR #323](https://github.com/banodoco/astrid-app/pull/323) coordinate canonical Goals and compatibility aliases. This is a **source review**, not a product qualification, complete issue census or independent critique.

**Approach:** Reuse the existing rubric homes, single-gap skill, first-principles PR boundary receipt and project/release records. Make one implementation-independent standard, collect representative examples with untouched holdout cases, calibrate independently, then carry out a bounded all-record census and propose only justified changes. Review the proposed old-to-new migration before writing canonicals. Keep Phases 6–7 as clearly documented future entry points, with no new weekly skill, scheduled automation, bot or checkpoint built now. Alternatives compared: (a) direct rewrite of all 22 gaps first — faster but would encode arbitrary abstraction; (b) add only a paragraph to `astrid-dev-gap` — too little empirical validation; (c) immediately build an automatic issue-to-gap classifier or weekly job — duplicates issue intake and prematurely fixes a taxonomy; (d) the selected definition-first, evidence-calibrated one-off project — produces a durable baseline and leaves future recurrence optional. Do less when the existing boundary or evidence alone needs no change.

**Challenge:** Pending — a genuinely independent high-judgment critique is required because this changes Astrid Dev's own gap authoring rules/checks and could affect the App's Vision feed, and the estimated effort exceeds five engineering days. No independent verdict has been performed or claimed in this planning session. Next: have an adviser/reviewer independently inspect the actual gap workstream, template, checks, Plan 52/53 boundaries, the proposed task scopes and the full PR diff; ask especially for deletions, overlap with Plan 44/53, premature new record types, weak holdout proof, ID-compatibility hazards, and overconfidence in issue searches. Record findings and disposition before greenlight. Later RS1 and RS2 guard the two load-bearing decisions during execution.

**Proof and limits:** Proposed (not executed): named sample and untouched holdout with issue/project/gap references and explicit disagreement results; accepted definition with positive and counterexamples; complete source census with GitHub query pagination, inclusion/exclusion and precise revision/cutoff; one disposition for every original gap and proposed new outcome, with meaningful negative closure cases; old-to-new ID mapping and non-loss of inbound links; actual `check`, original focused unit tests, `sync`, app/feed qualification if needed, and independent final review. Unknowns: true issue corpus/duplicates, which old gaps to keep or split, semantics of retired-ID presentation, how many code checks must change and what will land from the Goals migration. No invented success or closure is asserted.

**Review rounds:** Recommend one independent **RS1** after calibrating the definition, one independent **RS2** before applying the entire migration, and one integrated final **R** after code/content changes; at most one round at each stop, with specific findings converted to task rows if necessary. Two stops earn their cost because a bad rubric would invalidate Phase 4, and an incorrect catalogue/ID mapping would invalidate Phase 5. Pending the owner's agreement to this review count and the reviewer's first critique.

**Run start:** Pending — no implementation run authorized. Before work, record the authorized phases, actual base and affected repository heads, one accountable agent, current source ownership, task route/model bindings and precise permission boundaries as the [run contract](../../agent/shared/run-contract.md#who-answers-for-a-run) requires. Any future Phase 6/7 run requires separate explicit authorization.

### Observed reasons this needs its own plan

The [public vision catalogue](../../vision/README.md) currently enumerates 22 assessed outcomes and the [plan catalogue](../index.md) 66 projects. GitHub issue search returned 191 issues at the planning snapshot, including open and closed records; these are navigation counts, **not** a completed all-issue classification or guarantee about historical transfer. More important than the counts are competing boundaries: [F-003](../../vision/gaps/F-003-creative-execution.md) covers many different creator experiences, while [F-008](../../vision/gaps/F-008-portable-generation.md) includes both user portability and specific architecture. [Plan 55](../55-local-speed/plan.md) is primarily a latency outcome under F-008, [Plan 39](../39-green-mains/plan.md) is a test-confidence outcome under F-001, and [Plan 18](../18-timeline-editing/plan.md) maps to LS-003 despite important editing semantics. These are boundary questions to **test**, not outcomes already settled.

Examples for Phase 2's initial candidate pool (verify source revisions and reserve separate holdouts at execution):

| Candidate capability / tension | Evidence to inspect | What must not be assumed |
| --- | --- | --- |
| Durable editing and recovery vs broad creative execution | [#966](https://github.com/banodoco/astrid-dev/issues/966), [#732](https://github.com/banodoco/astrid-dev/issues/732), [#842](https://github.com/banodoco/astrid-dev/issues/842), [#1002](https://github.com/banodoco/astrid-dev/issues/1002); [Plans 18](../18-timeline-editing/plan.md), [35](../35-one-home-for-user-state/plan.md) | Four bugs do not automatically justify one new gap |
| Fine artistic generation control vs dependable execution | [#890](https://github.com/banodoco/astrid-dev/issues/890), [#885](https://github.com/banodoco/astrid-dev/issues/885), [#860](https://github.com/banodoco/astrid-dev/issues/860); [Plans 64–70](../64-h3-speaker-references/plan.md) | Model-specific implementation inputs are not automatically distinct gaps |
| Execution reliability vs retry/settlement correctness | [#958](https://github.com/banodoco/astrid-dev/issues/958), [#926](https://github.com/banodoco/astrid-dev/issues/926) | Related symptoms may have different root causes |
| Installation and readiness vs test-confidence infrastructure | [#721](https://github.com/banodoco/astrid-dev/issues/721), [#733](https://github.com/banodoco/astrid-dev/issues/733); [Plan 39](../39-green-mains/plan.md) | A green build or completed plan is not itself creator-facing closure |
| Outcomes without dense issue evidence | [CA-002](../../vision/gaps/CA-002-contributor-ownership.md), [F-006](../../vision/gaps/F-006-fully-hosted-workspace.md), [CI-002](../../vision/gaps/CI-002-federated-knowledge.md) | Current issue volume must not define the universe of important gaps |

Phase 2 must also include at least one genuinely valid existing gap, one non-gap engineering issue, one evidence-only update, one ambiguous split/merge case, and one vision-goal-derived candidate with no relevant issue. Separate source-held training samples from the independent holdout before calibration.

### Boundaries with neighboring projects and processes

- **Plan 52 / issue triage:** does ordinary intake and implementation routing. This project can inspect issue evidence and propose corrected `gap:ID` associations; it does not add issue statuses or change the triage bot without separate justified scope.
- **Existing Gap workstream:** owns the individual gap outcome, approach, closure evidence and route. Strengthen it rather than duplicating its rules in a new skill.
- **Plan 53 / Goals PR:** owns goal terminology, schemas and feed compatibility. Rebase or wait for its landed result before changing the same files; this project must not independently rename the public schema.
- **Plan 44 / public evidence:** owns making the vision-to-execution trail understandable to visitors. This project supplies accurate gap records and provenance, not another presentation feature.
- **Plan 58 / releases:** release briefs own delivery commitments; this project records evidence that informs gaps, not release scheduling.
- **Future Gap Review:** unlike this one-off full census, a weekly stream would collect deltas and keep checkpoints. Deliberately out of current implementation.

## Owner decisions

**D1 — Sequence (decided, 20 November 2026).** The owner chose definition first, then representative evidence, calibration, comprehensive reconciliation and approved migration; do not rewrite the gap catalogue before the rubric is validated.

**D2 — Recurrence boundary (decided, 20 November 2026).** The owner explicitly kept the recurring review workstream and its historical weekly validation as Phases 6 and 7 **deferred**. Do not install `astrid-dev-gap-review`, schedule any weekly run or build a permanent review-state system in Phases 1–5.

**D3 — Definition sign-off (pending).** Recommend requiring recorded owner acceptance of the independently challenged rubric at the Phase 3 gate before Phase 4. Next: present the tested rubric, disagreements and tradeoffs.

**D4 — Catalogue migration (pending).** Recommend reusing IDs for stable outcomes, maintaining explicit supersession references for splits/merges/retirements, and never marking a gap Closed merely because its definition moved. Next: review a complete old-to-new mapping and disposition examples at the Phase 4 gate.

**D5 — Check/schema changes (pending on evidence).** Recommend preserving the current PR boundary check and adding only focused validation for actual false accepts or broken links; avoid any schema/App changes unless validated compatibility necessitates them. Next: inspect the landed PR #1059/#323 contracts and propose a minimal diff.

**D6 — Review count and scheduling (pending).** Recommend RS1, RS2 and R, each one independent round; no release assignment or plan priority change as part of scope creation. Separately choose future Phase 6–7 cadence/activation only when those phases are proposed for execution.

**D7 — Execution authority (pending).** The owner has authorized writing this plan only. Next: request an explicit run start naming an accountable agent, approved Phases 1–5, exact baseline and repository/issue mutation permissions. Independently authorize future Phase 6/7.

## Source identities

**Planning base:** `banodoco/astrid-dev` `main` at `6d174521e6f3996349044e393d51b9fa06dbc625` (read 20 November 2026). Planning proposal branch: `scope/71-gap-definition-reconciliation`; initial destination `main` through a maintainer-reviewed scope PR, **not** a Release 14 plan branch. These are planning references, not implementation pins.

**Current shared surfaces:** `docs/contribution-workflow.md`, `templates/gap.md`, `skills/shared/workstreams/astrid-dev-gap/SKILL.md`, `scripts/check_gap_boundaries.py`, `scripts/check_docs.py`, `scripts/checks.py`, `scripts/gap_relationships.py`, `scripts/export_public_vision.py`, `vision/gaps/*.md` and `plans/*/plan.md`. The canonical PR #1059 migration and related App PR #323 remain in progress at planning time; check their live heads before task assignment.

**At implementation:** Re-read current refs, writer/ownership state, accepted Plan 53 output, issue inventory and actual App contract. If an active branch or owner conflicts on a shared record, coordinate before editing; do not fabricate compatible donors, an automatically rebased baseline or claimed CI results. Capture full issue-search pagination and any missing history during GD-6.

## References

- [Gap workstream](../../agent/shared/workstreams/gap.md), [project planning workstream](../../agent/shared/workstreams/plan.md), [contribution design principles](../../docs/contribution-design-principles.md).
- [Gap source template](../../templates/gap.md), [gap PR boundary check](../../scripts/check_gap_boundaries.py), [boundary regression tests](../../scripts/test_check_gap_boundaries.py), [public Vision exporter](../../scripts/export_public_vision.py).
- [Issue intake and triage](../../docs/contribution-workflow.md#issues), [project-format contract](../../docs/project-format.md), [releases and version strategy](../../strategy.md).
