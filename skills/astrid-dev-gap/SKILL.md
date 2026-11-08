---
name: astrid-dev-gap
description: Define, reassess and route Astrid vision gaps; write the closure approach and the route of plans that closes a gap, and keep both honest as plans land.
---

# Work on an Astrid vision gap

Enter through [astrid-dev](../astrid-dev/SKILL.md). Use [Plan](../astrid-dev-plan/SKILL.md) for a single project's scope. Use this skill for the outcome a set of projects serves, and for the strategy that connects them.

## The levels

- **Vision** ([pillars and principles](../../vision/README.md)): where Astrid is heading.
- **Strategy** ([`strategy.md`](../../strategy.md)): the order across gaps: which ones we're closing now, next and later, and why. It links to each gap's route and never restates it.
- **Gap** ([`vision/gaps/`](../../vision/gaps/)): an assessed outcome that blocks the vision. It names a result that would still matter if today's projects were replaced, and it has its own closure evidence.
- **Closure approach and route to closure** (sections of the gap): the strategy. The approach is prose explaining the idea and the order of work. The route is an ordered table of plans, showing which closure evidence each one delivers.
- **Plan** ([`plans/`](../../plans/index.md)): one project's scope, tasks and proof. Its `Vision gaps` line names the gap, and its `Contributes to closure` line names the evidence it delivers.
- **Catalog** ([`plans/index.md`](../../plans/index.md)): the only home for status, priority, owner and estimate.

## Steps

1. **Define or reassess the outcome.** Compare the existing gaps and the catalog first, and refine an existing gap rather than add one. Don't create a gap for a task, a technology choice or a milestone. Creating or materially redefining a gap needs the boundary record in the PR description ([contribution workflow](../../docs/contribution-workflow.md#define-or-reassess-a-vision-gap)). Start a new gap from [the template](../../templates/gap.md).
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
6. **Keep the strategy in step.** When a gap's route or assessment changes its place in the sequence, update its row in [`strategy.md`](../../strategy.md) in the same PR.

## Done when

- The gap reads well to an agent who has seen none of its plans.
- Every closure-evidence item has a route row, either a plan or `unplanned`.
- Every routed plan points back with `Vision gaps` and `Contributes to closure`.
- `python3 scripts/check_docs.py` passes.
