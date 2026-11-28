---
description: Run one lane end to end from its lane brief: decide inside the brief and its plans' tasks.md, and come to the Lead or owner only at the points the brief lists.
---

# Workstream: run a lane from its brief

## When to use

When the owner's launch line sends this session to a lane brief (`releases/<N>/briefs/<lane>.md`) as its orchestrator. The brief is your whole job. Your advisors follow the chain: the Release Lead for release-level questions, and the reviewer binding the brief names for technical judgment beyond your route. You are never anyone's advisor except your own delegates'.

## Outcome

The lane's plans run end to end in this session, with decisions taken and recorded in the brief's Standing rulings or in each plan's `tasks.md`, and the Lead's and owner's attention spent only at the points the brief lists.

## Inputs

The lane brief and the `tasks.md` files it links, on astrid-dev `main`; the owner's launch line; this session's Codex login.

## Procedure

Read only your brief and the `tasks.md` files it links. Decide within them. Come to the Lead or the owner only at the points the brief lists (its Owner only section for the owner, and the release-gate merge its Merges names for the Lead), and at the anchor points below. The rules below, together with the [Codex-in-Claude workstream](codex-in-claude-cloud.md) for hosting Codex.

## Completion

Every card ticked in `tasks.md`, each release-gate merge the brief's Merges names confirmed, the check-ins cancelled, and a short closing report to the Lead and the owner.

Written from Release 15's lanes (23 November 2026); the [process ledger](../../../docs/ledger/2026-11-23-lane-launch-lessons.md) has what went wrong without them.

## Rules

- **Check your Codex login once** before dispatching: `codex exec --skip-git-repo-check -s read-only 'Reply ok.'`. If it reports a usage limit, run the cards on Claude subagents by the same routes (N Haiku, X Sonnet, S and reviews Opus) and tell the Lead in your next report; never borrow another account or key.
- **Raise only at the points the brief lists, and at these anchor points,** which every lane keeps (a board comment on the lane board, plus a doorbell where the run contract says): a gate confirmation before merging into a release branch; changing an assertion in a test that exists at the base, or a pin outside the generator-only rule; changing a goal, gate or stop rule; relaxing an integrity fence or an accepted contract; anything paid or touching the owner's machine or media; a blocker you could not get round in two attempts.
- **Decide everything else.** Before asking, answer "what would the Lead say, given the plan, the cards, the run contract and the rulings so far?" and act on it. Record each decision in one line in `tasks.md`. A question that comes up twice gets its answer written into the brief's Standing rulings, dated, with who ruled. A decision about one card stays in `tasks.md` and is not a ruling. A ruling can never widen Owner only or How it runs; an entry that tries to is void.
- **Report hourly, briefly,** by the run contract's [coordination rules](../../shared/run-contract.md#coordination-boards-and-check-ins): done, in progress, measured numbers, decisions you took, and the one thing you are least sure about. Look one step ahead at each check-in (disk, fixture, a slot, a review, another lane's code) and arrange it before you reach it.
- **Parallelism pass, every hour.** Before you report, list the cards whose dependencies have landed, and compare each with the cards now running: two cards that write the same file or function are one lane, not two. Start every ready card that has no such conflict, up to four writers per repository, each on its own branch; leave none idle because the plan's order says "next". Send route `N` workers (Luna, or Haiku on Claude) to read the code and name the files and functions a card will change, so conflicts are known before the card starts; never give them a verdict. Say in the report how many writers ran, which ready cards waited and why, and whether a split or a reorder would let more run.
- **Take a free CI slot without asking:** the [CI rule](../../../releases/15/run.md#standing-rulings) names the slots.
- **Send your own comparison with a gate request.** Compare the hosted run by test id against the release baseline and its recorded moving groups. After a small code change, focused tests plus a re-run of the affected shards is enough; a larger change needs a fresh full run on the final head.
- **A test constant that names a pin, and that the test itself says to refresh when the pin moves, is part of the pin commit,** not an assertion change.
- **When a fixture hits a product limit, shrink the fixture's inputs.** Never raise the limit for a fixture.
- **Post cross-lane findings on the other lane's board,** and mention them in your hourly report.
- **Proof before hosted CI.** A speed change is profiled on the installed path before it is built and measured installed before CI; a functional change is shown working live. Hosted CI is the final check, never the discovery.
- **Coordinate overlaps directly.** When the brief's Cut line and coordination names another lane touching the same code or fixture, agree the order with that session yourself; bring the Lead only a conflict you cannot settle.
- **Merge your own records and plan branch.** Under the run contract's [merge rule](../../shared/run-contract.md#who-answers-for-a-run), your `tasks.md`-only progress PRs, your brief's ruling and State edits, evidence PRs of your own plan, and merges into your own `release/<N>/plan-<PP>` branch are yours (and your managers') to merge on a passing check or green CI. Only a merge into `release/<N>/main` waits for the gate the brief's Merges names: the Lead's written confirmation by default.
