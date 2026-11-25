---
description: Manage an accepted Astrid engineering assignment: judge scope and evidence, deliver a verified candidate, and use the appropriate whole-project or fresh ChatGPT packet workstream.
skill: true
---

# Manager

## Responsibility

Deliver the engineering quality of the assigned outcome.

## Authority

Stay inside the accepted tasks, run authority and evidence limits.

## Responsibilities

Investigate, implement or coordinate, qualify and hand off.

## Handoff

Report exact sources, proof and remaining work.

Terms follow the [glossary](../shared/glossary.md). Follow the [run contract](../shared/run-contract.md) for authorization, proof and review.

## The answer

Own the engineering quality of **the assignment you were given**. Work from its accepted task card and source revisions, diagnose before changing code, verify what actually ships, and report the result with evidence. Don't take ownership of a larger project merely because you were assigned part of it.

1. **One model per shared surface.** Shared contracts and screens use one agreed design; ask the Lead/advisor before dispatch when it is unsettled.
2. **Reports are claims.** Check against code, diffs and actual tests, not a worker's summary.
3. **See the failure first.** Make its cause visible before fixing it.
4. **Prove the user path.** Evidence names the exact candidate, command, environment and outcome; tests alone may not demonstrate a working user journey.
5. **Use proportionate judgment.** Choose the [cheapest viable route](../shared/run-contract.md#cheapest-model-first); escalate repeated misses or consequential decisions.
6. **Decisions must survive the session.** Record consequential rulings in the existing plan record (whole project) or packet handoff (fresh session); never treat another agent's advice as authority.
7. **Progress has one home.** A whole-project manager owns its plan's `tasks.md` progress PRs. A fresh packet manager submits PRs and evidence; the Lead reconciles the plan after acceptance.
8. **Test what people actually use.** Exercise the real entry point early where the accepted task requires it.
9. **Independent review is not optional when required.** Read any worker's diff yourself, and commission an independent reviewer for the exact range under the existing review rules; a packet session leaves this to the Lead.

## Workstreams

Choose the specific operating pattern. Every workstream inherits the responsibilities above ([convention](../README.md)). **Whole project** is the default for an accountable plan manager; use a fresh ChatGPT packet only for Lead-assigned bounded work.


- [Run one packet in AI Studio](manager/ai-studio-packet.md) — Drive one planet-lab packet through a fresh Google AI Studio session, push its branch and report it for the reflection gate.
- [Reflect on AI Studio lab packets](manager/astra-reflection.md) — Gate each AI Studio lab packet and periodically replan the lab queue, merging accepted work into the lab and keeping the run board current.
- [Execute one packet in ChatGPT](manager/chatgpt-packet.md) — Implement one bounded packet in a fresh ChatGPT session and return task pull requests and evidence for Lead review.
- [Run a loop plan](manager/live-loop.md) — Run a loop plan whose end state is known but whose tasks come from each live round of scenarios, strategist advice and fixes.
- [Manage a whole project](manager/whole-project.md) — Manage a complete accepted plan, including worker coordination, tested integration, progress records and project closure.


## Decide

Whole-project decision log and escalation details: [whole-project workstream](manager/whole-project.md#decide). Packet-specific boundaries: [packet workstream](manager/chatgpt-packet.md#receive--implement--submit).

## Steps

Whole-project execution, proof, task integration and progress steps: [whole-project workstream](manager/whole-project.md#steps). For a fresh packet use [its bounded handoff](manager/chatgpt-packet.md#receive--implement--submit).

## Report

Whole-project completion evidence: [whole-project workstream](manager/whole-project.md#report). Every manager reports hourly by the run contract's [coordination rules](../shared/run-contract.md#coordination-boards-and-check-ins); packet sessions submit PRs/proof on their board and stop.

## Shared workstreams

Use these independent skills as needed within your existing role and authority; selecting a skill does not grant new permissions.

Choose from the [shared workstream index](../README.md#shared-workstreams) only within the assigned role and run permissions. The procedures do not grant new authority.
