# <packet-id> — <bounded outcome>

**Source tasks:** `plans/<P-slug>/tasks.md` — <task IDs / bounded slices>
**Estimate:** <human engineering days; ~3 maximum>
**Outcome:** <one sentence>
**Dependencies:** <task / PR / evidence links, or none>
**Proof:** <source task IDs holding actual acceptance and checks>
**PR destination:** <product repo(s), task branch(es) → `release/<N>/plan-<P>`>
**Authority:** <link to accepted Run start and permissions>

One packet starts **one fresh ChatGPT session**. The session opens task PRs and submits proof, **but does not merge or edit `tasks.md`**. The Lead reviews, integrates and reconciles tasks; the Orchestrator tracks the handoff in `releases/<N>/run.md`. No independent project, issue, checklist or run is created.
