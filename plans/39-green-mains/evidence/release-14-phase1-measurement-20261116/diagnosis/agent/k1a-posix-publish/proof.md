# K1a POSIX native publication tests

Base checkout: `ba0bec4a803c959d476887fbcf51f8594e312ff7`
Working branch: `p39/k1a-posix-publish`

## Focused proof

Selectors:

```sh
bash scripts/worker-env/agent-pytest.sh -q \
  tests/core/pack/test_windows_publish.py::test_posix_sync_flushes_files_and_all_directories \
  tests/core/pack/test_windows_publish.py::test_posix_directory_open_failure_is_not_ignored \
  tests/core/pack/test_windows_publish.py::test_windows_sync_preserves_group_update_and_rollback
```

Base, before edit:

```text
....                                                                     [100%]
4 passed in 3.99s
```

Candidate, after edit:

```text
....                                                                     [100%]
4 passed in 3.07s
```

The first function remains parameterized over `platform=["linux", "darwin"]`; the other two remain single cases.

## Static and policy checks

- AST comparison against the base confirms these exact three function signatures and bodies are unchanged, and their parameterization is unchanged.
- `tests/lanes.py` registers `posix_native` as a platform lane available when `os.name == "posix"`, run in `unit-shard-ubuntu-latest`. The lane hook adds the declared lane skip when unavailable, preserving Windows exclusion.
- `tests/test_lane_registry.py` confirms platform lane jobs run the default pytest lane, and the `posix_native` job is Ubuntu. `.github/workflows/ci.yml` unit shard runs the default lane. The Windows native job has separate explicit selectors and does not claim these tests as native Windows coverage.
- `git diff --check`: passed.

## Scope

Only the three direct `skipif` decorators in `tests/core/pack/test_windows_publish.py` changed to `pytest.mark.posix_native`. No function bodies, imports, parameters, registry entries, or other files changed.

Commit: `ab729c533ce8ee29118530c99447dd09fb45dc4e`
Parent: `ba0bec4a803c959d476887fbcf51f8594e312ff7`
Tree: `18b1d5278960c8532d5403c3eebfc9f5f691a1a0`

Additional artifacts in this directory: `change.patch` (exact committed diff) and `commit.txt` (commit metadata).
