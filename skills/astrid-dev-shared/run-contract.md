# Shared run contract

This is the single policy owner for run identity, routing, focused proof, failure repair, carry-forward, review budget, and authority. The entrypoint and role guides link here instead of maintaining competing policy copies.

## Routing and bindings

Use `N` for everything below very hard, including ordinary hard work; `X` for very hard work with coupled or non-obvious reasoning; and `S` for super-hard work where deeper reasoning materially improves correctness. `N` is the default; tag a task `X` or `S` only when it clearly needs that depth. These labels describe capability bands, not exact model identities. Configure actual available model IDs, supported reasoning efforts, availability, and role bindings in that run's `run.yaml`. A role resolves through the binding in `run.yaml` to a model entry's exact `model_id` and `reasoning_effort`; do not infer availability from a class label, invent IDs, or silently substitute. Resolve unavailability explicitly. Plan/advisor/reviewer judgment bindings are configured separately from execution routes.

Default model for each route, using the newest available model of that family:

| Route | Work | Claude | Codex |
| --- | --- | --- | --- |
| `N` | Everything below very hard, including ordinary hard work: research, reading, running checks, most changes and fixes | Haiku | Luna |
| `X` | Very hard: intricate changes, subtle bugs, coupled or non-obvious reasoning | Sonnet | Terra |
| `S` | Super hard: deep design, or correctness that needs the deepest reasoning | Opus | Sol |

Reviews, plan judgment and advice use a separate high-judgment role: Opus (Claude) or Astra (Codex); configure it in run.yaml as `completion_reviewer`, `plan_judgment` and `advisor`.

Plans tag each task with its route, and execution uses that same tag. Normally **one accountable agent works on one project**. It can execute a scoped task directly; use a manager and bounded subagents when parallelism or genuinely separate research helps, not as mandatory ceremony for a small project. If delegating, the coordinating agent retains judgment, resolves each task's configured route model, checks returned evidence, and records actual model IDs and efforts in `run.yaml`.

For `X`/`S` execution leads, delegate bounded research or mechanical work to `N` helpers where useful. Reviewers and leaf advisors do not inherit that requirement. A plan may name route labels but must not duplicate model bindings.

## Scope, source identity, and state

A skill installation, plan, or run template does not authorize product execution or publication. Follow the active repository's pause/STOP controls and accepted plan. Do not start, resume, or broaden product work without its explicit authority.

For a new run, keep control artifacts at `<project>/.otto/runs/<run-id>/`; inspect and resume a matching existing run first. Record the actual source repository, ref and SHA, dirty state, and custody; separately identify each donor/dependency and its ref/SHA/dirty state and role. Preserve user changes and distinguish the current base from donor inputs. If identity or custody conflicts with the assignment, stop dependent mutation and resolve the discrepancy. Each assignment names its outcome, in-scope behavior/paths, dependencies, source identity, route, and focused acceptance evidence.

Keep only the recovery state needed to resume: goal, ready tasks/dependencies, candidate identity, completed/blocked tasks, failures, evidence, consumed review rounds, and next action. Do not add an acceptance-ledger or document framework without a concrete need. Continue independent work when another task is blocked. Never reset accepted run choices, budgets, evidence, or program state because guidance changed.

## Checks and failure repair

Run only explicitly scoped, feature-focused checks; never broad, auto-discovered, repository-wide, full affected, or opt-in suites. Planning-only work runs no checks unless specifically requested. Use a documented narrow command/selector grounded in the current repository and task; do not invent test names, selectors, or commands.

Record each proof's exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status and diagnostic output, result, and limitations. Judge the inner build/test/install command, not a wrapper's transport status. Interpret statuses such as 125 or 127 only according to the runner and command's documented semantics; they are not universal meanings. Use `PASS`, `FAIL`, `RETRYING` (infrastructure retry in progress), and `NO-RESULT` (missing evidence). A pass applies only to the exact candidate and inputs it names.

Preserve the initial failure and its exact command/candidate. If a check fails, repair its in-scope cause and rerun that same actual failing check on the repaired candidate. Keep product failures distinct from infrastructure failures. Transient capacity, readiness, network, eviction, or missing-result failures may be retried with the same inputs; invalid requests must be corrected. After two failures with the same signature, do not run unchanged again: first change or diagnose the cause, fixture, environment, or input. Do not mask a failure, replace it with a broader check, or claim an unrun check passed.

Carry proof forward only when its relevant inputs and product/dependency/generated/installed bytes are evidenced unchanged. A changed candidate invalidates only evidence dependent on the change; preserve unaffected passing proof. Protected surfaces and changed relevant inputs require proof for the exact candidate. Accepted scoped checks do not support a claim that an entire repository or suite passed.

## Review and promotion boundaries

For ordinary new delivery, unless the owner or accepted plan selects another policy, use one integrated final completion review after required scoped checks, with at most five total rounds and stop on an uncontested PASS. Do not pass with an unresolved blocking finding. Preserve an existing run's exact accepted review scope, stage, candidate, remaining rounds, and consumed count; never add stages, reset counts, silently change the reviewed candidate, or ask for sign-off after every task. Planning-only runs have no active review stage by default.

An iterate result is a feature candidate, not an integrated or promoted result. The release workflow alone composes and rechecks the integrated candidate and performs only the authorized promotion/publication. When integrated proof fails, route the repair to the same iterate loop, then recheck the integrated candidate. Advice does not waive a review or authorize execution/publication. Ask the owner only for a real authority, scope, or unresolved consequential choice.

## Run template

Copy [run template](templates/run.yaml) into a new run and fill the exact runtime model IDs, supported reasoning efforts, and availability before dispatch. Its class labels are illustrative only. Map role keys to configured model entries in `roles`; do not create a second binding source. A template is planning-only and does not initialize, reset, or authorize any existing run.
