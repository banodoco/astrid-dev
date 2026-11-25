# Plan 73 completion run — run board

The live state of Plan 73's completion run, rewritten by the orchestrator at each check-in. The plan's [`tasks.md`](tasks.md#completion-run-owner-go-24-november-2026) stays the record of progress; this board holds the authority, the rulings and the packet queue. Packets are in [packets/](packets/).

## Now (22:30 UTC, Tue 24 Nov)

The integration card has landed: the project branch is at `4584a138162eb6ea2b7e21af5c64ab2536b2fcbe`. Ready: P73-01, P73-02, P73-03. The first packet goes alone until its early STATUS proves a packet session can push, open a draft PR and comment.

## Authority

On 24 November 2026, in orchestrator session `session_011EzfW1Urc5P4hpm2SvVy5d`, the owner asked for Plans 71, 72 and 73 to be finished with that session as orchestrator and one manager per plan, using the fresh ChatGPT packet workstream the way Release 15's Plans 87 and 89 do ([release 15 run board](../../releases/15/run.md#plans-87-and-89-dispatch)). This is an astrid-dev-only run: there is no release, release branch or Release Lead.

- **Orchestrator** (`p71-73-orchestrator`, Claude session `session_011EzfW1Urc5P4hpm2SvVy5d`): the accountable agent for this plan. It takes the Lead's part of the [packet workstream](../../agent/roles/leader/multi-manager-release.md): it writes and orders packets, has each submission reviewed on the run contract's routes, applies the fix-it-yourself rule, merges accepted PRs into `project/73-markdown-first-agent-skills`, merges `main` into it, runs every proof, keeps `tasks.md` true through progress PRs, commissions the final review R, requests the owner's sense check and opens the completion PR. Its DECISIONs bind the manager and the packet sessions, within this section.
- **Manager** (`p73-manager-1`): a session in the owner's ChatGPT account, started by her own launch message and acting at her request. It takes the Orchestrator's part of [multi-manager dispatch](../../agent/roles/orchestrator/multi-manager-dispatch.md), with this plan's orchestrator as "the Lead". It may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. It does not edit the repository, merge, approve or dispatch hosted CI.
- **Packet sessions** (`p73-<packet>-<n>`): may push to the `p73/<card id>` branch their packet names, open pull requests into `project/73-markdown-first-agent-skills`, and comment on the mailbox. They never merge, never edit `tasks.md` or this board, never rebase a shared branch, never dispatch hosted CI and never take a second packet. Their mode follows the packet's Route: N High, X Extra High, S Pro ([run contract](../../agent/shared/run-contract.md#chatgpt-session-modes)).
- **Stays in the orchestrator's lane:** MSC-1 (integration), MSC-7 (the fresh-agent exercise, which the orchestrator arranges in a fresh Claude Code session), MSC-8 (cold start), R (final review), MSC-10 (completion PR and cutover) and every proof, build and install.
- **Needs the owner:** the cutover time and the final merge of the project branch into `main`; installing generated skills on anyone's real machine or session; publishing; anything paid; changing an existing test's assertion.

## Standing rulings

1. **Functions, not files, conflict.** Different functions or sections in one file are not a conflict between packets; the same function, section or new test table is. A function is free for the next packet once the last task that writes it has merged.
2. **Proof runs where the network is.** Packet sessions write code and tests and end with `READY-PROOF <repo> <PR> <head> <selectors>`; the orchestrator runs `python3 scripts/astrid_dev.py check`, `python3 -m unittest discover -s scripts -p "test_*.py"` and the packet's focused selectors on the exact head, and posts the result.
3. **The destination is the project branch.** Where the packet workstream says `release/<N>/plan-<P>`, read `project/73-markdown-first-agent-skills`. Cut each task branch from its current head; merge it in, never rebase; post BLOCKED if the board lists a different head for an existing draft.
4. **Dependants wait only for the cards they depend on,** not for a whole packet.
5. **Reviews.** The orchestrator runs every proof and reviews ordinary submissions itself. A high-judgment verdict goes to a fresh, read-only ChatGPT session in **Pro** (owner, 24 November 2026), using the review packet [P73-RV](packets/P73-RV.md). That covers S packets, any change to what a check accepts or refuses, and the final review R; in this plan, P73-07 (route S) and the final review R. The manager starts it only on the orchestrator's REQUEST, which names the review kind, the pull request, the exact head and the proof results, and it starts a fresh session for each REQUEST. No packet session reviews its own work. The owner's project-wide sense check is separate: a read-only session in **Pro** in normal ChatGPT Chat (owner, 24 November 2026; it replaces GPT-6.2 Astra at High), at most two rounds, also started only on the orchestrator's REQUEST. Astra is not substituted. If Pro is not offered, the manager says so and the orchestrator asks the owner, who starts the review manually in Pro.
6. **Cap:** at most two packets Running or Review in this plan at once. The first packet goes alone, until its early STATUS shows a session can push, open a draft PR and comment.
7. **Sessions:** packet sessions run in a normal ChatGPT Chat, not Work. One writer per branch: replace a stopped session only after its branch has been still for 30 minutes, naming the head in the replacement's first message.
8. **Plan records:** `plans/73-markdown-first-agent-skills/*.md` change on `main` only through the orchestrator's progress PRs. A packet may add only the evidence file its packet names.

## Mailbox

[astrid-dev #1882](https://github.com/banodoco/astrid-dev/issues/1882), run `p73-completion`, format in its first post.

| Role | Mailbox name | Session | Last processed comment |
|---|---|---|---|
| Orchestrator | `p71-73-orchestrator` | `session_011EzfW1Urc5P4hpm2SvVy5d` | — |
| Manager | `p73-manager-1` | named in its first STATUS | — |
| Packet session | `p73-<packet>-<n>`, for example `p73-P73-01-1` | from the manager's STATUS | — |

## When a session goes quiet

A branch, not a chat, shows health ([liveness](../../agent/shared/run-contract.md#coordination-boards-and-check-ins)).

- **A packet session:** the manager resumes it after 3 hours with no commit or STATUS, and replaces it as the [dispatch workstream](../../agent/roles/orchestrator/multi-manager-dispatch.md) says; the replacement is `p73-<packet>-<n+1>`.
- **The manager:** the orchestrator nudges it on the mailbox at 2 hours; at 3 hours it tells the owner, who starts a fresh manager from the launch message below as `p73-manager-2`.
- **The orchestrator:** the manager keeps running packets going, starts nothing that needs a ruling, and tells the owner at 3 hours.
- **A READY-PROOF** unanswered for 45 minutes, or a Review for 4 hours: the manager sends the orchestrator a REQUEST and tells the owner.

## Manager startup checks

The manager does these first, posts one STATUS with each as passed or failed, and dispatches nothing until the orchestrator's DECISION answers it. A failure is a manual step for the owner, written in that STATUS.

1. **Mailbox both ways:** read #1882, post one non-sensitive ACK, see the orchestrator's reply.
2. **Branches:** `project/73-markdown-first-agent-skills` exists at the head this board's dispatch queue names, and no `p73/*` branch exists that the board does not list.
3. **A fresh ChatGPT session** in the mode the first packet's Route sets, with nothing from an earlier chat.
4. **Resume:** reopen that session later and continue it.
5. **The hour:** a reminder that fires every hour, verified by one firing.
6. **GitHub from a packet session:** proved by the first packet's early STATUS: it pushed a `p73/<card id>` branch, opened a draft PR into `project/73-markdown-first-agent-skills` and commented on #1882.
7. **GitHub for the manager:** it can read pull requests, commits and workflow runs in astrid-dev, and comment on #1882.
8. **Capacity:** how many ChatGPT sessions the account can run at once, and whether Extra High and Pro are offered.

The orchestrator's own check (it runs the proofs): it can clone astrid-dev, run both checks and one focused test. Passed on 24 November 2026.

## Dispatch queue

Cap: two Running or Review at once (ruling 6). Dispatch the next as slots free and dependencies merge.

| Packet brief | Source tasks | Handoff | Session | Mode and next action |
|---|---|---|---|---|
| [P73-01](packets/P73-01.md) Milestone probes become tests; builder constants | MSC-2 | Ready (project head `4584a138`) | — | Extra High. First packet, alone |
| [P73-02](packets/P73-02.md) Forward-port `main`'s `skills/` changes, half A | MSC-3 | Ready (project head `7f9f9978`, P73-01 merged) | — | Extra High. In parallel with P73-03 |
| [P73-03](packets/P73-03.md) Forward-port, half B, new homes and run-contract sections | MSC-3 | Ready (project head `7f9f9978`, P73-01 merged) | — | Extra High. In parallel with P73-02 |
| [P73-04](packets/P73-04.md) Rule-preservation audit, roles and role workstreams | MSC-4 | Ready (project head `090c3f87`) | — | Extra High. In parallel with P73-05 |
| [P73-05](packets/P73-05.md) Rule-preservation audit, shared documents | MSC-4 | Ready (project head `090c3f87`) | — | Extra High. In parallel with P73-04 |
| [P73-06](packets/P73-06.md) Active consumers and the authoring guide | MSC-5 | Ready (project head `090c3f87`; the site-list DECISION, 85 sites, is on the board) | — | Extra High. Starts when one of P73-04 or P73-05 reaches READY-PROOF (cap two) |
| [P73-07](packets/P73-07.md) Delete the old layout | MSC-6 | Blocked on P73-01, P73-04, P73-05 and P73-06 merging | — | Pro. Pro |
| [P73-INT](packets/P73-INT.md) Absorb a landed Plan 71 or 72 (read-only fact-find, then the port) | MSC-9 | On REQUEST only | — | Extra High. A fresh session for each landing, on the orchestrator's REQUEST with the delta and link evidence |
| [P73-RV](packets/P73-RV.md) High-judgment review (read-only, Pro) | P73-07 (route S) and the final review R | On REQUEST only | — | Pro. A fresh session for each REQUEST |
| [P73-SC](packets/P73-SC.md) Project-wide sense check, round 1 (read-only) | SC | Blocked on R | — | Pro (normal Chat), read-only. Started only on the orchestrator's REQUEST |

**Conflicts:** `agent/**` files are split between P73-02 and P73-03 by file (each packet lists its own); P73-04 and P73-05 split the audit by document group and may each fix only their own group's files. P73-01 writes `scripts/` and `.github/workflows/docs.yml`; P73-06 writes `README.md`, `CONTRIBUTING.md`, `docs/**`, `templates/**`, `env/**` and active release and plan documents; P73-07 deletes `skills/**` and `sync.sh`.

## Landing with Plans 71 and 72

Plan 73 is the last to reach `main`, so it absorbs the other two; nothing is rebased (the repository merges, never rewrites a published branch). The owner decides each merge into `main`; the order they land in does not matter to Plan 73.

1. **Plan 72** and **Plan 71** each open their own completion pull request (PDC-7, GDC-7) once their sense check is accepted. They do not open a combined one: review intake labels exactly one `Project:` and one completion section per pull request.
2. After each lands, the orchestrator merges current `main` into this project branch and runs **MSC-9**: the ChatGPT session ([P73-INT](packets/P73-INT.md)) fact-finds from the orchestrator's `git log` and `git grep` output and re-applies any `skills/` edit to its `agent/` home. Session limits: it cannot run git, code search is default-branch only, and it cannot verify link anchors, so the orchestrator supplies the evidence and runs `check` before accepting.
3. Known surfaces (trial merge of the three heads into `main`, 25 November 2026: no conflicts, `check` exit 0, 683 tests): Plan 71's gap-workflow edit to `skills/shared/workstreams/astrid-dev-gap/SKILL.md` and 15 relative links into `skills/` in `docs/contribution-workflow.md`, Plan 71's `inputs.md` and eight evidence files; Plan 72's `scripts/checks.py` entry, `docs/checks.md` (regenerate after P73-07) and one section of `docs/extending.md`.
4. At MSC-10 the orchestrator merges `main` once more. R and SC need not repeat if the new `main` commits touch nothing under `agent/`, `skills/`, `scripts/` or Markdown links into them (the delta check and `git diff --stat` prove it); otherwise the orchestrator asks the reviewer for a delta read of those commits only.
5. Rollback is the revert of one merge commit per project; the project branches stay.

## Manager launch message

The owner pastes this into the manager's own ChatGPT session.

```text
You are the Manager for the Plan 73 completion run (Markdown-first agent documents and generated skills), reporting to the orchestrator (mailbox name p71-73-orchestrator, Claude session session_011EzfW1Urc5P4hpm2SvVy5d).
Follow skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md in banodoco/astrid-dev, taking its Orchestrator's part, with this plan's orchestrator as "the Lead".
Read plans/73-markdown-first-agent-skills/run.md on main, then again at every hourly check. Ready rows link the packets.
Mailbox: https://github.com/banodoco/astrid-dev/issues/1882, format in its first post. Your mailbox name: p73-manager-1.
First do the Manager startup checks in run.md and post one STATUS with each result; dispatch nothing until the orchestrator's DECISION answers it. Then give each Ready packet a FRESH ChatGPT session (a normal Chat, not Work) in the mode its packet's Route sets (N High, X Extra High, S Pro), with the packet start message in run.md. Dispatch the first packet alone. Every hour: read the mailbox by cursor, check every open packet, start every Ready packet that has no unmet dependency and no conflict with a Running one (up to the cap), resume or replace stalled sessions, pass READY-PROOF submissions to the orchestrator, and post one STATUS.
You may start, resume, stop and replace this plan's packet sessions and comment on the mailbox. You may not merge, edit the repository, dispatch hosted CI or approve anything. Send anything reserved to the owner to the orchestrator.
If a check fails, say which manual step the owner must do instead of promising automation.
```

## Packet start message

The manager sends this, filled in, as the first message of each fresh packet session ([workstream](../../agent/roles/orchestrator/multi-manager-dispatch.md#packet-start-message)).

```text
You are the ChatGPT manager implementing ONE packet for the Plan 73 completion run.
Follow skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md in banodoco/astrid-dev.
Packet: plans/73-markdown-first-agent-skills/packets/<id>.md at <main SHA>; its PR destination names your branches.
Authority: the Authority section of plans/73-markdown-first-agent-skills/run.md at <main SHA>, given by the owner.
Standing rulings: the same file's Standing rulings section; they bind you.
Board: https://github.com/banodoco/astrid-dev/issues/1882, run p73-completion, format in its first post. You are p73-<packet>-<n>;
the Manager is p73-manager-1; the orchestrator, in the Lead's place, is p71-73-orchestrator.
[Replacing <prior session>: continue from <branch> at <head> and <last STATUS link>;
 apply orchestrator decisions <comment IDs> not yet done.]
Write this packet's code and tests; do not clone, build or run tests. Post STATUS or BLOCKED as comments on the board,
the first as soon as your first branch is pushed and its draft pull request open.
End with READY-PROOF astrid-dev <PR> <head> <selectors>, then stop.
Do not merge, tick tasks.md or start another packet.
```
