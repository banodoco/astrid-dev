# Plan 72 completion run — run board

The live state of Plan 72's completion run, rewritten by the orchestrator at each check-in. The plan's [`tasks.md`](tasks.md#completion-run-owner-go-24-november-2026) stays the record of progress; this board holds the authority, the rulings and the packet queue. Packets are in [packets/](packets/).

## Now (22:30 UTC, Tue 24 Nov)

The integration card has landed: the project branch is at `c29908e587b59dc1ba8fc3891cce7ee94480412d`. Ready: P72-01. The first packet goes alone until its early STATUS proves a packet session can push, open a draft PR and comment.

## Authority

On 24 November 2026, in orchestrator session `session_011EzfW1Urc5P4hpm2SvVy5d`, the owner asked for Plans 71, 72 and 73 to be finished with that session as orchestrator and one manager per plan, using the fresh ChatGPT packet workstream the way Release 15's Plans 87 and 89 do ([release 15 run board](../../releases/15/run.md#plans-87-and-89-dispatch)). This is an astrid-dev-only run: there is no release, release branch or Release Lead.

- **Orchestrator** (`p71-73-orchestrator`, Claude session `session_011EzfW1Urc5P4hpm2SvVy5d`): the accountable agent for this plan. It takes the Lead's part of the [packet workstream](../../skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md): it writes and orders packets, has each submission reviewed on the run contract's routes, applies the fix-it-yourself rule, merges accepted PRs into `project/72-composable-project-delivery`, merges `main` into it, runs every proof, keeps `tasks.md` true through progress PRs, commissions the final review R, requests the owner's sense check and opens the completion PR. Its DECISIONs bind the manager and the packet sessions, within this section.
- **Manager** (`p72-manager-1`): a session in the owner's ChatGPT account, started by her own launch message and acting at her request. It takes the Orchestrator's part of [multi-manager dispatch](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md), with this plan's orchestrator as "the Lead". It may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. It does not edit the repository, merge, approve or dispatch hosted CI.
- **Packet sessions** (`p72-<packet>-<n>`): may push to the `p72/<card id>` branch their packet names, open pull requests into `project/72-composable-project-delivery`, and comment on the mailbox. They never merge, never edit `tasks.md` or this board, never rebase a shared branch, never dispatch hosted CI and never take a second packet. Their mode follows the packet's Route: N High, X Extra High, S Pro ([run contract](../../skills/shared/run-contract.md#chatgpt-session-modes)).
- **Stays in the orchestrator's lane:** PDC-1 (create the project branch and integrate), PDC-2 (delete the Release 15 scratch test), PDC-5 (integrated qualification), R (final review, up to two rounds), PDC-7 (completion PR) and every proof.
- **Needs the owner:** the final merge of the project branch into `main`; any change to the public feed shape, existing check verdicts or canonical records beyond the cards; publishing; anything paid; changing an existing test's assertion.

## Standing rulings

1. **Functions, not files, conflict.** Different functions or sections in one file are not a conflict between packets; the same function, section or new test table is. A function is free for the next packet once the last task that writes it has merged.
2. **Proof runs where the network is.** Packet sessions write code and tests and end with `READY-PROOF <repo> <PR> <head> <selectors>`; the orchestrator runs `python3 scripts/astrid_dev.py check`, `python3 -m unittest discover -s scripts -p "test_*.py"` and the packet's focused selectors on the exact head, and posts the result.
3. **The destination is the project branch.** Where the packet workstream says `release/<N>/plan-<P>`, read `project/72-composable-project-delivery`. Cut each task branch from its current head; merge it in, never rebase; post BLOCKED if the board lists a different head for an existing draft.
4. **Dependants wait only for the cards they depend on,** not for a whole packet.
5. **Reviews.** The orchestrator runs every proof and reviews ordinary submissions itself. A high-judgment verdict goes to a fresh, read-only ChatGPT session in **Pro** (owner, 24 November 2026), using the review packet [P72-RV](packets/P72-RV.md). That covers S packets, any change to what a check accepts or refuses, and the final review R; in this plan, P72-01 (it changes what `check` refuses) and the final review R (up to two rounds). The manager starts it only on the orchestrator's REQUEST, which names the review kind, the pull request, the exact head and the proof results, and it starts a fresh session for each REQUEST. No packet session reviews its own work. The owner's project-wide sense check is separate: a read-only session in GPT-6.2 Astra at High, at most two rounds, also started only on the orchestrator's REQUEST. If either mode is not offered, the manager says so and the orchestrator asks the owner.
6. **Cap:** at most two packets Running or Review in this plan at once. The first packet goes alone, until its early STATUS shows a session can push, open a draft PR and comment.
7. **Sessions:** packet sessions run in a normal ChatGPT Chat, not Work. One writer per branch: replace a stopped session only after its branch has been still for 30 minutes, naming the head in the replacement's first message.
8. **Plan records:** `plans/72-composable-project-delivery/*.md` change on `main` only through the orchestrator's progress PRs. A packet may add only the evidence file its packet names.

## Mailbox

[astrid-dev #1881](https://github.com/banodoco/astrid-dev/issues/1881), run `p72-completion`, format in its first post.

| Role | Mailbox name | Session | Last processed comment |
|---|---|---|---|
| Orchestrator | `p71-73-orchestrator` | `session_011EzfW1Urc5P4hpm2SvVy5d` | — |
| Manager | `p72-manager-1` | named in its first STATUS | — |
| Packet session | `p72-<packet>-<n>`, for example `p72-P72-01-1` | from the manager's STATUS | — |

## When a session goes quiet

A branch, not a chat, shows health ([liveness](../../skills/shared/run-contract.md#coordination-boards-and-check-ins)).

- **A packet session:** the manager resumes it after 3 hours with no commit or STATUS, and replaces it as the [dispatch workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md) says; the replacement is `p72-<packet>-<n+1>`.
- **The manager:** the orchestrator nudges it on the mailbox at 2 hours; at 3 hours it tells the owner, who starts a fresh manager from the launch message below as `p72-manager-2`.
- **The orchestrator:** the manager keeps running packets going, starts nothing that needs a ruling, and tells the owner at 3 hours.
- **A READY-PROOF** unanswered for 45 minutes, or a Review for 4 hours: the manager sends the orchestrator a REQUEST and tells the owner.

## Manager startup checks

The manager does these first, posts one STATUS with each as passed or failed, and dispatches nothing until the orchestrator's DECISION answers it. A failure is a manual step for the owner, written in that STATUS.

1. **Mailbox both ways:** read #1881, post one non-sensitive ACK, see the orchestrator's reply.
2. **Branches:** `project/72-composable-project-delivery` exists at the head this board's dispatch queue names, and no `p72/*` branch exists that the board does not list.
3. **A fresh ChatGPT session** in the mode the first packet's Route sets, with nothing from an earlier chat.
4. **Resume:** reopen that session later and continue it.
5. **The hour:** a reminder that fires every hour, verified by one firing.
6. **GitHub from a packet session:** proved by the first packet's early STATUS: it pushed a `p72/<card id>` branch, opened a draft PR into `project/72-composable-project-delivery` and commented on #1881.
7. **GitHub for the manager:** it can read pull requests, commits and workflow runs in astrid-dev, and comment on #1881.
8. **Capacity:** how many ChatGPT sessions the account can run at once, and whether Extra High, Pro and GPT-6.2 Astra at High are offered.

The orchestrator's own check (it runs the proofs): it can clone astrid-dev, run both checks and one focused test. Passed on 24 November 2026.

## Dispatch queue

Cap: two Running or Review at once (ruling 6). Dispatch the next as slots free and dependencies merge.

| Packet brief | Source tasks | Handoff | Session | Mode and next action |
|---|---|---|---|---|
| [P72-01](packets/P72-01.md) Delivery integrity as a registered check | PDC-3 | Ready (project head `c29908e5`) | — | Extra High. First packet, alone |
| [P72-02](packets/P72-02.md) Duplicate interpretation and the extension guide | PDC-4 | Blocked on P72-01 merging | — | Extra High. Investigation STATUS first |
| [P72-RV](packets/P72-RV.md) High-judgment review (read-only, Pro) | P72-01 (it changes what `check` refuses) and the final review R (up to two rounds) | On REQUEST only | — | Pro. A fresh session for each REQUEST |
| [P72-SC](packets/P72-SC.md) Project-wide sense check, round 1 (read-only) | SC | Blocked on R | — | GPT-6.2 Astra, High. Started only on the orchestrator's REQUEST |

**Conflicts:** P72-01 writes `scripts/checks.py:REGISTRY` and its tests; P72-02 writes link-deriving functions in `scripts/export_public_vision.py`, `scripts/project_contract.py`, `scripts/gap_relationships.py` and one section of `docs/extending.md`. They run in that order. Plan 73's P73-01 also edits `scripts/checks.py` (a different function) and P73-06 edits other sections of `docs/extending.md`: different functions and sections are not a conflict (ruling 1).

## Manager launch message

The owner pastes this into the manager's own ChatGPT session.

```text
You are the Manager for the Plan 72 completion run (Composable project-delivery relationships), reporting to the orchestrator (mailbox name p71-73-orchestrator, Claude session session_011EzfW1Urc5P4hpm2SvVy5d).
Follow skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md in banodoco/astrid-dev, taking its Orchestrator's part, with this plan's orchestrator as "the Lead".
Read plans/72-composable-project-delivery/run.md on main, then again at every hourly check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1881, format in its first post. Your mailbox name: p72-manager-1.
First do the Manager startup checks in run.md and post one STATUS with each result; dispatch nothing until the orchestrator's DECISION answers it. Then give each Ready packet a FRESH ChatGPT session (a normal Chat, not Work) in the mode its packet's Route sets (N High, X Extra High, S Pro), with the packet start message in run.md. Dispatch the first packet alone. Every hour: read the mailbox by cursor, check every open packet, start every Ready packet that has no unmet dependency and no conflict with a Running one (up to the cap), resume or replace stalled sessions, pass READY-PROOF submissions to the orchestrator, and post one STATUS.
You may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. You may not merge, edit the repository, dispatch hosted CI or approve anything. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```

## Packet start message

The manager sends this, filled in, as the first message of each fresh packet session ([workstream](../../skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md#packet-start-message)).

```text
You are the ChatGPT manager implementing ONE packet for the Plan 72 completion run.
Follow skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md in banodoco/astrid-dev.
Packet: plans/72-composable-project-delivery/packets/<id>.md at <main SHA>; its PR destination names your branches.
Authority: the Authority section of plans/72-composable-project-delivery/run.md at <main SHA>, given by the owner.
Standing rulings: the same file's Standing rulings section; they bind you.
Board: https://github.com/banodoco/astrid-dev/issues/1881, run p72-completion, format in its first post. You are p72-<packet>-<n>;
the Manager is p72-manager-1; the orchestrator, in the Lead's place, is p71-73-orchestrator.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply orchestrator decisions <comment IDs> not yet done.]
Write this packet's code and tests; do not clone, build or run tests. Post STATUS or BLOCKED as comments on the board,
the first as soon as your first branch is pushed and its draft pull request open.
End with READY-PROOF astrid-dev <PR> <head> <selectors>, then stop.
Do not merge, tick tasks.md or start another packet.
```
