# Plan 32 CI comparison — 26ee final candidate

## Run identity

- Candidate push CI: [run 42799672641](https://github.com/banodoco/astrid-agent/actions/runs/42799672641), head `26eeaff4f90fc5b91e25e0769477a9081deee5d3`.
- Baseline main CI: [run 42768047490](https://github.com/banodoco/astrid-agent/actions/runs/42768047490), head `a105de3a4852cb61b9647dfe2c920118bd29f272`.
- The candidate CI completed with failure. Logs were available for all jobs. The unit test command emitted `-rA`, but collection stopped before test IDs were reported. Main logs do not use `-rA`.

## Candidate and matching baseline jobs

| Candidate job | Result | Matching main job |
|---|---|---|
| [129773682579 boundary](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682579) | Passed | Not needed |
| [129773682279 fast checks](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682279) | Ruff gate failed at +119 findings | [129669093743](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093743) failed at +89; candidate count is +30 over main |
| [129773682800 Windows](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682800) | 13 failed, 23 passed; same 13 failures as main | [129669093846](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093846), same IDs/errors |
| [129773682700 wheel py3.11](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682700) | Installed `console-generate-list` smoke failed (`LaneExecutionError`, lane exit 1) | [129669093883](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093883), same smoke failure |
| [129773682652 wheel py3.12](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682652) | Installed `console-generate-list` smoke failed (`LaneExecutionError`, lane exit 1) | [129669093348](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093348), same smoke failure |
| [129773683225 unit shard 1](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773683225) | Collection exit 2; 23,557 deselected; same errors | [129669093701](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093701), same errors |
| [129773682932 unit shard 2](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682932) | Collection exit 2; 24,329 deselected; same errors | [129669093774](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093774), same errors |
| [129773682804 unit shard 3](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682804) | Collection exit 2; 25,404 deselected; same errors | [129669093808](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093808), same errors |
| [129773682836 unit shard 4](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682836) | Collection exit 2; 24,128 deselected; same errors | [129669093725](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093725), same errors |
| [129773682879 unit shard 5](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682879) | Collection exit 2; 23,826 deselected; same errors | [129669093720](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093720), same errors |
| [129773682904 unit shard 6](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682904) | Collection exit 2; 25,064 deselected; same errors | [129669093750](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093750), same errors |
| [129773683089 unit shard 7](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773683089) | Collection exit 2; 25,879 deselected; same errors | [129669093891](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093891), same errors |
| [129773682776 unit shard 8](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682776) | Collection exit 2; 26,087 deselected; same errors | [129669093912](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093912), same errors |
| [129773682796 Darwin](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129773682796) | Collection exit 2; 28,003 deselected; same errors | [129669093748](https://github.com/banodoco/astrid-agent/actions/runs/42768047490/job/129669093748), same errors |
| [129791985275 unit aggregate](https://github.com/banodoco/astrid-agent/actions/runs/42799672641/job/129791985275) | Skipped after shard collection failures | Main aggregate does not provide test-result IDs |

All eight unit shards and Darwin reported the same three collection errors:

1. `tests/pack_builder/test_pack_build.py` — `KeyError: 'ASTRID_BUILD_TEST_ESBUILD'`.
2. `tests/packs/test_b2_integrated_closure.py` — collection error.
3. `tests/packs/test_pack_layout_contract.py` — collection error.

Windows failures were the 12 parametrizations of `tests/core/rendering/test_remotion_host_regressions.py::test_declared_render_worker_controls_are_refused_before_launch`: `NODE_OPTIONS`, `PYTHONUTF8`, `LD_LIBRARY_PATH`, and `GIT_DIR`, each with `env_passthrough`, `command_env`, and `required_env`. All reported `PackInstallError: Group custody requires a supported POSIX filesystem.` The 13th was `test_captured_orchestrator_uses_platform_descriptor_launch`, failing with WinError 2 for missing `external_pkg`. The exact same failures appear in main's Windows job.

## Comparator result and limitation

Ran `astrid-dev/env/baseline-diff.py` against all eight candidate shard logs and the corresponding eight main shard logs:

```text
python astrid-dev/env/baseline-diff.py \
  --baseline main=/tmp/main2-129669093701.log,/tmp/main2-129669093774.log,/tmp/main2-129669093808.log,/tmp/main2-129669093725.log,/tmp/main2-129669093720.log,/tmp/main2-129669093750.log,/tmp/main2-129669093891.log,/tmp/main2-129669093912.log \
  --candidate /tmp/ci16-shard1.log,/tmp/ci16-shard2.log,/tmp/ci16-shard3.log,/tmp/ci16-shard4.log,/tmp/ci16-shard5.log,/tmp/ci16-shard6.log,/tmp/ci16-shard7.log,/tmp/ci16-shard8.log \
  --out /tmp/ci16-diff
```

It exited 2: `baseline-diff: a side has no PASSED/FAILED lines; run pytest with -rA`. Candidate and main both stopped during collection, so neither side has test-level result IDs for the comparator. No passed test IDs were observed. Matching collection errors provide baseline evidence for those collection failures; they do not establish that all tests pass or that there are no regressions elsewhere.

## Timings and follow-up

Compared each candidate test-step duration with the same main shard's duration:

| Step | Candidate | Main | Candidate / main | Result |
|---|---:|---:|---:|---|
| Unit shard 1 | 35m39 | 30m51 | 1.16× | Below 1.5× |
| Unit shard 2 | 33m02 | 30m26 | 1.08× | Below 1.5× |
| Unit shard 3 | 33m00 | 34m36 | 0.95× | Below 1.5× |
| Unit shard 4 | 18m29 | 18m26 | 1.00× | Below 1.5× |
| Unit shard 5 | 33m12 | 17m28 | 1.90× | Slow; collection still failed identically |
| Unit shard 6 | 29m49 | 33m42 | 0.89× | Below 1.5× |
| Unit shard 7 | 29m52 | 18m52 | 1.58× | Slow; collection still failed identically |
| Unit shard 8 | 22m59 | 19m41 | 1.17× | Below 1.5× |
| Darwin | 29m23 | 32m00 | 0.92× | Below 1.5× |

Shards 5 and 7 are nonblocking timing follow-ups because each exceeded 1.5× its matching main step. All shards and Darwin ultimately produced the same three baseline collection errors. A later focused investigation can use `--durations=30` and fake clocks; no local full suite was run for this comparison.
