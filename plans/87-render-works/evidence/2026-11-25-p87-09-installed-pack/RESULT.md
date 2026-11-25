# P87-09 installed proof (orchestrator, 2026-11-25)
Pinned astrid_motion 2379ab54 (digest 75234c10…) at <home>/Astrid/packs/astrid_motion; App dca367cb; Runtime 686ca695.
BASE Agent b2155fdc: film-shaped 23-clip render FAIL 85 s, webpack "Can't resolve '../../../../rendering/shared/element_contracts'" (render-film-base2155.log). (Also b934555c: film-shaped FAIL, 1 s image-only FAIL task 3f2d5c1a…)
HEAD Agent tree = PR #661 6158908d (my local merge 8d58a759, same tree 8730eb45):
- film-shaped 23-clip: ok, 128.6 s, task 6fe62071…, mp4 h264 1280x720 18 s 540 frames + aac (render-film-head661.log); timeline admits am-type from the pinned pack.
- 1 s image-only: ok, 48.9 s, task 85b8c28f… (render-image-head661.log).
- am-sprite clip: NOT built (SDK refuses a sprite asset inside a shot: content_sha256 12-char registry); film-shaped project exercises am-type.

Merged: astrid-agent #661, merge commit dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5 (tree 8730eb45, the proved tree). Proof comment: astrid-dev #1776 comment 7168141388. Packet: releases/15/packets/R15-P87-09.md.
Focused tests (nine files, base b2155fdc vs head 6158908d): 125 passed, 1 failed, 0 errors on both; the one failure test_render_authoritative_aliases.py::test_webpack_legacy_alias_is_scoped_to_host_issuer is identical on both. New test_installed_pack_element_contracts.py: 5 passed.
Not built: the am-sprite clip render (SDK refuses a sprite asset inside a shot: content_sha256 registry check; not established whether defect or fixture path).
Receipts in this directory: receipt-film23-sdk-run.md (film-shaped 23-clip SDK run, local overlay run, projected pack 414a6fd1, NOT the manifest pin) and receipt-rn10.md (RN-10 616-clip runs; built-in elements only).
