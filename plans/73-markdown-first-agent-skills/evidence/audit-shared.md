# MSC-4 — Shared rule-preservation audit

P73-05 / MSC-4. Source M: `2761114f93452d7c3110b71a9b55a5d4dc36490d`; gap source (INT): `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8`. Audited project base: `090c3f87a0b40cadd6b7587847ff9b57a277407b`. Decision: https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7154906536.

Each table uses one row per consequential rule unit (closely coupled requirements grouped; independent constraints split). Quotes are contiguous excerpts of rendered source wording, at most 25 words; a line reference includes the entire carrying clause even where the quote is abbreviated. Source line numbers are pinned to M except the gap pair. Agent line numbers refer to the audited project base unless explicitly stated. Read-only comparisons normalized Markdown link destinations and heading formatting, not rule words; semantic review also accounts for relocated contracts and superseded layout mechanics. Link-target verification and rewrite belong to MSC-6. Existing policy tensions are not resolved here. No proof was executed by the packet.

## Run contract

Source: `skills/shared/run-contract.md`; destination: `agent/shared/run-contract.md`. The heading texts are unchanged. All nonblank source lines except the two legacy source-region markers occur with the same wording in the new document (allowing link-target rebasing). The two markers are separately accounted for.

### Routing and bindings

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| This is the single policy owner for run identity, routing, focused proof, failure repair, carry-forward, review budget, and authority. | L3 | L7 | kept |
| The entrypoint and role guides link here instead of maintaining competing policy copies. Terms follow the glossary. | L3 | L7 | kept |
| Use `N` for everything below very hard, including ordinary hard work; | L7 | L11 | kept |
| `X` for very hard work with coupled or non-obvious reasoning; | L7 | L11 | kept |
| `S` for super-hard work where deeper reasoning materially improves correctness; and | L7 | L11 | kept |
| `T` for taste work: small, editorial refinement where the quality is a matter of judgment. | L7 | L11 | kept |
| `N` is the default; tag a task `X`, `S` or `T` only when it clearly needs that depth. | L7 | L11 | kept |
| These labels describe capability bands, not exact model identities. | L7 | L11 | kept |
| Configure actual available model IDs, supported reasoning efforts, availability, and role bindings in that run's `run.yaml`. | L7 | L11 | kept |
| A role resolves through the binding in `run.yaml` to a model entry's exact `model_id` and `reasoning_effort`; | L7 | L11 | kept |
| do not infer availability from a class label, invent IDs, or silently substitute. | L7 | L11 | kept |
| Resolve unavailability explicitly. | L7 | L11 | kept |
| Plan/advisor/reviewer judgment bindings are configured separately from execution routes. | L7 | L11 | kept |
| using the newest available model of that family: | L10 | L13 | kept |
| `N` \| Everything below very hard, including ordinary hard work: research, reading, running checks, most changes and fixes \| Haiku \| Luna \| | L14 | L17 | kept |
| `X` \| Very hard: intricate changes, subtle bugs, coupled or non-obvious reasoning \| Sonnet \| Terra \| | L15 | L18 | kept |
| `S` \| Super hard: deep design, or correctness that needs the deepest reasoning \| Opus \| Sol \| | L16 | L19 | kept |
| `T` \| Taste: small, editorial refinement of something that already exists, such as user-facing copy, error and refusal messages, names, a screen's layout or a … | L17 | L20 | kept |
| Reviews, plan judgment and advice use a separate high-judgment role: Opus (Claude) or Astra (Codex); | L19 | L22 | kept |
| configure it in run.yaml as `completion_reviewer`, `plan_judgment` and `advisor`. | L19 | L22 | kept |
| A review's verdict runs on the high-judgment role. | L21 | L24 | kept |
| A check of a bounded fix against a named oracle (its failing case or probe) may run on `X`. | L21 | L24 | kept |
| `N` may gather facts for a review (check status, failure IDs, diff scope) but never gives the verdict. | L21 | L24 | kept |
| Check a pure sync by tree equality. | L21 | L24 | kept |
| A bounded-fix check runs the focused tests on both base and head. | L21 | L24 | kept |
| A bounded-fix check goes to the high-judgment role only when its own tests cannot show it is right (see the per-card rule under review and … | L21 | L24 | kept |
| size alone is not a reason. | L21 | L24 | kept |
| A meter, gate or check is reviewed by injecting the failures it must catch. | L21 | L24 | kept |
| The run names the actual reviewer model, flags and permissions where it records its bindings (`run.yaml`, or the run board for a dispatch run). | L21 | L24 | kept |
| This table and the high-judgment role below it are the only place in the skills, docs and templates that defines model families; | L24 | L26 | kept |
| generated `block:routing` copies carry them where work is handed to a model; | L24 | L26 | kept |
| history records are exempt. | L24 | L26 | kept |
| `templates/run.yaml` and the Codex brief are fill-in copies of them. | L24 | L26 | kept |
| Elsewhere name the route, and a family only when the run used one other than the route's, never an exact model ID. | L24 | L26 | kept |
| When workers are on Codex, `T` work may run on the Codex taste family; Claude is recommended. | L24 | L26 | kept |
| `&lt;!-- block-source:routing:start --&gt;` | L9 | `agent/shared/run-contract.md` L9–26; `agent/shared/workstreams/plan.md` L105–107 links directly, as does `agent/guides/codex-in-claude-cloud/manager-brief.md` L29–31. `scripts/test_skill_builder.py::test_generate_canonical_metadata_and_links` and `test_missing_reference_and_heading_fail_before_mutation` enforce package link/anchor integrity; `scripts/test_views.py::test_real_repository_routing_copies` still tests legacy copies only. No observed check forbids a new competing routing copy in agent Markdown; flag for orchestrator ruling at MSC-6. | superseded |
| `&lt;!-- block-source:routing:end --&gt;` | L22 | `agent/shared/run-contract.md` L9–26; `agent/shared/workstreams/plan.md` L105–107 links directly, as does `agent/guides/codex-in-claude-cloud/manager-brief.md` L29–31. `scripts/test_skill_builder.py::test_generate_canonical_metadata_and_links` and `test_missing_reference_and_heading_fail_before_mutation` enforce package link/anchor integrity; `scripts/test_views.py::test_real_repository_routing_copies` still tests legacy copies only. No observed check forbids a new competing routing copy in agent Markdown; flag for orchestrator ruling at MSC-6. | superseded |

Count: 37 found, 35 kept, 0 restored, 0 moved, 2 superseded.

### ChatGPT session modes

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| When a task runs in a ChatGPT session (ChatGPT web sessions only: a fresh packet session in the dispatch workstream, or a session an orchestrator … | L28 | L30 | kept |
| a Codex manager or worker run by `codex exec` takes its model and effort from the run's bindings, not from this table), | L28 | L30 | kept |
| the session's mode follows the task's route. The owner set this on 23 November 2026: | L28 | L30 | kept |
| `N` \| High \| | L32 | L34 | kept |
| `X` \| Extra High \| | L33 | L35 | kept |
| `S` \| Pro \| | L34 | L36 | kept |
| A packet takes the mode of its hardest card, and its file names it (`Route:`). | L36 | L38 | kept |
| `T` work follows the run's brief; this table sets nothing for it. | L36 | L38 | kept |
| A mode that is not offered on the account is resolved explicitly (the next mode up, or the owner), never silently substituted. | L36 | L38 | kept |
| Moving a card up a route moves its session up a mode, on the same evidence as Cheapest model first. | L36 | L38 | kept |

Count: 10 found, 10 kept, 0 restored, 0 moved, 0 superseded.

### Cheapest model first

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| Judge a task's difficulty before delegating it, start it on the cheapest model that can plausibly do it at that difficulty, and | L40 | L42 | kept |
| move up only on evidence. | L40 | L42 | kept |
| A task with no route tag is `N`. | L40 | L42 | kept |
| A release brief may set a different starting model for its run (for example, a mid-tier default for everything that is not plain fact-finding); follow … | L40 | L42 | kept |
| Start at `N`. Fact-finding, reading, running checks, mechanical edits, and most fixes whose failing test and likely cause are already named go to `N`. | L42 | L44 | kept |
| Give the worker one bounded outcome, the exact files or selectors, and the proof you expect back. | L42 | L44 | kept |
| Escalate one step at a time, on a stated reason. | L43 | L45 | kept |
| Move `N` to `X` after two misses or 20 minutes without progress, or when the returned work is wrong in a way a better brief … | L43 | L45 | kept |
| Move `X` to `S` on the same test. | L43 | L45 | kept |
| Before escalating, ask whether the brief was the problem: a vague brief fails on every model. This threshold is the manager's. | L43 | L45 | kept |
| A worker's is different: it stops after three attempts or 45 minutes without progress on one failure and hands the manager the raw output, what … | L43 | L45 | kept |
| The next model gets the previous attempt's diff, raw output and best guess, so it starts from what was learned, not from zero. | L44 | L46 | kept |
| The manager checks each result against the diff and the proof, never against the worker's summary. | L45 | L47 | kept |
| Decisions, dispositions and reviews stay with the manager or the high-judgment role; they are not delegated down. | L45 | L47 | kept |
| Once a hard problem has a known cause, the remaining edits and reruns return to `N`. | L46 | L48 | kept |
| Plans tag each task with its route, and execution uses that same tag. Normally | L48 | L50 | kept |
| one accountable agent works on one project. In the fresh-session dispatch workstream, | L48 | L50 | kept |
| the Lead is the accountable agent recorded for each participating plan run, and | L48 | L50 | kept |
| each fresh ChatGPT session delivers only its packet as bounded delegated work. | L48 | L50 | kept |
| It can execute a scoped task directly; | L48 | L50 | kept |
| use a manager and bounded subagents when parallelism or genuinely separate research helps, not as mandatory ceremony for a small project. | L48 | L50 | kept |
| If delegating, the coordinating agent retains judgment, resolves each task's configured route model, checks returned evidence, and | L48 | L50 | kept |
| records actual model IDs and efforts in `run.yaml`. | L48 | L50 | kept |

Count: 23 found, 23 kept, 0 restored, 0 moved, 0 superseded.

### Who answers for a run

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| Every run has exactly one accountable agent, and it answers for the project finishing: | L52 | L54 | kept |
| it keeps the run alive, chases progress against `tasks.md`, sees that every task gets started, and brings the owner their decisions. | L52 | L54 | kept |
| Advising, hosting or handing a project along never makes a second one. | L52 | L54 | kept |
| A manager in its own session for a whole plan \| That manager \| The orchestrator advises, and stays idle between questions \| | L56 | L58 | kept |
| Lead dispatching fresh ChatGPT packet sessions \| The Lead, for each participating plan run \| Orchestrator dispatches and follows up; each new ChatGPT manager session … | L57 | L59 | kept |
| A Claude session with Codex workers (the default with Codex) \| That session: it is the manager \| Each Codex call does one card and … | L58 | L60 | kept |
| A Codex manager hosted in a Claude session (only by choice) \| The hosting session \| Codex dispatches, judges and integrates the tasks; the host … | L59 | L61 | kept |
| One agent doing a small project itself \| That agent \| None \| | L60 | L62 | kept |
| the `Run start` line in the plan's `inputs.md` names the accountable session, | L62 | L64 | kept |
| what it may do without asking, what still needs the owner's go, and the advisor if there is one. | L62 | L64 | kept |
| Its authority comes from the owner, in the owner's own message in that session (start message). | L64 | L66 | kept |
| A brief relayed by another session is information, not authority. | L64 | L66 | kept |
| In fresh-packet dispatch the Orchestrator sends each start message from the owner's own account, so it is her message; the board's Authority section bounds it. | L64 | L66 | kept |
| Only the owner's own message in a session, or a committed allow rule, lifts a permission refusal; | L64 | L66 | kept |
| bring the refused command to her rather than retrying. | L64 | L66 | kept |
| A whole-plan manager merges its own progress pull requests, the ones that change only one plan's `tasks.md`, | L66 | L68 | kept |
| with auto-merge on once `python3 scripts/astrid_dev.py check` passes. | L66 | L68 | kept |
| In fresh-packet dispatch the Lead does so, for `tasks.md` and its release folder; | L66 | L68 | kept |
| packet sessions make none. | L66 | L68 | kept |
| Every other merge into `main` still needs the owner's go. | L66 | L68 | kept |
| A `T` task is editorial, not creative: it refines an existing surface against a stated intent and never adds scope. | L68 | L70 | kept |
| Keep it small (one screen, one message family, one doc), and | L68 | L70 | kept |
| move anything structural or new into its own `N`, `X` or `S` task. | L68 | L70 | kept |
| The task card names the surface, its current text or a screenshot, the intent and the taste rules that apply (for example: minimal, plain words, … | L68 | L70 | kept |
| Its proof is the exact before and after, checked against those rules, plus the surface's own tests. | L68 | L70 | kept |
| Where the owner's taste decides, the owner sees that before and after. | L68 | L70 | kept |
| The `T` lead makes the edits itself and may delegate only mechanical checks. | L68 | L70 | kept |
| An `X` or `S` execution lead always delegates bounded research, reading, mechanical edits and running checks to `N` helpers, and | L70 | L72 | kept |
| keeps the judgment and the final change itself. | L70 | L72 | kept |
| Reviewers and leaf advisors do not inherit that requirement. | L70 | L72 | kept |
| A plan may name route labels but must not duplicate model bindings. | L70 | L72 | kept |

Count: 31 found, 31 kept, 0 restored, 0 moved, 0 superseded.

### Actual route provenance

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| Plan and role bindings in `run.yaml` are not proof of what ran. | L74 | L76 | kept |
| At each meaningful planning, research, implementation, testing or review invocation, record the route (`N`, `X` or `S`), role and task. | L74 | L76 | kept |
| Add `--override &lt;name&gt;` only where the run used a model other than the route's. | L74 | L76 | kept |
| Never put exact model IDs in PRs or other repository artifacts. | L74 | L76 | kept |
| The local `model-usage.jsonl` is under gitignored `.otto/`; | L82 | L84 | kept |
| do not publish raw logs. | L82 | L84 | kept |
| Copy the `Routes used:` line into the review submission, or write `Unknown — &lt;reason&gt;`. | L82 | L84 | kept |
| A manual log is reporting, not authentication. | L82 | L84 | kept |

Count: 8 found, 8 kept, 0 restored, 0 moved, 0 superseded.

### Scope, source identity, and state

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| An astrid-dev-only plan may be started without release membership only on the owner's explicit instruction, following Manage's dev-only project route. | L86 | L88 | kept |
| This does not loosen review, protected `main` merges, permission checks, evidence requirements or any product-repository release gate. | L86 | L88 | kept |
| A skill installation, plan, or run template does not authorize product execution or publication. | L88 | L90 | kept |
| Follow the repository's pause and stop instructions (a paused status, or a plan or brief that says stop) and its accepted plan. | L88 | L90 | kept |
| Do not start, resume, or broaden product work without its explicit authority. | L88 | L90 | kept |
| For a new run, keep control artifacts at `&lt;project&gt;/.otto/runs/&lt;run-id&gt;/`; | L90 | L92 | kept |
| inspect and resume a matching existing run first. | L90 | L92 | kept |
| Record the actual source repository, ref and SHA, dirty state, custody, and destination branch (the plan or fix branch the work lands on); | L90 | L92 | kept |
| separately identify each dependency and its ref/SHA/dirty state and role. | L90 | L92 | kept |
| Preserve user changes and distinguish the current base from dependency inputs. | L90 | L92 | kept |
| If identity or custody conflicts with the assignment, stop dependent mutation and resolve the discrepancy. | L90 | L92 | kept |
| Each assignment names its outcome, in-scope behavior/paths, dependencies, source identity, route, and focused acceptance evidence. | L90 | L92 | kept |
| Keep only the recovery state needed to resume: goal, ready tasks/dependencies, candidate identity, completed/blocked tasks, failures, evidence, consumed review rounds, and next action. | L92 | L94 | kept |
| Do not add an acceptance-ledger or document framework without a concrete need. | L92 | L94 | kept |
| Continue independent work when another task is blocked. | L92 | L94 | kept |
| Never reset accepted run choices, budgets, evidence, or program state because guidance changed. | L92 | L94 | kept |
| Add commits only: never rebase, amend or force-push, even on your own branch. | L94 | L96 | kept |
| To bring in a newer base, merge it in. | L94 | L96 | kept |
| Never rewrite a contributor's branch. | L94 | L96 | kept |
| Never read or print `.env` files, `~/.codex` or any credential or token file. | L94 | L96 | kept |
| A saved credential reaches every process in the environment, tests and workers included: keep it in an environment of its own, | L94 | L96 | kept |
| stub every test that would call the real provider, and | L94 | L96 | kept |
| keep paid or credentialed steps with the manager. | L94 | L96 | kept |
| Before a run pauses or ends, release every rented machine it made, and say which, whatever happened (steps). | L94 | L96 | kept |

Count: 24 found, 24 kept, 0 restored, 0 moved, 0 superseded.

### Decisions ledger when the owner is unavailable

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| When work proceeds without the owner (for example, a contributor or agent helping while the owner is offline or out of quota), keep a decisions … | L98 | L100 | kept |
| Record any proposed change to the written plan, | L98 | L100 | kept |
| an in-scope best guess where it is silent, | L98 | L100 | kept |
| any stop-and-ask decision awaiting authority (such as a conflict where both sides change one statement), | L98 | L100 | kept |
| the trajectory inferred, and improvements not built. | L98 | L100 | kept |
| Include evidence, the candidate SHA when one exists, and how to revert. | L98 | L100 | kept |
| A provisional proposal is never permission to execute work outside the accepted scope or bypass a stop. This is the concrete need the paragraph above … | L98 | L100 | kept |
| A ledger entry is never authorization: stop-and-ask boundaries remain stops, and anything that lands still needs the owner's go. | L98 | L100 | kept |

Count: 8 found, 8 kept, 0 restored, 0 moved, 0 superseded.

### Coordination: boards and check-ins

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| One astrid-dev issue per plan or run, titled `board: release &lt;N&gt; plan &lt;P&gt;` (or `&lt;name&gt;`), | L102 | L104 | kept |
| and one per release Lead, titled `board: release &lt;N&gt; lead`. | L102 | L104 | kept |
| Find one with `gh api "search/issues?q=repo:banodoco/astrid-dev+is:issue+is:open+in:title+%22board:+release+&lt;N&gt;%22"` (REST; `gh issue list` fails in Claude sessions), or create it with the header block (format). | L102 | L104 | kept |
| Your own updates go on your own board. | L103 | L105 | kept |
| A message about a plan goes on that plan's board. | L103 | L105 | kept |
| A Lead-to-Lead or release-wide message goes on the Lead's board. | L103 | L105 | kept |
| Reply where the message was posted. | L103 | L105 | kept |
| The Lead addresses orchestrators. | L104 | L106 | kept |
| An orchestrator addresses its manager. | L104 | L106 | kept |
| A manager relays to packet sessions. | L104 | L106 | kept |
| Peer orchestrators may post on each other's boards about shared code. | L104 | L106 | kept |
| Release-wide rulings live in the release's `run.md` "Standing rulings"; | L105 | L107 | kept |
| plan rulings live in that plan's section. | L105 | L107 | kept |
| A board DECISION states the ruling and links its home. | L105 | L107 | kept |
| Leads, orchestrators and managers post one STATUS an hour on their own board, in 10 lines or fewer ("no change" is one line). | L106 | L108 | kept |
| It lists what was acted on since the last update, which replaces standalone ACKs. | L106 | L108 | kept |
| Packets post only milestones: early STATUS, READY-*, BLOCKED and DONE. | L106 | L108 | kept |
| Post each message once, to one addressee. | L106 | L108 | kept |
| Read your board with `inbox.py --after &lt;cursor&gt;` (usage), putting the cursor in your STATUS. | L107 | L109 | kept |
| Read your parent's board for messages addressed to you. | L107 | L109 | kept |
| Re-read `run.md` Standing rulings only when it has a newer commit. | L107 | L109 | kept |
| Every Claude role and every manager creates its own hourly scheduled task at start-up, at a minute other than :30, | L108 | L110 | kept |
| checks that it fires, and | L108 | L110 | kept |
| never disables another session's task. | L108 | L110 | kept |
| A Claude cloud session also keeps a keep-awake loop. | L108 | L110 | kept |
| `send_message` is a Claude-to-Claude doorbell for what can't wait an hour. | L108 | L110 | kept |
| ChatGPT sessions post BLOCKED instead. | L108 | L110 | kept |
| A parent checks each child's last post and branch movement. | L109 | L111 | kept |
| Nudge at 2 hours; tell the owner at 3 hours. | L109 | L111 | kept |
| See who is where: `python3 scripts/boards.py roster &lt;N&gt;`. | L109 | L111 | kept |

Count: 30 found, 30 kept, 0 restored, 0 moved, 0 superseded.

### Checks and failure repair / load-bearing moments

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| Locally, run only explicitly scoped, feature-focused test runs; | L113 | L115 | kept |
| never broad, auto-discovered, repository-wide, full affected, or opt-in suites. | L113 | L115 | kept |
| The full relevant suite runs on hosted CI, only at the moments the table below names (how). | L113 | L115 | kept |
| Pure planning and research do not execute product checks unless specifically requested. | L113 | L115 | kept |
| Editing planning documents or check code still requires the appropriate local documentation validators and focused unit tests before submitting a PR; | L113 | L115 | kept |
| that validation is not permission to execute product tests. | L113 | L115 | kept |
| Use a documented narrow command/selector grounded in the current repository and task; do not invent test names, selectors, or commands. | L113 | L115 | kept |
| Record each proof's exact command, candidate SHA/tree, relevant inputs/environment, actual inner command status and diagnostic output, result, and limitations. | L115 | L117 | kept |
| Judge the inner build/test/install command, not a wrapper's transport status. | L115 | L117 | kept |
| Interpret statuses such as 125 or 127 only according to the runner and command's documented semantics; they are not universal meanings. | L115 | L117 | kept |
| Use `PASS`, `FAIL`, `RETRYING` (infrastructure retry in progress), and `NO-RESULT` (missing evidence). | L115 | L117 | kept |
| A pass applies only to the exact candidate and inputs it names. | L115 | L117 | kept |
| Preserve the initial failure and its exact command/candidate. | L117 | L119 | kept |
| If a check fails, repair its in-scope cause and rerun that same actual failing check on the repaired candidate. | L117 | L119 | kept |
| Keep product failures distinct from infrastructure failures. | L117 | L119 | kept |
| Transient capacity, readiness, network, eviction, or missing-result failures may be retried with the same inputs; | L117 | L119 | kept |
| invalid requests must be corrected. | L117 | L119 | kept |
| After two failures with the same signature, do not run unchanged again: first change or diagnose the cause, fixture, environment, or input. | L117 | L119 | kept |
| Do not mask a failure, replace it with a broader check, or claim an unrun check passed. | L117 | L119 | kept |
| Carry proof forward only when its relevant inputs and product/dependency/generated/installed bytes are evidenced unchanged. | L119 | L121 | kept |
| A changed candidate invalidates only evidence dependent on the change; preserve unaffected passing proof. | L119 | L121 | kept |
| Protected surfaces and changed relevant inputs require proof for the exact candidate. | L119 | L121 | kept |
| Accepted scoped checks do not support a claim that an entire repository or suite passed. | L119 | L121 | kept |
| Never edit, skip, loosen, xfail or delete a test, a fixture, an oracle line or a check to get a pass, in the file or … | L121 | L123 | kept |
| If a card would make one untrue and does not list it, the worker stops and reports the exact lines. | L121 | L123 | kept |
| The manager rules in the same turn and records the before and after in the card's row, and only then may the line change. | L121 | L123 | kept |
| A pinned test that pins a defect goes to the review or the contract's author, not to the worker. | L121 | L123 | kept |
| a mechanical test-setup change that keeps every assertion's meaning byte-identical: symbolic SHAs for literals, a permissions helper, setup writes through a shared helper (Release 15 … | L123 | L125 | kept |
| Only a change to an assertion's meaning is BLOCKED; it goes to the orchestrator, who may approve under the Lead's delegation. | L123 | L125 | kept |
| Run tests at the moments where the result changes a decision, and at no others. | L127 | L129 | kept |
| A run is load-bearing when someone is about to rely on it: | L127 | L129 | kept |
| Before the first task \| The plan's test inventory, once, on the starting versions \| Without it, a later failure can't be told from one … | L131 | L133 | kept |
| After each task \| Only that task's focused proof: the tests that would fail if this task were wrong \| It decides whether the task … | L132 | L134 | kept |
| Before others build on it (a contract, data model, shared interface or security boundary lands, or a chain hands over to a different worker) \| … | L133 | L135 | kept |
| Before review, and before anything reaches `main` or users \| The full relevant suite, once, on the integrated head, on CI \| It is the … | L134 | L136 | kept |
| Not load-bearing, so skip it: a broad suite after every task; | L136 | L138 | kept |
| re-running a proof whose inputs have not changed (carry it forward); | L136 | L138 | kept |
| a test with no baseline to compare against; | L136 | L138 | kept |
| a run whose result nobody will act on. | L136 | L138 | kept |
| A regression is a test that ran and passed on a baseline and fails on the candidate. | L136 | L138 | kept |
| A test that is absent, skipped or uncollected on every baseline has no baseline, so it is not a regression; it is fixed only if … | L136 | L138 | kept |
| A test this run added that fails on the candidate blocks like a regression: fix it, or | L136 | L138 | kept |
| leave the test out of the candidate and give it a row in its repository's green-mains plan (Plan 91 for the Agent, Plan 39 for … | L136 | L138 | kept |
| env/baseline-diff.py` (`astrid-baseline-diff`) sorts results by this rule; don't sort by hand. | L136 | L138 | kept |
| After each load-bearing run, compare with the baseline by this rule and fix only what is new. | L136 | L138 | kept |
| For a merge or a rebuild onto another branch, the baseline is the branch you merged onto, not the one you came from, and | L136 | L138 | kept |
| the test scope is every test file that touches a changed module, on both, not a focused subset: a clean textual merge can still break … | L136 | L138 | kept |
| when the whole inventory runs in seconds, run all of it at every moment above. The table exists to ration expensive runs, not to justify … | L138 | L140 | kept |
| A plan names its load-bearing moments in `tasks.md`: the test inventory, each task's focused proof, and any join that needs the shared part re-proven. | L140 | L142 | kept |
| In astrid-dev itself, run `python3 scripts/astrid_dev.py check` before every commit, merge and pull request. It checks structure and links in seconds, so the cost exception … | L142 | L144 | kept |

Count: 50 found, 50 kept, 0 restored, 0 moved, 0 superseded.

### Review and promotion boundaries

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| Review rounds are proportional, not a default ritual: where the accepted plan sets any, end with them on the integrated candidate. | L146 | L148 | kept |
| Per card, a high-judgment review runs only for: an `S` card; | L146 | L148 | kept |
| a change to what the product accepts, refuses or publishes (an integrity rule, a fence, a contract); | L146 | L148 | kept |
| or code brought in that a review has already judged unsound. | L146 | L148 | kept |
| Every other card, `N` or `X` (tests, fixtures, tooling, measurement, ordinary fixes), is proved by its own focused tests and waits for the final round. | L146 | L148 | kept |
| An early review costs a round now to save untangling later; spend it only where a late finding would be expensive. | L146 | L148 | kept |
| An accepted plan may also set a review stop after a load-bearing part (see the plan skill); | L146 | L148 | kept |
| a stop follows this same protocol on that part's integrated result, with its own agreed rounds, and the tasks built on it wait for it. | L146 | L148 | kept |
| The final review always runs after required scoped checks and before publishing or closing, by the `completion_reviewer`. | L146 | L148 | kept |
| The plan records how many rounds at most: the planner recommends a number from risk and complexity (as a guide, 0 for a simple, bounded … | L146 | L148 | kept |
| and the owner agrees. | L146 | L148 | kept |
| Each finding comes back as a task card (outcome, route, scope, dependencies, focused proof) and is done before the next round. | L146 | L148 | kept |
| Stop after a round with no blocking findings; | L146 | L148 | kept |
| a blocking finding still open after the last agreed round goes straight to the orchestrator, who rules under the owner's delegation or takes it to … | L146 | L148 | kept |
| a run with no orchestrator, or under fresh-packet dispatch, takes it to the owner. | L146 | L148 | kept |
| Do not pass with an unresolved blocking finding. | L146 | L148 | kept |
| Preserve an existing run's exact accepted review scope, stage, candidate, remaining rounds, and consumed count; | L146 | L148 | kept |
| never add stages, reset counts, silently change the reviewed candidate, or ask for sign-off after every task. | L146 | L148 | kept |
| Planning-only runs have no active review stage by default. | L146 | L148 | kept |
| An iterate result is a feature candidate, not an integrated or promoted result. | L148 | L150 | kept |
| Its author does not integrate, independently review, promote or publish it, or claim that any of these happened. | L148 | L150 | kept |
| The release workflow alone integrates and rechecks the candidate and performs only the authorized promotion/publication. | L148 | L150 | kept |
| When integrated proof fails, route the repair to the same iterate loop, then recheck the integrated candidate. | L148 | L150 | kept |
| Advice does not waive a review or authorize execution/publication. | L148 | L150 | kept |
| Ask the owner only for a real authority, scope, or unresolved consequential choice. | L148 | L150 | kept |

Count: 25 found, 25 kept, 0 restored, 0 moved, 0 superseded.

### Run template

| Rule (source excerpt) | Source line | Agent line or replacement | Status |
| --- | --- | --- | --- |
| Copy run template into a new run and fill the exact runtime model IDs, supported reasoning efforts, and availability before dispatch. Its class labels are … | L152 | L154 | kept |
| Map role keys to configured model entries in `roles`; | L152 | L154 | kept |
| do not create a second binding source. | L152 | L154 | kept |
| A template is planning-only and does not initialize, reset, or authorize any existing run. | L152 | L154 | kept |

Count: 4 found, 4 kept, 0 restored, 0 moved, 0 superseded.

Run-contract total: 250 found, 248 kept, 0 restored, 0 moved, 2 superseded. The Step 1 sample was a provisional count (172); the final count is the enumerated rows, including finer-grained clauses and the two markers.

