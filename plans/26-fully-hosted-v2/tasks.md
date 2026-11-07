# Plan 26 — tasks (draft planning cards)

[Plan](plan.md) · [Inputs and unresolved choices](inputs.md) · [Status, priority and owner](../index.md)

**Scope boundary:** this is a distinct, **fully hosted** project, not authorization to relocate V1 users or launch cloud services. The V1 execution/artifact contract must be demonstrated and accepted before implementation here. No database, object store or identity provider has been selected. Apply the [shared run contract](../../skills/astrid-dev-shared/run-contract.md); route (`N`, `X`, `S`), estimate and accountable task owners remain TBD until scoped.

## Task index

| ID / outcome | Route | Depends on | Progress | Focused completion evidence |
|---|---|---|---|---|
| C26-01 — Map V1 contracts and current local project/media custody | TBD | Accepted Plan 25 deliverables | Draft | Version-pinned source map of local database, media paths, schema, access rules and verified V1 execution/artifact boundaries |
| C26-02 — Choose hosted architecture and operating policy | TBD | C26-01 | Draft | Reviewed database, object store, identity, tenancy, residency, encryption, cost/quota and migration choices; explicit unsupported cases and owner approval |
| C26-03 — Implement hosted project state and durable file custody | TBD | C26-02 | Draft | Authenticated persistence, correct project/media references across sessions, isolation, versioning and negative cross-account tests |
| C26-04 — Connect hosted agents, generation and rendering | TBD | C26-03; accepted V1 execution contracts | Draft | Remote work uses cloud-owned artifacts without parallel task authority; job/artifact identity, consent, cancellation, recovery and cost proof |
| C26-05 — Qualify browser-only creative journey | TBD | C26-03, C26-04 | Draft | New user signs in, creates and edits, generates, renders, reopens on another supported device and recovers from interrupted sessions |
| C26-06 — Qualify operations, privacy and migration | TBD | C26-03, C26-05 | Draft | Repeatable backup/restore, export to local custody, revocation, deletion, limits, tenant isolation, incident recovery and evidence-backed F-006 assessment |

## Decisions and boundaries before dispatch

- Cloud **database and durable files** must be authoritative for the hosted project, not a browser UI pointed at a user's local machine. Hosting agent execution alone is V1 and does not satisfy V2.
- Build on the proven V1 agent, provider and rendering contracts; avoid a separate agent-family orchestration stack. Preserve local-first use for users who choose it.
- Make data export/migration, tenant isolation, access control, provider costs and recovery demonstrable. Do not automatically upload existing local/private projects or imply multi-user collaboration before its permission model is approved.
- Before execution, turn each proposed row into a bounded task card with `N/X/S` routing, dependency revisions, an owner, explicit checks and stop/rollback criteria. Decide provider credentials, spend and security/retention policy in a separate authorized scope.

Task progress belongs in this file after authorization; **plan status, owner, priority and remaining estimate** stay only in the [catalog](../index.md).
