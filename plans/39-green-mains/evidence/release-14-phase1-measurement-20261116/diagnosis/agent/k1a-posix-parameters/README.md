# K1a five POSIX gate migrations

Bounded implementation evidence for the five authorized gate scopes. Repository: `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`. Base: `7e78fd7846b3271d30ed5f32900d68d9ecbee921` (clean before the change). Only three test files were edited. No registry, workflow, expectation, product behavior, scanner, or CI files changed.

## Ownership and lane boundary

Read `/workspace/scratch/cd53b069f320/p39-g2-evidence/k1-ownership-resolution.md` before editing. It classifies the native audit-token test as the Plan38 hold, and describes Plan38 ownership as process birth identity, native tokens, peer custody, and shared source closure; Plan55 covers warm local job execution, resident sessions, transport, settlement, and invocation. None of the five selected contracts tests those behaviors. The excluded `test_host_cleanup_ack_barrier.py::test_native_exec_changes_token_without_changing_process_lifetime` was not edited.

All new marks use the already registered `posix_native` lane (`tests/lanes.py:132`), which is available on `os.name == "posix"`, is not default-off, and maps to Ubuntu `unit-shard` coverage. This is equivalent for supported Windows/Linux/macOS runners to the removed OS gates. On POSIX, the tests were already in default selection; on Windows, they were already excluded by the old guards. No mark was added to the separate filesystem filename-creation exception in model verification.

## Exact selected proof

Both pre and post runs used the same exact selectors through the canonical wrapper. The wrapper command used `-q -rA` and emitted JUnit XML outside the repository:

```sh
bash scripts/worker-env/agent-pytest.sh -q -rA --junitxml=/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-parameters/{before,after}.xml \
  tests/core/generation/test_model_verification_record.py::test_non_utf8_filename_hashes_then_reuses \
  'tests/core/pack/test_verified_relocations.py::test_forged_personal_relocation_is_rejected[public]' \
  'tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[partial]' \
  'tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[oversized]' \
  tests/packs/runpod/test_failure_diagnostics.py::test_partial_ipc_from_unkillable_caller_returns_with_pending_fence
```

The shell scripts in this directory record the exact individual pre/post command, log redirection, and exit capture. Both exit files contain `0`; both logs report exactly six passed cases. The JUnit node inventories (`before.xml.nodes.json`, `after.xml.nodes.json`) match exactly:

1. `tests/core/generation/test_model_verification_record.py::test_non_utf8_filename_hashes_then_reuses`
2. `tests/core/pack/test_verified_relocations.py::test_forged_personal_relocation_is_rejected[public]`
3. `tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[partial]`
4. `tests/packs/runpod/test_failure_diagnostics.py::test_bounded_observer_rejects_malformed_or_late_child_frame[oversized]`
5. `tests/packs/runpod/test_failure_diagnostics.py::test_partial_ipc_from_unkillable_caller_returns_with_pending_fence[False]`
6. `tests/packs/runpod/test_failure_diagnostics.py::test_partial_ipc_from_unkillable_caller_returns_with_pending_fence[True]`

The literal JUnit names are recorded in the JSON inventories; no broad file selection or extra collection was used.

## Change boundary

- Model verification: the POSIX OS guard is now `@pytest.mark.posix_native`; the independent filename-creation `try/except` skip remains unchanged.
- Verified relocation: only the `public` parameter receives `posix_native`; the other five forgery parameters remain unchanged. The whole-test Windows skip is removed.
- Failure diagnostics: only `partial` and `oversized` receive `posix_native`; `late` and `eof` remain untouched. The partial-IPC test receives the mark while preserving both `early_abort` values.

`patch.diff` contains the exact product diff. `ast-equivalence.py` and `ast-equivalence.json` show module AST equality after normalizing only these gates. The public-parameter IDs are explicitly checked as `original`, `selection`, `digest`, `reused`, `outside`, and `public`; only `public` carries `pytest.mark.posix_native`. `git diff --check` passed. These are selected proofs of the six requested nodes, not full-file or suite results, not a full skip-policy result, and not formal RS1/K1a completion.
