# K1a POSIX recovery gate migrations

Bounded implementation on Agent base `cfabc7dabeceef6340809db22f895e7952fc8cfd` in `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`. The card's expected count said four, but the three named selectors expand to six parameterized node IDs: three publication cuts, one disable/recovery case, and two stop cuts. Root confirmed that all six named-selector cases govern. The captured six-pass baseline is retained; it was not rerun.

## Ownership and selection

Read `/workspace/scratch/cd53b069f320/p39-g2-evidence/k1-ownership-resolution.md`. It assigns Plan38 birth identity, native tokens, peer custody, and source closure; Plan55 owns warm local job execution, resident sessions, transport, settlement, and invocation. These tests exercise fake launchd/systemd manager recovery around durable installer/registration publication and SIGKILL cut points. They do not assert native process identity/token behavior or generation-job execution. No ambiguity requiring a stop was found.

All replacements use `pytest.mark.posix_native` (`tests/lanes.py:132`), available when `os.name == "posix"`, not default-off, and mapped to Ubuntu unit-shard. On supported Ubuntu and Windows runners this preserves the prior `hasattr(os, "fork")` eligibility; the POSIX fork tests were already part of default Ubuntu selection. No module marks, parameters, symlink capability skip, assertions, environment, dependency, or workflow changed.

## Proof

Pre and post used the exact same canonical-wrapper selection, with `-rA` and JUnit XML outside the repository:

```sh
bash scripts/worker-env/agent-pytest.sh -q -rA --junitxml=/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-recovery/{before,after}.xml \
  tests/test_boundary_registration_launchd.py::test_launchd_sigkill_after_publication_link_replays \
  tests/test_installer_r0_stop.py::test_killed_after_disable_next_invocation_recovers \
  tests/test_installer_r0_stop.py::test_launchd_sigkill_at_each_stop_step_then_recover
```

Both exits were `0`; both runs passed all six node IDs. The before/after JUnit inventories are identical (`before.xml.nodes.json`, `after.xml.nodes.json`): publication `[journal]`, `[launcher]`, `[definition]`; `test_killed_after_disable_next_invocation_recovers`; stop step `[disable]`, `[bootout]`. Complete logs and raw XML are retained.

`patch.diff` is the complete product diff. `ast_equivalence.py` / `ast-equivalence.json` establish module AST equality after removing only the old fork checks and normalizing the equivalent lane decorators. `git diff --check` passed. This is a focused proof of these six cases only; it is not a full policy result, overall K1a completion, or formal RS1.
