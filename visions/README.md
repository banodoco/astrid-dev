# Visions

Begin with **[Astrid's vision](vision.md): Make Extraordinary Art Possible, Together.**

**Vision (including four principles) → Gaps → Plans → Evidence → reassessment.** The vision describes the destination. Gaps document where the observed reality still falls short. Plans are bounded interventions; their evidence is used to update the gaps, not assumed to prove them closed.

| Principle | Current gap assessments |
| --- | --- |
| [Built for Artistic Ambition](principles/artistic-ambition/principle.md) | [AA-001 — Sustained artistic work](principles/artistic-ambition/gaps/AA-001-sustained-creative-work.md) |
| [Agent-Powered Liquid Software](principles/liquid-software/principle.md) | [LS-001 — Portable components](principles/liquid-software/gaps/LS-001-portable-components.md) · [LS-002 — Agent workspace control](principles/liquid-software/gaps/LS-002-agent-workspace-control.md) · [LS-003 — Full-stack contributions](principles/liquid-software/gaps/LS-003-full-stack-contributions.md) |
| [Collective Intelligence That Compounds](principles/collective-intelligence/principle.md) | [CI-001 — Agent learning loop](principles/collective-intelligence/gaps/CI-001-agent-learning-loop.md) · [CI-002 — Federated knowledge](principles/collective-intelligence/gaps/CI-002-federated-knowledge.md) |
| [Collective Ambition, Shared Ownership](principles/collective-ambition/principle.md) | [CA-001 — Artistic challenge culture](principles/collective-ambition/gaps/CA-001-creative-challenge-culture.md) · [CA-002 — Contributor ownership](principles/collective-ambition/gaps/CA-002-contributor-ownership.md) |

## Shared foundations — not a fifth principle

Some missing outcomes underpin **all four** principles rather than fitting naturally under one:

- [F-001 — Reliability across supported environments](foundations/gaps/F-001-platform-reliability.md)
- [F-002 — Trustworthy user control and operation](foundations/gaps/F-002-safe-user-control.md)
- [F-003 — Dependable end-to-end creative execution](foundations/gaps/F-003-creative-execution.md)
- [F-004 — Dependable pack and extension lifecycle](foundations/gaps/F-004-pack-lifecycle.md)

Read [what a foundation gap means](foundations/README.md) and the [2026-11-06 provisional assessment of every current plan](references/plan-gap-assessment-2026-11-06.md). This dated assessment is **not a second maintained plan registry**; adopt mappings in the owning `plan.md` files only after review.

These are **initial assessed gaps**, not an exhaustive taxonomy or an approved work queue. An unplanned gap is legitimate. A plan can serve several gaps, while foundational enablers may not directly close any.

## How the system stays coherent

- **[Vision](vision.md):** one concise north star and four stable principles.
- **Gap documents:** live, source-grounded *desired → current → difference → closure evidence* assessments, one per independently provable outcome. See the [gap contract and maintenance process](gaps.md).
- **[Plans](../plans/):** each owns its implementation scope and records a **Vision gaps** link to its primary gap(s), whether principle-specific or cross-cutting, or explicitly identifies itself as a foundational **enabler**. **The plan is the sole owner of this relationship**; do not manually copy lists of plan IDs into gap files.
- **Evidence:** attached to the plan's existing tasks/inputs/evidence or a source-revision-pinned artifact. An agent can propose a gap update after a plan completes; a reviewer determines whether the result closes, partly closes or does not change the gap.
- **References:** detailed evidence/design notes only when useful; e.g. [Liquid Software components](principles/liquid-software/references/components.md), [agent learning loop](principles/collective-intelligence/references/agent-learning-loop.md) and the [Hivemind protocol proposal](principles/collective-intelligence/references/hivemind-protocol-proposal.md).

**Not yet automated:** no vision CI check, gap updater or scheduled audit is implemented by this documentation. Future deterministic checks can validate IDs/links/fields and plan declarations; agent review can assess evidence and propose PRs, not silently rewrite strategy. The [project queue](../README.md) remains the only source of plan status, ownership and priority. [Repository rules](../AGENTS.md) still govern authorization.
