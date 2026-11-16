# K1a POSIX installer tests

Base checkout: `ab729c533ce8ee29118530c99447dd09fb45dc4e`
Branch: `p39/k1a-posix-publish`

## Scope and gate equivalence

Migrated only these five pre-existing OS gates:

- Three `tests/test_installer_git_executable.py` tests for POSIX symlinks and executable fixtures.
- The module marks in `tests/installer/test_installed_lock_resolution.py` and `tests/installer/test_umask_0002_schema.py`, both covering POSIX modes.

Existing `posix_native` policy in `tests/lanes.py` is a platform lane with `os.name == "posix"`, run by the Ubuntu default unit lane. The old gates excluded Windows (`os.name == "nt"` or `sys.platform == "win32"`) and ran on the current POSIX CI OS; the new marker preserves that current CI selection and Windows exclusion. The installer module files still use `os` for `umask`; their `sys` imports were removed because they were used only by the replaced gates.

## Focused proof

Command:

```sh
bash scripts/worker-env/agent-pytest.sh -q \
  tests/test_installer_git_executable.py::test_path_alias_to_cwd_is_never_executed_or_recorded \
  tests/test_installer_git_executable.py::test_recorded_symlink_is_canonical_and_survives_retarget \
  tests/test_installer_git_executable.py::test_path_git_symlink_is_recorded_as_its_canonical_target \
  tests/installer/test_installed_lock_resolution.py \
  tests/installer/test_umask_0002_schema.py
```

Base, before edit: `6 passed in 0.95s`, exit 0.
Candidate, after edit: `6 passed in 0.91s`, exit 0.

Complete captured stdout/stderr and exit codes are in `before.log` and `after.log`.

## Static checks

- AST comparison against base: all three selected test function signatures/bodies/parameterization unchanged; all functions in both module test files unchanged in signatures/bodies/parameterization.
- `git diff --check`: passed.
- Only the three requested files changed; only the five requested gates changed, plus removal of the two now-unused `sys` imports.

Commit: `6c06460d3e7b46001f9d57e5b011cb114bfa23d0`
Parent: `ab729c533ce8ee29118530c99447dd09fb45dc4e`
Tree: `6336201f0ee7a042c80695f9449248ff1609d05a`

Additional artifacts: `change.patch` and `commit.txt`.
