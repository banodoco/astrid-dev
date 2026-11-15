# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (07:00 UTC Sun 15 Nov): read this first

**Schedule:** 08:45 candidate decision plus immediate freeze → ~08:50 s2i/roundfinal.sh <sha> (ready; ~3 h, ~$4; ends ~11:40–12:10) → binding CI table ~12:00–12:15 → publish on Hannah's go at 13:00. **Compose 079f66883.** Rehearsal int/r13-f5637687: CI clean (0 regressions; all fast checks pass), Lanes due ~07:45–08:00.

Candidate inputs:
- Tier 1 r13/machines-tier1 8eb4b4274 (W142 release fix and W145 inside; tier1_cards P3,P4,W-A..W-F,W-H,Q2). It needs the Astra reads of W144/W145/W149 and the W146/W147 proofs. Fallbacks: waoff 95c3dd184 (W-A off) if W-A round 5 isn't clean by 07:30; nowb 61970e7b1, to be rebuilt.
- Standalone release fix r13/machines-rel (W142; money blocker), for the case where tier1 doesn't go in.
- V1/A3 proofs (W135/W136).

Testers live, 0 comments. Disk 8.2 GB free. **Balance** $81.26, 0 pods.
