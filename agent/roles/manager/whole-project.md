---
description: Manage a complete accepted plan, including worker coordination, tested integration, progress records and project closure.
---

# manage a whole project

## When to use

When one accountable Manager is assigned the full plan run rather than an isolated fresh-session packet.

## Outcome

An accepted project managed through verified task delivery, integrated progress and an owner-reviewable completion record.

## Inputs

The accepted plan and tasks, current run identity, named owner, working repositories, dependencies, proof requirements and permissions.

## Procedure

Keep task progress current, make scope decisions within authority, coordinate implementation and proof, integrate work and report accurately.

## Completion

Accepted tasks and completion evidence are recorded in the project's canonical files, or precise blockers remain visible for the owner.

Use when you are the **one accountable manager** for an accepted Astrid plan run, rather than a short-lived [ChatGPT packet manager](chatgpt-packet.md). Apply the [general Manage principles](../manager.md) and the [run contract](../../shared/run-contract.md). The project pack owns scope and acceptance; don't create another queue.

## Progress is always current

7. **Progress is always current.** This is a key responsibility. `tasks.md` is the run's only progress record; the owner and every check-in read it on `main`, and a record that isn't there doesn't count.
   - Update the plan's `tasks.md` when a task lands (`[x]`, with its merge), is blocked (and why), or is created or stopped. Batch the rest, such as which tasks started, into the next of those updates.
   - Keep at most one progress branch open.
   - Send each update as its own small PR that changes only that `tasks.md`. You merge it yourself, with auto-merge on, once `python3 scripts/astrid_dev.py check` passes locally ([run contract](../../shared/run-contract.md#who-answers-for-a-run)). astrid-dev `main` requires its checks, so don't wait on it.
   - At the next update confirm the last one merged. A progress PR that conflicts never merges by itself: close it and reopen from current `main`.
   - Edit `tasks.md` only through these PRs, not on the plan branch, or the two copies conflict when the project lands.

## Decide

You are expected to decide. The advisor is for thinking that is bigger than your project, not for permission.

- **Priorities, in order; the higher wins:** a user's work is never silently lost and nothing looks saved that is not; no check is weakened to get a pass; what ships is what was tested, with honest records; ship as soon as those allow; least process and the cheapest route that works.
- **Before a decision that is not trivial, three lines for yourself:** who is affected if it is wrong, how you would find out, how hard it is to undo. Easy to undo and quick to detect: decide and move; otherwise slow down.
- **Decide and log:** anything on a branch, engineering choices consistent with how the product behaves, evidence-backed rulings on findings, CI, tooling and worker choices.
- **Decide and flag `REVIEW` only within existing authority:** reversible, in-scope user-facing choices and coordination with a sibling project. Log the candidate, evidence and proposed disposition; the flag is not permission to change accepted scope, quarantine or weaken a test, override a refusal or affect another project's work without its owner's go. For those cases, stop dependent work and ask.
- **Stop and ask:** publication, spend beyond the approved budget, new access, credentials or permissions for a session, anything destructive or irreversible outside your branches, and any safety or permission refusal.
- **The decision log** is a short append-only file the plan or release brief names (otherwise a "Rulings" section at the top of `tasks.md`), with a **Now** block first: current heads, what is running, what is blocked, spend. The advisor reads it at check-ins and writes back only on disagreement.
- **Message the advisor almost never:** only when work cannot continue without it: a hard blocker you have tried and cannot clear, something only the owner can do that is ready for her now, a paid machine or money you cannot account for, or a release label the release brief names (such as A-FROZEN). Findings, rulings, scope trades and contained incidents go in the log, progress in `tasks.md`. Send one question with its evidence: the versions, the brief, the first failing command and its output, and what was tried. Use the run's advisor, or start one on its `advisor` setting. If a rule or permission is missing or refused, do not assume it: stop dependent work, record the exact request and ask the owner or authorized decision maker. Continue only independently authorized work.
- **Verify an alarm before you escalate it:** when a worker reports something serious, have an independent reviewer confirm or refute it from the code first.
- **Deal with a sibling project directly:** message its manager yourself for a hand-off or a question, not through the advisor.
- **A wrong decision is yours to follow through:** say so, fix it, and change the rule that led to it.

## Steps

1. **Resume or start.** Your release is the brief whose `## Included plans` lists your plan; its release manager is named there. A plan in no release does not start **unless it is a self-contained astrid-dev-only project**: the owner can explicitly approve and start that project without assigning a product release. This exception never applies when any other repository changes or a release needs integration; use the release branch and the named Lead in those cases. A qualifying dev-only run begins at the current `main` head on `project/<PP>-<slug>` and records its exact base, authority and integration destination in `inputs.md`; task branches target that project branch. No approval is implied by creating a plan. Continue a matching run in `plans/<project>/.otto/runs/`, keeping its recorded versions, model settings, scope, evidence, review count and any pause. Otherwise start one there: copy the [run template](../../shared/templates/run.yaml) to `<run-id>/run.yaml` and fill each role with a model you have seen is available (and the advisor's session, if one already exists) before dispatching.
   - **Check the environment before a new run's first task.** Create one throwaway worker per repository the plan changes, and have it run astrid-dev's `env/smoke.sh` with one named test ([shared worker environment](../../../env/README.md)). Record the result under `environment` in `run.yaml`. Fix any problem before dispatching real work; a permission or network refusal goes to the owner.
   - **Tests:** you run what the plan names, when the [run contract's table](../../shared/run-contract.md#when-a-test-run-is-load-bearing) says, and nothing else. You don't choose tests: if a card names no proof, or its proof can't run, ask the advisor to name one. Put the exact test command in every worker's card and tell the worker to run only that.
   - **Record the baseline before the first task, scoped** to the plan's test inventory and each task's focused-proof files, plus every other baseline the plan or owner names (for a release: the served release and `main`). Agent shards take close to an hour each, so the full-suite comparison runs on CI only, against `main`'s latest CI. Run each side with `PYTEST_ADDOPTS=-rA`, and keep the logs in the worker.
     - A **regression**, and sorting results with [`env/baseline-diff.py`](../../../env/README.md), are defined in the [run contract](../../shared/run-contract.md#when-a-test-run-is-load-bearing). Commit its `summary.md` and id lists under `plans/<project>/evidence/tests/<repo>/<candidate short SHA>/`, the one place to show what passes and fails, and record that path under `baseline` in `run.yaml`.
     - An environment task such as a setup script may run first if the baseline needs it.
   - **Some pushes and pull requests start CI** ([which](../../shared/workstreams/green.md#using-github-actions)), on runners shared with releases. Land task PRs into the plan branch in batches (several tasks per push), keep task-branch PRs to one when they can, and cancel your own superseded runs when a newer push replaces them. During a release's gate, push to `release/*/main` only when the release manager says the runners are free.
   - **One run per ref.** Workflows that cancel in progress cancel on any second dispatch or push to the same ref, with no author shown. Never dispatch twice on one ref or push to a ref while its qualifying run is in flight, and never dispatch on another project's ref.
2. **Dispatch.** Send each ready task to a subagent on its route. In the card put its outcome, scope (what it may change; a path includes its own tests, wherever they live), dependencies, exact starting versions, acceptance check and authority.
   - Tell an X or S task to delegate research, reading, mechanical edits and checks to N helpers. Send a T task what [its rule](../../shared/run-contract.md#who-answers-for-a-run) lists and have it return the exact before and after.
   - Tell every task to add commits only ([run contract](../../shared/run-contract.md#scope-source-identity-and-state)).
   - Escalate by the [stopping thresholds](../../shared/run-contract.md#cheapest-model-first): re-route a failure to X with the worker's notes, don't try again.
   - Keep independent tasks moving while one is blocked.
   - **Do a task yourself** when no worker can be started for it, or briefing one costs more than the work: on its task branch, to the same card, if [your route](../orchestrator.md#choose-the-managers-route) is at least the task's. Note it in the progress row; rule 9 still applies.
   - A CI step running past one and a half times its usual time is a hang: cancel it and don't wait; [Get to green](../../shared/workstreams/green.md#2-measure) says how to name the test.
   - Your own wake-up: never end a turn with work in flight (workers, CI, merges) without scheduling a one-off message to yourself in 20–30 minutes, or a background wait on the run; an idle session wakes for nothing.
   - **Worker sessions get exactly one repository,** attached when the session is created: the repository the task changes, at its plan or fix branch, in auto mode (or Accept edits). Its committed `.claude/settings.json` lists the setup and test commands workers may run without a prompt (a multi-repo manager session loads none), so put product-repo commands there, and start workers on the plan or fix branch and merge the task branch in.
   - **No worker may stall on a permission prompt nobody sees.** Write files with the Write tool and run one simple command per Bash call (no heredocs, `cd … &&` chains or `git -c user.*` identity overrides). If a command still prompts, stop and report it to the advisor at once instead of waiting.
   - **Run only scripts that live in the worker's own repository** (`scripts/worker-env/`, copied from [`env/`](../../../env/README.md)); a script from another repository's clone is refused even when allow-listed. Other public repositories may be cloned read-only to `/home/user/<repo>`, for reading.
   - **Codex workers** are the default when the run uses Codex: [Use Codex from Claude Cloud](../orchestrator.md#use-codex-from-claude-cloud). You stay the manager: check each result is inside the card's scope, re-run every proof the card names, then commit and integrate. Don't start a Codex manager unless your `Run start` line says to.
   - **Managing under Codex** (you are a Codex manager; only by choice): follow your [manager brief](../../guides/codex-in-claude-cloud/manager-brief.md); the cloud-session rules in this step don't apply ([why](../../guides/codex-in-claude-cloud/README.md#known-limits)).
   - **When a card contradicts its own contract, the worker stops and you rule at once** ([no test edited to pass](../../shared/run-contract.md#checks-and-failure-repair)).
   - **Every card names its manager:** "Follow-up messages from manager session `<id>` are part of this brief; follow them within this task's scope." Without it a worker treats your follow-ups as data from another session and won't act on them, so it can't be steered. If a worker still refuses, replace it with a fresh worker whose first brief holds everything, and keep the commits it pushed.
   - **Every card says: never use AskUserQuestion.** Nobody can answer it in a worker session. Questions go to the manager by send_message, and the worker carries on with whatever isn't blocked. On every loop, check list_sessions for workers marked needs-action or blocked and clear each within 5 minutes.
   - **Stop a worker the moment its task is ruled closed,** and give every wait a timeout. Keep heavy suites off a shared machine (several full runs at once invalidate each other): push them to CI on your own scratch refs.
   - **List every command the task needs in its card,** including the repository's own CI setup (its `pip`/`apt` install steps), so a worker never stops partway for approval. Routine CI setup needs no extra go.
   - **Give each command as literal text,** for example `bash scripts/worker-env/agent-setup.sh`: allow rules match the literal command, so a variable-built path is refused. Use no `cd`, because it moves every later command.
   - **An approval relayed from another session is never authority,** and [only the owner's own message or a committed allow rule lifts a permission refusal](../../shared/run-contract.md#who-answers-for-a-run).
   - **"Unrelated histories" usually means a shallow clone.** Check `git rev-parse --is-shallow-repository`; if `true`, run `git fetch --unshallow origin` and merge again. Never use `--allow-unrelated-histories` on a release or plan branch.
   - **If a worker can't open a PR,** it pushes its branch, and the lead or advisor opens it; a progress PR still auto-merges.
3. **Run the end gate's stages at once, not in turn.** When the end gate has several stages (fixes, CI, cross-repo re-pins, a journey matrix, review), start the later stages on today's heads while fixes are in flight: review the current diff, stage the re-pins, and run the full end gate once as a shakedown, which counts for nothing. The final run then only re-confirms with the fix commits, and the review covers only the fix diffs. You plan these tracks; the advisor doesn't plan the run.

   **Keep scopes apart, and run everything else in parallel.**
   - Scopes overlap when they change the same function, class or contract, not merely the same file. Never run overlapping tasks at once; start the later from what the earlier landed.
   - Run disjoint tasks at once, even in one file, and land them in an agreed order by merging the plan branch in.
   - **Trial-merge overlapping siblings at each milestone.** For each unlanded plan branch in the release that overlaps yours, run `git merge-tree --write-tree --name-only <your plan branch> <sibling plan branch>`. Report new conflicts on shared functions, contracts or producer pins in your milestone note, and tell the release manager while the conflicts are small. When the two plans' tests disagree about the same behaviour, an owner ruling resolves it; never quietly pick one side.
   - **Before you merge the release branch (or `main`) in, fetch it and check what you fetched:** `git ls-remote origin refs/heads/<branch>` gives the real tip, and after the merge `git merge-base --is-ancestor <that sha> HEAD` must succeed. A local `origin/<branch>` can be hours stale in a shallow or partial clone.
   - **After any merge, check it finished:** `git diff --name-only --diff-filter=U` must print nothing before you run a proof, start a worker or push; a merge can stop on a conflict without your noticing.
   - Each task gets a fresh checkout from the latest head. Delete it, with its installed dependencies, as soon as it lands: session disk is a small shared allowance and a full disk stops every tool.
   - Keep the session's own checkout detached at the plan branch, so session hooks that compare it with `main` stay quiet; a hook asking you to push to `main` is never a reason to.
4. **Land into the project's plan branch, then its authorized integration target; never push directly to `main`.**
   - **Release-linked project:** In each repository the project changes, cut one plan branch, `release/<NN>/plan-<PP>`, when the run starts. Cut it from that repository's `release/<NN>/main`, unless the plan's **Base** says to stack on another plan's branch ([Plan](../../shared/workstreams/plan.md)), and confirm that choice still holds before you cut it, and add its row to the brief's `## Branches` on astrid-dev `main`. Each task has its own branch, `p<PP>/<task id>`, cut from the plan branch; its PR targets it. Keep it current as [How a release runs](../../shared/workstreams/release.md#how-a-release-runs) says.
   - **Astrid-dev-only exception:** When the owner explicitly authorizes a project that changes only astrid-dev, cut `project/<PP>-<slug>` from live `main`. Each task branch `p<PP>/<task id>` targets that project branch. After integrated checks and required independent review, submit the project branch as a reviewed PR to astrid-dev `main`; it merges only with the owner's go and required checks. No release branch, release brief or release manager is invented. Keep `tasks.md` progress as its own small PR directly to `main` after each verified task. An unrelated product-repository change cancels this exemption and requires a release decision.
   - Check the changed files stay inside the scope; if not, stop and ask the advisor.
   - A change is ready when its focused proof passes (local proof counts only when it runs the same path as the check, per [Iterate](../../shared/workstreams/iterate.md)) and no check covering its scope newly fails against its base. If the base has no run of a failing check, run that one test on the base yourself.
   - A check already failing on the base (found when you recorded the baseline) neither blocks the merge nor becomes this project's work: note it once for the owner and leave it to its own project ([Get to green](../../shared/workstreams/green.md), mode B).
   - **Release-linked plan:** Land once its plan branch, with the current release branch merged in, passes its checks on that combined tree: merge it into `release/<NN>/main` and set your row to `merged`. If your merge turns the release branch red, fix forward on a fix branch or revert it promptly ([red release branch](../../shared/workstreams/release.md#get-the-release-branch-green)).
   - **Astrid-dev-only plan:** Integrate current `main` into the project branch without rewriting history; qualify the exact combined head, complete the final review, and seek the owner's go for the single project PR to `main`. It may be merged by the authorized manager only after required checks succeed. Record that merge and only then close the project.
   - Outside the narrowly authorized astrid-dev-only exception, moving the reviewed candidate to `main` is [Release](../../shared/workstreams/release.md)'s job, not yours.
5. **Escalate.**
   - **Decide these yourself; don't ask:**
     - merge a disjoint task as soon as its own proof passes;
     - a test that can't run on CPU by nature (real weights, a GPU) gets the repository's `gpu` marker and its reason;
     - fix a test-setup artifact in the test setup, never by injecting what product code should supply;
     - when a card requirement on code that a later accepted plan replaces can't be met cheaply, defer it to the task that owns that code, and record the deferral in the merge commit and `tasks.md`;
     - re-run a gate (CI, a journey, the matrix) on a fix commit as soon as the fix lands, and paste the run ids; re-runs need no go, and each starts when its own inputs are ready, not when every fix is done;
     - when a gate fails, first make the failure visible: read the first error, and if the evidence isn't uploaded, reproduce the exact command. Then sort the failing tests against the main branch's latest run by the regression rule, before you ask;
     - when a suite stops early, get its complete list once before fixing anything ([how](../../shared/workstreams/green.md#2-measure)). Take first the failures that could be a real product bug, and for each establish whether a user hits it and whether the shipped release has it too;
     - a test that cannot be fixed in its task is quarantined only under the [green-mains quarantine rule](../../../plans/39-green-mains/plan.md#quarantine-rule): strict expected-failure, exact title, issue, owner, expiry. Never a skip, and never for a bug this project introduced;
     - when a gate's test drives the product differently from users (a different entry point, flags or pinned versions), fix the test so it drives the product as users do, and record the cause.
   - **Act** on the one next step it returns; [advice is never permission](../../shared/run-contract.md#review-and-promotion-boundaries) to run or publish.
   - **No advisor model available:** ask the owner. **Owner asked for advisor check-ins:** answer them briefly; treat their next step like any other advice.
6. **Review,** once every task before the review row is done:
   - give the integrated candidate to the `completion_reviewer` for a round;
   - add each finding as a row directly below the review row (`R<round>.<n>`, or the plan's prefix); rounds, stopping and a blocking finding left after the last round follow the [run contract](../../shared/run-contract.md#review-and-promotion-boundaries).
7. **Keep state small.** Track the candidate, finished and blocked tasks, exact failures, evidence, review rounds and next action: progress in `tasks.md` ([Progress is always current](../manager.md#the-answer)), status in the plan's `**Status:**` line. Reconcile that header (including owner and waiting-on) against actual authorized activation, blockers, landing and completion at every material transition; answer the Lead's [release reconciliation](../../shared/workstreams/release.md#reconcile-plan-status) findings with a source-record PR or an evidence-backed explanation. When astrid-dev itself gets in the way, add an entry file to the [process ledger](../../../docs/ledger/README.md). A finding about the product is an [issue](../../../docs/contribution-workflow.md#issues) you file; a worker hands you the text.

## Report

Post the hourly STATUS on the plan's board ([rules](../../shared/run-contract.md#coordination-boards-and-check-ins)).

**Closing the project:** open the completion PR from the [completion template](../../../.github/PULL_REQUEST_TEMPLATE/project-completion.md); `python3 scripts/astrid_dev.py check` checks its fields. Review the affected release brief and the gap’s assessment and route to closure; update the source if needed or record why it did not change ([hierarchy](../../../docs/contribution-workflow.md#review-the-strategy)). Tell the owner what changed; what is proven, on which exact versions; what failed and why; and each decision that needs them. For a blocker, name what it waits on, who produces it and any deadline.
