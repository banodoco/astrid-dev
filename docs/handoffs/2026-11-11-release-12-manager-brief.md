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
