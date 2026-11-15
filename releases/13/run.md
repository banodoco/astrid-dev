# Release 13 — run board

The live state of the Release 13 run: streams, owners and sessions, the timeline, and status. It's updated at every check-in. The [brief](../13.md) holds intent and approach; [decisions.md](decisions.md) holds dated rulings (append-only); [tests.md](tests.md) holds the test gate.

## Now (16:00 UTC Sun 15 Nov): read this first

**Hannah's GO is given** (0.0.13, full, REQUIRED, compact card). **Publish tuple:** Agent 37bd5e06 (PR astrid-agent#347), App adad82f0 (PR astrid-app#268), manifest 4a9e99c8, Runtime 6855dfa8. W207b (App) and W208 (installer move) are MERGE-READY.
**Open gate:**
- the linux-fresh flake gate: re-run 43729912653 AND the adad82f0 linux-fresh row 43729187987 must both pass (W209/W210 found no agent link, and the post-update page state is correct);
- the 13-row run 43728710873;
- the remaining fresh rows;
- PR #347/#268 by name.
**Windows tester (#652):** fresh installs need Git + long paths (pre-existing since R12). The update path is safe: identical path lengths, and a failure happens before the stop. Release-note item; fixes go to the first update.
**Next:** publish (Agent → Runtime fast-forward → App → served-manifest check). After that: an R13.1 milestone with issues from deferred.md (Hannah to confirm), model lookup, R14 docs. Balance $77.48, 0 pods.
