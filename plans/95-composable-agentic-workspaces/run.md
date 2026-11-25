# Plan 95 run board — Otto

The live state of Plan 95's run, rewritten by the orchestrator at each check-in. The plan's [`tasks.md`](tasks.md) stays the record of progress; this board holds the authority, the rulings and the packet queue. Packets are in [packets/](packets/).

## Now (19:15 UTC, Wed 25 Nov)

Plans 71, 72 and 73 are on `main` (`7cf00a5ed5ded3f4ca1b34b97214d693ab584fdd`). The Otto repository `banodoco/otto` exists, public and empty, and the orchestrator has push access. Ready: P95-03 (Otto package skeleton), P95-04 (contract design, Pro) and P95-15 (rule-preservation map, Pro), after the orchestrator's OT-1 and OT-2 are posted. The manager checks in **every 20 minutes** while any packet is Running or in Review, and hourly when idle.

## Authority

On 25 November 2026, in orchestrator session `session_011EzfW1Urc5P4hpm2SvVy5d`, the owner approved Plan 95 to run once Plans 71–73 were on `main`, decided D2 to D5 ([inputs](inputs.md#owner-decisions)), and said the plan should simply run. The owner-authorized dev-tooling exception covers astrid-dev, the public `banodoco/otto` and the private `banodoco/astrid-marketing`, and nothing else: no product repository, no Astrid release, no publication or spend.

- **Orchestrator** (`p71-73-orchestrator`, Claude session `session_011EzfW1Urc5P4hpm2SvVy5d`): the accountable agent. It takes the Lead's part of the [packet workstream](../../agent/roles/leader/multi-manager-release.md): it writes and orders packets, runs every proof, merges accepted PRs into Otto `main` (Otto cards) or `project/95-otto` (astrid-dev cards), keeps `tasks.md` true through progress PRs, commissions RS1 and R, and cuts Otto `v0.x` tags after the integrated proof passes. Merges into astrid-dev `main` need the owner's go, given when the plan is complete.
- **Manager** (`p95-manager-1`): a ChatGPT session in the owner's account, started by her launch message. It takes the Orchestrator's part of [multi-manager dispatch](../../agent/roles/orchestrator/multi-manager-dispatch.md), with this plan's orchestrator as "the Lead". It may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. It does not edit the repository, merge, approve or dispatch hosted CI.
- **Packet sessions** (`p95-<packet>-<n>`): may push to the `p95/<card id>` branch their packet names (in Otto or in astrid-dev, as the packet says), open pull requests, and comment on the mailbox. They never merge, never edit `tasks.md` or this board, never rebase a shared branch and never take a second packet. Their mode follows the packet's Route: N High, X Extra High, S Pro ([run contract](../../agent/shared/run-contract.md#chatgpt-session-modes)).
- **Stays in the orchestrator's lane:** OT-1, OT-2, OT-22, OT-23, RS1, R and every proof, build, tag and install.
- **Needs the owner:** the merge of `project/95-otto` into astrid-dev `main` (OT-24); installing generated skills on anyone's real machine or session; publishing; anything paid; changing an existing test's assertion in astrid-dev.

## Standing rulings

1. **Functions, not files, conflict.** Different functions or sections in one file are not a conflict between packets; the same function, section or new test table is.
2. **Proof runs where the network is.** Packet sessions write code and tests and end with `READY-PROOF <repo> <PR> <head> <selectors>`; the orchestrator runs the repository's checks and tests on the exact head and posts the result. Otto cards: `python3 -m unittest discover -s tests`. astrid-dev cards: `python3 scripts/astrid_dev.py check` and the full unit suite.
3. **Destinations.** Otto cards: `p95/<card id>` into Otto `main`. astrid-dev cards: `p95/<card id>` into `project/95-otto` (cut from `main`). Merge, never rebase; post BLOCKED if the board lists a different head for an existing draft.
4. **Dependants wait only for the cards they depend on.**
5. **Reviews.** The orchestrator reviews ordinary submissions itself. RS1 (the contract, after OT-4, one round) and R (the end, one round) are read-only **Pro** sessions in normal ChatGPT Chat on the orchestrator's REQUEST (packet [P95-RV](packets/P95-RV.md)); the manager starts a fresh session for each REQUEST. There is no sense check SC (owner, 25 November 2026).
6. **Cap:** at most three packets Running or Review at once (raised from two on 25 November 2026: the critical-path packets P95-04, P95-05 and P95-06 touch disjoint files and repositories). The first packet went alone and proved a session can push to Otto, open a draft PR and comment.
7. **Sessions:** packet sessions run in a normal ChatGPT Chat, not Work. One writer per branch: replace a stopped session only after its branch has been still for 30 minutes.
8. **Plan records:** `plans/95-composable-agentic-workspaces/*.md` change on `main` only through the orchestrator's progress PRs. A packet may add only the evidence file its packet names.
9. **Otto is public:** nothing private goes into it, and no secret is configured in its CI. Plan 96's Marketing data never goes into Otto.
10. **Cadence:** the manager checks in every 20 minutes while a packet is Running or in Review (relay submissions, resume stalled sessions, dispatch Ready packets) and hourly when idle.

## Mailbox

[astrid-dev #1886](https://github.com/banodoco/astrid-dev/issues/1886), run `p95-otto`, format in its first post.

| Role | Mailbox name | Session | Last processed comment |
|---|---|---|---|
| Orchestrator | `p71-73-orchestrator` | `session_011EzfW1Urc5P4hpm2SvVy5d` | — |
| Manager | `p95-manager-1` | named in its first STATUS | — |
| Packet session | `p95-<packet>-<n>` | from the manager's STATUS | — |

## When a session goes quiet

- **A packet session:** the manager resumes it after 3 hours with no commit or STATUS, and replaces it as the [dispatch workstream](../../agent/roles/orchestrator/multi-manager-dispatch.md) says.
- **The manager:** the orchestrator nudges it at 2 hours; at 3 hours it tells the owner, who starts `p95-manager-2` from the launch message below.
- **A READY-PROOF** unanswered for 45 minutes, or a Review for 4 hours: the manager sends the orchestrator a REQUEST and tells the owner.

## Manager startup checks

Post one STATUS with each as passed or failed; dispatch nothing until the orchestrator's DECISION answers it.

1. **Mailbox both ways:** read #1886, post one non-sensitive ACK, see the orchestrator's reply.
2. **Branches:** `banodoco/otto` exists (public, `main` has its first commit) and no `p95/*` branch exists that this board does not list.
3. **GitHub for packet sessions in Otto:** the ChatGPT GitHub connector can push a branch to, and open a draft pull request in, `banodoco/otto` as well as astrid-dev. If it cannot, that is a manual step for the owner, written in the STATUS.
4. **A fresh ChatGPT session** in each mode a Ready packet needs (High, Extra High, Pro) and the hourly reminder; then the 20-minute reminder while packets run.
5. **Capacity:** how many ChatGPT sessions the account can run at once, and whether Extra High and Pro are offered.

## Dispatch queue

Cap: three Running or Review at once (ruling 6). Priority: P95-09 (critical path), then P95-17, P95-12.

| Packet brief | Source tasks | Handoff | Session | Mode and next action |
|---|---|---|---|---|
| [P95-03](packets/P95-03.md) Otto package skeleton and CLI | OT-3 | Ready after OT-2 | — | High. First packet, alone; Otto repository |
| [P95-04](packets/P95-04.md) Contract design | OT-4 | Ready after OT-1 | — | Pro. After P95-03's early STATUS |
| [P95-15](packets/P95-15.md) Rule-preservation map | OT-15 | Ready after OT-1 | — | Pro. Beside P95-04 within the cap |
| [P95-05](packets/P95-05.md) Lift the Markdown, Git, check and view engines | OT-5 | Ready (OT-3 merged; Otto main `ef946b9d`) | — | High. Beside P95-04 and P95-06 |
| [P95-06](packets/P95-06.md) Lift the skill reader, builder and installer | OT-6 | Ready (OT-3 merged; Otto main `ef946b9d`) | — | Extra High. Beside P95-04 and P95-05 |
| [P95-07](packets/P95-07.md) Workspace config and record kinds as data | OT-7 | Ready (RS1 accepted; OT-5 merged; Otto main `4179ba5f`) | — | Extra High. Alone on the critical path; OT-8 and OT-11 follow it |
| [P95-16](packets/P95-16.md) Otto guidance: stand-up playbook, run-contract core, glossary | OT-16 | Ready (OT-15 merged into `project/95-otto`) | — | Extra High. Beside P95-17 and P95-07 |
| [P95-17](packets/P95-17.md) Otto guidance: generic roles and workstreams | OT-17 | Ready (OT-15 merged; merges after P95-16) | — | High. Beside P95-16 and P95-07 |
| [P95-08](packets/P95-08.md) Relation kinds and cardinality as data | OT-8 | Ready (OT-7 merged; Otto main `608ef135`) | — | Extra High. Critical path; first priority |
| [P95-11](packets/P95-11.md) Template selection and manifests | OT-11 | Ready (OT-7 merged; Otto main `608ef135`) | — | Extra High. Beside P95-08 within the cap |
| [P95-09](packets/P95-09.md) Pipeline declarations, listing and traversal | OT-9 | Ready (OT-8 merged; Otto main `cefbfc1e`) | — | Extra High. Critical path (then OT-10, OT-13) |
| [P95-12](packets/P95-12.md) Standard and loop templates; a third with no code change | OT-12 | Ready (OT-11 merged; Otto main `cefbfc1e`) | — | High |
| [P95-10](packets/P95-10.md) Pipeline conformance check | OT-10 | Ready (OT-9 merged; Otto main `d67cacfb`) | — | Extra High. Critical path (then OT-13) |
| [P95-PK](packets/P95-PK.md) Package the templates and guidance for installed Otto | gap from OT-12 | Ready (OT-12 and OT-17 merged) | — | Extra High. Beside P95-10; needed before OT-22 |
| [P95-RV](packets/P95-RV.md) High-judgment review (RS1, R) | RS1, R | On REQUEST only | — | Pro. A fresh session for each REQUEST |
| Other cards (OT-7 to OT-14, OT-16 to OT-21) | per [tasks.md](tasks.md) | Blocked on the cards they depend on | — | Packets are written by the orchestrator when each becomes Ready |

## Manager launch message

The owner pastes this into the manager's own ChatGPT session.

```text
You are the Manager for the Plan 95 run (Otto, an importable framework for Markdown-first organisations), reporting to the orchestrator (mailbox name p71-73-orchestrator, Claude session session_011EzfW1Urc5P4hpm2SvVy5d).
Follow agent/roles/orchestrator/multi-manager-dispatch.md in banodoco/astrid-dev, taking its Orchestrator's part, with this plan's orchestrator as "the Lead".
Read plans/95-composable-agentic-workspaces/run.md on main, then again at every check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1886, format in its first post. Your mailbox name: p95-manager-1.
First do the Manager startup checks in run.md and post one STATUS with each result; dispatch nothing until the orchestrator's DECISION answers it. Then give each Ready packet a FRESH ChatGPT session (a normal Chat, not Work) in the mode its packet's Route sets (N High, X Extra High, S Pro), with the packet start message in run.md. Dispatch the first packet alone. Check in EVERY 20 MINUTES while any packet is Running or in Review, and hourly when idle: read the mailbox by cursor, check every open packet, start every Ready packet that has no unmet dependency and no conflict with a Running one (up to the cap), resume or replace stalled sessions, pass READY-PROOF submissions to the orchestrator, and post one STATUS an hour.
You may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. You may not merge, edit the repository, dispatch hosted CI or approve anything. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```

## Packet start message

The manager sends this, filled in, as the first message of each fresh packet session.

```text
You are the ChatGPT manager implementing ONE packet for the Plan 95 run (Otto).
Follow agent/roles/manager/chatgpt-packet.md in banodoco/astrid-dev.
Packet: plans/95-composable-agentic-workspaces/packets/<id>.md at <main SHA>; its PR destination names your repository and branches.
Authority: the Authority section of plans/95-composable-agentic-workspaces/run.md at <main SHA>, given by the owner.
Standing rulings: the same file's Standing rulings section; they bind you.
Board: https://github.com/banodoco/astrid-dev/issues/1886, run p95-otto, format in its first post. You are p95-<packet>-<n>;
the Manager is p95-manager-1; the orchestrator, in the Lead's place, is p71-73-orchestrator.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply orchestrator decisions <comment IDs> not yet done.]
Write this packet's code, tests and documents; do not clone, build or run tests. Post STATUS or BLOCKED as comments on the board,
the first as soon as your first branch is pushed and its draft pull request open.
End with READY-PROOF <repo> <PR> <head> <selectors>, then stop.
Do not merge, tick tasks.md or start another packet.
```
