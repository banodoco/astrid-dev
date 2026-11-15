# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (19:00 UTC Sun 15 Nov): read this first

**R13 includes the Windows fixes (Hannah).** The recut tuple:
- **Agent** 8625a463 (PR #347; int/r13-8625a463) = 401dbd78 + advisor r14/windows-install 61661569 + Ruff lock-in;
- **App** 0d9d620d (PR #268): compact required card + re-pin;
- manifest da5976b8; Runtime 6855dfa8 (the DB-mode fix goes to R14).
**Done on the recut:** W217, the network_policy review (POSIX identical with and without the policy; no bypass), PASS. Local: cycles, ruff and the focused tests are green.
**Pending:**
- the 13-row journey 43747941639 plus linux-fresh ×2 (queued behind runner backlog);
- CI/Lanes on int/r13-8625a463;
- W218, App PR by name;
- **the Windows proof:** the advisor's guard real-generation on 61661569, or #651's clean run.
**Runner queue:** superseded 8e8e60b1 runs (CI 43747531839, Lanes 43747531811, Chat 43747531790) hold slots. The test manager's cancel was denied, so I asked Hannah whether to cancel them.
**Linux-fresh notice question:** verdict A, so it's not blocking (Hannah's rule); the fix is a follow-up. Balance $77.40, 0 pods.
