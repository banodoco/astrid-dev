# Repository rules

This is a planning and evidence-summary repository. Use the role-specific guidance in [skills/](skills/README.md) for planning, management, execution, and advice.

## Scope and authority

- This repository's setup and a plan's presence do not authorize product execution. The initiative is paused; do not launch workers, tests, schedules, or external operations until the owner explicitly starts the relevant work.
- Product source work, when started, is limited to the planned `pre-main` destination. Do not invent branches or refs; confirm actual source identities in the run before use.
- This repo stores portable plans, decisions, and evidence summaries only. Do not add credentials, private logs, absolute workstation paths, or local `.otto/` state.
- `README.md` is authoritative for active/upcoming project statuses and remaining human-days estimates. `ARCHIVE.md` is authoritative for terminal `done`/`cancelled` rows. Individual plans own task-level execution checkboxes and technical detail; do not repeat the project's status or estimate there.

## User routing and proof policy

- Route normal (`N`) work to a configured Luna/Haiku-class model, very hard (`X`) work to a configured Terra/Sonnet-class model, and super-hard (`S`) work to a configured Sol/Opus-class model. These are routing classes, not exact model identities. Every `X` or `S` execution lead delegates bounded research or mechanical work to configured `N` helpers. Reviewers do not inherit this helper requirement.
- Each run's `run.yaml` is the sole declaration of actual model IDs, reasoning efforts, availability, and role bindings. Do not infer exact equivalence from class labels or silently substitute an unavailable model.
- Run only explicitly scoped, feature-focused checks. Do not run broad, auto-discovered, repository-wide, or full affected suites. Planning-only work runs no tests unless specifically requested.
- Reviews are only those already required by the applicable plan, run configuration, and owner instruction. Preserve their exact candidate, scope, and remaining rounds; do not create extra approval stages or schedules.
