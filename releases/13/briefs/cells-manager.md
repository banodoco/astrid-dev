# Cells manager — brief (Release 13)

**You:** the Release 13 cells manager, a fork of the Release 13 manager. You manage: you dispatch Codex workers (full access, `-c model_reasoning_effort=…` on every launch: high for Sol and Astra, medium for Terra, low for Luna; check the log header), judge their results, commit, and hand branches to the Release 13 manager. You do little hands-on work yourself.
**Report to:** the Release 13 manager (main), with short messages: when a branch is ready, when blocked, and at each merge.
**Goal:** every one of the five live cells (TTS, SFX, t2i, edit, music) passes on the next composed candidate, with each fix structural, plus the small log fixes below. Fast, but no patches: the owner's rules apply (structure over patches, declare once, one path, no shims, every failure is a symptom).

## You own
1. **SFX: the enum type and offline schema identity.** Sol pass 2 is running in `/home/user/wt/c-sfxfix` (VibeComfy, `r13/sfxfix` at `a8a7be7c`). Brief: `live-s1-sfx-2.md`; log `live-s1-sfx-2.log`; pass 1 diff `live-s1-sfx-v1.patch`. Judge it against that brief: one owner of the type vocabulary, one field for the commit, offline resolution for every pack, and a CPU check over every ready template.
2. **TTS: transformers 5 drops the `pad_token_id` the node's config needs.** Sol is running in `/home/user/wt/c-ttsfix-ag` (Astrid at `f9214240`) and `c-ttsfix-vc` (VibeComfy at `a8a7be7c`). Brief: `live-s1-tts.md`; log `live-s1-tts.log`. On its report, check:
   - did it look for an upstream node fix before extending the declared patch?
   - did it list every other config attribute transformers 5 dropped that the node reads?
   - is its CPU proof real, with no weights?

   If the Astrid part touches files a lane owns, tell main.
3. **Music: stale admitted first-build digest.** Sol is running in `/home/user/wt/c-musicfix` (VibeComfy, `r13/musicfix` at `a8a7be7c`). Brief: `live-s1-music.md`; log `live-s1-music.log`. It includes a CPU check over every ready template.
4. **One VibeComfy branch for the candidate.** Combine the SFX and music fixes, plus TTS's VibeComfy part if there is one, on `a8a7be7c` as `r13/cells-vc`. Run the union of their focused proofs. Push it (worker clones have push disabled; push by URL to `https://github.com/banodoco/VibeComfy`), then hand main the SHA for the Astrid pin. The pin changes `astrid/packs/runpod/pins.json`, the recipes, the engine yaml and the Windows environment, as in `b306b2be`. Have a Terra worker do the pin on a branch cut from `r13/compose` (`origin/r13/compose` on astrid-agent), including any digest or tool-catalog regeneration the pin needs. Check `test_no_other_tracked_file_copies_the_pin` and the pins tests.
5. **Two log gaps (T tasks, small):**
   - `astrid tasks logs` requires `--project`. It should default to the selected project, like other commands. Find how other task commands default and follow that.
   - No skill tells an agent how to get a run's logs. Add `astrid tasks logs <task> [--name …]` and `astrid generate failure` to the right Astrid skill (`astrid/core/resources/skills/…`), in two or three plain lines.

   One Terra card on a branch from `r13/compose`; then an Opus check of the wording (a fresh Opus sub-agent can review text; it launches nothing).
6. **Stage 2 preparation, not the paid run.** When main says the candidate is composed, prepare the install and script for the five cells: the same shape as `/home/user/wt/install-r13b/runs/stage1.sh`, a new root `root-s2`, data `data-s2`, home `home-s2`, the same `UV_CACHE_DIR`. Use `/home/user/wt/install-r13b/install-r13b.md`-style steps and the scratchpad installer `sh <scratchpad>/r12-installer/install …`. The paid run itself stays with main.

## Not yours
- **The edit failure:** the keep-warm checkpoint (machines lane, card K1).
- **The machines and engine lanes' files:** `astrid/packs/runpod/`, `astrid/core/machines_cli.py`, `astrid/installer/`, `astrid/core/execution/`, `astrid/core/generation/`, `astrid/packs/vibecomfy/`. If a fix needs them, tell main.
- **Full-suite comparison:** the test lane on hosted CI. You run focused proofs only.

## Rules
- **No RunPod or paid calls of any kind,** and none from your workers: put this in every brief. No `astrid generate`, no `astrid machines`, no api.runpod.io or rest.runpod.io. The proxy injects a real key.
- No pushes to `main`, `cand/*` or Release 12 branches. No force-push, no rebase. Never read `.env`, credential files or `~/.codex`. No AI model names in commits or PRs.
- **Commit trailer:**
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_011EzfW2L4ou5fDudzKLrc9d
  ```
- **The machine:** 4 CPUs shared by about eight workers, about 3 GB of disk.
  - Delete your workers' temp folders when they finish.
  - **Before deleting any clone, run `git worktree list` from it.** Deleting `c-vc-patch` today broke three worktrees.
  - `/home/user/wt/vc.git` is a bare VibeComfy mirror to clone from.
- Python: `/home/user/astrid-agent.env/venv/bin/python`. Ruff baseline 2117 (`python -m scripts.reshape.compare_ruff_baseline`).
- **If the owner's rules and speed conflict, take the structural fix and tell main** what it costs.
