---
name: astrid-dev-plan
description: Define independently useful new Astrid project scope by reusing prior art, challenging consequential choices, and recording a verifiable end state.
---

# Plan a new Astrid project

Enter through [astrid-dev](../astrid-dev/SKILL.md) and its [domain map](../astrid-dev/references/domains.md). **Bugs, small fixes and maintenance normally belong in issues, not projects.** Existing project tasks use their accepted plan. This process is for a new, separately useful outcome that merits its own priority, owner and completion proof.

Planning is a decision, **not** authority to execute or release. Preserve earlier accepted scope and avoid repeated owner sign-offs.

## Investigate, decide, preserve

1. **Find prior art.** Search the affected source, existing issues, [plans](../../plans/index.md), [gaps](../../visions/README.md), and external approaches where relevant. Trace input → actual implementation → user-visible result, including useful source revisions, reuse opportunities, negative findings and uncertainties. Delegate bounded research when helpful; don't commission a broad audit without a decision it could change.
2. **Pick the smallest complete result.** Compare reusing or extending an existing pack, adding a pack, changing core, and doing less or nothing when relevant. Prefer an existing plan or gap to a new entry. Explain the chosen placement and tradeoffs from evidence, not a general architectural preference.
3. **Challenge proportional to consequence.** For material architecture, cross-repository contracts, expensive or difficult-to-reverse decisions, use a **distinct high-judgment** critic to identify real removals, consolidation and reuse. Record its findings and what you accepted or rejected. For a simple bounded project, a concise alternatives review and a reason not to commission a second planner is enough. Offer as many meaningful end-state alternatives as the owner needs; **ten are a useful exploration technique, not a quota**.
4. **Agree the outcome once.** Present the real options, their user-facing tradeoffs and a testable end state. Record the owner's actual selection with a traceable source. Creating a draft project or receiving no objection is not approval.
5. **Leave a compact handoff.** [`inputs.md`](../../templates/project/inputs.md) owns the source evidence, alternatives, challenge decision, approval and uncertainty. [`plan.md`](../../templates/project/plan.md) owns outcome, scope, sequence and completion. [`tasks.md`](../../templates/project/tasks.md) owns assignments and focused proof. Link to detailed work only when it has a distinct use; do not copy reasoning across all three files.

## Readiness

A draft can explicitly mark what is **Pending** and the next action. A defined project needs genuine prior-art findings, an explained reuse decision, a traceable owner choice and meaningful completion evidence; a consequential design additionally needs critique or an explicit unresolved blocker. Don't make the agent fabricate evidence or add a heavyweight ritual to a straightforward decision.

Before implementation, tasks identify their actual base/donor revisions, dependencies, route (N/X/S where useful), exact focused checks and authority. The [run contract](../astrid-dev-shared/run-contract.md) alone owns routing, execution state and review policy. **Planning does not run product tests or start work unless asked.**
