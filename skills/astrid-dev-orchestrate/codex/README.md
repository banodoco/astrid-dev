# Run Codex from a Claude Code cloud session

Use this when the orchestrator should hand a long, self-directed task to Codex, such as a GPU validation run, and keep overseeing it from its own session. Codex runs in the background inside the orchestrator's container. It keeps running while the orchestrator is idle, is resumed if it stops early, and talks to the orchestrator through two files.

Codex routes use the run contract's [Codex column](../../astrid-dev-shared/run-contract.md#routing-and-bindings):

| Route | Model |
| --- | --- |
| N | Luna |
| X | Terra |
| S | Sol |
| T and judgment | Astra |

Put exact model IDs in the run's `run.yaml`, never in this repository.

## One-time setup in the session

1. **Install:** `npm i -g @openai/codex` if `codex` is missing.
2. **Sign in with the owner's ChatGPT account:** run `codex login --device-auth` and give the owner the link and code it prints. Don't ask for an OpenAI API key.
3. **Check which model IDs this sign-in accepts:** run `codex exec -m <id> -s read-only --skip-git-repo-check 'Reply ok.'`. A ChatGPT sign-in refuses some IDs that exist elsewhere.
4. **Check which IDs subagents accept:** these can differ from the main model's list. Ask Codex to spawn a subagent with an unknown ID; the error lists the IDs it accepts.

## Start a run

```bash
setsid nohup skills/astrid-dev-orchestrate/codex/codex-runner.sh <workdir> <prompt.md> <run-dir> 6 <model-id> >/dev/null 2>&1 </dev/null &
```

- **`<workdir>`** is a git worktree for the task. Codex can write only there and in `/tmp`.
- **Keys:** Codex sees only PATH, HOME and the proxy and certificate variables. Add a key it needs by name, for example `CODEX_PASS_ENV=RUNPOD_API_KEY`. With that key passed, the runner also logs the RunPod balance and pod list to `money.log` every 5 minutes, and never logs the key.
- **Resumes:** `6` is the maximum number of times it resumes a Codex session that stopped before finishing.
- **Finish line:** the prompt must tell Codex to end with `RUN-STATUS: DONE`, `RUN-STATUS: BLOCKED: <reason>`, or `RUN-STATUS: WAITING` (see the mailbox below).

Then arm the watcher with the Bash tool's `run_in_background` (timeout 7200000), and re-arm it at every check-in:

```bash
skills/astrid-dev-orchestrate/codex/codex-watch.sh <run-dir>
```

The watcher exits, which wakes the orchestrator, when one of these happens:
- the run finishes, blocks or waits;
- Codex writes to the mailbox;
- the heartbeat goes stale for 5 minutes;
- about 110 minutes pass.

## Mailbox

| File | Who writes | Use |
| --- | --- | --- |
| `<run-dir>/to-orchestrator.md` | Codex | Notes and questions. The watcher wakes the orchestrator. |
| `<run-dir>/to-codex.md` | Orchestrator | Steering and answers. Codex reads it after each major step and before any costly action. |

If Codex can't continue without an answer, it writes its question and ends with `RUN-STATUS: WAITING`. The runner then holds until `to-codex.md` grows, and resumes Codex with the reply. That doesn't count against the resume limit. Answer quickly if paid resources may still be running.

## Run directory

- `status`: one of `running`, `waiting`, `done`, `blocked` or `gave-up`.
- `heartbeat`, `codex.log` and `result.md` (Codex's last message).
- `money.log` and the mailbox files.

## Oversight

The orchestrator still owns the judgment. At each check-in:
- read `codex.log`, the fixes Codex made and its notes;
- check that it's heading the right way;
- look for a shared, structural cause behind the separate failures it reports.

Steer through `to-codex.md`, and route structural fixes through the project's manager.

## Known limits

- **Sandbox:** use `-s workspace-write` with network on, which the runner sets. Auto mode refuses `danger-full-access` with approvals off.
- **Caches:** `~/.cache` is read-only inside the sandbox, so the runner points pip and XDG caches at `/tmp`.
- **Resume flags:** `codex exec resume` takes no `-C` or `-s`. The runner passes the sandbox through `-c sandbox_mode=...` and runs from the workdir.
- **The run lives in this container,** including the Codex sign-in. Scheduled check-ins keep the container busy; if it is reclaimed, sign in again and restart from the last `result.md`.
