---
description: Host Codex workers or a manager inside Claude Cloud while preserving explicit ownership, permissions and recovery.
---

# Workstream: Codex hosted inside Claude Cloud

## Workstream contract

**Outcome:** Codex work hosted inside Claude Cloud with explicit permissions, ownership and recoverable execution.
**When to use:** When a Claude Cloud Orchestrator hosts Codex as workers or, with justification, as a managed process.
**Inputs:** The approved task or plan, assigned actors, permissions, tool availability, current checkout, and environment guide.
**Procedure:** Establish noninteractive permissions, use the documented Codex-hosting path and preserve source, run and recovery evidence.
**Completion:** Delegated work and remaining blockers have verified receipts and an authorized handoff; no silent permission or merge escalation occurred.

Choose when a Claude Cloud session runs Codex in its container, either as **workers** (default) or, when justified, as a managed Codex process. The detailed commands and scripts remain in the [environment guide](codex-in-claude-cloud/README.md); do not copy them here. Follow the general [Orchestrate role](../SKILL.md) and [run contract](../../../shared/run-contract.md).

## Claude Cloud setup: no permission prompts

A session that waits on a prompt nobody sees is a stalled run. Before any work starts:

- **Worker sessions and their permissions** are set up as in [manage step 1](../../astrid-dev-manage/SKILL.md#steps). Add a missing allow rule by PR with the owner's OK: a rule change is a change to permissions.
- **Refusals:** who may lift one is in the [run contract](../../../shared/run-contract.md#who-answers-for-a-run).
- **Merges:** a manager merges its own progress pull requests; every other merge into `main` needs the owner's go ([the rule](../../../shared/run-contract.md#who-answers-for-a-run)). Auto mode refuses some merges, deletions and settings commits: ask once for the whole run ("merge the plan PRs; my progress PRs auto-merge") and record that go on the `Run start` line (`run.yaml` is local and git-ignored, so it can't carry it: [who answers for a run](../../../shared/run-contract.md#who-answers-for-a-run)).

## Use Codex from Claude Cloud

A Claude cloud session can run Codex in its own container ([`codex-in-claude-cloud/`](codex-in-claude-cloud/README.md)). There are two shapes, and the first is the default:

| Shape | Who manages | Use it when |
|---|---|---|
| **Codex workers (default)** | The Claude session manages: it briefs each card, starts one `codex exec` per card on the card's route, checks the result, commits and integrates ([how](codex-in-claude-cloud/README.md#use-codex-for-the-workers-under-a-claude-manager)) | A project run from a task list. This is what "Codex does the bulk of the work" means unless the owner says otherwise |
| **A Codex manager** | A long-running Codex process manages its own sub-agents; the Claude session hosts it and still answers for the run | One long, self-directed job with few decisions along the way (a GPU validation run), more parallel tracks than the session can supervise, or the owner asks for it. Say which reason applies on the `Run start` line |

This is the one statement that Codex workers are the default; every other file links here. Each route's model is in the [run contract's table](../../../shared/run-contract.md#routing-and-bindings). A Codex manager is a second manager in the same container: it can't commit, reaches you only through a mailbox, and needs a runner and a keep-alive. Don't add that layer by default, and never tell a session to "run the Codex manager" when you mean "send the cards to Codex".

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
