# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (12:00 UTC Sun 15 Nov): read this first

**Candidate A′ int/r13-f709407c** (A + h3first2 revert + prepstop): live recheck 5/5 validated (i2v MD5-identical to the reference route; no poisoning). A's binding table is CLEAN. G4 APPROVE.
**A″ train** (machines, ~12:45–13:00, each with fail-first tests; the test manager proves each):
- r13/machines-logfetch: a log-only fetch failure must not fail a completed generation (G3 W172 #3);
- r13/machines-redact: token-only URL userinfo, plus redaction at every print/return boundary (generate failure, tasks logs, MCP, remote install stdout) (G3 #2 and W176);
- r13/machines-winclaim: Windows RunPod claim (os.fchmod, directory os.open) (W171; W179 verifying).

Then freeze A″ → re-pin the App (now cf2f9535a on A′, CI running) → journey matrix → Hannah's go, ~14:00–14:30.
**Open:** the Runtime 6855dfa8 durable ref; Hannah's version/kind/required-update decision; tester links (0 comments).
**R14:** plan #662 (plans/55-local-speed; D1–D8 open); releases/14 docs PR in progress. **Balance** $77.5719805663, 0 pods.
