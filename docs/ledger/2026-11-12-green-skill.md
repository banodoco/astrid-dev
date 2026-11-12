Date: 2026-11-12
Kind: fix
Source: The incomplete-CI-results entry, and the owner's request for one skill covering the whole get-to-green journey
Resolved by: —

A new skill, `astrid-dev-green`, is now the one home for getting test results complete and acting on them.
- It measures first and treats a cancelled, skipped, setup-failed or zero-test job as NO-RESULT. It closes each kind of early stop with a NON-PROOF run.
- It then branches into mode A (no new failures, a gate) or mode B (retire old red by cause, in batches, with limits for when to spec a project), then guards.
- It holds the GitHub Actions practice #527 removed.

Iterate stays the single-change loop each card runs. The run contract now limits "never broad" to local runs. Manage's hang, serial-chain and "never take on full CI health" lines now link to the new skill. The release gate names the candidate's `int/**` run, because Agent PRs start no CI. Tool changes (timestamp stripping and NO-RESULT detection in `baseline-diff.py`) and moving the quarantine rule are separate follow-ups.

Follows: 2026-11-12-incomplete-ci-results
