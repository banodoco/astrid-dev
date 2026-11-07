# 25 — Cloud-assisted Astrid V1 (local files)

**Start here:** read [AGENTS.md](../../AGENTS.md), follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md), and review [tasks](tasks.md) and [inputs](inputs.md). Priority, owner, estimate and status live **only** in [plans/index.md](../index.md).

**Vision gaps:** [F-005 — Local projects cannot yet use coherent cloud execution](../../visions/gaps/F-005-local-files-cloud-assist.md) (primary); [F-003 — dependable creative execution](../../visions/gaps/F-003-creative-execution.md) and [F-002 — safe user control](../../visions/gaps/F-002-safe-user-control.md) (supporting). Do not claim those cross-cutting gaps closed on V1 alone.

## Goal and boundaries

Ship a **cloud-assisted local-first Astrid**: user's project database, timeline and durable files remain on their machine; optional cloud services carry out approved agent work, model generation and video rendering, with outputs returned into the same editable local project. This is **not** a fully hosted workspace or a cloud database.

**Included:** a cloud-agent execution route supporting agent-family workflows under existing Astrid Runtime/Agent task authority; selected remote image generation via suitable APIs; a remote video-rendering service for a real timeline/project; explicit provider choice/consent, credentials and spend controls; scoped transfer of required inputs; local result reconciliation, provenance, cancellation and recovery. The first proof can be bounded to one provider/engine per capability with clear unsupported cases.

**Not included:** relocating or syncing the canonical project database to the cloud, persistent cloud asset library, general hosted login/accounts, multi-user tenancy, unlimited provider compatibility, rewriting Astrid orchestration, or replacing FFmpeg/Remotion simply because rendering runs remotely. [Plan 26](../26-fully-hosted-v2/plan.md) owns hosted persistence and user accounts.

## Existing work to build upon

- [Reigh Worker Orchestrator](https://github.com/banodoco/reigh-worker-orchestrator) documents RunPod GPU pools, API orchestration for fal and Wavespeed, worker lifecycle and deployment tooling. It is a **source donor to evaluate, not an established production dependency**: [Astrid's rename/satellite dispositions](https://github.com/banodoco/astrid-agent/blob/main/tools/astrid-rename/satellites.md) mark it deprecated, and current deployment is unverified.
- [Astrid Agent cloud/local execution routes](https://github.com/banodoco/astrid-agent/blob/main/docs/reference/where-things-run.md), existing agent orchestration and current Runtime task/artifact custody must be checked at their actual revisions before proposing new agents or provider adapters.
- [Plan 12](../12-multiple-inference-routes/plan.md) and [Plan 20](../20-zero-to-first-image/plan.md) own other inference/onboarding foundations; don't duplicate their work. Reuse existing App timeline/editor, generation paths and media renderer as far as possible.

## Proposed sequence (not authorized)

1. **Audit first.** Record immutable source revisions, existing Reigh worker orchestrator capabilities, deprecation/current deployment status, Astrid Agent/Runtime cloud execution, render options and capability gaps. Decide what to retain/retire. Never create a parallel task authority.
2. **Provider decision.** Compare a small set of cloud agent-runtime APIs, image-generation APIs and remote rendering strategies on security, task lifecycle, price, logs, cancellation, latency and implementation effort. Choose intentionally; no provider is implied by this plan.
3. **Local-data custody contract.** Define input staging, content hashes, temporary remote retention, consent and spend, secure secrets, progress/cancel/retry and local project/artifact identity. Ensure agents have least authority and may not silently upload project files.
4. **Agent family in cloud.** Run one approved family/multi-step agent workflow remotely using existing task semantics; ensure logs, tool permissions, cancellation and output return are verifiable.
5. **Generation and render.** Demonstrate one remote image-generation route and one remote video-render route from a real Astrid project. Remote render may use existing FFmpeg/Remotion components behind a service; choosing a new engine requires separate evidence.
6. **Integrate and qualify.** Return and reconcile artifacts locally, preserve edits and database authority; test failure, cancellation, budget limits and interrupted connections end to end.

## Project interface and handoff

**Consumes:** current Runtime project/task/artifact custody, Agent execution contracts, existing generation/rendering paths and verified donor facts recorded in [inputs.md](inputs.md). These are starting points to inspect, not assumed-live cloud services.

**Produces:** a qualified, versioned contract for approved remote agent/generation/render jobs, temporary input staging, progress/cancel/retry, spend/permissions and **reconciliation back into the authoritative local project**. Record the integrated candidate and exact evidence in the completion PR. [Hosted V2](../26-fully-hosted-v2/plan.md) may reuse those proven contracts, but must independently qualify cloud-owned persistent data and account boundaries.

## Completion

With local project files and database clearly retained, a creator can instruct their agent to complete approved cloud work, generate an image, render a video and recover editable results in the local workspace. Evidence names exact versions/providers, transfer/retention behavior, spend/cancel controls and non-success tests. This is not proof of fully hosted Astrid.

**Authorization:** queued proposal only. Owner, provider and cost approvals, source identity, credentials, tests and integration destination require a later scoped decision. No deployment or spending authorized here.
