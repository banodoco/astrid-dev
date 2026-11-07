---
name: astrid-dev-manage
description: Run an accepted Astrid project or multi-agent effort end to end: dispatch tasks by route, judge what agents report, keep run state, integrate, and bring only real decisions to the owner.
---

# Manage an Astrid project

Use this when you coordinate work done by other agents. The manager is an administrator: it dispatches, checks and keeps state, and escalates judgment to [Advise](../astrid-dev-advise/SKILL.md). It covers running an accepted project, a cross-repository effort, or a batch of tasks. [Plan](../astrid-dev-plan/SKILL.md) defines the work, [Iterate](../astrid-dev-iterate/SKILL.md) does each change, and [Release](../astrid-dev-release/SKILL.md) integrates and publishes. The [run contract](../astrid-dev-shared/run-contract.md) owns routes, run state and review policy. A draft project or this skill is never authorization to execute.

## Principles

1. **One model per shared surface.** When two pieces of work touch the same screens, contract or files, settle one model before dispatching either. Do the same with other active projects.
2. **A report is a claim.** Trust agent output only as far as its evidence goes, and check the claims your next action depends on against code, logs or a run.
3. **See it before you fix it.** When a failure's cause isn't visible, first make it visible: full errors, uploaded logs, a diagnostic. Then fix.
4. **Prove what ships.** Evidence counts only for the exact candidate users will receive: every pinned version, on the path they will use.
5. **Spend judgement where it pays.** Start on the cheapest route that can do the task. Escalate when cheaper attempts guess, repeat a failure, or the stakes are security, data or an untested protocol.
6. **Decisions are durable.** Record owner decisions and enforce them with a test or check, so later work cannot quietly undo them. Ask the owner only what is genuinely theirs, with a recommendation. Decide the rest and record it.

## Run the work

- Resume the matching run before starting a new one. Preserve source and donor identities, `run.yaml` bindings, accepted scope, evidence, review counters and pause/STOP state.
- Dispatch only ready tasks, each to a subagent on its route. Every assignment states the outcome, the paths in scope, dependencies, frozen source identities, the route, the focused acceptance check, and the authority. Continue independent tasks while one is blocked.
- Take each assignment's scope from its task card: the paths, and any shared surface or contract, it may change. Never run two tasks with overlapping scopes at once; start the later one from the earlier one's landed result. At landing, compare the changed files with the scope, and if anything falls outside it, stop and consult [Advise](../astrid-dev-advise/SKILL.md) before widening it. If a task needs its own checkout to run checks, make it from the latest head and delete it when the task lands; a long-lived branch on a stale base is what hides collisions.
- Keep minimal state: the candidate, completed and blocked tasks, exact failures, evidence, review rounds used, and the next action. Keep task progress in the project's `tasks.md`, and status in the catalog.
- Keep one way into each integration target. Bring in changes that arrived another way before moving the target, and say so.
- When a cheaper attempt is stuck or the choice is consequential, consult [Advise](../astrid-dev-advise/SKILL.md).
- Never start paused work, add review stages, reset counters, or schedule work on the strength of these documents.

## Report

Tell the owner what changed, what is proven and on which exact candidate, what failed and why, and each decision that needs them, with your recommendation. A blocker names its dependency, producer, the awaited event and any deadline.
