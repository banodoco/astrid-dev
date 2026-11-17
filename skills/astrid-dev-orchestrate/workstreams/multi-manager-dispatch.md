# Workstream: dispatch ChatGPT managers

Use when a [Release Lead](../../astrid-dev-lead/SKILL.md) has prepared the [multi-manager queue](../../astrid-dev-lead/workstreams/multi-manager-release.md) and the owner has authorized this Orchestrator. The [Orchestrate role](../SKILL.md) always applies; this workstream specifies the **ChatGPT session and hourly loop**.

**Your job:** dispatch ready work, keep managers moving, and return results to the Lead. The Lead owns scope and acceptance; each plan still has **one accountable manager** for engineering and integration. By default, that ChatGPT manager implements its packets directly; additional parallel chats are bounded delegates. Do not redesign packets or take over implementation.

## Start once

1. Read `releases/<N>/run.md`, its packet briefs under `releases/<N>/packets/`, the linked plan `tasks.md`, and the **one coordination issue** linked from `run.md`. These are the queue, briefs, task truth and mailbox respectively.
2. Confirm the accountable manager, branch, scope, proof, dependencies and authorization for each Ready packet. Verify issue read/write and a message/acknowledgment with the Lead through the [existing mailbox protocol](../codex-cloud/README.md#establish-the-mailbox).
3. Start or reuse the plan's **authorized ChatGPT manager session**, giving it the packet link and [ChatGPT packet workstream](../../astrid-dev-manage/workstreams/chatgpt-packet.md). The launch message below supplies the whole routing contract; the packet and source tasks contain the engineering brief. One manager normally works through its plan's packets in turn, directly. An additional packet chat is a bounded delegate, not another accountable plan owner.
4. Record the session link and Running status in the release queue. Verify a working session-create/resume mechanism; **GitHub access or a chat URL alone is not one**.

### Short manager launch message

```text
You are the accountable manager for Plan <P> in Release <N> (or a bounded delegate
of manager <session>). Follow astrid-dev-manage and workstreams/chatgpt-packet.md.
Packet: releases/<N>/packets/<id>.md at <SHA>; source: plans/<P>/tasks.md.
Target task PRs at release/<N>/plan-<P> in the relevant product repos.
Mailbox: <issue URL>; Orchestrator: <session>; owner permissions: <run-start link>.
Implement and prove the packet. The accountable manager integrates task PRs and
updates tasks.md by its normal astrid-dev main progress PR. Post STATUS with
PRs/evidence to this mailbox for Lead review, or BLOCKED with the impediment.
Do not publish; follow existing authority, budgets and merge rules.
```

This message is routing, **not an owner's go**. The plan manager must have the owner's own authorization or an accepted committed allow rule before executing. Confirm that ChatGPT session creation/resume actually works; if not, return the ready-to-paste message to the owner.

## Every hour

1. **Read the mailbox** since the last acknowledged message, including replies from the Lead and managers. Acknowledge addressed requests; follow the [mailbox protocol](../codex-cloud/README.md) for session identity and replay.
2. **Check every open packet** in `run.md`: Ready, Running, Review and Blocked. Compare its manager report, session activity, PRs and proof since the previous check. A blocker is a reported impediment, unresolved dependency, repeated failed attempt or unreachable stopped session. No visible change for an hour alone calls for investigation, **not a blocked label**.
3. **Take the next action:** assign Ready work; leave moving work alone; nudge a quiet manager with one specific question/action; recover a stopped session if possible; or escalate a real technical, dependency or permission blocker to the Lead. Submitted work with linked task PRs, proof and the accountable manager's `tasks.md` progress PR goes to **Review**. Only mark **Done** after the Lead accepts and the plan records match. Return rejected packets for rework in the same manager session.
4. **Post one short hourly STATUS comment** in the *same coordination issue*, timestamped and attributed to your role/session: one line per open packet with `ID — state — session — latest evidence or no change — next action/ask`. Include requests to the Lead there. No separate hourly log, no repeated briefs. Update `run.md` **only when a handoff state, session or next action changes**, rereading its latest version to avoid conflicts.

## Manager contact and stopping

Each manager receives the **same mailbox issue**, checks messages addressed to its session on start/resume and at a milestone or before stopping, and posts a link-backed **STATUS** message on submission or a **BLOCKED** message when needed. Managers work from their plan's existing records; they are **not required to write hourly reports**. The Orchestrator is responsible for checking them hourly.

The hour is a check-in cadence, **not automatic session wake-up**. If scheduling and remote session resume are not verified, report the manual nudge needed and never claim unattended supervision. Stop check-ins when the authorized dispatch run ends.
