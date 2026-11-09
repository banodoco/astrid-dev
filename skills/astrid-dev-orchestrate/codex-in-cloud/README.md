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
5. **Install the astrid-dev skills for Codex:** `mkdir -p ~/.agents && rm -rf ~/.agents/skills && cp -r <astrid-dev>/skills ~/.agents/skills`. Codex finds skills in `~/.agents/skills/` and in `.agents/skills/` under the directory it starts in. Re-copy them after astrid-dev's skills change. Leave `~/.codex` alone: it holds the sign-in.

## Start a run

```bash
CODEX_EFFORT=medium CODEX_MAX_THREADS=12 setsid nohup skills/astrid-dev-orchestrate/codex-in-cloud/codex-runner.sh <workdir> <prompt.md> <run-dir> 6 <model-id> >/dev/null 2>&1 </dev/null &
```

- **`<workdir>`** is where Codex works. For a manager, make it a folder of partial clones (`git clone --filter=blob:none`) of the repositories the plan touches, plus `run/`. Codex can write only there and in `/tmp`. The runner passes `--skip-git-repo-check`, because that folder isn't itself a repository.
- **`CODEX_EFFORT`** sets the reasoning effort (`low`, `medium` or `high`). **`CODEX_MAX_THREADS`** raises the cap on open sub-agent threads, which defaults to 6. A finished sub-agent keeps its slot until it's closed, so tell the manager to close each one when its result is in.
- **Keys:** Codex sees only PATH, HOME and the proxy and certificate variables. Add a key it needs by name, for example `CODEX_PASS_ENV=RUNPOD_API_KEY`. With that key passed, the runner also logs the RunPod balance and pod list to `money.log` every 5 minutes, and never logs the key.
- **Resumes:** `6` is the maximum number of times it resumes a Codex session that stopped before finishing.
- **Finish line:** the prompt must tell Codex to end with `RUN-STATUS: DONE`, `RUN-STATUS: BLOCKED: <reason>`, or `RUN-STATUS: WAITING` (see the mailbox below).

Then arm the keep-alive with the Bash tool's `run_in_background` (timeout 7200000). Re-arm it at every check-in, with all live runs:

```bash
skills/astrid-dev-orchestrate/codex-in-cloud/codex-hold.sh <run-dir> [<run-dir> ...]
```

It keeps the session busy for about 55 minutes, then exits so the next check-in re-arms it. Every 30 seconds it checks each run:
- **Runner gone:** if the runner process has disappeared while the run is unfinished, it restarts it. The runner saved its arguments in `runner.args` and `runner.env`, and resumes the same Codex session. After three failed restarts, it exits with `RESTART FAILED`.
- **Wake the orchestrator:** it exits when Codex writes to the mailbox, or when a run reaches `done`, `blocked`, `gave-up` or `waiting`.

`codex-watch.sh` still works as a watch-only version, and also reports a dead runner.

**Restarts kill everything.** A restart of the Claude session's worker kills every process in the container: the runner, Codex and the keep-alive. Only a server-side scheduled check-in (`send_later` or a scheduled task) survives a restart. So while a run is live, keep a check-in at most 20 minutes away, and make each check-in start `codex-hold.sh` again. Restarting is safe: Codex rebuilds its state from the mailbox, `run.yaml`, `tasks.md`, and its branches and worktrees.

## Mailbox

| File | Who writes | Use |
| --- | --- | --- |
| `<run-dir>/to-orchestrator.md` | Codex | Notes and questions. The watcher wakes the orchestrator. |
| `<run-dir>/to-codex.md` | Orchestrator | Steering and answers. Codex reads it after each major step and before any costly action. |

If Codex can't continue without an answer, it writes its question and ends with `RUN-STATUS: WAITING`. The runner then holds until `to-codex.md` grows, and resumes Codex with the reply. That doesn't count against the resume limit. Answer quickly if paid resources may still be running.

## Run directory

- `status`: one of `running`, `waiting`, `done`, `blocked` or `gave-up`.
- `heartbeat`, `codex.log` and `result.md` (Codex's last message).
- `runner.pid`, `runner.args` and `runner.env`, which the keep-alive uses to restart the runner, and `hold.log`, the keep-alive's restarts.
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
- **The run lives in this container,** including the Codex sign-in. If the container is reclaimed, sign in again and start the run again. The runner resumes from `codex.log`'s session id when that file survives.
- **No nested Codex:** a Codex process inside the sandbox can't start another (`~/.codex` is read-only there). Get parallel work from sub-agents, not from child `codex exec` processes.
- **Shared filesystem:** sub-agents share one filesystem. Every worker brief must name its own `git worktree add` path and its `<worktree>.env`, and only the manager touches the base clones. Two workers in one checkout will collide on git locks.
- **GitHub through the proxy:** `git push`, the REST API (`POST /pulls`, workflow dispatch) and artifact downloads work with no token. The proxy appends a Claude Code attribution to PR bodies Codex creates, so mention in the PR body that Codex wrote it.
- **One branch per PR:** never push to a branch whose PR is already merged. Open a fresh branch for each PR.
- **Manage skill under Codex:** the cloud-session rules in the manage skill (one-repo sessions, allow lists, `list_sessions`, `send_message`) don't apply. Keep their intent: one repository's scope per brief, one worktree per task, commits added and never rewritten, and evidence for every claim. The mailbox stands in for `send_message`.
- **On a local machine,** run Codex in a terminal instead. This runner and keep-alive exist for cloud sessions.
