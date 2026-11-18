# Workstream: dispatch to fresh ChatGPT sessions

Use when the [Release Lead](../../astrid-dev-lead/SKILL.md) has prepared the [packet queue](../../astrid-dev-lead/workstreams/multi-manager-release.md) and the owner has authorized this Orchestrator. The general [Orchestrate role](../SKILL.md) still applies.

**One packet, one fresh ChatGPT session.** The packet session implements and submits; **you** keep sessions moving; **the Lead** reviews and integrates.

## Start

1. Read the board, its packets, their `tasks.md` rows and the mailbox issue. Confirm each packet's dependencies, repository, PR destination, proof and authority.
2. Do the board's startup checks: the mailbox both ways ([protocol](codex-cloud/README.md#establish-the-mailbox)), how sessions start and resume (a comment or session URL cannot wake one), and how many ChatGPT sessions this account's subscription can run at once. Tell the Lead if that is below the board's cap.
3. **Find every earlier manager or packet session** on this release's plans: stopped, stalled, broken or finished early. Stop any you can reach, name any you cannot for the owner, and list each one's branches and open pull requests with heads; the Lead decides what each becomes.
4. Dispatch the first packet alone: its early STATUS proves a packet session can push, open a pull request and comment. Each later packet's early STATUS proves its own repository.
5. Give each Ready packet a **new ChatGPT session** with the [start message](#packet-start-message), and name it in your next STATUS; a packet's ID is its file name.

## Packet start message

```text
You are the ChatGPT manager implementing ONE packet for Release <N>.
Follow skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md in banodoco/astrid-dev.
Packet: releases/<N>/packets/<id>.md at <SHA>; its PR destination names your branches.
Authority: the Authority section of releases/<N>/run.md at <SHA>, given by the owner.
Standing rulings: the same file's Standing rulings section; they bind you.
Mailbox: <issue URL>, run <run id>, format in its first post. You are <mailbox name>;
the Orchestrator is <name>; the Lead is <name>.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply Lead decisions <comment IDs> not yet done.]
Implement and prove this packet. Post STATUS or BLOCKED as comments on the mailbox issue,
the first as soon as your first branch is pushed and its draft pull request open.
Do not merge, tick tasks.md or start another packet.
```

You send it from the owner's account, as her message ([run contract](../../../shared/run-contract.md#who-answers-for-a-run)). If you cannot start a session, give the owner a ready-to-paste prompt and report the limitation.

## Every hour

1. **Read the mailbox** and ACK what is addressed to you.
2. **Inspect every open packet** in the release queue: Ready, Running, Review or Blocked. Check its messages, PRs and evidence since last time. The branch, not the chat, shows health. No commit or STATUS for 3 hours: resume it. A chat that will not load after one reload, gives no reply 30 minutes after a resume, or is quiet for 6 hours is broken. Replace it only once its branch has not moved for 30 minutes, from the branch head and last STATUS, and name that head in the replacement's first message. Never two writers on one branch.
3. **Relay, then confirm.** A message is delivered only when it shows in the chat or the session ACKs it. Otherwise, post it on the mailbox addressed to that session, then resume the session so it reads it; mark it "unconfirmed" in STATUS until it ACKs.
4. **Act once where needed:** dispatch Ready packets to fresh sessions; nudge/resume stalled sessions; pass submitted PRs and proof to the Lead as Review; relay rework to the same packet, never duplicated; escalate genuine technical/permission/dependency blockers; an environment block (no way to start, resume or push) is one BLOCKED naming the missing capability. Set Done only on the Lead's DONE. If a session cannot dispatch an authorized workflow on its own branch, dispatch it for the session. A Review unanswered for 4 hours: send the Lead a REQUEST and tell the owner.
5. **Post one hourly STATUS**: first an `acted on:` line naming each Lead message since the last STATUS and what you did about it, then a line per open packet with state, session, latest evidence (or no change) and next action. That STATUS, with `cursor:` your last processed comment, is the live record of handoffs and sessions; the Lead copies it to `run.md`. 

If scheduling or resume is unverified, name the manual nudges. End check-ins when dispatch ends.
