---
description: Execute one bounded engineering, research or review packet in a fresh ChatGPT session and push the authorized result for its accountable coordinator.
---

# execute one packet in ChatGPT

## When to use

When a fresh ChatGPT session receives one engineering, research or review packet with explicit scope, authority and destination from its authorized dispatch.

## Outcome

One bounded packet with its implementation or original evidence pushed to the assigned branch and handed off by exact commit.

## Inputs

The exact packet, applicable task rows or research/review question, board and current rulings, target repository, base, permitted paths, handoff and permissions.

## Procedure

Receive and verify the assignment, follow the engineering path or the evidence-only path below, and push the result with an exact-head mailbox handoff.

## Completion

Every assigned task or question has a traceable disposition, exact source and a remotely readable result, with no unauthorized merging or scope changes.

Use when a fresh ChatGPT session receives **one** accepted packet from the [Orchestrator](../orchestrator/multi-manager-dispatch.md). For engineering follow [Manage](../manager.md) and the existing implementation path below; the Lead owns review. For a commissioned research or review packet use the evidence-only path. **You do your own packet's work**; take no second packet and commission no other sessions unless explicitly authorized.

## Receive → implement → submit (engineering)

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

## Receive → investigate or judge → submit (evidence only)

Use when the assignment explicitly authorizes writing a report, not changing the product or the records being assessed. Apply [Scope a release](../../shared/workstreams/scope-release.md) or [Sense check](../../shared/workstreams/sense-check.md) as commissioned. The same one-packet, mode, source identity, mailbox, resume and authority rules apply; engineering-specific steps and READY-PROOF do not.

1. **Receive.** Read the pinned brief and applicable board authority, rulings, source register and prerequisite reports; verify the actual mode, question, report path, packet branch, exact starting commit and proposal PR destination. Keep the reviewed source/head distinct from the branch used to submit evidence. If a verdict is read-only with no report-write authority, do not infer it; ask for the authorized evidence destination or return the original through the named fallback.
2. **Investigate or judge.** Read actual sources and original evidence. Write one full original Markdown report answering the packet, including identities, limitations, findings and verification. Keep fact, inference and unverified claims distinct. A reviewer must not amend the proposed records, patch the candidate or approve execution. Only the named evidence file(s) are writable; no adjacent-edit exception. Do not test, build, clone, spend or dispatch CI unless separately authorized.
3. **Push your own report.** Use the GitHub connector on the packet's dedicated branch in astrid-dev. Open or continue the assigned draft evidence PR into the scoping proposal branch (not main, a product branch or an active delivery branch). Before a pause push genuine progress and post STATUS; never claim incomplete work is final. Post the early STATUS as soon as the first real report content and draft PR are pushed. Verify the exact remote head and report path by readback. Do not overwrite prior findings; a rework or superseding verdict is a new linked revision. Do not rebase, force-push or share a writable packet branch. Follow the named restricted-evidence path for confidential inputs; do not publish secrets, personal material or raw chats.
4. **Submit and stop.** Post `READY-REPORT <repo> <PR> <head> <report-path>` in the existing STATUS format, to the coordinator, naming the exact reviewed identities, limitations and any blocking finding. The report must be complete and readable at that head. This is delivery of evidence, not acceptance of its claims. The coordinator verifies the pushed report and makes it available to dependent sessions through immutable links; no chat transcript or coordinator transcription is required. Never merge the evidence PR yourself or change the shared evidence index, accepted scope, task progress or release authority. If connector write/readback or the mailbox fails, post BLOCKED with the exact failure and preserved report location; the coordinator may use an explicitly recorded manual intake of the complete original as a fallback.
