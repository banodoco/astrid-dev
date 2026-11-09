---
name: astrid-dev-plan
description: Define independently useful new Astrid project scope by reusing prior art, challenging consequential choices, and recording a verifiable end state.
---

# Plan a new Astrid project

Enter through [astrid-dev](../astrid-dev/SKILL.md) and its [domain map](../astrid-dev/references/domains.md).

## Terms

- **Owner:** the person who chooses a project's outcome and makes its decisions.
- **Planner:** you, an administrator: gather evidence, write the task cards, and send consequential judgment to the advisor ([Orchestrate](../astrid-dev-orchestrate/SKILL.md), advise path). An orchestrator may also plan a project itself before farming it out.
- **Route:** N, X, S or T; the [run contract](../astrid-dev-shared/run-contract.md) alone owns routing, execution state and review policy.
- **Scope** (of a task): the paths, and any shared surface or contract, it may change; a path includes its own tests, wherever they live. Name the functions or classes too (`path:symbol`) when the task changes only part of a file.

## The answer

You produce an agreed, testable end state and tasks another agent can run.

1. **Projects are for new, separately useful outcomes** with their own priority, owner and completion proof. Bugs, small fixes and maintenance normally go in issues; existing project tasks use their accepted plan.
2. **Planning authorizes no execution or release.** Run no product tests and start no work unless asked.
3. **Agree the outcome once.** Record the owner's actual choice with a traceable source; a draft project or PR, or no objection, is not approval. Keep earlier accepted scope; avoid repeated sign-offs.

## Steps

1. **Start from [`strategy.md`](../../strategy.md),** so the project fits the current sequence, then **find prior art** in affected source, issues, [plans](../../plans/index.md), [gaps](../../vision/README.md) and, where relevant, outside approaches. Trace input → actual implementation → user-visible result, noting useful source revisions, reuse, negative findings and uncertainties. Delegate bounded research when helpful, but no broad audit without a decision it could change.
2. **Pick the smallest complete result.** Compare reusing or extending a pack, adding one, changing core and, when relevant, doing less or nothing. Prefer an existing plan or gap to a new entry. Justify placement and tradeoffs from evidence, not architectural preference. When the gap has a route to closure, place the plan in it with the [Gap](../astrid-dev-gap/SKILL.md) skill, and add the plan's `Contributes to closure:` line.
3. **Challenge in proportion to consequence.** For material architecture, an expensive or hard-to-reverse decision, or a table case below, have the advisor critique the plan for real removals, consolidation and reuse; record its findings and what you accepted or rejected. A simple bounded project needs only a concise alternatives review and a reason to skip the advisor.
4. **Agree the outcome.** Present the real options (as many as the owner needs; ten is a useful technique, not a quota), their user-facing tradeoffs and a testable end state.
5. **Write a compact handoff,** one home per fact: [`inputs.md`](../../templates/project/inputs.md) for source evidence, alternatives, challenge decision, approval and uncertainty; [`plan.md`](../../templates/project/plan.md) for outcome, scope, sequence and completion; [`tasks.md`](../../templates/project/tasks.md) for assignments and focused proof ([rules below](#write-the-task-list)). Link detailed work only for a distinct use.
6. **Seek greenlight.** A contributor may [open a proposal issue](../../docs/contribution-workflow.md#propose-and-greenlight-new-work) without permission. A maintainer-reviewed **scope PR** greenlights new scope by recording the owner's actual decision in `inputs.md` and adding one queued catalog entry.

## Scale the method

Each step below earns its cost only under its condition; skip it otherwise. Each produces a file the next step reads.

| Step | Do it when |
|---|---|
| Map current behaviour with parallel N helpers, one read-only area each | the behaviour spans several repositories or areas, or no one planning knows it |
| List each problem with its root cause and where it is fixed | the request starts from symptoms (bugs, confusing UI) rather than a new capability |
| Consult the advisor ([Orchestrate](../astrid-dev-orchestrate/SKILL.md)) as the critic, briefed to build as little as possible and to verify claims in code | the plan touches a cross-repository contract, a user-visible flow, release, security or data, or exceeds about five days |
| Phase it: a first phase with most of the value, later phases committed, estimates per phase | the estimate exceeds about ten days or value is uneven across tasks |
| Ambiguity pass by N helpers per task group, resolving from code and listing only real owner decisions | other agents will execute the tasks, or any task is X, S or T |
| Record owner decisions in `inputs.md` and enforce them with a test | a later merge could silently undo the decision |

## Write the task list

In the [tasks template](../../templates/project/tasks.md), every task has a scope and:

- **A route:** N by default, X for coupled or non-obvious changes, S where correctness needs the deepest reasoning (a protocol never run end to end, security, data safety, migration), and T for taste: small, editorial refinement that needs a high level of polish, such as user-facing copy, refusal and error messages, naming, a screen's layout or a skill's voice. A T task refines something that exists against a stated intent; it is not creative and adds no scope. Split taste out of larger tasks, so the functional change is N, X or S and the wording or polish is its own small T task ([run contract](../astrid-dev-shared/run-contract.md#routing-and-bindings)).
- **Dependencies,** only where one task needs another's result, or both change the same function, class or contract. Sharing a file is not a dependency: tasks that change different functions in one file run in parallel, with a merge order. The same applies across other active projects. If a shared surface needs one model first, consult the advisor.
- **The critical path:** state it in `tasks.md`, and keep it as short as the work allows. Chain tasks only where the rule above requires it.
- **Before implementation:** its actual base and donor revisions, exact focused checks and authority.
- **Checks a cloud worker can run.** Setup and checks use astrid-dev's [shared worker environment](../../env/README.md), called by literal path. They must work in a session with only the task's repository attached:
  - other repositories come from public git at pinned commits;
  - no GitHub archive downloads;
  - no private repositories;
  - small fixtures go inline in the task card.

  Add a missing script there, not in the plan folder.

End with the review row, before any publishing task, which depends on it. Recommend its number of review rounds from risk and complexity (guide in the run contract), say why, and record the owner's agreed number in `inputs.md`. With 0, leave the row out.

## Readiness

- A draft can mark what is **Pending**, with the next action.
- A defined project needs real prior-art findings, an explained reuse decision, a traceable owner choice and meaningful completion evidence; a consequential design also needs critique or an explicit unresolved blocker.
- Don't make the agent fabricate evidence, or add heavy ritual to a simple decision.
