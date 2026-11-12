# W14b — Python 3.11 mypy findings added over R12

## Gate result

| Run | Gate count | CI count | Reproduced |
|---|---:|---:|---|
| R12 `0e1543e0da2215db9cb3320cfd1083174c3c62a9` | 2,338 (baseline 2,192) | 2,338 | Yes |
| Candidate `913c6b8fff8c63aeb05cb1b5ae160463f6d5e641` | 2,420 (baseline 2,192) | 2,420 | Yes |

The line-number-free multiset diff is in `new-findings.tsv` and `removed-findings.tsv`. It has 192 added findings and 110 removed findings, for a net increase of 82. This matches the gate delta. Full mypy output is in `mypy-r12.txt` and `mypy-913c6b8f.txt`; gate outputs are in the corresponding `gate-*.txt` files.

## Added findings grouped by file

Introducing commits are `git blame` abbreviations for candidate flagged lines. A `^` prefix is retained when blame identifies an ancestor of the candidate's first-parent history; these findings may have surfaced due to surrounding changes rather than a change to that exact line. Top codes are the most frequent in each file, with counts where ties matter.

| File | New | Top error codes | Blamed introducing commits | Owner |
|---|---:|---|---|---|
| `astrid/packs/runpod/machine.py` | 28 | attr-defined 13, arg-type 6, operator 3 | `80bbf6904`, `9e7b2a481`, `d072cf5da`, `d27d79b88`, `c6c805cc3`, `65d766afb`, `3bcd524e3`, `14155ab34`, `b6c17c8fc`, `80a437c26` | Machines lane |
| `astrid/sdk/generation.py` | 20 | attr-defined 10, index 5, union-attr 2 | `73fb63c7c`, `cd27ed9d7`, `335643a8f`, `b9a611eaa`, `1ae020677`, `ee3015a5a`, `^b4e66cc3`, `974a50812`, `e4a0e8cc7`, `68b26db0a` | Test manager |
| `astrid/packs/runpod/remote_placement.py` | 18 | union-attr 8, operator 7, assignment 2 | `a72ad64f1`, `^b4e66cc3`, `80bbf6904`, `993fd926e`, `4a21520aa`, `15e212016`, `dd20b74b0` | Machines lane |
| `astrid/packs/runpod/target_selection.py` | 14 | arg-type 6, attr-defined 3, assignment 2 | `16ffaa601`, `2d905bd52`, `14155ab34`, `0a7de39c1` | Machines lane |
| `astrid/packs/vibecomfy/local_job.py` | 12 | index 5, arg-type 4, assignment 1 | `47e77a513`, `fe066bdc9`, `260ee2304` | Engine lane |
| `astrid/packs/runpod/worker_owner.py` | 11 | arg-type 2, attr-defined 2, index 2 | `80bbf6904`, `c0f505d4d`, `d3c440236`, `d1ed6a7d6` | Machines lane |
| `astrid/core/generation/job_inputs.py` | 7 | union-attr 4, dict-item 1, misc 1 | `fe411d26a`, `4286515d8` | Engine lane |
| `astrid/core/execution/generic_host.py` | 7 | union-attr 3, arg-type 1, attr-defined 1 | `^e862934c`, `c0f505d4d`, `744585fa6`, `f96644329`, `e75a5a8ee` | Machines lane |
| `astrid/sdk/invocation.py` | 5 | operator 2, arg-type 1, assignment 1 | `16ffaa601`, `05f10de9b` | Test manager |
| `astrid/packs/runpod/adapter.py` | 5 | operator 2, type-var 2, union-attr 1 | `d91818db1`, `16ffaa601` | Machines lane |
| `astrid/core/machines_cli.py` | 5 | arg-type 4, index 1 | `7d8239a64`, `748625413`, `0253d3b46`, `644f1a280` | Machines lane |
| `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py` | 4 | attr-defined 2, arg-type 1, import-untyped 1 | `100a239d6`, `4aae76278`, `75e553104` | Engine lane |
| `astrid/packs/runpod/generation.py` | 4 | union-attr 3, arg-type 1 | `b6c17c8fc`, `9e7b2a481` | Machines lane |
| `astrid/core/cli/domain_tasks.py` | 4 | union-attr 2, override 1, return-value 1 | `^9373955d`, `90551c4f9`, `cffffe056`, `90ae9c314` | Test manager |
| `astrid/packs/runpod/provider.py` | 3 | arg-type 3 | `ad7723a8f` | Machines lane |
| `astrid/packs/h3_av/shared/verify.py` | 3 | arg-type 2, assignment 1 | `^3e551fde` | Test manager |
| `astrid/installer/progress.py` | 3 | union-attr 3 | `f9d526f17` | Machines lane |
| `astrid/core/generation/managed_preparation.py` | 3 | assignment 1, index 1, return-value 1 | `2ac650593`, `d4da4927e` | Engine lane |
| `astrid/core/generation/cli.py` | 3 | arg-type 2, assignment 1 | `561d32a29`, `80bbf6904` | Engine lane |
| `astrid/core/_shared/run_logs.py` | 3 | operator 2, arg-type 1 | `15db432fa` | Test manager |
| `astrid/packs/vibecomfy/local_server_engine.py` | 2 | attr-defined 1, index 1 | `121a7af1a`, `878d13f46` | Engine lane |
| `astrid/packs/h3_av/shared/prepare.py` | 2 | operator 1, union-attr 1 | `^3e551fde` | Test manager |
| `astrid/packs/h3_av/shared/generation.py` | 2 | union-attr 2 | `75e553104` | Test manager |
| `astrid/core/pack/validate_first_party.py` | 2 | assignment 1, no-redef 1 | `^3e551fde` | Test manager |
| `astrid/core/generation/local_job.py` | 2 | arg-type 2 | `fe066bdc9`, `5f370640f` | Engine lane |
| `astrid/core/generation/backends/vibecomfy.py` | 2 | union-attr 2 | `7efe5bb65` | Engine lane |
| `astrid/core/engine_cli.py` | 2 | union-attr 2 | `72fbdf65c` | Test manager |
| `astrid/packs/h3_av/shared/request.py` | 1 | no-redef 1 | `^3e551fde` | Test manager |
| `astrid/packs/runpod/pod_fields.py` | 1 | arg-type 1 | `e6d857667` | Machines lane |
| `astrid/packs/runpod/failure_receipt.py` | 1 | arg-type 1 | `30795fec8` | Machines lane |
| `astrid/packs/h3_av/shared/planner.py` | 1 | no-redef 1 | `^3e551fde` | Test manager |
| `astrid/packs/h3_av/shared/compile.py` | 1 | arg-type 1 | `^e862934c` | Test manager |
| `astrid/packs/h3_av/cli.py` | 1 | arg-type 1 | `^3e551fde` | Test manager |
| `astrid/packs/generation/extensions/points/engine_protocol.py` | 1 | misc 1 | `66e47777e` | Test manager |
| `astrid/installer/backend.py` | 1 | arg-type 1 | `0f584c920` | Machines lane |
| `astrid/core/generation/target_inventory.py` | 1 | index 1 | `ac1e8ffd0` | Engine lane |
| `astrid/core/generation/entries.py` | 1 | assignment 1 | `98dccc3c4` | Engine lane |
| `astrid/core/generation/engine_recipe.py` | 1 | var-annotated 1 | `^3e551fde` | Engine lane |
| `astrid/core/generation/engine_custody.py` | 1 | has-type 1 | `2ac650593` | Engine lane |
| `astrid/core/generation/defaults.py` | 1 | arg-type 1 | `ee3015a5a` | Engine lane |
| `astrid/core/generation/backends/vibecomfy_local_server.py` | 1 | var-annotated 1 | `121a7af1a` | Engine lane |
| `astrid/core/execution/machine_run.py` | 1 | assignment 1 | `3bcd524e3` | Machines lane |
| `astrid/skills/__init__.py` | 1 | assignment 1 | `64b29bb7f` | Test manager |

## Totals by owner

| Owner | Added findings |
|---|---:|
| Machines lane | 102 |
| Engine lane | 41 |
| Test manager | 49 |
| **Total** | **192** |

## Commands run

From `/home/user/wt/agent-r12`:

```sh
uv venv -q --seed --python 3.11 /tmp/mypy311-r12
uv pip install -q --python /tmp/mypy311-r12/bin/python -e '/home/user/wt/agent-r12[dev]'
bash /home/user/astrid-dev/env/agent-setup.sh
uv pip install -q --python /tmp/mypy311-r12/bin/python --no-deps /home/user/wt/agent-r12.env/runtime /home/user/wt/agent-r12.env/runtime/packages/python
/tmp/mypy311-r12/bin/python -m scripts.reshape.compare_mypy_baseline
/tmp/mypy311-r12/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
```

From `/home/user/wt/agent-compose`:

```sh
uv venv -q --seed --python 3.11 /tmp/mypy311-913c6b8f
uv pip install -q --python /tmp/mypy311-913c6b8f/bin/python -e '/home/user/wt/agent-compose[dev]'
bash /home/user/astrid-dev/env/agent-setup.sh
uv pip install -q --python /tmp/mypy311-913c6b8f/bin/python --no-deps /home/user/wt/agent-compose.env/runtime /home/user/wt/agent-compose.env/runtime/packages/python
/tmp/mypy311-913c6b8f/bin/python -m scripts.reshape.compare_mypy_baseline
/tmp/mypy311-913c6b8f/bin/python -m mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes
```

The R12 setup initially exited while removing a nonempty Python 3.13 temporary test directory, so the setup command was retried successfully. The Runtime paths are the adjacent environment directories created by `agent-setup.sh` (`<checkout>.env/runtime`). Each gate and direct mypy invocation ran sequentially. Both temporary Python 3.11 environments were deleted after their side completed.
