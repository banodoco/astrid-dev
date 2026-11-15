# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (09:00 UTC Sun 15 Nov): read this first

**Candidate A frozen 08:20:** int/r13-a91c35df = a91c35dfd (compose including the W142 release fix; no Tier 1). CI 43693935046 and Lanes 43693934998 are running; the test manager builds the binding table (~11:30–12:00). **Final live round on A is running** (s2i/roundfinal.log; ~3 h; ends ~11:15–11:30). So far, 5/5 pass: claim 145 s; t2i-7 cold 12 m 55 s; warm t2i 3 m 35 s / 3 m 33 s; edit 3 m 42 s; tts 3 m 48 s. Seed check: the PNG carries noise_seed equal to the request; `tasks show` has no seed_used field.

**Candidate B** = A + Tier 1 (r13/machines-tier1-nowb-waoff abef725c1: W-A off, W-B out). W160 APPROVE; it waits on lane 2's quiet-box reruns (~09:15–09:45). If it's MERGE-READY, it's frozen separately with a short live re-measure after A's round.

Out: A3, V1, L7, W-B, W-A (plan 54). Testers live, 0 comments. Publish on Hannah's go at 13:00.
