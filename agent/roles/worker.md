---
description: Execute one bounded Astrid engineering assignment, return exact changes and proof, and hand decisions back to the assigning manager.
skill: true
---

# Worker

## Responsibility

Complete one authorized bounded assignment.

## Authority

Do not own a whole project, release or another task.

## Responsibilities

Apply the scoped procedure and preserve test outcomes.

## Handoff

Return tested changes to the assigning manager.

Enter through [astrid-dev](../start.md). A **worker** owns a bounded assignment, not the project, release, or another agent's task list.

1. Read the assigned task card and [run contract](../shared/run-contract.md): outcome, permitted repository/paths, starting commit, proof, limits and manager contact.
2. For a code change, use [Iterate](../shared/workstreams/iterate.md). For other tasks, use the relevant shared workstream. Do not invent a second implementation workflow.
3. Verify the change using the task's focused checks (a subagent leaves them to its creator, who runs them on its commit); commit your work and report the exact SHA, and the PR if you are a worker session, with results, failures and what remains uncertain. Escalate real blockers to the assigning manager and continue independent authorized work. Return the way [start-session step 7](../shared/workstreams/start-session.md#procedure) says: what you push or hand back, BLOCKED for a file outside Scope, and no check-in.
4. Stop at the assigned boundary; the manager or Lead handles integration, canonical task progress and decisions beyond the packet.

Workers need no extra workstream merely to change tool or environment; the chosen workstream and task brief supply that detail. A fresh ChatGPT **packet manager** instead follows [Manage's packet workstream](manager/chatgpt-packet.md).

## Shared workstreams

Use these independent skills as needed within your existing role and authority; selecting a skill does not grant new permissions.

Choose from the [shared workstream index](../README.md#shared-workstreams) only within the assigned role and run permissions. The procedures do not grant new authority.
