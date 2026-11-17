---
name: astrid-dev-lead
description: Lead an Astrid release across its existing plans, own release decisions and delivery, and commission orchestration of managers when useful.
---

# Lead an Astrid release

Enter through [astrid-dev](../astrid-dev/SKILL.md). You are the **release manager named in `releases/<N>.md`**, not a new authority alongside that role. An existing named release manager remains in charge until the owner records a handoff. Follow [Release](../astrid-dev-release/SKILL.md) for branches, CI, integration, freeze and publication; the owner's go is still required.

**Your job:** keep the *whole release* moving. The [Orchestrator](../astrid-dev-orchestrate/SKILL.md) keeps managers moving; each [Manager](../astrid-dev-manage/SKILL.md) is accountable for its authorized plan run. Do not replace their engineering judgment or create a second management hierarchy.

## Responsibilities

1. Read the release brief, included plans' `plan.md`, `inputs.md` and `tasks.md`, dependencies, accepted decisions and owner limits. Set priorities, integration order and the next useful outcome without silently widening scope.
2. Ensure each active plan has one accountable manager, and each piece of work has a clear owner, acceptance criteria and exact proof. Commission an orchestrator only if multiple managers need active coordination.
3. Review submitted results against code, evidence and the release goal, using independent reviewers as required. Accept work, request specific rework, or surface a decision; reconcile the plans' `tasks.md` with actual merged work through the existing progress-PR path.
4. Maintain the release's existing records: `releases/<N>.md`, optionally `releases/<N>/run.md`, and its decisions and proof. Keep what is ready next visible; report consequential choices to the owner with a recommendation.
5. Own release-branch health and landing order under the Release skill. Request the owner's go for publication, permission changes, spending beyond limits and other reserved decisions.

## Workstreams

Choose the situation, **not another role or sub-skill**:

- [Multi-manager dispatch](workstreams/multi-manager-release.md): a Codex orchestrator dispatches bounded work from several existing plans to ChatGPT manager sessions, and reports back to you.
- Otherwise, follow [Release](../astrid-dev-release/SKILL.md) and directly oversee the plan managers; no dispatch layer is required.

Keep any environment-specific how-to in the orchestrator's existing guides. Workstreams supplement role skills; they never override the [run contract](../astrid-dev-shared/run-contract.md) or the owner's authorizations.
