# Repository rules

This is a planning and evidence-summary repository. Read the vendored [Megado method](.agents/skills/megado/SKILL.md) for planning/delivery mechanics; its linked references and templates are included in the same directory.

## Scope and authority

- This repository's setup and a plan's presence do not authorize product execution. The initiative is paused; do not launch workers, tests, schedules, or external operations until the owner explicitly starts the relevant work.
- Product source work, when started, is limited to the planned `pre-main` destination. Do not invent branches or refs; confirm actual source identities in the run before use.
- This repo stores portable plans, decisions, and evidence summaries only. Do not add credentials, private logs, absolute workstation paths, or local `.otto/` state.
- `README.md` is authoritative for active/upcoming project statuses and remaining human-days estimates. `ARCHIVE.md` is authoritative for terminal `done`/`cancelled` rows. Individual plans own task-level execution checkboxes and technical detail; do not repeat the project's status or estimate there.

## User routing and proof policy

- Route normal (`N`) execution work to Luna, very hard (`X`) work to Terra, and super-hard (`S`) work to Sol. Every Terra or Sol **execution lead** uses Luna helpers for bounded research, mechanical edits, fixtures, and focused checks. This helper requirement does not apply to reviewers.
- A run's `run.yaml` is the sole declaration of actual role, model, and reasoning-effort bindings for that run. Plans use the route labels above; do not duplicate divergent bindings in prose.
- `targeted-tests-only` is the repo's test policy and overrides general Megado defaults: run only explicitly scoped, feature-focused tests. Do not run broad, auto-discovered, repository-wide, or full affected suites, including the vendored method's general final broad-suite default. No tests are needed for planning-only work unless specifically requested.
- Reviews are only those required by the applicable plan/run and user instruction. Do not create extra approval stages or schedules.
