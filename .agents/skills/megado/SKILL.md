---
name: megado
description: "Plan and deliver substantial work with subagent-first execution, explicit coordinator/oracle roles, delegated exploration and implementation, and bounded evidence-based review. Use when the user requests Megado or a coordinated plan/execution run; supports planning-only work."
---

# Megado

**Subagent-first execution is the default. All substantive work belongs in delegated subagents: research, planning input, implementation, test execution, debugging, validation, review, and artifact generation. The coordinator orchestrates, writes mechanical briefs and run records, collects evidence, and routes decisions; it does not personally perform substantive work when a subagent route exists. The designated oracle owns consequential judgment, except that an explicitly appointed coordinator/oracle dual-role agent may coordinate and adjudicate within those two assigned responsibilities. Deliver the smallest complete outcome that preserves required behavior. Test continuously, review proportionately, and add process only for a concrete risk.**

The coordinator may read enough authoritative state to formulate a brief and may make mechanical updates to run-control artifacts, but it must delegate any work that changes a technical conclusion, source artifact, test result, validation result, or product decision. If a task can be assigned to a subagent, assign it rather than doing it inline. This rule applies in planning-only and delivery modes alike; reviewers and the oracle are independent subagents by default, except when the run explicitly appoints one agent to both coordinator and oracle responsibilities.

User instructions, including planning-only scope and review overrides, control the run. Do not turn a discussion of a desirable future capability into an implementation obligation. Do not require the user to override default role assignments to retain their chosen judgment owner.

## Choose the mode

- **Planning only:** inspect, explore and produce a concrete plan/tasklist with decisions, uncertainties, estimate and validation approach. Stop there. No execution tests, implementation worktree, deployment preparation, certification packet or independent contract review is required merely to plan.
- **Delivery:** plan enough to execute, implement in the source custody explicitly chosen at kickoff, test and integrate, review under the policy below, then sync only as authorized. Read [execution mechanics](references/execution.md) before source mutation or executable certification.
- **Unattended/cloud delivery:** also read [AgentBox handoff](references/agentbox.md) when a cloud handoff is actually needed. Do not load or perform cloud setup for ordinary planning.

For a plan-only source inspection, record the repository/ref and dirty state, use read-only access, and identify whether uncommitted material is included. A detached snapshot is optional when concurrent changes make the source ambiguous. Do not silently exclude authoritative dirty work. Use the run location and structure below for planning as well as delivery; do not create empty execution directories or stage/commit product source for planning.

## Run location and structure

For a new run, set `PROJECT_ROOT` to the invoking repository and `OTTO_DIR` to `$PROJECT_ROOT/.otto/runs/<run-id>/`. The directory is spelled `.otto`. Inspect existing runs first and resume the matching run rather than create a duplicate. Use another control root only when the user explicitly selects one; record it once. Keep architecture/product documents at their existing source paths and link them from the run.

The minimum setup structure is:

```text
.otto/runs/<run-id>/
  run.yaml          # sole model, stage and budget declaration
  northstar.md      # enduring direction
  agent_goal.md     # scope, authority and links
  plan.md           # approach, assumptions and estimate
  tasklist.md       # outcomes, dependencies, routes and proof
  status.md         # mode, counters, source identity and next action
```

Add source-state records, implementation criteria or a launch README only where useful. Create briefs, receipts and evidence directories when actual work produces them; planning-only setup needs no execution scaffolding. Report the canonical run path when handing off.

Control storage and source-branch custody are independent. Before any delivery
mutation, Megado must explicitly ask (or record the user's already-given choice):
work directly on the invoking repository's `main`, or create an isolated
worktree. If a worktree is chosen, it must be inside the relevant repository at
`<repo>/.otto/worktrees/<run-id>/`; never create the execution worktree beside
the repository, in a global pool, or in another checkout. If `main` is chosen,
source edits and tests happen in the invoking checkout and the run's control
artifacts still live under `<repo>/.otto/runs/<run-id>/`. Record the choice and
exact path in `agent_goal.md` and `status.md`, and do not silently switch
custody later. Git ignoring `.otto` is intentional local control storage, not a
reason to relocate it into tracked docs or force-add it. Preserve existing run
state when explicitly relocating a run, update live references, and leave only
one authoritative copy.

## Establish the minimum useful outcome

Before detailing tables, services or batches, write the answers in plain language:

1. What must work for the first useful outcome, and what existing behavior must remain?
2. What is explicitly required now, what can be removed/consolidated, and what is deferred?
3. Which users, data, consumers and deployment constraints actually exist?
4. Which correctness properties cannot be cut, and how can a small backend fixture or experiment demonstrate them?

Simplify implementation and process first; do not silently drop required behavior. Adapting existing search to a changed schema is not permission to redesign it or disable working paths. For an unused/early project, prefer a direct conversion with one relevant inventory/export/rehearsal over shims, dual writes and deprecation machinery—unless actual callers/data justify them. Few users is not permission to destroy data.

Judge every proposed new layer by a current requirement. Prefer a bounded concrete implementation over a generalized graph, workflow/policy engine, parser, storage service or framework. These are examples of scope to justify, not a blacklist. Retain real invariants such as exact revision identity, transactionality and authorization even when implementation is otherwise small.

Estimate the agreed scope in focused engineering days, name major uncertainty and distinguish agent elapsed time. If offering a cheaper milestone, state precisely what it excludes. An estimate, its upper bound, or a two-week threshold never automatically creates review gates.

## Roles and model policy

**Coordinator and oracle are separate responsibilities.** The coordinator runs the agreed process; the oracle owns consequential adjudication. “Host” names the session running the process, not automatic oracle authority. One agent may hold both responsibilities only when the run explicitly assigns both; do not silently transfer authority when delegating coordination. The subagent-first rule applies to the coordinator role: it does not reassign explicitly appointed reviewers or oracle slots. Reviewers, the oracle and other leaf agents do not redelegate; an explicitly appointed coordinator/oracle dual-role agent is the exception to the separate-responsibility default and may coordinate and adjudicate only within those assigned responsibilities. Role slots and model bindings are independent: Luna, Sol and Astra are default model bindings, not roles, and any binding may be replaced in run configuration without changing the responsibility contract.

| Role | Responsibility | Boundary |
| --- | --- | --- |
| Coordinator | Orchestrate the agreed process: draft briefs/plans, dispatch ready work, collect evidence, dispatch prescribed tests and collect results plus mechanical readiness checks, and track stages/counters | Follow the mandate; escalate contested findings, design changes and exceptions |
| Worker | Implement the assigned outcome and report evidence | Propose alternatives; no silent scope changes |
| Reviewer | Verify completion against the assigned scope and evidence; when asked, assess strategic coherence and produce actionable correction tasks | Report source-backed findings; never certify its own implementation, dispatch work, or change scope |
| XHARD reviewer | Apply the reviewer responsibility to harder completion questions that justify the XHARD route | The route changes assignment, not authority or acceptance criteria |
| Final reviewer | Review the whole candidate for completion and strategic coherence | Report findings against the declared contract; recommendations do not automatically change scope |
| Oracle | Adjudicate consequential decisions and contested findings, settling direction and permitted exceptions | Remain within user authorization; never waive demonstrated failure or reset user budgets |

The coordinator may advance on required passing tests and an uncontested stage PASS, or route clear in-scope defects through the prescribed correction path. It must not dismiss a blocker, weaken an acceptance criterion, alter architecture, grant deployment authority or increase budgets on its own. It sends unresolved judgment to the configured oracle. Thus not every reviewer response requires a separate oracle call, and a cheap coordinator need not judge sophisticated disagreements.

**Normal/XHARD routes assignments, not authority.** Normal and XHARD are assignment classifications. Worker and reviewer model bindings are selected independently, and a final reviewer binding is independently replaceable. The default bindings are recorded in the run template; neither a model name nor a strategic lens makes work XHARD. Oracle has one configured slot, not a normal/XHARD hierarchy.

**Normal** suits work with an established approach, mostly local reasoning, and straightforward implementation or verification. **XHARD** suits work where deeper, sustained reasoning is likely to materially improve correctness or avoid costly rework: coupled state/lifecycle behavior, concurrency or timing, cross-component contracts, non-obvious compatibility constraints, or design/debugging with several interacting causes. Name the concrete reasoning challenge; touching several files or being important does not alone qualify.

Assign XHARD proactively when that benefit is clear. It does not require an irreducibility claim, proof that a normal worker cannot succeed, a failed normal attempt, or a lack of effective tests. Decompose where useful so routine work stays normal, but do not exhaust decomposition before routing a coherent reasoning-heavy task to XHARD. Diagnose brief/tool/environment problems on their own merits. A short task-specific rationale is enough for clear routing; request oracle judgment only when classification is genuinely uncertain or disputed. Routing does not change scope, authority, review stages, budgets, or configured model bindings.

**Declare the run once using [the run template](templates/run.yaml).** Copy it to `$OTTO_DIR/run.yaml`, apply its default role slots and model bindings and select meaningful stage triggers, honoring the user's instructions, and link it from agent_goal.md. It is the single model/stage/budget declaration; do not duplicate divergent settings in prose. Read [configuration semantics](references/run-config.md) before creating or changing it. Preserve the keys `coordinator`, `worker_normal`, `worker_xhard`, `reviewer_normal`, `reviewer_xhard`, `oracle` and `final_reviewer`; each key names a responsibility slot whose model/reasoning binding can be replaced independently. The default bindings are GPT-5.6 Luna medium for coordinator, GPT-5.6 Luna XHigh for the normal worker, GPT-6.1 Sol high for XHARD worker and oracle, GPT-6 Astra medium for normal and final reviewers, and GPT-6 Astra high for XHARD reviewer. Use these defaults when no override exists. Megado normally has no numeric oracle-call limit: consult the oracle only for a real blocker, contested judgment, or consequential exception, not for reassurance or routine progress. An explicit run may set a cap when required by its authority or environment. Existing explicit run choices win; do not silently replace them with new defaults. No automatic switch of the current host model or running agents occurs by editing YAML.

The oracle is invoked only for a concrete blocker, consequential new evidence, contested finding, uncertain escalation, or exception that current instructions cannot settle. Routine dispatch, passing tests and uncontested completion do not require reassurance calls. An oracle call is a decision request, not a disguised extra review; “no limit” is not an invitation to consult it continuously.

## Durable direction and run state

Keep a succinct `northstar.md`: desirable end state, enduring properties and anti-patterns. Adopt an existing one where appropriate. Keep `agent_goal.md` linked to it: this run's objective, scope/non-goals, source, user authorization, selected models/review budget, acceptance scenarios, stop criteria and validation/resource limits appropriate to the mode. The North Star supplies direction, not additional authority.

The goal is the current agreed contract, not a reason to freeze a still-forming conversation. Direct user steering authorizes the corresponding update: record what changed and reconcile affected tasks without asking for the same approval again. Do not broaden scope yourself. If documents conflict, use the latest explicit instruction when it resolves the conflict; ask only for a genuine unresolved user decision.

For planning, a plan and tasklist plus concise goal/direction/status are enough. Put criteria, decisions and assumptions in these documents rather than generating a ledger of ledgers. Add `acceptance-ledger.md` for delivery where tracking integrated evidence is useful, not as an independent gate. Keep briefs/findings/receipts when agents run; reuse the run's existing evidence rather than repeating an inventory per reviewer. Execution custody and review identities are in the execution reference.

## Oracle decision requests

Use this lightweight exchange when a worker or delegated coordinator needs the designated oracle's judgment. It is not a new service, scheduled review or requirement to ask about routine work. Proceed under the current brief for ready tasks, prescribed tests and authorized correction patterns. Ask before consequential dependent work when evidence contradicts the plan, alternatives materially affect scope/interfaces/data/authority, findings conflict, or repeated failures undermine the approach. A coordinator may recommend; it cannot grant itself exceptions.

**Persistent oracle conversation:** Default to one resumable oracle conversation per coherent run when the runtime supports it. Bootstrap it with compact project background, the North Star, current goal and authority boundaries, and paths to the authoritative configuration, plan, status and prior decisions. Record its conversation/session identifier and resume mechanism in the existing run notes so a replacement coordinator can continue it. Resume that conversation for consequential follow-ups, supplying the specific decision, changes since the last exchange and exact evidence links instead of repeating the full project context. Routine status lookups and dispatch remain with the coordinator.

Before deciding, the oracle refreshes relevant current state and source/test identities from authoritative artifacts; conversation memory is not evidence that facts are still current. Keep rulings, reasons and return conditions in the existing run notes so the conversation is recoverable. If resumption is unavailable or context becomes unwieldy, start a replacement from those artifacts and a compact handover of unresolved questions and decision rationale. Across runs, carry forward relevant durable decisions and explicitly refresh the mandate rather than depend on one indefinitely growing conversation. Recovery or replacement preserves existing authority and budget counters.

Independent reviewers still use fresh conversations with the declared scope and evidence; the persistent oracle does not replace independent review. If a run declares an oracle cap, each invoked response consumes it; otherwise there is no numeric call budget to exhaust. Persistence changes context delivery, not invocation triggers, authority or review policy.

Keep request and reply together under a stable decision ID in existing run notes (for example a section in status.md). Reuse that ID when revisiting the same question; link deeper evidence rather than paste transcripts.

**Request — answer five questions:**
1. What specific decision is needed?
2. Why cannot current instructions or an existing ruling settle it?
3. What new evidence matters? Link exact source/test identities and any prior ruling.
4. What do you recommend, and what is the main alternative/tradeoff?
5. What work is waiting, and how many times has this same decision returned?

If there is neither a concrete decision nor new evidence, apply the existing ruling instead of requesting reassurance. An uncovered decision may be raised the first time without an experiment; do not fabricate evidence to fill the template. Objective triggers (failed required checks, contract changes, conflicting findings, exhausted correction allowance) supplement self-reported uncertainty—a weaker coordinator may not know it is confused.

**Oracle reply — four fields:**
- Disposition: proceed / change approach / investigate / blocked.
- Decision and reason: concise, grounded in the goal and evidence.
- Next action: a concrete dispatch or bounded investigation; state affected scope. Every executable worker assignment/worker brief, including one for an action unrelated to a review correction, carries the outcome, acceptance evidence, dependency scope, and `normal`/`xhard` route to the corresponding `run.yaml` worker. An XHARD action names the concrete reasoning challenge and expected benefit of deeper reasoning. “Investigate further” must name the uncertainty and evidence sought; unresolved difficulty is not an executable route.
- Return condition: what result or changed circumstance requires another decision; otherwise continue within the mandate.

The reply operates within user authorization; the oracle cannot grant missing deployment/scope authority. Pause only dependent work while a decision is unresolved. Continue independent work. Pause the whole run only if the uncertainty affects overall scope, authority or correctness. “Blocked” identifies the actual prerequisite, not mere discomfort.

**Loop rule:** if the same decision returns twice without new evidence or action, do not reconsider it a third time. Diagnose the coordination failure: ambiguous brief, insufficient mandate, unsuitable worker, tool/environment problem or an approach that needs narrowing. Choose a concrete repair, bounded experiment, decomposition or justified escalation. Ten consecutive checks without substantive progress is a coordination alarm, not diligence; the number of distinct useful decisions alone is not the problem. Preserve prior rulings and review counts. Every oracle interaction should unlock action or reduce a named uncertainty, and these requests must not disguise extra independent review rounds. If an explicit oracle cap is reached, pause only the affected decision and request authority; do not self-adjudicate or rename calls. If no cap is configured, continue consulting only while each call addresses a new blocker or consequential decision. If the oracle requests a review, that review also consumes the applicable stage budget.

## Delegation

**SUBAGENT-FIRST RULE — Delegate every substantive task.** This mandate applies to the coordinator role, not as a reassignment of explicitly appointed reviewer or oracle roles. Treat the current session as a coordinator, not an implementer. Dispatch subagents for all exploration, source inspection beyond the minimum needed to brief work, planning analysis, coding, configuration changes, test runs, debugging, validation, documentation drafts, review, and consequential decisions. Use the configured worker, reviewer, or oracle slot that matches the responsibility and route. The coordinator may only perform lightweight orchestration: maintain the tasklist and status, write/assemble briefs, dispatch work, collect and link evidence, reconcile already-authorized results, and make mechanical bookkeeping updates. Do not use the coordinator as a fallback worker merely because a task is small, familiar, or faster to do directly. Leaf agents do not redelegate. If the required subagent runtime is unavailable or cannot honor the declared route, resolve that execution problem before doing substantive work in the coordinator.

> DELEGATION MANDATE — Delegate every substantive investigation, implementation and validation task to the selected workers. The coordinator writes mechanical briefs, dispatches ready work, collects evidence and maintains the agreed state. The oracle owns consequential design and adjudication; the coordinator follows its rulings and requests judgment for ambiguity or exceptions rather than deciding them silently. Workers may propose alternatives, not widen scope. Do not delegate merely to manufacture another verdict or force tiny coordination/document updates through a worker. Normal workers execute their task; reviewers, oracle advisers and other leaf agents do not redelegate. The explicitly appointed coordinator/oracle dual-role exception may coordinate and adjudicate within its two assigned roles, but does not reassign explicitly appointed reviewers or change reviewer routing.

Include this mandate in execution-capable manager briefs, not in leaf worker/reviewer briefs. Give each dispatch the complete succinct North Star, applicable goal/task constraints, current source identity and required evidence. Record actual model, command/tool, source, brief/result paths and digests, timing and exit status without secrets. A plan-only read-only fact check does not need execution-capable permissions.

If the North Star or agreed goal changes, record the authoritative user instruction and updated digest; reconcile affected tasks and briefs before dispatch. Map changed criteria to their previous IDs and invalidate only affected evidence/approvals. Preserve unaffected results and existing review counters; do not silently give queued work a different contract. An adopted North Star records its source path and digest.

## Explore and form the plan

The coordinator assembles the plan from delegated findings and identifies uncertainties; the oracle settles unresolved consequential direction. Delegate narrow questions when the answer could change scope, implementation or proof. Good explorations locate the active dependency closure, distinguish facts from assumptions, identify reusable mechanisms and test whether an adjacent abstraction can disappear. Return conclusions with file/line evidence; keep bulk output outside the host context.

**Factual exploration is not a review round.** Additional cheap fact checks may be worthwhile after an initial fan-out; no arbitrary wave quota or new permission is needed within authorized time/cost/scope. Give each one a named unresolved question. Stop when another answer would not change a decision; do not run repeated general audits in pursuit of certainty. Expensive, live or mutating experiments still obey their authorization/budget.

The coordinator incorporates factual findings within the mandate and sends consequential choices to the oracle. Optional Sol/Grok planning advice is for a concrete difficult question; it is not a mandatory plan/revise/STABLE ceremony. No reserved empty phase and no requirement for a model to pronounce `STABLE`.

Actively pressure-test complexity while forming a substantial plan: ask normal-model explorers/critics to find unnecessary abstractions, duplicate mechanisms and handoffs, and propose concrete deletions, consolidation or reuse supported by source evidence. Do not use cheap agents only to confirm the proposed architecture. The oracle decides consequential scope cuts; the coordinator applies them while preserving required behavior.

Once coherent, use the smallest useful normal-model simplicity critique if it can improve a substantial plan. Ask what can be cut, merged, reused or deferred without losing the goal. This is discovery, not certification. Bound repeated whole-plan critiques to two rounds by default; later facts do not reset that cap. Local details become tasks or bounded spikes. Do not make a model critique mandatory for a straightforward update to an already agreed plan.

Freeze for execution when the coordinator can explain the complete path to the outcome, material architecture/authority decisions are resolved, and remaining implementation unknowns have an owner/test/spike. “No critic can find another idea” is not a stopping criterion. Optional discoveries go to deferred notes, not new blockers.

## Tasklist and execution

Tasks name their outcome, real dependencies, affected scope, model/classification and acceptance proof. Group at natural integration seams; labels do not create global barriers. The coordinator checks explicit goal/task/authorization agreement and sends ambiguous conflicts to the oracle; an extra independent pre-execution contract review is not the ordinary default.

Every executable worker assignment/worker brief, including a correction dispatched after review, carries
the same compact contract: the concrete outcome, acceptance evidence, source and
dependency scope, and a route of `normal` or `xhard`. The route resolves through
`run.yaml` to `worker_normal` or `worker_xhard`; it is not a new role. An XHARD
worker assignment/worker brief includes a brief justification naming the concrete reasoning challenge and
how deeper reasoning should improve correctness or reduce rework. The coordinator records these
fields in the worker brief/receipt and dispatches to the corresponding configured worker.
This requirement applies to corrections as well as first-pass tasks; it does not
add a gate or an extra model call. This worker-only routing requirement does not
govern reviewer stages, which remain routed through their declared `reviewer_role`.

In planning-only mode, deliver the plan/tasklist, unresolved assumptions and estimate now. Do not proceed into the execution reference's setup or claim future tests have passed.

For delivery, use [execution mechanics](references/execution.md), dispatch unblocked work, and have subagents run focused tests during implementation and converge around coherent source checkpoints. Only dependents of a failed invariant must wait. Batches/checkpoints are for integration and source identity, not automatic model-review gates. The oracle adjudicates material plan changes; user scope/authority cannot be expanded by an executor or reviewer.

## Review policy — one source of truth

Distinguish three activities: factual exploration resolves questions; tests establish behavior; model review independently challenges a candidate. They have different costs and need not share cadence.

Reviewers use two **lenses**, not separate authority hierarchies:

| Lens | Question | Routing |
| --- | --- | --- |
| Completion | Is the agreed work actually done and correct, with adequate executable evidence? | Normal for straightforward verification; XHARD for reasoning-heavy correctness or integration questions |
| Strategic | Is the approach coherent, appropriately simple and aligned with the agreed goal across components? | Often benefits from the designated judgment model; use XHARD routing when the reasoning warrants it or a user override specifies the model |

A strategic lens does not automatically make an assignment XHARD, nor authorize reopening settled product scope. A normal critic can expose unnecessary architecture. A strategic review cannot excuse a concrete functional failure. For each review, record only lens, question/scope, classification/model/reasoning, evidence and round budget; both lenses can share one integrated review when appropriate. No requirement to run two reviewers for every checkpoint.

**Final-review bias and Astra default.** The presumption is to do one integrated review at the end of the work, after the candidate is implemented, integrated and tested. Use the configured Astra reviewer slots (`reviewer_normal`, `reviewer_xhard` and especially `final_reviewer`) for scheduled reviews by default. Add an earlier review only when a distinct consequential boundary needs a readiness decision, late discovery would be unusually costly, or the user explicitly requests it; do not create routine per-task or per-wave reviews. Explicit user-selected models, stages and budgets remain authoritative.

**Default review schedule.** Concentrate independent Astra review at completion
and consequential boundaries. For ordinary delivery, use one final integrated
review. For work that continues into a bulk migration or another consequential
operation, review the completed implementation and readiness evidence before
that operation, then review the resulting integrated outcome afterward. When
that last boundary completes the agreed scope, it is the final review; do not
append another final stage. Choose boundaries by the decision and cost of late
discovery, not task counts, implementation waves, repository count or elapsed
time. Routine per-task and per-wave model reviews are not the default.
Declare each selected trigger, scope, evidence and bounded round budget in
`run.yaml` before dispatch, honoring explicit user review policies.

**Review gates remain real.** Every review invocation must end with an explicit
verdict. `PASS` means all scoped required criteria have adequate evidence, no
blocking finding remains, and no correction task is still pending. `REWORK` means
the reviewer has produced actionable normal/XHARD correction tasks and the stage
must not pass until those tasks are implemented, tested and re-reviewed. `UNKNOWN`
means the candidate or evidence cannot be assessed reliably. When UNKNOWN is caused
by an access or identity problem, the review may be retried within the stage's
remaining round budget only after that cause is resolved and the candidate and
evidence identities are revalidated; the consumed UNKNOWN round is not restored.
The declared stage gate requires PASS; the coordinator advances on that uncontested
result, while the oracle adjudicates disputes and exceptions. An oracle disposition
rejecting all blockers does not itself replace the stage verdict: a remaining review
round is needed for the reviewer to obtain PASS, and if no round remains, surface
the review-budget decision. At the run's chosen meaningful
checkpoints, completion review establishes readiness; strategic review addresses
consequential design/integration questions or the final whole. Accepted blockers
hold affected dependents; unrelated work continues. Optional suggestions do not
become requirements. A gate is a decision about required evidence, not an
automatic stronger-model call. User-selected final-only arrangements take
precedence over default checkpoint choices.

The final allocated review stage may contain multiple allocated rounds; it is not
itself the last allocated round. It remains a final-stage review, not a reason to
waive remaining work. Tell the final reviewer that it is reviewing
the final allocated review stage and whether this invocation is its last allocated
round. It may still produce additional correction tasks or non-blocking
revision suggestions. Blocking correction tasks mean REWORK, not PASS, until
they are executed and verified. A final reviewer may still return PASS while
listing optional revisions, as long as all required criteria pass and no
blocking task remains; optional revisions do not receive a dispatch route and
do not hold completion. On the last allocated
round of the final allocated review stage, the reviewer may return `HARD_BLOCK` when direct
evidence shows an unresolved in-scope `contract_violation`, `implementation_defect`
or `required_evidence_gap` remains. HARD_BLOCK stops truthful completion and may
list the remaining correction tasks/conditions; it is not for optional
improvements, polish or a disagreement about an unrequired alternative. Never
convert a real blocker into PASS merely because the final review budget is
exhausted, and never create an unapproved extra review round to avoid HARD_BLOCK.


**Schedule comes from run.yaml.** A stage is a named checkpoint trigger and review scope; a round is one independent reviewer invocation within that stage. Each stage selects a reviewer role, lens and maximum rounds; the role's configured model binding is execution metadata. The list and its caps are authoritative; do not append a hidden default final review. Later rounds verify corrections and affected integration, stopping early when resolved.

**User-directed Astra final-review cap.** When the user explicitly selects this five-round Astra final
review policy, the final stage has at most five rounds total and stops
immediately on an uncontested PASS. The fifth round is the last opportunity;
it may return HARD_BLOCK for a directly evidenced unresolved in-scope blocking
finding after the correction opportunity. Ordinary polish, optional
improvements, or alternatives outside the contract do not justify a hard block.
Never create a sixth Astra round, rename a round, or add another review stage to
evade the cap; route a disputed hard-block classification to the configured
oracle when judgment is needed. Rounds two through five are correction
verification, not a quota for repeated reassurance. This specific five-round
policy does not override a different explicit user stage budget.

Select only boundaries that need a distinct readiness or completion decision;
name what must be established and which dependent work it protects. A review
may interpret passing tests and source evidence together; it need not wait for
an assumption that is impossible to test mechanically. Merge stages that would
inspect the same candidate and evidence. Default intermediate stages allow up
to two rounds each; the final reviewer stage allows up to five. These are
correction caps, not quotas: stop immediately on an uncontested PASS, and spend
another round only after an actionable blocking finding, the affected
correction, and fresh checks, or to retry an UNKNOWN caused by an access or
identity problem within the remaining stage-round budget after that cause is
resolved and the candidate and evidence identities are revalidated, or for a
post-oracle verification round within the remaining stage-round budget when the
oracle rejects all blockers so the reviewer can obtain PASS. The consumed
UNKNOWN round still counts; the post-oracle verification uses an existing round
and creates no extra round or budget. Do not use remaining rounds for generic hardening,
repeated discovery, or reassurance. Architecture or authority uncertainty goes
to the oracle. A user-selected final-only policy remains authoritative; do not
silently add a stage or increase an adopted budget. Planning-only mode dispatches
no executable review stages. Ordinary tests, integration checks and required
pre-operation validation continue throughout implementation.

A stage checks the complete scope named at its checkpoint, not just its final task. The final holistic lens covers overall completion and strategic coherence; it is a configured reviewer assignment, not another oracle hierarchy. The same model may hold multiple roles, but reviewer invocations remain independent of implementation context.

At the final integrated review, ask Astra to assess both the technical outcome and the quality of how the outcome is achieved and communicated. Alongside correctness, contracts, tests, integration, simplicity and scope, inspect—when applicable—whether documentation, explanations, user-facing text, names, examples, errors and structure are clear, accurate, appropriately audience-aware and sufficient to let someone understand or use the result. For non-text work, assess the equivalent clarity of the interface, behavior, workflow or handoff. Do not invent a writing requirement for work with no communication surface; mark the dimension not applicable. Treat clarity problems as blockers only when they violate the agreed goal/criteria or materially mislead users; otherwise report them as optional improvements.

Every reviewer is an independent leaf in a fresh conversation with read-only access, receives the frozen scope and candidate plus relevant evidence/oracle dispositions, and may not spawn reviewers or invent requirements. First review is integrated; correction rounds cover affected criteria and their dependencies, preserving unaffected approvals. No panels or repeated whole-project discovery after a demonstrated blocker. Use one source census per relevant candidate/path set, not one per reviewer.

Classify findings as `contract_violation`, `implementation_defect`, `required_evidence_gap`, `optional_improvement`, `out_of_scope` or `stale_or_repeated`. Only the first three can block. The coordinator routes clear in-scope findings under the mandate; the oracle verifies contested claims against source/tests and records an evidence-backed disposition. No automatic promotion of a reviewer's recommendation into authority.

For each finding, keep blocking classification separate from correction difficulty.
Only an actionable correction finding receives a recommended difficulty of `normal`
or `xhard`; optional, out-of-scope, stale, or otherwise unaccepted findings receive
no dispatch route. Astra reviewers must emit each actionable finding as a concrete
correction task, not only as review prose: state the outcome, acceptance evidence,
source/dependency scope, affected criterion, and `normal` or `xhard` route. An
unresolved or disputed difficulty is referred to the oracle, then the executable
next action receives a `normal` or `xhard` route. A clear normal route goes to
`worker_normal`; a clear XHARD route goes to `worker_xhard` with its
justification. The coordinator mechanically dispatches those correction tasks
through the same subagent-first execution path as first-pass work; it does not fix
them inline. Workers implement and test the correction, report evidence, and the
affected criteria return to the same declared review stage for verification. The
coordinator may route a reasoning-heavy correction directly to XHARD without first
trying a normal worker. After two failed substantive correction cycles, require a
root-cause decision on the brief/tools, decomposition, bounded spike, or justified
XHARD assignment; do not silently repeat the same correction. Run affected tests
before another review. These routing records do not create a fixer role or review
gate and do not authorize resetting the review budget.
A review cap ends repetitive model reviewing, not responsibility for the outcome. At
the stage or total budget cap, request oracle diagnosis if its budget permits,
continue authorized corrective work/tests where useful, and surface a needed
budget/authority decision. The coordinator cannot bypass an unpassed required gate
or reset its budget. Do not launch an equivalent review under a new name, reset
counters, label failure PASS or hand back a solvable problem merely because reviews
are exhausted. If further independent certification is essential, report that gap
and seek only the needed review-budget change; never claim unreviewed corrections
received a pass. Explicit user round counts take precedence.

The cap applies across renaming/repackaging/checkpoints for the same review scope. Record counts and accepted findings once. Increase a fixed user budget only with their approval; when a new risk requires different scope, explain it rather than hide another review in a new name.

## Completion

Planning completion means the plan is coherent, scoped and ready to implement; report it as such. Delivery completion requires a final-stage PASS, executable evidence for the agreed outcome, disposition of blocking findings and an honest summary of remaining limitations. REWORK, UNKNOWN or HARD_BLOCK is not completion. Run the broad affected suite once on the final candidate; repeat only affected checks after changes. Frozen review mechanics and sync authorization are in the execution reference; do not infer deployment from a successful review.

## Review packet assembly

Use the [review packet template](templates/review-packet.md) and [artifact assembly rules](references/review-packets.md). Each declared stage names its task/criterion scope up front. Completion review checks actual implementation and proof; the final holistic lens also checks coherence, simplicity, North Star alignment and applicable communication clarity. The coordinator fills the packet from exact artifacts instead of inventing the reviewer's goals. This adds no model call or review stage.

## Model invocations

Use available native subagents or the installed launchers; preserve the selected model and reasoning effort and record the actual invocation. For launcher model specs, carry the `run.yaml` effort as a suffix (for example, `codex:gpt-5.6-luna:xhigh`); pass the configured effort separately to native subagents or CLIs. If a runtime cannot honor the configured effort, resolve that before dispatch rather than silently relying on its default or doing the work in the coordinator. Tool permissions come from the environment and task, not from this skill. Read-only exploration/review stays read-only; a delegated manager needs network access if its launcher uses it. Never bypass an environment prohibition to match an example.

```bash
# Normal worker example: carry the configured model and effort, grant only the tools needed.
PYENV_VERSION=3.11.11 python ~/.claude/skills/subagent-launcher/launch_hermes_agent.py \
  --model="codex:gpt-5.6-luna:xhigh" --toolsets="file" \
  --query-file="$BRIEF" --project-dir="$SOURCE_DIR"
# Flash alternative: --model="deepseek:deepseek-v4-flash"
# Normal implementation adds terminal tools in the isolated execution worktree.
# For multiple independent briefs use fan.py, with the same declared model.

# Optional Sol advice; not a required planning phase. Seal stdin.
codex exec -C "$SOURCE_DIR" --sandbox read-only \
  -c model=gpt-5.6-sol -c model_reasoning_effort=high \
  "$(cat "$BRIEF")" </dev/null
# Optional Grok advice:
grok --cwd "$SOURCE_DIR" --prompt-file "$BRIEF" \
  -m grok-4.6 --reasoning-effort high --permission-mode plan
```

Set an invocation timeout with the launcher/process supervisor (normally at most 30 minutes), not a blocking wait that prevents host updates. For implementation, assign permissions appropriate to source mutation; for a manager, include delegation permissions only if it actually dispatches. For any reviewer, use the run's recorded model and reasoning, a frozen candidate and non-mutating access. The examples are invocation mechanics, not additional model gates.

## Operational gotchas

- Seal `codex exec` stdin with `</dev/null`; otherwise it can wait for input indefinitely.
- A user's existing model/role/review choices persist. The coordinator cannot silently assume oracle authority; oracle decisions never broaden user authorization.
- Preserve dirty local work. A worktree from HEAD does not include uncommitted files; identify which source is authoritative before executing.
- Keep run artifacts in the recorded control root and execution in its recorded worktree. Do not recompute the project root inside a nested checkout on resume.
- Source custody and test evidence prevent false completion; process liveness and reviewer approval alone do not prove the product works.
- Run capacity checks before expensive work. After ENOSPC or disk-I/O failure, fix capacity before retrying; do not repeatedly dispatch into the same failure.
- Reuse unchanged passing evidence. Fixes invalidate only affected criteria and their dependency closure, not the whole project.
- Report launches, findings, decisions, failures and completions. Keep no-change polling out of progress logs.
- Never infer merge, push, production mutation or deployment authority from the North Star, a review verdict or the word “sync.”

## Shared maintenance

Keep the **Roles and model policy**, **Oracle decision requests**, **Delegation**, **Model invocations**, and **Operational gotchas** blocks identical in Megado and Microdo. Their planning/review cadence is intentionally different; do not copy mode-specific gates between them. Maintain shared execution references consistently when changing custody/invocation mechanics. Do not append conflicting copies of the review policy to examples or cloud briefs.
