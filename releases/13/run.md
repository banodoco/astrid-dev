# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (13:00 UTC Sun 15 Nov): read this first

**Hannah's GO is given** (0.0.13, full, REQUIRED update; publish without waiting for the final head's full CI). **Blocker:** an upgrade regression. Every older install updating to 13 is rolled back (BootManifestDrift; 9f00e2ae2/a26030e78). Cells' r13/cells-bootmanifest is due ~14:05. The journey on the new harness harness/31-r13-upgrade (R0/R9/R11/R12 → 13, fresh) runs 43715487164 on A″ to scope it.
**A‴ components:** A″ 34fee0cf + boot-manifest (pending) + the Windows stack r13/machines-winnofollow (pending: winclaim, fcntl, graph_facts, credential read) + logfetch 8b6f8434d (W181 proof) + redact 887f81594 (READY) + LTX marker 8519cd2a0 (READY).
**Then:** freeze → App re-pin with --require → journey all rows → publish (Agent → Runtime fast-forward 6855dfa8 → App → deploy check). ETA live ~16:30.
**Post-R13:** first update = model lookup (cells) + generate-failure leftovers. R14 = local speed (Plan 55), and release docs 14–19 in astrid-dev#664. Balance $77.5428138996, 0 pods.
