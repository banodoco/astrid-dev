---
name: astrid-dev-manage
description: Manage an accepted Astrid engineering assignment: judge scope and evidence, deliver a verified candidate, and use the appropriate whole-project or fresh ChatGPT packet workstream.
---

# Manage Astrid engineering work

Terms follow the [glossary](../astrid-dev-shared/glossary.md). Follow the [run contract](../astrid-dev-shared/run-contract.md) for authorization, proof and review.

## The answer

Own the engineering quality of **the assignment you were given**. Work from its accepted task card and source revisions, diagnose before changing code, verify what actually ships, and report the result with evidence. Don't take ownership of a larger project merely because you were assigned part of it.

1. **One model per shared surface.** Shared contracts and screens use one agreed design; ask the Lead/advisor before dispatch when it is unsettled.
2. **Reports are claims.** Check against code, diffs and actual tests, not a worker's summary.
3. **See the failure first.** Make its cause visible before fixing it.
4. **Prove the user path.** Evidence names the exact candidate, command, environment and outcome; tests alone may not demonstrate a working user journey.
5. **Use proportionate judgment.** Choose the [cheapest viable route](../astrid-dev-shared/run-contract.md#cheapest-model-first); escalate repeated misses or consequential decisions.
6. **Decisions must survive the session.** Record consequential rulings in the existing plan record (whole project) or packet handoff (fresh session); never treat another agent's advice as authority.
7. **Progress has one home.** A whole-project manager owns its plan's `tasks.md` progress PRs. A fresh packet manager submits PRs and evidence; the Lead reconciles the plan after acceptance.
8. **Test what people actually use.** Exercise the real entry point early where the accepted task requires it.
9. **Independent review is not optional when required.** Read any worker's diff yourself, and commission an independent reviewer for the exact range under the existing review rules.

## Workstreams

Choose the specific operating pattern. Both inherit the responsibilities above ([convention](../astrid-dev-shared/workstreams.md)).

- **[Whole project](workstreams/whole-project.md)** — the default when you are accountable for an entire plan run: dispatch, manage workers and run state, land and reconcile tasks, and close the project.
- **[Fresh ChatGPT packet](workstreams/chatgpt-packet.md)** — one new ChatGPT session executes exactly one packet and returns task PRs and evidence to the Lead; no plan-level run, task-progress PR, or release merge.

## Decide

Whole-project decision log and escalation details: [whole-project workstream](workstreams/whole-project.md#decide). Packet-specific boundaries: [packet workstream](workstreams/chatgpt-packet.md#receive-implement-submit).

## Steps

Whole-project execution, proof, task integration and progress steps: [whole-project workstream](workstreams/whole-project.md#steps). For a fresh packet use [its bounded handoff](workstreams/chatgpt-packet.md#receive-implement-submit).

## Report

Whole-project completion evidence: [whole-project workstream](workstreams/whole-project.md#report). Packet sessions submit PRs/proof through the shared issue and stop.
