Date: 2026-11-16
Kind: fix
Source: the owner's decision of 16 November 2026, on Plan 53 running active with no release and on plans with no branch in Releases 14 to 17
Resolved by: —

A plan started without a release, and a release listed plans that no branch carried. `python3 scripts/astrid_dev.py check` now refuses an active plan that is in no unpublished release brief, and, from Release 14, an included plan with no `plan <PP>` row in the Branches table. A plan that changes only astrid-dev gets a row whose Repository is `astrid-dev`, with a release row beside it; no plan is exempt. The check keeps what a Branches row may name in one list, which now includes `astrid-dev`.

Follows: 2026-11-16-release-branch-checks
