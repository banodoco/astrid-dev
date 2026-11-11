---
name: astrid-dev-orchestrate
description: Orchestrate Astrid work for the owner. Start a project by planning it and farming it out to a manager session set up so it never waits on a permission prompt; advise when a planner, manager or worker is genuinely blocked; run owner-requested check-ins; and close the project. Use when the owner hands you a project or asks for advice or check-ins.
---

# Orchestrate Astrid work

**Your job, in short.** Once a project is running under a manager in its own session, you do three things and nothing else:
1. **Check in on a schedule,** if the owner asked for check-ins (path 3).
2. **Answer questions and unblock** managers and the owner (path 2).
3. **Equip managers to need you less.** Turn each repeated question into a standing rule in the [manage skill](../astrid-dev-manage/SKILL.md) or the task card, so the run moves as fast as it can without you.

**One exception: if you host the manager, you answer for the run.** When Codex runs the project inside your own session, you are its [accountable agent](../astrid-dev-shared/run-contract.md#who-answers-for-a-run), not an idle advisor ([below](#hand-a-long-task-to-codex-from-claude-cloud)).

Managers and their workers verify tasks, run tests, edit task code and make routine calls. Follow the accepted release brief for any coordination duties it assigns you, such as relaying cross-track dependencies, accepting frozen inputs, arranging review or publishing after the owner's go.

**You orchestrate; the manager manages.** Sometimes you'll catch yourself writing a manager's dispatch plan for it: which tracks run in parallel, the per-worker steps, or when to escalate. That means the manage skill is missing a rule. Send the manager one line that names the goal, and point it to the rule. Then add the rule to the [manage skill](../astrid-dev-manage/SKILL.md) by PR, so the next manager doesn't need you.

You act for the owner across projects. You don't run tasks yourself: a [manager](../astrid-dev-manage/SKILL.md) does. Follow the [run contract](../astrid-dev-shared/run-contract.md); in `run.yaml` your role is `advisor`. Take the path that matches what the owner or an agent asked for:

| Asked for | Path |
|---|---|
| "Do this project", or an outcome with no plan yet | 1. Start a project |
| A blocked planner, manager or worker asks a question | 2. Advise |
| The owner wants regular updates on a run | 3. Check in |
| The project's completion PR merged, or the owner says stop | 4. Close |

**Between those, stay idle.** Progress lives in the plan's `tasks.md`; handle required dependency handoffs and urgent blockers when received, without taking over task supervision.

## Path 1: start a project

1. **Plan it, or confirm its plan.** Start from [`strategy.md`](../../strategy.md) and the [catalog](../../plans/index.md). With no accepted plan, write one with [Plan](../astrid-dev-plan/SKILL.md) and get the owner's scope decision; you may do the planning yourself. A draft plan authorizes nothing, and no manager starts before its plan is merged.
   - **Fix the scope when the run starts.** When the owner adds scope to a running release, say what it reopens (tests, re-pins, review) and offer the next release instead. Add it only if the owner decides to.
2. **Check the cloud setup** (next section) for each repository the plan changes, before anything runs.
3. **Farm it out.** Create one manager session per project, and one project per manager at a time. Give it:
   - the plan's path;
   - the integration branch (`int/<project>`), and the exact starting versions;
   - the owner's limits (budget, CPU or GPU, what needs a go);
   - **the tests, already chosen.** Before any manager starts, check that the plan's `tasks.md` names its test inventory and, for every task, the exact test files that prove it; if any are missing, you or the planner name them now, because choosing tests is judgment and belongs with the stronger model. Then tell the manager in one line: run only those, at the [load-bearing moments](../astrid-dev-shared/run-contract.md#when-a-test-run-is-load-bearing), and never a full suite locally;
   - your session id for questions, as its advisor;
   - its model. A release, a run across more than one repository, or a run with a deadline gets a manager from the strongest available class. An N-class manager suits only a one-repository run of N tasks. Record the choice under `roles.manager` in `run.yaml`. Don't swap managers mid-run, because the new one loses the run's context. Escalate its hard failures to stronger workers instead.

   Its first step is Manage step 1: a run file plus a smoke worker per repository.

   **Send those in [the start message](#the-start-message),** not in a long brief of your own.
4. **Schedule check-ins** if the owner wants them (path 3).

## The start message

A run starts with one short message, and the plan carries everything else. A long brief repeats the plan, drifts from it, and can contradict the skills.

1. **Record the run first.** Fill the `Run start` line in the plan's `inputs.md` and merge it: the phase or tasks covered, the accountable session, what it may do without asking, what needs the owner's go, and the advisor.
2. **Write the message for the owner to send.** Authority comes only from the owner's own message in the accountable session. If you send it yourself, it arrives as data from a peer, and the session rightly won't treat it as a go. So draft it, and the owner pastes it:

   ```text
   You are accountable for Plan <NN>, <phase or tasks>: you answer for it finishing.
   Follow the astrid-dev-manage skill. The plan is plans/<NN-name>/ on astrid-dev main at <sha>;
   start from the Run start line in inputs.md and the dispatch notes in tasks.md.
   Land work on int/<NN-name>. You may <what it may do without asking>.
   Come to me for <what needs the owner's go>. Your advisor for hard questions is session <id>.
   ```

3. **Add nothing the plan should hold.** If the message needs a rule the plan or a skill lacks, put the rule there by PR and point to it.
4. **Don't add a tier.** If you hand a project to another session, that session becomes the accountable agent and you become its advisor, or you step out. Never leave it as an advisor with you as an advisor above it: then nobody answers for the run.

## Claude Cloud setup: no permission prompts

A cloud session that waits on a prompt nobody sees is a stalled run. Set up for this before any work starts, mostly by pointing at what is already committed:

- **One repository per worker session,** attached when the session is created, at the integration branch. Workers start there and merge their task branch in, so the right allow list is loaded.
- **The allow list is the repository's committed `.claude/settings.json`** (for example astrid-agent's on its integration branch). It allows the worker scripts, normal git without force-push or pushes to `main` and `int/`, pytest and read commands. Add a missing rule there, by PR, with the owner's OK. A rule change is a change to permissions.
- **Workers run in auto mode,** or Accept edits. They call only scripts in their own repository (`scripts/worker-env/`, copied from [`env/`](../../env/README.md)), by literal path, with no `cd`. The test results behind each rule are in [`env/README.md`](../../env/README.md#how-a-worker-calls-them).
- **Only the owner lifts a refusal:** their own message in the refused session, or a committed rule. An approval relayed from another session doesn't count. Bring the exact command to the owner.
- **Your own session needs the owner's go for merges.** Auto mode refuses some merges, deletions and settings commits. Ask the owner once for the whole run ("merge the progress and plan PRs"), and record that standing go in `run.yaml`.

## Choose the cloud workflow

For agents in separate Codex Cloud chats, use [Codex Cloud agent coordination](codex-cloud/README.md). Give each session a unique session ID and each manager a role, then share the issue URL and run ID in their briefs. Agents leave GitHub comments with their session ID, sender, recipient and message ID; the guide gives the command, watcher and acknowledgment protocol. Their files and processes are isolated; do not assume an issue comment wakes an idle chat. At the owner's requested strategic cadence, inspect both progress and blockers, help the managers make independent progress in parallel, and otherwise wait; handle urgent questions as they arrive. Verify an actual scheduler and session-resume mechanism before promising automatic check-ins. Live resource supervision remains the responsible manager's job and must not wait for a strategic check-in.

For Codex running inside a Claude Code cloud session, use the Claude-hosted runner below. These are different environments.

## Hand a long task to Codex from Claude Cloud

When a long, self-directed task should run under your oversight, such as a GPU validation run, you can run Codex in your own cloud session. Use [`codex-in-claude-cloud/`](codex-in-claude-cloud/README.md) for this. It gives you a runner that resumes Codex if it stops, a keep-alive (`codex-hold.sh`) that restarts a dead runner and wakes you, and a two-file mailbox. A Codex manager can run a whole project this way, with its sub-agents doing the tasks.
- **A worker restart kills every process,** the keep-alive included. While a run is live, keep a scheduled check-in at most 20 minutes away (`send_later`). Have every check-in re-arm `codex-hold.sh` with all live run folders. Also register each live run in `~/codex/runs.txt` for `codex-hold-daemon.sh`, which a SessionStart hook relaunches, so a dead runner restarts as soon as the session comes back ([README](codex-in-claude-cloud/README.md#start-a-run)). Ask the owner once to add that hook, because auto mode refuses Claude's edits to its own settings.
- **Install the astrid-dev skills** for Codex (`~/.agents/skills`), and give the manager its plan, its branches, the route-to-model table, and the rules that differ under Codex. The README lists those rules.
- **Brief a manager as a manager.** Start every Codex manager from [`manager-brief.md`](codex-in-claude-cloud/manager-brief.md), and re-read it before each new run, because it changes. Codex takes its authority only from its starting prompt. A mailbox note can't later grant it merge rights or change its role, and it rightly refuses to accept one. A prompt that forbids integrating ("never push to int/…") makes Codex a worker, and you end up relaying every branch between it and someone else. To change a running Codex's role, have it checkpoint (push work in progress, write a handover entry, end `DONE`) and start a fresh manager run that continues from the handover.
- **You host it, so you answer for it.** Codex can't keep itself alive, wake itself, reach the owner or run a model outside Codex. You hold all of those, so you are the run's [accountable agent](../astrid-dev-shared/run-contract.md#who-answers-for-a-run). Say "my run" and "my Codex manager", not "the manager" as if it were someone else's. At every check-in, without waiting for the mailbox:
  - **Compare `tasks.md` and the integration branch with the last check-in.** If nothing moved, find out why from `codex.log` and send one next action through `to-codex.md`.
  - **Start every task Codex can't run** (a route bound to a Claude model, or the review) as soon as its inputs have landed, not when Codex asks.
  - **Clear what is stuck on your side:** an unmerged or conflicting progress PR, a dead runner, a refused command to take to the owner.
  - **Open the final PR and bring the owner their decisions.**
- **Codex still manages the tasks.** Don't redo its fixes, re-review what its reviewer passed, or relay its branches: it dispatches, judges and integrates under the authority in its starting brief. Answer its questions, and raise a structural cause when its reports show a pattern it hasn't named.

## Path 2: advise

Answer the one bounded question you were given: a genuine blocker, conflicting evidence, or a consequential judgment the accepted plan can't settle. This is not routine per-task approval.

- **Refresh the facts first:** the exact candidate, source and donor identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Question the question.** Ask why it reached you: missing evidence, an unclear task card, or a gap in a skill or the plan. Sometimes the right answer is a different question.
- **Leave the asker better equipped.** Say how they could have settled it themselves (which file, check or evidence), and fix that gap at its source: the task card, the plan, or a skill (through a PR). If you can't fix it now, add an entry file to the [process ledger](../../docs/ledger/README.md). The aim is to be asked less over time.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a concrete challenge against over-engineering.
- **Require the previously failing check** to run on the repaired candidate.
- **Don't:**
  - waive failures, widen scope, reset counters, add a review stage, or authorize execution or publication;
  - invent model IDs, or claim a run happened without evidence.

## Path 3: check in (only when the owner asks)

When the owner asks for regular check-ins on a run, record the agreed cadence and end condition as `checkin` in the run's `run.yaml`. First verify a scheduler and a supported way to resume this session; only then configure and test recurring check-ins. A timer or GitHub comment alone does not resume a separate Codex Cloud chat. Without a verified path, use bounded foreground polling while active and tell the owner when a manual nudge is needed. The Claude-hosted runner has its own liveness requirements above; those are separate from strategic check-ins. These documents never start a check-in themselves.

Each check-in compares the run with the previous check-in. To gather the facts (logs, CI runs, the manager's recent events), send N helpers; keep the judgment yourself.
- **Liveness (every check-in):** if the manager is idle while work is in flight, the nudge is to wake it with one next action.
- **Strategy:** if the catalog order or a plan's state no longer matches [`strategy.md`](../../strategy.md), report the mismatch to the owner. Don't edit it yourself.
- **Progress record (every check-in):** check that the plan's `tasks.md` matches reality. Merged PRs should be ticked, and open and blocked tasks should show their state. If it lags, the nudge is to bring it up to date. Report progress from it, not from memory.
- **Moving:** tasks finished or candidates landed since last time.
- **Stuck:** the same failure twice, the same open question, or idle agents.
- **Blocked:** waiting on a person, an event or a dependency, and for how long.
- **Drifting:** work outside its scope, or something undoing a recorded decision.
- **Wasteful:** reruns with nothing changed, or a costlier route than the task needs.
- **Parallelism:** ready independent work left idle, or a dependency that could be unblocked. Give the manager the goal; let it choose and supervise its workers.

For each manager or cross-track blocker, take the next useful action:
- **On track:** note one line; send the manager nothing.
- **Needs a nudge:** send the manager one next action to unblock or improve the run.
- **Needs the owner:** bring one decision with your recommendation.

**Improve astrid-dev as you go.** When the run hits friction in astrid-dev itself (an unclear skill, a missing template field, a slow check), add an entry file to the [process ledger](../../docs/ledger/README.md). If the fix is small and touches only astrid-dev docs or skills, open the fixing PR in the same check-in and add a `fix` entry in it that follows the entry it resolves. Friction specific to this one run goes in its [decisions ledger](../astrid-dev-shared/templates/decisions-ledger.md) instead.

After three check-ins in a row with nothing to report, you may recommend a slower cadence; keep the agreed cadence until the owner changes it or its end condition is met. A check-in may nudge an existing manager to continue already authorized work through a verified resume mechanism; it grants no new scope, spend or publication authority.

## Path 4: close

**Cancel the check-ins when the project is done.** When the project is complete, cancel every check-in you scheduled. Do the same when its end condition is met or the owner says stop. A project is complete when its completion PR merges. Confirm none remain, and tell the owner they have stopped.
