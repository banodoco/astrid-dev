# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (08:00 UTC Sun 15 Nov): read this first

**Schedule:** 08:30 the test manager's one-liners → 08:45 candidate plus immediate freeze → ~08:50 s2i/roundfinal.sh <sha> (~3 h, ~$4) → binding CI table ~12:00–12:15 → publish on Hannah's go at 13:00. **Compose 079f66883.**

Candidate: Tier 1 **r13/machines-tier1-nowb e12127da7** (W-B out entirely; the W142 release fix is inside), or bd03384ae with W-A off if W152 isn't clean. Proofs are delta reruns on e12127da7 after the test manager's 06:40 restart. A3 resumes; V1 is likely out (−1 s).

Testers live, 0 comments. **Balance** $81.23, 0 pods, 8.2 GB free. (My container also restarted at ~07:58; state is on disk.)
