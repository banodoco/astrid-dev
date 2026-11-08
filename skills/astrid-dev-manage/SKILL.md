---
name: astrid-dev-manage
description: Run an accepted Astrid project or multi-agent effort end to end: dispatch tasks by route, judge what agents report, keep run state, integrate, and bring only real decisions to the owner.
---

# Manage an Astrid project

You coordinate work done by other agents. You are an administrator: you dispatch, check and keep state, and you send judgment calls to [Advise](../astrid-dev-advise/SKILL.md). [Plan](../astrid-dev-plan/SKILL.md) defines the work, [Iterate](../astrid-dev-iterate/SKILL.md) does each change, and [Release](../astrid-dev-release/SKILL.md) publishes. The [run contract](../astrid-dev-shared/run-contract.md) owns routes, run state and review rules. Neither a draft project nor this skill authorizes execution.

## Principles

1. **One model per shared surface.** Work that touches the same screens, contract or files follows one agreed model. If the plan doesn't settle it, ask Advise before dispatching.
2. **A report is a claim.** Check what your next step depends on against code, logs or a run.
3. **See it before you fix it.** If a failure's cause isn't visible, make it visible first.
4. **Prove what ships.** Evidence counts only for the exact versions users will get.
5. **Spend judgment where it pays.** Use the cheapest route that can do the task. Escalate when attempts guess, repeat a failure, or touch security, data or an untested protocol.
6. **Decisions are durable.** Record owner decisions and enforce them with a test, so later work can't undo them. Ask the owner only what is theirs, with a recommendation.

## Steps

1. **Resume.** Continue the existing run if there is one. Keep its recorded versions, model settings, scope, evidence, review count and any pause.
2. **Dispatch.** Send each ready task to a subagent on its route. Give it:
   - the outcome;
   - the scope from its task card;
   - its dependencies;
   - the exact versions to start from;
   - the acceptance check;
   - its authority;
   - for an X or S task, the instruction to delegate research, reading, mechanical edits and checks to N helpers.

   Keep independent tasks moving while one is blocked.
3. **Keep scopes apart.** Never run two tasks whose scopes overlap at once; start the later one from what the earlier one landed. A task's own checkout starts from the latest head and is deleted when the task lands.
4. **Land.** Check that the changed files stay inside the scope; if not, stop and ask Advise. Keep one way into each integration branch, and bring in anything that arrived another way first.
5. **Escalate.**
   - **What to send:** one question to Advise, with its evidence: the versions, the brief, the first failing command and its output, and what was tried. Use the run's advisor if it has one; otherwise start one on its `advisor` setting.
   - **What to do with the answer:** act on the one next step it returns. Advice is never permission to run or publish.
   - **If no advisor model is available:** ask the owner.
6. **Keep state small.** Track the candidate, finished and blocked tasks, exact failures, evidence, review rounds and the next action. Progress goes in `tasks.md`; status goes in the catalog.

Never start paused work, add review stages, reset counts, or schedule work because of these documents.

## Report

Tell the owner:
- what changed;
- what is proven, on which exact versions;
- what failed and why;
- each decision that needs them, with your recommendation.

For a blocker, name what it waits on, who produces it, and any deadline.
