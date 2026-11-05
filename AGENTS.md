# Repository rules

This is a planning and evidence-summary repository. Use the role-specific guidance in [skills/](skills/README.md). Shared run mechanics live in the [shared run contract](skills/astrid-dev-shared/run-contract.md); the [manager role reference](skills/astrid-dev-shared/roles/manager.md) and [advisor role reference](skills/astrid-dev-shared/roles/advisor.md) define their respective responsibilities.

## Scope and authority

- This repository's setup and a plan's presence do not authorize product execution. The initiative is paused; do not launch workers, tests, schedules, or external operations until the owner explicitly starts the relevant work.
- Product source work, when started, is limited to the planned `pre-main` destination. Do not invent branches or refs; confirm actual source identities in the run before use.
- This repo stores portable plans, decisions, and evidence summaries only. Do not add credentials, private logs, absolute workstation paths, or local `.otto/` state.
- `README.md` is authoritative for active/upcoming project statuses and remaining human-days estimates. `ARCHIVE.md` is authoritative for terminal `done`/`cancelled` rows. Individual plans own task-level execution checkboxes and technical detail; do not repeat the project's status or estimate there.

## User routing and proof policy

- Follow the shared run contract for generic routing, source identity, model bindings, and proof mechanics. This repository's authority rules above still apply: no execution without explicit start, and no branch assumptions.
- Run only explicitly scoped, feature-focused checks. Do not run broad, auto-discovered, repository-wide, or full affected suites. Planning-only work runs no tests unless specifically requested.
- Reviews are only those already required by the applicable plan, run configuration, and owner instruction. Preserve their exact candidate, scope, and remaining rounds; do not create extra approval stages or schedules.
