# Shared run contract

This is the single policy owner for run identity, routing, focused proof, failure repair, carry-forward, review budget, and authority. The entrypoint and role guides link here instead of maintaining competing policy copies. Terms follow the [glossary](glossary.md).

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

This table and the high-judgment role below it are the only place in the skills, docs and templates that names model families; history records are exempt. `templates/run.yaml` and the Codex brief are fill-in copies of them. Elsewhere name the route, and a family only when the run used one other than the route's, never an exact model ID. When workers are on Codex, `T` work may run on the Codex taste family; Claude is recommended.

### Cheapest model first

Judge a task's difficulty before delegating it, start it on the cheapest model that can plausibly do it at that difficulty, and move up only on evidence. A task with no route tag is `N`. A release brief may set a different starting model for its run (for example, a mid-tier default for everything that is not plain fact-finding); follow the brief.

- **Start at `N`.** Fact-finding, reading, running checks, mechanical edits, and most fixes whose failing test and likely cause are already named go to `N`. Give the worker one bounded outcome, the exact files or selectors, and the proof you expect back.
- **Escalate one step at a time, on a stated reason.** Move `N` to `X` after two misses or 20 minutes without progress, or when the returned work is wrong in a way a better brief would not fix. Move `X` to `S` on the same test. Before escalating, ask whether the brief was the problem: a vague brief fails on every model. This threshold is the manager's. A worker's is different: it stops after three attempts or 45 minutes without progress on one failure and hands the manager the raw output, what it tried and its best guess.
- **Pass the failure up.** The next model gets the previous attempt's diff, raw output and best guess, so it starts from what was learned, not from zero.
- **Judgment stays put.** The manager checks each result against the diff and the proof, never against the worker's summary. Decisions, dispositions and reviews stay with the manager or the high-judgment role; they are not delegated down.
- **Drop back down.** Once a hard problem has a known cause, the remaining edits and reruns return to `N`.

Plans tag each task with its route, and execution uses that same tag. Normally **one accountable agent works on one project**. It can execute a scoped task directly; use a manager and bounded subagents when parallelism or genuinely separate research helps, not as mandatory ceremony for a small project. If delegating, the coordinating agent retains judgment, resolves each task's configured route model, checks returned evidence, and records actual model IDs and efforts in `run.yaml`.

### Who answers for a run

**Every run has exactly one accountable agent,** and it answers for the project finishing: it keeps the run alive, chases progress against `tasks.md`, sees that every task gets started, and brings the owner their decisions. Advising, hosting or handing a project along never makes a second one.

| Setup | Accountable agent | Others |
|---|---|---|
| A manager in its own session | The manager | The orchestrator advises, and stays idle between questions |
| A Claude session with [Codex workers](../astrid-dev-orchestrate/SKILL.md#use-codex-from-claude-cloud) (the default with Codex) | That session: it is the manager | Each Codex call does one card and returns |
| A Codex manager [hosted in a Claude session](../astrid-dev-orchestrate/SKILL.md#use-codex-from-claude-cloud) (only by choice) | The hosting session | Codex dispatches, judges and integrates the tasks; the host does everything Codex can't |
| One agent doing a small project itself | That agent | None |

**It is recorded where everyone can read it:** the `Run start` line in the plan's [`inputs.md`](../../templates/project/inputs.md) names the accountable session, what it may do without asking, what still needs the owner's go, and the advisor if there is one. `run.yaml` is local and git-ignored, so it can't carry this.

**Its authority comes from the owner,** in the owner's own message in that session ([start message](../astrid-dev-orchestrate/SKILL.md#the-start-message)). A brief relayed by another session is information, not authority. Only the owner's own message in a session, or a committed allow rule, lifts a permission refusal; bring the refused command to her rather than retrying.

**A manager merges its own progress pull requests,** the ones that change only one plan's `tasks.md`, with auto-merge on once `python3 scripts/astrid_dev.py check` passes. Every other merge into `main` still needs the owner's go.

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

A skill installation, plan, or run template does not authorize product execution or publication. Follow the repository's pause and stop instructions (a paused status, or a plan or brief that says stop) and its accepted plan. Do not start, resume, or broaden product work without its explicit authority.

For a new run, keep control artifacts at `<project>/.otto/runs/<run-id>/`; inspect and resume a matching existing run first. Record the actual source repository, ref and SHA, dirty state, and custody; separately identify each donor/dependency and its ref/SHA/dirty state and role. Preserve user changes and distinguish the current base from donor inputs. If identity or custody conflicts with the assignment, stop dependent mutation and resolve the discrepancy. Each assignment names its outcome, in-scope behavior/paths, dependencies, source identity, route, and focused acceptance evidence.

Keep only the recovery state needed to resume: goal, ready tasks/dependencies, candidate identity, completed/blocked tasks, failures, evidence, consumed review rounds, and next action. Do not add an acceptance-ledger or document framework without a concrete need. Continue independent work when another task is blocked. Never reset accepted run choices, budgets, evidence, or program state because guidance changed.

**Add commits only:** never rebase, amend or force-push, even on your own branch. To bring in a newer base, merge it in. Never rewrite a contributor's branch. Never read or print `.env` files, `~/.codex` or any credential or token file. A saved credential reaches every process in the environment, tests and workers included: keep it in an environment of its own, stub every test that would call the real provider, and keep paid or credentialed steps with the manager. Before a run pauses or ends, release every rented machine it made, and say which, whatever happened ([steps](../astrid-dev-gpu-validate/SKILL.md#pod-hygiene)).

### Decisions ledger when the owner is unavailable

When work proceeds without the owner (for example, a contributor or agent helping while the owner is offline or out of quota), keep a decisions ledger from the [template](templates/decisions-ledger.md). Record every override of the written plan, every best guess where the plan is silent, every place the plan says stop and ask, such as a conflict where both sides change one statement, that you resolved provisionally instead of waiting, the trajectory you inferred, and improvements you did not build, each with evidence, the candidate SHA and how to revert. This is the concrete need the paragraph above asks for: it lets the owner accept, change or revert each call later, without rereading the run. A ledger entry is never authorization; anything that lands still needs the owner's go.

## Checks and failure repair

Locally, run only explicitly scoped, feature-focused test runs; never broad, auto-discovered, repository-wide, full affected, or opt-in suites. The full relevant suite runs on hosted CI, only at the moments the [table below](#when-a-test-run-is-load-bearing) names ([how](../astrid-dev-green/SKILL.md#using-github-actions)). Planning-only work runs no checks unless specifically requested. Use a documented narrow command/selector grounded in the current repository and task; do not invent test names, selectors, or commands.

Record each proof's exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status and diagnostic output, result, and limitations. Judge the inner build/test/install command, not a wrapper's transport status. Interpret statuses such as 125 or 127 only according to the runner and command's documented semantics; they are not universal meanings. Use `PASS`, `FAIL`, `RETRYING` (infrastructure retry in progress), and `NO-RESULT` (missing evidence). A pass applies only to the exact candidate and inputs it names.

Preserve the initial failure and its exact command/candidate. If a check fails, repair its in-scope cause and rerun that same actual failing check on the repaired candidate. Keep product failures distinct from infrastructure failures. Transient capacity, readiness, network, eviction, or missing-result failures may be retried with the same inputs; invalid requests must be corrected. After two failures with the same signature, do not run unchanged again: first change or diagnose the cause, fixture, environment, or input. Do not mask a failure, replace it with a broader check, or claim an unrun check passed.

Carry proof forward only when its relevant inputs and product/dependency/generated/installed bytes are evidenced unchanged. A changed candidate invalidates only evidence dependent on the change; preserve unaffected passing proof. Protected surfaces and changed relevant inputs require proof for the exact candidate. Accepted scoped checks do not support a claim that an entire repository or suite passed.

**Never edit, skip, loosen, xfail or delete a test, a fixture, an oracle line or a check to get a pass,** in the file or on the command line. If a card would make one untrue and does not list it, the worker stops and reports the exact lines. The manager rules in the same turn and records the before and after in the card's row, and only then may the line change. A pinned test that pins a defect goes to the review or the contract's author, not to the worker.

### When a test run is load-bearing

Run tests at the moments where the result changes a decision, and at no others. A run is load-bearing when someone is about to rely on it:

| Moment | Run | Why it bears load |
| --- | --- | --- |
| **Before the first task** | The plan's test inventory, once, on the starting versions | Without it, a later failure can't be told from one that was already there |
| **After each task** | Only that task's focused proof: the tests that would fail if this task were wrong | It decides whether the task is done |
| **Before others build on it** (a contract, data model, shared interface or security boundary lands, or a chain hands over to a different worker) | The tests that cover that shared part | A mistake found later means redoing every task built on it |
| **Before review, and before anything reaches `main` or users** | The full relevant suite, once, on the integrated head, on CI | It is the last point where a failure is cheap |

Not load-bearing, so skip it: a broad suite after every task; re-running a proof whose inputs have not changed (carry it forward); a test with no baseline to compare against; a run whose result nobody will act on. A **regression** is a test that ran and passed on a baseline and fails on the candidate. A test that is absent, skipped or uncollected on every baseline has no baseline, so it is not a regression; it is fixed only if this run added it. A test this run added that fails on the candidate blocks like a regression: fix it, or leave the test out of the candidate and give it a row in the green-mains plan ([Plan 39](../../plans/39-green-mains/plan.md)). [`env/baseline-diff.py`](../../env/README.md) (`astrid-baseline-diff`) sorts results by this rule; don't sort by hand. After each load-bearing run, compare with the baseline by this rule and fix only what is new. For a merge or a rebuild onto another branch, the baseline is the branch you merged onto, not the one you came from, and the test scope is every test file that touches a changed module, on both, not a focused subset: a clean textual merge can still break (one side deletes a file the other starts reading), and the old branch's existing failures hide it.

**One exception, by cost:** when the whole inventory runs in seconds, run all of it at every moment above. The table exists to ration expensive runs, not to justify skipping cheap ones.

A plan names its load-bearing moments in `tasks.md`: the test inventory, each task's focused proof, and any join that needs the shared part re-proven.

In astrid-dev itself, run `python3 scripts/astrid_dev.py check` before every commit, merge and pull request. It checks structure and links in seconds, so the cost exception applies.

## Review and promotion boundaries

Review rounds are proportional, not a default ritual: where the accepted plan sets any, end with them on the integrated candidate. An accepted plan may also set a review stop after a load-bearing part (see the [plan skill](../astrid-dev-plan/SKILL.md#write-the-task-list)); a stop follows this same protocol on that part's integrated result, with its own agreed rounds, and the tasks built on it wait for it. The final review always runs after required scoped checks and before publishing or closing, by the `completion_reviewer`. The plan records how many rounds at most: the planner recommends a number from risk and complexity (as a guide, 0 for a simple, bounded project where ordinary PR review is enough; 1 for meaningful complexity; 2 or 3 only for cross-repository, release, security or data work) and the owner agrees. Each finding comes back as a task card (outcome, route, scope, dependencies, focused proof) and is done before the next round. Stop after a round with no blocking findings; a blocking finding still open after the last agreed round goes straight to the orchestrator, who rules under the owner's delegation or takes it to the owner; a run with no orchestrator takes it to the owner. Do not pass with an unresolved blocking finding. Preserve an existing run's exact accepted review scope, stage, candidate, remaining rounds, and consumed count; never add stages, reset counts, silently change the reviewed candidate, or ask for sign-off after every task. Planning-only runs have no active review stage by default.

An iterate result is a feature candidate, not an integrated or promoted result. Its author does not integrate, independently review, promote or publish it, or claim that any of these happened. The release workflow alone composes and rechecks the integrated candidate and performs only the authorized promotion/publication. When integrated proof fails, route the repair to the same iterate loop, then recheck the integrated candidate. Advice does not waive a review or authorize execution/publication. Ask the owner only for a real authority, scope, or unresolved consequential choice.

## Run template

Copy [run template](templates/run.yaml) into a new run and fill the exact runtime model IDs, supported reasoning efforts, and availability before dispatch. Its class labels are illustrative only. Map role keys to configured model entries in `roles`; do not create a second binding source. A template is planning-only and does not initialize, reset, or authorize any existing run.
