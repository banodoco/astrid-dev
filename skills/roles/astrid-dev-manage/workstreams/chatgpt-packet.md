---
description: Implement one bounded packet in a fresh ChatGPT session and return task pull requests and evidence for Lead review.
---

# Workstream: execute one packet in ChatGPT

Use when a fresh ChatGPT session receives **one** accepted packet from the [Orchestrator](../../astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md). Follow [Manage](../SKILL.md) for scoped engineering and proof; the review is the Lead's, so commission none. **You do this packet's engineering yourself**; you do not own the plan, and you take no second packet.

## Receive → implement → submit

1. **Receive.** Read the mailbox for messages to you; do so again on every resume and before finishing. Then read the start message, the packet and its `tasks.md` rows, on astrid-dev `main` unless the packet names a branch. Confirm scope, proof, dependencies, working repository, base and **PR target**, limits and authorization. The start message is the owner's; the board's Authority section bounds it and its Standing rulings bind you ([run contract](../../../shared/run-contract.md#who-answers-for-a-run)).
2. **Implement.** Work directly, and link the plan/task IDs.
   - **Branches.** In each repository, open PR(s) to the packet's **PR destination**: from `p<P>/<task-id>` into `release/<N>/plan-<P>`, or, for an issue packet, from `release/<N>/<topic>` into `release/<N>/main`; never `main`. Cut a new branch from the PR destination's current head. Continue an existing draft rather than open a second PR; if its head differs from the one the board lists, post BLOCKED and do not push. Merge a base in; never rebase. Post an early STATUS once your first branch is pushed and its draft PR open.
   - **Proof.** Run the task's focused tests (for a document, its card's proof), attach exact SHAs and evidence, and fix failures within scope. Compare failures with the base by test ID, never by count, and tell a suspected flip by isolated runs, never by rerunning until green ([Green 3A](../../../capabilities/astrid-dev-green/SKILL.md#3a-no-new-failures), step 6). Before final proof, merge the destination's current head ([land](../../../capabilities/astrid-dev-release/SKILL.md#how-a-release-runs)) and name it in STATUS. Before starting a hosted run, check none is running on your branch: a new one cancels it.
   - **Pins.** Put any pin change in its own commit and name it in STATUS; pins are not yours to approve.
   - **Pauses.** Before any pause, push work in progress and post STATUS, so a replacement continues from the branch.
3. **Submit and stop.** When the work and proof are ready, post a `STATUS` comment in the shared issue addressed to the Orchestrator: **packet ID; task IDs; PR URLs; tested SHAs and evidence; remaining limits**. It is *submitted for Lead review*, not Done; end the session. For rework, the Orchestrator resumes it or starts a **replacement session for the same packet**.
4. **If blocked**, post `BLOCKED` with the failure, what you tried and the action needed, then continue any independent work.

**Do not merge, update `tasks.md`, keep a parallel progress file or claim the plan is finished:** review, integration and `tasks.md` are the Lead's. A row the work needs and the plan lacks goes in STATUS as a proposal; the Lead adds it.
