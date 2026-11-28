# Lane brief — dependable

**Lane:** dependable
**Releases:** 16
**State:** running; takes over Plans 93, 94 and 38 from the earlier Release 16 setup, and starts Plan 79. Its orchestrator moved from Claude to Codex on 28 November (owner).
**Go:** given on 28 November 2026 in the [planning session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG): owner-authorized run of Plans 93, 94, 38 and 79 in Release 16 to the cut on Friday 4 December 2026, CPU and Linux scope (see Owner rulings). The orchestrator replaces the Codex Lead `r16-lead` for these plans; their existing managers and chats continue under it.
**Orchestrator:** one Codex session in the Codex app on the owner's computer, on route S (Sol), mailbox `dependable-orchestrator` (owner, 28 Nov 2026). It replaces the Claude session `session_011EzfVzdahcZYHKAzfLeHTj`, which opened the board and stood down. It records its thread name here in its first progress PR.
**Reviewer:** a fresh Claude Opus session, independent of every author and of the orchestrator; one per review stop ([reviewer-h3.md](reviewer-h3.md) is the template, with this lane's board)
**Board:** [`board: lane dependable`](https://github.com/banodoco/astrid-dev/issues/2086), opened on 28 November. It is this lane's one message board.

This is the one home for how the dependable lane runs. **Precedence:** for this lane, this brief wins over the orchestrator skill wherever they differ. The [run contract](../../../agent/shared/run-contract.md)'s safety, proof and permission rules win over this brief. Branches, merges and pull requests follow [the pipeline](../../../agent/shared/pipeline.md#branches-and-pull-requests).

## Outcome

By the cut, Plans 93, 94, 38 and 79 land in `release/16/main` with their CPU and Linux scope proven: an existing ComfyUI is found, set up and recovered (93, 94), Agent and Runtime agree on one process identity on Linux (38), and local media of any size imports without loading whole files into memory (79). Desktop and Windows paths are marked unqualified, and their real-machine cells are Release 17 work.

## Plans and order

| Plan | Release | Starts when | Branches |
| --- | --- | --- | --- |
| [93 ComfyUI Desktop and existing environments](../../../plans/93-comfyui-desktop-and-existing-environments/plan.md) | 16 | Now: CD-N and CD-3S, then its join and final review | astrid-agent `release/16/plan-93`, astrid-app `release/16/plan-93` |
| [94 Dependable environment setup and recovery](../../../plans/94-dependable-environment-setup-and-recovery/plan.md) | 16 | Now: 94-B; 94-F and 94-H after Plan 93 lands in `release/16/main` | astrid-agent `release/16/plan-94` |
| [38 One process identity](../../../plans/38-one-process-identity/plan.md) | 16 | Now: 38-Q, 38-scan, 38-01 and 38-04 in parallel | astrid-runtime and astrid-agent `release/16/plan-38` |
| [79 Local media of any size](../../../plans/79-local-media-any-size/plan.md) | 16 | Now: its first unit makes every card's Focused proof an exact command | astrid-runtime, astrid-agent and astrid-app `release/16/plan-79`, cut by the orchestrator from `release/16/main` |

## Queue

Each plan's `tasks.md` is the queue: its Release 16 recovery or remaining queue, in order. [Plan 93](../../../plans/93-comfyui-desktop-and-existing-environments/tasks.md), [Plan 94](../../../plans/94-dependable-environment-setup-and-recovery/tasks.md), [Plan 38](../../../plans/38-one-process-identity/tasks.md), [Plan 79](../../../plans/79-local-media-any-size/tasks.md). Rows marked `blocked:` or Release 17 are not dispatched.

## How it runs

**Option:** packets

- **Start.** If the lane board already exists, read it from the first post and continue from the last STATUS; skip what is already done (the stand-down below was posted on 28 November). Otherwise take over in the first hour: post `DECISION dependable-orchestrator to: r16-lead: stand down as Release 16 Lead; Plans 93, 94 and 38 now run under releases/16/briefs/dependable.md, by the owner's go recorded there. Post one final STATUS on each plan board, delete your scheduled automation, and stop.` on `board: release 16 lead`; open the lane board, then post one final comment on each plan board ([#2032](https://github.com/banodoco/astrid-dev/issues/2032), [#2051](https://github.com/banodoco/astrid-dev/issues/2051), [#2050](https://github.com/banodoco/astrid-dev/issues/2050)): `DECISION dependable-orchestrator: this plan now runs under releases/16/briefs/dependable.md; post to board: lane dependable from now on, to: dependable-orchestrator`, with the lane board's link, and close the plan board. Each plan's existing manager keeps its chats and its in-flight units; it reads the lane board from its next check-in. Post STATUS 1 listing, per plan, the units in flight and the next one.
- **Dispatch.** Four plans active in ChatGPT at once, one chat each (owner, 28 November). A unit already in a chat continues in that chat; a new unit gets a fresh chat from the [chat start message](#start-messages), in its route's mode (N High, X Extra High, S Pro). Plan 79 has no manager yet: the orchestrator opens a new Codex thread for `r16-p79-manager` with the [manager launch](#start-messages) itself, if the Codex app lets one thread start another; the first time, it records the exact steps as a `TOOLKIT` comment on [#2030](https://github.com/banodoco/astrid-dev/issues/2030). If the app can't, it posts `LAUNCH r16-p79-manager` on the lane board and tells the owner. Two units never write the same function at once; 94-F and 94-H wait for Plan 93's merged work.
- **Proof.** New work commits on `task/<PP>/<id>` and posts `READY-PROOF <repo> <branch> <sha> <tests>`; an in-flight draft PR into a plan branch may finish as it is. The proof is the orchestrator's own run of the unit's focused tests, by id, on the merged tree, on the owner's computer (owner, 28 November): in its Codex workspace it keeps local clones of astrid-agent, astrid-runtime and astrid-app, sets up each repository once with its `scripts/worker-env/agent-setup.sh`, merges the task in a scratch worktree, runs the tests there, and pushes the plan branch only if they pass. Evidence is one post: the command, the SHA, and the pass and fail counts. No archives, checksums, tree audits or acceptance tuples; evidence already posted stands and is not redone.
- **Reviews.** Plan 93's final review (R16-P93-R), Plan 94's 94-K, Plan 38's 38-RS and 38-11, and Plan 79's LM-R need the reviewer's ACCEPT. Other units merge on the orchestrator's proof.
- **Merges.** The orchestrator merges units into each plan branch. When a plan is ready it merges `release/16/main` forward, runs `ci.yml` once on that head, opens the PR into `release/16/main` and posts it on `board: release 16 lead`; the Lead merges, one plan at a time. Plan 93 lands first, so that Plan 94 can merge it forward.
- **Check-ins.** The orchestrator's hourly Codex automation is its wake path; nothing else can wake it, so anything urgent for it goes to the owner. Each check starts by pulling banodoco/astrid-dev `main` (`git pull --ff-only` in its astrid-dev clone, and `skills install` again if `agent/` changed), so this brief and every `tasks.md` are current. Each check reads the lane board by cursor, acts, and posts one STATUS of 10 lines or fewer: units merged, in flight, blocked with cause, next, `acted on:` and `cursor:`.

## Roles

- **Orchestrator:** accountable for every plan in this lane; answers to the owner, and hands each ready plan to the Release 16 Lead. It may cut and merge plan branches, dispatch, resume and replace chats and reviewers, and post on boards.
- **Managers:** each plan's existing Codex manager, and `r16-p79-manager`. They open, resume and replace their plan's chats, write each unit's start message, and relay to the orchestrator. They never merge, rule or run proof.
- **Owner:** see [Owner only](#owner-only).

## Standing rulings

Dated and append-only; this is the one home for this lane's rulings.

- 28 Nov 2026 (owner):
  - The orchestrator takes over from the Codex Lead for these plans; existing managers and chats continue under it.
  - Proof is the light pipeline proof above.
  - Release 16 is CPU and Linux. To Release 17: Plan 93 CD-5, CD-0L, CD-3L, CD-4L; Plan 94 94-C, 94-D, 94-I, 94-J, 94-P; Plan 38 38-02, 38-03, 38-08U, 38-10, 38-10W, 38-12 to 38-14. If a Windows machine is booked by Monday 30 November, 94-C's pin and one Windows round return. Desktop and Windows are marked unqualified in the release notes.
- 28 Nov 2026 (Release 16 Lead, on the plans' recorded recommendations):
  - Plan 93: the person starts Desktop (D3); two plans with one RS1 and one final review, as run (D4); base `release/16/main` (D5). CD-3S may edit `tests/test_setup_skill_branches.py` only if the reviewer agrees each assertion keeps its intent.
  - Plan 94: Portable confirmed (D3); no automatic paid rental in Release 16; RS1 and R are one review, 94-K (D5, D6); 94-G runs only if Plan 90's producer has landed by 1 December, else Release 17.
  - Plan 38: renew the quarantine date to 12 December (38-Q) and route each exposed failure to its owner; old-format journals stay fail-closed (D3); Windows #682 is restricted and recorded, not repaired, in Release 16.

## Context

- **Where each plan stood on 28 November:** the reconciled queues in each plan's `tasks.md`, and the old boards [#2032](https://github.com/banodoco/astrid-dev/issues/2032), [#2051](https://github.com/banodoco/astrid-dev/issues/2051) and [#2050](https://github.com/banodoco/astrid-dev/issues/2050) as history.
- **The earlier setup:** `releases/16/run.md`'s Delivery section and `briefs/lead.md`, superseded for these plans by this brief.

## Cut line and coordination

- **Never slips:** Plan 93's join, Plan 94's CPU setup and recovery, Plan 38's Linux provider with Agent adoption.
- **Slips first:** Plan 79, then Plan 38 past 38-09.
- **Other lanes:** Plan 67's PACK-B is already on `release/16/plan-93`; its open PRs (astrid-agent #701, astrid-app #413) belong to the H3 lane. Plan 93's join carries PACK-B; the H3 orchestrator lands the rest. Plan 38 owns the Runtime pin.
- **CI:** astrid-agent and astrid-runtime CI are shared with the H3 lane. Dispatch `ci.yml` once per plan, when it is ready, after checking the running runs.

## Owner only

- scope changes, including bringing a Release 17 row back;
- booking or using real machines, and anything that spends money or needs a GPU;
- publication.

## Start messages

**Manager launch** for Plan 79, posted on the board by the orchestrator for the owner to paste into a new Codex thread:

```text
You are r16-p79-manager, the ChatGPT dispatcher for Plan 79 in the dependable lane; sign comments r16-p79-manager. Follow the astrid-dev-orchestrator skill's multi-manager-dispatch workstream (install the skills from a banodoco/astrid-dev checkout: mkdir -p ~/.agents/skills && python3 scripts/astrid_dev.py skills install --destination ~/.agents/skills). Your brief is releases/16/briefs/dependable.md on banodoco/astrid-dev main; it wins over the workstream where they differ. Created by session <orchestrator session id>, signing dependable-orchestrator. Board: <board URL>. Use the Codex-app steps in the TOOLKIT comments on banodoco/astrid-dev#2030 for your hourly automation and for opening and resuming chats. First: create your hourly automation, read the board, and post one STATUS.
```

**Chat start message,** sent by a manager as the first message of each fresh chat, in the unit's mode:

```text
You are <chat name>, the ChatGPT author of ONE unit of the dependable lane. Follow agent/roles/manager/chatgpt-packet.md in banodoco/astrid-dev; the lane brief releases/16/briefs/dependable.md on main is your authority and wins where they differ.
Unit: <unit> in plans/<PP>-<slug>/tasks.md on main. Outcome: <one line>. May touch: <the card's Scope>, and the fixtures its tests pin to. Must not touch: anything else.
Repository: banodoco/<repo>. Base: release/16/plan-<PP> at <sha>. Commit on task/<PP>/<unit>, cut from that SHA, and push it. Open no pull request.
First check that your GitHub connector can read banodoco/astrid-dev and read and push banodoco/<repo>; if not, post BLOCKED.
Focused tests: <the card's proof command>. Run them here only if you can without cloning or building; otherwise say so. The orchestrator runs them on the merged tree.
Board: <board URL>. Post STATUS once your branch is pushed; end by posting READY-PROOF <repo> task/<PP>/<unit> <sha> <tests run, or "not run">, or BLOCKED <reason>. Keep each post short: what changed, the SHA, the tests. Then stop. Do not merge, tick tasks.md or start another unit.
```

**Continuation message,** sent by a manager into a chat that already holds an in-flight unit:

```text
From now on this unit runs under releases/16/briefs/dependable.md on banodoco/astrid-dev main, and you report to dependable-orchestrator on <board URL>. Finish the unit you have. Prove it with its focused tests only, and post READY-PROOF with the branch, SHA and tests, in a few lines. No archives, checksums or tree audits.
```

## Launch

The owner pastes this into a new thread in the Codex app, with Chrome signed in to the owner's ChatGPT account:

```text
Follow the astrid-dev-orchestrator skill (install the skills from a banodoco/astrid-dev checkout: mkdir -p ~/.agents/skills && python3 scripts/astrid_dev.py skills install --destination ~/.agents/skills). Your brief is releases/16/briefs/dependable.md on banodoco/astrid-dev main; you are dependable-orchestrator. Created by the owner. First: create your hourly automation, read the lane board, and post one STATUS.
```

Everything else, including opening the board first, is in this brief.

## Status

Read `python3 scripts/astrid_dev.py release status 16` and this lane's board. Do not keep a second copy here.
