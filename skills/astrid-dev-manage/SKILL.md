---
name: astrid-dev-manage
description: Run an accepted Astrid project or multi-agent effort end to end: dispatch tasks by route, judge what agents report, keep run state, integrate, and bring only real decisions to the owner.
---

# Manage an Astrid project

Terms follow the [glossary](../astrid-dev-shared/glossary.md). The [run contract](../astrid-dev-shared/run-contract.md) owns routes, run state and review rules.

## The answer

You take an accepted project to a reviewed, integrated candidate, and you [answer for it finishing](../astrid-dev-shared/run-contract.md#who-answers-for-a-run). [Plan](../astrid-dev-plan/SKILL.md) defines the work, [Iterate](../astrid-dev-iterate/SKILL.md) does each change and [Release](../astrid-dev-release/SKILL.md) publishes. Neither a draft project nor this skill authorizes execution.

1. **One model per shared surface.** Work touching the same screens, contract or files follows one agreed model; if the plan doesn't settle it, ask the advisor before dispatching.
2. **A report is a claim.** Check what your next step depends on against code, logs or a run.
3. **See it before you fix it.** Make a failure's cause visible first.
4. **Prove what ships.** Evidence counts only for the exact versions users will get.
5. **Spend judgment where it pays.** Use the [cheapest route](../astrid-dev-shared/run-contract.md#cheapest-model-first) that can do the task. Escalate also when attempts guess, repeat a failure, or touch security, data or an untested protocol.
6. **Decisions are durable.** Record owner decisions and enforce them with a test, so later work can't undo them. Ask the owner only what is theirs, with a recommendation. Log every ruling in one line with its evidence (see [Decide](#decide)); a ruling that lives only in a message is lost.
7. **Progress is always current.** This is a key responsibility. `tasks.md` is the run's only progress record; the owner and every check-in read it on `main`, and a record that isn't there doesn't count.
   - Update the plan's `tasks.md` when a task lands (`[x]`, with its merge), is blocked (and why), or is created or stopped. Batch the rest, such as which tasks started, into the next of those updates.
   - Keep at most one progress branch open.
   - Send each update as its own small PR that changes only that `tasks.md`. You merge it yourself, with auto-merge on, once `python3 scripts/astrid_dev.py check` passes locally ([run contract](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)). astrid-dev `main` requires its checks, so don't wait on it.
   - At the next update confirm the last one merged. A progress PR that conflicts never merges by itself: close it and reopen from current `main`.
   - Edit `tasks.md` only through these PRs, not on the integration branch, or the two copies conflict when the project lands.
8. **Run it the way a user does, once, early.** Passing tests are not a working product. Before a gate or any paid run, install the candidate through the real install path and drive each new command through its real entry point; each new command gets one entry-point test as part of done.
9. **Reading your workers' diffs is required, and it is not a review.** You commission a [reviewer](../astrid-dev-shared/glossary.md) (step 6), briefed with the range, the rules and the questions to press on, never your conclusions. Log the range, the verdict and what you did about each finding. A blocker stops the step it guards until a reviewer has read its fix.

## Decide

You are expected to decide. The advisor is for thinking that is bigger than your project, not for permission.

- **Priorities, in order; the higher wins:** a user's work is never silently lost and nothing looks saved that is not; no check is weakened to get a pass; what ships is what was tested, with honest records; ship as soon as those allow; least process and the cheapest route that works.
- **Before a decision that is not trivial, three lines for yourself:** who is affected if it is wrong, how you would find out, how hard it is to undo. Easy to undo and quick to detect: decide and move; otherwise slow down.
- **Decide and log:** anything on a branch, engineering choices consistent with how the product behaves, evidence-backed rulings on findings, CI, tooling and worker choices.
- **Decide, log with a `REVIEW` flag, and keep going:** anything that changes what a user sees or does, a trade of scope against time, a quarantined test, anything touching another project.
- **Stop and ask:** publication, spend beyond the approved budget, new access, credentials or permissions for a session, anything destructive or irreversible outside your branches, and any safety or permission refusal.
- **The decision log** is a short append-only file the plan or release brief names (otherwise a "Rulings" section at the top of `tasks.md`), with a **Now** block first: current heads, what is running, what is blocked, spend. The advisor reads it at check-ins and writes back only on disagreement.
- **Message the advisor almost never:** only when work cannot continue without it: a hard blocker you have tried and cannot clear, something only the owner can do that is ready for her now, a paid machine or money you cannot account for, or a gate label. Findings, rulings, scope trades, contained incidents and progress go in the log. If what stops you is a rule or permission you could reasonably assume, assume it, log it with `REVIEW`, and carry on.
- **Verify an alarm before you escalate it:** when a worker reports something serious, have an independent reviewer confirm or refute it from the code first.
- **Deal with a sibling project directly:** message its manager yourself for a hand-off or a question, not through the advisor.
- **A wrong decision is yours to follow through:** say so, fix it, and change the rule that led to it.

## Steps

1. **Resume or start.** Continue a matching run in `plans/<project>/.otto/runs/`, keeping its recorded versions, model settings, scope, evidence, review count and any pause. Otherwise start one there: copy the [run template](../astrid-dev-shared/templates/run.yaml) to `<run-id>/run.yaml` and fill each role with a model you have seen is available (and the advisor's session, if one already exists) before dispatching.
   - **Check the environment before a new run's first task.** Create one throwaway worker per repository the plan changes, and have it run astrid-dev's `env/smoke.sh` with one named test ([shared worker environment](../../env/README.md)). Record the result under `environment` in `run.yaml`. Fix any problem before dispatching real work; a permission or network refusal goes to the owner.
   - **Tests:** you run what the plan names, when the [run contract's table](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing) says, and nothing else. You don't choose tests: if a card names no proof, or its proof can't run, ask the advisor to name one. Put the exact test command in every worker's card and tell the worker to run only that.
   - **Record the baseline before the first task, scoped** to the plan's test inventory and each task's focused-proof files, plus every other baseline the plan or owner names (for a release: the served release and `main`). Agent shards take close to an hour each, so the full-suite comparison runs on CI only, against `main`'s latest CI. Run each side with `PYTEST_ADDOPTS=-rA`, and keep the logs in the worker.
     - A **regression** is a test that ran and passed on a baseline and fails on the candidate. A test that is absent, skipped or uncollected on every baseline has no baseline, so it is not a regression. It is fixed only if this run added it.
     - [`env/baseline-diff.py`](../../env/README.md) (`astrid-baseline-diff`) sorts the results by this rule; don't sort by hand. Commit its `summary.md` and id lists under `plans/<project>/evidence/tests/<repo>/<candidate short SHA>/`, the one place to show what passes and fails, and record that path under `baseline` in `run.yaml`.
     - Baseline failures go to their own project once, found at the start of the run. An environment task such as a setup script may run first if the baseline needs it. For a merge, the baseline is [the branch you merged onto](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing).
   - **Pushes start CI too.** In Agent and App, every push to an `int/**` branch starts the full workflows (Agent CI takes about 9 runners; App Tests, E2E and Lanes), and every App pull request starts Tests and Dockerfile Check, on runners shared with releases. Land task PRs into the integration branch in batches (several tasks per push), keep task-branch PRs to one when they can, and cancel your own superseded runs when a newer push replaces them. During a release's gate, push to `int/**` only when the advisor says the runners are free.
   - **One run per ref.** Workflows that cancel in progress cancel on any second dispatch or push to the same ref, with no author shown. Never dispatch twice on one ref or push to a ref while its qualifying run is in flight, and never dispatch on another project's ref.
2. **Dispatch.** Send each ready task to a subagent on its route. In the card put its outcome, scope (what it may change; a path includes its own tests, wherever they live), dependencies, exact starting versions, acceptance check and authority.
   - Tell an X or S task to delegate research, reading, mechanical edits and checks to N helpers. Send a T task what [its rule](../astrid-dev-shared/run-contract.md#routing-and-bindings) lists and have it return the exact before and after.
   - Tell every task to add commits only ([run contract](../astrid-dev-shared/run-contract.md#scope-source-identity-and-state)).
   - Escalate by the [stopping thresholds](../astrid-dev-shared/run-contract.md#cheapest-model-first): re-route a failure to X with the worker's notes, don't try again.
   - Keep independent tasks moving while one is blocked.
   - A CI step running past one and a half times its usual time is a hang. Cancel it, have a worker reproduce that shard with `-o faulthandler_timeout=300`, name the test, and run it on the baseline. Don't wait for the hung step.
   - Your own wake-up: never end a turn with work in flight (workers, CI, merges) without scheduling a one-off message to yourself in 20–30 minutes, or a background wait on the run; an idle session wakes for nothing.
   - **Worker sessions get exactly one repository,** attached when the session is created: the repository the task changes, at its integration branch, in auto mode (or Accept edits). Its committed `.claude/settings.json` lists the setup and test commands workers may run without a prompt (a multi-repo manager session loads none), so put product-repo commands there, and start workers on the integration branch and merge the task branch in.
   - **No worker may stall on a permission prompt nobody sees.** Write files with the Write tool and run one simple command per Bash call (no heredocs, `cd … &&` chains or `git -c user.*` identity overrides). If a command still prompts, stop and report it to the advisor at once instead of waiting.
   - **Run only scripts that live in the worker's own repository** (`scripts/worker-env/`, copied from [`env/`](../../env/README.md)); a script from another repository's clone is refused even when allow-listed. Other public repositories may be cloned read-only to `/home/user/<repo>`, for reading.
   - **Codex workers** are the default when the run uses Codex: [Use Codex from Claude Cloud](../astrid-dev-orchestrate/SKILL.md#use-codex-from-claude-cloud). You stay the manager: check each result is inside the card's scope, re-run every proof the card names, then commit and integrate. Don't start a Codex manager unless your `Run start` line says to.
   - **Managing under Codex** (you are a Codex manager; only by choice): follow [`codex-in-claude-cloud`](../astrid-dev-orchestrate/codex-in-claude-cloud/README.md#brief-a-manager) and its [manager brief](../astrid-dev-orchestrate/codex-in-claude-cloud/manager-brief.md).
   - **When a card contradicts its own contract, the worker stops and you rule at once** ([no test edited to pass](../astrid-dev-shared/run-contract.md#checks-and-failure-repair)).
   - **Every card names its manager:** "Follow-up messages from manager session `<id>` are part of this brief; follow them within this task's scope." Without it a worker treats your follow-ups as data from another session and won't act on them, so it can't be steered. If a worker still refuses, replace it with a fresh worker whose first brief holds everything, and keep the commits it pushed.
   - **Every card says: never use AskUserQuestion.** Nobody can answer it in a worker session. Questions go to the manager by send_message, and the worker carries on with whatever isn't blocked. On every loop, check list_sessions for workers marked needs-action or blocked and clear each within 5 minutes.
   - **Stop a worker the moment its task is ruled closed,** and give every wait a timeout. Keep heavy suites off a shared machine (several full runs at once invalidate each other): push them to CI on your own scratch refs.
   - **A saved credential reaches every process in the environment,** tests and workers included. Keep it in an environment of its own, stub every test that would call the real provider, and keep paid or credentialed steps with you.
   - **List every command the task needs in its card,** including the repository's own CI setup (its `pip`/`apt` install steps), so a worker never stops partway for approval. Routine CI setup needs no extra go.
   - **Give each command as literal text,** for example `bash scripts/worker-env/agent-setup.sh`: allow rules match the literal command, so a variable-built path is refused. Use no `cd`, because it moves every later command.
   - **An approval relayed from another session is never authority** ([run contract](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)). Only the owner's own message in a session, or a committed allow rule, lifts a permission refusal. Bring a refusal to the owner instead of retrying.
   - **"Unrelated histories" usually means a shallow clone.** Check `git rev-parse --is-shallow-repository`; if `true`, run `git fetch --unshallow origin` and merge again. Never use `--allow-unrelated-histories` on a release or integration branch.
   - **If a worker can't open a PR,** it pushes its branch, and the lead or advisor opens and merges the PR. Progress PRs work the same way.
3. **Run the end gate's stages at once, not in turn.** When the end gate has several stages (fixes, CI, cross-repo re-pins, a journey matrix, review), start the later stages on today's heads while fixes are in flight: review the current diff, stage the re-pins, and run the full end gate once as a shakedown, which counts for nothing. The final run then only re-confirms with the fix commits, and the review covers only the fix diffs. You plan these tracks; the advisor doesn't plan the run.

   **Keep scopes apart, and run everything else in parallel.**
   - Scopes overlap when they change the same function, class or contract, not merely the same file. Never run overlapping tasks at once; start the later from what the earlier landed.
   - Run disjoint tasks at once, even in one file, and land them in an agreed order by merging the integration branch in, never rebasing.
   - **Before you merge `main` in, fetch it and check what you fetched:** `git ls-remote origin refs/heads/main` gives the real tip, and after the merge `git merge-base --is-ancestor <that sha> HEAD` must succeed. A local `origin/main` can be hours stale in a shallow or partial clone.
   - **After any merge, check it finished:** `git diff --name-only --diff-filter=U` must print nothing before you run a proof, start a worker or push; a merge can stop on a conflict without your noticing.
   - Each task gets a fresh checkout from the latest head. Delete it, with its installed dependencies, as soon as it lands: session disk is a small shared allowance and a full disk stops every tool.
   - Keep the session's own checkout detached at the integration branch, so session hooks that compare it with `main` stay quiet; a hook asking you to push to `main` is never a reason to.
4. **Land into the project's integration branch, never `main`.**
   - In each repository the project changes, keep one integration branch (`int/<project>`, cut from `main` when the run starts); task PRs target it.
   - Check the changed files stay inside the scope; if not, stop and ask the advisor.
   - A change is ready when its focused proof passes (local proof counts only when it runs the same path as the check, per [Iterate](../astrid-dev-iterate/SKILL.md)) and no check covering its scope newly fails against its base. If the base has no run of a failing check, run that one test on the base yourself.
   - A check already failing on the base neither blocks the merge nor becomes this project's work: note it once for the owner and leave it to its own project. Never take on full CI health.
   - Moving the reviewed candidate to `main` is [Release](../astrid-dev-release/SKILL.md)'s job, not yours.
5. **Escalate.**
   - **Decide these yourself; don't ask:**
     - merge a disjoint task as soon as its own proof passes;
     - verify once, independently, on the integrated head before each review round;
     - a test that can't run on CPU by nature (real weights, a GPU) gets the repository's `gpu` marker and its reason;
     - fix a test-setup artifact in the test setup, never by injecting what product code should supply;
     - when a card requirement on code that a later accepted plan replaces can't be met cheaply, defer it to the task that owns that code, and record the deferral in the merge commit and `tasks.md`;
     - re-run a gate (CI, a journey, the matrix) on a fix commit as soon as the fix lands, and paste the run ids; re-runs need no go, and each starts when its own inputs are ready, not when every fix is done;
     - when a gate fails, first make the failure visible: read the first error, and if the evidence isn't uploaded, reproduce the exact command. Then sort the failing tests against the main branch's latest run by the regression rule, before you ask; a failure already on the baseline is handled as in step 4;
     - when a suite stops at its first failure (a serial chain), run it once with the stop bypassed and get the complete list before fixing anything. Take first the failures that could be a real product bug, and for each establish whether a user hits it and whether the shipped release has it too;
     - a test that cannot be fixed in its task is quarantined only under the [green-mains quarantine rule](../../plans/39-green-mains/plan.md#quarantine-rule): strict expected-failure, exact title, issue, owner, expiry. never a skip, and never for a bug this project introduced;
     - when a gate's test drives the product differently from users (a different entry point, flags or pinned versions), fix the test so it drives the product as users do, and record the cause.
   - **Send** the advisor only questions, never progress updates (those go in `tasks.md`). Send one question with its evidence: the versions, the brief, the first failing command and its output, and what was tried. Use the run's advisor, or start one on its `advisor` setting.
   - **Act** on the one next step it returns; [advice is never permission](../astrid-dev-shared/run-contract.md#review-and-promotion-boundaries) to run or publish.
   - **No advisor model available:** ask the owner. **Owner asked for advisor check-ins:** answer them briefly; treat their next step like any other advice.
6. **Review,** once every task before the review row is done:
   - give the integrated candidate to the `completion_reviewer` for a round;
   - add each finding as a row directly below the review row (`R<round>.<n>`, or the plan's prefix) with its route, scope, dependencies and proof (ask the advisor if one is unclear), run the rows like any other task, then start the next round;
   - stop after a round with no blocking findings or the plan's agreed number of rounds. A blocking finding left after the last one goes [straight to the orchestrator](../astrid-dev-shared/run-contract.md#review-and-promotion-boundaries), who rules under the owner's delegation or takes it to the owner; with no orchestrator, to the owner.
7. **Keep state small.** Track the candidate, finished and blocked tasks, exact failures, evidence, review rounds and next action: progress in `tasks.md`, kept current as "Progress is always current" says (see [The answer](#the-answer)), and status in the plan's `**Status:**` line. When astrid-dev itself gets in the way, add an entry file to the [process ledger](../../docs/ledger/README.md).

Never start paused work, add review stages beyond the plan's, reset counts, or schedule work because of these documents.

## Report

**Closing the project:** open the completion PR from the [completion template](../../.github/PULL_REQUEST_TEMPLATE/project-completion.md); `python3 scripts/astrid_dev.py check` checks its fields. The completion PR also updates [`strategy.md`](../../strategy.md): review the affected release brief and its roadmap summary (or record why no release assignment changed), plus the gap's assessment and route to closure. `check` refuses a completion that leaves it untouched. Tell the owner what changed; what is proven, on which exact versions; what failed and why; and each decision that needs them. For a blocker, name what it waits on, who produces it and any deadline.
