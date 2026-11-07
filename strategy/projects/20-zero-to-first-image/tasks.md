# Tasks: zero-to-first-image onboarding

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../../README.md)

This is a draft outline, not a ready-to-dispatch breakdown. Executable task boundaries, dependencies, route labels, and exact focused selectors remain to be scoped from current source; do not infer them here.

## Intended work and proof

- **20 — One-command journey.** Define a supported starting state (existing inference service and model availability, account needs, platform, and Astrid setup performed). Detect existing prerequisites and explain only actionable gaps. Provide a discoverable command and matching agent instruction that carry setup/connection through generation and output registration to a visible timeline result. Keep required consent visible without making users assemble backend commands or diagnose architecture; where feasible, the direct command should need no agent reasoning.
- **20 — Real completion proof.** Exercise that exact journey from the declared starting state with real inference and a real displayed result. Separate targeted unit checks from end-to-end proof; mocked generation does not establish completion.
- **20 — Recovery proof.** Cover unavailable service/model, interrupted setup, cancelled generation, and safe rerun without duplicate installs or unintended work. Show the failed step and shortest recovery.
- **20 — First-image effort evidence.** Measure total agent tokens from initial instruction to visible result, including retries; record model, starting state, interventions, elapsed time, and token use against the ~50,000-token target. If users choose the separate sandbox setup, report any onboarding friction to [Plan 15](../15-openshell-safe-execution/plan.md); do not expand this plan's acceptance checks into a full-stack isolation qualification.

These are outcome areas, not assigned task cards: split or combine them only after identifying source paths, dependencies, route labels, and grounded selectors. Follow existing authority and review limits in the [shared run contract](../../../skills/astrid-dev-shared/run-contract.md); this draft adds no review stage or round count.
