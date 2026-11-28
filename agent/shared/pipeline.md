---
description: How work moves from a vision gap to a published release, who does what at each level, and how branches and pull requests are used.
---

# The pipeline

How work moves from a vision gap to a published release, who holds it at each step, and how it is committed. This is the one overview; each step links the page with the detail, and the [run contract](run-contract.md) holds the rules on safety, proof and permission that bind every step.

**In one paragraph.** Work goes down one start message at a time and comes back one commit at a time. The owner decides scope, the lane split, every go and publication. The Lead runs the release and is the only session that merges into `release/<N>/main`. A lane orchestrator, or outside a lane a plan's manager, is the plan's accountable agent: it runs its tasks and is the only session that writes its plan branch. Workers and chats do one task each, push it, and never merge. Whoever runs a level closes it, and each level's `done` needs the level below. astrid-dev holds every record; the product repositories (astrid-agent, astrid-app, astrid-runtime and the others a release lists) hold only code, on the branches below.

## The steps

1. **Gap to plan.** A gap says what must improve; a plan says what is built. A scope PR adds the plan's `plan.md`, `inputs.md` and `tasks.md`, and the owner's greenlight sets its Scope decision to `Accepted` ([plan](workstreams/plan.md)). *What goes wrong:* a plan without an exact proof per task, so its worker invents one.
2. **Plan to release.** The owner chooses what a release ships. The Lead lists the plans in `releases/<N>.md` and cuts `release/<N>/main` and each plan's branch ([release](workstreams/release.md)). *What goes wrong:* a branch cut before the repository's allow rules let workers push.
3. **Release to lanes.** The Lead proposes two or three ways to group the plans; the owner chooses. The Lead writes each lane's brief, the owner records the go in it and sends the launch ([lanes](../roles/leader/lane-orchestrators.md)). *What goes wrong:* a brief that assumes something its repositories don't do; run its [agent tests](workstreams/improve.md#agent-tests) and check its proof against the repository's CI before the go.
4. **Lane to tasks.** The accountable agent keeps the queue moving: it starts each ready task with one start message ([start-session](workstreams/start-session.md#procedure) step 7) and checks in hourly. *What goes wrong:* a silent session; the [liveness clock](run-contract.md#coordination-boards-and-check-ins) nudges at 2 hours and acts at 3.
5. **Task to plan branch.** The worker pushes its task branch and posts READY-PROOF; the accountable agent merges it, proves the merged tree and ticks it ([branches and pull requests](#branches-and-pull-requests)). *What goes wrong:* a stale base when tasks run in parallel, which is why the proof runs on the merged tree; a needed file outside Scope, which is a BLOCKED naming the lines.
6. **Plan to release branch.** The accountable agent makes the plan ready and opens one PR per repository into `release/<N>/main`; the Lead merges it, then the accountable agent opens the plan's completion PR. *What goes wrong:* two plans landing at once; the Lead merges one at a time and announces each, and the others merge forward.
7. **Release to users.** The Lead freezes, qualifies and, with the owner's go, publishes ([release](workstreams/release.md)).

## Who does what

| Level | Record | States | Opened by | Run by | Merges | Closed by |
| --- | --- | --- | --- | --- | --- | --- |
| **Release** | `releases/<N>.md`: `**State:**` and `## Branches` | `Draft`, `Final` | the Lead, from the template; the owner chooses what it ships | the Lead | each ready plan PR into `release/<N>/main`, one at a time | the Lead, after the owner's go to publish |
| **Lane** | `releases/<N>/briefs/<lane>.md`: `**State:**`, `**Go:**` | `prepared`, `running`, `paused`, `done` | the Lead writes the brief; the owner records the go and sends the launch | its orchestrator | (its plans' merges) | its orchestrator, once every plan is `done`: State `done`, manager stopped, check-in cancelled, a closing note to the Lead |
| **Plan** | `plans/<PP>-<slug>/plan.md`: `**Status:**`, `**Owner:**` | `queued`, `active`, `blocked`, `paused`, `done`, `cancelled` | a scope PR the owner greenlights | its accountable agent | task branches into its plan branch | its accountable agent's completion PR, after the Lead merges the plan |
| **Task** | a row of `tasks.md`: its Progress cell | `[ ]`; `[x]` with its merge; or a disposition such as `blocked: <reason>` | its accountable agent, by a start message | one worker: a session, a subagent or a ChatGPT chat | nothing | the accountable agent ticks it in its next progress PR; a worker never edits `tasks.md` |

## Branches and pull requests

1. **Pull requests go only into gated branches:** `release/<N>/main` in a product repository, `main` in astrid-dev. Nothing else gets one.
2. **One task, one branch, one author.** The worker commits on `task/<PP>/<id>`, cut from the plan branch at the SHA its start message pins, pushes it, and posts `READY-PROOF <repo> <branch> <sha> <tests run, or "not run">` on its board. A subagent works in a worktree its creator names, returns the SHA, and its creator pushes.
3. **Only the accountable agent writes a plan branch.** In a scratch worktree it merges the task's SHA into the plan branch's current head with `git merge --no-ff -m "Merge P<PP>-<id>: <title>"`, runs the task's focused proof on that merged tree, pushes, posts `MERGED <id> <merge sha>`, and deletes the task branch. If the proof fails it discards the worktree, pushes nothing, and sends the failure back to the author. `git log --first-parent release/<N>/plan-<PP>` is then the plan's task list.
4. **Reviews are by SHA.** A reviewer reviews a head SHA; its verdict goes on the board and its findings become `tasks.md` rows.
5. **One plan PR per plan per repository.** When a plan's tasks are merged and its review stop accepted, the accountable agent merges `release/<N>/main` forward, runs the repository's full CI on that head (`workflow_dispatch` of `ci.yml`, once), opens the PR into `release/<N>/main` and posts it on the Lead's board. A plan that changes several repositories posts its PRs in merge order.
6. **astrid-dev records:** one scope PR and one completion PR per plan, and at most one progress PR per lane (or per plan outside a lane) at each hourly check-in, only when state changed. They auto-merge on a passing check; the completion PR needs independent review.
7. **Undo a task with `git revert -m 1 <merge sha>`** on the plan branch; history is only added to.
