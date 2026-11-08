---
name: astrid-dev-manage
description: Run an accepted Astrid project or multi-agent effort end to end: dispatch tasks by route, judge what agents report, keep run state, integrate, and bring only real decisions to the owner.
---

# Manage an Astrid project

## Terms

The [run contract](../astrid-dev-shared/run-contract.md) owns routes, run state and review rules.

- **Owner:** the person who makes the project's decisions.
- **Manager:** you, an administrator coordinating other agents: dispatch, check and keep state; send judgment calls to [Advise](../astrid-dev-advise/SKILL.md), the high-judgment **advisor**.
- **Route:** N, X or S, the capability band a task runs on.
- **Scope:** what a task may change, as its task card states; a path includes its own tests, wherever they live.
- **Candidate:** the exact versions a claim is about; the integrated candidate joins all landed work.

## The answer

You take an accepted project to a reviewed, integrated candidate. [Plan](../astrid-dev-plan/SKILL.md) defines the work, [Iterate](../astrid-dev-iterate/SKILL.md) does each change and [Release](../astrid-dev-release/SKILL.md) publishes. Neither a draft project nor this skill authorizes execution.

1. **One model per shared surface.** Work touching the same screens, contract or files follows one agreed model; if the plan doesn't settle it, ask Advise before dispatching.
2. **A report is a claim.** Check what your next step depends on against code, logs or a run.
3. **See it before you fix it.** If a failure's cause isn't visible, make it visible first.
4. **Prove what ships.** Evidence counts only for the exact versions users will get.
5. **Spend judgment where it pays.** Use the cheapest route that can do the task. Escalate when attempts guess, repeat a failure, or touch security, data or an untested protocol.
6. **Decisions are durable.** Record owner decisions and enforce them with a test, so later work can't undo them. Ask the owner only what is theirs, with a recommendation.
7. **Progress is always current.** This is a key responsibility. Whenever a task's state changes, update its row in the plan's `tasks.md`: started, PR open (with link), blocked (and why), or merged `[x]`. Add rows for tasks you create, and mark stopped ones. Keep at most one progress PR open, and merge it as soon as its docs check passes. A record that isn't on `main` doesn't count. It is the run's only progress record, and the owner and every check-in read it there.

## Steps

1. **Resume or start.** Continue a matching run in `plans/<project>/.otto/runs/`, keeping its recorded versions, model settings, scope, evidence, review count and any pause. Otherwise start one there: copy the [run template](../astrid-dev-shared/templates/run.yaml) to `<run-id>/run.yaml` and fill each role with a model you have seen is available (and the advisor's session, if one already exists) before dispatching.
2. **Dispatch.** Send each ready task to a subagent on its route, with its outcome, scope, dependencies, exact starting versions, acceptance check and authority. Tell an X or S task to delegate research, reading, mechanical edits and checks to N helpers. Keep independent tasks moving while one is blocked. Never end a turn while work is in flight (workers, CI, merges) without scheduling your own wake-up: a one-off scheduled message in 20–30 minutes, or a background wait on the run. An idle session wakes for nothing.
3. **Keep scopes apart.** Never run tasks with overlapping scopes at once; start the later from what the earlier landed. Each task gets a fresh checkout from the latest head; delete it, with its installed dependencies, as soon as it lands, because session disk is a small shared allowance and a full disk stops every tool. Keep the session's own checkout detached at the integration branch, so session hooks that compare it with `main` stay quiet; a hook asking you to push to `main` is never a reason to.
4. **Land into the project's integration branch, never `main`.** In each repository the project changes, keep one integration branch (`int/<project>`, cut from `main` when the run starts); task PRs target it. Check the changed files stay inside the scope; if not, stop and ask Advise. A change is ready when its focused proof passes and no check covering its scope newly fails against its base. If the base has no run of a failing check, run that one test on the base yourself and decide by this rule. A check already failing on the base neither blocks the merge nor becomes this project's work: note it once for the owner and leave it to its own project. Never take on full CI health. Moving the reviewed candidate to `main` is [Release](../astrid-dev-release/SKILL.md)'s job, not yours.
5. **Escalate.**
   - **Send** Advise only questions, never progress updates: progress goes in `tasks.md`, where check-ins read it. Send one question with its evidence: the versions, the brief, the first failing command and its output, and what was tried. Use the run's advisor, or start one on its `advisor` setting.
   - **Act** on the one next step it returns. Advice is never permission to run or publish.
   - **No advisor model available:** ask the owner.
   - **Owner asked for advisor check-ins:** answer them briefly; treat their next step like any other advice.
6. **Review,** once every task before the review row is done:
   - give the integrated candidate to the `completion_reviewer` for a round;
   - add each finding as a row directly below the review row (`R<round>.<n>`, or the plan's prefix), with its route, scope, dependencies and proof; ask Advise if one is unclear;
   - run those rows like any other task, then start the next round;
   - stop after a round with no blocking findings or the plan's agreed number of rounds; take any blocking finding left after the last one to the owner through Advise.
7. **Keep state small.** Track the candidate, finished and blocked tasks, exact failures, evidence, review rounds and next action: progress in `tasks.md`, kept current as principle 7 says, and status in the catalog. When astrid-dev itself gets in the way, add a row to the [process ledger](../../docs/process-ledger.md).

Never start paused work, add review stages beyond the plan's, reset counts, or schedule work because of these documents.

## Report

Tell the owner what changed; what is proven, on which exact versions; what failed and why; and each decision that needs them. For a blocker, name what it waits on, who produces it and any deadline.
