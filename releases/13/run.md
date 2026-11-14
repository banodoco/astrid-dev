# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (23:00 UTC Sat 14 Nov): read this first

**CUTOFF 13:00 UTC Sun (Hannah)**: freeze with what's proven. Model limit at warning: conserve. **Compose d753a87df.** In proof:
- W3 6a6ab6f4d (verdict ~23:30) and W4 r3 (a test-only fix from cells, warmrel6);
- P4 1ef476993 (a load-flake isolation, W112);
- P3 916a654d8 (W110; Astra APPROVE);
- P6 (Astra blocked it twice; the P6 session is fixing the settlement wrapper);
- h3first2 (proof W117 plus Astra W118; it merges only on Hannah's ship).

**Live now:** P1 same-model timing on W3 6a6ab6f4d (pod 65y7tk8hiheike: t2i ×3, h3 8 and 20 steps, then t2i after h3); a helper analyses Fable's four numbers per job. The real-clip h3 package is ready (e3fe473) for the final repeat. **Testers:** cut at 02:00, CI by 04:00, issues live by 07:00. **Balance** ~$82.7 before this round.

