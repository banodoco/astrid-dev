# Workstream: dispatch to fresh ChatGPT sessions

Use when the [Release Lead](../../astrid-dev-lead/SKILL.md) has prepared the [packet queue](../../astrid-dev-lead/workstreams/multi-manager-release.md) and the owner has authorized this Orchestrator. The general [Orchestrate role](../SKILL.md) still applies.

**One packet = one fresh ChatGPT session.** Never give successive packets to a continuing manager. The packet manager implements and submits; **you** dispatch and keep sessions moving; **the Lead** reviews, integrates and reconciles plan tasks.

## Start

1. Read `releases/<N>/run.md`, the linked `releases/<N>/packets/<id>.md` and source `tasks.md`, plus the **one GitHub coordination issue** linked from the release board. Confirm each packet's dependencies, product repo, PR target, proof and authorization.
2. Verify the mailbox by exchanging a message and ACK with the Lead using the [existing protocol](../codex-cloud/README.md#establish-the-mailbox). Verify how ChatGPT sessions can be started/resumed; a GitHub comment or session URL alone cannot wake one.
3. For each Ready packet, launch a **new authorized ChatGPT session**, using the [short message](#packet-start-message), and link it in the queue. Do not make an ongoing plan manager or ask the packet session to take the next packet.

## Packet start message

```text
You are the ChatGPT manager implementing ONE packet for Release <N>.
Follow astrid-dev-manage and workstreams/chatgpt-packet.md.
Packet: releases/<N>/packets/<id>.md at <SHA>.
Source plan/tasks: <path>; working product repo(s): <repos>.
Start from the named plan branch; PRs target release/<N>/plan-<P>.
Owner authorization/limits: <exact recorded authority or requirement>.
Mailbox: <issue URL>; Orchestrator session: <id>.
Implement and prove this packet. Open task PRs to the plan branch.
Post STATUS with PRs, SHAs and evidence here when submitted, or BLOCKED
with the impediment. Do not merge, tick tasks.md or start another packet.
```

This message is not a substitute for the owner's own session authorization or a committed allow rule. If you cannot start an authorized session, give the owner a ready-to-paste prompt and report the limitation.

## Every hour

1. **Read the mailbox** and acknowledge addressed requests, including Lead decisions and manager submissions.
2. **Inspect every open packet** in the release queue: Ready, Running, Review or Blocked. Check recent manager messages, PRs and evidence since last time. One quiet hour calls for a check, not an automatic blocker.
3. **Act once where needed:** dispatch Ready packets to fresh sessions; leave healthy Running work alone; nudge/resume stalled sessions; pass submitted PRs and proof to the Lead as Review; relay rework to the same packet (resume or replace its session, never duplicate the assignment); escalate genuine technical/permission/dependency blockers. Set Done **only after** the Lead confirms acceptance, landing and `tasks.md` reconciliation.
4. **Post one short hourly STATUS** in the same GitHub issue, attributed to your role/session: one line per open packet with state, session, latest evidence (or no change) and next action/request. Update `run.md` only when handoff state, session or next action changes. No separate log and no hourly paperwork for packet managers.

The manager only checks mailbox messages on start/resume and before handing off. If hourly scheduling or session resume is unverified, state what manual nudges are required; do not claim unattended operation. End check-ins when dispatch ends.
