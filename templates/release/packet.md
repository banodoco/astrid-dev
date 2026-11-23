# <packet-id> — <bounded outcome>

**Source tasks:** `plans/<P-slug>/tasks.md` — <task IDs>; for an issue packet, issues on the brief's list
**Route:** <N, X or S, the hardest card's route; sets the ChatGPT mode: N High, X Extra High, S Pro ([run contract](../../skills/shared/run-contract.md#chatgpt-session-modes))>
**Estimate:** <human engineering days; ~3 maximum>
**Outcome:** <one sentence>
**Dependencies:** <task / PR / evidence links, or none>
**Proof:** <source task IDs holding actual acceptance and checks>
**PR destination:** <repo(s): `p<P>/<task id>` → `release/<N>/plan-<P>`, or `release/<N>/<topic>` → `release/<N>/main`>
**Authority:** <link to accepted Run start and permissions>

One packet starts **one fresh ChatGPT session**. The session opens task PRs and submits proof, **but does not merge or edit `tasks.md`**. The Lead reviews, integrates and reconciles tasks; the Orchestrator reports the handoff in its hourly STATUS.
