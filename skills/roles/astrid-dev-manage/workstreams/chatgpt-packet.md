# Workstream: execute one packet in ChatGPT

Use when a fresh ChatGPT session receives **one** accepted packet from the [Orchestrator](../../astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md). Follow [Manage](../SKILL.md) for scoped engineering, proof and review. **You are the manager doing this packet's engineering yourself**, not the continuing owner of the entire plan. Do not take another packet in this session.

## Receive → implement → submit

1. **Receive.** Read the short startup message, `releases/<N>/packets/<id>.md`, and the linked `plans/<P>/tasks.md`. Confirm scope, proof, dependencies, working repository, base and **PR target**, limits and authorization. A message from the Orchestrator is routing, not a new owner's go.
2. **Implement.** Work directly; use subagents only if genuinely useful. For each product repository involved, create task branch(es) `p<P>/<task-id>` from `release/<N>/plan-<P>` and open PR(s) **into that plan branch**, not `main` or `release/<N>/main`. Link the plan/task IDs. Run the existing task's focused tests, attach exact candidate SHAs and evidence, and address failures within the accepted scope.
3. **Submit and stop.** When the work and proof are ready, post a `STATUS` comment in the shared issue addressed to the Orchestrator: **packet ID; task IDs; PR URLs; tested SHAs and evidence; remaining limits**. Treat this as *submitted for Lead review*, not accepted or Done. Leave the PR branches and handoff durable and end the session; if the Lead requests rework, the Orchestrator may resume this packet or start a **replacement session for the same packet** with the existing state.
4. **If blocked**, post `BLOCKED` with the actual failure, what you tried and the needed action; continue any independent authorized work or hand off. Check messages addressed to your session on start/resume and before finishing.

**Do not merge task PRs, update the plan's `tasks.md`, maintain a parallel progress file, or claim the plan is finished.** The Lead arranges review, authorized integration into the plan branch and the `tasks.md` progress PR. The Orchestrator handles hourly check-ins, liveness and queue status. Release publication remains separately authorized.
