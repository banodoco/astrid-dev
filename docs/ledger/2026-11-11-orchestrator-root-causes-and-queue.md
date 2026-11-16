Date: 2026-11-11
Kind: fix
Source: Owner, after Plan 48's Phase 1 run
Resolved by: —

The orchestrator answered the Phase 1 manager's questions without fixing why they were asked, and nothing told it to keep a queue of phases moving. Three causes from that run are now rules. The manager merged a stale local `main` and reported the conflict as a display lag: the manage skill now says to fetch, read the real tip and check it is an ancestor. Progress PRs were opened per update and one conflicted and sat unmerged, while `tasks.md` was also edited on the integration branch: the manage skill now says progress goes only through small auto-merged PRs, each confirmed merged at the next update. Its old text also said to merge without waiting for CI, which `main`'s required checks no longer allow. The orchestrate skill now says every question is a symptom to fix at its source in the same turn, records check-in cadence on the plan's Run start line, and has a rule for an owner's queue: prepare the next item early, get one standing go, confirm at each check-in that the manager moved on, and build a gated item on its integration branch.

Follows: 2026-11-11-nobody-answered-for-the-run
