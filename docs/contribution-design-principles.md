# Contribution design principles

> **Make good contributions easy, poor decisions difficult, and results independently verifiable—with the least machinery necessary.**

Astrid Dev is a shared knowledge and coordination layer for many contributors, typically **one accountable owner and one agent per project**. It should remain understandable to newcomers without constraining capable agents to unnecessary ceremony.

## Eight principles

1. **One understandable path.** Orient → Investigate → Decide → Build → Prove → Land. Enter at the first unresolved stage, reuse accepted decisions, and stop where the work requires. Specialist skills deepen a stage rather than create a competing process.
2. **One authoritative home per fact.** Keep status, owner and priority in the [project catalog](../plans/index.md); scope and inherited knowledge in the project pack; missing outcomes in the [gap records](../visions/gaps.md); product behavior in its product repository. Derive views or link sources, never maintain competing copies.
3. **Proportional rigor and competent judgment.** Small fixes belong in issues, independently useful outcomes in projects. Increase investigation, independent challenge and review with uncertainty, impact, cost and irreversibility—not with document type, word counts or a fixed number of agents.
4. **Reuse before invention.** Trace existing behavior and prior art, preserve qualified work, and justify replacing or extending it. Prefer a simpler implementation or an existing abstraction when it can meet the user outcome.
5. **Clear ownership, boundaries and handoffs.** One accountable owner per project; ownership can be relinquished or reassigned transparently. Each project states what it consumes, produces and proves so another agent can safely build on the result. Avoid a centralized agent scheduler.
6. **Evidence bound to actual claims.** Name the exact source/dependency identity, environment, check, observed result, relevant failures and unproven cases. Record models *actually used*, distinguishing runtime evidence from self-reporting or unknown identities. The review submission links original receipts; it is not another evidence database.
7. **Objective CI, independent judgment and explicit authority.** CI validates structures, relationships, transitions and checks it actually runs; it does **not** establish that a linked result proves a claim. Reviewers judge sufficiency and risks. Claiming, accepting scope, authorizing execution, admitting review, merging code, completing work and publishing are distinct decisions. Automation of bookkeeping must fail closed and never run untrusted code with merge credentials.
8. **Subtract before adding.** Templates ask only what helps the next agent act; drafts can be incomplete without pretending otherwise. Prefer existing skills, parsers and GitHub capabilities. Add a new state, document, role or validator only if it removes a real ambiguity or failure, and keep decisions reversible where practical.

## Where to apply them

The [contributor skill](../skills/astrid-dev/SKILL.md) owns entry and routing. The [contribution workflow](contribution-workflow.md) describes GitHub claims, proposals, reviews and completion; [maintainer setup](contribution-automation-setup.md) owns bot configuration. The [project format](project-format.md), [run contract](../skills/astrid-dev-shared/run-contract.md) and [repository rules](../AGENTS.md) own the actual work and safety boundaries.

**Before extending the system, ask:** Which concrete failure are we preventing? Is the fact already owned? Is this objectively checkable or a judgment? Could we remove something instead? Will a new contributor understand the next action without reconstructing a conversation?
