---
name: astrid-dev-advise
description: Answer one bounded question when an Astrid manager or working agent is genuinely blocked, faces conflicting evidence, or must make a consequential judgment; return one concrete next action. Use only when asked for advice.
---

# Advise on an Astrid blocker

Use this only when a manager or working agent asks. That means a genuine blocker, conflicting evidence, or a consequential judgment the accepted plan cannot settle. It is not routine per-task approval. Follow the [run contract](../astrid-dev-shared/run-contract.md), and answer the bounded question you were given.

- **Refresh the facts first:** the exact candidate, source and donor identities, dirty state, the brief, the first failing command, the repair history, and the review budget.
- **Diagnose from evidence.** A claim in the request is a claim until code, logs or a run supports it. If the cause isn't visible, the next action is to make it visible.
- **Return one concrete next action,** with its route, focused acceptance check, dependencies and return condition. For a high-judgment choice, give the simplest viable option, its trade-off, and a concrete challenge against over-engineering.
- **Require the previously failing check** to run on the repaired candidate.
- **Don't:**
  - waive failures, widen scope, reset counters, add a review stage, or authorize execution or publication;
  - invent model IDs, or claim a run happened without evidence.
- **If explicitly configured,** give one bounded progress or root-cause review at most every two hours, then stop. This is not a monitor or a schedule.
