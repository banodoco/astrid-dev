# Release 13 test table

Kept by the Release 13 test manager ([brief](test-manager-brief.md)). There is one row per failing or missing test id, or per job with no result. Results are sorted only with `env/baseline-diff.py`, by the rules in [`astrid-dev-green`](../../skills/astrid-dev-green/SKILL.md) (once #572 merges).

## Latest comparison

**None yet.** The first comparison runs when these runs finish:
- Agent CI `43254543283` on `int/r13` at `f9214240`;
- Agent CI `43264364443` on `int/r13-next` at `fc4b36d4`;
- Agent Lanes `43268483674` on `r13/compose` at `9f9db742`, which is `fc4b36d4` plus the Lanes fix.

**Baselines,** all at R12 `main` `0e1543e0`:
- CI `43155525231`;
- CI `43134432721`, attempts 1 and 2 (the same SHA, on `cand/29-r12`);
- shard 5 from CI `43264595988`, on scratch `r13/tests/baseline-r12` `5d108da7` (R12 plus `--ignore=tests/sdk/test_h3_endpoint_r4.py`, which changes coverage; the release manager rules at the binding run);
- Lanes `43155525276` (push) and `43205560755` (schedule).

| Bucket | f9214240 | fc4b36d4 |
|---|---|---|
| 1 regression | pending | pending |
| 2 new test failing, R13 behaviour | pending | pending |
| 3 new test failing, defect already on R12 | pending | pending |
| 4 preexisting | pending | pending |
| 5 missing | pending | pending |
| 6 flaky | pending | pending |
| UNSORTED (no baseline yet) | pending | pending |

## Rows

| id | bucket | candidate SHA | cause | introduced by | owner | disposition | link |
|---|---|---|---|---|---|---|---|
| Lanes: all 5 test jobs (opt-in, integration 1–4) | 1 (NO-RESULT, job-level) | f9214240, fc4b36d4 | "Read the pinned VibeComfy revision" raises `UnknownEngine: vibecomfy`, so 0 tests run | `cff69d9c` moved `ci.yml` to `scripts/vibecomfy_pin.py` and missed `lanes.yml` | test manager | fixed: `895d08c8`, merged in `r13/compose` `9f9db742`; hosted proof pending, Lanes `43268483674` | agent `r13/tests/lanes-vibecomfy-pin` |
| `tests/test_skip_policy.py::test_no_test_file_skips_by_hand` | 4 (49 offenders on R12) | f9214240 (57) | R13 added 5 hand skips, each hiding a test | `07ed95f3`, `9deeef5b`, `15db432f`, `09724310`, `feea4ac6` | test manager (3), engine lane (2) | 3 fixed and merged (`72a6db07` run-logs; `f9f109e7` G3 ×2); 2 relayed to the engine lane (`r13/engine-skips`) | release manager rule: run with the skip removed first |
| `tests/test_vibecomfy_pin.py::test_no_other_tracked_file_copies_the_pin` | UNSORTED | f9214240 | the pin is copied in `test_engine_cli.py`, `test_engine_recipe.py` and `test_installer_sources.py` | pending | pending | pending the comparison | — |
| `tests/integrations/test_remote_machine_cpu.py::test_resolved_runpod_policy_controls_the_claim_and_warm_hold` | UNSORTED | f9214240 (local) | teardown: `AcquisitionUnresolvedError`, then `RunPodWorkerOwnerError`, then `CustodyError` "host graph cleanup remains unresolved" (`generic_host.py:7164`) | pending | machines lane if bucket 1 or 2 | pending the comparison | W07 local run |
| `tests/sdk/test_h3_endpoint_r4.py::*` (all ids) | 5 (missing) | f9214240 | file deleted | `3079370d` (Plan 32 T6b-3, retires the h3 stage actions) | — | ruling by the release manager (12 Nov): removed on purpose. Applies once W06 Part D confirms the commit removes exactly the covered behaviour | — |

## Plan 39 rows to open

- **R12 unit shard 5 never finishes.** On `main` `0e1543e0`, `tests/sdk/test_h3_endpoint_r4.py`'s tests hit the 600 s pytest-timeout in turn (leaked `serve_forever` threads). The shard is cancelled at 120 min, 43% through 4,471 tests, in all three R12 runs. The file is gone in R13.

## Plan 50 evidence (offline checks)

Stage 1 live, 12 Nov: three failures a CPU check should have caught (owned and being fixed by the release manager's lanes):
- SFX: VibeComfy refused `CHOICE` against `COMBO` on a public input.
- TTS: transformers 5 dropped `pad_token_id` from the node's config.
- Music: VibeComfy's stale first-build digest.
