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

## Produce a ready plan

After scope agreement, write focused tasks with outcome, route (`N`, `X` or `S`; see below), actual base and donor identities, dependencies, explicitly scoped acceptance checks, estimate, deferred scope, and required inputs. Distinguish evidence from assumptions. Keep active/upcoming project status and remaining human-day estimate in the working repo's authoritative project index; plans own technical detail and task progress. Do not run tests while planning unless asked, create a generic framework, or add recurring reviews. Existing accepted plans continue under their accepted scope and review policy without new planning sign-off.

## Tag each task with its route

Use the [routing table](../astrid-dev-shared/run-contract.md#routing-and-bindings). `N` is the default and covers everything below very hard, including ordinary hard work (Haiku or Luna). Tag a task `X` only when it is very hard (Sonnet or Terra) and `S` only when it is super hard (Opus or Sol). Name the route, not the model: execution sends each task to its route’s model, so one tag serves both the plan and the build.
