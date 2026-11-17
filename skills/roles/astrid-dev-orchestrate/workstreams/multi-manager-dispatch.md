# Workstream: dispatch to fresh ChatGPT sessions

Use when the [Release Lead](../../astrid-dev-lead/SKILL.md) has prepared the [packet queue](../../astrid-dev-lead/workstreams/multi-manager-release.md) and the owner has authorized this Orchestrator. The general [Orchestrate role](../SKILL.md) still applies.

**One packet, one fresh ChatGPT session.** The packet session implements and submits; **you** keep sessions moving; **the Lead** reviews and integrates.

## Start

1. Read the board, its packets, their `tasks.md` rows and the mailbox issue. Confirm each packet's dependencies, repository, PR destination, proof and authority.
2. Do the board's startup checks: the mailbox both ways ([protocol](codex-cloud/README.md#establish-the-mailbox)), and how sessions start and resume; a comment or session URL cannot wake one.
3. **Find every earlier manager or packet session** on this release's plans: stopped, stalled, broken or finished early. Stop any still running, and list each one's branches and open pull requests with heads in a STATUS; the Lead decides what each becomes.
4. For each Ready packet, launch a **new authorized ChatGPT session**, using the [short message](#packet-start-message), and name it in your next STATUS. A packet's ID is its file name.

## Packet start message

```text
You are the ChatGPT manager implementing ONE packet for Release <N>.
Follow skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md in banodoco/astrid-dev.
Packet: releases/<N>/packets/<id>.md at <SHA>; its PR destination names your branches.
Authority: the Authority section of releases/<N>/run.md at <SHA>, given by the owner.
Mailbox: <issue URL>, run <run id>, format in its first post. You are <mailbox name>;
the Orchestrator is <name>; the Lead is <name>.
[Replacing <prior session>: continue from <branch> and <last STATUS link>.]
Implement and prove this packet. Post STATUS or BLOCKED as comments on the mailbox issue.
Do not merge, tick tasks.md or start another packet.
```

You send it from the owner's account, as her message ([run contract](../../../shared/run-contract.md#who-answers-for-a-run)). If you cannot start a session, give the owner a ready-to-paste prompt and report the limitation.

## Every hour

1. **Read the mailbox** and acknowledge addressed requests, including Lead decisions and manager submissions.
2. **Inspect every open packet** in the release queue: Ready, Running, Review or Blocked. Check recent manager messages, PRs and evidence since last time. Running with no commit or STATUS for 3 hours: resume it; for 6 hours: replace it from its branch.
3. **Act once where needed:** dispatch Ready packets to fresh sessions; leave healthy Running work alone; nudge/resume stalled sessions; pass submitted PRs and proof to the Lead as Review; relay rework to the same packet (resume or replace its session, never duplicate the assignment); escalate genuine technical/permission/dependency blockers; an environment block (no way to start, resume or push) is one BLOCKED naming the missing capability. Set Done only on the Lead's DONE. A Review unanswered for 4 hours: send the Lead a REQUEST and tell the owner.
4. **Post one short hourly STATUS** in the same GitHub issue, attributed to your role/session: one line per open packet with state, session, latest evidence (or no change) and next action/request. That STATUS, with `cursor:` your last processed comment, is the live record of handoffs and sessions; the Lead copies it to `run.md`. 

A packet session reads the mailbox only on start, resume and hand-off. If scheduling or resume is unverified, name the manual nudges. End check-ins when dispatch ends.
