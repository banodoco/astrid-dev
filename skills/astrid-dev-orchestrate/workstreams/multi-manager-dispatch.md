# Workstream: dispatch ChatGPT managers

Use only when the Release Lead has prepared a release [dispatch queue](../../astrid-dev-lead/workstreams/multi-manager-release.md) and the owner has authorized this Codex orchestration session.

**Goal:** keep all assigned work moving. The Lead owns release priorities and packet acceptance; each accountable plan manager owns its plan run and integration. You supervise session liveness and handoffs, not product architecture or release decisions.

## Start

1. Read the release brief, `releases/<N>/run.md`, mailbox and linked `tasks.md` cards. Check owner permissions, starting commits, proof, dependencies and who is accountable for each plan.
2. For a Ready packet, launch or nudge an authorized ChatGPT manager session with the exact task IDs, accepted plan, environment, branch/ref, tests, limits, evidence expectations and [Manage](../../astrid-dev-manage/SKILL.md). If using a separate packet chat, give it a bounded assignment under its existing accountable plan manager; do not create a competing run owner.
3. Record the session link and Running status in `run.md`. One active packet per execution session. Do not rewrite task briefs in the mailbox.

## Every hour

1. Read new mailbox messages (including your own account's), acknowledge requests and reconcile the queue with linked PRs and manager reports.
2. For each Running or Blocked packet, identify concrete forward movement since the last check. If stalled, send **one specific next action**; recover or replace an unusable session with a durable link to its prior state. Never claim a GitHub message woke a session without verifying that it did.
3. Resolve ordinary assignment/environment friction. Escalate technical, scope or cross-plan blockers to the Lead with evidence and a requested decision. Owner-reserved actions still require the owner's go.
4. When a manager has submitted the named PRs and proof, mark **Review** (not Done) and ask the Lead for acceptance. Relay any rework. Mark **Done only after the Lead's acceptance** and the accountable plan manager's task record is reconciled.
5. Dispatch the next Ready packet and write a short, attributable status/request in the shared mailbox **only when something changed or needs action**.

Use the existing [Codex Cloud mailbox protocol](../codex-cloud/README.md#establish-the-mailbox) for `from`, `from_session`, `to`, `to_session`, `message_id`, type, request, acknowledgement and deduplication. One mailbox, one release queue, no parallel status file. If hourly execution or remote session resume is not supported, tell the owner what needs a manual nudge rather than claiming continuous monitoring.
