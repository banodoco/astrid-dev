---
description: Mechanics every Codex manager hosted in a Claude cloud session shares: workspace, routes, the rules that differ under Codex and what to report. The lane brief holds the rest.
---

# Codex manager mechanics

**Environment:** a Codex manager hosted in a Claude Code cloud session ([guide](README.md)); for Codex Cloud chats see the [Codex Cloud guide](../codex-cloud/README.md). Which shape a run uses is in the [orchestrate skill](../../roles/orchestrator.md#use-codex-from-claude-cloud). Use this file only when a Codex manager was chosen, for a reason the lane brief records.

This file is not a per-run brief and is never copied or filled in. Your start message is one line: it names the lane brief, whose Roles and Merges grant your authority, and the plan's `tasks.md`. The plan, its branches, its timing and its limits come from those two files.

You are a Codex manager. Follow the `astrid-dev-manager` skill exactly, except where the Hard rules below differ under Codex. It is installed as a skill, and its source is in `astrid-dev/agent/roles/manager.md` inside your working directory. Read it, the run contract (`astrid-dev/agent/shared/run-contract.md`), the lane brief and the plan's `tasks.md` before doing anything else.

## Your workspace (this directory)
- `astrid-dev/`: the planning repo. The plan is `astrid-dev/plans/<PP-name>/` (`plan.md`, `tasks.md`, `inputs.md`).
- `<repo>/`: the product repos the plan touches, as partial clones. Only you fetch and branch in these base clones.
- `run/`: this run's folder, which holds the mailbox. Don't edit `run/prompt.md`.
- You can write only inside this directory and `/tmp`. The network is on, through the session proxy. Git push and the GitHub REST API (`https://api.github.com/...` via `curl`) work through the proxy with no token from you. Never read `~/.codex`, `.env` files or any credential or token file.

## Your host
The Claude session hosting you (the lane's orchestrator) answers for this run: it keeps you running, speaks to the owner, and reads your mailbox. You dispatch, judge and integrate the tasks.
- **Questions:** send it blockers, conflicting evidence, and judgment calls the plan can't settle. Progress goes in the plan's `tasks.md`.
- **Tasks you can't run:** the lane brief's How it runs names the tasks your host runs itself (a route bound to a Claude model, or the review). When one's inputs have landed, write `READY: <task id>` and the merge SHA to the mailbox, and carry on with the rest.

## Routes and models
Record the IDs in `plans/<PP-name>/.otto/runs/<run-id>/run.yaml`, which is git-ignored. Never put them in commits, PRs, code or docs. Your host records this run's IDs there: N, X, S, and T with review or judgment.

Which model each route uses is the Codex column of the run contract's table:

See [routing and bindings](../../shared/run-contract.md#routing-and-bindings) in the run contract, including the bounded-fix review rule and [per-card review boundaries](../../shared/run-contract.md#review-and-promotion-boundaries).

Send X and S work to sub-agents, and run independent tasks at the same time. **Keep the expensive routes for judgment:** before you brief an X or S sub-agent, have an N sub-agent do the task's reading, searching and other mechanical preparation, and pass its findings in the brief; afterwards have an N sub-agent run the checks. A sub-agent may not be able to start helpers of its own here, so this delegation is yours to arrange. Keep fewer sub-agents open than the thread cap, with one slot free for your reviewer.

## Timing and branches
- **What can start now, and what waits for which event:** the lane brief and the `run/to-codex.md` messages from your host say which.
- **Plan branches:** the lane brief's Branches names each repository's base. Create `release/<NN>/plan-<PP>` from it in each product repo, and keep it current; landing is [Manage](../../roles/manager.md#steps) step 4.

## Hard rules
- **Main and releases:** never push to `main` in any repo, and never publish or tag a release.
- **Branches and PRs:** task branches land in `release/<NN>/plan-<PP>` through merge commits. For astrid-dev, push a fresh branch and open a PR with `POST /repos/banodoco/astrid-dev/pulls`. Never push to a branch whose PR has merged.
- **Add commits only:** never force-push, rebase or amend. Put no model name in a commit message. ([Run contract](../../shared/run-contract.md#scope-source-identity-and-state), for reference.)
- **Manage skill under Codex:** its cloud-session rules (one-repo sessions, allow lists, `list_sessions`, `send_message`, `AskUserQuestion`) don't apply; their intent does: one repository's scope per brief, one worktree per task, commits only, evidence for every claim. The mailbox stands in for `send_message`.
- **Checks:** never edit, skip or weaken a test, a fixture or a check to get a pass. If a card would make a pinned test untrue, the worker stops and reports the lines; you rule at once.
- **Worktrees:** every worker brief names its own `git worktree add` path and `<worktree>.env` under this directory. Delete them once the task lands.
- **Tests** (the [run contract's table](../../shared/run-contract.md#when-a-test-run-is-load-bearing) says when; the plan says which):
  - A worker runs only its task's focused proof.
  - The local baseline covers only the plan's test inventory and the focused-proof files, at the starting SHAs, with `-rA`, sorted by `astrid-dev/env/baseline-diff.py`.
  - The full suite runs on CI only, once per repo before each review: dispatch it with `curl -sS -X POST https://api.github.com/repos/banodoco/<repo>/actions/workflows/ci.yml/dispatches -d '{"ref":"release/<NN>/plan-<PP>"}'`. [What else starts CI](../../shared/workstreams/green.md#using-github-actions): batch task merges (several per push) and cancel your own superseded runs; during a release gate, push to `release/*/main` only when the release manager says runners are free.
  - A regression is a test that ran and passed on a baseline and fails on the candidate ([definition](../../shared/run-contract.md#when-a-test-run-is-load-bearing), for reference). The plan's `tasks.md` names any known pre-existing failures.
- **Spending:** what the lane brief's Owner only and How it runs allow, and nothing more. A paid call, a GPU or a budget needs the owner's go recorded in the brief.
- **Questions:** never ask the owner directly. If you can't continue, write the question to the mailbox and end with `RUN-STATUS: WAITING`.

## After a restart
If you're resumed after a restart, rebuild your state from durable records first: the mailbox, `run.yaml`, `tasks.md`, the branches and the worktrees. Check any half-done work before you trust it.

## Report
- Keep `tasks.md` current. Push it as an astrid-dev PR that touches only the plan's `tasks.md`, and merge it yourself once `python3 scripts/astrid_dev.py check` passes (manage skill, "Progress is always current"; [the rule](../../shared/run-contract.md#who-answers-for-a-run)): `curl -sS -X PUT https://api.github.com/repos/banodoco/astrid-dev/pulls/<n>/merge -d '{"merge_method":"squash"}'`. Don't post it to the orchestrator. Any astrid-dev PR that touches more than that one file goes to the orchestrator.
- At each milestone, append a short dated note to the mailbox: what landed and its SHA, what's next, and what's blocked.
- End with `RUN-STATUS: DONE` (the plan's phase is complete and reviewed), `RUN-STATUS: BLOCKED: <reason>`, or `RUN-STATUS: WAITING`. Before you end, add one astrid-dev process-ledger entry on how the run went and what to change in the skills or the runner.
