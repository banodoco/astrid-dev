# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (10:00 UTC Sun 15 Nov): read this first

**A (int/r13-a91c35df) live round done:** 10/18 pass: t2i ×3 (warm 215 s), edit, tts, sfx, music, h3 v2v, h3 video-edit, and the claim 2 t2i. BLOCKERS found: (1) h3 i2v with one image fails, because h3first2 compiles to MiniMaxH3CustomKeyframesMasked, whose dynamic sockets VibeComfy rejects; it's being reverted (cells r13/revert-h3first2 8d88fc7ec, proof ~10:35). (2) That failure poisoned the warm machine (CustodyUnresolved from a 5 s stop of a reused engine); fix r13/machines-prepstop 16dbe5b41. **P6 not effective** (release note). seed_used appears only in `generate --json` (deferred).

**Next:** A′ = a91c35dfd + revert + prepstop → freeze → short live recheck. B′ = A′ + Tier 1 (r13/machines-tier1-bprime) → freeze → short recheck. B's short round (a639ff3f) is running for Tier 1 warm timing. A's CI table (test manager) is ~12:00. Publish on Hannah's go at 13:00, likely slipping to ~14:00–15:00 for A′'s recheck.

**R13.1** (from 11:00): W-A design read (two forms) and W-B dispatch-only plus the truncated-get fix; W-B collection dropped; W-C → plan 54. Advisor: duplication dive done; local < 0.1 s question due ~12:30. Testers: 0 comments. **Balance** $79.10, 1 pod (B round).
