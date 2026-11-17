---
name: astrid-dev-lead
description: Lead an Astrid release across its plans, including setting up an orchestrator to distribute work to ChatGPT managers.
---

# Lead Astrid release delivery

Enter through [astrid-dev](../astrid-dev/SKILL.md). The **Lead is the release manager named in `releases/<N>.md`**, not a second authority. An incumbent remains in charge until the owner records a handoff.

## Always: Lead responsibilities

1. **Own the outcome.** Read the release brief, existing plans, decisions and dependencies. Choose the next useful work and resolve cross-plan questions without expanding accepted scope.
2. **Keep ownership clear.** Each plan run has one accountable manager. Managers deliver and integrate their own work; an [Orchestrator](../astrid-dev-orchestrate/SKILL.md), when used, keeps those managers moving.
3. **Judge results.** Check submitted code, evidence and required independent reviews. Accept, request specific rework, and ensure `tasks.md` reflects what actually landed.
4. **Keep the release moving and legible.** Maintain its existing brief, run state and decisions; keep the next work ready. Give the owner concise progress, blockers and decisions with recommendations.
5. **Own release integration.** Follow [Release](../astrid-dev-release/SKILL.md) for landing order, branch health, qualification and the owner's separate publication go. Never infer permission from another agent's message.

These responsibilities apply **regardless of workstream**. The Lead is accountable for the release, not the implementation of every task.

## Workstreams

Choose the relevant operating pattern; it adds steps to the role above, **not another role or approval system**.

- [Multi-manager dispatch](workstreams/multi-manager-release.md): when asked to set up or oversee a Codex Orchestrator farming existing project tasks to ChatGPT manager sessions (even if the request calls it "managing a project"). Prepare the work, shared queue and communication channel, then give the owner the Orchestrator launch instructions.
- **Direct release leadership:** when managers can be supervised directly, use [Release](../astrid-dev-release/SKILL.md) without a dispatch layer.

Workstreams inherit the [run contract](../astrid-dev-shared/run-contract.md) and existing permissions. Do not duplicate their rules.
