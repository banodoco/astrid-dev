# Release 13 cells manager: handover (12 Nov, 23:15 UTC)

Brief: [cells-session-brief.md](../cells-session-brief.md) (on `r13-progress/decision-log`). Log, with every ruling: [cells-log.md](../cells-log.md) (this branch, `r13-progress/cells-log`). Local state: `/home/user/cells/` (`run.yaml`, `briefs/`, `logs/`, `evidence/`); Codex launcher `/home/user/cells/bin/card.sh <name> <model> <effort> <worktree> <brief>` (always full access, explicit effort, thread cap).

## Candidate state
- VibeComfy `r13/cells-vc` **`b3f20f33`**, frozen: music, both SFX fixes, recapture (`pack_identity_commits`), POSIX model paths, the defaults fix, the `preflight` marker, wan_animate to drafts.
- Agent pin `r13/cells-vc-pin` `7eb60798`, merged in `r13/compose`; compose is now `e24853a8`.
- Gate `r13/preflight` `79bab65a`, handed over. Five live cells PASS catalog, schema and rebuild; TTS constructor PASS; four constructor UNVERIFIED. Cells come from `scripts/live_cells.json`.
- Also handed over: `r13/catalog-fixes` `1cca5aab`, `r13/sfx-route` `c4b01ec2`, `r13/catalog-two` `aa556c9b`, `r13/fallback-hash` `c9c05673` (group B), `r13/h3-schema-helper` `195e847f`, `r13/ttsfix-3` `fae4b09b` (merged), `r13/ttsfix-4` `5123240b`.

## Running cards
1. **Placement redesign**: VibeComfy `r13/cells-vc-fix` (`14e5690e` carries the known loader class; `cda37a7e` makes analysis record unknown placement with a reason, so only the fetch and staging owners raise). Codex Sol, card `vcfix3`, brief `briefs/vcfix2.md` plus its addendum.
   - Proof: Agent `test_windows_gpu_availability.py` (G), `test_generate_target_journey.py` (E), `tests/packs/vibecomfy/test_local_server_run.py` (L1–L3), `tests/packs/test_vibecomfy_runtime_real_service_integration.py` (L4), each run on `b3f20f33` and on the fix. VibeComfy focused tests via baseline-diff, plus `make template-index` and a digest check.
   - First a control run with R12's VibeComfy `e65f4941`: on the fix, the windows tests reached `EngineNotInstalled` (run setup or a real fault; to be decided).
   - **L2:** `staged Python semantic digest differs` instead of `failed hash verification`. If the refusal is deliberate, the Agent test asserts the typed refusal; if not, fix VibeComfy. **L4:** `vibecomfy.import` refuses a non-empty output directory; test or product, decided with evidence.
2. **Next on the same branch**: `briefs/vcfix4.md` (Sol). Backslash model paths: normalize `\` once at ingestion (owner ruling: Windows-saved workflows must import; `..` and absolute paths stay refused). CFGGuider ×2: find the cause.
   - Proof adds `tests/sdk/test_generation_target.py` (whole file), `test_entries.py` (2 ids), `test_local_run_site.py` and `test_t4g_local_complete.py`.
   - Then: merge into `r13/cells-vc`, one re-pin (`scripts/vibecomfy_pin.py <sha> --checkout /home/user/vibecomfy`), hand the SHAs to the orchestrator and the test lane.
3. **sdk-target-tests**: Agent `r13/sdk-target-tests` `f2e90305` (card `sdkt`, Terra, finishing). The unqualified-catalog tests build their own unqualified entry; wan-2.2 i2v's local route is not re-added.
4. **Catalog contracts #342–#344**: staged as VibeComfy `r13/cells-vc-next` `ce4acd54` (with `r13/ltx-flf`) and Agent `r13/contracts-land-2` `6ee65b1c`. After the regression fix: merge it into `cells-vc-next`, re-pin, hand over. Due at the cut line, Fri 13 Nov 18:00 UTC. The all-entries T14 test and the ratchet (`r13/catalog-inputs`) land after #607 (engine lane).
5. **Lifecycle**: once the machines lane's runpod-lifecycle `r13/rest-v2` exists, VibeComfy depends on that one commit, or re-vendors its wheel at it. This only matters for VibeComfy's own `runpod` and `prepare` commands (the host uses `--no-deps` and `pins.json`). Before 15 Nov.

## Rules
- No RunPod or paid calls in any brief; `astrid generate` only with `--dry-run`. Never read `.env`, credentials or `~/.codex`. No pushes to main, `cand/*` or R12 branches; no force-push or rebase.
- **Structural fixes only:** one declared source per fact, one path, no shims, no silent defaults; find the deeper cause.
- **Agent R-6:** no xfail, skip or known-failures list; a red new test doesn't land. Never weaken a check; a test changes only to assert a deliberately changed design.
- Every Codex brief: `-c model_reasoning_effort` (high for Sol and Astra, medium for Terra, low for Luna), full access, Luna sub-agents. If Codex hits its usage limit, fall back to Claude sub-agents and tell the orchestrator the exact message.
- Findings go to astrid-dev issues (`observation:`/`bug:`/`idea:`, About Plan 39). Filed: #605, #607, #610, #622, #626, #630.
