# Check environment scripts

Small scripts from the earlier generation run, copied unchanged. They build a clean test environment next to a checkout and run `pytest` in it with a wiped environment. They are inputs to the checks in [tasks.md](../tasks.md); nothing here authorizes running them.

Call the scripts as `bash "$ENV/<script>"` with `ENV=<astrid-dev checkout>/strategy/projects/02-consistent-generation/env`, from the product checkout root; they are not inside the product checkouts.

| File | What it does |
|---|---|
| `agent-setup.sh` | Run from an Agent checkout root. Needs `uv`, `git`, `ffmpeg` and network reads to PyPI and GitHub. Builds `<checkout>.env/` (Python 3.13 venv with `-e .[dev]`, Runtime at the commit in `runtime.lock.json`, VibeComfy at the checkout's own pinned revision). Exit 3 means a missing tool or environment, not a test result. |
| `agent-pytest.sh` | Run from the same checkout after setup. Passes its arguments to `pytest`. Exit 3 means setup was not run. If `GEN_DESELECT_FILE` names a file of node ids, each is deselected. |
| `vc-setup.sh`, `vc-pytest.sh` | The same pair for a VibeComfy checkout (`uv sync --frozen`, then `pytest`). |
| `shared-failure-exceptions.txt` | The nine test nodes the owner approved as allowed to keep failing, because they fail on both the base and the candidate (owner answer A, 3 Nov 2026 17:40Z). Use it as `GEN_DESELECT_FILE`. Any other failure is not excepted. |

`VERIFY_SIDE` is only passed through to the test process (the earlier runner set it to `base` or `head`). It is not defined by this repository; ignore it.

Re-read each script against the candidate before relying on it: the setup script expects `scripts/ci_install_runtime.py` and `VIBECOMFY_ENGINE_REVISION` in Agent, which exist on Agent `pre-main` at the time of writing.
