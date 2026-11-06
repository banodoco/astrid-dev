# Astrid vision-page feedback and cloud roadmap — 2026-11-07

**Status:** consolidated proposal and implementation tracker, not authorization to start product engineering. Keep this brief as a map of the user's requested outcomes; canonical copy lives in `visions/vision.md`, `visions/principles.md`, gap files and the [single plan catalog](../../plans/index.md). **Do not duplicate project status here.** Resolve and update this map as decisions are made.

## Vision and editorial decisions

| ID | Requested outcome | Source / owner | State |
|---|---|---|---|
| V-01 | Headline frames Astrid as unlocking the collective artistic ambition of the open-source community | [Vision](../vision.md) | Current draft |
| V-02 | Lead includes **individual artists and the community as a whole** pursuing artistic work beyond what they thought possible | [Vision](../vision.md) | Incorporated in draft |
| V-03 | Four pillars have grounded, first-person descriptions and explicit **1–4** numbering; fourth is **A Shared Creative Endeavor** | [Vision](../vision.md), [App](https://github.com/banodoco/astrid-app) | Rename proposed; numbering implemented |
| V-04 | Four operating principles: local-first/cloud-capable, open by design, creator control, **eliminate needless technical wrangling**; agents handle model selection, setup and infrastructure, people create | [Principles](../principles.md) | Proposed in draft |
| V-05 | Gap titles read as **short statements of missing outcomes/problems** rather than aspirational project names | [Gaps](../gaps.md) | Draft, retained stable IDs |
| V-06 | Creative challenge gap acknowledges Banodoco community and prior Arca Gidan art competitions while stating Astrid-specific creative culture is not yet established | [CA-001](../gaps/CA-001-creative-challenge-culture.md) | Draft, not audited |
| V-07 | Ownership gap says **no implemented contributor-ownership model**; mention founder-reported prior Banodoco arrangement that lapsed and need to design terms for Astrid | [CA-002](../gaps/CA-002-contributor-ownership.md) | Draft; legal details remain unverified |
| V-08 | End with one contribution invitation, workbench mink beside it, and a link to the [agent contribution instructions](../../README.md#want-to-contribute-give-this-to-your-agent) | [App](https://github.com/banodoco/astrid-app), [Vision](../vision.md) | UI draft |
| V-09 | Remove old aphorism and tools-shaped-by-AI scene, second mobile juggling mink, and the generated-data provenance footer | [App](https://github.com/banodoco/astrid-app) | UI draft |

## Mobile, loading, and project presentation

| ID | Requested outcome | State |
|---|---|---|
| UI-01 | Expanded gap details use the **full available width**, not an indented column beside the ID | Planned |
| UI-02 | Mobile gap details start **collapsed**; tapping opens/closes; **show all gaps** reveals newly mounted rows | Already covered by prior App fix; keep regression tests |
| UI-03 | On initial page load show stable **text skeletons**, rather than an empty page that pops into layout | Planned |
| UI-04 | Show about **eight projects plus a final View all tile** in a responsive desktop three-column grid; fewer columns on mobile | Planned; editorial layout choice |
| UI-05 | View all projects opens immediately; rows preloaded in memory, reveal observer registers newly rendered rows, no leaving/reopening page | Planned; preserve button accessibility |
| UI-06 | Keep actual status, priority and links sourced from the [plan catalog](../../plans/index.md); never duplicate project copy in App | Existing contract |

## Cloud roadmap — separate project stages

**V1 — Local files and database, remote execution.** Proposed [Plan 25](../../plans/25-cloud-assist-v1/plan.md) and [F-005](../gaps/F-005-local-files-cloud-assist.md). Astrid remains a local workspace. Approved cloud agent sessions, generation/model APIs, and a remote video-render service handle expensive or technically difficult work. Selected files may be transferred with explicit consent; project files and persistent database remain local, with editable outputs returned and reconciled locally. Explore an agent **family**, cloud runtime provider APIs, rendering pipeline, costs and recovery. **Not** an always-on hosted workspace.

**V2 — Fully hosted workspace.** Proposed [Plan 26](../../plans/26-fully-hosted-v2/plan.md) and [F-006](../gaps/F-006-fully-hosted-workspace.md). Build on verified V1 execution routes. Hosted authentication, persistent project database, durable media storage, running agents, rendering, sharing and backup/recovery live in the cloud, with browser access and no required local installation. Require a migration/export path and explicit ownership, permissions, security and cost controls.

**Existing donor and risk:** [`banodoco/reigh-worker-orchestrator`](https://github.com/banodoco/reigh-worker-orchestrator) already documents RunPod GPU-worker orchestration and fal/Wavespeed API tasks. However [Astrid Agent's satellite-disposition notes](https://github.com/banodoco/astrid-agent/blob/main/tools/astrid-rename/satellites.md) label it **deprecated**, and do not verify current deployment. *Audit and reuse proven capabilities rather than rewriting or assuming this is production-ready.* Also inspect [current execution routes](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md), Astrid Runtime task custody, the existing inference plans, and App/Remotion renderer before selecting APIs or building anything.

## Unresolved decisions and proof required

- Pick the actual cloud-agent runtime/API provider(s), auth model and agent-family scheduling. No provider is selected merely by this plan.
- Decide whether video rendering uses the existing renderer remotely, a service wrapper, or a new renderer. Moving render execution to a remote worker does **not** by itself require replacing FFmpeg/Remotion.
- Specify file upload minimization, transient remote retention, encryption, credentials, provider permissions, spend limits, cancellation, retry, and deterministic local result mapping.
- Determine the V2 backend, tenancy, database, object storage, account model, data residency, migration/export and rollback only after V1 has evidence.
- Ensure both cloud stages have independent closure tests and don't duplicate [F-001](../gaps/F-001-platform-reliability.md) or [F-003](../gaps/F-003-creative-execution.md); these remain cross-cutting.
- Existing Plan 25/26 queue items are **queued drafts** only. They are not authorized product work and must honor the shared run contract.

## How to maintain this tracker

Keep the canonical Markdown and plan catalog authoritative. Mark an item here resolved only when a linked code/document PR and evidence exist; remove outdated draft labels as those PRs merge. This is a feedback record, not another source of project status, copy, or gap closure.
