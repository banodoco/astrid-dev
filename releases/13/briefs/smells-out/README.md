# Observations

Things someone saw in Astrid that are not planned yet: a smell, a suspected bug, a usability trip, a slow path. Log it in a minute and carry on. An observation is not a plan, a task or a commitment; it is what a planner reads before writing one.

**One file per observation**, named `YYYY-MM-DD-<short-slug>.md` (lowercase letters, digits and hyphens), so PRs never conflict. Format:

```
Date: 2026-11-12
Source: where it was seen (a run, a release, a review, a person)
About: F-008; Plan 32   (gap IDs and plans it bears on, or — if you don't know)
Outcome: open

One short paragraph: what was seen, how sure you are, where in the code if known, and what would settle it.
```

**Outcome** is the only line anyone edits later. It is one of:

- `open`: nobody has placed it yet.
- `folded: plans/NN-name/tasks.md <task id>`: a plan's task now covers it. The plan owns it from here.
- `fixed: <repository>#<PR>` or a commit: it was small and someone fixed it.
- `issue: #<number>`: it became an incident with a user to recover ([bug skill](../../skills/astrid-dev-bugfix/SKILL.md)).
- `dropped: <reason>`: looked at and not worth doing, or no longer true.

New evidence is a dated line added under the paragraph. Nothing else is edited or deleted. Keep credentials, private logs and machine-specific data out, as in any project pack.

## Where things go

| You have | It goes |
|---|---|
| Something seen in the product, not planned, maybe not certain | here |
| Friction in astrid-dev itself (a skill, template, check) | the [process ledger](../../docs/ledger/README.md) |
| A failure a user needs recovering from | a [bug issue](../../.github/ISSUE_TEMPLATE/bug.md) |
| A finding inside a running project's own scope | a row in that plan's `tasks.md` |
| A missing outcome that would still matter if today's projects were replaced | a [gap](../../vision/README.md) |

## How it feeds plans and gaps

- **Planning.** Before scoping a plan or a task list, read the open observations about that plan and its gap: `grep -l "^Outcome: open" observations/*.md | xargs grep -l "Plan 32"`. Fold the ones the plan will cover by adding a row to its `tasks.md` and setting `Outcome: folded: …`.
- **Gaps.** When a gap is reassessed, its open observations are evidence for its Current state. Several open observations about one gap with no plan is the sign that a route step is missing.
- **Releases.** When a release closes, whoever closes it reads the observations still `open` from that release's runs and gives each an outcome, or leaves it open with a dated line saying why.

Until the check and the generated list exist (draft plan: observations register), this folder is unchecked: keep the four header lines exact so the check can adopt these files unchanged.
