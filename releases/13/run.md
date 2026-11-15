# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (20:00 UTC Sun 15 Nov): read this first

**R13 includes the Windows fixes (Hannah).** The last full tuple: agent 36f04678 (PR #347), App f1967a1e (PR #268), manifest 11ad26ee, Runtime 6855dfa8.
- 13/13 rows GREEN (43753381312).
- Windows generation proven on a clean install (advisor guard 43750797446).
- W217 PASS.
- BUT the hosted mypy gate is RED (Windows attr-defined), so 36f04678 can't publish.
**Waiting on the advisor's single batch:** the mypy fixes, 0cdfaec3 (.exe program names), the node-pack install commands, and the short Windows VibeComfy runtime root (Hannah asked; possibly a VibeComfy pin). Then: a mypy/cycles preview, recut, the 13 rows + NEW gate row `direct-windows-r12-update` (being built, harness/33-win-r12-update), CI, a W217 delta, and the App by name.
**Open:**
- the macos-fresh uninstall intermittent (1/5 since the Windows merge, 3/3 before); W224 is testing the new stderr print hypothesis;
- linux-fresh capture ×2 on 36f04678.
Standing OK from Hannah to cancel superseded runs. Codex is limited until 19 Nov (Haiku/Sonnet subagents). Balance $77.37, 0 pods.
