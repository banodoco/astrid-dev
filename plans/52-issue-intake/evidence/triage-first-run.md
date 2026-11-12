# The first triage pass on astrid-dev (Plan 52 II-12, real pass)

12 Nov 2026, about 20:35 UTC, at a check-in, under the Issues section as merged in #620. The manager read all 40 open issues and wrote the plan; the orchestrator applied the labels (the manager's label writes are refused by the classifier). Nothing was closed, edited or commented.

## Before and after

| Search (all `repo:banodoco/astrid-dev is:issue`) | Before | After |
| --- | --- | --- |
| `is:open` | 40 | 41 (one filed after the read: #622) |
| `is:open -label:backlog -label:planned` (New) | 40 | 1 (#622) |
| `is:open label:backlog` (Backlog) | 0 | 39 |
| `is:open label:planned` (Planned) | 0 | 0 |
| `is:open label:backlog label:planned` | 0 | 0 |
| `is:open` with none of `observation`, `bug`, `idea`, `question` | 3 (#621, #368, #40) | 1 (#368) |
| `is:closed reason:completed` / `reason:"not planned"` / `reason:duplicate` | 1 / 1 / 0 | 1 / 1 / 0 |

Check-in report: new 1, backlog 39, planned 0, closed since the last check-in 0.

## What was decided

- **Planned: none.** No task row in any plan cites an open issue. (The `#40` in Plan 29's tasks is Runtime pull request #40, not this issue.)
- **Backlog:** the 22 migrated observations (#575 to #596) keep their labels and gain `backlog`; so do #601, #603, #605, #606, #607 and #610 to #619. #621 gains `observation`, `plan:39` and `backlog`. #40 gains `bug` and `backlog`. #368 gains `backlog`.
- **Left in New:** #622, filed at 20:35, after the read; it is for the next check-in.
- **Proposed closure for the owner's batch:** #368 (the Release 12 coordination mailbox), as not planned, with one comment: "Release 12 coordination mailbox; the release is over and the issue grants no authority." Not closed; the owner should confirm Release 12 is finished first.
- **Duplicates:** none found. #615 names #606 as a separate issue; #577 and #578 are different failures. So `reason:duplicate` is **not confirmed**: the search is valid and returns 0, but no issue has been closed as a duplicate to show it listing one.

## Not done in this pass

The planted case on the scratch repository (three issues that try to steer the reader) has not been run; II-12 stays open for it.
