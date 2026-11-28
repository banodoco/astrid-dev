# The golden path

What each session should do when it starts, written once so that [agent tests](README.md) can check it. Every line rests on a document or on one of the four rules below. A behaviour that rests on neither is not an expectation yet.

Gathered on 28 November 2026 by three read-only inventories (Lead, orchestrator and reviewer; managers and nesting; workers, chats and contributors) against `main` with Plan 108 merged. They found about thirty contradictions or gaps. Read for causes, those come down to four missing parent rules.

## Governing thought

**A session takes its authority, its hand-off and its clock from its run's brief, and does only what its host can do.** Role documents give defaults. The brief says what this run changes. The run contract's safety, proof and permission rules bind everyone.

## The four rules

Ranked by consequence times likelihood. Each lists the findings it settles.

### 1. Authority: the brief changes defaults, and says so

*Written into the [run contract](../agent/shared/run-contract.md#who-answers-for-a-run) on 28 Nov 2026.*

A role document states defaults. The run's brief (a lane brief, or a plan's `Run start` and `tasks.md` outside a lane) may change a default within the owner's go, and must name each change in its Roles, Merges or How it runs. A rule written for another lane or run does not bind this one. The run contract's safety, proof and permission rules win over both.

**Settles:**
- who merges into `release/<N>/main`;
- who may send a launch;
- whether an orchestrator sets its own check-in;
- whether an orchestrator may run units on a fallback;
- which sections of `releases/16/run.md` bind the H3 lane (its Delivery section binds only the Delivery lane);
- the Lead's gate in a lane that has its own.

### 2. Hand-off: one start message per edge, and one way back

*The way back is written into [start-session](../agent/shared/workstreams/start-session.md#procedure), step 7, on 28 Nov 2026.*

Every edge from a parent to a child (owner to Lead, owner to orchestrator, orchestrator to manager, manager or orchestrator to worker or chat, orchestrator to reviewer) has one start message. It lives in [start-session](../agent/shared/workstreams/start-session.md) for the general case, or in the brief for a lane. It names:
- what the child reads, and at which ref;
- the base SHA it starts from;
- its branch, named for the card or unit (`p<PP>/<id>`);
- that it commits its own work, and what it pushes and where; a PR into the plan branch starts as a draft and is marked ready at READY-PROOF;
- that whoever merges its work ticks the task in `tasks.md`, and it never does;
- how it returns: one milestone vocabulary;
- whom it escalates to: its creator, never a third session.

Role documents link to it and don't restate it.

**The milestone vocabulary:**
- **Workers and chats:** early STATUS, READY-PROOF, BLOCKED.
- **Reviewers:** ACCEPT, or HOLD with numbered findings. HOLD blocks the merge.
- **Managers and orchestrators:** hourly STATUS, with REQUEST and DECISION.

**Settles:**
- where the card is read;
- pinned base versus current head;
- branch names;
- draft or ready PRs, and who opens them;
- READY-PROOF, DONE and the return value;
- ACCEPT/HOLD versus BLOCKING/FOLLOW-UP/NOTE;
- the permission-prompt escalation target;
- who sends a chat's start message;
- launch lines missing the creator.

### 3. Clock: long-running roles check in, one-shot roles report

*Written into the [run contract](../agent/shared/run-contract.md#coordination-boards-and-check-ins), items 5, 7 and 8, on 28 Nov 2026.*

A long-running role (Lead, orchestrator, manager) sets an hourly check-in at start with its own host's scheduler. On Claude that is a scheduled task or `/loop`; in the Codex app, its automation tool. It names the check-in and its end condition in its first STATUS, never sets a second one when it wakes, and cancels it at the end condition, confirming none remain; no other session disables it. A one-shot role (worker, chat, reviewer) sets none and posts milestones only.

Liveness has one clock: a parent nudges a silent child at 2 hours, and at 3 hours resumes, replaces or falls back, and tells the owner. A child that nothing can wake (a Codex-app session, a ChatGPT chat) moves to the parent's fallback at that point.

**Settles:**
- "only when the owner asks" against "every Claude role" for check-ins;
- the 20-minute and hourly cadences;
- the 2, 3 and 6-hour thresholds;
- reviewer and worker check-ins;
- the missing reviewer fallback.

### 4. Host: what a session can do decides where work runs

A session that can't build doesn't run proofs: CI on the PR is the proof, and a plan's baseline comes from CI. A session with several repositories dispatches product commands rather than running them. A session commits and pushes only where its host can. Skills are installed only by a session that will follow them, never to orient someone.

**Settles:**
- whether a chat runs its tests;
- where the baseline runs;
- a multi-repository manager running proofs;
- a Codex manager's sandbox and commits;
- installing skills versus orienting a contributor.

## Each role's path

`[n]` cites the rule above; any other citation is the document line.

### Owner

- **Gives:** the go, by recording it on a brief, and every launch, by pasting the line ([start-session](../agent/shared/workstreams/start-session.md) step 5).
- **Decides:** the lane split ([leader](../agent/roles/leader.md)), scope, spending, publication, and a unit parked after one replacement.

### Release Lead

- **Brief:** the release brief's Included plans and the run board ([release](../agent/shared/workstreams/release.md)).
- **Lanes:** it proposes the lane split, and the owner chooses. It writes the briefs, and never sends a lane's launch ([leader](../agent/roles/leader.md)).
- **Check-in and posting:** hourly check-in [3]; posts on `board: release <N> lead`.
- **Code:** reads no code and runs no tests. It merges into `release/<N>/main` only where no lane brief takes that gate [1].

### Lane orchestrator

- **Brief:** its lane brief and the `tasks.md` files it links, nothing else ([lane-orchestrator](../agent/roles/orchestrator/lane-orchestrator.md)).
- **Start:**
  1. confirm its model;
  2. attach repositories;
  3. install skills [4];
  4. open `board: lane <lane>`, with its session id in the first post;
  5. create its hourly check-in [3];
  6. post STATUS 1;
  7. post the first progress PR;
  8. post the baseline from CI [4].
- **Delegates:** it gives each one the brief's start message [2]. A delegate it can't create (a Codex-app manager) gets a LAUNCH post for the owner to paste.
- **Code:** it doesn't write code itself. On the brief's fallback it runs units through workers [1]. It merges unit PRs into plan branches, and plan branches into `release/<N>/main` only if the brief gives it that gate [1].
- **Proof:** it runs no full suite locally. It answers READY-PROOF by checking CI against the unit's focused tests [4].
- **Escalation:** it brings only the brief's owner-only points to the owner.

### Manager outside a lane

- **Brief:** the plan's `Run start` and `tasks.md` ([manager](../agent/roles/manager.md)).
- **Start:** hourly check-in [3], then the plan's test inventory once, on the starting versions ([run contract](../agent/shared/run-contract.md#when-a-test-run-is-load-bearing)).
- **Workers:** one card each, through start-session's worker message [2].
- **Code and proof:** re-runs each task's focused proof, integrates and pushes to the plan or project branch. The full relevant suite runs on CI before review. It merges its own progress PRs; the release gate takes the rest [1].

### Codex-app manager (ChatGPT dispatcher)

- **Start:** started only by the owner's paste [2]. It installs skills into `~/.agents/skills` and creates its hourly automation [3].
- **Dispatch:** at most three chats, each from the chat start message [2], in the route's mode (N High, X Extra High, S Pro).
- **Limits:** it never runs proof, merges or rules [4]. It records the steps for a new mode the first time it uses one.

### Nested: a manager whose workers are managed

- **Integration:** each level integrates and pushes only its own children's work, into its own branch, and opens one PR to its parent's branch [2].
- **Workers:** a worker never pushes to a level above its creator.

### Worker (Claude session or subagent)

- **Reads:** its card, at the ref its start message names [2].
- **Branch and tests:** works on `p<PP>/<id>` from the pinned base, and runs only the card's focused tests [4].
- **Returns:** to its creator. Every worker runs only its card's focused tests and commits its own work. A worker session also pushes its branch and opens a draft PR; a subagent returns the commit SHA, and its creator pushes [2].
- **Check-in:** none [3].
- **Never:** merge, edit a test to pass, use AskUserQuestion, or touch a file outside its Scope. A needed file outside Scope is a BLOCKED naming the lines ([run contract](../agent/shared/run-contract.md#checks-and-failure-repair)).

### ChatGPT chat

- **Start:** checks that its connector can read astrid-dev and push the code repository [2].
- **Code and tests:** pushes `p<PP>/<id>` with a draft PR. It runs its focused tests only if it needn't build; otherwise CI is the proof [4].
- **Finish:** marks the PR ready at READY-PROOF, then stops.

### Reviewer

- **Start:** started by the orchestrator with the reviewer brief filled in. It is independent of the author.
- **Work:** reads the code and the CI results, and posts ACCEPT or HOLD on the lane board [2].
- **Limits:** no check-in [3]; pushes nothing.

### Contributor (astrid-dev-start, no assignment)

- **Start:** finds existing work first, then the smallest outcome ([start](../agent/start.md)). It installs nothing to orient itself [4].
- **Lands work:** in a focused PR linked to its issue or card, merged by a maintainer. For astrid-dev, that PR goes into `main`.

## Owner questions

1. Rule 1 makes the brief the place where a run's defaults change. Is that the line you want, rather than role documents listing lane exceptions?
2. Rule 3 sets one clock: nudge at 2 hours, act and tell you at 3. Does that replace the current 20-minute packet pass and 6-hour chat replacement?
3. HOLD from a reviewer blocks a merge. Yes?
