Date: 2026-11-16
Kind: fix
Source: the Release 14 page checked against GitHub on 16 November 2026: its Branches table said `not yet cut` for branches that exist, and two `release/14/*` branches were not listed
Resolved by: —

The Branches table is checked for structure only, so it could drift from the repositories. `scripts/release_branches.py` checks it by hand against GitHub (branch existence, unlisted branches, merged heads and cut commits) and lists heads for a tester build. The Release skill says when to run it and requires a clean check before the owner's go; the tester build procedure, branch protection and branch clean-up are written there once.

Follows: 2026-11-16-release-branches-per-repository
