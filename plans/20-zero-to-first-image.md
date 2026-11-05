# 20 — Zero-to-first-image onboarding

**Draft scope — top-priority upcoming project.** Current status and owner are in the [README queue](../README.md).

## Goal

Make the first useful result effortless for a person and their agent: starting with an existing supported inference installation, one copyable command takes them through setup to a generated image visibly placed on an Astrid timeline. Apply the [philosophy](../philosophy.md): good defaults, understandable choices, and user control.

## Scope

Start with one supported existing inference route and make that complete journey excellent. Reuse current installation, connection, generation, media, and timeline capabilities. Expand to additional routes after the first path is demonstrated; do not make finishing every backend a prerequisite.

Offer the full-stack sandbox option during onboarding through [Plan 15](15-openshell-safe-execution.md). Reuse [agent/account setup](16-streamlined-agent-experience.md) and the [shared inference lifecycle](12-multiple-inference-routes.md) as available. Keep required consent visible within the flow, without asking users to stitch together backend commands or diagnose architecture.

## Intended work and focused proof

- Define the supported starting state: existing inference service and model availability, account needs, platform, and what Astrid setup the command performs. Detect what is already present and explain only actionable missing prerequisites.
- Provide one discoverable command and matching agent instruction. Carry the user from setup/connection through generation, output registration, and a visible timeline result in the app.
- Exercise that exact journey from the declared starting state with real inference and a real displayed result. Separate targeted unit checks from end-to-end proof; a mocked generation response is not the completed journey.
- Cover a small named set of recovery paths: unavailable service/model, interrupted setup, cancelled generation, and safe rerun without duplicate installs or unintended work. Report the failed step and the shortest recovery.
- Measure the total agent tokens from the initial instruction to the visible result, including retries. Aim for fewer than roughly 50,000 tokens for the supported agent-assisted journey, with no agent reasoning required for a direct command where feasible. Record the model, starting state, interventions, elapsed time, and token use; treat the budget as a measured design target, not a claim of current performance.

## Completion

A new user can follow the short instruction and see a generated image on the timeline through the supported one-command path. The selected recovery paths pass focused checks, and recorded journey evidence shows the setup steps, user interventions, real output, and token cost. The supported sandbox variant has evidence for the whole app/backend path and its stated isolation boundary; any unsupported variant is explicit.

## Before implementation

Inspect existing source and freeze repository/base SHAs, reusable work, verified inputs, candidate branches, and intended integration destinations (`pre-main` where applicable). Choose exact tasks, difficulty levels, and focused test selectors from that evidence. Run no broad suites. This draft does not start product work or authorize compute use.
