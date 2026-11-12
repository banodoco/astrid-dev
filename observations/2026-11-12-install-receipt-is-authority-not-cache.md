Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (smell 2)
About: F-001; Plan 09
Outcome: open

Engine install receipts are treated as an authority, not a cache. A changed recipe hash returns a generic `integrity_failed` instead of converging on the new recipe (Agent `engine_runner.py` about 590-596 and 925-927). Not sure whether U1–U5 removes this or only the reinstall; check when U1–U5 merges. Same family as Plan 09 Phase 2's incomplete installation-state transitions.
