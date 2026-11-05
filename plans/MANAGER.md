# Initiative handoff (legacy adapter)

This initiative-specific note adapts the existing orchestrator's M-00/M-01 preparation cards. It is not a general workflow; use the [shared manager role](../skills/astrid-dev-shared/roles/manager.md) and [run contract](../skills/astrid-dev-shared/run-contract.md) for current run policy.

The initiative is paused: product work and product workers have not started. Existing advisor and orchestrator automations remain paused under STOP. A plan or skill install does not start work. Keep STOP in force until the owner explicitly starts the relevant project. Do not create replacement schedules.

## First preparation cards

When using the existing orchestrator, keep these first two IDs and meanings:

| ID | Purpose | Completion evidence |
|---|---|---|
| M-00 | Stage card amendments for the next increment and any independently ready work. Map plan task IDs to existing rows; preserve prior cards and results; scope each task's FILES and TEST selectors; resolve pinned inputs once. Do not make all six plan rewrites a prerequisite to the first Installer Consent increment. | Concise card-to-plan map, exact selectors, immutable input manifest, and no stale whole-release assertion on selected rows. |
| M-01 | Validate staged cards and the actual dependency graph; align ready rows with configured N/X/S routes through the existing manager. Do not edit live state by hand. | Every ready row has a valid card, configured route, and real prerequisites; independent eligible work is not blanket-gated. |

These IDs retain their existing meanings and dependency references. They do not authorize hand-editing live run state or require rewriting every plan before the first Installer Consent increment.

## Scope and order

Use the accepted project plan for scope, exclusions, dependencies, and focused acceptance evidence. The root [README queue](../README.md) alone owns project status and remaining human-day estimates; plans own task progress. Use the shared contract for `N`/`X`/`S` route meanings and configured model bindings.

Plan 08 (Release 1) runs under its own merge coordinator. Plan 09 (install and update confidence) is first in the queue and starts from Plan 08's verified output. Plans 01–06 describe the staged pre-main sequence. Generation may be prepared independently after explicit start, but its integration follows Installer Consent. Later work uses reviewed inputs. Plan 07 (Pinokio) starts with a review of historical notes against current source. It has no automatic dependency on Packs; record any concrete dependency found during that review.

## Review and stopping

Preserve the accepted run's review scope, candidate, and remaining review rounds. Do not add stages, reset counts, or request approval after every task. The shared run contract owns review and proof rules.

Check-ins are optional: use them only after the owner requests one or an existing run configures advisory review. The advisor's former cadence was every two hours; do one bounded review, then stop. The orchestrator's former cadence was every 15 minutes with an hourly operational review; both automations remain paused. Do not create a monitor or replacement schedule.

For a check-in, review the oldest current blocker or changed acceptance boundary. Use task counts, blocker cause, exact source and verification evidence, and whether checks are unexecuted, failed, cancelled, or passed. Check for independent work waiting unnecessarily. For X/S execution leads, use N helpers where useful. If a check failed, require the original failing check to run on the repaired candidate. Record durable conclusions in the existing run or plan.

Stop product work when paused. Run only focused checks named by the plan and targeted-check policy. Record exact source identity, check command and result, intended integration, and unresolved claims in existing run evidence. Cancellation is not a product failure; missing proof is not a pass.

Promote only the exact reviewed heads allowed by the plan, using ordinary fast-forward or create operations. Never force-push or publish to `main`, `int/r1`, or `release-1`. No GPU or pod work, model downloads, provider calls, credential access, other publication, or schedule changes are authorized by this handoff. A plan or review does not expand the owner's authorization.
