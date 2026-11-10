# Tasks: repository cleanup

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../README.md)

**Draft only; no executable assignments are ready.** Task IDs, breakdown, routes, dependencies, selectors, review rounds, and per-task acceptance evidence must be scoped after inspecting current sources. Do not infer assignments or readiness from this outline.

## Intended work

- Inventory tracked files. Distinguish product code, tests, generated assets, useful examples, historical evidence, and temporary material; establish references and packaging use before removal.
- Remove only demonstrably obsolete or duplicated scripts, documentation, artifacts, or dead code. Consolidate competing instructions and entry points by purpose.
- Move useful examples or historical documentation to an appropriate home and repair links. Preserve unpublished work, active experiments, required package data, and evidence still supporting releases.
- Coordinate where agent catalogs or integration instructions overlap, leaving one authoritative extension path.
- Check only affected imports, entry points, packaging, documentation links, and named feature behavior. No repository-wide test run or automatic test discovery.

## Scoping boundary

Before dispatch, inspect the source identities and work recorded in [inputs.md](inputs.md), agree the bounded cleanup inventory, then assign IDs and difficulty/routes, dependencies, focused selectors, acceptance evidence, and existing review/publication limits. Missing selectors must be identified during setup, not invented here.

## Review follow-ups (Plan 32 review, 9 Nov, at 7209ffcc7)

**When (owner, 10 Nov):** start the RunPod items below (the prepared-worker island, the unused RunPod release code) only after Plan 34's first GPU run is recorded, because that run exercises `astrid/packs/runpod/`. The flags item can go any time after Plan 32's completion PR merges.

- **Prepared-worker island: audit, then delete (N, Medium).** `RunPodRemoteWorkerPreparer`, `PreparedRunPodHost`, `RunPodWarmSessionOwner` and `RunPodRemoteWorkerInspector` (`astrid/packs/runpod/worker_owner.py:538,915,937,2358`) appear referenced only inside `worker_owner.py` and `prepared_task.py`; with `worker_process.py`, `worker_staging.py`, `worker_session.py` and `installed_session.py` that is about 8,000 lines. Step 0 is a reachability audit (grep found no caller; not proven dead). The `generic_host.py` and `run.py` plumbing goes with [Plan 13](../13-execution-host-refactor/tasks.md). Also in scope, per the Plan 32 fix7 review (9 Nov): `_ProductionPreparedTaskRuntime._components` with its RunPod account-ref refusal (`prepared_task.py:608`), reached only via `PreparedWorkerSelection.bind_client` → `PreparedRunPodGeneration.bind_client` (`runpod/generation.py:201-214`), which nothing calls; the machine route uses `prepare_retained_generation` (`machine.py:469`, `adapter.py:18`). Its tests are in `test_prepared_task.py` and the `test_https_transport.py:236` stanza.
- **Unused RunPod release code (N, Medium).** Delete `astrid/packs/runpod/h3_release*.py` (934 lines), `gpu_sanity.py` and, if nothing live needs it, `model_downloader.py` (701 lines; kept mostly for the release code, per `tests/core/generation/test_run_local.py:131-140`), with their script and test users.
- **Legacy generate flags (N, Low).** Remove the `--model` "legacy selector" and `--execution` flags (`astrid/core/generation/cli.py:177,183`) after checking callers. The TOML-import removal date is [Plan 35](../35-one-home-for-user-state/tasks.md)'s.
