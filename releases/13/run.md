# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (14:00 UTC Sun 15 Nov): read this first

**Hannah's GO is given** (0.0.13, full, REQUIRED update; publish without waiting for the final head's full CI). A‴ is frozen: Agent 8e0006f5 (int/r13-8e0006f5); App 200e6647 (required block). Publish PRs are open but not merged: astrid-agent#347 and astrid-app#268.
**Blockers:**
- (1) **W194 on the boot-manifest restamp:** rollback to R12 breaks after the restamp, a busy host gets restamped, and the match isn't exact. Cells' bootmanifest2 is due ~15:05.
- (2) **The hosted Import-cycles gate is red:** machines' redact f5d8c2b9d added it. Fix: move redact_log to a leaf module, a new commit on r13/machines-redact.
**Journey on A‴ (43718444065):** 8/13 green, including R0 → 13 on Linux and macOS, R12 → 13 on macOS and R9 on Linux; none failed so far.
**Then:** A⁗ = A‴ + bootmanifest2 + the cycle fix (+ log-fetch add-on 51971b0e2 if W197 is MERGE-READY). Then re-pin the App, rerun W194's probes and the full 13 rows, and publish. ETA live ~16:45.
**Post-R13:** first update = model lookup (cells; built, paused) + generate-failure leftovers. R14 = local speed (Plan 55). Balance $77.51, 0 pods.
