# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (05:00 UTC Sun 15 Nov): read this first

**CUTOFF 13:00 UTC.** Testers are LIVE (#651–#653; answering session alive, 0 comments). **Compose c6a631510** (fixture gaps and the darwin audio timeout merged). Waiting on:
- the Tier 1 integrated head (machines, ~06:30: r13/machines-tier1 8ee344b2d plus W129/W-C3/W-B3; W-C goes to plan 54 if W-C3 isn't clean by 08:00), then the ~09:00 live re-measure;
- V1 (56404c33/e188765f9) and A3 (65f026d79) proofs; L7 (Astra W134);
- the ruff fix acef27e45 (W140 verifying; mypy green per W139);
- **BLOCKER:** activation-recovery [False] finds 3 output rows vs 1 (W141 bisects; possible custody); machine-cli release bind [True] `assert 0 == 1` (W142).

**Balance** $81.32, 0 pods.
