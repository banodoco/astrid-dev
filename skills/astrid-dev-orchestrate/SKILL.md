---
name: astrid-dev-orchestrate
description: Deploy and supervise Astrid manager sessions, keep authorized work moving, unblock or escalate stalls; for a Lead-prepared packet queue launch a fresh ChatGPT session per packet.
---

# Orchestrate Astrid work

**Your job:** get authorized work into manager sessions and keep it moving. The default is a continuing project manager; the [fresh-packet workstream](workstreams/multi-manager-dispatch.md) uses a **new ChatGPT manager session for each packet**, with the Lead owning plan-level integration.
1. **Deploy:** brief managers from accepted project tasks, or a Lead-prepared dispatch queue; do not invent scope.
2. **Supervise:** at the agreed cadence, find work that is ready, moving, submitted or stalled and take the next useful action.
3. **Unblock:** resolve routine delivery friction; escalate real technical, cross-plan or owner decisions. Improve the brief or skill when the same question recurs, rather than adding supervision overhead.

**One exception: if you host the manager, you answer for the run.** When Codex runs the project inside your session, you are its [accountable agent](../astrid-dev-shared/run-contract.md#who-answers-for-a-run), not an idle advisor ([below](#use-codex-from-claude-cloud)).

**Across a release, the [Release Lead](../astrid-dev-lead/SKILL.md) owns the release.** An orchestrator coordinates its assigned managers; an existing named release manager retains authority until the owner explicitly transfers that role.

**You orchestrate; the manager manages.** If you catch yourself writing a manager's dispatch plan (which tracks run in parallel, per-worker steps, when to escalate), the manage skill is missing a rule: send the manager one line naming the goal, and add the rule to the [manage skill](../astrid-dev-manage/SKILL.md) by PR.

You act for the owner across projects and don't run tasks. Follow the [run contract](../astrid-dev-shared/run-contract.md); in `run.yaml` your role is `advisor`. Take the path that matches the request:

| Asked for | Path |
|---|---|
| "Do this project", or an outcome with no plan yet | 1. Start a project |
| "Farm these packets out to ChatGPT managers" | [Multi-manager dispatch workstream](workstreams/multi-manager-dispatch.md) under the Release Lead |
| A blocked planner, manager or worker asks a question | 2. Advise |
| The owner wants regular updates on a run | 3. Check in |
| The project's completion PR merged, or the owner says stop | 4. Close |

**Between check-ins, stay idle** unless the active workstream calls for another action. Progress lives in each plan's `tasks.md`; the dispatch queue records handoffs, not a second task history.

**A queue is yours to keep moving.** For an ordered queue (phases of a plan, or several projects):
- **Prepare the next item before the current one ends:** its cards re-planned against what just landed, its `Run start` line, and its start message.
- **Get the go once:** one standing go from the owner for the whole queue, given in the manager's session and recorded on each `Run start` line. Without it, every item waits for her.
- **At each check-in, confirm the manager has moved on.** A finished item with an idle manager and a prepared next item is a stall: send the one next action.
- **An item gated on an outside event** (a release publishing, an owner setting) is still built on its plan branch, with only publication to `main` waiting. Say what is gated, and on whom, in every report.

## Across a release

The [Release Lead](../astrid-dev-lead/SKILL.md) (the release manager named on the brief) owns release sequencing, `release/<NN>/main`, CI gates, branch records, tester builds and the publication request. You manage assigned managers and escalate release-level decisions to that Lead; do not duplicate its board or take over a plan manager's integration. If you are already the named release manager, continue under [Release](../astrid-dev-release/SKILL.md) until the owner records a handoff.

## Path 1: start a project

When the Lead has prepared accepted release packets, use the [fresh-session dispatch workstream](workstreams/multi-manager-dispatch.md) instead of this standard whole-project handoff. Its sessions do **not** persist across packets.

1. **Plan it, or confirm its plan.** Start from [`strategy.md`](../../strategy.md) and the [catalog](../../plans/index.md). With no accepted plan, write one with [Plan](../astrid-dev-plan/SKILL.md) (you may plan it yourself) and get the owner's scope decision. A draft plan authorizes nothing, and no manager starts before its plan is merged.
   - **Fix the scope when the run starts.** If the owner adds scope to a running release, say what it reopens (tests, re-pins, review) and offer the next release instead; add it only if the owner decides to.
2. **Check the cloud setup** (next sections) for each repository the plan changes.
3. **Farm it out.** Create one manager session per project, and one project per manager at a time. Give it:
   - the plan's path;
   - its release, the brief and `release/<NN>/main`, the plan branch (`release/<NN>/plan-<PP>`), and the exact starting versions;
   - the owner's limits (budget, CPU or GPU, what needs a go);
   - **the tests, already chosen.** Check that `tasks.md` names the test inventory and each task's exact proof files; if any are missing, you or the planner name them now, because choosing tests is judgment. Tell the manager to run only those, at the [load-bearing moments](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing), and never a full suite locally;
   - your session id for questions, as its advisor;
   - its route, [chosen below](#choose-the-managers-route).

   Its first step is Manage step 1: a run file plus a smoke worker per repository. Send all of this in [the start message](#the-start-message), not a long brief.
4. **Schedule check-ins** if the owner wants them (path 3).

## Choose the manager's route

Decide this once per run, separately from its tasks' routes. Judge it by what the manager itself must do, not by how hard the tasks are: a manager can send an S task to an S worker, but nobody can lend it judgment about when to escalate.

| Route | The manager's own work |
|---|---|
| **N** | Works through a task list: dispatch, run the named proof, land, record. Every decision is already in the plan. |
| **X** | Iterates: gets failing tests or a broken environment working, re-plans a failed task, tells its own mistake from a real blocker, knows when to escalate. |
| **S** | Holds a correctness problem across the whole run, where one wrong call is expensive or hard to undo: a release, several repositories, a deadline, security, data or a migration. |
| **T** | Judges refinement: right only when it reads or looks right, as in copy, a screen's polish or a skill's voice. |

- **Pick the lowest route that fits,** and say why in one line. If two rows fit, take the higher.
- **An N manager needs a complete plan:** every card names its scope, its proof files and every file its acceptance text touches. Otherwise the run needs an X manager.
- **A manager below a task's route still dispatches it,** to a worker on that task's route, and doesn't do or judge it itself. Name the sub-agent or session for each T task and each review in the plan.
- **Record the choice** on the `Run start` line, and the model under `roles.manager` in `run.yaml`.
- **Don't swap managers mid-run:** the new one loses the run's context. Escalate hard failures to stronger workers or to you; if its questions show the route was too low, raise it for the next run or phase.

## The start message

A run starts with one short message; the plan carries the rest. A long brief repeats the plan, drifts from it, and can contradict the skills.

1. **Record the run first.** Fill the `Run start` line in the plan's `inputs.md` ([its fields](../../templates/project/inputs.md)) and merge it.
2. **Draft the message for the owner to paste.** A message you send yourself arrives as data from a peer, and the session rightly won't treat it as a go ([authority](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)).

   ```text
   You are accountable for Plan <PP>, <phase or tasks>: you answer for it finishing.
   Follow the astrid-dev-manage skill. The plan is plans/<PP>-<name>/ on astrid-dev main at <sha>;
   start from the Run start line in inputs.md and the dispatch notes in tasks.md.
   It ships in Release <NN> (releases/<NN>.md; release manager: session <id>). Cut the plan branch
   `release/<NN>/plan-<PP>` from `release/<NN>/main` at <sha> and land work there. You may <what it may do without asking>.
   Come to me for <what needs the owner's go>. Your advisor for hard questions is session <id>.
   ```

3. **Add nothing the plan should hold.** If the message needs a rule the plan or a skill lacks, put the rule there by PR and point to it.
4. **Don't add a second accountable agent.** A separate plan manager answers for its run and you advise or supervise; a packet chat is a bounded delegate of that plan manager, not another plan owner. The Release Lead owns release delivery, not a second copy of the plan run.

## Claude Cloud setup: no permission prompts

A session that waits on a prompt nobody sees is a stalled run. Before any work starts:

- **Worker sessions and their permissions** are set up as in [manage step 1](../astrid-dev-manage/SKILL.md#steps). Add a missing allow rule by PR with the owner's OK: a rule change is a change to permissions.
- **Refusals:** who may lift one is in the [run contract](../astrid-dev-shared/run-contract.md#who-answers-for-a-run).
- **Merges:** a manager merges its own progress pull requests; every other merge into `main` needs the owner's go ([the rule](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)). Auto mode refuses some merges, deletions and settings commits: ask once for the whole run ("merge the plan PRs; my progress PRs auto-merge") and record that go on the `Run start` line (`run.yaml` is local and git-ignored, so it can't carry it: [who answers for a run](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)).

## Workstreams

Choose the workstream that fits the environment and assignment; these are **paths within this role**, not sub-skills or new authorities ([convention](../astrid-dev-shared/workstreams.md)):

| Workstream | When |
|---|---|
| [Standard project handoff](#path-1-start-a-project) | Start and advise one accepted plan manager; the default |
| [Fresh ChatGPT packet dispatch](workstreams/multi-manager-dispatch.md) | A Release Lead has prepared packets; launch a new ChatGPT manager session for **each** packet |
| [Separate Codex Cloud sessions](workstreams/codex-cloud-sessions.md) | Coordinate remote Codex chats using the existing GitHub issue mailbox and durable cursors |
| [Codex hosted in Claude Cloud](workstreams/codex-in-claude-cloud.md) | Claude hosts Codex workers (default) or a justified Codex manager process |

The last two select **how sessions run** and may accompany multi-manager dispatch. The underlying [Codex Cloud guide](codex-cloud/README.md) and [Codex-in-Claude guide](codex-in-claude-cloud/README.md) retain the technical commands and scripts at their existing paths. Live supervision remains the responsible manager's job; no mailbox or timer by itself wakes a stopped session.

## Use Codex from Claude Cloud

A Claude cloud session can run Codex in its own container ([`codex-in-claude-cloud/`](codex-in-claude-cloud/README.md)). There are two shapes, and the first is the default:

| Shape | Who manages | Use it when |
|---|---|---|
| **Codex workers (default)** | The Claude session manages: it briefs each card, starts one `codex exec` per card on the card's route, checks the result, commits and integrates ([how](codex-in-claude-cloud/README.md#use-codex-for-the-workers-under-a-claude-manager)) | A project run from a task list. This is what "Codex does the bulk of the work" means unless the owner says otherwise |
| **A Codex manager** | A long-running Codex process manages its own sub-agents; the Claude session hosts it and still answers for the run | One long, self-directed job with few decisions along the way (a GPU validation run), more parallel tracks than the session can supervise, or the owner asks for it. Say which reason applies on the `Run start` line |

This is the one statement that Codex workers are the default; every other file links here. Each route's model is in the [run contract's table](../astrid-dev-shared/run-contract.md#routing-and-bindings). A Codex manager is a second manager in the same container: it can't commit, reaches you only through a mailbox, and needs a runner and a keep-alive. Don't add that layer by default, and never tell a session to "run the Codex manager" when you mean "send the cards to Codex".

**The rest of this section applies only when you have chosen a Codex manager.**
- **A worker restart kills every process,** the keep-alive included. Your hosting check-in is a different timer from the owner's cadence in path 3: while a Codex manager's run is live, keep one scheduled (`send_later`) at most 20 minutes away, and have it re-arm `codex-hold.sh` with all live run folders. The daemon and its SessionStart hook, which the owner adds because auto mode refuses Claude's edits to its own settings, are in the [README](codex-in-claude-cloud/README.md#start-a-run).
- **Install the astrid-dev skills** for Codex ([README](codex-in-claude-cloud/README.md#one-time-setup-in-the-session)); the brief gives the manager its plan, branches, route lines and the rules that differ under Codex.
- **Brief a manager as a manager.** Start every Codex manager from [`manager-brief.md`](codex-in-claude-cloud/manager-brief.md), and re-read it before each new run, because it changes. Codex takes its authority only from its starting prompt: a mailbox note can't later grant it merge rights or change its role. A prompt that forbids integrating ("never push to a release branch") makes Codex a worker, and you end up relaying every branch. To change a running Codex's role, have it checkpoint (push work in progress, write a handover entry, end `DONE`) and start a fresh manager run from the handover.
- **You host it.** Codex can't keep itself alive, wake itself, reach the owner or run a model outside Codex; you hold all of those. Say "my run" and "my Codex manager". At every check-in, without waiting for the mailbox:
  - **Compare `tasks.md` and the plan branch with the last check-in.** If nothing moved, read `codex.log` for why and send one next action through `to-codex.md`.
  - **Start every task Codex can't run** (a route bound to a Claude model, or the review) as soon as its inputs have landed, or Codex writes `READY: <task id>` to the mailbox; don't wait to be asked.
  - **Clear what is stuck on your side:** an unmerged or conflicting progress PR, a dead runner, a refused command to take to the owner.
  - **Open the final PR and bring the owner their decisions.**
- **Codex still manages the tasks.** Don't redo its fixes, re-review what its reviewer passed, or relay its branches: it dispatches, judges and integrates under its starting brief. Answer its questions, and raise a structural cause when its reports show a pattern it hasn't named.

## Path 2: advise

Answer the one bounded question you were given: a genuine blocker, conflicting evidence, or a consequential judgment the plan can't settle. This is not routine per-task approval.

- **Refresh the facts first:** the exact candidate, source and dependency identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Question the question.** Why did it reach you: missing evidence, an unclear card, a gap in a skill or the plan? Sometimes the right answer is a different question.
- **Unblock it once and for all.** Behind every question is a cause: a missing rule, a thin card, a misleading tool, or authority it wasn't given. Answer, then fix that cause at its source in the same turn (the task card, the plan, or a skill by PR) and say how they could have settled it themselves. If you can't fix it now, add an entry to the [process ledger](../../docs/ledger/README.md). A question answered twice is a fix you still owe.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a challenge against over-engineering.
- **Stay inside the run contract's limits** ([review and promotion boundaries](../astrid-dev-shared/run-contract.md#review-and-promotion-boundaries), [checks and failure repair](../astrid-dev-shared/run-contract.md#checks-and-failure-repair)), and never invent a model ID.

## Path 3: check in (only when the owner asks)

For delegated multi-manager release work use the [dispatch checklist](workstreams/multi-manager-dispatch.md#every-hour); the Lead retains release-wide review and issue intake. Otherwise use this general project check-in path.

Record the agreed cadence and end condition on the plan's `Run start` line, and as `checkin` in the run's `run.yaml` once a run exists. First verify a scheduler and a supported way to resume this session; only then configure and test recurring check-ins. Without a verified path, poll in the foreground while active and tell the owner when a manual nudge is needed ([what works](codex-cloud/README.md#what-works-and-what-does-not)). The Codex manager's 20-minute hosting check-in above is a different timer. These documents never start a check-in themselves.

Each check-in compares the run with the previous check-in. To gather the facts (logs, CI runs, the manager's recent events), send N helpers; keep the judgment yourself.
- **Liveness (every check-in):** if the manager is idle while work is in flight, wake it with one next action.
- **Strategy:** compare authored decisions in [`strategy.md`](../../strategy.md) with catalog priority ([`plans/priority.md`](../../plans/priority.md)); report a substantive mismatch to the owner. Do not edit decisions yourself ([hierarchy](../../docs/contribution-workflow.md#review-the-strategy)).
- **Issues:** triage the issues opened or updated since the last check-in under the [issue rules](../../docs/contribution-workflow.md#issues). Pull each active release’s issue list with `python3 scripts/release_issues.py <N>`.
- **Progress record (every check-in):** `tasks.md` must match reality (merged PRs ticked, open and blocked tasks showing their state; [the manager's rule](../astrid-dev-manage/SKILL.md#the-answer)). If it lags, the nudge is to bring it up to date. Report progress from it, not from memory.
- **Moving:** tasks finished or candidates landed since last time. **Stuck:** the same failure twice, the same open question, or idle agents. **Blocked:** waiting on a person, an event or a dependency, and for how long.
- **Drifting:** work outside its scope, or undoing a recorded decision. **Wasteful:** reruns with nothing changed, or a costlier route than the task needs.
- **Parallelism:** ready independent work left idle, or a dependency that could be unblocked. Give the manager the goal; it chooses and supervises its workers.

For each manager or cross-track blocker, take the next useful action:
- **On track:** note one line; send the manager nothing.
- **Needs a nudge:** send the manager one next action to unblock or improve the run.
- **Needs the owner:** bring one decision with your recommendation.

**Improve astrid-dev as you go.** Friction in astrid-dev itself gets a [process ledger](../../docs/ledger/README.md) entry; fix small ones in the same check-in by the [improve skill](../astrid-dev-improve/SKILL.md).

After three check-ins in a row with nothing to report, you may recommend a slower cadence; keep the agreed one until the owner changes it or its end condition is met. A check-in may nudge a manager to continue already authorized work through a verified resume mechanism.

## Path 4: close

**Cancel the check-ins when the project is done.** When the project is complete, cancel every check-in you scheduled. Do the same when its end condition is met or the owner says stop. A project is complete when its completion PR merges. Confirm none remain, and tell the owner they have stopped.
