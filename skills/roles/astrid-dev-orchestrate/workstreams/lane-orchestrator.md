---
description: Run one lane of a release for the Release Lead end to end, deciding inside the plan and coming to the Lead only at anchor points.
---

# Workstream: run a lane for the Release Lead

## Workstream contract

**Outcome:** The lane's carded plan runs end to end in this session, with decisions taken and recorded here and the Lead's attention spent only on anchor points.
**When to use:** When the owner's launch message makes this session a release lane's orchestrator, with the Release Lead as advisor (the Lead's side is its [lane orchestrators workstream](../../astrid-dev-lead/workstreams/lane-orchestrators.md)).
**Inputs:** The plan's `tasks.md` cards and `Run start` line on astrid-dev `main`, the owner's launch message, and this session's Codex login.
**Procedure:** The rules below, together with the [Codex-in-Claude workstream](codex-in-claude-cloud.md) for hosting Codex.
**Completion:** Every card ticked in `tasks.md`, each landing confirmed by the Lead, the check-ins cancelled, and a short closing report to the Lead.

Written from Release 15's lanes (23 November 2026); the [process ledger](../../../../docs/ledger/2026-11-23-lane-launch-lessons.md) has what went wrong without them.

## Rules

- **Check your Codex login once** before dispatching: `codex exec --skip-git-repo-check -s read-only 'Reply ok.'`. If it reports a usage limit, run the cards on Claude subagents by the same routes (N Haiku, X Sonnet, S and reviews Opus) and tell the Lead in your next report; never borrow another account or key.
- **Message the Lead only at anchor points:** a gate confirmation before merging into a release branch; changing an assertion in a test that exists at the base, or a pin outside the generator-only rule; changing a goal, gate or stop rule; relaxing an integrity fence or an accepted contract; anything paid or touching the owner's machine or media; a blocker you could not get round in two attempts.
- **Decide everything else.** Before asking, answer "what would the Lead say, given the plan, the cards, the run contract and the rulings so far?" and act on it. Record each decision in one line in `tasks.md`. A question that comes up twice gets its answer written into `tasks.md` or the `Run start` line.
- **Report hourly, briefly:** done, in progress, measured numbers, decisions you took, and the one thing you are least sure about. Look one step ahead at each check-in (disk, fixture, a slot, a review, another lane's code) and arrange it before you reach it.
- **Parallelism pass, every hour.** Before you report, list the cards whose dependencies have landed, and compare each with the cards now running: two cards that write the same file or function are one lane, not two. Start every ready card that has no such conflict, up to four writers per repository, each on its own branch; leave none idle because the plan's order says "next". Send route `N` workers (Luna, or Haiku on Claude) to read the code and name the files and functions a card will change, so conflicts are known before the card starts; never give them a verdict. Say in the report how many writers ran, which ready cards waited and why, and whether a split or a reorder would let more run.
- **Take a free CI slot without asking.** Two Agent CI runs may run at once. Check the running `ci.yml` and `lanes.yml` runs, take a free slot, and name it in your hourly report.
- **Send your own comparison with a gate request.** Compare the hosted run by test id against the release baseline and its recorded moving groups. After a small code change, focused tests plus a re-run of the affected shards is enough; a larger change needs a fresh full run on the final head.
- **A test constant that names a pin, and that the test itself says to refresh when the pin moves, is part of the pin commit,** not an assertion change.
- **When a fixture hits a product limit, shrink the fixture's inputs.** Never raise the limit for a fixture.
- **Send cross-lane findings straight to the other lane,** and mention them in your hourly report.
- **Proof before hosted CI.** A speed change is profiled on the installed path before it is built and measured installed before CI; a functional change is shown working live. Hosted CI is the final check, never the discovery.
- **Coordinate overlaps directly.** When the `Run start` line names another lane touching the same code or fixture, agree the order with that session yourself; bring the Lead only a conflict you cannot settle.
- **Keep the container awake.** An idle container is reclaimed between check-ins and every process in it dies: keep a background `sleep` loop of about 110 minutes running and restart it at each check-in.
- **Merge your own records and plan branch.** `tasks.md`-only progress PRs, evidence PRs of your own plan, and merges into your own `release/<N>/plan-<PP>` branch are yours (and your manager's) to merge on green; only a merge into `release/<N>/main` waits for the Lead's written gate confirmation.
