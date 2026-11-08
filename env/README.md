# Shared worker environment

Setup and test scripts that any Astrid project's worker can run in a **single-repository cloud session**. Plans reference these scripts instead of keeping their own copies.

## Rules every script here follows

- **Run from the product checkout root.** The script builds `<checkout>.env/` next to the checkout, never inside it.
- **Other repositories come only from git,** at the commit the product checkout pins (for example `runtime.lock.json` or `VIBECOMFY_ENGINE_REVISION`), and each fetch checks the SHA. Nothing downloads a GitHub archive: a cloud session's GitHub proxy only serves archives for its attached repository.
- **Public repositories and PyPI only.** Nothing private, no credentials, no cloud resources.
- **Exit 3 means an environment problem,** never a test result.

## Copy them into the product repository

A single-repo cloud worker in auto mode refuses scripts cloned from another repository, even with an allow rule. Each product repository therefore carries its own copy under `scripts/worker-env/` (astrid-agent first, on Plan 33's integration branch), and workers call those copies. This folder is the canonical source; keep the copies in step.

## How a worker calls them

Clone astrid-dev read-only to the fixed path `/home/user/astrid-dev`, then call each script by its **literal** path from the product checkout root. Each product repository's committed `.claude/settings.json` allows exactly these paths. A path built from a variable doesn't match an allow rule, so it is refused.

```text
git clone -q --depth 1 https://github.com/banodoco/astrid-dev /home/user/astrid-dev
bash /home/user/astrid-dev/env/agent-setup.sh                  # astrid-agent checkout
bash /home/user/astrid-dev/env/agent-pytest.sh -q <selectors>
bash /home/user/astrid-dev/env/vc-setup.sh                     # VibeComfy checkout
bash /home/user/astrid-dev/env/vc-pytest.sh -q <selectors>
bash /home/user/astrid-dev/env/smoke.sh agent|vc <one selector>
```

| File | What it does |
|---|---|
| `agent-setup.sh` | Builds a Python 3.13 venv with `-e .[dev]`, then git-fetches the Runtime (installed `--no-deps`, with its Python client) and VibeComfy at the checkout's pins. Needs `uv`, `git` and `ffmpeg`. |
| `agent-pytest.sh` | Runs `pytest` in that environment with a wiped caller environment. Its arguments go to `pytest` verbatim. |
| `vc-setup.sh`, `vc-pytest.sh` | The same pair for a VibeComfy checkout. |
| `smoke.sh` | Setup plus one named test. A manager runs it in one throwaway worker per repository before a run's first task, so environment problems surface once, in minutes. |

Plan 02's original copies stay frozen in `plans/02-consistent-generation/env/` for its recorded proof. Use the copies here for new work.
