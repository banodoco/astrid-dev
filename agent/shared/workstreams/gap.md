---
description: Define, reassess and route Astrid vision gaps; write closure approaches and plans for each gap, and keep them aligned with release-led strategy when decisions change.
skill: true
---

# Work on an Astrid vision gap

## When to use

When assessing an aspiration blocked by several potential projects or revisiting a gap's closure approach.

## Outcome

A well-defined vision gap with closure evidence, a rationale and a route through relevant plans and strategy.

## Inputs

The vision and aspiration references, existing gaps and plans, supporting observations, strategy and authorized decision makers.

## Procedure

Compare the vision to current capability, write or revise the gap and its closure route, then maintain plan and strategy links.

## Completion

The gap records testable closure evidence and consistent references; consequential strategic decisions have been reviewed.

Enter through [astrid-dev](../../start.md). Use [Plan](plan.md) for a single project's scope. Use this skill for the outcome a set of projects serves; releases and their briefs own the cross-project delivery strategy.

## The levels

- **Vision** ([elements and their aspirations](../../../vision/README.md)): where Astrid is heading; a gap [names its aspirations](../../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap).
- **Strategy** ([`strategy.md`](../../../strategy.md)) draws on release briefs; see [how the documents fit](../../../docs/contribution-workflow.md#review-the-strategy).
- **Gap** ([`vision/gaps/`](../../../vision/gaps)): an assessed outcome that blocks the vision. It names a result that would still matter if today's projects were replaced, and it has its own closure evidence.
- **Closure approach and route to closure** (sections of the gap): the strategy. The approach is prose explaining the idea and the order of work. The route is an ordered table of plans, showing which closure evidence each one delivers.
- **Plan** ([`plans/`](../../../plans/index.md)): one project's scope, tasks and proof. Its `Vision gaps` line names the gap, and its `Contributes to closure` line names the evidence it delivers.
- **Catalog** ([`plans/index.md`](../../../plans/index.md)): every plan's status, priority, owner and estimate, generated from the six lines at the top of each `plan.md` and from [`plans/priority.md`](../../../plans/priority.md); edit those, not the catalog.

## Steps

1. **Define or reassess the outcome.** Compare the existing gaps and the catalog first, and refine an existing gap rather than add one. Don't create a gap for a task, a technology choice or a milestone. Creating or materially redefining a gap needs the boundary record in the PR description ([contribution workflow](../../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap)). Start a new gap from [the template](../../../templates/gap.md).
2. **Write the closure approach once plans exist.** A new agent should understand the strategy from it alone:
   - the idea behind closing the gap;
   - why this order;
   - what each stage changes for creators;
   - what is deliberately out.

   Keep it to a few paragraphs, and cite evidence rather than restating it.
3. **Write the route to closure.**
   - One row per step, in order. Run steps in parallel with `∥` in the Plan cell.
   - Map **every** closure-evidence item to a plan, or to an `unplanned` row.
   - Name milestones a creator would notice, and state the critical path.
   - Put no statuses, owners, estimates or tasks in it.
4. **Make the link two-way.** Each plan in the route names the gap in its `Vision gaps` line and states its `Contributes to closure:` items. A reviewer checks the two sides agree. CI checks the structure only.
5. **Reassess as plans land.** When a plan completes, update the gap's assessment and current state with real evidence, and adjust the route. Completing a plan never closes a gap automatically. Close the gap only when its closure evidence is observed.
6. **Keep releases in step.** When a gap’s route or assessment materially changes a planned release, update its [brief](../../../releases/TEMPLATE.md). Do not silently assign other work to a release.

## Revisit the strategy

[`strategy.md`](../../../strategy.md) summarizes release briefs, rather than repeating gap plans. Revisit it when gap reassessment or completed work materially changes the intended release outcome:
1. **Read the strategy page, the affected release briefs, the catalog and the affected gap route.** Each plan's `plan.md` owns its status and `plans/priority.md` owns priorities; the gap owns closure evidence; a release brief owns which plans are bundled for delivery and why.
2. **Update the release document first**, if its highlight, intent, approach or included plans change. Drafts can change without a publication event. An already finalized release is history: plan the change in a later release.
3. **Create a numbered release brief** when needed and its scope is credible. A queued plan alone does not warrant a number or promise shipment.
4. **Review authored strategy decisions** and update **Last reviewed** when direction changes. Sequencing is the owner’s decision.
5. **[Check it.](../run-contract.md#when-a-test-run-is-load-bearing)** `python3 scripts/astrid_dev.py check` verifies document structure; generated material is refreshed from its sources.

## Done when

- The gap reads well to an agent who has seen none of its plans.
- Every closure-evidence item has a route row, either a plan or `unplanned`.
- Every routed plan points back with `Vision gaps` and `Contributes to closure`.
- The affected release brief reflects the decision, without duplicating catalog ownership/status or gap closure evidence.
- `python3 scripts/astrid_dev.py check` passes.
