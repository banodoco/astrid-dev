---
description: Implement one bounded packet in a fresh ChatGPT session and return task pull requests and evidence for Lead review.
---

# execute one packet in ChatGPT

## When to use

When a fresh ChatGPT session is assigned an accepted packet with explicit scope and authority by the release dispatch.

## Outcome

One bounded packet implemented on draft task pull requests, ready for orchestrator proof and Lead review.

## Inputs

The exact packet, assigned task rows, board and current rulings, target repository and base, accepted proof and permissions.

## Procedure

Receive and verify the assignment, implement code and tests directly on the permitted branch, and submit the draft PR and exact-head proof handoff to the orchestrator.

## Completion

Every assigned task has a traceable disposition, exact candidate source and proof selectors, and a Lead-visible handoff without unauthorized merging.

Use when a fresh ChatGPT session receives **one** accepted packet from the [Orchestrator](../orchestrator/multi-manager-dispatch.md). Follow [Manage](../manager.md) for scoped engineering and proof; the review is the Lead's, so commission none. **You do this packet's engineering yourself**; you do not own the plan, and you take no second packet.

## Receive → implement → submit

0. **Check your mode** against your packet's Route ([ChatGPT session modes](../../shared/run-contract.md#chatgpt-session-modes)); if it differs, say so in your first STATUS.
1. **Receive.** Read your board and the Lead board ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)) for messages to you; do so again on every resume and before finishing. Then read the start message, the packet and its `tasks.md` rows, on astrid-dev `main` unless the packet names a branch. Confirm scope, proof, dependencies, working repository, base and **PR target**, limits and authorization. Startup confirms only what the connector does: read files, push a branch, open a draft PR, comment. The start message is the owner's; the board's Authority section bounds it and its Standing rulings bind you ([run contract](../../shared/run-contract.md#who-answers-for-a-run)).
2. **Implement.** Work directly, and link the plan/task IDs.
   - **Branches.** In each repository, open PR(s) to the packet's **PR destination**: from `p<P>/<task-id>` into `release/<N>/plan-<P>`, or, for an issue packet, from `release/<N>/<topic>` into `release/<N>/main`; never `main`. Cut a new branch from the PR destination's current head. Continue an existing draft rather than open a second PR; if its head differs from the one the board lists, post BLOCKED and do not push. Merge a base in; never rebase. Post an early STATUS once your first draft PR is open.
   - **Proof.** Write the code and its tests. Never clone, build, run tests, take timings or check the UI mode selector, and never need a real ComfyUI, GPU, installed build or catalog: the orchestrator runs the proof. Before `READY-PROOF`, merge the destination's current head ([land](../../shared/workstreams/release.md#how-a-release-runs)) and name it in STATUS.
   - **Scope.** The packet's **May touch** is yours. An adjacent edit of about 20 lines or fewer outside it, and not in **Must not touch**, is allowed without asking: list it in the PR body under "adjacent edits". Anything larger, or anything in Must not touch, is one BLOCKED with the exact list.
   - **Tests.** Change test setup and assertions only as the [run contract](../../shared/run-contract.md#checks-and-failure-repair) allows.
   - **Pins.** Put any pin change in its own commit and name it in STATUS; pins are not yours to approve.
   - **Pauses.** Before any pause, push work in progress and post STATUS.
3. **Submit and stop.** When code and tests are pushed on the draft PR, post `READY-PROOF <repo> <PR> <head> <selectors>` as a `STATUS` on your board, `to:` the Orchestrator, with the packet ID, task IDs, adjacent edits and remaining limits; then stop. It is not Done. A fix round is a resume with the orchestrator's findings, never a held BLOCKED; the Orchestrator may instead start a **replacement session for the same packet**.
4. **If blocked**, post `BLOCKED` with the failure, what you tried and the action needed; continue independent work.

**Do not merge, update `tasks.md` or claim the plan is finished:** those are the Lead's. A row the plan lacks goes in STATUS as a proposal.
