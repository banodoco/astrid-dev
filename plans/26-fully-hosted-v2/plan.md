# 26 — Fully hosted Astrid V2 (cloud database and files)

**Start here:** read [AGENTS.md](../../AGENTS.md), follow the [shared run contract](../../skills/astrid-dev-shared/run-contract.md), then review [tasks](tasks.md) and [inputs](inputs.md). Status, priority, owner and remaining estimate live only in the [catalog](../index.md).

**Vision gaps:** [F-006 — Fully hosted workspace](../../visions/gaps/F-006-fully-hosted-workspace.md) (primary); [F-001 — reliability](../../visions/gaps/F-001-platform-reliability.md) and [F-002 — safe user control](../../visions/gaps/F-002-safe-user-control.md) (supporting). Completion does not automatically close any gap.

## Goal and distinction

Deliver a **fully cloud-hosted Astrid** accessible from a browser: the **persistent project database, media files, application services, agents, generation and rendering** run in hosted infrastructure. A user should not have to install or host the application to start creating.

V1 ([Plan 25](../25-cloud-assist-v1/plan.md)) is intentionally local-first with remote workers. **V2 is separately scoped cloud custody and a hosted experience**, not an incremental checkbox in the V1 remote-execution implementation.

**Included (proposed):** identity/accounts, cloud project/database authority, durable object/file storage, hosted App/runtime, permissioned agent and model/render execution built on V1 contracts, upload/download, project restore/export, backup, isolation, quotas, cost and security/retention policies, device/browser compatibility.

**Deferred:** replacing the local-first app or forcing existing local users to move data; automatic conversion of private projects without consent; new artistic features unrelated to hosted readiness; arbitrary multi-tenant collaboration without accepted permissions.

## Build on existing work

- Accepted V1 remote execution and artifact contracts; do not duplicate cloud worker orchestration.
- Existing Astrid App, Runtime authority, project/timeline schema, generation/render execution and authorization model. Audit source revisions before selecting storage/database.
- Preserve a bidirectional or at least complete **export** path, documented custody and user-controlled access. No provider/database platform is selected by this draft.

## Proposed sequence (not authorized)

1. Revalidate the V1 results and map canonical project state, media references, permissions, workspaces and all persistent local file paths.
2. Choose cloud database/object storage, identity, hosted app/runtime topology and tenant boundaries; identify ownership, cost, data residency and recovery.
3. Implement hosted persistence and asset APIs with versioned project identity and access control, verified no cross-account data leakage.
4. Adapt the cloud-agent/generation/render path from V1 to operate against cloud-owned project state and durable cloud assets.
5. Test new-user signup/open, project edits/reopen across devices, storage reliability, billing/quotas and stop/retry.
6. Test backup/restore, privacy, deletion, export/migration to local custody, and security/load evidence. Publish only supported cells.

## Project interface and handoff

**Consumes:** [Plan 25](../25-cloud-assist-v1/plan.md)'s *verified* remote-work/job and artifact contracts, with exact source/evidence references recorded at implementation start. Plan 25 being queued or eventually marked done is not, by itself, proof that a particular integration contract is qualified.

**Produces:** an authenticated hosted project-state and media-custody contract (identity, access, persistence, backup, export and deletion) that other hosted features can consume, with exact candidate revisions and negative tenancy tests linked from the completion PR. Do not duplicate V1's remote worker orchestration.

## Completion

An authenticated browser user can create and revisit a hosted Astrid project with durable cloud files/database, run a generation and render, and recover after interruption. Evidence includes tenancy isolation, revocation, permission controls, backup/restore, export/deletion, limits and disaster recovery. The existing local-first mode remains available.

**Authorization:** queued proposal; cloud-provider choice, spend, legal/security review, migration policy, owner and task routing must be explicitly approved before building or shipping.
