# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (00:00 UTC Sun 15 Nov): read this first

**CUTOFF 13:00 UTC Sun (Hannah: option A).** Model limit at warning: conserve. **Compose 22ffe8483** (phase 4, W3, P4 and P6 merged tonight). **Open:**
- Tier 1 warm-latency cards on machines (W-A/B/C/D/E/H plus Q2 one-audit, Q5 node receipt, Q6 skip-clean-reset; W-G out); integrated head ~03:30–04:00.
- Cells: L1 once-per-job, L4 hash-once, L7 content-named inputs (by 08:00).
- P3 65d368844 (test manager); W4 r4 f4d124717 (lane 2, ~01:15); h3first2 ee00d80e8 (merges only if Hannah says ship).

**Live:** P1 done (warm t2i prompt 2.9 s vs ~4 min wall; table d6384df). The re-measure is ~09:00 on the integrated head, adding realm_job_rows counts. Cards not proven live by ~10:00 go to plan 54. **Plan 54 "Generation speed": astrid-dev#654** (PR for Hannah; target architecture being added). **Testers:** cut at 02:00 (22ffe8483 + W4 if ready), CI by 04:00, issues live by 07:00. **Balance** $81.55, 0 pods.

