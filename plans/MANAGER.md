# Execution handoff

This is a static handoff for a future, explicitly started effort. It does not start product work or reactivate any automation. Until the owner starts the initiative, leave the existing worker and advisor schedules paused and do not alter STOP controls.

## Before work

1. Read the relevant project plan and shared references from [MASTER.md](MASTER.md).
2. Create or resume the matching run using [Manage](../skills/astrid-dev-manage/SKILL.md). Keep its `run.yaml` as the single source of actual role/model/effort bindings and its `.otto/` control and evidence state local and ignored.
3. Confirm the owner's explicit start and select source custody for the product repository as required by the [shared run contract](../skills/astrid-dev-shared/run-contract.md). Freeze actual current source identities; do not reuse historical refs as current inputs or invent branches.
4. Dispatch only scoped tasks with outcomes, exact dependencies, feature-focused acceptance selectors, resource limits, and evidence destinations. Use N/Luna, X/Terra, S/Sol routing. Terra/Sol execution leads use Luna helpers; reviewers do not.

## Initial card preparation

When the existing orchestrator is used, retain its first two preparation IDs:

| ID | Purpose | Completion evidence |
|---|---|---|
| M-00 | Stage the card amendments for the next increment and any independently ready work. Map plan task IDs to existing rows, preserve old cards/results, scope each task's FILES and TEST selectors, and resolve pinned inputs once. Do not make all six plan rewrites a prerequisite to the first installer increment. | A concise card-to-plan map, exact selectors, immutable input manifest, and no stale whole-release assertion on selected rows. |
| M-01 | Validate the staged cards and actual dependency graph; align ready rows with the configured N/X/S routes through the existing manager. Do not edit live state by hand. | Every ready row has a valid card, configured route, real prerequisites, and independent eligible work is not blanket-gated. |

## Order and integration

Plans 01–06 deliver the staged pre-main sequence: installer consent; generation completion and its later integration; concurrent editing; accepted remaining fixes; CPU Packs. Track actual task progress in the run, not by adding another project status list here. Let independent work proceed only when its real inputs are available; generation integration waits for installer, and later increments consume actual reviewed inputs. Promote only the exact verified heads allowed by the plan, using ordinary fast-forward/create operations; no force, main, int/r1, or release-1 publication.

Plan 07 Pinokio is queued last. Start with reconciling dated historical plans against current source and the product's present scope. It may progress independently after an explicit start. There is no blanket dependency in either direction between Pinokio and Packs; only a concrete dependency found during reconciliation may gate work, and the run must record it. Do not treat historical `BLOCKED` snapshots as live state or as proof of current failure/success.

## Evidence and stop boundaries

Use only the exact feature-focused tests named by the plan and the user's targeted-tests-only policy. Do not run broad or auto-discovered suites. Reuse unchanged evidence; rerun only checks affected by changed code or composed inputs. Record exact source heads, selectors, pass/fail/unexecuted outcomes, intended integration, and remaining claims in the run evidence. Cancellation is not a product failure; missing proof is not a pass.

No GPU, pod, model downloads, provider calls, credential access, main/release publication, or schedule changes are authorized by this handoff. A plan and a successful review do not expand the owner's authorization.
