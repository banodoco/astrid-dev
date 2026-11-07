# Plan 25 — tasks (draft planning cards)

[Plan](plan.md) · [Inputs and source identities](inputs.md) · [Status, priority and owner](../index.md)

**Scope boundary:** these are dependency-aware proposed tasks, not dispatched work. No implementation, cloud spend, provider commitment or access to user files is authorized without a scoped owner decision and the [shared run contract](../../../skills/astrid-dev-shared/run-contract.md). Routes (`N`, `X`, `S`) and estimates remain undecided until source audits establish actual complexity; do not guess or treat a draft as ready for execution.

## Task index

| ID / outcome | Route | Depends on | Progress | Focused completion evidence |
|---|---|---|---|---|
| C25-01 — Audit existing cloud/orchestrator paths | TBD | None | Draft | Exact revision-pinned map of Reigh Worker Orchestrator, Astrid Agent/Runtime, generation and render; verified retain/replace/deprecation decisions |
| C25-02 — Choose bounded providers and render strategy | TBD | C25-01 | Draft | Comparison of agent-hosting APIs, model APIs and remote rendering with explicit permissions, cost, cancellation, data custody and owner approval |
| C25-03 — Specify and implement local-first cloud job/artifact contract | TBD | C25-01, C25-02 | Draft | Tests of explicit file-transfer consent, local project authority, secure credentials, artifact hashes, retries, cancellation, recovery and budget limits |
| C25-04 — Demonstrate a remote family of agents | TBD | C25-03 | Draft | One real approved multi-step/family workflow using existing Astrid task authority, with traceable permissions, logs, stop/retry and returned results |
| C25-05 — Demonstrate remote generation and video render | TBD | C25-03 | Draft | Real image-generation and timeline video-render jobs; correct editable local imports, project identity, media hashes, retention and cost receipts |
| C25-06 — Qualify user journey and reassess F-005 | TBD | C25-04, C25-05 | Draft | End-to-end supported matrix and negative tests for interruption, disconnection, failure, spend limits and user control; an evidence-backed F-005 assessment |

## Implementation boundaries to resolve before dispatch

- **Reuse before replacement:** the existing [Reigh Worker Orchestrator](https://github.com/banodoco/reigh-worker-orchestrator) is a donor to audit, not assumed deployable; Astrid Agent's satellite notes mark it deprecated. Review exact commits and current Runtime custody before choosing any worker or agent-family architecture.
- **Keep the local authority:** the canonical project database, timeline and durable assets stay on the user's machine. Cloud receives only explicitly approved inputs; completed outputs must return to the same editable local project. No hosted persistence or user-account migration belongs in V1.
- **Rendering decision:** provide a remote video-render service that removes local rendering requirements for this route. Whether it wraps current FFmpeg/Remotion or uses another engine is an evidence-based choice, not a precondition to replace an otherwise working engine.
- **Dispatch prerequisites:** each task must gain a route and bounded detailed card under the [project template](../../../templates/project/tasks.md), source SHAs, an accountable owner, provider/spend approvals, relevant test selectors and a clear rollback/stop boundary. C25-04 and C25-05 may proceed independently only after C25-03 is qualified.

Task progress belongs in this file after authorization; **plan status, owner, priority and remaining estimate** stay only in the [catalog](../index.md).
