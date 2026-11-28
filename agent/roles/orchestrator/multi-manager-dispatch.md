---
description: Run a lane's packets option: dispatch and supervise fresh ChatGPT packet sessions, with the orchestrator's review and merges as the lane brief sets them.
---

# dispatch to fresh ChatGPT sessions

## When to use

When a lane brief's How it runs names the `packets` option and the owner has launched its orchestrator under that brief.

## Outcome

Authorized units of the lane assigned and supervised through fresh ChatGPT packet sessions, each with an identified session and evidence, and reviewed and merged on the lane's terms.

## Inputs

The lane brief, the unit rows in each plan's `tasks.md`, the lane board and mailbox, session access, capacity and dispatch authority.

## Procedure

Run startup and resume checks, dispatch one packet per session, track check-ins and surface blocked work to the owner or the Lead, as the brief lists.

## Completion

Every dispatched packet has an identified session, current state and evidence or an explicit blocker; each one is reviewed and merged as the brief's Reviews and Merges say.

Use when a lane brief's How it runs names this option. The lane brief sets which plans and units it covers; the general [Orchestrate role](../orchestrator.md) still applies.

**Packets go only to a new normal chat in ChatGPT on the web:** open chatgpt.com in your browser, signed in to the owner's own account. Never ChatGPT for Work, never Codex. A Codex-app manager opens these chats by the steps in the [Codex-app guide](../../guides/codex-app/README.md).

**The packet's Route sets the session's mode, every time** (normal tasks N, hard X, very hard S): N High, X Extra High, S Pro ([run contract](../../shared/run-contract.md#chatgpt-session-modes)), never one mode for all or by feel. If a mode isn't offered, say so in STATUS and ask the owner.

**One packet, one fresh ChatGPT session.** The session writes its unit and shows its proof. **You** review, keep sessions moving and merge on green, as the lane brief's Merges says. Fixes are packet work: you diagnose and review, and a fix goes back to a packet session.

## Start

1. Read the lane brief, the unit rows in each plan's `tasks.md`, and the board. Confirm each unit's Depends, repository, PR destination (the brief's Branches), proof and authority (the brief's Roles).
2. Do the board's startup checks: the mailbox both ways ([protocol](../../guides/codex-cloud/README.md#establish-the-mailbox)), how sessions start and resume (a comment or session URL cannot wake one), how many ChatGPT sessions this account's subscription can run at once, and that **you** can clone, build the environment and run one focused test on a network-capable machine (packet sessions never do).
3. **Find every earlier manager or packet session** on this lane's plans. Stop any you can reach, name any you cannot for the owner, and list each one's branches and open pull requests with heads. You decide what each becomes within the brief; the Lead decides any release-level effect.
4. Dispatch the first packet alone: its early STATUS proves a packet session can push, open a pull request and comment. Each later packet's early STATUS proves its own repository.
5. Give each Ready packet a **new ChatGPT session** in its Route's mode with the [start message](#packet-start-message), and name it in your next STATUS; a packet's ID is its file name, or in a lane its unit's card IDs.

## Packet start message

When your brief has its own chat start message, send that one. This template is for releases with prepared packet files.

```text
You are the ChatGPT manager implementing ONE packet for Release <N>.
Follow agent/roles/manager/chatgpt-packet.md in banodoco/astrid-dev.
Lane brief: <brief path> at <SHA>; your units: <card IDs>, from each plan's tasks.md at <SHA>.
Packet: written at dispatch from those rows and posted on the board; its PR destination names your branches.
Authority: the lane brief's Roles and Merges at <SHA>, given by the owner.
Standing rulings: the brief's Standing rulings section; they bind you.
Board: <issue URL>, run <run id>, format in its first post. You are <mailbox name>;
the orchestrator is <name>.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply orchestrator decisions <comment IDs> not yet done.]
Write this packet's code and tests and push after each task; run its Proof command here if it names one; do not clone or build. Post STATUS or BLOCKED as comments on the board,
the first as soon as your first branch is pushed and its draft pull request open.
End with READY-PROOF <repo> <PR> <head> <selectors>, then stop.
Do not merge, tick tasks.md or start another packet.
```

You send it as the owner's message ([run contract](../../shared/run-contract.md#who-answers-for-a-run)). If you cannot start a session, give the owner a ready-to-paste prompt.

Releases that still have packet files use the earlier form: replace the lane brief and card-ID lines with `Packet: releases/<N>/packets/<id>.md at <SHA>; its PR destination names your branches.`

## Every hour

At each check-in (hourly, unless the brief sets another cadence), a pass relays submissions, resumes stalled sessions and starts Ready packets. If your own run ends, for example at the end of a ChatGPT agent window, say so in your last STATUS, with the text the owner pastes to resume you. Don't stop while your plan may still need packets.

1. **Read by cursor** ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)): the lane board, where every message about the lane's plans goes.
2. **Inspect every open packet** in the lane: Ready, Running, Review or Blocked. The branch, not the chat, shows health. No commit or STATUS for 3 hours: resume it. A chat that will not load after one reload, is silent 30 minutes after a resume, or is quiet for 6 hours is broken: replace it once its branch has not moved for 30 minutes, naming the head in the replacement's first message. Never two writers on one branch.
   **Proof turnaround.** Answer each `READY-PROOF` within 45 minutes. The author runs the focused proof and shows it in its pull request; green CI and the shown proof are the evidence. Run a proof yourself, side by side with others in background subagents, only when the shown one is missing or doubtful. Findings go back to the packet's session, or to a fresh session at its head; they never become a fix of yours ([fixes are packet work](../leader/lane-orchestrators.md#at-each-lead-check-in)). After a ruling, resume it if quiet for 30 minutes.
3. **Relay, then confirm.** A message is delivered when it shows in the chat or the session's next post answers it. Otherwise post it on the board to that session, resume the session, and mark it "unconfirmed" in STATUS.
4. **Act once where needed:** dispatch Ready packets to fresh sessions; nudge/resume stalled sessions; review submitted PRs as the brief's Reviews names, and send to the reviewer it names any that need one; relay rework to the same packet, never duplicated; escalate genuine technical/permission/dependency blockers; an environment block (no way to start, resume or push) is one BLOCKED naming the missing capability. Set Done only once the review the brief requires has accepted the unit. A review unanswered for 4 hours: send the reviewer a REQUEST and tell the owner.
5. **Post one hourly STATUS** on the lane board ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)): `acted on:` and `cursor:` lines, then a line per open packet with state, session, latest evidence (or no change) and next action. That STATUS, with `cursor:` your last processed comment, is the live record of handoffs and sessions. Packet handoff state lives there and in each plan's `tasks.md` Progress, not in a table in `run.md`.

If scheduling or resume is unverified, name the manual nudges.
