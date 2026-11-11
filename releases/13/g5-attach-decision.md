# G5: choose one attach design

**Status: Recommended, awaiting orchestrator.** This record recommends a choice. It is not a merge and not acceptance. The orchestrator makes the final choice.

**Recommendation:** keep Release 12's owner-credential attach (`3639d63d`) and drop the Runtime-side variant. The Runtime pin becomes `42ae24aff8d2cb854f874ce134161077a3ba3641` in both Agent lock files. Keep the generation error contract (`e724eb50`..`e1731b9e`) and the lifecycle probe fix (`fa2dcaa1`). Neither depends on Runtime `8b312c4b`.

## The bug

Resident pack-host attach (`astrid machines setup`, before any claim) reads the host's executor record from Runtime with `GET /v1/executors/{id}`. In Runtime `42ae24aff`, that endpoint accepts only the owner with `admin` scope (`42ae24aff:runtime_protocol/server.py:1442`, `service.py:8287`). The Agent attach logs in with the **worker** credential (`1439ccc6:astrid/sdk/host_bootstrap.py:1894-1895`). Runtime rejects that request. The resulting `ApiError` becomes `live.check_raised` (`host_bootstrap.py:1921`), and the attach is refused. There was a second defect: the ready marker stored the typed `Executor` as a repr string inside a registration wrapper. Attach then could not see `source_epoch`/`source_digest`/`dependency_digest`. This is the 11 Nov installed failure in `plans/32-generation-placement-targets/tasks.md` ("installed proof failed").

## The two fixes

| | Release 12: Agent `3639d63d` (on `cand/29-r12` and `r12/cand-next`) | Generation: Runtime `8b312c4b` plus Agent `1edb88a0`, `992dbde1`, `8560b9c6`, `d7a38b94` |
|---|---|---|
| Who reads the executor | Attach reads the selected Runtime's `support_root/credentials/owner.token`. That file must be owner-only, current-user, and in the same directory as the worker credential. Attach checks `/health` status, epoch, instance and schema digest before `get_executor` (`3639d63d:astrid/sdk/host_bootstrap.py:1898-1919`). Runtime scope is unchanged. | Runtime widens `GET /v1/executors/{id}`: the owner with `admin`, **or** an actor equal to `executor_id` with `worker:execute` (`8b312c4b:runtime_protocol/server.py:1440-1447`, `service.py:8292`). Agent attach is unchanged and still uses the worker. `1edb88a0` re-pins the root lock and vendored client digest to `8b312c4b`. |
| Ready marker identity | After every successful (re)registration, the host republishes the marker through `_publish_ready_registration` (`3639d63d:astrid/core/execution/generic_host.py:7802`), with dataclasses serialized by `asdict` (`:14068`). Attach unwraps the nested record (`host_bootstrap.py:1926`). | `992dbde1` copies the identity fields to the top of the startup envelope (`1439ccc6:generic_host.py:1713`, `:17202`). It also makes `register_executor` reject a Runtime receipt that lacks or changes the submitted identity (`:1700`, `:5233`). |
| Runtime | `42ae24aff`, which Release 12 ships | `8b312c4b` (a child of `42ae24aff`: 5 commits, `git log --oneline 42ae24aff..8b312c4b`) |

Besides tests and generated digests, `8b312c4b` changes only that predicate and docs (`git diff --stat 42ae24aff 8b312c4b`: `server.py` and `service.py` at 11 lines each, `docs/executor-observation.md`, `contract/openapi/workspace-v1.yaml` description, digests, `tests/test_executor_self_observation.py`).

## What on the candidate needs `8b312c4b`

Only the worker-credential attach. On `1439ccc6`, the `/v1/executors/` callers are `host_bootstrap.py:1895` (worker attach), `astrid/packs/runpod/prepared_task.py:675` (owner `WorkspaceClient`, the same as `r12/cand-next:…prepared_task.py:786`), the TypeScript client and tests that use the owner token. The error contract, Plan 40, Plan 20 and the self-observe handoff do not call the executor observation endpoint. All focused runs below used `/home/user/wt/logs/g5/bin/run_focused.sh`. It puts the exact Agent and Runtime trees first on `PYTHONPATH` and records the import origins and both schema digests. Raw logs are in `/home/user/wt/logs/g5/runs/<label>/`, with hashes in `/home/user/wt/logs/g5/SHA256SUMS`.

| Label | Agent tree | Runtime | Selection | Exit | Result |
|---|---|---|---|---|---|
| A1i | `1439ccc6` | `8b312c4b` | `-m integration tests/sdk/test_host_attach_rejection.py::test_serialized_runtime_registration_attaches_and_tampering_refuses` | 0 | PASS, 1 passed |
| A2i | `1439ccc6` | `42ae24aff` | same | 1 | FAIL on schema digest (`2b23a675…` vendored vs `9628bb5f…` live), so this is a pin mismatch, not the bug |
| B1i | `1439ccc6` with `1edb88a0` reverted (uncommitted) | `42ae24aff` | same | 1 | FAIL `live.check_raised expected='completed' actual='ApiError'`: **the bug.** This is the focused test that passes with `8b312c4b` and fails with `42ae24aff` |
| C5i | B1 tree plus `3639d63d`'s two source hunks and a trial shim (below) | `42ae24aff` | `-m integration` trial `test_owner_attach_real_runtime_attaches_and_tampering_refuses` | 0 | PASS: real Runtime attach with the owner credential. Nested source epoch and digests tampered, and the legacy marker, are each refused. The worker credential alone is still refused on `get_executor` |
| C6 | C5 tree | `42ae24aff` | `-rA tests/sdk/test_host_attach_rejection.py` | 0 | PASS, 5 passed, including `test_registration_response_must_match_submitted_identity[*]` |
| D2 | C5 tree | `42ae24aff` | error-contract and lifecycle-probe selectors from `plans/32-…/evidence/release12-b5-focused-cpu.md`, minus attach | 0 | PASS, 12 passed |
| D3 | `1439ccc6` | `8b312c4b` | same | 0 | PASS, 12 passed |

D2 and D3 also put VibeComfy `8d065a8f` (git archive) and lifecycle `f2948817` on the path.

Failures and limits, kept as recorded:

- `INVALID-B1i` was run while the scratch worktree was still in the middle of a trial merge. It ran on the wrong tree, so it is NO-RESULT.
- C3i and C4i failed on my trial test's fixture: a fake `schema-1` and `rt-1` instead of the live digest and instance. I fixed the fixture, and C5i is the passing run. Product assertions were not changed.
- C3i also shows the candidate's own real Runtime test failing under Release 12's serializer, at `assert isinstance(ready["registration"]["registration"], str)`. Release 12 replaces that test; it does not regress it.
- C1 and C2 ran Release 12's unit attach tests from `3639d63d` on the partial composition. They could not run there, because they need Release 12 work the generation branch lacks: `missing_required_capabilities` (`89e5cbe5`), `_renew_executor_registration(deliberate=…)` (`bc96e5f3`) and `HostRegistrationError`. That is NO-RESULT for those tests until the Phase 1 merged head exists.
- The C5 shim is one class attribute, `missing_required_capabilities = ()`, standing in for `89e5cbe5`.
- The trial diff and tests are saved in `/home/user/wt/logs/g5/trial-composition/`. Nothing was committed to the Agent repo, and the scratch worktree is reset to `1439ccc6`.
- No installed product, App or GPU run was done.

## The 14 conflicting files

`git merge --no-commit --no-ff` of `origin/cand/29-r12` and of `origin/r12/cand-next` into `1439ccc6` both exit 1, with the same 14 files. Both merges were aborted. The lists are in `trial-merge-*-conflicts.txt`, and the per-file commit attribution is in `conflict-file-commits.txt`.

- **Caused by the attach fixes (2):**
  - `runtime.lock.json`: one hunk, `8b312c4b` against `42ae24aff`. Only `1edb88a0` causes it; before that commit both sides pinned `42ae24aff`.
  - `tests/sdk/test_host_attach_rejection.py`: the import line, then `992dbde1`/`8560b9c6` tests against `3639d63d`/`bcb5ac48` tests.
- **Mixed (1):** `tests/test_generic_host.py`. One block is appended on both sides: the generation side is Plan 32 T4g (`acbf3cd2`), the Release 12 side is `3639d63d` ready-marker tests. Keep both.
- **Other drift (11):**
  - `astrid/core/execution/orchestrator/runner.py`, `astrid/core/generation/asset_alignment.py`, `…/backends/vibecomfy.py`, `…/engine_local_endpoint.py`, `astrid/packs/h3_av/actions/transform/run.py` (deleted on the generation side), `astrid/packs/h3_av/shared/compile.py` (moved), `astrid/packs/runpod/adapter.py` and `astrid/sdk/invocation.py`: mostly Release 12's Ruff import sort (`7d1aea91`) against Plan 32 restructuring.
  - `astrid/core/generation/entries.py`: Release 12 fixes `a6ee9432`, `699e7913` and `2762a85a` against Plan 32.
  - `astrid/packs/runpod/target_selection.py`: `59afedd7`.
  - `tests/installed/test_installed_generation_package.py`: `4da7da9d` and `b1523f88` against Plan 32 T3.

**Silent hazard:** `astrid_runtime_client/contract_metadata.py` and `generated.py` merge *cleanly* to the `8b312c4b` digest `2b23a675…`, even though the lock conflicts. If the merge takes `42ae24aff` in the lock alone, the result is the A2i schema mismatch. `generic_host.py` also merges cleanly and runs both ready-identity designs at once.

## Two Agent lock files (manager's question)

At `1439ccc6`, the root `runtime.lock.json` says `8b312c4b` and the packaged `astrid/resources/runtime.lock.json` says `b983b0457dff…`. On both Release 12 heads, root is `42ae24aff` and packaged is still `b983b045`. The packaged copy last moved in `08533b59` (8 Nov). Every later pin commit changed only the root file: `e2a7fad0`, `7b08260d`, `4ad089ee` and `1edb88a0`.

1. **Which file each code path reads** (all cited at `1439ccc6`):
   - `runtime_lock_path(root)` resolves the installed `root/runtime.lock.json` first, then the package copy, then source (`astrid/core/rendering/_local_schema.py:151-155`, `astrid/core/product_resources.py:9-13`). In a checkout, it returns the root file.
   - The installer installs Runtime `manifest["runtime"]["sha"]` (`astrid/installer/backend.py:1242`). It copies the staged Agent's root lock to `product_root/runtime.lock.json` (`:1293-1294`) and verifies the schema against that root lock (`:689`). Before that copy exists, `_secure_installed_schema_inputs` resolves the lock to the packaged copy (`:209`). That is the only installed read of `b983b045`.
   - The pod bootstrap pins (`astrid/packs/runpod/managed_sources.py:48`, with `AGENT_ROOT` = `product_root` at `:19`) read `runtime_lock_path`, so they get the installer's root copy, and they must equal the manifest (`:59`). `remote_placement.py:166`, `:265` and `adapter.py:370` read `product_root/runtime.lock.json` directly. `pod_bootstrap.py` uses `requirements/runtime.lock`, a pip lock, not this JSON.
   - Importing the Runtime client reads neither lock. The wheel ships the vendored `astrid_runtime_client` (`pyproject.toml:111`), and its digest is hard-coded (`astrid_runtime_client/generated.py:20`).
   - The packaged copy is therefore a stale fallback. It is not the selector.
2. **`b983b045` in Runtime** (8 Nov, "CI: darwin-native installs the Agent non-editably…") is an ancestor of both pins. `git merge-base --is-ancestor b983b045 42ae24aff` exits 0, and the same check against `8b312c4b` exits 0. Neither pin is its ancestor (both reverse checks exit 1). It is 49 commits behind `42ae24aff`. It has the same schema digest `9628bb5f…` and the same owner-only executor GET (`b983b045:runtime_protocol/server.py:1436`). Its client file hashes and `producer_version` equal `42ae24aff`'s.
3. **Which Runtime the 10–11 Nov R12-F2 checks ran against.** All recorded as `8b312c4b`: the focused proofs, the failed installed proof, the installer retry and the direct installed attach/refusal check. Sources: `plans/32-…/tasks.md` R12-F2 entries and `evidence/release12-b5-focused-cpu.md`. The provisional Apps pin Runtime `8b312c4b` with Agents `1edb88a0` and `d7a38b94` (`astrid-app` `ab7977c5` and `43bad29f`: `public/install-manifest.json` `.runtime.sha`, and `runtime.lock.json`). The installer installs that manifest SHA, so the packaged `b983b045` copy never chose the Runtime. The raw receipts under `/workspace/r12-f2-*` are not on this host, so I could not check them. **"Needs `8b312c4b`" was proven only for the worker-credential attach design, against the manifest/root-lock Runtime. It was never proven against the packaged copy.** If that copy had chosen the Runtime, it would have refused attach exactly as `42ae24aff` does.

## Options

1. **Keep Release 12's fix and drop the Runtime-side variant (recommended).** It is already shipping. Runtime grants no new scope and stays at Release 12's pin. B1i shows the generation code needs nothing else from `8b312c4b`, and C5i, C6 and D2 prove the combination on `42ae24aff`.
2. **Keep the Runtime-side variant.** This needs a new Runtime pin for Release 13 above what Release 12 ships, coordinated App and Agent schema artifacts, a security review of the widened worker read, and installed re-proof. It also leaves two attach paths, because Release 12's owner path arrives with Phase 1 anyway.
3. **Keep both.** This violates "no two ways of doing one thing" and still needs the re-pin.

## What dropping it means at the Phase 1 merge

- **Pin:**
  - Take Release 12's side for `runtime.lock.json`, `astrid_runtime_client/contract_metadata.py` and `generated.py`. That is `42ae24aff`, digest `9628bb5f…`; it effectively reverts `1edb88a0`.
  - Check with `scripts/vendor_lock.py check runtime.lock.json --producer <42ae24aff checkout>`.
  - Separately, move `astrid/resources/runtime.lock.json` from `b983b045` to `42ae24aff`. This is shared Release 12 drift and the orchestrator's call.
- **`generic_host.py`:**
  - Remove `_ready_registration_envelope` and its startup call (`1439ccc6:…/generic_host.py:1713`, `:17202`). Release 12's structured marker and nested unwrap replace them, and the call's comment would become false.
  - Keep the `_executor_registration_identity` receipt check (`:1700`, `:5233`) and `d7a38b94`. They are independent and fail closed, and registration passed with them on `42ae24aff` (B1i, C5i).
- **`host_bootstrap.py`:** take Release 12's (it merges cleanly).
- **`tests/sdk/test_host_attach_rejection.py`:**
  - Keep both imports (`os`, `Path`), all of Release 12's tests, and `test_registration_response_must_match_submitted_identity`.
  - Replace `test_serialized_runtime_registration_attaches_and_tampering_refuses` with an owner-credential real Runtime version. `trial-composition/test_g5_trial_owner_attach_real_runtime.py` is a starting draft; it is not reviewed.
- **`tests/test_generic_host.py`:** keep both appended blocks.
- **Keep from `e1731b9e`'s branch:** `e724eb50`, `5611df87`, `069677c9`, `2c0c4a22`, `81df1507`, `e1731b9e` (the error contract) and `fa2dcaa1` (the lifecycle probe). None of them touches the Runtime contract.
- **Not needed:** Runtime `handoff/r12-self-observe` and its App schema artifacts.
- **Proof on the exact merged head:**
  - the Release 12 attach selectors: `tests/sdk/test_host_attach_rejection.py`, `tests/test_generic_host.py -k ready_marker`, `tests/sdk/test_host_recovery.py`
  - the ported real Runtime attach test, with `-m integration`
  - the D2 error-contract selectors
  - then one installed no-claim `machines setup` attach on the Phase 1 tuple

## Not verified

- Release 12's unit attach tests on a full merged head (C1 and C2 are NO-RESULT; the head does not exist yet).
- Installed or App behaviour of the recommended combination.
- The `/workspace` raw receipts for the 10–11 Nov checks.
- That the venv's lifecycle package equals `f2948817`. I put the lifecycle checkout at that SHA on the path, but the site-packages copy was not compared.
