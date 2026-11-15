# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (11:00 UTC Sun 15 Nov): read this first

**R13 = A′, frozen 10:39: int/r13-f709407c = f709407cb** (A a91c35dfd + the h3first2 revert 8d88fc7ec + prepstop 16dbe5b41; branch r13/compose-aprime). The revert is MERGE-READY (W164 faithful, 0 regressions); prepstop has Astra APPROVE, with its quiet-box paired proof due ~11:15. A′ CI 43705081374 / Lanes 43705081352 are running. A's CI table is clean (0 regressions in all 8 unit shards; darwin = R12; one LTX catalog timeout rerunning). **A′ live recheck running** (s2i/roundA2.log: h3 i2v, t2i after it, bike i2v, h3 edit, t2i). Publish on Hannah's go after the recheck, ~12:00–12:30.

**Next release = R14, local-first speed** (Hannah 10:45; RunPod speed out of scope). Plan draft astrid-dev#662 (plans/55-local-speed), with seven decisions for Hannah. RunPod R13.1 cards were stopped at pushed branches (W-A life finishing ~13:30, flag off, a local donor). Tier 1 data: B warm t2i 153–156 s vs A 215 s.

**Release notes must say:** P6 not yet effective; first-frame i2v reverted (reference route as in R12); seed_used only in `generate --json`. Testers: 0 comments. **Balance** $78.38, 1 pod (recheck).
