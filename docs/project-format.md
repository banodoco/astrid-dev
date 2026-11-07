# Issues and project packs

[Start with Astrid's development skill](../skills/astrid-dev/SKILL.md) and the [contributor/writing workflow](contribution-workflow.md). **Bugs, small improvements, maintenance and documentation fixes belong in an issue or an existing task**, with a focused PR and evidence. They do not need a new project folder. Create a project only for an independently useful result that merits its own priority, owner, dependencies and completion criteria.

Each project uses one folder with three complementary files:

| File | Owns |
| --- | --- |
| [`plan.md`](../templates/project/plan.md) | What useful result, scope, existing foundation, sequence and completion proof |
| [`inputs.md`](../templates/project/inputs.md) | Why this approach: prior art, reuse/placement decision, any needed independent challenge, owner choice, source identities and limits |
| [`tasks.md`](../templates/project/tasks.md) | Bounded work, dependencies, focused checks, route and task progress |

The **handoff between projects** is a contract, not an extra file: name the actual prior output consumed, the artifact or behavior produced, and the exact proof that would let another agent use it. An unqualified dependency or a plan being marked done isn't sufficient evidence; link the accepted candidate and its receipt when available.

These are not three long forms. Drafts can state genuine unknowns; a defined scope must cite findings and the decision. The [planning skill](../skills/astrid-dev-plan/SKILL.md) scales scrutiny to actual risk. Existing accepted plans do not require another planning exercise because a different agent joins.

The [catalog](../plans/index.md) is the one authority for project status, priority, owner and estimate. Issues own small fixes and incidents; PRs contain the exact candidate and proof. Completing a project is not automatic evidence that its [vision gap](../vision/README.md) closed.

Add supporting designs, evidence or task cards only when several readers or tasks need them independently; [the website project](../plans/21-astrid-website/plan.md) is one example. Do not create empty parallel folder structures or duplicate status ledgers. For source ownership use the [domain map](../skills/astrid-dev/references/domains.md); for run identity, security, checks and reviews use the [shared contract](../skills/astrid-dev-shared/run-contract.md).
