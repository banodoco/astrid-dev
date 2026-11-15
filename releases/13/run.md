# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (06:00 UTC Sun 15 Nov): read this first

**Schedule (05:55):** 08:45 candidate decision plus immediate freeze → ~09:00 paid final live repeat on that head → binding CI table ~12:00–12:15 → publish on Hannah's go at 13:00. **Compose 079f66883** (fixture gaps, darwin timeout, ruff fix, activation-logs merged; mypy green; rehearsal CI int/r13-f5637687 running). Open:
- **BLOCKER (money):** W142, a stale-id `machines release` returning ok while the pod is live. Fix r13/machines-rel 1da0d1528 awaits the Astra read (07:30); fallback: revert 1c08bd3c4's release change.
- Tier 1 (r13/machines-tier1 d99612c1d): W146/W147 proofs running; W-C approved but its saving is inactive on the default path (no termination authority); W-A/W-B re-reads running; a host_checkpoint_evidence regression from W-B3 is being fixed (08:00 line).
- V1/A3 proofs (W135/W136). L7 out.

Testers live, 0 comments. **Balance** $81.29, 0 pods.
