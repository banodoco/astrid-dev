# F-003 — Creative execution isn't yet dependable end to end

**Applies to:** [Eliminate needless technical wrangling](../principles/eliminate-needless-technical-wrangling.md) (primary) · [A Tool for Artistic Ambition](../pillars/artistic-ambition.md) (supporting) · **Assessment:** Partially evidenced; Plan 32 CPU evidence, with real creative results still required (2026-11-10).

## Desired state

From a declared supported, usable Astrid workspace, a creator and agent can choose a creative operation, prepare an appropriate model or provider, execute real inference or media processing, and receive the intended **correct, editable creative result** with progress and recoverable failures. The core proof is successful creative work—not reinstalling or updating Astrid.

## Current state

Astrid has Runtime execution/task primitives, packs, generation integrations and the video editor. [Plan 02](../../plans/02-consistent-generation/plan.md) aims to establish consistent defaults and pinned stack on fixtures and a fresh Linux CPU setup, **explicitly not real inference**. [Plan 12](../../plans/12-multiple-inference-routes/plan.md) targets real multiple inference routes. [Plan 20](../../plans/20-zero-to-first-image/plan.md) targets a real first generated image on a timeline; [Plan 16](../../plans/16-streamlined-agent-experience/plan.md) improves agent readiness.

[Plan 32](../../plans/32-generation-placement-targets/plan.md)'s CPU evidence adds the common generation path, placement defaults and overrides, progress, cancellation and output retrieval on managed-local, attached and shipped-job RunPod stand-ins. Its [current candidate](../../plans/32-generation-placement-targets/inputs.md#integrated-cpu-candidate-for-completion-review) is Agent `99724131d2c3eff11867a189986c4ba147e5a81b`, a test-only change from reviewed `26eeaff4f`; runtime proof retains its tested revisions. Implementation is ready for completion review, while final CI and main landing wait on the owner's Release 12 freeze/hold. [Separate Plan 34 evidence](../../plans/32-generation-placement-targets/inputs.md#separate-plan-34-image-receipt) records one Qwen RunPod image at exact `26eeaff4f`, with unchanged-runtime carry-forward to `99724131d`. This is not Plan 32 paid work or proof of editable timeline integration across workflows. The earlier heartbeat cause, same-marker altered imports before reset and broader hardware coverage remain unproven.

## Gap

The end-to-end **creative job**—capability selection, model/provider readiness, actual task execution, artifact identity and usable output—has not been dependably proven across selected supported workflows and failure paths. Install/update lifecycle belongs to F-001; approval and access decisions belong to F-002.

## Closure evidence

On a stated supported setup, run real creative generation or processing and inspect the resulting editable artifact for correct content, project identity, output settings and usable timeline/workspace integration. Demonstrate failed-job diagnostics, stop/retry and cleanup; separately qualify platform installation and permission boundaries in F-001/F-002.

## Sources and reassessment

[Plan 02](../../plans/02-consistent-generation/plan.md) · [Plan 33](../../plans/33-unblock-live-generation/plan.md) · [Plan 32 CPU evidence](../../plans/32-generation-placement-targets/tasks.md) · [Plan 34](../../plans/34-real-gpu-proof/plan.md) · [Plan 12](../../plans/12-multiple-inference-routes/plan.md) · [Plan 16](../../plans/16-streamlined-agent-experience/plan.md) · [Plan 20](../../plans/20-zero-to-first-image/plan.md). Do not equate fixture checks with real GPU/inference qualification. Portability across machines and engines is [F-008](F-008-portable-generation.md).
