# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (18:00 UTC Sun 15 Nov): read this first

**R13 publish is ON HOLD (Hannah, 22:45):** the Windows fresh-install fixes go INTO R13. The advisor ("the lead") owns them on astrid-agent r14/windows-install (base 37bd5e06) plus a Runtime DB-mode branch, and sends SHAs per part. The orchestrator composes them onto r13/compose-aprime 401dbd78; the test manager proves each part; then recut, re-pin the App (and the Runtime if it changed), and run the full journey.
**Current base (proven):** agent 37bd5e06 / 401dbd78 (Ruff lock-in); App adad82f0 (compact required card); manifest 4a9e99c8; Runtime 6855dfa8.
- 13/13 rows green;
- App PR clean by name;
- fast checks green;
- unit shards: 0 regressions vs R12.
**Linux-fresh notice question:** still open. On the final tuple, 4 passed and 1 failed at the click step; capture rows continue. Hannah's rule: publish only if only the notice is missed.
**Codex is rate-limited until 19 Nov:** worker reads run as Claude Haiku/Sonnet subagents (Hannah). Cells' ml131 (model lookup) proofs are running via Haiku. Balance $77.38, 0 pods.
