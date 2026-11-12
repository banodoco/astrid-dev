# Release 13 cells manager log

Append-only. The NOW block is replaced; entries below it are never edited. Entries flagged **REVIEW** change what a user sees, trade scope against time, or touch another stream. Brief: [cells-session-brief.md](cells-session-brief.md). Reports to the Release 13 manager (orchestrator).

## NOW (17:25 UTC)

| Item | State | Next |
|---|---|---|
| 1. Judge fixes | TTS `eb594e09` (merged in `r13/compose`) judged short; rework `r13/ttsfix-2` (Sol, high) running. SFX (pass 3) and music still with the orchestrator | Judge each SHA as it lands |
| 2. Pin | `r13/cells-pin` from `fc4b36d`, pinning VibeComfy `a8a7be7c` (Terra, medium), running; re-pin to `r13/cells-vc` later is one bump | Read diff, rerun proofs, hand SHA |
| 3. Log gaps | Done in the orchestrator's session: `90ae9c31`, merged (`fc4b36d`). One resolver (`astrid/core/cli/current_project.py`) for tasks and timelines | — |
| 4. Offline preflight | Survey done (below); design waits for the SFX and music checks | Design once they land |

Heads: Agent `r13/compose` `fc4b36d`; VibeComfy base `a8a7be7c`. Spend: none.

## Entries

### 17:05 UTC — Started
- Every Codex launch goes through one launcher (`-s danger-full-access`, `-c model_reasoning_effort=<level>`, `-c agents.max_threads`), which checks the log header shows the effort. Accepted IDs on this sign-in: Luna and Astra at 6, Terra and Sol at 6.1.
- **REVIEW** Log gaps: the brief says other task commands already default to the selected project; they don't. All eight `astrid tasks` verbs share one `--project` argument with `required=True` (`astrid/core/cli/domain_tasks.py` `_add_project_arg`); the timelines family is the one that falls back to the runtime's current project. Ruling: fix it once in the shared argument, through the path timelines already uses, so every task verb gets the default, not only `logs`. This may overlap Group B's T11 (default project); flagged to the orchestrator with the branch.

### 17:25 UTC — Scope change; baseline; TTS ruling; preflight survey
- The orchestrator's session already did log gaps (`90ae9c31`) and TTS (`eb594e09`), both merged into `r13/compose` `fc4b36d`; no VibeComfy TTS part. My duplicate log-gaps worker stopped with no commits. The REVIEW note above stands for the orchestrator (all task verbs now default).
- Baseline, VibeComfy `a8a7be7c`: env smoke ENV-PASS; `tests/test_ready_templates.py tests/test_cli_models_fetch.py` 82 passed, 2 failed, 3 skipped. Failing on the base: `test_template_index_matches_ready_template_discovery`, `test_native_wan_animate_template_declares_frame_count_binding`. Log kept in the session (`evidence/vc-a8a7be7c-focused.log`).
- Pin card: Agent `r13/cells-pin` from `fc4b36d`, VibeComfy `a8a7be7c`, through `scripts/vibecomfy_pin.py`, mirroring `b306b2be`'s files, with generators for anything else that depends on the pin; base-vs-candidate `baseline-diff` on the pin, recipe, installer-source and CPU patch tests.
- **TTS ruling:** `eb594e09` falls short on two of the brief's questions. Only `pad_token_id` is named; nothing lists the other `PretrainedConfig` defaults transformers 5 dropped that the node reads. The CPU proof round-trips the config but builds no model. Upstream was checked for the node, not for Qwen3-TTS's own package. Rework `r13/ttsfix-2` (Sol, high): upstream first; attribute table from both transformers versions' source; models constructed on the meta device from the patched node source under the lock's transformers and torch, failing without the patch; any further attribute in the same declared patch, own commit. Touches the live lane's patch and digests, as `eb594e09` did; told the orchestrator.
- Preflight survey: VibeComfy enumerates ready templates in one place (`vibecomfy/registry/ready.py` `_discover_ready_templates`); `tests/test_ready_templates.py` globs on its own instead. `test_template_roundtrip.py` checks first load against a reload, not the admitted digest. The object-info identity lookup matches `git_commit` only: 13 of 49 cache files carry it, 42 carry `pack_version`. Agent has no check over every catalog entry (T14 open), and the `engine_deps` lane (from `eb594e09`) has no CI job. There is no Plan 50 folder on astrid-dev; the closest stated harness is `structural-runpod-design.md` §7 Piece D (offline end-to-end harness).
