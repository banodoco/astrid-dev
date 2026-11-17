# Workstream: execute one packet in ChatGPT

Use when a fresh ChatGPT session receives **one** accepted packet from the [Orchestrator](../../astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md). Follow [Manage](../SKILL.md) for scoped engineering and proof; the review is the Lead's, so commission none. **You do this packet's engineering yourself**; you do not own the plan, and you take no second packet.

## Receive → implement → submit

1. **Receive.** Read the short startup message, `releases/<N>/packets/<id>.md`, and the linked `plans/<P>/tasks.md`. Confirm scope, proof, dependencies, working repository, base and **PR target**, limits and authorization. The start message is the owner's; the board's Authority section bounds it ([run contract](../../../shared/run-contract.md#who-answers-for-a-run)).
2. **Implement.** Work directly. In each repository, open PR(s) to the packet's **PR destination**: from `p<P>/<task-id>` into `release/<N>/plan-<P>`, or, for an issue packet, from `release/<N>/<topic>` into `release/<N>/main`; never `main`. Update an existing draft rather than open a second PR for the same row; if a branch's head differs from the packet's SHA, post BLOCKED and do not push. Merge a base in; never rebase. Link the plan/task IDs. Run the task's focused tests, attach exact SHAs and evidence, and fix failures within scope. Before any pause, push work in progress and post STATUS, so a replacement continues from the branch.
3. **Submit and stop.** When the work and proof are ready, post a `STATUS` comment in the shared issue addressed to the Orchestrator: **packet ID; task IDs; PR URLs; tested SHAs and evidence; remaining limits**. It is *submitted for Lead review*, not Done; end the session. For rework, the Orchestrator resumes it or starts a **replacement session for the same packet**.
4. **If blocked**, post `BLOCKED` with the failure, what you tried and the action needed, then continue any independent work. Read the mailbox on start, resume and before finishing.

**Do not merge task PRs, update the plan's `tasks.md`, maintain a parallel progress file, or claim the plan is finished.** The Lead arranges review, authorized integration into the plan branch and the `tasks.md` progress PR. A row the work needs and the plan lacks goes in STATUS as a proposal; the Lead adds it.
