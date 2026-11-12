Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (smell 4; task T14)
About: F-003; Plan 50
Outcome: open

The catalog promises inputs its entries refuse: `z-image/i2i`, `ltx-2.3/t2v` and `/flf` require `image_ref` but refuse it; `scail-2/v2v` needs a `--video-ref` flag that does not exist; `lava-sr` and `deepfilternet3` refuse a prompt. Found by a dry run of every catalog entry (`briefs/wave3/t14/test_catalog_entries_dry_run.py`), which costs no GPU. Two things follow: fix each entry (small tasks), and keep the dry run as a standing corpus check, which is the cheap check the Plan 50 critique asks for.
