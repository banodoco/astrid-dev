# Gaps — outcomes Astrid has not yet proven

**[Vision](vision.md) → Gaps → [Projects](../projects/index.md) → Evidence.** A gap describes something creators still cannot reliably do, independently of any particular proposed implementation. Its own document defines the desired result, current evidence and a meaningful closure test. Completing a project does **not** automatically close a gap.

## Current gaps

| Area | Missing outcomes |
| --- | --- |
| **Artistic ambition** | [AA-001 — Sustained ambitious creative work](gaps/AA-001-sustained-creative-work.md) |
| **Liquid software** | [LS-001 — Portable creative components](gaps/LS-001-portable-components.md) · [LS-002 — Agent-reconfigurable workspace](gaps/LS-002-agent-workspace-control.md) · [LS-003 — Composable frontend/backend extensions](gaps/LS-003-full-stack-contributions.md) |
| **Compounding intelligence** | [CI-001 — Reliable agent learning](gaps/CI-001-agent-learning-loop.md) · [CI-002 — Federated Hiveminds](gaps/CI-002-federated-knowledge.md) |
| **Shared creative endeavor** | [CA-001 — Creative challenge culture](gaps/CA-001-creative-challenge-culture.md) · [CA-002 — Contributor ownership model](gaps/CA-002-contributor-ownership.md) |
| **Cross-cutting product experience** | [F-001 — Platform reliability](gaps/F-001-platform-reliability.md) · [F-002 — Safe user control and recovery](gaps/F-002-safe-user-control.md) · [F-003 — Dependable creative execution](gaps/F-003-creative-execution.md) · [F-004 — Pack lifecycle](gaps/F-004-pack-lifecycle.md) · [F-005 — Cloud execution for local projects](gaps/F-005-local-files-cloud-assist.md) · [F-006 — Fully hosted workspaces](gaps/F-006-fully-hosted-workspace.md) · [F-007 — First-class sandbox](gaps/F-007-first-class-sandbox.md) |

Each record lives once in `gaps/<ID>-<slug>.md`. The stable ID is identity, not exclusive conceptual ownership. Every gap has one **primary** [pillar](vision.md#four-pillars) *or* [creator principle](principles.md), with only justified supporting connections. Plan files own their forward gap links; gap files do not repeat project status, owner or reverse plan lists.

## When to add or change a gap

Before creating a new gap, check the list above and the [project catalog](../projects/index.md). Prefer refining an existing gap or proposing a project under it. Add a gap only when **the missing outcome would still matter if today's proposed project disappeared** and it has distinct closure evidence. Don't create a gap for a technology choice, a task or an incomplete milestone.

A gap record keeps the standard headings: **Desired state**, **Current state**, **Gap**, **Closure evidence**, and **Sources and reassessment**, plus `Applies to` and `Assessment` metadata. Source revisions and dates are *observations*, not automatic proof that external code still behaves that way.

If a PR creates, retires, renames or materially redefines a gap (title, relationships, desired state, gap or closure evidence), include one short `## Gap boundary assessment — ID` section in the PR description. The existing CI gate checks that it has:

```md
## Gap boundary assessment — F-005

Decision: Refine — <why>
Outcome: <creator-facing missing result>
Existing alternatives: <nearby gaps/projects and why they do not cover this>
Why this level: <why independent of implementation>
Independent closure: <real acceptance and negative evidence>
Primary connection: principle:local-first-cloud-capable — <reason>
Supporting connections: principle:in-the-creators-control — <reason>
Evidence: <source URL or exact SHA>
```

Use `Supporting connections: None — <reason>` when appropriate. The [gap boundary validator](../../scripts/check_gap_boundaries.py) checks structural consistency, **not whether the judgment is correct**. Reviewers decide if the gap duplicates another or has meaningful independent proof. Updating only **Current state**, **Assessment**, or **Sources and reassessment** does not need another boundary review.

Assessments are **Open**, **Partially evidenced**, **Closed**, or **Needs recheck**, supported by current evidence. A [completion PR](../../.github/PULL_REQUEST_TEMPLATE/project-completion.md) assesses the linked gaps without automatically changing their status. Small evidence updates follow the normal [contributor/writing workflow](../../docs/contribution-workflow.md).
