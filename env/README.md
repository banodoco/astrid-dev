# Shared worker environment

Setup and test scripts that any Astrid project's worker can run in a **single-repository cloud session**. Plans reference these scripts instead of keeping their own copies.

## Rules every script here follows

- **Run from the product checkout root.** The script builds `<checkout>.env/` next to the checkout, never inside it.
- **Other repositories come only from git,** at the commit the product checkout pins (for example `runtime.lock.json` or `VIBECOMFY_ENGINE_REVISION`), and each fetch checks the SHA. Nothing downloads a GitHub archive: a cloud session's GitHub proxy only serves archives for its attached repository.
- **Public repositories and PyPI only.** Nothing private, no credentials, no cloud resources.
- **Exit 3 means an environment problem,** never a test result.

## Simplest: let the cloud environment run them

Give the cloud environment workers run in `cloud-setup.sh` as its setup script, once. It runs before Claude starts, so no permission check applies. For each Astrid checkout in the session it builds `<checkout>.env/` and puts the test commands on PATH:
- `astrid-agent-pytest` and `astrid-agent-pytest-pod`;
- `vibecomfy-pytest`.

A worker then runs no setup, and a repository needs no copy of these scripts. It needs only an allow rule for its test command, for example `Bash(astrid-agent-pytest:*)`. Its log is `/var/log/astrid-cloud-setup.log`.

## Copy them into the product repository (when the environment can't run them)

A single-repo cloud worker in auto mode refuses scripts cloned from another repository, even with an allow rule. Each product repository therefore carries its own copy under `scripts/worker-env/` (astrid-agent first, on Plan 33's integration branch), and workers call those copies. This folder is the canonical source; keep the copies in step.

## How a worker calls them

Create the worker session on the product repository's integration branch, in **auto** or **Accept edits** mode. Prefer auto: it doesn't stall on harmless unlisted commands. Call each in-repo copy by its **literal** path from the checkout root. The repository's committed `.claude/settings.json` allows exactly these commands, and a path built from a variable doesn't match an allow rule.

```text
bash scripts/worker-env/agent-setup.sh                  # astrid-agent checkout
bash scripts/worker-env/agent-pytest.sh -q <selectors>
bash scripts/worker-env/agent-pytest-pod.sh <selectors>
bash scripts/worker-env/smoke.sh agent <one selector>
```

What a permission stress test showed (three auto-mode workers, astrid-agent int/33 at 187d692, 8 Nov 2026):
- **Ran without a prompt:** the in-repo scripts, the allow-listed git commands, pipes, an env-var prefix, and harmless unlisted commands.
- **Denied by the deny list:** force-push.
- **Refused every time, despite the allow rule:** a script run from a `/home/user/astrid-dev` clone ("Code from External").
- **Never use `cd`:** a `cd` changes the working directory for every later command in the session, so later literal paths fail.

| File | What it does |
|---|---|
| `agent-setup.sh` | Builds a Python 3.13 venv with `-e .[dev]`, then git-fetches the Runtime (installed `--no-deps`, with its Python client) and VibeComfy at the checkout's pins. Needs `uv`, `git` and `ffmpeg`. |
| `agent-pytest.sh` | Runs `pytest` in that environment with a wiped caller environment. Its arguments go to `pytest` verbatim. |
| `vc-setup.sh`, `vc-pytest.sh` | The same pair for a VibeComfy checkout. |
| `smoke.sh` | Setup plus one named test. A manager runs it in one throwaway worker per repository before a run's first task, so environment problems surface once, in minutes. |

Plan 02's original copies stay frozen in `plans/02-consistent-generation/env/` for its recorded proof. Use the copies here for new work.
