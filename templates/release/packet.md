# <packet-id> — <bounded outcome>

**Source tasks:** `plans/<P-slug>/tasks.md` — <task IDs>; for an issue packet, issues on the brief's list
**Route:** <N, X or S, the hardest card's route; sets the ChatGPT mode: N High, X Extra High, S Pro ([run contract](../../agent/shared/run-contract.md#chatgpt-session-modes))>
**Estimate:** <human engineering days; ~3 maximum>
**Repro:** <issue packets only: failing test id or exact command>
**Outcome:** <one sentence>
**Dependencies:** <task / PR / evidence links, or none; all merged before Ready>
**May touch:** <files and functions>
**Must not touch:** <files and functions>
**Proof:** <source task IDs holding actual acceptance and checks>
**PR destination:** <repo(s): `p<P>/<task id>` → `release/<N>/plan-<P>`, or `release/<N>/<topic>` → `release/<N>/main`>
**Authority:** <link to accepted Run start and permissions>

One packet starts **one fresh ChatGPT session**. The session opens task PRs and ends with `READY-PROOF`, **never merging or editing `tasks.md`**. The orchestrator runs the proof, has the PR reviewed where the brief requires, and merges it into the plan branch.
