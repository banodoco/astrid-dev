# Consistent generation path

Finish the retained generation work and merge it into `pre-main`, preserving the installer work already there. Reuse the existing implementation; finish its missing behavior and checks, then integrate the repositories together.

Current status, owner, and estimate are in the [project queue](../../README.md). The retained-work descriptions below come from the historical audit, not a fresh execution report.

## What this delivers

A coherent generation code path: consistent default selection, compatible dependency versions, and a tested installed-package interface. The checks cover the actual installation and a controlled generation-service protocol fixture.

**This increment does not yet prove an actual model-generated image reaching the gallery.** Model readiness, real inference, training, and GPU execution remain outside its accepted scope. The [first-image onboarding](../20-zero-to-first-image.md) and [multiple inference routes](../12-multiple-inference-routes.md) projects define later real-inference outcomes.

## What we build on

There are two kinds of starting code: **the current destination base** and **retained feature work from other branches or checkpoints**. Both matter. Using `pre-main` does not mean starting generation from scratch or discarding the existing implementation.

| Repository | Existing work to reuse | How it joins the result |
|---|---|---|
| Agent | PINS implementation and the unfinished DEFAULTS checkpoint. | Finish the retained work, then combine it with current `pre-main`, preserving Installer Consent. |
| VibeComfy | Resource and template changes. | Compose them onto the current producer base and check the result. |
| Lifecycle | Retained source/API changes. | Qualify the source and use the resulting exact version in Agent. |
| Runtime | Stop/ownership change, if generation actually depends on it. | Include only on source evidence; otherwise keep the current Runtime version. |
| App | Current base including Installer Consent; no separate generation feature donor. | Update its references to the final verified Agent and Runtime versions. |

The [input record](inputs.md) identifies the retained commits. Some are incomplete or only partly verified, so they are inputs to finish and integrate, not automatically ready-to-merge branches. Final dependency locks must describe the combined result.

## The sequence

1. **Finish the retained work.** Verify the dependency/build path (PINS), finish default selection (DEFAULTS), check the installed package (INSTALLED-TEST), and complete the existing acceptance review (END). Some code and local evidence already exist; the retained defaults edits are incomplete, and the cancelled verification run has no final verdict.
2. **Prepare the integration base.** Installer Consent must already be merged into Agent/App `pre-main` before final generation composition. Snapshot the then-current destination in each repository and create a separate candidate branch from it. Independent completion and producer checks can proceed earlier after the project is started.
3. **Combine the work and check the combined result.** Integrate VibeComfy and lifecycle inputs first, then Agent, then update the App's dependency references. Include the Runtime stop change only if source comparison proves generation needs it. Resolve conflicts, regenerate dependency locks, and run the affected focused checks on the combined code.
4. **Review and merge to `pre-main`.** Use the existing independent integration review, then promote those same reviewed commits. If the destination has moved, reconcile the change and repeat only the affected checks and review.

So `pre-main` is both the integration starting point and the final destination. We do not replace it with an old generation branch. If a producer repository has no `pre-main`, use its recorded current `main` as the candidate base and create `pre-main` only through the reviewed promotion procedure.

## Where to read next

| Document | Purpose |
|---|---|
| [tasks.md](tasks.md) | The four completion items and seven integration steps, with links to each task's instructions, dependencies, lead, checks, and done condition. |
| [inputs.md](inputs.md) | Exact retained commits, source evidence, branch rules, and how to recover the original targeted checks. |

The task details are sections within `tasks.md`; separate files are unnecessary for these short cards. The old Plan 02 and Plan 03 are now the completion and integration phases of this one project. The [older inclusion assessment](../../references/INCLUDING-GENERATION.md) remains background evidence, not another plan to follow.

Installer Consent is a separate preceding increment. Concurrent editing, Packs, and unrelated fixes are not pulled into this generation merge. No broad test suites, new approval stages, or product execution are introduced by this reorganization.
