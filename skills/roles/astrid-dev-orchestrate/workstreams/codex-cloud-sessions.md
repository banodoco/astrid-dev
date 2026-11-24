---
description: Coordinate separate Codex Cloud sessions through the shared GitHub mailbox and durable session handoffs.
---

# Workstream: separate Codex Cloud sessions

## Workstream contract

**Outcome:** Separate Codex Cloud sessions coordinated through one durable mailbox, with ownership and handoffs preserved.
**When to use:** When an authorized Orchestrator and plan manager work in different Codex Cloud chats.
**Inputs:** An accepted plan, named accountable manager, permitted session identities, mailbox, task boundaries and tested resume mechanism.
**Procedure:** Register sessions, send bounded briefs, reconcile their evidence and recover stalled work using the linked Codex Cloud guide.
**Completion:** The manager has a complete session handoff and traceable task evidence; unwakeable sessions are reported rather than assumed active.

Choose this when the orchestrator and plan managers work in **different Codex Cloud chats**. For the actual mailbox commands, session registration, authentication limits, acknowledgments, polling and recovery use the existing [Codex Cloud guide](codex-cloud/README.md); its scripts remain in that directory.

1. Start from an accepted plan and its authorized `Run start`; name **one accountable plan manager**. Use the plan's board ([rules](../../../shared/run-contract.md#coordination-boards-and-check-ins)) and agree durable per-session identities and cursors.
2. Give each session the plan/task links, exact proof, branches, limits and its manager/advisor roles. Follow [Manage](../../astrid-dev-manage/SKILL.md) inside the accountable manager session.
3. Follow the agreed check-in cadence to reconcile GitHub evidence and recover stalled sessions; a GitHub comment or timer alone **cannot wake** an idle Codex Cloud chat. Do not promise unattended progress without a verified resume mechanism.

When a Release Lead has prepared multiple packet briefs, combine this environment workstream with [multi-manager dispatch](multi-manager-dispatch.md). The dispatch board and packet files still live under the release, not in GitHub issue bodies.
