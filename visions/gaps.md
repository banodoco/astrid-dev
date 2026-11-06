# Gap records: how the vision stays grounded

**This is the documentation contract, not an implemented CI system or a substitute for the [run contract](../skills/astrid-dev-shared/run-contract.md).**

## What belongs where

- **[Vision](vision.md)** and four `principle.md` files: durable goals and reasoning about what matters; not technical status or implementation tasks.
- **`visions/principles/<principle>/gaps/<ID>-<slug>.md`**: a missing outcome directly tied to one of the four principles.
- **`visions/foundations/gaps/F-<number>-<slug>.md`**: a cross-cutting outcome required by multiple principles, e.g. reliable use on supported platforms. **Foundations are not another artistic principle.**
- **Both types of gap** are independently assessable and may be open with no plan or survive several completed plans.
- **`plans/<id>/plan.md`**: a specific attempt to close one or more gaps, or an explicitly named foundational enabler. Plans own their gap links, scope, tasks, dependencies, authorizations, status (through the root queue), and acceptance evidence.
- **Evidence:** a plan's recorded checks/reviews/artifacts, or a revision-pinned independent source. Evidence is assessed against a *gap's closure test*, not assumed from a task checkbox.

**Single owner per fact:** the root README owns plan statuses/owners/priorities; the plans own their gap relationships; gaps own the current-state assessment and closure criteria. Do not maintain a reverse plan catalog inside gap docs.

## Minimal gap contract

A new gap follows the same format as the existing gap files:

```md
# LS-004 — Short outcome name

**Principle:** [Agent-Powered Liquid Software](../principle.md) · **Assessment:** Open (YYYY-MM-DD, basis)

## Desired state
What would be true if we had achieved this?

## Current state
What was actually observed, with source revision/date and limitations?

## Gap
The missing ability or outcome—not a proposed implementation.

## Closure evidence
Observable outcome and the proof needed to judge it, including important negative cases.

## Sources and reassessment
Links to source/evidence; what remains uncertain or due for re-check.
```

Stable IDs are principle-prefixed (`AA`, `LS`, `CI`, `CA`), or `F` for cross-cutting foundations; they do not change when filenames or priority change. Foundation records replace the sample `**Principle:**` line with `**Category:** [Shared foundations](../README.md)`. The file's ID is its heading; links should point to the actual file, not assume GitHub can resolve the ID automatically. A gap's assessment may be **open**, **partially evidenced**, **closed**, or **needs recheck**; these are descriptions backed by evidence, not an automatic numeric score. Don't create new gaps for every plan task, and avoid claiming unknown things are absent just because the reviewer did not find them.

## Minimal plan declaration

Near the beginning of a plan, after its introduction:

```md
**Vision gaps:** [LS-001 — Portable components](../../visions/principles/liquid-software/gaps/LS-001-portable-components.md) (primary); [LS-002 — Agent workspace control](../../visions/principles/liquid-software/gaps/LS-002-agent-workspace-control.md) (supporting).
```

The primary gap can instead be a [cross-cutting foundation](foundations/README.md) such as `F-001`. Do not force operating-system qualification or safe update behavior into a single artistic principle.

Or, where a plan is infrastructure **without directly proving a gap outcome**, such as a behavior-preserving refactor:

```md
**Vision role:** Foundational enabler — explain in one sentence what future creative capability this makes safer or possible.
```

**Prefer one primary gap; list supporting gaps only where the plan really produces evidence toward them.** A plan completion may contribute only partial evidence to several gaps. For the existing backlog, add these declarations incrementally after reviewing actual plan scope; use the [dated assessment](references/plan-gap-assessment-2026-11-06.md) as a starting proposal, **not as a second live map**. Do not pretend every legacy plan is already classified. New plans should use the [project template](../templates/project/plan.md).

## Reconciliation: plan completion → new gap assessment

1. **Trigger:** a plan completes, or meaningful new source/evidence contradicts a gap's current assessment.
2. **Collect:** identify linked gap IDs from the *plan*, capture exact source revisions, run/evaluation evidence, limitations, and relevant original target state.
3. **Assess:** an agent proposes how each affected gap changed—closed, partially evidenced, unchanged, or needs recheck. Explicitly compare the actual proof with the gap's closure evidence; don't infer success from `done`.
4. **Review:** a human or authorized reviewer checks the proposal. Updating a gap is a docs decision; it does not retroactively change a project's accepted status or authorize new product work.
5. **Publish:** update the gap's **current state**, assessment date, evidence links and remaining differences. Preserve provenance; open a new plan only when the next distinct work outcome is scoped and authorized.

A later regression, new environment or conflicting evidence can reopen a gap. A gap that has never been proven in relevant real-world conditions may remain *needs recheck* even when related plans have passed.

## Future enforceability (not built yet)

**Deterministic GitHub checks** could validate unique gap IDs, expected headings/fields, valid relative links, the presence of `Vision gaps` or `Vision role` declarations on newly introduced plans, and existence of evidence links for explicit closure claims.

**Agent review** could inspect completed plans and changed repository evidence, then propose scoped gap-update PRs. Judgment about artistic quality, confidence, exact environmental applicability and whether a gap is truly closed must not be reduced to a naive CI pass.

**Do not implement automation until** one or two real gap-to-plan-to-evidence cycles are proven manually. Avoid scheduled broad autonomous code scanning, a second project queue, duplicated plan ownership, or any process that silently edits the vision.
