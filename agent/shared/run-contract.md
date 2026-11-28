---
description: Shared authority, routing, proof and run rules for Astrid development.
---

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

**Reviews.** A review's verdict runs on the high-judgment role. A check of a bounded fix against a named oracle (its failing case or probe) may run on `X`. `N` may gather facts for a review (check status, failure IDs, diff scope) but never gives the verdict. Check a pure sync by tree equality. A bounded-fix check runs the focused tests on both base and head. A bounded-fix check goes to the high-judgment role only when its own tests cannot show it is right (see the per-card rule under [review and promotion boundaries](#review-and-promotion-boundaries)); size alone is not a reason. A meter, gate or check is reviewed by injecting the failures it must catch. The run names the actual reviewer model, flags and permissions where it records its bindings (`run.yaml`, or the run board for a dispatch run).

This table and the high-judgment role below it are the only place in the skills, docs and templates that defines model families; other documents link here rather than copy it; history records are exempt. `templates/run.yaml` and the Codex brief are fill-in copies of them. Elsewhere name the route, and a family only when the run used one other than the route's, never an exact model ID. When workers are on Codex, `T` work may run on the Codex taste family; Claude is recommended.

### ChatGPT session modes

When a task runs in a ChatGPT session (ChatGPT web sessions only: a fresh packet session in the [dispatch workstream](../roles/orchestrator/multi-manager-dispatch.md), or a session an orchestrator starts in ChatGPT; a Codex manager or worker run by `codex exec` takes its model and effort from the run's bindings, not from this table), the session's mode follows the task's route. The owner set this on 23 November 2026:

| Route | ChatGPT mode |
| --- | --- |
| `N` | High |
| `X` | Extra High |
| `S` | Pro |

A packet takes the mode of its hardest card, and its file names it (`**Route:**`). `T` work follows the run's brief; this table sets nothing for it. A mode that is not offered on the account is resolved explicitly (the next mode up, or the owner), never silently substituted. Moving a card up a route moves its session up a mode, on the same evidence as [Cheapest model first](#cheapest-model-first).

### Cheapest model first

Judge a task's difficulty before delegating it, start it on the cheapest model that can plausibly do it at that difficulty, and move up only on evidence. A task with no route tag is `N`. A release brief may set a different starting model for its run (for example, a mid-tier default for everything that is not plain fact-finding); follow the brief.

- **Start at `N`.** Fact-finding, reading, running checks, mechanical edits, and most fixes whose failing test and likely cause are already named go to `N`. Give the worker one bounded outcome, the exact files or selectors, and the proof you expect back.
- **Escalate one step at a time, on a stated reason.** Move `N` to `X` after two misses or 20 minutes without progress, or when the returned work is wrong in a way a better brief would not fix. Move `X` to `S` on the same test. Before escalating, ask whether the brief was the problem: a vague brief fails on every model. This threshold is the manager's. A worker's is different: it stops after three attempts or 45 minutes without progress on one failure and hands the manager the raw output, what it tried and its best guess.
- **Pass the failure up.** The next model gets the previous attempt's diff, raw output and best guess, so it starts from what was learned, not from zero.
- **Judgment stays put.** The manager checks each result against the diff and the proof, never against the worker's summary. Decisions, dispositions and reviews stay with the manager or the high-judgment role; they are not delegated down.
- **Drop back down.** Once a hard problem has a known cause, the remaining edits and reruns return to `N`.

Plans tag each task with its route, and execution uses that same tag. Normally **one accountable agent works on one project**. In a [lane](glossary.md), the **lane's orchestrator is the accountable agent for every plan run in it**, and each fresh ChatGPT packet session delivers only its packet as bounded delegated work ([packets option](../roles/orchestrator/multi-manager-dispatch.md)). It can execute a scoped task directly; use a manager and bounded subagents when parallelism or genuinely separate research helps, not as mandatory ceremony for a small project. If delegating, the coordinating agent retains judgment, resolves each task's configured route model, checks returned evidence, and records actual model IDs and efforts in `run.yaml`.

### Who answers for a run

**Every run has exactly one accountable agent,** and it answers for the project finishing: it keeps the run alive, chases progress against `tasks.md`, sees that every task gets started, and brings the owner their decisions. Advising, hosting or handing a project along never makes a second one.

| Setup | Accountable agent | Others |
|---|---|---|
| A plan in a [lane](glossary.md), in either option | The lane's orchestrator, for every plan run in the lane | Its hosted manager or packet sessions are bounded delegates; the Lead holds the release-level part |
| Outside a lane: a manager in its own session for a whole plan | That manager | The orchestrator advises, and stays idle between questions |
| Outside a lane: a Claude session with [Codex workers](../roles/orchestrator.md#use-codex-from-claude-cloud) (the default with Codex) | That session: it is the manager | Each Codex call does one card and returns |
| Outside a lane: a Codex manager [hosted in a Claude session](../roles/orchestrator.md#use-codex-from-claude-cloud) (only by choice) | The hosting session | Codex dispatches, judges and integrates the tasks; the host does everything Codex can't |
| One agent doing a small project itself | That agent | None |

**It is recorded where everyone can read it, once:** the `Run start` line in the plan's [`inputs.md`](../../templates/project/inputs.md) names the accountable session, what it may do without asking, what still needs the owner's go, and the advisor if there is one. In a lane, `Run start` is a pointer to the lane brief, and the brief holds the rest. The Lead writes the brief and each plan's pointer in one PR, and records the owner's go in the brief's `**Go:**` before the launch. The orchestrator never writes `Run start`. Outside a lane, the session preparing the run writes it with the owner's go, in the owner's words.

**Its authority comes from the owner,** in the owner's own message in that session ([start message](../roles/orchestrator.md#the-start-message)). The owner sends every launch personally, a lane's included. The lane's orchestrator sends its delegates' start messages (packet sessions, and a hosted Codex manager) from the owner's own ChatGPT account; they are bounded by the brief and are not launches. A hosted Codex manager's start message carries the same three parts as the launch line; a packet session's start message is the one in [multi-manager-dispatch.md](../roles/orchestrator/multi-manager-dispatch.md). A Claude-to-Claude message is never a launch or a go, and a brief relayed by another session is information, not authority. Only the owner's own message in a session, or a committed allow rule, lifts a permission refusal; bring the refused command to the owner rather than retrying.

**One merge rule for the accountable agent.** On a passing check or green CI, it merges its plan's `tasks.md`-only progress PRs (auto-merge on once `python3 scripts/astrid_dev.py check` passes), its brief's Standing rulings and State edits, and PRs into its plan branches. Into `release/<N>/main` it merges only through the release gate named in the brief's Merges (the Lead by default). Every other merge into `main` needs the owner's go. Packet sessions merge nothing.

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

An **astrid-dev-only plan** may be started without release membership only on the owner's explicit instruction, following [Manage's dev-only project route](../roles/manager/whole-project.md#steps). This does not loosen review, protected `main` merges, permission checks, evidence requirements or any product-repository release gate.

A skill installation, plan, or run template does not authorize product execution or publication. Follow the repository's pause and stop instructions (a paused status, or a plan or brief that says stop) and its accepted plan. Do not start, resume, or broaden product work without its explicit authority.

For a new run, keep control artifacts at `<project>/.otto/runs/<run-id>/`; inspect and resume a matching existing run first. Record the actual source repository, ref and SHA, dirty state, custody, and destination branch (the plan or fix branch the work lands on); separately identify each dependency and its ref/SHA/dirty state and role. Preserve user changes and distinguish the current base from dependency inputs. If identity or custody conflicts with the assignment, stop dependent mutation and resolve the discrepancy. Each assignment names its outcome, in-scope behavior/paths, dependencies, source identity, route, and focused acceptance evidence.

Keep only the recovery state needed to resume: goal, ready tasks/dependencies, candidate identity, completed/blocked tasks, failures, evidence, consumed review rounds, and next action. Do not add an acceptance-ledger or document framework without a concrete need. Continue independent work when another task is blocked. Never reset accepted run choices, budgets, evidence, or program state because guidance changed.

**Add commits only:** never rebase, amend or force-push, even on your own branch. To bring in a newer base, merge it in. Never rewrite a contributor's branch. Never read or print `.env` files, `~/.codex` or any credential or token file. A saved credential reaches every process in the environment, tests and workers included: keep it in an environment of its own, stub every test that would call the real provider, and keep paid or credentialed steps with the manager. Before a run pauses or ends, release every rented machine it made, and say which, whatever happened ([steps](workstreams/gpu-validate.md#pod-hygiene)).

### Decisions ledger when the owner is unavailable

When work proceeds without the owner (for example, a contributor or agent helping while the owner is offline or out of quota), keep a decisions ledger from the [template](templates/decisions-ledger.md). Record any proposed change to the written plan, an in-scope best guess where it is silent, any stop-and-ask decision awaiting authority (such as a conflict where both sides change one statement), the trajectory inferred, and improvements not built. Include evidence, the candidate SHA when one exists, and how to revert. A provisional proposal is never permission to execute work outside the accepted scope or bypass a stop. This is the concrete need the paragraph above asks for: it lets the owner accept, change or revert each call later, without rereading the run. A ledger entry is never authorization: stop-and-ask boundaries remain stops, and anything that lands still needs the owner's go.

## Coordination: boards and check-ins

1. **Boards.** One astrid-dev issue per plan or run, titled `board: release <N> plan <P>` (or `<name>`), and one per release Lead, titled `board: release <N> lead`. A [lane](glossary.md) has one board, titled `board: lane <lane>`, named in its brief's `**Board:**` line; a plan in a lane has no board of its own. When a lane starts, its orchestrator posts a final comment on each existing plan board of its plans, pointing to the lane board, and closes it; those boards stay as history. Find one with `gh api "search/issues?q=repo:banodoco/astrid-dev+is:issue+is:open+in:title+%22board:+release+<N>%22"` (REST; `gh issue list` fails in Claude sessions), or `board: lane <lane>` for a lane (`python3 scripts/boards.py roster <N>` lists both), or create it with the header block ([format](../guides/codex-cloud/README.md#establish-the-mailbox)).
2. **Where to post.** Your own updates go on your own board. A message about a plan in a lane goes on the lane's board; a message about a plan outside a lane goes on that plan's board. A Lead-to-Lead or release-wide message goes on the Lead's board. Reply where the message was posted.
3. **Chain.** The Lead addresses orchestrators. An orchestrator addresses its manager. A manager relays to packet sessions. Peer orchestrators may post on each other's boards about shared code.
4. **One home per ruling.** Four homes, by reach: release-wide rulings in the release's `run.md` "Standing rulings"; a lane's rulings in its brief's Standing rulings; a ruling that holds beyond the release in the skill or role document; and a decision about one task in that plan's `tasks.md` (its row or decision log), which is not a ruling. Never in `Run start`, a launch or the board alone. A board DECISION states the ruling and links its home. A lane ruling can never widen the brief's Owner only or How it runs; an entry that tries to is void.
5. **Hourly update.** Leads, orchestrators and managers post one STATUS an hour on their own board, in 10 lines or fewer ("no change" is one line). It lists what was acted on since the last update, which replaces standalone ACKs. Packets post only milestones: early STATUS, READY-*, BLOCKED and DONE. Post each message once, to one addressee.
6. **Read by cursor.** Read your board with `inbox.py --after <cursor>` ([usage](../guides/codex-cloud/inbox.py)), putting the cursor in your STATUS. Read your parent's board for messages addressed to you. Re-read `run.md` Standing rulings only when it has a newer commit.
7. **Waking and urgency.** Every Claude role and every manager creates its own hourly scheduled task at start-up, at a minute other than :30, checks that it fires, and never disables another session's task. A Claude cloud session also keeps a keep-awake loop. `send_message` is a Claude-to-Claude doorbell for what can't wait an hour. ChatGPT sessions post BLOCKED instead.
8. **Liveness.** A parent checks each child's last post and branch movement. Nudge at 2 hours; tell the owner at 3 hours. See who is where: `python3 scripts/boards.py roster <N>`.

## Checks and failure repair

Locally, run only explicitly scoped, feature-focused test runs; never broad, auto-discovered, repository-wide, full affected, or opt-in suites. The full relevant suite runs on hosted CI, only at the moments the [table below](#when-a-test-run-is-load-bearing) names ([how](workstreams/green.md#using-github-actions)). Pure planning and research do not execute product checks unless specifically requested. Editing planning documents or check code still requires the appropriate local documentation validators and focused unit tests before submitting a PR; that validation is not permission to execute product tests. Use a documented narrow command/selector grounded in the current repository and task; do not invent test names, selectors, or commands.

Record each proof's exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status and diagnostic output, result, and limitations. Judge the inner build/test/install command, not a wrapper's transport status. Interpret statuses such as 125 or 127 only according to the runner and command's documented semantics; they are not universal meanings. Use `PASS`, `FAIL`, `RETRYING` (infrastructure retry in progress), and `NO-RESULT` (missing evidence). A pass applies only to the exact candidate and inputs it names.

Preserve the initial failure and its exact command/candidate. If a check fails, repair its in-scope cause and rerun that same actual failing check on the repaired candidate. Keep product failures distinct from infrastructure failures. Transient capacity, readiness, network, eviction, or missing-result failures may be retried with the same inputs; invalid requests must be corrected. After two failures with the same signature, do not run unchanged again: first change or diagnose the cause, fixture, environment, or input. Do not mask a failure, replace it with a broader check, or claim an unrun check passed.

Carry proof forward only when its relevant inputs and product/dependency/generated/installed bytes are evidenced unchanged. A changed candidate invalidates only evidence dependent on the change; preserve unaffected passing proof. Protected surfaces and changed relevant inputs require proof for the exact candidate. Accepted scoped checks do not support a claim that an entire repository or suite passed.

**Never edit, skip, loosen, xfail or delete a test, a fixture, an oracle line or a check to get a pass,** in the file or on the command line. If a card would make one untrue and does not list it, the worker stops and reports the exact lines. The manager rules in the same turn and records the before and after in the card's row, and only then may the line change. A pinned test that pins a defect goes to the review or the contract's author, not to the worker.

**Exception, allowed and listed in the PR:** a mechanical test-setup change that keeps every assertion's meaning byte-identical: symbolic SHAs for literals, a permissions helper, setup writes through a shared helper (Release 15 [ruling 6](../../releases/15/run.md#standing-rulings-plans-87-and-89), the forging-step helper). Only a change to an assertion's meaning is BLOCKED; it goes to the orchestrator, who may approve under the delegation in its brief (outside a lane, the owner's).

### When a test run is load-bearing

Run tests at the moments where the result changes a decision, and at no others. A run is load-bearing when someone is about to rely on it:

| Moment | Run | Why it bears load |
| --- | --- | --- |
| **Before the first task** | The plan's test inventory, once, on the starting versions | Without it, a later failure can't be told from one that was already there |
| **After each task** | Only that task's focused proof: the tests that would fail if this task were wrong | It decides whether the task is done |
| **Before others build on it** (a contract, data model, shared interface or security boundary lands, or a chain hands over to a different worker) | The tests that cover that shared part | A mistake found later means redoing every task built on it |
| **Before review, and before anything reaches `main` or users** | The full relevant suite, once, on the integrated head, on CI | It is the last point where a failure is cheap |

Not load-bearing, so skip it: a broad suite after every task; re-running a proof whose inputs have not changed (carry it forward); a test with no baseline to compare against; a run whose result nobody will act on. A **regression** is a test that ran and passed on a baseline and fails on the candidate. A test that is absent, skipped or uncollected on every baseline has no baseline, so it is not a regression; it is fixed only if this run added it. A test this run added that fails on the candidate blocks like a regression: fix it, or leave the test out of the candidate and give it a row in its repository's green-mains plan ([Plan 91](../../plans/91-agent-main-green/plan.md) for the Agent, [Plan 39](../../plans/39-green-mains/plan.md) for the Runtime and the App). [`env/baseline-diff.py`](../../env/README.md) (`astrid-baseline-diff`) sorts results by this rule; don't sort by hand. After each load-bearing run, compare with the baseline by this rule and fix only what is new. For a merge or a rebuild onto another branch, the baseline is the branch you merged onto, not the one you came from, and the test scope is every test file that touches a changed module, on both, not a focused subset: a clean textual merge can still break (one side deletes a file the other starts reading), and the old branch's existing failures hide it.

**One exception, by cost:** when the whole inventory runs in seconds, run all of it at every moment above. The table exists to ration expensive runs, not to justify skipping cheap ones.

A plan names its load-bearing moments in `tasks.md`: the test inventory, each task's focused proof, and any join that needs the shared part re-proven.

In astrid-dev itself, run `python3 scripts/astrid_dev.py check` before every commit, merge and pull request. It checks structure and links in seconds, so the cost exception applies.

## Review and promotion boundaries

Review rounds are proportional, not a default ritual: where the accepted plan sets any, end with them on the integrated candidate. **Per card, a high-judgment review runs only for:** an `S` card; a change to what the product accepts, refuses or publishes (an integrity rule, a fence, a contract); or code brought in that a review has already judged unsound. Every other card, `N` or `X` (tests, fixtures, tooling, measurement, ordinary fixes), is proved by its own focused tests and waits for the final round. An early review costs a round now to save untangling later; spend it only where a late finding would be expensive. An accepted plan may also set a review stop after a load-bearing part (see the [plan skill](workstreams/plan.md#write-the-task-list)); a stop follows this same protocol on that part's integrated result, with its own agreed rounds, and the tasks built on it wait for it. The final review always runs after required scoped checks and before publishing or closing, by the `completion_reviewer`. The plan records how many rounds at most: the planner recommends a number from risk and complexity (as a guide, 0 for a simple, bounded project where ordinary PR review is enough; 1 for meaningful complexity; 2 or 3 only for cross-repository, release, security or data work) and the owner agrees. Each finding comes back as a task card (outcome, route, scope, dependencies, focused proof) and is done before the next round. Stop after a round with no blocking findings; a blocking finding still open after the last agreed round goes straight to the orchestrator, who rules under the owner's delegation or takes it to the owner; in a lane, the orchestrator rules under its brief and brings the owner only what the brief's Owner only lists. A run with no orchestrator takes it to the owner. Do not pass with an unresolved blocking finding. Preserve an existing run's exact accepted review scope, stage, candidate, remaining rounds, and consumed count; never add stages, reset counts, silently change the reviewed candidate, or ask for sign-off after every task. Planning-only runs have no active review stage by default.

An iterate result is a feature candidate, not an integrated or promoted result. Its author does not integrate, independently review, promote or publish it, or claim that any of these happened. The release workflow alone integrates and rechecks the candidate and performs only the authorized promotion/publication. When integrated proof fails, route the repair to the same iterate loop, then recheck the integrated candidate. Advice does not waive a review or authorize execution/publication. Ask the owner only for a real authority, scope, or unresolved consequential choice.

## Run template

Copy [run template](templates/run.yaml) into a new run and fill the exact runtime model IDs, supported reasoning efforts, and availability before dispatch. Its class labels are illustrative only. Map role keys to configured model entries in `roles`; do not create a second binding source. A template is planning-only and does not initialize, reset, or authorize any existing run.
