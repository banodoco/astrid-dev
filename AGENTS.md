# Repository rules

This repository contains plans and evidence summaries, not product source. Follow the relevant [workflow guide](skills/README.md), [shared run contract](skills/astrid-dev-shared/run-contract.md), and role notes for run mechanics.

## Scope and authority

- Follow each project’s current authorization and run controls. For the legacy M-GPU run, consult the [initiative handoff](plans/MANAGER.md). Creating plans or installing skills does not itself start or resume product work.
- When started, follow the accepted plan and use its intended `pre-main` destination. Confirm source identities in the run; do not assume branches or refs.
- Keep plans, decisions, and evidence portable. Do not add credentials, private logs, machine-specific absolute paths, or local `.otto/` state.
- The root `README.md` owns active/upcoming status, owner, and remaining human-day estimates. `ARCHIVE.md` owns completed and cancelled entries. Plans own technical scope and task checkboxes; do not keep a second owner record in a plan. Owner identifies accountability, not work authorization or status.

## Routing and checks

- Use the shared run contract for routes, model bindings, source identity, and proof. Initiative rules here still apply: no execution without explicit start and no assumed branches.
- Run only focused checks explicitly named for the work. Never run broad, auto-discovered, repository-wide, or full affected suites. Planning work runs no checks unless requested.
- Keep the review scope and remaining rounds set by the plan, run configuration, and owner. Do not add approval stages or schedules.
