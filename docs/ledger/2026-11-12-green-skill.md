Date: 2026-11-12
Kind: fix
Source: The incomplete-CI-results entry, and the owner's request for one skill covering the whole get-to-green journey
Resolved by: —

A new skill, `astrid-dev-green`, is now the one home for getting test results complete and acting on them.
- It measures first: it sorts jobs into test jobs, aggregates, non-test checks and expected omissions, and treats a cancelled, timed-out, setup-failed or zero-test test job as NO-RESULT. It diagnoses each kind of early stop with a NON-PROOF run, kept apart from the qualifying run.
- It then branches into mode A (no new failures, a gate, where a flip or a deleting commit excuses nothing) or mode B (retire old red by cause, in batches, with limits for when to spec a project).
- It holds the GitHub Actions practice #527 removed.

Iterate stays the single-change loop each card runs. The run contract now limits "never broad" to local runs. Manage's hang, serial-chain and "never take on full CI health" lines now link to the new skill. The release gate names complete CI runs, and the candidate's `int/**` runs for Agent CI and Lanes, which don't run on pull requests. Tool changes (timestamp stripping and NO-RESULT detection in `baseline-diff.py`) and moving the quarantine rule are separate follow-ups.

Follows: 2026-11-12-incomplete-ci-results
