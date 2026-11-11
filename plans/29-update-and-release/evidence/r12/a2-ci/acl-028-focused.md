# Group 028 ACL focused reproduction

On 11 Nov, under an exclusive host window, the exact selector `tests/test_installer_acl.py::test_windows_staged_version_folder_is_a_protected_record_parent` ran once per frozen side with `-vv --tb=long -p no:cacheprovider`, `PYTEST_ADDOPTS=-rA`, a distinct `acl028` basetemp, sanitized `env -i`, and the matching side's existing Python venv, HOME, TMPDIR, cache, VibeComfy, Runtime and lifecycle checkouts under `/workspace/r12-a2-resume`.

- Base Agent `313bbd46f1e24bfe635655d78b27ab0b321145d5`: exit 0, 1 passed, pytest 2.22 seconds.
- Candidate Agent `ec48555d8298d155390ffbb37d1950c3e80b43a4`: exit 1, 1 failed, pytest 3.74 seconds. The folder privacy assertion passed; `_runtime_private_read(folder / "manifest.json")` failed because the mocked first source call raised before the candidate wrote that file.

The focused stdout/stderr was returned directly in the worker tool result and was not redirected to durable log files. This confirms the local staging-order difference, but does not by itself determine whether earlier staged-manifest behavior or the test's stop point is the correct release contract. It is not native Windows proof and does not establish full comparison parity.

For the original reproduction, run the following from each frozen Agent checkout, substituting `SIDE=base` or `SIDE=candidate` and using the corresponding prepared side environment. The local paths describe the original machine; a new machine must first recreate and verify the pinned side checkouts and Python environment using the recorded A2 setup.

```bash
SIDE=base  # repeat with candidate
TASK_ROOT=/workspace/r12-a2-resume
cd "$TASK_ROOT/$SIDE"
env -i PATH="$TASK_ROOT/$SIDE.env/venv/bin:/usr/local/bin:/usr/bin:/bin" \
  HOME="$TASK_ROOT/$SIDE.env/home" TMPDIR="$TASK_ROOT/$SIDE.env/tmp" \
  XDG_CACHE_HOME="$TASK_ROOT/$SIDE.env/cache" LANG=C.UTF-8 \
  PYTEST_ADDOPTS=-rA PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 PYTHONSAFEPATH=1 \
  PYTHONPATH="$TASK_ROOT/$SIDE.env/vibecomfy" VIBECOMFY_SOURCE="$TASK_ROOT/$SIDE.env/vibecomfy" \
  ASTRID_RUNTIME_CHECKOUT="$TASK_ROOT/$SIDE.env/runtime" \
  ASTRID_VIBECOMFY_CHECKOUT="$TASK_ROOT/$SIDE.env/vibecomfy" \
  ASTRID_TEST_LIFECYCLE_CHECKOUT="$TASK_ROOT/$SIDE.env/lifecycle" \
  "$TASK_ROOT/$SIDE.env/venv/bin/python" -m pytest -vv --tb=long -p no:cacheprovider \
  --basetemp="$TASK_ROOT/$SIDE.env/basetemp/acl028" \
  tests/test_installer_acl.py::test_windows_staged_version_folder_is_a_protected_record_parent
```
