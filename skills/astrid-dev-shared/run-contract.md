# Shared run contract

This is the single policy owner for run identity, routing, focused proof, failure repair, carry-forward, review budget, and authority. The entrypoint and role guides link here instead of maintaining competing policy copies.

## Routing and bindings

Use `N` for everything below very hard, including ordinary hard work; `X` for very hard work with coupled or non-obvious reasoning; `S` for super-hard work where deeper reasoning materially improves correctness; and `T` for taste work: small, editorial refinement where the quality is a matter of judgment. `N` is the default; tag a task `X`, `S` or `T` only when it clearly needs that depth. These labels describe capability bands, not exact model identities. Configure actual available model IDs, supported reasoning efforts, availability, and role bindings in that run's `run.yaml`. A role resolves through the binding in `run.yaml` to a model entry's exact `model_id` and `reasoning_effort`; do not infer availability from a class label, invent IDs, or silently substitute. Resolve unavailability explicitly. Plan/advisor/reviewer judgment bindings are configured separately from execution routes.

Default model for each route, using the newest available model of that family:

| Route | Work | Claude | Codex |
| --- | --- | --- | --- |
| `N` | Everything below very hard, including ordinary hard work: research, reading, running checks, most changes and fixes | Haiku | Luna |
| `X` | Very hard: intricate changes, subtle bugs, coupled or non-obvious reasoning | Sonnet | Terra |
| `S` | Super hard: deep design, or correctness that needs the deepest reasoning | Opus | Sol |
| `T` | Taste: small, editorial refinement of something that already exists, such as user-facing copy, error and refusal messages, names, a screen's layout or a doc's voice | Opus | Astra |

Reviews, plan judgment and advice use a separate high-judgment role: Opus (Claude) or Astra (Codex); configure it in run.yaml as `completion_reviewer`, `plan_judgment` and `advisor`.

Plans tag each task with its route, and execution uses that same tag. Normally **one accountable agent works on one project**. It can execute a scoped task directly; use a manager and bounded subagents when parallelism or genuinely separate research helps, not as mandatory ceremony for a small project. If delegating, the coordinating agent retains judgment, resolves each task's configured route model, checks returned evidence, and records actual model IDs and efforts in `run.yaml`.

A `T` task is **editorial, not creative**: it refines an existing surface against a stated intent and never adds scope. Keep it small (one screen, one message family, one doc), and move anything structural or new into its own `N`, `X` or `S` task. The task card names the surface, its current text or a screenshot, the intent and the taste rules that apply (for example: minimal, plain words, never lies, always a next step). Its proof is the exact before and after, checked against those rules, plus the surface's own tests. Where the owner's taste decides, the owner sees that before and after. The `T` lead makes the edits itself and may delegate only mechanical checks.

An `X` or `S` execution lead always delegates bounded research, reading, mechanical edits and running checks to `N` helpers, and keeps the judgment and the final change itself. Reviewers and leaf advisors do not inherit that requirement. A plan may name route labels but must not duplicate model bindings.

## Actual route provenance

Plan and role bindings in `run.yaml` are not proof of what ran. At each meaningful planning, research, implementation, testing or review invocation, record the **route** (`N`, `X` or `S`), role and task. Add `--override <name>` only where the run used a model other than the route's. Never put exact model IDs in PRs or other repository artifacts.

```sh
python3 scripts/model_usage.py --run-dir plans/<project>/.otto/runs/<id> record \
  --route N --role implementation --task task-1 [--override <name>]
python3 scripts/model_usage.py --run-dir plans/<project>/.otto/runs/<id> summary
```

The local `model-usage.jsonl` is under gitignored `.otto/`; do not publish raw logs. Copy the `Routes used:` line into the review submission, or write `Unknown — <reason>`. A manual log is reporting, not authentication.

## Scope, source identity, and state

A skill installation, plan, or run template does not authorize product execution or publication. Follow the active repository's pause/STOP controls and accepted plan. Do not start, resume, or broaden product work without its explicit authority.

For a new run, keep control artifacts at `<project>/.otto/runs/<run-id>/`; inspect and resume a matching existing run first. Record the actual source repository, ref and SHA, dirty state, and custody; separately identify each donor/dependency and its ref/SHA/dirty state and role. Preserve user changes and distinguish the current base from donor inputs. If identity or custody conflicts with the assignment, stop dependent mutation and resolve the discrepancy. Each assignment names its outcome, in-scope behavior/paths, dependencies, source identity, route, and focused acceptance evidence.

Keep only the recovery state needed to resume: goal, ready tasks/dependencies, candidate identity, completed/blocked tasks, failures, evidence, consumed review rounds, and next action. Do not add an acceptance-ledger or document framework without a concrete need. Continue independent work when another task is blocked. Never reset accepted run choices, budgets, evidence, or program state because guidance changed.

### Decisions ledger when the owner is unavailable

When work proceeds without the owner (for example, a contributor or agent helping while the owner is offline or out of quota), keep a decisions ledger from the [template](templates/decisions-ledger.md). Record every override of the written plan, every best guess where the plan is silent, every STOP hunk you resolved provisionally instead of waiting, the trajectory you inferred, and improvements you did not build, each with evidence, the candidate SHA and how to revert. This is the concrete need the paragraph above asks for: it lets the owner accept, change or revert each call later, without rereading the run. A ledger entry is never authorization; anything that lands still needs the owner's go.

## Checks and failure repair

Run only explicitly scoped, feature-focused checks; never broad, auto-discovered, repository-wide, full affected, or opt-in suites. Planning-only work runs no checks unless specifically requested. Use a documented narrow command/selector grounded in the current repository and task; do not invent test names, selectors, or commands.

Record each proof's exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status and diagnostic output, result, and limitations. Judge the inner build/test/install command, not a wrapper's transport status. Interpret statuses such as 125 or 127 only according to the runner and command's documented semantics; they are not universal meanings. Use `PASS`, `FAIL`, `RETRYING` (infrastructure retry in progress), and `NO-RESULT` (missing evidence). A pass applies only to the exact candidate and inputs it names.

Preserve the initial failure and its exact command/candidate. If a check fails, repair its in-scope cause and rerun that same actual failing check on the repaired candidate. Keep product failures distinct from infrastructure failures. Transient capacity, readiness, network, eviction, or missing-result failures may be retried with the same inputs; invalid requests must be corrected. After two failures with the same signature, do not run unchanged again: first change or diagnose the cause, fixture, environment, or input. Do not mask a failure, replace it with a broader check, or claim an unrun check passed.

Carry proof forward only when its relevant inputs and product/dependency/generated/installed bytes are evidenced unchanged. A changed candidate invalidates only evidence dependent on the change; preserve unaffected passing proof. Protected surfaces and changed relevant inputs require proof for the exact candidate. Accepted scoped checks do not support a claim that an entire repository or suite passed.

## Review and promotion boundaries

For ordinary new delivery, unless the owner or accepted plan selects another policy, end with review rounds on the integrated candidate. An accepted plan may also set a review stop after a load-bearing part (see the [plan skill](../astrid-dev-plan/SKILL.md#write-the-task-list)); a stop follows this same protocol on that part's integrated result, with its own agreed rounds, and the tasks built on it wait for it. The final review always runs after required scoped checks and before publishing or closing, by the `completion_reviewer`. The plan records how many rounds at most: the planner recommends a number from risk and complexity (as a guide, 0 for a trivial change where ordinary PR review is enough, 1 for a small low-risk change, 2 for an ordinary project, 3 for cross-repository, release, security or data work) and the owner agrees. Each finding comes back as a task card (outcome, route, scope, dependencies, focused proof) and is done before the next round. Stop after a round with no blocking findings; a blocking finding still open after the last agreed round goes to the owner. Do not pass with an unresolved blocking finding. Preserve an existing run's exact accepted review scope, stage, candidate, remaining rounds, and consumed count; never add stages, reset counts, silently change the reviewed candidate, or ask for sign-off after every task. Planning-only runs have no active review stage by default.

An iterate result is a feature candidate, not an integrated or promoted result. The release workflow alone composes and rechecks the integrated candidate and performs only the authorized promotion/publication. When integrated proof fails, route the repair to the same iterate loop, then recheck the integrated candidate. Advice does not waive a review or authorize execution/publication. Ask the owner only for a real authority, scope, or unresolved consequential choice.

## Run template

Copy [run template](templates/run.yaml) into a new run and fill the exact runtime model IDs, supported reasoning efforts, and availability before dispatch. Its class labels are illustrative only. Map role keys to configured model entries in `roles`; do not create a second binding source. A template is planning-only and does not initialize, reset, or authorize any existing run.
