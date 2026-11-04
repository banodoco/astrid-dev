---
name: astrid-dev-manage
description: "Manage an accepted Astrid development plan: dispatch ready scoped tasks, maintain exact run/source state, repair failures, and preserve existing proof and review budgets."
---

# Manage Astrid development work

Read the [shared run contract](../astrid-dev-shared/run-contract.md), then consult the active working repository’s instructions. Manage work within its accepted scope and authority. Honor current run pause/STOP controls; installing or editing skills never starts or resumes work.

## Dispatch and track

- Inspect the existing run first and resume it. Preserve its actual model/effort choices, source custody, tested candidate, review counters, and program state.
- Freeze the current source identity: repository, ref/SHA, dirty state, custody, donor heads, and real dependencies. Do not treat a donor as the current base.
- Send each ready task with its outcome, scope, dependencies, exact source identity, `N`/`X`/`S` route, and explicit focused acceptance check. Give each dispatched worker [the Work guide](../astrid-dev-work/SKILL.md) with its scoped brief. Use [Advise](../astrid-dev-advise/SKILL.md) for a genuine blocker and [Release](../astrid-dev-release/SKILL.md) when entering an authorized integration or release phase. Leave dependent work waiting only on its actual dependency; continue independent tasks.
- Resolve routes through the run's exact model IDs and efforts. Never infer availability from a class label or silently substitute. Every `X`/`S` execution lead delegates bounded research or mechanical work to `N` helpers.
- Keep run state simple and current: candidate, completed/blocked tasks, exact failures, proof, review rounds consumed, and next action. Preserve passed evidence when unaffected.

## Failures and reviews

When work or a check fails, keep the first failure and its exact command/candidate. Make a concrete in-scope repair, then run the actual failing check again. If the same failure returns, inspect whether the cause, source, environment, or brief was repaired before another attempt; correct the cause at its source. Do not loop on unchanged failure or replace a failed check with a broader suite. Run only explicitly scoped feature checks.

Use the existing review plan and budget exactly. Do not add stages, reset rounds, change the reviewed candidate silently, or ask for sign-off after every task. A reviewer verifies the assigned candidate and evidence independently. Invoke [Advise](../astrid-dev-advise/SKILL.md) only for a real blocker, conflicting evidence, or consequential judgment that the accepted plan cannot settle. Ask the owner only for a genuine authority or scope decision.

At handoff, state exact candidate identity, completed tasks and checks, preserved review state, unresolved issues, and the next action. Never claim a check or review that did not run and pass.
