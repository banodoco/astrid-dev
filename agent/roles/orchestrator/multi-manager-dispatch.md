---
description: Dispatch and supervise Lead-approved packets in fresh ChatGPT sessions while leaving review and integration to the Lead.
---

# dispatch to fresh ChatGPT sessions

## When to use

When the Release Lead has prepared a packet queue and an owner has authorized the Orchestrator to dispatch it.

## Outcome

Authorized release packets assigned and supervised through fresh ChatGPT sessions with a reliable Lead handoff.

## Inputs

The live run board, accepted packet briefs, task rows, mailbox, session access, capacity and dispatch authority.

## Procedure

Run startup and resume checks, dispatch one packet per session, track check-ins and surface blocked work for Lead decisions.

## Completion

Every dispatched packet has an identified session, current state and evidence or an explicit blocker; the Lead retains review and integration.

Use when the [Release Lead](../leader.md) has prepared the [packet queue](../leader/multi-manager-release.md) and the owner has authorized this Orchestrator. The general [Orchestrate role](../orchestrator.md) still applies.

**Packets go only to a new normal chat in the ordinary ChatGPT app,** in the owner's own account: never ChatGPT for Work, never Codex.

**The packet's Route sets the session's mode, every time** (normal tasks N, hard X, very hard S): N High, X Extra High, S Pro ([run contract](../../shared/run-contract.md#chatgpt-session-modes)), never one mode for all or by feel. If a mode isn't offered, say so in STATUS and ask the Lead.

**One packet, one fresh ChatGPT session.** The session writes; **you** run proof and keep sessions moving; **the Lead** reviews and integrates.

## Start

1. Read the board, its packets, their `tasks.md` rows and your board. Confirm each packet's dependencies, repository, PR destination, proof and authority.
2. Do the board's startup checks: the mailbox both ways ([protocol](../../guides/codex-cloud/README.md#establish-the-mailbox)), how sessions start and resume (a comment or session URL cannot wake one), how many ChatGPT sessions this account's subscription can run at once, and that **you** can clone, build the environment and run one focused test on a network-capable machine (packet sessions never do).
3. **Find every earlier manager or packet session** on this release's plans. Stop any you can reach, name any you cannot for the owner, and list each one's branches and open pull requests with heads; the Lead decides what each becomes.
4. Dispatch the first packet alone: its early STATUS proves a packet session can push, open a pull request and comment. Each later packet's early STATUS proves its own repository.
5. Give each Ready packet a **new ChatGPT session** in its Route's mode with the [start message](#packet-start-message), and name it in your next STATUS; a packet's ID is its file name.

## Packet start message

```text
You are the ChatGPT manager implementing ONE packet for Release <N>.
Follow agent/roles/manager/chatgpt-packet.md in banodoco/astrid-dev.
Packet: releases/<N>/packets/<id>.md at <SHA>; its PR destination names your branches.
Authority: the Authority section of releases/<N>/run.md at <SHA>, given by the owner.
Standing rulings: the same file's Standing rulings section; they bind you.
Board: <issue URL>, run <run id>, format in its first post. You are <mailbox name>;
the Orchestrator is <name>; the Lead is <name>.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply Lead decisions <comment IDs> not yet done.]
Write this packet's code and tests and push after each task; run its Proof command here if it names one; do not clone or build. Post STATUS or BLOCKED as comments on the board,
the first as soon as your first branch is pushed and its draft pull request open.
End with READY-PROOF <repo> <PR> <head> <selectors>, then stop.
Do not merge, tick tasks.md or start another packet.
```

You send it as the owner's message ([run contract](../../shared/run-contract.md#who-answers-for-a-run)). If you cannot start a session, give her a ready-to-paste prompt.

## Every hour

Every 20 minutes while a packet is Running or in Review, a short pass relays submissions, resumes stalled sessions and starts Ready packets. The STATUS stays hourly. If your own run ends, for example at the end of a ChatGPT agent window, say so in your last STATUS, with the text the owner pastes to resume you. Don't stop while your plan may still need packets.

1. **Read by cursor** ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)): your board, and your parent's board for messages to you.
2. **Inspect every open packet** in the release queue: Ready, Running, Review or Blocked. The branch, not the chat, shows health. No commit or STATUS for 3 hours: resume it. A chat that will not load after one reload, is silent 30 minutes after a resume, or is quiet for 6 hours is broken: replace it once its branch has not moved for 30 minutes, naming the head in the replacement's first message. Never two writers on one branch.
   **Proof turnaround.** Answer each `READY-PROOF` within 45 minutes, running independent proofs side by side in background subagents, not one box in turn. You run the proof. Findings go back to the packet's session, or to a fresh session at its head; they never become a fix of yours ([fixes are packet work](../leader/multi-manager-release.md#at-each-lead-check-in)). After a ruling, resume it if quiet for 30 minutes.
3. **Relay, then confirm.** A message is delivered when it shows in the chat or the session's next post answers it. Otherwise post it on the board to that session, resume the session, and mark it "unconfirmed" in STATUS.
4. **Act once where needed:** dispatch Ready packets to fresh sessions; nudge/resume stalled sessions; pass submitted PRs and proof to the Lead as Review; relay rework to the same packet, never duplicated; escalate genuine technical/permission/dependency blockers; an environment block (no way to start, resume or push) is one BLOCKED naming the missing capability. Set Done only on the Lead's DONE. A Review unanswered for 4 hours: send the Lead a REQUEST and tell the owner.
5. **Post one hourly STATUS** on your board ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)): `acted on:` and `cursor:` lines, then a line per open packet with state, session, latest evidence (or no change) and next action. That STATUS, with `cursor:` your last processed comment, is the live record of handoffs and sessions; the Lead copies it to `run.md`. 

If scheduling or resume is unverified, name the manual nudges.
