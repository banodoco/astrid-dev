# F-006 — A fully hosted Astrid workspace does not yet exist

**Applies to:** [Local-first, cloud-capable](../principles.md#local-first-cloud-capable) · [In the creator's control](../principles.md#in-the-creators-control) · [Eliminate needless technical wrangling](../principles.md#eliminate-needless-technical-wrangling) · **Assessment:** Open; no qualified fully hosted project/database/media lifecycle.

## Desired state

A creator can use Astrid from a browser without maintaining a local install. The hosted workspace owns persistent project/database state, files/media, accounts and access controls, while cloud agents, generation and video rendering execute under explicit authorization and clear budgets. Projects can be exported or migrated back into user custody; reliable backup, restore, isolation and deletion are supported.

## Current state

Astrid has a browser-capable App, Runtime and cloud/provider execution paths, but the [Cloud-assisted V1 plan](../../plans/25-cloud-assist-v1/plan.md) deliberately **keeps durable files and project database local**. An always-available hosted tenancy, canonical cloud database, durable object storage and migration/recovery contract are not qualified.

## Gap

Hosted ownership and tenancy of persistent project state, database and media are missing, as are the authenticated project API, account permissions, asset retention, durability, quotas/spend controls, backups and migrations. These are not automatically supplied by remote inference or cloud-hosted agents.

## Closure evidence

A new user can open a hosted Astrid workspace in a browser, create a project, save and reopen across sessions/devices, run a generation and render, and observe durable, permission-scoped data; accounts are isolated. Backup/restore, quota, delete, export/migration and interrupted execution are tested. A local-first/offline option remains a distinct supported route rather than being silently replaced.

## Sources and reassessment

[Plan 26 — fully hosted Astrid V2](../../plans/26-fully-hosted-v2/plan.md) · [Plan 25 — cloud-assisted local-files V1](../../plans/25-cloud-assist-v1/plan.md) · [F-001 — platform reliability](F-001-platform-reliability.md). This gap is **cloud persistence/tenancy** and has a separate closure test from F-005.
