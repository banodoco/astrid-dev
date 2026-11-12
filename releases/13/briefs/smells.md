# Smells observed in Release 13 work (12 Nov) — logged, not yet planned

1. **A managed engine can't upgrade in place.** A changed helper or environment identity forces a manual reinstall into `<root>-clean` (`engine_contracts.py` about 78-103; `engine_runner.py` about 575-618). That fires on almost any Astrid release. (Being fixed: U1–U5, in the candidate.)
2. **Install receipts are treated as an authority, not a cache.** A changed recipe hash gives a generic `integrity_failed` instead of converging (`engine_runner.py` about 590-596, 925-927).
3. **Model declarations come in five shapes,** and VibeComfy silently guessed `checkpoints` for unknown loaders. 39 templates had bare filenames. (Being fixed: T2+T3; 18 templates moved to drafts.)
4. **The catalog promises inputs entries don't accept:** `z-image/i2i`, `ltx-2.3/t2v` and `/flf` require `image_ref` but the entries refuse it; `scail-2/v2v` needs a `--video-ref` flag that doesn't exist; `lava-sr` and `deepfilternet3` refuse a prompt. Found by a catalog-wide dry-run check (`briefs/wave3/t14/test_catalog_entries_dry_run.py`).
5. **A fresh install can't generate until someone creates a project.**
6. **The real Agent-and-Runtime CPU journey takes 57 minutes for 26 tests,** so nobody runs it, and CI never has.
7. **Plan 50 is over-built** relative to two cheap corpus checks (Fable: the scrubber, the ratchet and RB-4).
8. **Five `test_warm_session` paid-expiry deletion tests have failed since `b306b2be`** (money safety); cause unknown.
9. **On a warm machine, models are unloaded at every job end** (`engine_custody.py:1054` `/api/free`, `_cold_free`). The machine stays warm but the engine goes cold; 54 s to collect one PNG.
10. **Successful runs don't capture engine logs** (owner rule: logs for every generation).
11. **The `generate` heartbeat says only "running waiting=-".** The stock wait is logged on the host, not shown to the user.
12. **The Agent heartbeat reads `waiting_details`,** which the pinned Runtime doesn't send (that field is on the unpinned Runtime `1269ada`).
13. **The integration lane's dependencies** (Runtime checkout, lifecycle) are not provisioned, so the lane errors at setup unless you know the env vars.
