Date: 2026-11-17
Kind: fix
Source: two fresh-context dry runs, after the Orchestrator's real startup on #796, of the Orchestrator and of the first packet session, 17 November 2026
Resolved by: —

Both dry runs read only what they would be given.

**What they found:**
- The early STATUS the Lead asked for was in its DECISION, not in the workstream's start message, so a literal follower would skip it.
- "The packet's SHA" was undefined. A plan branch that had moved on read as a reason to stop.
- Nothing said which branch a packet's files are read on.
- A document's proof was asked for as "focused tests".
- The Orchestrator was told both to stop earlier sessions and that the owner was stopping them.

**The fixes:**
- **Dispatch workstream.** The first packet goes out alone, and its early STATUS proves a packet session can push, open a pull request and comment. Each later packet's early STATUS proves its own repository. The start message asks for that early STATUS. The Orchestrator stops the earlier sessions it can reach and names for the owner the ones it cannot.
- **Packet workstream.**
  - Files are read on `main` unless the packet names a branch.
  - A new branch is cut from the plan branch's current head.
  - BLOCKED applies only when a draft's head differs from the board's table.
  - A document is proved by its card.
- **R14-P55-01** says why it has no dependency to wait for and where to read each file. It quotes the Windows cells separately and has the design assume the forced-write budget instead of measuring it.

Skills are 48 words longer.

Follows: 2026-11-17-dispatch-ownership-and-clocks
