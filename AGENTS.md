# Repository rules

This repository contains [vision](visions/vision.md), [evidence-based gap assessments](visions/README.md), plans and their evidence summaries—not product source. Read the [extensibility philosophy](docs/extensibility-philosophy.md) for the technical direction. Follow the relevant [workflow guide](skills/README.md), [shared run contract](skills/astrid-dev-shared/run-contract.md), and role notes for run mechanics.

## Scope and authority

- Follow each project’s current authorization and run controls. For the legacy M-GPU run, consult the [initiative handoff](plans/MANAGER.md). Creating plans or installing skills does not itself start or resume product work.
- When started, follow the accepted plan and use its intended `pre-main` destination. Confirm source identities in the run; do not assume branches or refs.
- Keep plans, decisions, and evidence portable. Do not add credentials, private logs, machine-specific absolute paths, or local `.otto/` state.
- The [`plans/index.md`](plans/index.md) catalog owns all plans' status, owner, priority order and remaining estimates, including `done` and `cancelled`. The root README only displays a generated top-ten preview, and `ARCHIVE.md` points to the catalog. Each project lives in a folder with required `plan.md` (overview), `tasks.md` (work and progress), and `inputs.md` (starting code and evidence). The queue links directly to `plan.md`. Do not keep a second owner record in a plan. Owner identifies accountability, not work authorization or status.

Use the [project folder template](templates/project/plan.md) for every new project, including drafts. The [project format guide](docs/project-format.md) explains how to extend it for different kinds of work. Keep unknowns explicit; the three files can be short. Add task, design, asset, or evidence files only when they provide useful detail, linked from the three entry documents. Do not create competing README/START-HERE/PLAN overviews.

## Vision, gaps and plans

The [gap contract](visions/gaps.md) defines a small, enforceable-in-principle structure. The vision's pillars describe the creative outcomes; its operating principles describe cross-cutting constraints; stable shared gap IDs record a current source-grounded difference and closure evidence; plans declare the gaps they address (or an explicit foundational-enabler rationale). Plans own their gap links, and the plan catalog remains the only owner of project status, priority and responsibility. Do not maintain a second gap-to-plan list inside gap files.

When a plan finishes, use its exact evidence to **propose** updates to linked gaps and distinguish closed, partial, unchanged or needs-recheck outcomes. A completed plan is not proof a vision gap has closed. Preserve evidence provenance, review the proposal, and do not silently change the vision, execution scope or publication authority. Existing plans can be aligned incrementally; no automated gap updater or structural CI gate is installed yet.

## Local documentation checks

After catalog or documentation edits, run the focused `python3 scripts/check_docs.py` check. For catalog changes, regenerate the root preview with `python3 scripts/check_docs.py --sync`. CI checks this invariant and the local links/plan structure; it never rewrites the repository. See [the plan catalog](plans/index.md). These checks do not constitute product acceptance or authorization.

## Routing and checks

- Use the shared run contract for routes, model bindings, source identity, and proof. Initiative rules here still apply: no execution without explicit start and no assumed branches.
- Run only focused checks explicitly named for the work. Never run broad, auto-discovered, repository-wide, or full affected suites. Planning work runs no checks unless requested.
- Keep the review scope and remaining rounds set by the plan, run configuration, and owner. Do not add approval stages or schedules.
