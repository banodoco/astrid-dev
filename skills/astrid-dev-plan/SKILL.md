---
name: astrid-dev-plan
description: Define independently useful new Astrid project scope by reusing prior art, challenging consequential choices, and recording a verifiable end state.
---

# Plan a new Astrid project

Enter through [astrid-dev](../astrid-dev/SKILL.md) and its [domain map](../astrid-dev/references/domains.md). **Bugs, small fixes and maintenance normally belong in issues, not projects.** Existing project tasks use their accepted plan. This process is for a new, separately useful outcome that merits its own priority, owner and completion proof.

A contributor may [open a proposal issue](../../docs/contribution-workflow.md#propose-and-greenlight-new-work) without permission. New independent project scope is greenlit by a maintainer-reviewed Astrid-dev **scope PR** that records the owner's actual decision in `inputs.md` and adds one queued catalog entry. A PR draft is not acceptance.

Planning is a decision, **not** authority to execute or release. Preserve earlier accepted scope and avoid repeated owner sign-offs.

## Investigate, decide, preserve

1. **Find prior art.** Search the affected source, existing issues, [plans](../../plans/index.md), [gaps](../../vision/README.md), and external approaches where relevant. Trace input → actual implementation → user-visible result, including useful source revisions, reuse opportunities, negative findings and uncertainties. Delegate bounded research when helpful; don't commission a broad audit without a decision it could change.
2. **Pick the smallest complete result.** Compare reusing or extending an existing pack, adding a pack, changing core, and doing less or nothing when relevant. Prefer an existing plan or gap to a new entry. Explain the chosen placement and tradeoffs from evidence, not a general architectural preference.
3. **Challenge proportional to consequence.** The planner is an administrator: it gathers evidence, writes the cards and escalates judgment. For material architecture, cross-repository contracts, expensive or difficult-to-reverse decisions, consult [Advise](../astrid-dev-advise/SKILL.md) as the critic, to identify real removals, consolidation and reuse. Record its findings and what you accepted or rejected. For a simple bounded project, a concise alternatives review and a reason not to commission a second planner is enough. Offer as many meaningful end-state alternatives as the owner needs; **ten are a useful exploration technique, not a quota**.
4. **Agree the outcome once.** Present the real options, their user-facing tradeoffs and a testable end state. Record the owner's actual selection with a traceable source. Creating a draft project or receiving no objection is not approval.
5. **Leave a compact handoff.** [`inputs.md`](../../templates/project/inputs.md) owns the source evidence, alternatives, challenge decision, approval and uncertainty. [`plan.md`](../../templates/project/plan.md) owns outcome, scope, sequence and completion. [`tasks.md`](../../templates/project/tasks.md) owns assignments and focused proof. Link to detailed work only when it has a distinct use; do not copy reasoning across all three files.

## Scale the method to the project

Each step below earns its cost only under its condition; skip it otherwise. Each produces a file the next step reads.

| Step | Do it when |
|---|---|
| Map current behaviour with parallel N helpers, one read-only area each | the behaviour spans several repositories or areas, or no one planning knows it |
| List each problem with its root cause and where it is fixed | the request starts from symptoms (bugs, confusing UI) rather than a new capability |
| Consult [Advise](../astrid-dev-advise/SKILL.md) as the critic, briefed to build as little as possible and to verify claims in code | the plan touches a cross-repository contract, a user-visible flow, release, security or data, or exceeds about five days |
| Phase it: a first phase with most of the value, later phases committed, estimates per phase | the estimate exceeds about ten days or value is uneven across tasks |
| Ambiguity pass by N helpers per task group, resolving from code and listing only real owner decisions | other agents will execute the tasks, or any task is X or S |
| Record owner decisions in `inputs.md` and enforce them with a test | a later merge could silently undo the decision |

Route each task by the [run contract](../astrid-dev-shared/run-contract.md): N by default, X for coupled or non-obvious changes, S where correctness needs the deepest reasoning (a protocol that has never run end to end, security, data safety, migration). Give each task a scope: the paths, and any shared surface or contract, it may change. Tasks with overlapping scopes must be ordered by a dependency, including against other active projects; if a shared surface needs one model first, consult Advise. End the task list with the review row from the [tasks template](../../templates/project/tasks.md), placed before any publishing task, which depends on it. Recommend how many review rounds from the project's risk and complexity (the run contract gives a guide), say why, and record the owner's agreed number in `inputs.md`. With 0 rounds, leave the review row out.

## Readiness

A draft can explicitly mark what is **Pending** and the next action. A defined project needs genuine prior-art findings, an explained reuse decision, a traceable owner choice and meaningful completion evidence; a consequential design additionally needs critique or an explicit unresolved blocker. Don't make the agent fabricate evidence or add a heavyweight ritual to a straightforward decision.

Before implementation, tasks identify their actual base/donor revisions, dependencies, route (N/X/S where useful), exact focused checks and authority. The [run contract](../astrid-dev-shared/run-contract.md) alone owns routing, execution state and review policy. **Planning does not run product tests or start work unless asked.**
