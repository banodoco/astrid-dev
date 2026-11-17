# Workstream: execute a release packet in ChatGPT

Use when an authorized ChatGPT session receives a packet from the [Orchestrator](../../astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md). Follow [Manage](../SKILL.md) for engineering, testing and reviews; this is only the **handoff**.

**Default:** one accountable plan manager per plan, executing its packets directly and in order. No extra workers are required. If another session helps the same plan in parallel, it is a bounded delegate: it returns code/PRs to the accountable manager, who alone integrates the plan and updates task progress.

## Receive → build → submit

1. **Receive.** Read the Orchestrator's short launch message, the packet at `releases/<N>/packets/<id>.md`, and its source `plans/<P>/tasks.md`. Confirm task IDs, scope, proof, dependencies, authorized starting ref, target repository/branch and limits. Ask the Orchestrator about missing routing information; a relayed message never supplies missing owner permission.
2. **Build.** Work directly, or delegate only where useful. In each changed **product repo**, create the appropriate task branch `p<P>/<task-id>` from `release/<N>/plan-<P>`; open PR(s) **targeting that plan branch**, not `main` or `release/<N>/main`. Link the plan and task IDs. Run the focused proof and review required by the existing task and Manage rules.
3. **Land and record.** The accountable plan manager reviews and lands authorized task PRs in its **plan branch**, then updates the corresponding `tasks.md` rows through a **separate tasks.md-only progress PR into astrid-dev `main`** using Manage's established rules. Do not tick tasks merely because a PR opened. A delegate instead submits the PRs/evidence to the accountable manager and does **not** update `tasks.md`.
4. **Submit.** Post one `STATUS` message in the shared GitHub issue addressed to the Orchestrator: packet ID, source tasks, landed PRs/SHAs, tests/review evidence, progress PR and anything unfinished. This means **ready for Lead acceptance**, not Done. Remain available for concrete rework or leave a durable handoff if the session must end. After the Lead accepts and the task record is reconciled, the Orchestrator marks the packet Done.

If blocked, post `BLOCKED` with the exact impediment, what was tried and the next needed decision; continue unrelated authorized work. Check the shared issue for messages to your session on start/resume, at milestones and before stopping. **No hourly report and no second packet log:** the Orchestrator owns the hourly check-in and release queue. A plan's final completion and release publication still follow their existing separate gates.
