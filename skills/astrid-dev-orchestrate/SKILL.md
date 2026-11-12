---
name: astrid-dev-orchestrate
description: Orchestrate Astrid work for the owner. Start a project by planning it and farming it out to a manager session set up so it never waits on a permission prompt; advise when a planner, manager or worker is genuinely blocked; run owner-requested check-ins; and close the project. Use when the owner hands you a project or asks for advice or check-ins.
---

# Orchestrate Astrid work

**Your job, in short.** Once a project is running under a manager in its own session, you do three things and nothing else:
1. **Check in on a schedule,** if the owner asked for check-ins (path 3).
2. **Answer questions and unblock** managers and the owner (path 2).
3. **Equip managers to need you less.** Treat every question as a symptom: fix its cause in the [manage skill](../astrid-dev-manage/SKILL.md), the plan or the task card, so it isn't asked twice.

**One exception: if you host the manager, you answer for the run.** When Codex runs the project inside your session, you are its [accountable agent](../astrid-dev-shared/run-contract.md#who-answers-for-a-run), not an idle advisor ([below](#use-codex-from-claude-cloud)).

Follow the accepted release brief for any coordination duties it assigns you, such as relaying cross-track dependencies, accepting frozen inputs, arranging review or publishing after the owner's go.

**You orchestrate; the manager manages.** If you catch yourself writing a manager's dispatch plan (which tracks run in parallel, per-worker steps, when to escalate), the manage skill is missing a rule: send the manager one line naming the goal, and add the rule to the [manage skill](../astrid-dev-manage/SKILL.md) by PR.

You act for the owner across projects and don't run tasks. Follow the [run contract](../astrid-dev-shared/run-contract.md); in `run.yaml` your role is `advisor`. Take the path that matches the request:

| Asked for | Path |
|---|---|
| "Do this project", or an outcome with no plan yet | 1. Start a project |
| A blocked planner, manager or worker asks a question | 2. Advise |
| The owner wants regular updates on a run | 3. Check in |
| The project's completion PR merged, or the owner says stop | 4. Close |

**Between those, stay idle.** Progress lives in the plan's `tasks.md`. Handle required dependency handoffs and urgent blockers when received, without taking over task supervision.

**A queue is yours to keep moving.** For an ordered queue (phases of a plan, or several projects):
- **Prepare the next item before the current one ends:** its cards re-planned against what just landed, its `Run start` line, and its start message.
- **Get the go once:** one standing go from the owner for the whole queue, given in the manager's session and recorded on each `Run start` line. Without it, every item waits for her.
- **At each check-in, confirm the manager has moved on.** A finished item with an idle manager and a prepared next item is a stall: send the one next action.
- **An item gated on an outside event** (a release publishing, an owner setting) is still built on its integration branch, with only the merge to `main` waiting. Say what is gated, and on whom, in every report.

## Path 1: start a project

1. **Plan it, or confirm its plan.** Start from [`strategy.md`](../../strategy.md) and the [catalog](../../plans/index.md). With no accepted plan, write one with [Plan](../astrid-dev-plan/SKILL.md) (you may plan it yourself) and get the owner's scope decision. A draft plan authorizes nothing, and no manager starts before its plan is merged.
   - **Fix the scope when the run starts.** If the owner adds scope to a running release, say what it reopens (tests, re-pins, review) and offer the next release instead; add it only if the owner decides to.
2. **Check the cloud setup** (next sections) for each repository the plan changes.
3. **Farm it out.** Create one manager session per project, and one project per manager at a time. Give it:
   - the plan's path;
   - the integration branch (`int/<project>`), and the exact starting versions;
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
   You are accountable for Plan <NN>, <phase or tasks>: you answer for it finishing.
   Follow the astrid-dev-manage skill. The plan is plans/<NN-name>/ on astrid-dev main at <sha>;
   start from the Run start line in inputs.md and the dispatch notes in tasks.md.
   Land work on int/<NN-name>. You may <what it may do without asking>.
   Come to me for <what needs the owner's go>. Your advisor for hard questions is session <id>.
   ```

3. **Add nothing the plan should hold.** If the message needs a rule the plan or a skill lacks, put the rule there by PR and point to it.
4. **Don't add a tier.** If you hand a project to another session, it becomes the accountable agent and you become its advisor, or step out. Never stay an advisor above an advisor: then nobody answers for the run.

## Claude Cloud setup: no permission prompts

A session that waits on a prompt nobody sees is a stalled run. Before any work starts:

- **One repository per worker session,** attached at creation, at the integration branch. Workers start there and merge their task branch in, so the right allow list is loaded.
- **The allow list is the repository's committed `.claude/settings.json`** (for example astrid-agent's on its integration branch). Add a missing rule there, by PR, with the owner's OK: a rule change is a change to permissions.
- **Workers run in auto mode,** or Accept edits, calling only scripts in their own repository (`scripts/worker-env/`, copied from [`env/`](../../env/README.md)) by literal path, with no `cd`; the results behind each rule are in [`env/README.md`](../../env/README.md#how-a-worker-calls-them).
- **Only the owner lifts a refusal** ([authority](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)); an approval relayed from another session doesn't count. Bring the exact command to the owner.
- **Merges:** a manager merges its own progress pull requests; every other merge into `main` needs the owner's go ([the rule](../astrid-dev-shared/run-contract.md#who-answers-for-a-run)). Auto mode refuses some merges, deletions and settings commits: ask once for the whole run ("merge the progress and plan PRs") and record that standing go in `run.yaml`.

## Choose the cloud workflow

For agents in separate Codex Cloud chats, use [Codex Cloud agent coordination](codex-cloud/README.md): its issue mailbox, session IDs and what does not wake an idle chat. Live resource supervision stays the responsible manager's job and never waits for a check-in. Codex inside a Claude Code cloud session is the next section: a different environment.

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
- **Brief a manager as a manager.** Start every Codex manager from [`manager-brief.md`](codex-in-claude-cloud/manager-brief.md), and re-read it before each new run, because it changes. Codex takes its authority only from its starting prompt: a mailbox note can't later grant it merge rights or change its role. A prompt that forbids integrating ("never push to int/…") makes Codex a worker, and you end up relaying every branch. To change a running Codex's role, have it checkpoint (push work in progress, write a handover entry, end `DONE`) and start a fresh manager run from the handover.
- **You host it, so you answer for it.** Codex can't keep itself alive, wake itself, reach the owner or run a model outside Codex; you hold all of those. Say "my run" and "my Codex manager". At every check-in, without waiting for the mailbox:
  - **Compare `tasks.md` and the integration branch with the last check-in.** If nothing moved, read `codex.log` for why and send one next action through `to-codex.md`.
  - **Start every task Codex can't run** (a route bound to a Claude model, or the review) as soon as its inputs have landed, or Codex writes `READY: <task id>` to the mailbox; don't wait to be asked.
  - **Clear what is stuck on your side:** an unmerged or conflicting progress PR, a dead runner, a refused command to take to the owner.
  - **Open the final PR and bring the owner their decisions.**
- **Codex still manages the tasks.** Don't redo its fixes, re-review what its reviewer passed, or relay its branches: it dispatches, judges and integrates under its starting brief. Answer its questions, and raise a structural cause when its reports show a pattern it hasn't named.

## Path 2: advise

Answer the one bounded question you were given: a genuine blocker, conflicting evidence, or a consequential judgment the plan can't settle. This is not routine per-task approval.

- **Refresh the facts first:** the exact candidate, source and donor identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Question the question.** Why did it reach you: missing evidence, an unclear card, a gap in a skill or the plan? Sometimes the right answer is a different question.
- **Unblock it once and for all.** Behind every question is a cause: a missing rule, a thin card, a misleading tool, or authority it wasn't given. Answer, then fix that cause at its source in the same turn (the task card, the plan, or a skill by PR) and say how they could have settled it themselves. If you can't fix it now, add an entry to the [process ledger](../../docs/ledger/README.md). A question answered twice is a fix you still owe.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a challenge against over-engineering.
- **Require the previously failing check** to run on the repaired candidate.
- **Don't** waive failures, widen scope, reset counters, add a review stage, authorize execution or publication, invent model IDs, or claim a run happened without evidence.

## Path 3: check in (only when the owner asks)

Record the agreed cadence and end condition on the plan's `Run start` line, and as `checkin` in the run's `run.yaml` once a run exists. First verify a scheduler and a supported way to resume this session; only then configure and test recurring check-ins. Without a verified path, poll in the foreground while active and tell the owner when a manual nudge is needed ([what works](codex-cloud/README.md#what-works-and-what-does-not)). The Codex manager's 20-minute hosting check-in above is a different timer. These documents never start a check-in themselves.

Each check-in compares the run with the previous check-in. To gather the facts (logs, CI runs, the manager's recent events), send N helpers; keep the judgment yourself.
- **Liveness:** if the manager is idle while work is in flight, wake it with one next action.
- **Strategy:** if the priority order ([`plans/priority.md`](../../plans/priority.md)) or a plan's state no longer matches [`strategy.md`](../../strategy.md), report the mismatch to the owner. Don't edit it yourself.
- **Progress record:** `tasks.md` must match reality (merged PRs ticked, open and blocked tasks showing their state; [the manager's rule](../astrid-dev-manage/SKILL.md#the-answer)). If it lags, the nudge is to bring it up to date. Report progress from it, not from memory.
- **Moving:** tasks finished or candidates landed since last time. **Stuck:** the same failure twice, the same open question, or idle agents. **Blocked:** waiting on a person, an event or a dependency, and for how long.
- **Drifting:** work outside its scope, or undoing a recorded decision. **Wasteful:** reruns with nothing changed, or a costlier route than the task needs.
- **Parallelism:** ready independent work left idle, or a dependency that could be unblocked. Give the manager the goal; it chooses and supervises its workers.

For each manager or cross-track blocker, take the next useful action:
- **On track:** note one line; send the manager nothing.
- **Needs a nudge:** send the manager one next action to unblock or improve the run.
- **Needs the owner:** bring one decision with your recommendation.

**Improve astrid-dev as you go.** Friction in astrid-dev itself (an unclear skill, a missing template field, a slow check) gets a [process ledger](../../docs/ledger/README.md) entry; if the fix is small and touches only astrid-dev docs or skills, open the fixing PR in the same check-in, following the [improve skill](../astrid-dev-improve/SKILL.md). Friction specific to this one run goes in its [decisions ledger](../astrid-dev-shared/templates/decisions-ledger.md).

After three check-ins in a row with nothing to report, you may recommend a slower cadence; keep the agreed one until the owner changes it or its end condition is met. A check-in may nudge a manager to continue already authorized work through a verified resume mechanism; it grants no new scope, spend or publication authority.

## Path 4: close

**Cancel the check-ins when the project is done.** When the project is complete, cancel every check-in you scheduled. Do the same when its end condition is met or the owner says stop. A project is complete when its completion PR merges. Confirm none remain, and tell the owner they have stopped.
