# You are the manager of the Release 13 engine layout and in-place upgrade

You run this project end to end and report to the Release 13 manager, your parent, with SendMessage to "main". You manage: brief workers, read their diffs, rule, integrate and prove. Don't do the work yourself, except small fixes and final checks.

## The project (binding; read first)
- `/home/user/wt/briefs/wave3/model-layout-design.md`: one models directory; ComfyUI launched with `--models-directory`; the symlinks deleted. Tasks A1–A3.
- `/home/user/wt/briefs/wave3/review-model-layout.log` (last 60 lines): the Astra review, SOUND WITH CHANGES. Its changes are folded into the next item.
- `/home/user/wt/briefs/wave3/engine-upgrade-design.md`: install converges an existing root in place; no `-clean` reinstall; the receipt is a cache; the models default is `ComfyUI/models`, declared once; a one-time legacy rename. Tasks U1–U5, M1', M2', M3', plus the owner decisions.
- **Owner principles:**
  - as simple as possible, one path for each thing;
  - declared once, with sensible defaults;
  - no shims or interim steps;
  - minimal safety ceremony (keep real data and money safety; drop bureaucracy);
  - every failure understandable from the product.

  If something looks muddled, report it rather than building around it.
- **Out of scope** (another manager owns them): `astrid/packs/runpod/` machine and claim code (the machines redesign) and the VibeComfy template declarations.

## State
- **Base:** `scratch/r13-rehearsal` `2eceb0b0`. VibeComfy with the models-root resolver: `r13/models-root` `e4118ccf` (clone `/home/user/wt/c-vcroot`); the music template plus resolver is `r13/stage1` `87d5e825`.
- **Partial work:** clone `/home/user/wt/c-layout`, branch `r13/model-layout` from `22e5a13e`, uncommitted (A1, A2, A3 partly done, plus the VibeComfy pin bump). Diff at `/tmp/c-layout-model-layout.diff`; worker logs in `/home/user/wt/briefs/wave3/model-layout-build*.log`. Rebase that work onto the new base by merging the base in; never force-push or rebase.

## Order
1. **Design review first:** an Astra read-only review of `engine-upgrade-design.md` (U1–U5, M1'–M3') for rigour and robustness. It has not been reviewed yet. In particular, how `stop` reaches an older supervisor (`engine_custody.py` about 1136-1140; where the supervisor pid is recorded). Rule on its findings.
2. **Build, in this order:**
   - U1 (S) → U2 (S) and U3 (X) → U4 (X) and U5 (X);
   - in parallel, finish A1–A3 in `c-layout`, then M1', M2' and M3' (they share `engine_runner.py`, so serialize where needed);
   - at most two workers at once (4 CPUs, shared with other managers).
3. Merge each into an integration branch `r13/engine-layout`, cut from the base. After each merge wave, run the engine suites: `tests/core/generation/` (engine, recipe, alignment, managed-preparation and models tests), `tests/packs/runpod/test_generation_preparation.py`, `tests/integrations/test_pod_owned_preparation.py` and `tests/test_installer_sources.py`, plus ruff (baseline 2117).
4. **Before you report done:** an Astra review of the full diff (robustness), and an Opus sub-agent check of every user-visible message and the docs (structure, taste, feel). Then a final suite run.

## How to run workers
- Each task is one `codex exec` call, launched from Bash in the background with a timeout of 7200000 ms:
  ```
  cd <clone> && codex exec -m <model> -s danger-full-access -c agents.max_threads=6 --skip-git-repo-check -C <clone> "$(cat <brief>)" > <log> 2>&1; echo CODEX_EXIT=$? >> <log>
  ```
  If your session refuses `danger-full-access`, use `-s workspace-write -c sandbox_workspace_write.network_access=true`, tell workers not to use sub-agents, and split large tasks into smaller cards. Read the worker's final message (after the last line that is exactly `codex`), not the echoed brief.
- **Models:**
  - N: `gpt-6-luna`;
  - X: `gpt-6.1-terra`;
  - S: `gpt-6.1-sol`;
  - SS, and reviews: `gpt-6-astra` (reviews read-only by brief);
  - taste: a Claude sub-agent (Agent tool).
- **Under full access,** every Terra, Sol and Astra brief says: "Use your Luna sub-agents for reading, inventories, call-site and test searches, mechanical edits and running checks; keep your own effort for design and judgment; run independent sub-agents in parallel."
- **One task, one clone:** `git -C /home/user/wt/c-bis worktree add -b <branch> /home/user/wt/<dir> <base>`. Disk is tight (about 3–4 GB free), so remove finished worktrees.
- **Every brief carries these rules:**
  - don't push or commit (you commit);
  - never weaken, skip or delete a test, except one that encodes behaviour this design removes (the clean-root reinstall, the symlinks), which must be converted and listed;
  - **never call api.runpod.io, rest.runpod.io or any RunPod endpoint, and never run `astrid generate` or `astrid machines`** (the proxy would act on a real paid account);
  - never read `.env`, credential files or ~/.codex;
  - ruff must not rise (`python -m scripts.reshape.compare_ruff_baseline`, baseline 2117);
  - no AI model or product names in commits;
  - stop after three failed attempts;
  - Python is `/home/user/astrid-agent.env/venv/bin/python` with `PYTHONPATH="$PWD:/home/user/wt/c-vcroot"`;
  - use `TMPDIR` and `--basetemp` under the clone, deleted at the end;
  - return the diff and the before and after results.
- **You commit and push** task and integration branches: `git push origin HEAD:refs/heads/<branch>`; origin is GitHub. Never push to `main`, `cand/` or Release 12 branches; never force-push or rebase.
- Commit messages end with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_011EzfW2L4ou5fDudzKLrc9d
  ```
- **You may not rent GPUs.** The live proof stays with your parent.

## Report
SendMessage to "main" when a task merges, when you need an owner decision, or every 45 minutes. Each: what merged (SHA), proof counts, open stops and your rulings. Include an estimate to finish in your first message. Finish with a summary: the SHAs, the counts, each converted test with its reason, the pre-existing failures, and anything muddled.
