---
name: astrid-dev-plan
description: Plan a new Astrid development project by tracing prior art, challenging complexity, defining ten owner-facing end-state choices, and producing a ready scoped plan after owner scope agreement.
---

# Plan Astrid development work

Read the [shared run contract](../astrid-dev-shared/run-contract.md), then consult the active working repository’s instructions and accepted plan index. This workflow is for a genuinely new project or materially new scope. It does not retroactively request approval for an already accepted plan.

## Find the smallest sound shape

1. Make the first decision whether the capability should extend an existing pack, become a new pack, or live in shared core. Search relevant repos, docs, skills, and prior plans for evidence before asking; delegate bounded `N` searches, require file/path evidence, and follow data from inputs through existing reuse points to output. Then give the owner an evidence-based recommendation and ask them to resolve that placement as part of scope agreement. Avoid broad audits that cannot change the decision.
2. Have a high-judgment planner propose the simplest complete approach, based on those findings. Use an exact available model configured in the run; do not invent a model ID or substitute silently.
3. Ask a separate, fresh high-judgment planner to challenge overengineering. It must identify concrete removals, consolidations, or reuse and what outcomes each preserves or gives up. Reconcile disagreement using evidence; preserve real user outcomes and constraints.
4. Present **ten concrete, provocative end-state statements** for the owner to react to. These are tradeoffs that make the possible outcomes legible, not ten features or hidden tasks. State outcomes and tradeoffs in plain language, not promises or an implementation checklist.
5. Obtain the owner's agreement on the new project's scope/end state before treating it as an accepted plan. This agreement accepts the plan; product execution and publication still need their own explicit authority. Existing accepted plans do not need this sign-off again.

## Produce a ready plan

After scope agreement, write focused tasks with outcome, `N`/`X`/`S` difficulty, current base and donor identities, dependencies, focused checks, estimate, deferred items, and required inputs. Distinguish evidence from assumptions and preserve current project status/estimates in the README as their single source. Do not run tests for planning unless asked. Do not add recurring reviews or a generic framework.

Finish with the ten end-state statements and decisions, the ready task plan, estimates/uncertainties, and any deferred scope. Existing accepted plans proceed under their existing authority and review choices without a new planning sign-off.
