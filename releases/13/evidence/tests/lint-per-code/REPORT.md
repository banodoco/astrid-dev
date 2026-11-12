# W31 — Per-file Ruff and mypy regression gates

## Gate reproduction

| Gate / revision | Findings | Expected | Reproduced |
|---|---:|---:|---|
| Ruff R12 `0e1543e0da2215db9cb3320cfd1083174c3c62a9` | 2,128 | 2,128 | Yes |
| Ruff compose head `d5ed516204f89141d51090c602ab0690985999ef` | 2,117 | 2,117 | Yes |
| mypy R12 `0e1543e0da2215db9cb3320cfd1083174c3c62a9` | 2,338 | 2,338 | Yes |
| mypy reused candidate `913c6b8fff8c63aeb05cb1b5ae160463f6d5e641` | 2,420 | 2,420 | Yes |

Ruff positive `(file, code)` deltas total 59, despite a net total change of −11. Mypy positive `(file, error code)` deltas total 179; the net change is +82 because negative per-file/code changes offset positive rows. Ruff uses newest remote compose head `d5ed5162`; mypy uses the specifically supplied 913c6b8f findings and reproducing gate.

## Ruff positive rows

Counts are positive deltas by file and code. Commits are candidate-line blame for the unmatched candidate diagnostics, matched by `(file, code, message)`.

### Machines

| File | Code | Delta | Introducing commits |
|---|---|---:|---|
| `astrid/core/execution/generic_host.py` | I001 | 2 | e862934c |
| `astrid/core/execution/machine_run.py` | BLE001 | 1 | 14155ab3 |
| `astrid/core/execution/phase_timing.py` | BLE001 | 2 | 3bcd524e |
| `astrid/core/machines_cli.py` | BLE001 | 6 | 7d8239a6, c0f505d4, 4960d98d, 3ce1c970, 74862541 |
| `astrid/installer/backend.py` | I001 | 1 | e862934c |
| `astrid/packs/runpod/machine.py` | BLE001 | 17 | f001318c, 3bcd524e, 80bbf690, b6c17c8f, d1ed6a7d, 4a21520a, b6d6da56, e75a5a8e |
| `astrid/packs/runpod/managed_sources.py` | I001 | 1 | 3e551fde |
| `astrid/packs/runpod/storage_probe.py` | BLE001 | 1 | 3e551fde |
| `astrid/packs/runpod/target_selection.py` | BLE001 | 3 | 080b797b, 3e551fde |
| `astrid/packs/runpod/worker_owner.py` | BLE001 | 2 | 3e551fde |
| `astrid/sdk/generation.py` | I001 | 3 | b4e66cc3 |

### Engine

| File | Code | Delta | Introducing commits |
|---|---|---:|---|
| `astrid/core/generation/asset_alignment.py` | BLE001 | 1 | a290dc69 |
| `astrid/core/generation/cli.py` | BLE001 | 2 | 80bbf690 |
| `astrid/core/generation/defaults.py` | BLE001 | 3 | ee3015a5 |
| `astrid/core/generation/engine_runner_target.py` | F401 | 1 | b1830b9e |
| `astrid/core/generation/entries.py` | BLE001 | 2 | f001318c, 2762a85a |
| `astrid/core/generation/managed_preparation.py` | BLE001 | 1 | 80d30156 |
| `astrid/core/generation/managed_preparation.py` | F841 | 1 | 993fd926 |
| `astrid/core/generation/placement.py` | BLE001 | 1 | cef4da11 |
| `astrid/core/generation/settings.py` | BLE001 | 1 | ee3015a5 |
| `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py` | BLE001 | 1 | 75e55310 |
| `astrid/packs/vibecomfy/local_server_engine.py` | BLE001 | 1 | 86778e33 |
| `astrid/packs/vibecomfy/local_server_engine.py` | I001 | 1 | b4e66cc3 |

### Test manager

| File | Code | Delta | Introducing commits |
|---|---|---:|---|
| `astrid/core/gateway/dispatch.py` | E402 | 1 | cdc1774a |
| `astrid/packs/h3_av/cli.py` | I001 | 1 | 974a5081 |
| `astrid/packs/h3_av/shared/compile.py` | F841 | 1 | e862934c |
| `astrid/sdk/invocation.py` | BLE001 | 1 | e862934c |

## Mypy positive rows

Counts use the requested reused normalized mypy outputs. Commits blame candidate warning lines from 913c6b8f. Normalized message multiset comparison yields 192 added and 110 removed findings; only 179 positive per-file/code counts remain after aggregating by code. `astrid/packs/runpod/remote_placement.py` `union-attr` has 8 added normalized messages but a per-file/code delta of 7, so its commit set is a line-level lead for that row.

### Machines

| File | Error code | Delta | Introducing commits |
|---|---|---:|---|
| `astrid/core/execution/machine_run.py` | assignment | 1 | 3bcd524e3 |
| `astrid/core/machines_cli.py` | arg-type | 4 | 7d8239a64,748625413,0253d3b46 |
| `astrid/core/machines_cli.py` | index | 1 | 644f1a280 |
| `astrid/installer/backend.py` | arg-type | 1 | 0f584c920 |
| `astrid/packs/runpod/adapter.py` | operator | 2 | 16ffaa601 |
| `astrid/packs/runpod/adapter.py` | type-var | 2 | 16ffaa601 |
| `astrid/packs/runpod/adapter.py` | union-attr | 1 | d91818db1 |
| `astrid/packs/runpod/failure_receipt.py` | arg-type | 1 | 30795fec8 |
| `astrid/packs/runpod/generation.py` | arg-type | 1 | b6c17c8fc |
| `astrid/packs/runpod/generation.py` | union-attr | 3 | 9e7b2a481 |
| `astrid/packs/runpod/machine.py` | arg-type | 6 | c6c805cc3,65d766afb,3bcd524e3,d072cf5da |
| `astrid/packs/runpod/machine.py` | assignment | 1 | 80bbf6904 |
| `astrid/packs/runpod/machine.py` | attr-defined | 13 | 9e7b2a481,14155ab34,80bbf6904,3bcd524e3,80a437c26,d072cf5da |
| `astrid/packs/runpod/machine.py` | call-arg | 2 | b6c17c8fc,d27d79b88 |
| `astrid/packs/runpod/machine.py` | dict-item | 1 | d072cf5da |
| `astrid/packs/runpod/machine.py` | operator | 3 | 80bbf6904,9e7b2a481 |
| `astrid/packs/runpod/machine.py` | union-attr | 2 | 3bcd524e3,d072cf5da |
| `astrid/packs/runpod/pod_fields.py` | arg-type | 1 | e6d857667 |
| `astrid/packs/runpod/provider.py` | arg-type | 3 | ad7723a8f |
| `astrid/packs/runpod/remote_placement.py` | arg-type | 1 | a72ad64f1 |
| `astrid/packs/runpod/remote_placement.py` | assignment | 2 | dd20b74b0,a72ad64f1 |
| `astrid/packs/runpod/remote_placement.py` | operator | 7 | 4a21520aa,15e212016 |
| `astrid/packs/runpod/remote_placement.py` | union-attr | 7 | 80bbf6904,993fd926e,b4e66cc3c |
| `astrid/packs/runpod/target_selection.py` | arg-type | 6 | 0a7de39c1,2d905bd52,16ffaa601 |
| `astrid/packs/runpod/target_selection.py` | assignment | 2 | 14155ab34 |
| `astrid/packs/runpod/target_selection.py` | attr-defined | 3 | 14155ab34 |
| `astrid/packs/runpod/target_selection.py` | operator | 2 | 0a7de39c1,16ffaa601 |
| `astrid/packs/runpod/target_selection.py` | return-value | 1 | 16ffaa601 |
| `astrid/packs/runpod/worker_owner.py` | arg-type | 2 | d3c440236,d1ed6a7d6 |
| `astrid/packs/runpod/worker_owner.py` | attr-defined | 2 | 80bbf6904 |
| `astrid/packs/runpod/worker_owner.py` | dict-item | 1 | d1ed6a7d6 |
| `astrid/packs/runpod/worker_owner.py` | index | 2 | 80bbf6904 |
| `astrid/packs/runpod/worker_owner.py` | operator | 1 | d3c440236 |
| `astrid/packs/runpod/worker_owner.py` | return-value | 1 | c0f505d4d |
| `astrid/packs/runpod/worker_owner.py` | union-attr | 2 | d1ed6a7d6 |
| `astrid/sdk/generation.py` | assignment | 1 | cd27ed9d7 |
| `astrid/sdk/generation.py` | attr-defined | 10 | 335643a8f,b9a611eaa,1ae020677,b4e66cc3c,73fb63c7c,e4a0e8cc7,68b26db0a |
| `astrid/sdk/generation.py` | index | 5 | 73fb63c7c,974a50812,e4a0e8cc7 |
| `astrid/sdk/generation.py` | union-attr | 2 | 974a50812 |
| `astrid/sdk/generation.py` | valid-type | 1 | 73fb63c7c |

### Engine

| File | Error code | Delta | Introducing commits |
|---|---|---:|---|
| `astrid/core/generation/backends/vibecomfy.py` | union-attr | 2 | 7efe5bb65 |
| `astrid/core/generation/backends/vibecomfy_local_server.py` | var-annotated | 1 | 121a7af1a |
| `astrid/core/generation/cli.py` | arg-type | 2 | 80bbf6904 |
| `astrid/core/generation/cli.py` | assignment | 1 | 561d32a29 |
| `astrid/core/generation/defaults.py` | arg-type | 1 | ee3015a5a |
| `astrid/core/generation/engine_custody.py` | has-type | 1 | 2ac650593 |
| `astrid/core/generation/engine_recipe.py` | var-annotated | 1 | 3e551fded |
| `astrid/core/generation/entries.py` | assignment | 1 | 98dccc3c4 |
| `astrid/core/generation/job_inputs.py` | dict-item | 1 | fe411d26a |
| `astrid/core/generation/job_inputs.py` | misc | 1 | 4286515d8 |
| `astrid/core/generation/job_inputs.py` | union-attr | 4 | 4286515d8,fe411d26a |
| `astrid/core/generation/job_inputs.py` | var-annotated | 1 | 4286515d8 |
| `astrid/core/generation/local_job.py` | arg-type | 2 | 5f370640f,fe066bdc9 |
| `astrid/core/generation/managed_preparation.py` | assignment | 1 | 2ac650593 |
| `astrid/core/generation/managed_preparation.py` | index | 1 | d4da4927e |
| `astrid/core/generation/managed_preparation.py` | return-value | 1 | 2ac650593 |
| `astrid/core/generation/target_inventory.py` | index | 1 | ac1e8ffd0 |
| `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py` | arg-type | 1 | 75e553104 |
| `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py` | attr-defined | 2 | 100a239d6,4aae76278 |
| `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py` | import-untyped | 1 | 75e553104 |
| `astrid/packs/vibecomfy/local_job.py` | arg-type | 4 | 47e77a513,fe066bdc9 |
| `astrid/packs/vibecomfy/local_job.py` | assignment | 1 | 260ee2304 |
| `astrid/packs/vibecomfy/local_job.py` | index | 5 | fe066bdc9 |
| `astrid/packs/vibecomfy/local_job.py` | operator | 1 | 47e77a513 |
| `astrid/packs/vibecomfy/local_job.py` | union-attr | 1 | fe066bdc9 |
| `astrid/packs/vibecomfy/local_server_engine.py` | attr-defined | 1 | 878d13f46 |
| `astrid/packs/vibecomfy/local_server_engine.py` | index | 1 | 121a7af1a |

### Test manager

| File | Error code | Delta | Introducing commits |
|---|---|---:|---|
| `astrid/core/_shared/run_logs.py` | arg-type | 1 | 15db432fa |
| `astrid/core/_shared/run_logs.py` | operator | 2 | 15db432fa |
| `astrid/core/cli/domain_tasks.py` | override | 1 | 90ae9c314 |
| `astrid/core/cli/domain_tasks.py` | return-value | 1 | 9373955d4 |
| `astrid/core/cli/domain_tasks.py` | union-attr | 2 | cffffe056,90551c4f9 |
| `astrid/core/engine_cli.py` | union-attr | 2 | 72fbdf65c |
| `astrid/core/pack/validate_first_party.py` | assignment | 1 | 3e551fded |
| `astrid/installer/progress.py` | union-attr | 3 | f9d526f17 |
| `astrid/packs/generation/extensions/points/engine_protocol.py` | misc | 1 | 66e47777e |
| `astrid/packs/h3_av/cli.py` | arg-type | 1 | 3e551fded |
| `astrid/packs/h3_av/shared/compile.py` | arg-type | 1 | e862934c2 |
| `astrid/packs/h3_av/shared/generation.py` | union-attr | 2 | 75e553104 |
| `astrid/packs/h3_av/shared/prepare.py` | operator | 1 | 3e551fded |
| `astrid/packs/h3_av/shared/prepare.py` | union-attr | 1 | 3e551fded |
| `astrid/packs/h3_av/shared/verify.py` | arg-type | 2 | 3e551fded |
| `astrid/packs/h3_av/shared/verify.py` | assignment | 1 | 3e551fded |
| `astrid/sdk/invocation.py` | assignment | 1 | 16ffaa601 |
| `astrid/sdk/invocation.py` | operator | 2 | 16ffaa601 |
| `astrid/sdk/invocation.py` | union-attr | 1 | 05f10de9b |
| `astrid/skills/__init__.py` | assignment | 1 | 64b29bb7f |

## Totals by owner and code

### Ruff

| Owner | BLE001 | F821 | I001 | F401 | Other | Total |
|---|---:|---:|---:|---:|---:|---:|
| Machines | 32 | 0 | 7 | 0 | 0 | 39 |
| Engine | 13 | 0 | 1 | 1 | 1 | 16 |
| Test manager | 1 | 0 | 1 | 0 | 2 | 4 |
| **Total** | 46 | 0 | 9 | 1 | 3 | 59 |

Positive Ruff totals by code: BLE001 46, F821 0, I001 9, F401 1; other codes 3.

### Mypy

| Owner | Positive findings |
|---|---:|
| Machines | 110 |
| Engine | 41 |
| Test manager | 28 |
| **Total** | **179** |

Positive mypy totals by code: arg-type 41, assignment 15, attr-defined 31, call-arg 2, dict-item 3, has-type 1, import-untyped 1, index 16, misc 2, operator 21, override 1, return-value 4, type-var 2, union-attr 35, valid-type 1, var-annotated 3.

## Commands and inputs

Ruff ran using Python 3.11 environments and the repository CI target `make ruff` (from `.github/workflows/ci.yml`: checks installs `.[dev]`, then runs `make ruff`). Raw findings came from the same command embedded by `compare_ruff_baseline.py`.

```sh
git -C /home/user/astrid-agent ls-remote origin refs/heads/r13/compose
git -C /home/user/astrid-agent worktree add --detach /tmp/w31-compose d5ed516204f89141d51090c602ab0690985999ef
uv venv -q --seed --python 3.11 /tmp/w31-r12
uv pip install -q --python /tmp/w31-r12/bin/python -e '/home/user/wt/agent-r12[dev]'
cd /home/user/wt/agent-r12 && make ruff PY=/tmp/w31-r12/bin/python
cd /home/user/wt/agent-r12 && /tmp/w31-r12/bin/python -m ruff check . --output-format json
uv venv -q --seed --python 3.11 /tmp/w31-venv-compose
uv pip install -q --python /tmp/w31-venv-compose/bin/python -e '/tmp/w31-compose[dev]'
cd /tmp/w31-compose && make ruff PY=/tmp/w31-venv-compose/bin/python
cd /tmp/w31-compose && /tmp/w31-venv-compose/bin/python -m ruff check . --output-format json
```

Mypy followed `briefs/w14b.md` steps 1–4 with the existing setup-created Runtime directories, and ran sequentially with Python 3.11. The supplied normalized findings were reused for the per-file/code diff.

```sh
uv venv -q --seed --python 3.11 /tmp/w31-mypy-r12
uv pip install -q --python /tmp/w31-mypy-r12/bin/python -e '/home/user/wt/agent-r12[dev]'
uv pip install -q --python /tmp/w31-mypy-r12/bin/python --no-deps /home/user/wt/agent-r12.env/runtime /home/user/wt/agent-r12.env/runtime/packages/python
cd /home/user/wt/agent-r12 && make mypy PY=/tmp/w31-mypy-r12/bin/python
uv venv -q --seed --python 3.11 /tmp/w31-mypy-compose
uv pip install -q --python /tmp/w31-mypy-compose/bin/python -e '/home/user/wt/agent-compose[dev]'
uv pip install -q --python /tmp/w31-mypy-compose/bin/python --no-deps /home/user/wt/agent-compose.env/runtime /home/user/wt/agent-compose.env/runtime/packages/python
cd /home/user/wt/agent-compose && make mypy PY=/tmp/w31-mypy-compose/bin/python
/tmp/w31-mypy-compose/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
```

Ruff gate outputs are `ruff-r12-gate.txt` and `ruff-candidate-gate.txt`; JSON diagnostics are `ruff-r12.json` and `ruff-candidate.json`. Mypy gate outputs are `mypy-r12-gate.txt` and `mypy-913c6b8f-gate.txt`; the reusable finding lists are `../w14/mypy-r12.txt` and `../w14/mypy-913c6b8f.txt`. The temporary Ruff and mypy virtual environments were deleted after their runs.
