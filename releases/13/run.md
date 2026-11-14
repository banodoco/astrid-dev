# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (20:00 UTC Sat 14 Nov): read this first

**Compose 5193a2331** (httpj r5 and batch A merged this hour). **Open, in merge order:** W3 r5 d58115106 → 5b 2463b4e39 (lane 2), hostwedge5 (cells; r4 held for the 0755 data-root refusal), phase 4 cf49d415 plus R4.N, W4 r3 4e3a20af1 (lane 2), h3 docs, P6 (being built; it waits for W3 5b), P4/P3 (machines). **Live:** h3 masking round on s16 (a921b7dce), pod ephmvk5zhes2uk: T1 passed in 16m10s, T2 in 7m52s, T3–T5b running; a helper validates. P1 timing runs after W3 merges. **Testers:** issues astrid-dev #651–#653 are marked "Not ready yet"; the dry Windows proof is running at a921b7dce (astrid-agent runs 43633299413/43633299370). The tester head is cut at 02:00 UTC, CI should be green by 04:00, and the issues go live by 07:00 Sunday. **Balance** $83.67 with 1 pod. No fixed freeze; the review gate is in force.

