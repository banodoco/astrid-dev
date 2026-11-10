# F-003 — Creative execution isn't yet dependable end to end

**Applies to:** [Eliminate needless technical wrangling](../principles/eliminate-needless-technical-wrangling.md) (primary) · [A Tool for Artistic Ambition](../pillars/artistic-ambition.md) (supporting) · **Assessment:** Partially evidenced; Plan 32 CPU evidence, with real creative results still required (2026-11-10).

## Desired state

From a declared supported, usable Astrid workspace, a creator and agent can choose a creative operation, prepare an appropriate model or provider, execute real inference or media processing, and receive the intended **correct, editable creative result** with progress and recoverable failures. The core proof is successful creative work—not reinstalling or updating Astrid.

## Current state

Astrid has Runtime execution/task primitives, packs, generation integrations and the video editor. [Plan 02](../../plans/02-consistent-generation/plan.md) aims to establish consistent defaults and pinned stack on fixtures and a fresh Linux CPU setup, **explicitly not real inference**. [Plan 12](../../plans/12-multiple-inference-routes/plan.md) targets real multiple inference routes. [Plan 20](../../plans/20-zero-to-first-image/plan.md) targets a real first generated image on a timeline; [Plan 16](../../plans/16-streamlined-agent-experience/plan.md) improves agent readiness.

[Plan 32](../../plans/32-generation-placement-targets/plan.md)'s CPU evidence adds the common generation path, placement defaults and overrides, progress, cancellation and output retrieval on managed-local, attached and shipped-job RunPod stand-ins. Its [task record](../../plans/32-generation-placement-targets/tasks.md) names each tested revision and its limits; the [current integrated snapshot](../../plans/32-generation-placement-targets/inputs.md#integrated-cpu-candidate-for-completion-review) is Agent `a2ccbde9192ec26c5a736c7894bc2ecda7bb9656`. Reviewed liveness, GPU identity and reset/readiness repairs, plus the exact i2v CPU retry, have scoped passing proof. A new Plan 34 cell-4 failure is under diagnosis; an expected batched repair and final-candidate CI comparison remain pending. The earlier heartbeat failure's cause remains unknown under Plan 34's liveness-family follow-up. These stand-ins do not establish the content, editability or timeline integration of a real generated artifact. [Plan 34](../../plans/34-real-gpu-proof/plan.md) supplies the separate real-GPU proof.

## Gap

The end-to-end **creative job**—capability selection, model/provider readiness, actual task execution, artifact identity and usable output—has not been dependably proven across selected supported workflows and failure paths. Install/update lifecycle belongs to F-001; approval and access decisions belong to F-002.

## Closure evidence

On a stated supported setup, run real creative generation or processing and inspect the resulting editable artifact for correct content, project identity, output settings and usable timeline/workspace integration. Demonstrate failed-job diagnostics, stop/retry and cleanup; separately qualify platform installation and permission boundaries in F-001/F-002.

## Sources and reassessment

[Plan 02](../../plans/02-consistent-generation/plan.md) · [Plan 33](../../plans/33-unblock-live-generation/plan.md) · [Plan 32 CPU evidence](../../plans/32-generation-placement-targets/tasks.md) · [Plan 34](../../plans/34-real-gpu-proof/plan.md) · [Plan 12](../../plans/12-multiple-inference-routes/plan.md) · [Plan 16](../../plans/16-streamlined-agent-experience/plan.md) · [Plan 20](../../plans/20-zero-to-first-image/plan.md). Do not equate fixture checks with real GPU/inference qualification. Portability across machines and engines is [F-008](F-008-portable-generation.md).
