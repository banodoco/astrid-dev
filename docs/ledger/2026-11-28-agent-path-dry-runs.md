Date: 2026-11-28
Kind: fix
Source: H3 lane launch preparation, planning session (owner's request): cold-read dry runs of the lane orchestrator (twice), the Codex-app manager, a ChatGPT chat and a Claude worker, each a Haiku given only what that role receives
Resolved by: —

**What they found:** about 25 gaps a real launch would have hit. 66-U1 waited on a baseline nobody owned; the manager launch and chat start message were never written; who writes packets, who runs proof and who merges into the release branch were each stated two ways; the chat could not run the proof it was told to run; skills install failed without an existing destination; workers were told both to set an hourly task and to post only milestones. Each level found gaps the level above could not see.

**The fix:** agent tests. Each path a session can be started on has a declared case (`agent-tests/cases/`) naming the documents it covers, its brief, its host and its exact starting message, with Expect and Must not lines drawn from a sourced golden path. A cheap actor plays it, a judge checks the report, and the owner reads what the session would do. Changing a covered document re-runs its cases ([improve](../../agent/shared/workstreams/improve.md)); the `agent-tests` check validates structure only. Principle 11 in the [design principles](../contribution-design-principles.md).

Follows: 2026-11-17-fresh-context-dry-runs
