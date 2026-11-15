# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (15:00 UTC Sun 15 Nov): read this first

**Hannah's GO is given** (0.0.13, full, REQUIRED; at 16:35 she chose a compact required card). **FINAL candidate:** Agent 91b60416 (A⁗ = A‴ + cycle fix a06d55a79 + rollback-safe restamp 1e1aa811a; PR astrid-agent#347) and App e7d27462 (PR astrid-app#268). Manifest sha256 206601dc…, Runtime 6855dfa8.
**Gate (all running):**
- W200: restamp rollback/busy/exact-match re-proof;
- W207: delta read of the App notice change;
- 13 journey rows on agent 91b60416 (43725021701, no failures so far) + 3 fresh rows on App e7d27462;
- A⁗ fast checks (cycle gate);
- PR #268 by name (release-guard, three-products).
**Then publish:** Agent #347 → Runtime fast-forward → App #268 → deploy → served-manifest check. ETA live ~17:15.
**Deferred to the first update:** model lookup (cells, paused), log-fetch 4eb67605d (MERGE-READY), touch-layout card overlap. R14 = local speed (Plan 55). Balance $77.51, 0 pods.
