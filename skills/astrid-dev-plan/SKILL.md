---
name: astrid-dev-plan
description: Plan a genuinely new Astrid project or materially new scope by tracing prior art, challenging complexity, and agreeing one concrete end state with the owner.
---

# Plan Astrid development work

Use this workflow only for a genuinely new project or materially new scope. Consult the active working repository's instructions and accepted plan index first. An accepted plan does not need retroactive owner approval. Read the [shared run contract](../astrid-dev-shared/run-contract.md); planning itself does not start product work.

## Decide the smallest sound outcome

1. Search relevant repositories, docs, skills, and prior plans for prior art before asking for placement or scope decisions. Follow the behavior from inputs through existing reuse points to the observable outcome. The manager dispatches bounded `N` prior-art research with concrete path/evidence requests; avoid broad audits that cannot change the decision.
2. Decide whether to extend an existing pack, add a pack, or change shared core, and recommend the smallest viable placement with evidence. Identify any material uncertainties for the owner.
3. Have a configured high-judgment planner propose the simplest complete approach from the findings. Then ask a distinct, fresh configured high-judgment planner to challenge overengineering. It must name specific removals, consolidations, or reuse and say which user outcomes each preserves or gives up. Reconcile disagreement from evidence and protect real user constraints. Luna-class planning is for prior-art research, not either design judgment.
4. Present **ten concrete, provocative end-state statements** for the owner to react to. They should make meaningful outcome/tradeoff choices clear, not list ten features or implementation tasks.
5. Obtain one owner's agreement on the new scope/end state before treating it as an accepted plan. This agreement is not a recurring per-task sign-off; it does not independently authorize product execution or publication.

Use exact configured model IDs and supported effort from the run's `run.yaml`; class labels are not identities. Do not invent IDs or silently substitute an unavailable model.

## Preserve planning evidence in the project pack

The planning conversation is not evidence by itself. Leave a **reviewable trail in `inputs.md`** before representing a project as accepted and ready for execution:

1. **Prior art and actual behavior:** cite the repositories, docs, earlier plans and useful external approaches searched (including exact revision/links where it matters). Trace the current behavior from input to user-visible outcome; record promising reuse points, negative search results, and uncertainties. "No prior art" is a finding to justify, not a default assumption.
2. **Reuse and placement:** compare extending an existing pack, creating a pack, adapting shared core, and doing less or nothing. State the chosen placement, source-backed rationale, tradeoffs and what it preserves. Do not mistake a new project for a new vision gap: use the existing [gap contract](../../visions/gaps.md), identify the most relevant existing gap first, and only propose a new outcome-level gap with its own independent closure test.
3. **Independent simplification challenge:** record the separate high-judgment planner's concrete suggested removals, consolidations, or reuse; record what was accepted/rejected and why. Identify what it actually reviewed and where the record lives. A rubber-stamp approval or unrun challenge is not proof.
4. **End-state choice:** preserve the ten genuinely different end-state statements or a durable link to them, the meaningful alternatives the owner rejected, and the *actual owner-agreed outcome*, with a date/source. Do not infer approval from silence or from creating a queued catalog entry.
5. **Evidence limitations:** separate observed facts, reasoned assumptions and unresolved source/permission/hardware questions. Link relevant evidence rather than pasting bulky transcripts into multiple files.

Use the [project pack's `inputs.md` template](../../templates/project/inputs.md) as the **single planning-evidence location**. `plan.md` holds the *decision* (the chosen end state, scope, retained work and completion test); `tasks.md` holds the *implementation handoff* (source inputs, dependencies and focused proof). Link to supporting research or owner-decision records when they need independent homes. Never maintain duplicate findings/status ledgers across those files.

**Draft versus accepted:** a new project may be recorded as a draft while research, the independent challenge, ten end-state options or owner approval is genuinely pending. State each missing item as `Pending — <why; next action>`; do not fill it with invented links or claim readiness. Before promoting the scope as accepted, replace pending evidence with actual findings, a specific owner decision, and the aligned ready tasks. The catalog still owns status/owner/priority; this scope-decision record does not change that or authorize execution.

The existing documentation CI checks that newly introduced project packs have an explicit planning-evidence record and that an **Accepted** record has sources rather than unresolved placeholders. It cannot judge whether an actual search was diligent, the proposed architecture is minimal, or owner agreement is authentic. A reviewer must make that judgment; this is not an additional sign-off round.

## Produce a ready plan

After scope agreement and with the planning evidence captured in `inputs.md`, write focused tasks with outcome, route (`N`, `X` or `S`; see below), actual base and donor identities, dependencies, explicitly scoped acceptance checks, estimate, deferred scope, and required inputs. Distinguish evidence from assumptions. Keep active/upcoming project status and remaining human-day estimate in the working repo's authoritative project index; plans own technical detail and task progress. Do not run tests while planning unless asked, create a generic framework, or add recurring reviews. Existing accepted plans continue under their accepted scope and review policy without new planning sign-off.

## Use one project folder

Use the working repository's project-folder template. In this workspace, copy [templates/project/](../../templates/project/) to `plans/<id-name>/`. Every project, including a draft, has three required files:

- `plan.md`: the central explanation—goal, scope, existing work, sequence, and completion.
- `tasks.md`: the task index and detailed cards, with routes, dependencies, focused proof, and task progress.
- `inputs.md`: source materials, predecessor outputs, references, and evidence limits; for code projects include repositories, actual starting branches/SHAs, retained work/donors, candidate branches, and destinations.

The project index links to `plan.md` and remains the sole owner of status, accountable owner, and estimate. Short task cards stay in `tasks.md`. For a substantial phased project, the index may link to `tasks/<phase>.md`; substantial design, assets, or evidence may have their own linked homes. Do not create empty support folders or duplicate task cards. Avoid multiple competing entry documents. Unknowns stay explicit in drafts; complete executable task fields before dispatch without inventing source identities or introducing a new approval gate.

## Tag each task with its route

Use the [routing table](../astrid-dev-shared/run-contract.md#routing-and-bindings). `N` is the default and covers everything below very hard, including ordinary hard work (Haiku or Luna). Tag a task `X` only when it is very hard (Sonnet or Terra) and `S` only when it is super hard (Opus or Sol). Name the route, not the model: execution sends each task to its route’s model, so one tag serves both the plan and the build.
