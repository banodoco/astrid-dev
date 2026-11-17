Date: 2026-11-17
Kind: issue
Source: the Release 14 Lead, setting up packet dispatch for every Release 14 plan except 59 and the release's issues, 17 November 2026
Resolved by: 2026-11-17-issue-packets

The fresh-packet dispatch workstream let a packet refer only to one plan's `tasks.md` rows and sent every packet pull request to a plan branch, never `release/<N>/main`. A release's issues have no plan: by the Release skill they land through a fix branch `release/<N>/<topic>` into `release/<N>/main`. So the owner's request to farm out all remaining Release 14 work, issues included, had no route for the issues, and a packet session following the packet start message ("PRs target release/<N>/plan-<P>") could not do a fix.
