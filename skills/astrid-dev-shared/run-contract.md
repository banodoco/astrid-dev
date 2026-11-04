# Shared run contract

## Routing and bindings

Use `N` for normal, established work; `X` for very hard work with coupled or non-obvious reasoning; and `S` for super-hard work where deeper reasoning materially improves correctness. Configure each route in that run's `run.yaml` with the exact available model ID and supported reasoning effort. Luna/Haiku-class, Terra/Sonnet-class, and Sol/Opus-class describe intended capability bands only; they do not assert exact equivalence. Select high-judgment planning/advisor models independently from an Astra/Opus/Fable-class band. Do not invent IDs or silently fall back when a selected model is unavailable: record the issue and resolve it explicitly.

Every `X` or `S` execution lead delegates bounded research, mechanical edits, fixtures, or focused checks to `N` helpers where useful. This does not apply to reviewers or leaf advisors. The run configuration declares actual roles and bindings; plans may state route labels but must not duplicate model bindings.

## Scope, identity, and state

For a new run, keep control artifacts at `<project>/.otto/runs/<run-id>/`; inspect and resume an existing matching run first. Keep the minimum recovery state: source/goal, ready tasks and dependencies, evidence, and next action. Do not add an acceptance-ledger or document framework without a concrete need. Before execution, record the actual source repository, ref and SHA, dirty state, donors/dependencies, and chosen custody. Distinguish the current source/base from donor inputs and preserve user changes. Each assignment names its outcome, in-scope paths/behavior, dependencies, route, and acceptance evidence. Keep a simple run state with current candidate identity, completed work, failures, remaining checks, and next action. Continue independent work when one task is blocked.

Maintain existing run choices and evidence. Do not reset review counts, re-open passed criteria, or restart program execution because these skill documents changed. Preserve the exact tested candidate and declared review scope/budget. A changed candidate invalidates only evidence that depends on the changed content.

## Checks and repair

Run only explicitly scoped, feature-focused checks. Never run broad, auto-discovered, repository-wide, or full affected suites. Preserve the exact failing command and candidate identity. When a check fails, fix the cause in scope and rerun that same failing check; do not repeatedly rerun an unchanged failure or claim success without the result. Keep passing evidence for unaffected behavior.

An independent completion reviewer is separate from the advisor. For ordinary new delivery runs, use one integrated final completion review after scoped checks, unless the owner or accepted plan selects another policy. Allow up to five total review rounds; stop on uncontested PASS, and never pass with an unresolved blocking finding. Existing runs use their accepted plan and budget: do not add stages, reset rounds, change the reviewed candidate silently, or ask for sign-off after every task. Advice does not waive an independent review gate. Ask the advisor for a genuine blocker or consequential judgment, not routine decisions. Ask the owner only when a real authority, scope, or unresolved consequential choice requires them.

## Run template

Copy [run template](templates/run.yaml) into a new run and fill exact runtime model IDs, reasoning efforts, and availability before dispatch. A template is not a live run and does not change existing runs. Track consumed rounds in run state so restart/recovery cannot reset them.
