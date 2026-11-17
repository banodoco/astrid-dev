# Workstream: dispatch multiple release plans

Use when one Release Lead directs a Codex Orchestrator supervising ChatGPT managers across several already accepted plans. This is an **execution queue**, not a new kind of project, issue or release.

## Lead: set up once

1. Read `releases/<N>.md` and the included project packs. Partition eligible `tasks.md` work into **packets of at most about three human engineering days**. A packet is one task or a bounded set of task IDs, with outcome, dependencies, proof, branch/ref and permissions inherited from its plan. If the task card lacks those, improve it through the normal reviewed plan process before dispatch. Do not make a new plan or expand accepted scope.
2. Put a concise **Dispatch queue** in the existing `releases/<N>/run.md` (create it from the release template if needed). One row per packet: `ID | plan/tasks | estimate | Ready/Running/Review/Blocked/Done | manager session | next action/links`. Links lead to the canonical task cards, PRs and evidence. The queue tracks **handoff state**, not task completion; the plan's `tasks.md` remains the only engineering progress record.
3. For each plan, identify **one accountable plan manager** under the [run contract](../../astrid-dev-shared/run-contract.md#who-answers-for-a-run). A separate packet chat may implement bounded work for that manager, but does not become another accountable agent for the same run or independently integrate its plan. Record the integrator and how packet output returns to them. Do not start manager sessions without the owner's required go.
4. If separate chats need an asynchronous channel, designate **one coordination-only GitHub issue** for this release and link it from `run.md`. Use the existing [Codex Cloud mailbox format](../../astrid-dev-orchestrate/codex-cloud/README.md#establish-the-mailbox), with `from`, `from_session`, `to`, `to_session`, type, message ID, request and links. Acknowledgements and decisions are new comments. GitHub comments alone cannot wake a stopped chat.
5. Give the owner the release/queue/mailbox links and an exact **Orchestrator start message** to paste in an authorized session, specifying session, cadence, limits and when to escalate. Verify an hourly scheduler *and* session-resume mechanism before promising unattended check-ins.

## Lead: every hourly check-in

- Read and acknowledge addressed requests and newly submitted packets.
- Check commits, PRs, tests and independent review where required. **Only you accept a packet for the queue**, but the accountable plan manager remains responsible for the plan's integration and its `tasks.md` updates.
- Return insufficient work with one concrete next action; settle cross-plan dependencies and replenish Ready packets.
- Reconcile the queue with plan records and release branch state; log meaningful rulings in the release's existing `decisions.md`, not the mailbox.

## Issue boundary

**Do not open an Astrid-dev issue per packet or use issue labels as packet statuses.** Existing issues are reports, ideas and questions; their `plan:NN`/`release:NN` labels feed release intake. Link an existing issue from the relevant task when it concerns real product work. A coordination mailbox is transport only: identify it explicitly, do not label it `plan:NN`, `release:NN` or `planned`, and never treat its comments as scope approval or task instructions. It will still appear as an issue in ordinary issue views; keep it to one per release and close it when coordination ends.

## Orchestrator launch prompt

```text
You are the execution Orchestrator for Release <N>, supervised by the Release Lead
<session>. Follow astrid-dev-orchestrate and its multi-manager dispatch workstream.
Read releases/<N>.md and releases/<N>/run.md at <SHA>; mailbox: <issue URL>.
Dispatch only Ready packets linked to accepted tasks, using the recorded plan managers
and owner-approved ChatGPT sessions. Check every active session hourly through a
verified scheduler/resume path. Recover stalls, submit evidence for Lead review,
and ask the Lead about technical or cross-plan decisions. You may <authorized actions>;
you must escalate <reserved decisions>. Do not publish or accept work for the Lead.
```
