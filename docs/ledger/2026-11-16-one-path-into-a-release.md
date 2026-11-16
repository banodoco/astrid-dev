Date: 2026-11-16
Kind: fix
Source: the owner in the advisor's session on 16 November 2026, after two investigations: a pull request could change a release's plan list and merge itself, and issues were tied to releases by title prefixes the release pages never saw
Resolved by: —

A plan joins a release one way: its line under the brief's `## Included plans`, in a pull request the owner approves; a plan split across releases is listed in each brief and has one plan branch per release, and a plan in no brief does not start. An issue joins a release one way: a label, `plan:<P>` for an included plan or `release:<N>` set at triage by the release manager or the owner; the brief's Issues block is the computed list, and a title prefix is not a mechanism. A fix branch names only an issue that is in the release: from Release 14 on, `check` fails a `fix #<issue>` row whose issue is not in the same brief's Issues block. `release_issues.py` recomputes each row's Via from current labels. A pull request that changes any brief's `## Included plans` is no longer auto-merged; it needs the owner, as a change to Kind or State does.

Follows: 2026-11-16-release-branch-checks
