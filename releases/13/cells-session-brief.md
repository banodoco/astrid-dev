# Release 13 cells manager (own session) — brief

**You:** the Release 13 cells manager, Opus, in your own session, so your workers get this session's CPUs. You **manage**: you dispatch Codex workers and sub-agents, judge their results, commit, and hand branches over. You do little hands-on work yourself.
**You report to:** the Release 13 manager (orchestrator), session `session_011EzfW2L4ou5fDudzKLrc9d`, by `send_message`. Release, scope and ownership questions go there. Hannah reaches you through the orchestrator, unless she writes in your session herself.
**Written:** 12 Nov 2026, about 16:50 UTC, at Hannah's request ("get everything moving as rapidly as possible").

## Your goal
Every one of the five live generation cells (TTS, SFX, t2i, edit, music) passes on the next composed candidate, and every fix is **structural**. The owner's rules:
- structure over patches;
- declare each fact once, with one owner;
- one path for each thing;
- no shims;
- every failure is a symptom of a deeper issue: find it.

Plus two small log fixes. Speed matters, but never at the cost of a patch: if they conflict, take the structural fix and tell the orchestrator what it costs.

## Read first
- The [run contract](../../skills/astrid-dev-shared/run-contract.md), [Iterate](../../skills/astrid-dev-iterate/SKILL.md) and [Manage](../../skills/astrid-dev-manage/SKILL.md) skills, and the [Codex in Claude Cloud](../../skills/astrid-dev-orchestrate/codex-in-claude-cloud/README.md) guide.
- `releases/13/decisions.md` on this branch, especially the NOW block and the entries from 15:56 UTC on: the live Stage 1 results and the four failures.
- `releases/13/test-manager-brief.md`, for how the hosted test lane works. It owns full-suite comparison; you run focused proofs only.

## State when you start
- **Live Stage 1** on candidate `f9214240`: t2i passed; four cells failed.
  - **TTS:** model load fails with `'Qwen3TTSTalkerConfig' object has no attribute 'pad_token_id'`. The engine locks `transformers==5.22.1`, and the `ComfyUI-QwenTTS` node needs a config attribute that version dropped.
  - **SFX:** `public_input_incompatible`, `CHOICE` against `COMBO`. Deeper causes:
    - the enum socket type is spelled three ways across about ten VibeComfy modules;
    - the offline object-info identity lookup fails for 48 of 49 cache files (they carry the commit only as `pack_version`), so the offline type checks almost never run.
  - **Music:** `canonical first-build semantic digest differs from admitted candidate` (`vibecomfy/workflow_bundle.py:1722`). The template's model declarations and its picker values drift through the canonicalizer's round trip.
  - **Edit:** not yours. It's the machines lane's keep-warm checkpoint fix (K1).
- **Three Sol workers are finishing these in the orchestrator's session.** When they're done, their branches are pushed to GitHub:
  - VibeComfy `r13/sfxfix` (structural pass 2);
  - VibeComfy `r13/musicfix`;
  - Astrid `r13/ttsfix-ag`, plus VibeComfy `r13/ttsfix-vc` if needed.

  All are based on VibeComfy `a8a7be7c` (the declarations pass: every ready template declares its models as records) and Agent `f9214240`. The orchestrator messages you each SHA as it lands. Until then, start on item 3.
- **The candidate branch is Agent `r13/compose`** (it starts from `f9214240`, plus test and log fixes). Cut every Agent branch from it.

## You own
1. **Judge each pushed fix against the owner's rules,** before you combine it. Specifically:
   - **SFX:** one module owns the socket-type vocabulary, with a ratchet test. One field holds a pack's commit. Offline identity resolves for every cached pack. A CPU check type-checks every ready template's public inputs offline.
   - **TTS:** did it look for an upstream node fix before extending the node's existing declared patch? Did it list every config attribute `transformers` 5 dropped that the node reads? Is the CPU proof real, with no weights?
   - **Music:** one source for the admitted digest, and a CPU check that every ready template's canonical first build matches.

   Send rework with a clear brief where a fix falls short.
2. **One VibeComfy branch for the candidate:** `r13/cells-vc`, from `a8a7be7c`, combining the accepted fixes. Run the union of their focused proofs. Then have a Terra worker pin it into Astrid on a branch from `r13/compose`, the same files as `b306b2be` changed: `astrid/packs/runpod/pins.json`, the recipes, the engine yaml and the Windows environment. Include any digest or tool-catalog regeneration the pin needs, and keep `test_no_other_tracked_file_copies_the_pin` and the pins tests green. Hand the orchestrator both SHAs.
3. **Two log gaps, one small Terra card on a branch from `r13/compose`:**
   - `astrid tasks logs <task>` requires `--project`. It should default to the selected project, the way other task commands do.
   - No Astrid skill tells an agent how to get a run's logs. Add `astrid tasks logs <task> [--name …]` and `astrid generate failure` to the right skill under `astrid/core/resources/skills/`, in two or three plain lines.

   Then have a fresh Opus sub-agent check the wording.
4. **The CPU preflight, as one thing.** The SFX and music fixes each add a CPU check over every ready template, and TTS adds a check that a node's config loads under the locked dependencies. Make sure these sit together as one coherent offline preflight, not three unrelated tests. Tell the orchestrator how it could grow into Plan 50's offline harness.

## Not yours
- Edit (machines lane K1).
- Live-lane files: `astrid/packs/runpod/`, `astrid/core/machines_cli.py`, `astrid/installer/`, `astrid/core/execution/`, `astrid/core/generation/`, `astrid/packs/vibecomfy/`. If a fix needs them, send the finding to the orchestrator. The pin in item 2 is the one exception, and touches only the pin files listed.
- Full-suite comparison (the test lane).
- Any paid or GPU work. Stage 2, the live retest, stays with the orchestrator.

## Rules
- **No RunPod or paid calls of any kind, from you or your workers:** no api.runpod.io, no rest.runpod.io, no `astrid generate`, no `astrid machines`. The network proxy may inject a real key. Put this in every worker brief.
- **Codex:**
  - always `-s danger-full-access`;
  - always `-c model_reasoning_effort=<level>`: high for Sol and Astra, medium for Terra, low for Luna. Check that the log header shows it;
  - `-c agents.max_threads` as high as the CPUs allow;
  - Luna sub-agents for all reading and mechanical work.
- **No full test suites locally;** focused proofs only.
- **Git:**
  - no push to `main`, `cand/*` or Release 12 branches;
  - no force-push, no rebase;
  - never read `.env`, credential files or `~/.codex`;
  - no AI model names in commits or PRs.
  - Commit trailer: the one your session's system prompt gives.
- **Before deleting any clone,** run `git worktree list` from it.

## Reporting
Send short messages to the orchestrator, leading with any decision you need:
- after setup;
- when a branch is ready, with its branch, SHA and proof;
- when blocked.
