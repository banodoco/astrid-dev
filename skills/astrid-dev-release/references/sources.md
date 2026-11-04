# Product release sources

These sources were read from clean configured checkouts during discovery. Commits identify the inspected snapshots, not a claim that they remain current. At task time, inspect the actual source checkout and use its current authoritative contracts.

## Astrid Agent

Observed repository: [`banodoco/astrid-agent`](https://github.com/banodoco/astrid-agent), branch `main`, commit `2958bacea3e3c7961788fa9c625dd9db0be282de` (clean at inspection).

- [Reproducible release inputs](https://github.com/banodoco/astrid-agent/blob/2958bacea3e3c7961788fa9c625dd9db0be282de/docs/runbooks/reproducible-release.md) — release lock and toolchain contracts, source pins, and Remotion closure.
- [Paired release recipe](https://github.com/banodoco/astrid-agent/blob/2958bacea3e3c7961788fa9c625dd9db0be282de/docs/setup/release-recipe.md) — producer handoff manifest and installed artifact receipt contract; pending tuple values are not inferable.
- [Local Make targets](https://github.com/banodoco/astrid-agent/blob/2958bacea3e3c7961788fa9c625dd9db0be282de/Makefile), `scripts/reshape/release_reproducibility.py`, `scripts/reshape/installed_artifact.py`, and `scripts/reshape/remotion_gate.py` — product-owned gates and artifact/toolchain evidence.
- [CI workflow](https://github.com/banodoco/astrid-agent/blob/2958bacea3e3c7961788fa9c625dd9db0be282de/.github/workflows/ci.yml) — CI orchestration and release-wheel artifacts.
- `docs/setup/SKILL.md` is named `astrid-setup`; it guides end-user installation and is not a developer release skill.

## Astrid App

Observed repository: [`banodoco/astrid-app`](https://github.com/banodoco/astrid-app), branch `main`, commit `d38edf434a575f3aed941c516fe2a5338135820b` (clean at inspection).

- [Deployment and migration guide](https://github.com/banodoco/astrid-app/blob/d38edf434a575f3aed941c516fe2a5338135820b/docs/structure_detail/deployment_and_migration_guide.md) — hosted bundle path and Docker/Railway source of truth.
- [Extension release runbook](https://github.com/banodoco/astrid-app/blob/d38edf434a575f3aed941c516fe2a5338135820b/docs/extensions/extension-release-runbook.md) — extension-only candidate and evidence procedure.
- [Extension release checklist](https://github.com/banodoco/astrid-app/blob/d38edf434a575f3aed941c516fe2a5338135820b/docs/video-editor/extension-platform-release-checklist.md) — canonical checklist data for that RC lane.
- [Installer pin implementation](https://github.com/banodoco/astrid-app/blob/d38edf434a575f3aed941c516fe2a5338135820b/scripts/installer/pin.mjs), `scripts/installer/release-check.mjs`, and `public/install-manifest.json` — shared Agent/Runtime compatibility tuple and monotonic release guard.
- [Served manifest canary](https://github.com/banodoco/astrid-app/blob/d38edf434a575f3aed941c516fe2a5338135820b/.github/workflows/served-manifest-canary.yml) — checks public deployed manifest coherence; it is not a deploy action.
- No developer release `SKILL.md` was found in the inspected App checkout or bounded workspace candidate; these docs and tools are the source for this central workflow.
