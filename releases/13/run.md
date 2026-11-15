# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (17:05 UTC Sun 15 Nov): read this first

**Hannah's GO is given** (0.0.13, full, REQUIRED, compact card). **Publish tuple:** Agent 37bd5e06 (PR #347 head 401dbd78 = + Ruff baseline lock-in), App adad82f0 (PR #268), manifest 4a9e99c8, Runtime 6855dfa8.
**Green:** 13/13 rows (43728710873); macos-fresh and windows on adad82f0; App PR clean by name (release-guard, three-products); W207b, W208, W211 (unit-8 extras are R12-preexisting); local paired run.
**Held on:**
- (1) **linux-fresh:** 3 fails and 2 passes on the 8-second "Astrid updated: Release N → M" page notice. The post-update state is correct, and no agent or Runtime defect was found (W209, W210, W212, W214). Hannah: wait for the evidence. Capture runs (harness/32-r13-capture): linux ×3 (43738941120 / 43738950381 / 43738959409) plus a macos control (43738967961). Publish if only the notice is missed; fix first if it's a real problem.
- (2) **PR #347 fast checks on 401dbd78:** ruff, mypy and cycles, still to run.
**R13.1:** the Windows fresh-install work is the advisor's (r14/windows-install); machines' TLS 95b8130e8 and CI guard 59497cf9d are handed over; cells' model lookup is running. Balance $77.46, 0 pods.
