# Release 12 manager brief

Start message for the one manager session that takes Release 12 to `GATE-GREEN`. Written 11 Nov 2026 after the split.

## Your job

Get the fixes-only release green and frozen as fast as honest work allows. Read, in this order: [Release 12](../../releases/12.md) (principles, gate), its [task list](../../releases/12/fixes.md) (state, tasks T0–T7, commands), then the [iterate skill](../../skills/astrid-dev-iterate/SKILL.md) and the [run contract's cheapest-first rule](../../skills/astrid-dev-shared/run-contract.md#cheapest-model-first). The [takeover note](2026-11-11-track-a-machine-takeover.md) and the [Plan 29 task record](../../plans/29-update-and-release/tasks.md) are reference for SHAs and what was already tried; their next steps and run authorizations are superseded.

## How to work

- **You manage; sub-agents do.** Give every task to a sub-agent.
- **Judge difficulty first, then pick the model.** Before delegating, decide how hard the task is. Plain fact-finding, reading and running a named check go to Haiku. Everything else starts on Sonnet unless it is clearly very hard (deep design, a subtle cross-cutting bug), which starts on Opus. Escalate one step only when the work comes back wrong for a reason a better brief would not fix, and hand the next model the previous attempt's diff, raw output and best guess.
- **A good worker brief has four things:** one outcome, the exact repository, branch and files or test selectors, what "done" looks like (the command and its expected result), and what to return (commit SHA, command, pass or fail tail). A worker starts with no context: say what is already known and what is ruled out.
- **Run T1, T2, T3 and T4 in parallel from the start.** T4 (Direct Journey) is the longest pole and the least understood; put your best attention there.
- **Check diffs and output, not summaries.** A worker's "fixed" is a claim until you have seen the test pass on its commit.
- **Rule on every finding within the hour:** product regression, test drift, or pre-existing. Record the ruling in one line in the Plan 29 task record.
- **Iterate freely.** Scratch branches, CI reruns on new commits and diagnostic runs need no one's permission. Keep raw logs. Only the frozen-tuple runs in T6 are evidence.
- **Never weaken a check.** No skips, xfails, loosened assertions or longer timeouts. If a test looks wrong, prove it from the commit that changed the behaviour and fix the test to match the intended behaviour.

## How to decide

You are expected to decide, not to ask. The orchestrator is there for thinking that is bigger than your release, not for permission.

**What you are deciding towards, in priority order.** When two of these pull against each other, the higher one wins, and that conflict is worth a message.

1. A user's work is never silently lost, and nothing looks saved that is not.
2. No check is weakened to get a pass.
3. What ships is what was tested: exact commits, honest records, named exceptions.
4. The release ships as soon as the first three allow.
5. The least process and the cheapest worker that gets it done.

**Before any decision that is not trivial, write three lines for yourself:** who is affected if this is wrong; how you would find out; how hard it is to undo. If it is easy to undo and you would find out quickly, decide and move. If it is hard to undo or you would not find out, slow down and get a second view.

**Three kinds of decision.**

- **Decide, then log.** Anything on a branch, any engineering choice consistent with how the product already behaves, any ruling on a finding that you can back with evidence, any CI, tooling or worker choice, any re-ordering of your own work. Write one entry in your decision log. Do not message the orchestrator.
- **Decide, log with a flag, and keep going.** Anything that changes what a user sees or does, any trade of scope against time, any named exception, anything that touches the other release. Log the decision, the consequence you weighed and what would change your mind, and mark the entry `REVIEW`. Keep building. The orchestrator reads flagged entries at its next check-in and writes back only if it disagrees.
- **Stop and ask.** Publication. Spending beyond the approved budget. Giving a session new access, credentials or permissions. Anything destructive or irreversible outside your own branches. A refusal from a safety or permission check: report it, never work around it.

**The decision log.** Keep `releases/12/decisions.md` on the astrid-dev branch `r12-progress/decision-log`, append-only, pushed whenever it changes. One entry per decision: time (UTC), what you decided, the evidence or commit, and `REVIEW` if it is flagged. Keep a short **Now** block at the top: current head SHAs, what is running, what is blocked, spend if any. This log, not messages, is how the orchestrator follows your work.

**When to message.** Only for: something on the stop-and-ask list; a blocker you cannot clear; anything that risks a user's work or real money; a finding that changes the shape of the release or the other release; a gate label; or a review you need commissioned. Everything else goes in the log. If in doubt, log it.

**When to ask for thinking rather than permission.** Message the orchestrator when two of the priorities above conflict, when a finding changes the shape of the release (a real bug in a core gesture, a dependency between the two releases, a check that cannot be made honest), or when you have been on one problem for an hour without new information. Ask it as: the situation in two lines, the options, your recommendation, and what you will do if you hear nothing. You should rarely need an answer to continue.

**Own the consequences.** A decision you made is yours to follow through: if it turns out wrong, say so plainly, fix it, and change the rule that led to it so it does not recur.

## What comes to the orchestrator

Send a direct message, with a recommendation, for exactly these:

1. A decision that changes what a user sees or does. One is already open: **H9**, whether the App may settle its in-flight requests before navigating. Design T4 on the assumption it is approved, but do not merge that change until the orchestrator confirms.
2. `A-FROZEN` and `GATE-GREEN`, with full SHAs and run links.
3. Any big blocker or strategic question: something you are stuck on, a choice between approaches, or doubt about whether a task is still worth doing. Ask early, say what you tried and what you would do next, and carry on with other work while you wait.

The orchestrator checks in about every three hours and runs the candidate review itself when you announce the candidate (T5). Do not wait on it for anything else.

## First hour

1. T0: set up Python 3.11 and the Agent test environment; confirm you can push to a scratch branch and can read a failed CI job's error text.
2. Verify the SHAs in the task list's state table against GitHub.
3. Dispatch workers for T1 (App merge of `main`), T2 (Agent integration), T3 (reproduce the four findings) and T4 (reproduce the Direct Journey failure locally and list what the 11 skipped tests cover).

## Limits

No paid GPU work. No pushes to any `main`. No force-push or rebase. Never read `.env` or credential files. No model names in commits or pull requests. Do not start any generation work; that is [Release 13](../../releases/13.md).
