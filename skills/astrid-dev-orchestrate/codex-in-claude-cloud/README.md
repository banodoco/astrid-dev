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
3. **Check which model IDs this sign-in accepts:** run `codex exec -m <id> -s read-only --skip-git-repo-check 'Reply ok.'`. A ChatGPT sign-in refuses some IDs that exist elsewhere. IDs can carry a minor version, such as `<family>-6.1-<tier>`, so check OpenAI's current Codex model list before you conclude a tier is unavailable.
4. **Check which IDs subagents accept:** these can differ from the main model's list. Ask Codex to spawn a subagent with an unknown ID; the error lists the IDs it accepts.
5. **Install the astrid-dev skills for Codex:** `mkdir -p ~/.agents && rm -rf ~/.agents/skills && cp -r <astrid-dev>/skills ~/.agents/skills`. Codex finds skills in `~/.agents/skills/` and in `.agents/skills/` under the directory it starts in. Re-copy them after astrid-dev's skills change. Leave `~/.codex` alone: it holds the sign-in.

## Use Codex for the workers under a Claude manager

Use this when a Claude manager session keeps managing (briefing, checking diffs, ruling, integrating) and its workers run on Codex. It needs no runner, keep-alive or mailbox: each task is one `codex exec` call that returns when the task is done.

- **Routes.** `N` tasks go to Luna, `X` to Terra, `S` to Sol. Reviews go to Astra, run read-only (`-s read-only`) on the exact commit range and given the previous round's report. `T` (taste) tasks stay on Claude sub-agents at the high-judgment tier. The manager judges the difficulty first, as the [run contract](../../astrid-dev-shared/run-contract.md#cheapest-model-first) says, and escalates one step only on evidence.
- **Sign-in first, once per session.** Do the [one-time setup](#one-time-setup-in-the-session): install, then `codex login --device-auth`. Post the link and the code it prints in your own reply, where the owner can see them, and tell the orchestrator they are waiting. The code expires in minutes, so ask for it when the owner is present, and ask again if it lapses. Each manager session is its own container and needs its own sign-in. Never read or copy `~/.codex`.
- **One task, one call, one worktree.** From a Claude sub-agent, so the output stays out of the manager's context:

  ```bash
  codex exec -m <model-id> -s workspace-write -c sandbox_workspace_write.network_access=true \
    --skip-git-repo-check -C <worktree> "$(cat <brief.md>)" </dev/null
  ```

  The wrapping sub-agent writes the brief to a file, runs the call, and returns Codex's last message plus the commit SHA and the test tail. It does not do the task itself. Give every task its own `git worktree add` path; Codex can write only there and in `/tmp`.
- **The brief is the same four things** as for any worker: one outcome, the exact repository, branch and files or selectors, what done looks like, and what to return. Add the run's rules that Codex cannot infer: commits are added and never rewritten, no model names in commit messages, never weaken a check, and stop after three attempts.
- **What stays with the manager.** Pushing to candidate branches, dispatching CI, messages to the orchestrator, anything paid, and anything that needs a credential. A Codex worker inherits the session's network, so a credential the proxy injects reaches it too: do not give Codex workers tasks that call a paid provider.
- **Switch at a task boundary.** Let running Claude workers finish; start new tasks on Codex. If a model ID is refused or the sign-in is lost, fall back to the Claude route for that task and say so; do not wait.
- **A review is independent of the work it reviews.** The reviewer is never the worker that wrote the change and is not briefed with the author's conclusions, only the commit range, the rules that apply and the questions to press on. Whoever owns the gate (the orchestrator, where the release brief says so) commissions the review and rules on its findings.

## Brief a manager

To hand a whole project to a Codex manager, start from [`manager-brief.md`](manager-brief.md). It is the Plan 38 brief, with the project-specific parts as placeholders. It covers:
- the workspace layout;
- the route-to-model table;
- timing and branches;
- the rules that differ under Codex;
- what to report.

## Start a run

```bash
CODEX_EFFORT=medium CODEX_MAX_THREADS=12 setsid nohup skills/astrid-dev-orchestrate/codex-in-claude-cloud/codex-runner.sh <workdir> <prompt.md> <run-dir> 6 <model-id> >/dev/null 2>&1 </dev/null &
```

- **`<workdir>`** is where Codex works. For a manager, make it a folder of partial clones (`git clone --filter=blob:none`) of the repositories the plan touches, plus `run/`. Codex can write only there and in `/tmp`. The runner passes `--skip-git-repo-check`, because that folder isn't itself a repository.
- **`CODEX_EFFORT`** sets the reasoning effort (`low`, `medium` or `high`). **`CODEX_MAX_THREADS`** raises the cap on open sub-agent threads, which defaults to 6. A finished sub-agent can keep its slot, and Codex may give the manager no tool to close it, so set the cap above the number of sub-agents you expect at once (12 works). Tell the manager to keep a slot free for its reviewer.
- **Keys:** Codex sees only PATH, HOME and the proxy and certificate variables. Add a key it needs by name, for example `CODEX_PASS_ENV=RUNPOD_API_KEY`. With that key passed, the runner also logs the RunPod balance and pod list to `money.log` every 5 minutes, and never logs the key.
- **Resumes:** `6` is the maximum number of times it resumes a Codex session that stopped before finishing.
- **Finish line:** the prompt must tell Codex to end with `RUN-STATUS: DONE`, `RUN-STATUS: BLOCKED: <reason>`, or `RUN-STATUS: WAITING` (see the mailbox below).

Then arm the keep-alive with the Bash tool's `run_in_background` (timeout 7200000). Re-arm it at every check-in, with all live runs:

```bash
skills/astrid-dev-orchestrate/codex-in-claude-cloud/codex-hold.sh <run-dir> [<run-dir> ...]
```

It keeps the session busy for about 55 minutes, then exits so the next check-in re-arms it. Every 30 seconds it checks each run:
- **Runner gone:** if the runner process has disappeared while the run is unfinished, it restarts it. The runner saved its arguments in `runner.args` and `runner.env`, and resumes the same Codex session. After three failed restarts, it exits with `RESTART FAILED`.
- **Wake the orchestrator:** it exits when Codex writes to the mailbox, or when a run reaches `done`, `blocked`, `gave-up` or `waiting`.

`codex-watch.sh` still works as a watch-only version, and also reports a dead runner.

**Restarts kill everything.** A restart of the Claude session's worker kills every process in the container: the runner, Codex and the keep-alive. Restarting is safe: Codex rebuilds its state from the mailbox, `run.yaml`, `tasks.md`, and its branches and worktrees. Three layers bring a run back, from fastest to most durable:

| Layer | Survives a restart | What it does |
| --- | --- | --- |
| `codex-hold.sh` (background task) | No | Restarts a dead runner and wakes you on mailbox text or a finished run. Re-arm it at every check-in. |
| `codex-hold-daemon.sh` (SessionStart hook) | Yes, when the session resumes | Restarts a dead runner within 30 seconds of the session starting again, without waiting for you. Wakes nobody. |
| Scheduled check-in (`send_later` or a scheduled task) | Yes, server-side | The only thing that wakes you after a restart. Keep one at most 20 minutes away while a run is live. |

**Set up the daemon once per container:**
1. List each live run folder, one per line, in `~/codex/runs.txt`, or point `CODEX_RUNS` at another file. Remove a run's line when it finishes.
2. Add this SessionStart hook to the user settings (`~/.claude/settings.json`). It starts the daemon detached, so session start isn't held up. A lock keeps a second copy from running:

```json
{"hooks": {"SessionStart": [{"hooks": [{"type": "command", "timeout": 10,
  "command": "setsid nohup <workdir-parent>/bin/codex-hold-daemon.sh >/dev/null 2>&1 </dev/null & exit 0"}]}]}}
```

3. Start it once by hand with the same command; the hook covers later starts.

Auto mode refuses Claude's own edits to its settings file ("Self-Modification"), so the owner adds the hook, or approves the edit. Until it's added, the scheduled check-in is what restarts the run, through `codex-hold.sh`.

## Mailbox

| File | Who writes | Use |
| --- | --- | --- |
| `<run-dir>/to-orchestrator.md` | Codex | Notes and questions. The watcher wakes the orchestrator. |
| `<run-dir>/to-codex.md` | Orchestrator | Steering and answers. Codex reads it after each major step and before any costly action. |

If Codex can't continue without an answer, it writes its question and ends with `RUN-STATUS: WAITING`. The runner then holds until `to-codex.md` grows, and resumes Codex with the reply. That doesn't count against the resume limit. Answer quickly if paid resources may still be running.

## Run directory

- `status`: one of `running`, `waiting`, `done`, `blocked` or `gave-up`.
- `heartbeat`, `codex.log` and `result.md` (Codex's last message).
- `runner.pid`, `runner.args` and `runner.env`, which the keep-alive and the daemon use to restart the runner, and `hold.log`, the restarts both have made.
- `money.log` and the mailbox files.

## Oversight

The hosting session answers for the run ([who answers for a run](../../astrid-dev-shared/run-contract.md#who-answers-for-a-run)). Codex manages the tasks; the host does everything Codex can't. At each check-in it reads the mailbox, `tasks.md` and the integration branch, and ([orchestrate skill](../SKILL.md#hand-a-long-task-to-codex-from-claude-cloud)):
- sends one next action through `to-codex.md` if nothing has moved since the last check-in;
- starts any task Codex can't run, once Codex has written `READY` for it or its inputs have landed;
- clears what is stuck on its own side, such as a progress PR that can't merge or a dead runner;
- brings the owner a decision when one is theirs.

It doesn't review Codex's fixes or relay its branches. Codex's own reviewer sub-agent reviews, and a Codex manager integrates its own work. That needs the authority in its starting brief ([`manager-brief.md`](manager-brief.md)); a mailbox note can't grant it.

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
- **bubblewrap:** Codex warns that `bubblewrap` isn't on PATH and uses its bundled copy. That works.
- **On a local machine,** run Codex in a terminal instead. This runner and keep-alive exist for cloud sessions.
