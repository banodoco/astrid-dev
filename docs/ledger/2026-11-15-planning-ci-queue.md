Date: 2026-11-15
Kind: issue
Source: Pull request 664 and the owner, 15 November 2026
Resolved by: 2026-11-15-planning-ci-auto-merge

Planning PR 664 sat unmerged for over an hour: each required documentation run waited 16–21 minutes for a GitHub-hosted runner, then ran for about one minute. Pushes and PR-description edits queued about a dozen documentation and review-intake runs without cancelling superseded runs. Three pushes failed scripts/test_golden.py because the author ran only the repository check locally, omitting unit tests. Auto-merge also needed enabling by hand on every PR. The owner asked to reduce this friction systematically and merge relevant PRs automatically after checks pass.
