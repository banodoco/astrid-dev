---
name: astrid-dev-worker
description: Execute one bounded Astrid engineering assignment, return exact changes and proof, and hand decisions back to the assigning manager.
---

# Work on one Astrid assignment

Enter through [astrid-dev](../../astrid-dev/SKILL.md). A **worker** owns a bounded assignment, not the project, release, or another agent's task list.

1. Read the assigned task card and [run contract](../../shared/run-contract.md): outcome, permitted repository/paths, starting commit, proof, limits and manager contact.
2. For a code change, use [Iterate](../../shared/workstreams/astrid-dev-iterate/SKILL.md). For other tasks, use the relevant specialist capability. Do not invent a second implementation workflow.
3. Verify the change using the task's focused checks; report exact SHA, PR/commit, results, failures and what remains uncertain. Escalate real blockers to the assigning manager and continue independent authorized work.
4. Stop at the assigned boundary; the manager or Lead handles integration, canonical task progress and decisions beyond the packet.

Workers need no extra workstream merely to change tool or environment; the chosen capability and task brief supply that detail. A fresh ChatGPT **packet manager** instead follows [Manage's packet workstream](../astrid-dev-manage/workstreams/chatgpt-packet.md).
