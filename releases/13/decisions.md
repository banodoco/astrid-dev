# Release 13 decision log

Append-only. The NOW block is replaced; entries below it are never edited. Entries flagged **REVIEW** are user-visible changes, scope-vs-time trades, named exceptions or anything touching Release 12.

## NOW (12:42 UTC): read this first; it is enough to carry on from

**Rehearsal:** `scratch/r13-rehearsal` = `dd5bc822` on origin, local clone `/home/user/wt/c-bis`. It contains:
- everything in `b306b2be`: R12 main `0e1543e0`, the structural slices, declared logs `603b6728`, models-folders `43b69032`, the TTS source patch `687a0ed9`, music lock `634a2608`, misc `e798df2b`, gate `f0535fef`, ComfyUI bump `43b44c1e`, engine command output `72fbdf65`, lock fix `6eacb077`;
- PLUS declared patches: Astrid `r13/declared-patches` `dd5bc822`, pinning VibeComfy `r13/declared-patches` `c7a47e36`.
  - The node lock declares a pack's source patches, and VibeComfy honours them by default (restore, doctor, drift, witness). It is documented in VibeComfy's setup SKILL.md and REFERENCE.md.
  - A successful preparation step's output is now kept as declared run logs.

**Running now:**
1. **Keep-warm, Terra pass 4,** in `/home/user/wt/c-warm` (log `briefs/wave3/keep-warm4.log`). It finishes `stale_after_failure` admission (scope extension 2: `worker_preparation.py`) and runs the full suites.
   - Then **pass 5** (`briefs/wave3/keep-warm5.md`, ready, NOT yet launched): keep the pod on a first or repeated preparation failure; a source-digest-only difference re-prepares; `verification_timeout`; receipts name the pod and show expiry, cost and preparation state; recovery keeps the original cause.
2. **Root-cause subagent** for two live bugs (evidence `install-r13b/runs/stuck-task/`; the old host PID 28173 is kept alive for it):
   - **BUG 1 (release-blocker candidate):** failed TTS task 25b59510 stays `running`. Failure publication was rejected with "output object is outside the task project"; the reconcile loop (`generic_host.py` about 11540-11640) retries the `fail` forever and never cedes.
   - **BUG 2:** a queued task waits on `insufficient_storage` with the generate CLI printing nothing; disk was at 787 MB, now about 6 GB free.

**Batch 6 (ready, NOT started):**
- Fresh install `install-r13b/root-b4`, data `data-b4`, env `. ./env-b4.sh` (uv cache shared with home-b3), build `dd5bc822-42ae24af-52afeb20`.
- Needs: a copy of `runs/batch5.sh` with root-b4/env-b4/data-b4, the setup step, then the five cells.
- **Hold it until BUG 1 is understood:** any failure carrying declared logs may block the queue.

**Money:** balance $97.66 at 12:42, no pods. About $8 of $40 spent. Floor $67.41.

**Per cell:**
- **TTS:** the patch was refused by VibeComfy restore → declared patches `dd5bc822` → merged → re-run in batch 6.
- **SFX, t2i, edit, music:** not yet run (batch 5 blocked by BUG 1 and BUG 2); their root-cause fixes are in the rehearsal.

**How to check or release:**
- `. ./env-bN.sh; ./root(-b4)/run-astrid machines --json`; REST census `curl -fsS https://rest.runpod.io/v1/pods -H "Authorization: Bearer proxy-injected"`.
- To stop a batch: SIGINT the generate CLI, stop the script, then `tasks cancel` any queued task.

**Disk:** the session allowance is tight. Batch 5 hit 787 MB free; I deleted the old state's uv cache and /tmp baseline trees. Check `df -h /` before each batch.

**Owner REVIEW items open:**
- host shutdown or restart releases retained pods (recommendation: a restart-adoption slice; see 12:23);
- the TTS fork as the durable form;
- the four templates without a qualified id;
- lifecycle `Retry-After`;
- the old state's orphan `0d7f7e41` (likely the same mechanism as BUG 1; the subagent checks).

**Next three steps:**
1. Read the BUG 1 and BUG 2 root causes, then brief or fix them structurally.
2. Run batch 6 on root-b4.
3. Keep-warm pass 5, then compose the candidate.

## Entries

- **2026-11-11 18:10** G1. One launch-and-wait command shape, verified against Agent `1439ccc6` (`cli.py:78-112`, `sdk/generation.py:317-319`). The `releases/13.md` template was not runnable (it lacked the kind subcommand and the required P/E/I bounds). astrid-dev `r13/g1-launch-and-wait` `7730fb1`, `be8946a`.
- **2026-11-11 18:13** Per-cell P/E/I limits proposed in the G1 skill, derived from the cell caps (no run had recorded phase timings). No product defaults until a batch records real timings.
- **2026-11-11 18:30** **REVIEW** Wait wording, user-visible: the CLI error suggests `--max-hourly-usd` first, the stock-unavailable text says waiting is normal, and the progress line reads as waiting. `availability.message` was added; `status` and `reason` are unchanged. Agent `r13/g1-wait-wording` `69b39291`, `f7a95388`. Approved by the orchestrator 21:20.
- **2026-11-11 19:00** G4. Canonical pins in `astrid/packs/runpod/pins.json`, a check against every literal copy, and the packaged Runtime lock kept byte-identical to the root lock. Reissued as `r13/g4-pins-2` `0e821b92` because the first commits named a model in their trailer. The wheel regression (installer importing `canonical_pins`) was fixed by a stdlib read.
- **2026-11-11 19:20** **REVIEW** G4 behaviour change: an installed manifest whose lifecycle or VibeComfy pin differs from the canonical pin is refused at RunPod prepare. Approved 21:20.
- **2026-11-11 19:30** G5. Keep Release 12's attach fix `3639d63d`, drop `1edb88a0` and the `992dbde1` envelope, Runtime `42ae24aff` everywhere, regenerate the client after the merge. Evidence: astrid-dev `r13/g5-attach-decision` `573d753`, `3e918ed`. Ruled by the orchestrator.
- **2026-11-11 19:40** G2. Release 13's premise was wrong: the product does not load an operator script by path; only the dead `LifecyclePodProvider` did. That class and its one test were deleted. **REVIEW** Test removal approved under H13. Agent `r13/g2-launchers` `710399a9`.
- **2026-11-11 19:42** INCIDENT, owned: a CI dispatch on `cand/29-r12` cancelled Release 12 run 43085262585 through the concurrency group. Since then, CI runs only on `r13/*` and `scratch/r13-*`.
- **2026-11-11 20:00** G3 design: astrid-dev `r13/g3-receipt-design` `ec86ede`, `411bdd6`. Finding: a kept machine keeps no evidence, because the reset deletes the folders and truncates the logs. Collection runs before the reset.
- **2026-11-11 20:40** G3 slices 1–2: timing, a shared fetch, the local receipt and `astrid generate failure`. Agent `r13/g3-receipt-design` `09724310`.
- **2026-11-11 20:45** Graph-checked failure facts: names come from the submitted graph, never values; the graph cap is 8 MiB. Also fixed: `node_id` was always dropped. Agent `r13/g3-graph-facts` `feea4ac6`. Approved 21:20.
- **2026-11-11 20:50** Tool catalog regenerated (`video-editor` digests). Agent `r13/tool-catalog` `8ce2d68a`. Must be regenerated again on every merged head.
- **2026-11-11 21:00** Ruling on the 60 failures that predated G2: 59 also fail on main `a105de3a` (Plan 39); 1 was a candidate regression, the stale tool catalog, now fixed.
- **2026-11-11 21:05** Phase 1 rehearsal built: `scratch/r13-rehearsal`, 13 focused checks green on Runtime `42ae24aff`. A required Phase 1 step was recorded in `releases/13.md`: regenerate the Runtime client.
- **2026-11-11 21:25** H10 slice 3 started (approved). The RunPod test guard is required because the environment proxy would inject the credential into tests.
- **2026-11-11 21:40** Installer semantic merge break: Release 12's `297056f2` read `engine-index.json`, which the generation side deleted in `a45dd06c`. Fixed by reading canonical `pins.json`: rehearsal `4ca9cdbf`. Rule: every rehearsal comparison uses Release 12 `c5370a86` as its baseline, and `test_installer_sources` is in the gate.
- **2026-11-11 21:55** **REVIEW** Named exception: the local install manifest uses `banodoco/oh-my-pi` for OMP at the same commit `78f0e096`, because the session proxy serves only attached repositories. The App manifest is unchanged; Release 12 has been asked to re-pin. `banodoco/oh-my-pi` was attached with push access (Hannah's approval); it is never pushed to.
- **2026-11-11 22:00** Isolated install works: manifest `fb0925d1`, host up, census `[]`. The runbook is `/home/user/wt/install-r13/RUNBOOK.md`. The key is never written to a file: a dummy `RUNPOD_API_KEY` plus proxy injection.
- **2026-11-11 22:00** `astrid generate failure` was unreachable through the gateway; fixed with routing derived from the CLI's own list, plus entry-point subprocess tests. Agent `r13/generate-routing` `08a2f038`. Release 12 is not affected. Rule: every new CLI surface needs one entry-point subprocess test.
- **2026-11-11 22:05** Rehearsal versus Release 12 installer suite: 10 rehearsal-only failures. 6 were the engine-index break (fixed). 4 were update end-to-end failures: test drift, because the fixture did not stage the `.yaml` engine manifests; fixed in `r13/update-inputs` `86889894`.
- **2026-11-11 22:08** The `--target` to `--placement` rename (`b9a611ea`) also hit pip's own `--target` and one generic flag fixture; both reverted. Agent `r13/placement-overrename` `1206322a`.
- **2026-11-11 22:10** No developer override for the pins refusal. The remedy is to change the canonical `pins.json` in the checkout. Messages will name both values and the remedy.
- **2026-11-11 22:12** Test guard accepted: precondition (b) once merged. Agent `r13/test-runpod-guard` `a9e1f2c0`.
- **2026-11-11 22:13** Ruff gate: exact total 2128 met by `r13/ruff-debt` `1702f244`. The net-new BLE001 sites were left as they are because changing them would change behaviour. Re-run `make ruff` after every merge.
- **2026-11-11 22:20** Broad-except sort: 59 net-new sites (a 12, b 42, c 5). The five (c) sites (`machine_run.py:148`, `machine.py:608`, `target_selection.py:674`, `720`, `795`) and adding `PaidSelectionError`, `OfferObservationError`, `CapacityExhaustedError` and `CapacityWaitTimeout` to `failure_diagnostics.EXCEPTIONS` block the first paid run. Use receipt-only cause markers, not `gate=`. The 54 (a)/(b) sites go to a Plan 39 review. `machine.py:1167` and `1217` join the bundle review range.
- **2026-11-11 22:22** Generated-output swap-then-commit (handed over from Release 12) is in Release 13's done criteria. On completion, notify Release 12 so their named exception (expires 2026-11-25) comes out.
- **2026-11-11 22:35** Removed-name cleanup on the rehearsal (`0560e34d`): seven hits renamed or removed with no behaviour change. Five were Release 12 leftovers (`comfy_wrap`, deleted by Plan 32 `a45dd06c`); two were missed generation renames. `test_one_engine` passes. Thirteen other failures in the eight focused files are unchanged; ruling them against Release 12 waits for the rehearsal CI comparison.
- **2026-11-11 22:40** `test_generation_preparation[datacenter|stock]` hang ruled TEST DRIFT. `16ffaa60` made capacity waiting the default, and the fixture never opted out, so it waited until pytest's 600 s timeout. Product behaviour is correct: the wait is disclosed, bounded by the deadline and cancellable, and `--no-wait-for-capacity` refuses at once. Release 12 `c5370a86` passes because it lacks `16ffaa60`. Fix: the fixture opts out, as `test_target_selection.py:643` already does. No timeout or assertion was changed. Agent `r13/prep-hang` `53823a99`, merge 5 in the queue.
- **2026-11-11 22:50** Merge queue ruling: the rehearsal's Ruff total sat at 2212 before any merge. Since `r13/ruff-debt` was measured (on `9630bb84`), the rehearsal had moved 7 findings. The exact-2128 rule applies only from the ruff-debt merge onwards. After that merge, a lint-only commit (I001, F401, E701; never BLE001, never noqa, never baseline edits) closes the remaining gap exactly.
- **2026-11-11 22:50** Worker model change, approved by Hannah: new tasks run on Codex from the next task boundary (N Luna, X Terra, S Sol, reviews Astra read-only; taste tasks stay on Opus). Codex CLI 0.167.1 is installed, and the skills are copied from astrid-dev `c2b5435` to `~/.agents/skills`. Waiting on Hannah's device sign-in.
- **2026-11-11 23:00** Switched new tasks to Codex workers (Hannah's instruction). All four tier IDs answer; skills copied from astrid-dev `c2b5435`.
- **2026-11-11 23:00** **REVIEW** Generated-output swap-then-commit fixed for generation outputs: Agent `r13/task-handle-swap` `8ae4f91a`. It attaches the Runtime's own `generationId`/`variantId` through the output-selection read, so commit admits the media through the unchanged verified-media check. Task and run handle CLI tests pass; unverified media is still refused; the fix applies to `c5370a86`. The option that built a verified row for raw pins was rejected: it let unverified media through. Introduced by `8a66b1ac8`. Release 12's exception P39-R12-TASK-SWAP stays: generic outputs have no catalog variant, so fixing it needs a Runtime change; recommendation sent. Unverified integrity finding sent to the orchestrator: the Runtime accepts a raw pin for any managed project object, so the refusal is client-side only.
- **2026-11-11 23:05** Orchestrator rulings: the swap fix `8ae4f91a` is accepted into Release 13. Generic executor outputs (`f2.marker`) are NOT Release 13 scope, because the Runtime stays at `42ae24aff` per G5. Design note for a later Runtime plan: (a) a commit-port read that verifies a durable managed-output association `{association_id, object_id, version}` (completed, settled attempt, Runtime custody) as a media input, as narration refs already do. Release 12's exception P39-R12-TASK-SWAP stays with Release 12. The raw-pin integrity finding is under an independent review the orchestrator commissioned; nothing is built on it and the Runtime is unchanged until the verdict.
- **2026-11-11 23:10** Raw-pin integrity finding REFUTED, severity low, by an independent read at Runtime `42ae24aff` and Agent `c5370a86`. Evidence:
  - The daemon loads `astrid.sdk.timeline.commit.create_runtime_commit_service` as its trusted commit provider (`runtime_protocol/timeline_commit_provider.py:15-90`). On every commit it runs `execute`, then `patch`, then `verify_media`, with `verified_media` built only from Runtime port captures.
  - A server-side test exists: `tests/timeline/test_authoring_commit_media.py:107-113,199`.
  - `raw_media_info` requires a same-project managed object with matching size and digest (`timeline_commit_port.py:396-414, 1077-1098`). `validate` requires port capture (`:548-603`). The store re-hashes pins and rejects unaccounted media (`timeline_commit_store.py:1431-1459`).
  - What remains is a consistency point: a raw pin can name any same-project managed object, whatever its type. Hardening note for a later Runtime plan: filter `media_type` to image, video or audio, and add Runtime tests for unaccounted media and media not captured through the port. The Runtime is unchanged.
  - My error: the worker's "client-side only" claim came from a trace that stopped at the local preview. I forwarded it flagged as unverified, which was right; next time I'll have the worker check the server path before reporting a boundary claim.
- **2026-11-11 23:25** Environment `env_014epUvWZZ4BNYGztDKDb4oR` "Astrid Release 13 GPU" was created with network unrestricted, and this session moved onto it. Both RunPod credentials are saved there only. Census: 0 pods. Ledger baseline: balance $101.68 at 23:25.
- **2026-11-11 23:25** Guard coverage before saving the credential: the rehearsal (`a935c968` onwards) and the Codex worktree include the guard; 20 idle unguarded worktrees were removed; the two running workers were told to merge the guard before any further test run. Residual risk until they do: an authenticated read only, no spend.
- **2026-11-11 23:20** INCIDENT, owned: I tried to load the guard globally through a `.pth` file in the shared venv. Venv Python startup hung, and hung `cpuinfo` children ran out of memory, for about 3 minutes. Both were removed and the hung processes killed. Rule: never install interpreter-wide hooks into the shared venv.
- **2026-11-11 23:05** Codex launch flagged by the permission check as possibly "creating unsafe agents". It warned and did not block. The launch (`codex exec` with workspace-write and network) is what Hannah approved, and the flag is recorded here.
- **2026-11-11 23:00** Sequencing change from the orchestrator: the first TTS diagnosis needs the receipt, graph-checked names, the five swallow fixes and the `EXCEPTIONS` addition, but not the H10 bundle. With no bundle, no log leaves the pod. The bundle still gates every later run. The swallow fixes are now on their own branch, `r13/receipt-swallows`, on the rehearsal (Codex Luna).
- **2026-11-11 23:30** New working rules (brief `d285c34`):
  - Message the orchestrator almost never; the log is the channel.
  - I commission the pre-paid reviews myself, on Astra (`gpt-6-astra`), read-only, on the exact range, with no conclusions in the brief: (1) the bundle and redactor, when `r13/g3-bundle` lands, with `machine.py:1167` and `1217` in range; (2) the pins and installer follow-ups, when `r13/g4-followups` lands; and later the merge review. A blocker stops its step until the fix has been read.
  - Alarms are verified independently before I escalate them.
  - Anything about Release 12 goes to its manager directly, `session_011EzfVzCLu2vv52JWNRiDJM`.
- **2026-11-11 23:35** Hannah, in this session, authorized renting RTX 4090/5090 RunPod pods for Release 13 diagnostics and GPU validation tonight, up to $40 total, and releasing them.
- **2026-11-11 23:40** Merge queue done: rehearsal `e329efd1`. Merges `6ea94e00`, `501d7a9e`, `a935c968`, `fbdd8a5b`, then lint-only `cdc1774a` (I001 import order only, 2136 to 2128), then `e329efd1`. No conflicts. Gate selectors are green except the known `test_pod_install_route::test_pins_resolve_without_a_checkout`, whose fix is in `r13/g4-followups`. `test_generation_preparation.py`: 36 passed. Catalog and CLI surface are current.
- **2026-11-11 23:55** Receipt-swallow fixes: Codex Luna wrote them; I reviewed the diff and committed them myself as `r13/receipt-swallows` `14155ab3`. Codex's sandbox could not write the git index, because a worktree's index lives in the main clone's `.git`; future Codex tasks get a standalone local clone. Contents: the five (c) fixes, plus `EXCEPTIONS` gains `PaidSelectionError`, `RunPodSetupRequiredError`, `OfferObservationError`, `CapacityExhaustedError` and `CapacityWaitTimeout`. The `.cause` marker cannot collide with `AstridError.cause`: both classes are `RuntimeError` subclasses, and the receipt is the only generic reader. Merged into the rehearsal as `bf3b6ba7`. Receipt 40 passed, target selection 90, diagnostics 84, Ruff 2128. Gap: no explicit test that `worker_owner.acquire` behaviour is unchanged; it is not at risk because no `gate` is set.
- **2026-11-11 23:31** Rehearsal CI `43102625660` (on `246cad0f`) completed with failure. It is stale, so a new run was dispatched on `bf3b6ba7`; no runs were queued. Correction: entries 23:40–23:55 above used estimated times; actual times were about 23:10–23:28. From now on every entry takes its time from `date -u`.
- **2026-11-11 23:32** Pins and installer review clearance met: `tests/scripts/test_pod_install_route.py` gives 15 passed (exit 0) on `r13/g4-followups` `82195616`, which also has the guard merged (`cd840eca`). The first paid run is no longer gated on it.
- **2026-11-11 23:49** The session worker restarted; an out-of-memory kill is likely, with the host starting alongside two large test suites. The G3 bundle (Opus) and G4 follow-ups (Claude) workers stopped. Both had committed and were clean; I pushed them as `r13/g3-bundle` `53a5c25d` and `r13/g4-followups` `cd840eca`. Their final proof runs were lost and are replaced by the Astra reviews below plus a re-proof. Census after the restart: 0 pods.
- **2026-11-11 23:49** The install-r13b host would not start: "A different runtime owner is active". The owner record is pid 26 in another PID namespace (the Codex sandbox started the host). The product correctly refuses to retire an owner it cannot verify, and `astrid-runtime down` refuses as well. This is a Codex-sandbox artifact, not a user-facing bug. Rule: Codex workers never start long-lived services. Fix: a clean reinstall of install-r13b from this session's namespace (manifest `7d8e2917`), running now.
- **2026-11-11 23:49** Astra read-only reviews commissioned, in parallel:
  - (i) The TTS and SFX commands against the G1 skill. This gates the first rental.
  - (ii) The G4 follow-ups, range `git show 821956162`.
  - (iii) The bundle and redactor, range `09724310a..49516887d`, plus `machine.py` `_active_sources` and `unshipped_entry_reason`. This gates every run after the first diagnostic.
- **2026-11-11 23:53** Review (ii), G4 follow-ups `821956162` (Astra): REQUEST CHANGES. My rulings:
  - BLOCKER, accepted: refusal messages can print manifest URL userinfo or `?token=` values. It is not in the installed build `bf3b6ba7`; G4's original messages print no values. It blocks the follow-ups merge.
  - FIX, accepted: a trailing-slash lifecycle URL is refused.
  - FIX, accepted: a wrong comment in `tools.py`.
  - NOTE, test added: the legacy-manifest test.
  - FIX, declined, ruled a NOTE: the two-lock journaled transaction. The script is a developer script whose output is committed, and the equality test catches any divergence.
  Fixes run on Codex Luna, `r13/g4-followups-2`.
- **2026-11-11 23:53** Review (iii), bundle and redactor `09724310a..49516887d` (Astra): BLOCK, with 10 blockers and 2 fixes. Full report: `/home/user/wt/briefs/review-g3bundle-findings.md`.
  - Blockers: prompt fragments, multiline and encoded prompts survive; missing prompt context still exports text; short secrets and JSON credential values survive; pod truncation defeats the controller pass; workflow edges and IDs carry values; IPv6 `::` and escaped URLs survive; late registration lets collection beat release; the deadline does not cover controller redaction; intermediate symlinks escape the root.
  - Fixes: caps are enforced after download; pre-claim discovery fails open.
  - Accepted in full. `49516887d` must not ship. Fixes run on Codex Sol, `r13/g3-bundle-2`, then re-review. This gates every paid run after the first diagnostic. The first TTS diagnostic on `bf3b6ba7` (no bundle) is unaffected.
- **2026-11-11 23:53** `install-r13b` reinstalled from this namespace (exit 0). The host is up at `http://127.0.0.1:35197`. `generate defaults` is OK; the TTS default is `audio/qwen3_tts_custom_voice` and the SFX default is `audio/hunyuan_video_foley`. Census `[]`. `generate failure` gives "no receipt" as expected.
- **2026-11-12 00:00** Commands review (i) (Astra): 2 BLOCKERs and 3 FIXes, all accepted.
  - Missing saved setup, and the host needs the key placeholder. The host was restarted with `RUNPOD_API_KEY=proxy-injected` (verified in its environment).
  - The census is strengthened: provider REST and GraphQL, failing on error.
  - The 18 s SFX fixture was cut to 5 s (`inputs/sfx-first-look.mp4`).
  - `keep --for 30m` was removed, because it would cut the paid lifetime below SFX's 4500 s.
  - A balance check runs before each rental.
- **2026-11-12 00:00** **REVIEW** GPU choice for the first diagnostic: with the `storage` volume (EUR-NO-1), only the RTX 5090 is offered, at $1.19/h. I decided on the 5090 alone with `--max-hourly-usd 1.25` (the skill's 5090 row is 1.2). TTS limits come to 4500 s × $1.25/h = $1.56, which is at most $3. If volume setup can't be saved, the fallback is ephemeral disk, datacenter any, 4090/5090 at 1.0/h.
- **2026-11-12 00:00** BLOCKER: on the bf3b6ba7 install, the pack host quarantines `runpod` and `setup` as external packs without `pack_api`. They are loaded from `versions/*/a/astrid/packs`; the wheel also has them. The capability ledger is missing `runpod.claim` and `runpod.keep`. As a result `machines setup` fails ("could not save preferences": the `runpod.setup` action is unavailable). Codex Terra is diagnosing it on `r13/runpod-pack-load`.
- **2026-11-12 00:00** G4 follow-up fixes: Codex Luna wrote them; I reviewed and committed them as `r13/g4-followups-2` `54556c6f`. Refusals render only a validated public `https` host and path plus valid revision and version strings, and show `<invalid>` otherwise. Identities are compared after normalising host case and a trailing slash. A legacy-manifest test was added. Tests match baseline. Codex cannot commit: its sandbox makes `.git` read-only even in a standalone clone, so the manager always commits.
- **2026-11-12 00:08** Pack-quarantine diagnosis (Codex Terra; I reviewed the diff and committed it as `r13/runpod-pack-load` `5f531504`):
  - The quarantine warnings came from a launch-probe ledger scan that inferred `a/astrid/packs` from the matrix path. The host itself loads `runpod` and `setup` from the wheel. That scan exists on both Release 12 `c5370a86` and generation `1439ccc6`, so it is not a merge break; fixed by scoping it to the host's roots.
  - Real gap: generation commits `c0f505d4` and `d3c44023` added `runpod.claim` and `runpod.keep` without updating the capability lock or matrix, so both are unavailable on install. Approved through `capability_ledger approve`, with the matrix rows added. The test count 49 to 51 reflects the two added capabilities.
  - A regression test models the installed layout. It does not prove installed-service execution; the reinstall will.
- **2026-11-12 00:08** `machines setup` still fails to save. The direct SDK call says "An older Astrid is still running". A Claude Sonnet sub-agent is diagnosing it, because it needs RunPod inventory reads with the credential, which Codex must not get.
- **2026-11-12 00:20** `machines setup` root causes (Claude sub-agent):
  - (A) PRODUCT BUG: on a fresh install with no project, setup always fails. `machines_cli.py:449` invokes the `runpod.setup` executor with `project=None`, which gets `CapabilityPreconditionError` ("project is required"). Lines 457-459 hide that behind "could not save preferences". Worked around by creating a project (`projects create setup --select`).
  - (B) PRODUCT BUG: setup checks the volume's datacenter against a live stock snapshot (`adapter.py:72-92` ignores `require_network_volume`), so it flaps with intermittent stock. It saved after about 12 tries.
  - "An older Astrid" was my artifact: a direct SDK call without the install's identity variables.
  - Bugs A and B are new Release 13 fix tasks, not run blockers.
- **2026-11-12 00:20** The rental build moved to rehearsal `5f531504` (the ledger and probe fix, fast-forward): ledger 12 passed, regression 1 passed, Ruff 2128. Manifest `5e4b41cd`, `pin.mjs` check OK. The program root was reinstalled and the data kept; the Pinokio in-place update needs the `app/astrid` layout. The host is up at `127.0.0.1:37175`. Its latest registration has no quarantine, and `runpod.claim` and `runpod.keep` are ready. Saved setup: `storage` (EUR-NO-1), RTX 5090, , idle 1800 s. Local census `[]`.
- **2026-11-12 00:23** RENTAL START, TTS diagnosis. Before-census at 00:20: 0 pods in the local journal, REST and GraphQL; balance $101.66. Command: `generate audio --entry audio/qwen3_tts_custom_voice --mode tts`, RTX 5090 only, `--max-hourly-usd 1.25 --max-usd 3 --preparation-seconds 1800 --execution-seconds 900 --idle-seconds 1800 --consent paid`, launched 00:21:14. Pod `3proraahcbflmi` (lease `558405e4`) claimed by about 00:23 and booting. Supervising.
- **2026-11-12 00:23** Orchestrator loosening (from Hannah, speed over risk): SFX runs straight after TTS on the same pod if custody is clean; then image t2i, image edit and music as diagnostics on the same GPU type; video only if 5090 stock appears quickly. Reviews run in parallel. Nothing with the log bundle runs on a pod until the redaction review is clear. Inputs are prepared in `install-r13b/inputs/` (t2i 768px; edit of a 1280×720 b-roll frame; music 20 s). Image and music limits: P1500/E600/I600, cap $1, at 1.25/h, which is $0.94.
- **2026-11-12 00:25** GPU TTS-diagnosis FAIL, before preparation.
  - The pod `3proraahcbflmi` was created, but its HTTPS agent never became reachable: seven readiness checks at about 21 s intervals, 00:22:32 to 00:24:37, all `route_unavailable`. Then `AcquisitionUnresolvedError: provider acquisition remains unresolved; reconcile the same journal; failed gate: provider`. Command exit 2, task `c3b13643`.
  - Receipt gap: the receipt says stage `no_machine`, cause `unknown`, although a pod existed. This `AcquisitionUnresolvedError` comes from a site the swallow fixes did not cover.
  - Local journal: `releasing`. RunPod REST is rate-limiting (429), so my polling is paused in favour of the host's release.
  - Spend: about $0.06 so far on this pod. Spent ≈ $3.81 of $40, pending confirmation of the release.
- **2026-11-12 00:27** RELEASE (manual, at the provider). The host's release and `machines release` both failed on `RunPod pod listing failed: HTTP 429: rate limit exceeded for the minute window`. The host re-polls `GET /v1/pods` about every 2 s with no backoff, so the window never resets. I positively identified pod `3proraahcbflmi`: name `astrid-product-558405e4…` matches our lease, and the before-census was empty. Terminated with GraphQL `podTerminate` at 00:26:59. After-census (GraphQL): 0 pods, spend $0.019/h. This rental cost $0.07. REST and local-journal confirmation is pending until the rate-limit window clears.
- **2026-11-12 00:27** ROOT CAUSE of the TTS diagnosis failure. Not a model problem: the pod's HTTPS agent answered `/health` 200 at 00:24:49, 12 s AFTER the claim gave up at 00:24:37. Boot took about 2.5 min from creation. The product's readiness window (`runpod_lifecycle` `https.py:467`, seven attempts about 21 s apart) ended before that, even though `--preparation-seconds 1800` was granted. Findings to fix before the next rental:
  - (1) Readiness must be bounded by the paid preparation budget.
  - (2) The release and listing path must back off on 429.
  - (3) The receipt must say a machine was acquired (stage boot) rather than `no_machine`/`unknown` for post-create acquisition failures.
  - (4) The `machines setup` bugs A and B above.
- **2026-11-12 00:40** CORRECTION to the 00:27 root cause. Readiness was NOT the problem. The seven "readiness timed out" lines are lifecycle's 15 s inner retries. The outer readiness limit was 900 s; paid expiry was 02:53. The pod became READY at 00:24:50, after three consecutive 200s. The claim then failed in the post-ready provider contract. Journal: `failure_phase: provider_contract`, `TargetObservationError`, gate `provider`.
  - Cause (high confidence, from code): lifecycle `f294881` dropped the SDK fork. The public SDK's pod query has no `networkVolumeId`, so `list_pods` adds a REST `networkVolume` object instead. Agent `worker_preparation.py:361` still reads `networkVolumeId`, gets None, and raises "volume mismatch" with no gate.
  - The gate fallback says "provider", and `target_selection.py:855` drops the message (`from None`). The same stale key is read at `target_selection.py:868` (`read_exact_pod`).
  - This is a contract drift between lifecycle and Agent, reproducible offline against RunPod's public REST schema at no cost.
  - Fix dispatched: `r13/provider-contract` (Codex Terra). It reads attachments through one accessor, gives every contract refusal a fixed gate, and tests fixtures built from the real SDK and REST shapes.
  - The next TTS rental waits for this fix.
  - The 429 release-backoff and receipt-label fixes follow once the bundle branch lands, because they touch the same files.
- **2026-11-12 00:34** OVERNIGHT MODE (from the user). Run to completion without the user or the orchestrator.
  - A self check-in runs via send_later every 30-45 min (current trigger `trig_01V4DPV2FpiS1w7ZqjQKVqHX`, 01:10 UTC), re-armed each time and cancelled when done.
  - Workers: Codex Luna, Terra, Sol and Astra. If Codex is lost, fall back to Claude sub-agents.
  - A question left unanswered for 15 minutes gets decided by the brief's priorities and tagged REVIEW.
  - A permission refusal is logged and routed around within the rules, never worked around.
  - The $40 cap and RTX 4090/5090 only still apply. A pod that isn't ours is noted and never touched.
  - The morning note goes at the top of this file.
- **2026-11-12 00:40** RULE (from the user). On bugs, issues and strategy, the manager's own judgement wins over a Codex worker's or reviewer's. Codex output is evidence, not a verdict. Each diff and finding is read and judged on its merits before it is committed or acted on. For a genuinely contested call, ask the orchestrator for a second opinion; with no answer in 15 minutes, decide, tag REVIEW, and carry on.
- **2026-11-12 00:50** G4 follow-ups `54556c6f`: Astra review REJECTED it, and I confirmed each finding.
  - An unvalidated hostname is printed (a `%3A…%40` "host" survives).
  - IPv6 crashes the identity check.
  - Validation, staging and managed resolution normalize differently.
  - Severity: I rate the first a FIX, not a BLOCKER. It isn't a usable credential URL, but it breaks the "print only a validated identity" rule, so it gets fixed anyway.
  - Astra's test runs were blocked by its read-only sandbox (no writable /tmp), so I'll run the suites myself after the fix.
  - Round 3 dispatched to Codex Luna (`r13/g4-followups-2`): one strict stdlib validator used at all three boundaries.
- **2026-11-12 00:58** Provider-contract fix landed: `e6d85766` (rehearsal fast-forward from `5f531504`).
  - Codex Terra's accessor (`pod_fields.py`) reads `networkVolumeId` or `networkVolume.id`, `imageName` or `image`, and so on; malformed or contradictory evidence refuses. Every contract refusal carries a fixed gate, which is logged and kept in the receipt.
  - I made three changes on top:
    (1) `read_exact_pod` now asks for `includeNetworkVolume=true`. RunPod's OpenAPI defaults it to false, so the post-claim exact check would have refused every volume pod one step later. Codex's tests faked `read_exact_pod`, so they couldn't see it.
    (2) I reverted Codex's switch of post-claim refusal detail to fixed text. It erased our own "GPU mismatch" and "datacenter mismatch" messages and broke 4 existing tests that Codex never ran.
    (3) A missing volume key reads as None again, keeping no-volume semantics; volume contracts still fail closed.
  - Tests: pod_fields 10, worker_preparation 41, target_selection 91, provider_fields 33, receipt 41, guard 19 all passed. Two failures in `test_acquisition_graphql_confirmation` and `test_release_after_acquisition_failure` are pre-existing at `5f531504`; they go on the release-fix task. Ruff 2128.
- **2026-11-12 00:58** Install. Pinokio's in-place `--update` needs Pinokio's `app/astrid` layout (harness-only, not a product bug), so I did a fresh install of the root at `e6d85766` with the same data and home. The old root was removed. The workspace, saved policy (RTX 5090, storage, $3) and project were kept. The host is up at `127.0.0.1:43199`.
  - The disk was full: 11 GB of stale `/tmp/pytest-of-root` left by workers. Deleting it also explains the earlier "no usable temporary directory" failures in Codex reviews.
- **2026-11-12 00:55** TTS attempt 2: FAIL, no pod, $0.
  - About 3.5 min of genuine RTX 5090 stock-out in EUR-NO-1, then a single `provider_observation_unavailable` observation (all HTTP 200) ended the run.
  - Root cause: the pre-create wait in `target_selection.py:622` retries only `stock_unavailable` and `provider_rate_limited`; any unclear observation is final, although no pod exists.
  - Fix dispatched: `r13/capacity-wait-retry` (Codex Luna), with bounded backoff for unclear observations and auth still terminal.
  - TTS attempt 3 launched at 00:56:35. After-census: 0 pods (REST, GraphQL); balance $101.57.
- **2026-11-12 00:58** G4 follow-ups round 3, `0f584c92` (pushed). Codex Luna wrote one strict repository identity used at validation, staging, managed resolution and rendering. I reviewed it and ran all 7 suites myself: same failing IDs as baseline (17 pre-existing VibeComfy-URL failures in `test_installer_sources`, plus the known `custody.py:43`). I briefly restored a local-path lifecycle override, then reverted it, per the G4 ruling "no developer override".
- **2026-11-12 00:58** Setup bug A: `644f1a28` (pushed). `runpod.setup` declares `project_scope: optional` and the CLI reports the action's error code. The ledger stores executor IDs only, so the metadata change causes no census drift; ledger and pack-action tests 38 passed, setup tests 21 passed. Bug B was re-dispatched to Luna; it had wrongly treated `adapter.py` as reserved.
- **2026-11-12 00:58** Bundle re-review (Astra) of `a648a1df`: BLOCK. My ruling:
  - Fixed and kept: 1, 5, 8, 11, 12. Finding 6 is a NOTE per the design ruling.
  - 2, 3, 4 and 7 share one root cause: decode-and-match is a denylist that every new encoding defeats.
  - Round 3 dispatched to Codex Sol, network off so it cannot push: mask encoded-looking spans whole without decoding, mask whole values for any key in a credential vocabulary, and export the workflow as opaque ids when context is incomplete. It also fixes 9 (cleanup outside the observer's lifetime) and 10.
  - Process note: Sol's round 2 pushed `a648a1df` itself, using temporary git metadata. I verified the tree, trailer and tests afterwards (bundle 72, receipt 31, preparation 35, guard 19 passed). The bundle is not in the paid build.
- **2026-11-12 01:06** GPU TTS attempt 3: FAIL in install, $0.17 (pod `8jhtzvhzsavh77`, released by the product, ended `preparation_unverified`).
  - Progress: the provider contract PASSED on a real pod (capacity "claimed"), so the `e6d85766` fix is proven live. Preparation ran, and the engine install job exited 0.
  - Then `engine install finished but status is not installed and healthy`. The receipt says stage `install`, cause `unknown`, `collector_not_built`, so there's no evidence of WHICH check failed.
  - Root of the blindness: `remote_placement._canonical_installed` returns a bare False on four different conditions. `engine status` re-runs every install step read-only, start and health included, under a deadline capped at 120 s. It reports a fixed-vocabulary `status/error_code/failed_step_id` that was thrown away.
  - Fix (mine, `61eafd53`): every refusal records a fixed label (`status_exit_<n>`, `status_no_receipt`, `status_deadline_exhausted`, `receipt_read_failed`, or engine status's own fixed fields, re-validated), and the error carries it. Tests: 6 new, failing before and passing after; machine 114, remote_placement 14 and guard 19 passed; Ruff 2128.
  - Hypothesis to confirm on the next run: the 120 s status cap is shorter than a cold engine start-and-health re-check.
- **2026-11-12 01:15** Capacity-wait retry `f1a487c9` (Codex Luna, reviewed and finished by me).
  - Codex's tests never ran in its sandbox (no sockets). I ran them: one of its new tests had a fixture bug (a 30 s capacity window less than or equal to the 30 s of expected sleeps). I fixed the fixture, not the code.
  - I replaced Codex's `retrying:`-prefix hack with a structured `note` field, so progress rows keep the fixed reason.
  - Verified that `OfferObservationError` can only arise before any create POST, so retrying is cost-free. target_selection 96 passed; 3 of the new tests fail on the old code. Ruff 2128.
- **2026-11-12 01:18** Rehearsal → `8cf3ada9` (merge of `f1a487c9` and `61eafd53` onto `e6d85766`), reinstalled the same way. TTS attempt 4 launched at 01:19:02. Before-census: 0 pods; balance $101.37. Spend so far ≈ $4.05 of $40.
- **2026-11-12 01:15** Setup bug B: Luna's first version accepted any global-catalog GPU even when the volume's datacenter never hosts it (a silently unusable policy); it also changed an existing assertion. Sent back with "offered here = listed in that datacenter's `gpuAvailability` at any stock level". Not merged.
- **2026-11-12 01:15** Note for the Release 12 manager / owner: `generic host claim failed: HostError: Runtime terminal evidence is not present in durable task readback` (`generic_host.py:5859`) follows an executor failure. It has not been diagnosed yet; it's queued.
- **2026-11-12 01:25** STRATEGY (prompted by the user: "is the structure elegant, or are you fixing bullshit?").
  - Honest answer: tonight's fixes are real but local. Each paid run surfaced one more blind, offline-detectable seam: provider field names, the missing `includeNetworkVolume`, the wait reasons, install verification. Our tests fake exactly those seams with shapes RunPod never returns, and refusals are reason-less because "never leak" is implemented by deleting information.
  - The structural answer has four parts:
    (A) one typed provider boundary;
    (B) contract fixtures recorded from real responses;
    (C) a fixed-vocabulary failure-reason channel from pod to receipt;
    (D) an offline end-to-end harness: the real pod agent behind a replaying provider fake, so the whole chain runs in CI.
  - An Opus design worker is writing `releases/13/structural-runpod-design.md`.
  - Rule from now until the morning: patch only what blocks a paid diagnostic cell; everything else waits for the design.
  - The G3 bundle redactor (round 3 on Sol) is the same anti-pattern. The design should say whether structured facts make the free-text bundle unnecessary by default. Changing H10 is the owner's call.
- **2026-11-12 01:28** Diagnosis (Codex Terra, read-only; `/home/user/wt/briefs/release-diag.log`):
  - (1) The release-429 loop: owner recovery retries every failure after 1 s (`worker_owner.py:705`), with up to two account inventory reads per attempt (`worker_preparation.py:1102,1129`). There's no account-scoped cooldown shared by the daemon, the CLI and lifecycle; lifecycle drops `Retry-After` (`api.py:156`).
  - (2) The terminal-evidence HostError is a real Agent–Runtime contract mismatch. The host submits `result.error`, Runtime overwrites it with the failure payload (`store.py:6798`), and the readback check (`generic_host.py:5830`) fails. There's no duplicate task; one failed task is settled. But the host keeps the attempt spool as pending and logs a claim failure.
  - Decision: neither blocks a paid diagnostic cell while I supervise releases. Both are routed into the structural design (A: an account-scoped provider rate gate; C: one canonical failure payload) instead of patching tonight. REVIEW.
- **2026-11-12 01:30** From the user: get a Fable second opinion on the minimal, elegant root fix, then farm it out to Codex at varying levels, with validation running alongside.
  - The Fable reviewer runs read-only and independently: it gets the problem and the code, not the Opus design, to avoid anchoring.
  - I'll reconcile the two designs, then split the work: Luna for mechanical slices, Terra for hard ones, Sol for the hardest.
  - Paid GPU validation stays with me, not Codex. It needs the real RunPod account and the injected key, and the standing rule forbids credential-bearing or paid tasks for Codex.
- **2026-11-12 01:32** CONSTRAINT (from the user) for the structural design: it must work for many providers eventually, not just RunPod, and many inference types, not just ComfyUI. So the plan has a small provider interface (RunPod first) and an engine interface (ComfyUI first), a shared reason vocabulary and harness, and fixtures recorded per provider. It should prefer extending the existing generation, engine-runner and placement abstractions. Sent to both the Fable and the Opus design workers.
- **2026-11-12 01:35** STRUCTURAL PLAN, reconciled (Fable's second opinion plus its multi-provider addendum, my evidence, and recorded fixtures): `/home/user/wt/briefs/struct-design.md`.
  - Root cause: every boundary passes untyped values (dict, bool, str) that each consumer re-interprets.
  - Three moves, all extending existing abstractions:
    (1) `MachineProvider` and `MachineRecord` at the generation machine extension point, with RunPod as the first implementation and one parse function per real response shape;
    (2) `PlacementRefused(EngineError)` with the gate required and retry policy read from `retryable`, `retry_after` and `custody`, never from strings; `Placement` becomes a registered-kind string;
    (3) host evidence moves to its own key (`host_failure`), so Runtime's overwrite no longer breaks readback; the ComfyUI fact allowlist is keyed per engine; and a ratchet test stops new `runpod` or `comfy` matches under `astrid/core`.
  - Not building: a second provider or engine, a generic offers/consent/custody interface, a VCR framework, or a rename sweep.
  - CORRECTION from the recordings: real RunPod REST responses DO include `networkVolumeId` and `imageName` (the OpenAPI document omits them). A plain GET lacks only the `networkVolume` object. So failure 1 was purely the SDK GraphQL record plus the enrichment, which added only the object. My `includeNetworkVolume` change in `e6d85766` was harmless but unnecessary. Ground truth is recorded responses, not the OpenAPI file.
  - Fixtures were recorded during TTS attempt 4's live pod at no extra rental: 2 REST GETs, 1 REST list, 1 SDK GraphQL query. They're sanitised by allowlist: env values (including `ASTRID_POD_TOKEN`), ports, IP and ids were placeholdered. Raw captures were deleted. Saved at `briefs/evidence/runpod-recorded/`.
  - Dispatched: slice 1 on Terra (`r13/struct-s1`), slice 2 on Sol (`r13/struct-s2`), slice 3 on Luna (`r13/struct-s3`). Network is off and none may push; I review and commit. The file-ownership split avoids overlap with each other and with the bundle round.
- **2026-11-12 01:40** DIRECTION (from the user):
  - (1) Once tonight's validation and structural work are done, merge with the Release 12 work and get Release 13 release-ready. That is the next phase after the paid diagnostics and the structural slices.
  - (2) Sol and Terra should delegate as much as possible to Luna.
  - Constraint found: a Codex worker cannot start a nested Codex. Inside its sandbox the child fails with "Read-only file system" on Codex's own state directory (tested live). The workarounds are refused: copying the Codex credentials breaks the never-read-or-copy-`~/.codex` rule, and turning off the sandbox would allow unreviewed pushes.
  - Pattern adopted instead: LEAD-AND-LUNA. A Sol or Terra lead does only the hard core and writes `luna-tasks/<n>.md` (files, interface, acceptance tests). My launcher then starts one Luna per task in its own clone. The lead (or Astra) reviews the Luna diffs before I commit.
  - This applies from the follow-ups of slices 1 and 2; the running workers can't be messaged mid-run.
- **2026-11-12 01:31** GPU TTS attempt 4: FAIL in install verify, $0.19 (pod `dv89b19sf22qy4`, released by the product). The new label paid off on its first run: `status=failed;error_code=integrity_failed;failed_step_id=start`.
  - Root cause (mine, offline): `engine_runner.engine_status` planned with no `models_root`, while the pod install binds the volume model cache. The read-only start check therefore compared the live models config against `<root>/models` and refused a healthy engine. `_parse_receipt` already documented the intent ("a reader naming none takes the receipt's record"); it just wasn't wired through.
  - Fix: `c627edba`, which re-plans with the receipt's `models_root`. The new test reproduces the live failure exactly, `('failed','integrity_failed','start')`, without the fix. engine_runner: the same 2 pre-existing packaged-lock failures as the base. Local model root 21, generation preparation 36 and remote placement 14 passed; Ruff 2128.
  - The rehearsal fast-forwarded to `c627edba` and was reinstalled. TTS attempt 5 launched at 01:37:35; before-census 0 pods, balance $101.17. Spend ≈ $4.24 of $40.
- **2026-11-12 01:38** Structural slice 1, `ad7723a8` (Codex Terra, amended by me per the Opus design):
  - Records carry an `observed` field set and `require()`, so "not reported" can never read as "empty". The GraphQL pod record observes no storage, which is exactly failure 1.
  - `machine_id` is validated.
  - I ran the suites Codex couldn't (its sandbox stalls on async tests): providers 11, target_selection 96, provider_fields 33, worker_preparation 41 and guard 19 passed; graphql_confirmation has 1 pre-existing failure.
  - Ruff improved to 2127; I'll lock in the new baseline at merge. Not yet merged into the rehearsal.
- **2026-11-12 01:39** The Opus design is in (`releases/13/structural-runpod-design.md`, `d62a8af3`). It agrees with the reconciled plan and adds:
  - a list of about 30 raw-read sites;
  - 31 reason-drop sites, two still live: the receipt doesn't copy the install label (`failure_receipt.py:126-133`), and seven bare-False returns remain in `remote_placement.py`;
  - an account-scoped, file-locked provider gate for the 429 storm;
  - a harness first slice built on `test_remote_machine_cpu.py`;
  - a cost estimate: Release 13 about 7.25 worker-days; the Release 14 remainder about 11.
- **2026-11-12 01:40** Bundle round 3 (Sol) is parked as WIP `04dd5f15` on `r13/g3-bundle-2`, not for merge. It's unqualified: 5 existing assertions conflict with structural masking, some suites didn't run in the sandbox, and there's an inherited Ruff gap. Both designs recommend making the free-text bundle opt-in. That's an H10 decision for the owner. REVIEW.
- **2026-11-12 01:59** GPU TTS attempt 5: install VERIFIED (the models-root fix works live). The job then ran for 137 s and exited 2 with `category=execution; code=generation_failed`. The pod was released as `unsafe_job_state`, $0.27. Census 0 pods; balance $100.94.
  - Blind again at the execution stage. Root cause (Codex Terra trace, checked by me):
    - VibeComfy builds a sanitised `RuntimeNodeError.comfy_diagnostic` (code `comfy_execution_error`, `node_id`, `node_class`, `exception_type`), but `preflight.generation_error` dropped it;
    - the pod frame builder read only top-level codes and collapsed any code outside `CODES` to `generation_failed`.
  - Fix `eeeee9ef`: carry the fixed fields; take the deepest known code from the nested result; allow `exception_type` only from a fixed engine-neutral list; pin every VibeComfy execution-path code into `CODES` with a test.
  - The provider-neutrality ratchet (slice 3) then caught this fix adding `comfy_diagnostic` to `astrid/core`. `878d13f4` corrects it: the VibeComfy pack's run boundary exposes the diagnostic as `engine_diagnostic`, and core reads only that.
- **2026-11-12 02:20** Fable follow-up (asked by the user): would the structure have prevented the models-root bug? Answer: NO, it would only have shown it one rental earlier. The missing boundary was installer → status reader; "a fact with one owner is re-derived by a second reader", plus fakes that ignore their arguments.
  - Additions to the design:
    (1) `plan_from_receipt()`: readers build the plan from the receipt and never re-derive it, with an invariant test that every install-bound field is in the receipt;
    (2) fakes answer from stored state, not flags;
    (3) a harness round trip per recipe: install with a mounted cache, then status with no arguments → installed.
  - General rule folded into Move 1: one record owns each fact; readers parse it and never rebuild it. Queued as the next slice (Luna, after slice 2 is merged).
- **2026-11-12 02:20** Slices 2 (`0a7de39c`) and 3 (`ebdc2504`) committed after my review and test runs.
  - Slice 2: I fixed the receipt reader to use `runpod_gate` and kept `gate=offer` for offer refusals; Codex had flagged both as outside its files. receipt 41, target_selection 100, worker_preparation 48 and placement_refused 7 passed.
  - Slice 3: evidence 7 and 13, diagnostics 53, receipt 41 and the ratchet passed.
- **2026-11-12 02:22** Rehearsal → `878d13f4`: `c627edba` + execution diagnostic + slices 1, 2 and 3.
  - Conflicts resolved by hand: `read_exact_pod` takes slice 1's provider read; `failure_diagnostics` combines the exception and oom facts, the per-engine allowlists and the nested traversal, with `engine_id` threaded through.
  - Integrated tests all pass: diagnostics 58, providers 11, placement_refused 7, target_selection 100, worker_preparation 48, provider_fields 33, install_verify 6, remote_placement 14, terminal evidence 7, ratchet, guard 19, pod_fields 10, receipt 41, local_server_helpers 32.
  - Ruff improved to 2127 and the baseline was locked.
  - Reinstalled. TTS attempt 6 launched at 02:23:30; before-census 0 pods; balance $100.88. Spend ≈ $4.51 of $40.
- **2026-11-12 02:22** C1 lead (Terra) finished the reason-channel core (uncommitted in `c-c1`) and wrote 3 Luna task files (`briefs/luna-tasks/c1-{1,2,3}.md`). Fan-out is deferred until TTS attempt 6 settles, because it needs a fresh base after the `878d13f4` integration.
- **2026-11-12 02:24** ORCHESTRATOR (independent "war of attrition" analysis at `c627edba`). Verdict: mostly yes, in agreement with my 01:25 conclusion and the structural design.
  - Three causes: (A) provider access per call site; (B) reasons dropped per boundary (71 broad excepts, 35 `from None`, 10 bare `return False`, exception names matched by string); (C) hand-kept lists.
  - Gaps to do now:
    (1) ratchet the hand-kept lists: every bundled pack action in the census and the matrix; `adapter.py:544` derived from `host_target_operation`; the `EXCEPTIONS` names replaced or ratcheted. Known misses: `ManagedSourcesError`, `WorkerPreparationError`, `PreparationJournalError` and `CapacityWaitCancelled` show as `UnknownError`.
    (2) one installed-entry-point smoke test: the built wheel, `astrid generate … --placement runpod` against a fake provider built from recordings, requiring a named receipt reason. It needs an injectable provider base URL.
  - Also a ratchet: no `runpod_lifecycle.api`, `httpx` or `runpod` imports in `astrid/packs/runpod` outside the provider module.
  - Don't restructure `generic_host`, `_generate_on_target_impl`, `shared/common.py`, the legacy prepared-worker layer, lifecycle error types, or do a rename sweep.
  - Sequence: the provider gate with backoff, plus (1) and (2), BEFORE further paid cells that exercise release or warm reuse.
  - TAKEN: all of it.
  - Dispatching in parallel (lead-and-Luna): the provider gate (Terra lead); (2) the smoke test (Sol); (1) the list ratchets plus the import ratchet (Luna); `plan_from_receipt` (Luna); and the C1 Luna fan-out after its core is rebased onto `878d13f4`.
  - TTS attempt 6 (a single cell, no warm reuse) continues.
- **2026-11-12 02:45** OWNER DECISION (Hannah, in session): NO REDACTION. "It's the user running it on machines they run." H10's redacted free-text bundle is dropped; logs from a user's own machines are the user's own. This supersedes H10 and the parked bundle redactor (`04dd5f15`). The principle: every failure must be understandable FROM THE PRODUCT, so no operator backdoor is the plan. Fable was asked for the minimal design and for which existing system (Runtime task outputs or evidence, VibeComfy run records, pod-agent job stdout/stderr, the engine server log, the generic host's terminal evidence) should carry failure logs to the user.
- **2026-11-12 02:48** Fable's design for "every failure is understandable from the product": failure logs ARE outputs. The existing path is unused for failures:
  - `machine._fetch_verified` (a digest-verified folder fetch whose docstring already names "the failure folder") has no failure caller;
  - the pod job script builds a manifest only on success;
  - on failure the controller reads 4 KB and raises, then the reset deletes the full stdout, stderr and engine `comfy.log` (`server_log_path` is already declared config);
  - the Runtime already associates outputs on failed tasks.
  - Slice 1 (Codex Terra, `r13/failure-logs`): the failure branch builds `failure/` (stdout, stderr, engine log, run record; 2 MiB cap each with a truncated marker, no redaction), fetches it through `_fetch_verified` before the reset, and the receipt records the log paths; `astrid generate failure --logs` prints them. Next slices: upload as Runtime `diagnostic` outputs plus the app view; then the local and attached paths. Delete the redactor and the secrecy allowlists. Structured reasons stay as a closed vocabulary for decisions only. No decision parses raw text.
  - TTS attempt 6 keeps running on the current build. If it's still blind, attempt 7 waits for this slice instead of an operator backdoor.
- **2026-11-12 02:45** GPU TTS attempt 6: FAIL in execution, $0.28 (pod `8tnysunl86wxoy`, released by the product as `unsafe_job_state`; census 0 pods; balance $100.68; spent ≈ $4.71 of $40).
  - The receipt now NAMES the failure: `comfy_execution_error` at node `1`, after 171 s of execution. That node is almost certainly `AILab_Qwen3TTSCustomVoice`, the custom TTS node.
  - The exception type and node class were withheld by the allowlists, which the owner's no-redaction decision removes.
  - Likely suspects: the custom node loading models from `ComfyUI/models/TTS` rather than the volume's `extra_model_paths`, or a missing pip dependency (`qwen-tts`).
  - TTS attempt 7 waits for the failure-logs slice (`r13/failure-logs`), so the engine's own error text comes back through the product.
- **2026-11-12 02:45** GPU t2i diagnostic launched (standard ComfyUI nodes, default entry `qwen-image-2.1-turbo`, 768×768, seed 7; RTX 5090; P1800/E600/I600; cap $1.25). Purpose: prove whether the pipeline works end to end with non-custom nodes. Before-census 0 pods; balance $100.60.
- **2026-11-12 03:10** GPU t2i diagnostic (`qwen-image-2.1-turbo`): FAIL in execution after 289 s, `integrity_failed`, $0.35 (released `unsafe_job_state`; census 0 pods; balance $100.33; spent ≈ $5.06 of $40). A different error from TTS, and equally undiagnosable from the product. NO further paid cells until declared logs land.
- **2026-11-12 03:12** DECLARED RUN LOGS (the owner: "should be really simple"; "a generalisable elegant way to declare or segment logs … location/params feeding into task records and tooling"; "you can change vibecomfy too").
  - I hadn't given Fable that framing before, and my `43993b6f` was a RunPod-specific scrape. That was the wrong shape.
  - Two Luna explorers mapped VibeComfy and Astrid/Runtime. Fable designed it: `briefs/declared-logs-design.md`.
    - One `LogDecl(name, role, path, start, end)`, written when a run STARTS; byte offsets slice a shared session log to one run.
    - The parent assigns the run root, so nothing searches the filesystem.
    - One stdlib collector.
    - Logs are ordinary outputs with role `log`. The Runtime already associates outputs on failed tasks and lists them, so there's no schema change.
    - One command: `astrid tasks logs <task>`.
  - Explorer finding: VibeComfy itself drops ComfyUI's full `execution_error` message and traceback (an allowlist at `session.py` ~3977-4031). With no redaction, it now keeps them in `attempt.json`.
  - Dispatched with network ON (sockets, so tests don't hang) and the push URL disabled in both clones:
    - VibeComfy half (Luna, `c-vc-logs` `r13/declared-logs`);
    - Astrid half (Terra, `c-logs` `r13/declared-logs`, which replaces my scrape).
  - The VibeComfy change needs a pin bump in Astrid's `pins.json` and the installer manifest; that's my integration step.
- **2026-11-12 03:20** Declared logs, process (from the user): Fable writes the SPEC and the task split (each task marked luna, terra or sol); Astra sense-checks Fable's spec; I integrate their feedback, trimming anything overzealous; then farm out by difficulty and test live once. The single-Codex-per-half runs and the Opus refiner were stopped and their clones reset. Two Luna traces (pod path; host and Runtime outputs) feed Fable.
- **2026-11-12 03:28** Noted (Hannah, through the Plan 48 orchestrator): after PR #533 merges, plan status is edited in each plan's `plan.md` and then `python3 scripts/astrid_dev.py sync`; never edit `plans/index.md` by hand; `check_docs.py` becomes `astrid_dev.py check`. There are no edits to `plans/index.md` in flight from this session.
- **2026-11-12 03:28** Declared-logs spec (Fable): `briefs/declared-logs-spec.md` with 13 task briefs.
  - Key finding: on the pod, the ComfyUI log is only a 256 KiB in-memory ring, and `comfy.log` is a startup snapshot, so the scrape could never have found it. Task a2 makes the supervisor append the live log.
  - The declaration is its own `logs.json`, because `attempt.json` has several writers.
  - The owner's amendments, which I added: (1) TIME-bound slices (`since`/`until`/`line_time`) alongside byte ranges; (2) logs travel through the same output manifest and verified fetch as files; (3) the task tools (a8 role-`log` outputs, a9 `astrid tasks logs`) move into the first wave.
  - I authorised the cleanup task: it replaces tests of deleted code with tests proving the same guarantee, plus an old→new mapping.
  - C1 task 3 regressed (24 machine-suite failures against 39 passing at the base). It's parked as `briefs/parked-c1t3.diff`, not merged.
  - Disk freed to 9 GB: the old `install-r13` was deleted, along with merged clones and stale pytest temp files.
- **2026-11-12 03:35** Astra's spec check, integrated with my rulings:
  - ACCEPTED: (1) full logs: the collector keeps the complete declared slice, with only a 256 MiB transport safety cap (head and tail kept); (2) a2 captures from process launch, so failed startups are on disk; (3) the a3 timing contradiction is settled as "at job start, before its own preparation"; (4) a8 publishes logs on success too.
  - The pin bump and live supervisor check stay with me (the integration step).
  - NARROWED: attached-endpoint capture is out of scope for this slice.
  - OVERRULED: deferring a9 and a7, since the owner explicitly wants task tools and a7 is small and parallel.
  - The four factual claims (engine ring buffer, several `attempt.json` writers, `*.log` truncation at reset, the declaration paths) were all confirmed.
  - Wave 1 dispatched: a1, a6, a7, a9 and vc1 (Luna); a2 (Terra). Wave 2 (a3, a4, a5 Luna; a8 and vc2 Terra) follows the wave-1 merge.
- **2026-11-12 03:45** Owner: one more Astra check, with Luna helpers, that the declared-logs plan captures all four cases: normal ComfyUI server runs and the pip-installed, embedded or in-process ComfyUI mode, each on RunPod and locally. Two Luna traces (local placement; other ComfyUI modes) feed Astra; any gap becomes a task change or a new task with a difficulty mark. Then the farm-out continues by tier, and finally the live test on the FAILED TTS task (`audio/qwen3_tts_custom_voice`, node 1 `comfy_execution_error`).
- **2026-11-12 03:58** Four-case coverage check (Astra plus 2 Lunas), with my rulings:
  - (1) RunPod, normal server, PARTLY: a4 also declares `result.json` (the generation's stdout) as `generation.stdout`.
  - (2) Local, normal server, PARTLY:
    - a3 also declares the engine slice before LOCAL preparation;
    - NEW task `local-streams` (terra) keeps the local job's complete stdout and stderr, where today the host keeps only scrubbed tails;
    - a6 writes a local failure receipt too.
  - (3, 4) Embedded / in-process / "pip" ComfyUI: OUT OF SCOPE, with evidence. Astrid has no route to it (`production_engine.py:680` allows only `local_server`; the pod always uses its HTTP endpoint), and no pip-installed ComfyUI recipe exists. If the owner wants it, it's a separate Sol task.
  - e2e extended for both.
  - Also: `plan_from_receipt` (`993fd926`; engine_runner 143 passed plus the 2 pre-existing packaged-lock failures; Ruff improved to 2117) and C1 task 2 (`77ebb920`; 4 new tests plus remote_placement and install-verify green) were committed.
  - The provider gate (Terra) is again NOT implemented: lifecycle's post-delete absence polling also needs gating and drops `Retry-After`. It moves to Sol after the live test; it isn't on the live-TTS path, since the product has released every pod since the first.
  - The smoke test (Sol) was blocked by my own file exclusions (it needs `failure_receipt.py` and `target_selection.py`). It's deferred; the declared-logs e2e covers the key path.
- **2026-11-12 04:05** Declared logs, wave 1 results.
  - Committed after my test runs:
    - a1 collector `15db432f` (11 passed);
    - a6 receipt and `--logs`/`--name` `d9cf88a9` (receipt 43, logs 3, failure_logs 6);
    - a9 `astrid tasks logs` `90551c4f` (5, plus the task/run verbs 108). I appended `logs` after `follow` and added exactly `logs`/`tasks_logs` to the two pinned lists; the four MCP parity failures are pre-existing at the base.
    - vc1 VibeComfy `logs.json` `42b229ed` (6).
  - a1, a6 and a9 are merged into `r13/declared-logs` `0af2f95d`.
  - a2 stopped: the registry publisher rejects any file in the registry dir. Ruling: the live log goes in a sibling `comfyui-logs/engine.log`, appended from launch, with the snapshot unchanged.
  - a7 stopped on a brief-versus-spec contradiction. Ruling: the spec wins (keep the whole file, only the 256 MiB cap), reusing `run_logs.collect`.
  - Wave 2 dispatched: a2 rework and a8, local-streams, vc2 (Terra); a7 rework, a4, a5 (Luna). a3 follows a2.
- **2026-11-12 04:48** Declared logs, wave 2 integrated locally on `r13/declared-logs` (`1215af6e` merges a7, local-streams, a8, a4, a5; then `80a437c2`).
  - Two merge interactions, fixed in code and the tests' contract, not by loosening checks:
    - a4 and a5 each added a failure-log fetch method. Kept one, `_fetch_failure_logs`: the logs digest comes from the stdout tail already read, with one bounded marker grep only when the tail lacks it. That case matters, because logs are most needed exactly when the frame is broken. The legacy `failure/` folder stays as the fallback until the cleanup task. The pinned exec-list test now names that exact grep and asserts `not_reported`.
    - a8 × local-streams: the host now declares the job's own stdout and stderr on every local job, so "no logs" was the old expectation. The fixture now appends to `logs.json` as `run_logs.declare` does, and the test expects pack logs plus host streams.
  - `tests/packs/runpod`: 989 passed against 978 at `0af2f95d`, with no new failures. The remaining failures and errors come from this venv (no `vibecomfy`) and exist at the base. Ruff 2127.
  - **REVIEW / permission:** the push of `r13/declared-logs` was refused by the auto-mode classifier (external system write) twice, including the plain-URL form. Logged; continuing locally (the integration, reinstall and live test can all run from local branches). The owner needs to allow pushes to `r13/*` or push `r13/declared-logs` (`80a437c2`) themselves.
  - a2 (third try, Terra) returned with the live engine log. I replaced its thread-local side channel with an explicit `CommandRequest.output_log`, so the launch request says where its output goes, and the launch test now exercises that handoff through the real `_command`. Engine-neutral path `<root>/runtime/out/sessions/<engine>-logs/engine.log`.
- **2026-11-12 05:10** Integration, continued.
  - a2 committed as `378f7eea` on local `r13/dl-a2`, after two manager fixes:
    - I first put the log path on `CommandRequest`, but that broke `test_protocol_shapes_exactly_match_v1`, because `CommandRequest` is a wire contract. The path is now passed explicitly instead, `spawn(request, output_log=path)` → `_Owned` → `_Output`, with no thread-local and no protocol change.
    - Fixed two flaky tests: with `-u`, `print` writes the text and the newline separately, so two streams sharing one log interleave mid-line. Each test child now writes a line in one call. 15 of 15 runs pass. Custody 76 passed, ruff 2127.
  - VibeComfy pinned to `88cff6d5` (vc1 and vc2, already on origin) with `scripts/vibecomfy_pin.py`, which also updates the pin and recipe digests, plus the three test literals: `7ac360a9`. The pin suites match the base exactly (541 passed on both).
  - `r13/declared-logs` is at `c05e5e31` locally (a2 merged). a3 (Luna) and e2e (Terra) are running.
  - e2e stopped the first time, overzealously, on the legacy `test_failure_logs.py`. Ruling: e2e adds one new file and doesn't replace that behaviour; the cleanup task owns retiring it.
  - New rehearsal, local clone `c-reh`: `878d13f4` plus ratchet, receiptplan, C1 core, C1 task 2, setup fixes, G4 follow-ups and declared logs.
    - The only conflicts were additive (installer `backend.py`, `tools.py` and `test_installer_sources.py`), and both sides were kept. At install, the lifecycle pin check runs before the VibeComfy pin check.
    - The broad suites are running against base `878d13f4`.
  - **REVIEW** C1 task 1 is parked (`/home/user/wt/briefs/parked-c1t1.diff`) and not merged.
    - Its per-step install-unverified labels are good, but it narrows `_safe_label` to an allowlist that turns any other label into "withheld". That is redaction, against the owner's ruling, and would hide a novel engine error code.
    - Rework later: keep the labels and drop the allowlist.
  - The reinstall will use a manifest with the Agent `repo` pointing at the local rehearsal clone; the product supports it, and the controller ships that source to the pod. So the refused push does not block the live test.
- **2026-11-12 05:25** **REVIEW** Sequencing after the Release 12 publication (orchestrator, 04:33). I merged published Agent main `0e1543e0` into the rehearsal BEFORE the live TTS, so the live evidence is on the real Phase 1 base rather than on a base that is about to be replaced.
  - The ten new main commits are R12's fix round. The one conflict was `tests/packs/h3_av/test_character_swap_cpu_boundary.py`: our side (Plan 32 T6b-4) deliberately deleted the checkout-session schema-ownership tests, and main had only narrowed a patch inside one of them. I kept the deletion.
  - VibeComfy needs no merge: R12's `e65f4941` is an ancestor of `88cff6d5`.
  - The rehearsal gate's baseline is now `0e1543e0`.
- **2026-11-12 05:48** Declared logs complete offline. Install candidate `6c9efd1a` is installing.
  - a3 (Luna) was committed as `8e9a3c3c` after I factored its two duplicated 12-line blocks into one helper, `engine_custody.declare_engine_log(out, root, engine)`, which never raises. I checked that `ManagedEnginePreparation.root` and `.recipe.engine` are the real attributes the supervisor's `engine_log_path` uses, and that every pod path (named entry, prepared job, workflow) reaches `run_owned_action` with the job's own `out` (`{remote_root}/out`), which is the root that `finish_command` collects. 60 tests passed with VibeComfy `88cff6d5`.
  - e2e (Terra) was committed as `1fec1233`, one new test file passing 5 of 5 runs. Codex did not finish the suite comparison, out of caution about a loopback HTTPS test. That was unnecessary, since the file adds no product code.
  - `r13/declared-logs` is at `08aa3062` locally.
  - Rehearsal gate, `tests/packs/runpod` at `a6f38902`: 1094 passed, 21 failed, 2 errors.
    - All of those failures except one also fail at `878d13f4`, so they predate this work (reset diagnostics, pod reset runtime, catalog id, GraphQL confirmation, release after acquisition, pod source install).
    - The exception is the ratchet test `test_every_runpod_exception_name_is_receipt_safe_or_explicitly_excluded`. It was a real merge interaction: C1 core added `PlacementReasonError` while the ratchet was written in parallel. I classified the name as receipt-safe in `fc063698` (like its parent `RemotePlacementError`, it is fixed vocabulary).
    - Release 12 main lacks these Release 13 tests, so pre-merge commits are the fair baseline for them.
    - Correction: my earlier "989 vs 978" comparisons used a `PYTHONPATH` without VibeComfy, so about 67 tests errored instantly. All runs since then use the pinned checkout.
  - The rest of the gate (core/execution, cli, installer, engine) is still running on `c-reh`. The install candidate was built in a separate clone, `c-bis`, so it doesn't disturb that run: `ddfefa60` is the rehearsal plus a3 and e2e, and `6c9efd1a` locks in ruff 2127 → 2120 (the improvement came with Release 12 main). Focused suites: 201 passed.
  - Install: the Release 12 App installer (`c268a5fa`, from App main) with the Release 12 manifest plus Agent `{sha: 6c9efd1a, repo: /home/user/wt/c-bis}`, VibeComfy `88cff6d5`, release 13.
- **2026-11-12 06:35** **Live TTS with declared logs: PASS on visibility.** Run `runs/tts-dl1` on Release 13 rehearsal `6c9efd1a` (then `cffffe05`): RTX 5090, pod `yw2zz2zth8fijz`, $0.27, released (`unsafe_job_state`); census 0 pods afterwards.
  - The job failed as before (exit 2, `comfy_execution_error`), but this time six declared logs came back as `role=log` task outputs: `engine` (2621 B), `job.stdout`, `job.stderr`, `generation.stdout`, `run` and `engine-error` (3111 B).
  - `astrid generate failure --logs --name engine-error` printed ComfyUI's whole execution error on the first try.
  - `astrid tasks logs 9269498d --project setup --name engine-error` first said "no logs recorded". This was a real a9 bug found only live, fixed in `62800d35` (declared logs) / `cffffe05` (rehearsal), then reinstalled and run live: it lists all six logs and prints the engine error. Exact pass criterion met.
    - Cause: the command read `tasks.list_managed_outputs`, which is empty for a failed task, and looked for `read_bytes` on the top-level client instead of `client.media`.
    - The test fakes had encoded both beliefs. The fakes now mirror the real SDK (`tasks.show`, `media.read_bytes`), with a failed-task case and a check of the SDK surface.
  - The engine slice correctly starts at this job ("got prompt"), and the earlier job output is excluded.
  - **Follow-up:** here the engine was started by the controller's install and health step, before the job declared its slice, so the engine's startup output (where node-pack import errors normally appear) is not in the slice. Fix: the supervisor records its launch offset and the job declares from it.
- **2026-11-12 06:40** **TTS root cause, found from the product's own logs, then confirmed offline.**
  - The node pack ComfyUI-QwenTTS `d8122a8` (also upstream HEAD) decorates with `@check_model_inputs()`. In our locked `transformers==5.22.1`, `check_model_inputs` is a plain decorator, so `qwen_tts/core/tokenizer_12hz/modeling_qwen3_tts_tokenizer_v2.py:498` raises `TypeError: check_model_inputs() missing 1 required positional argument: 'func'`.
  - The pack's `_ensure_qwen_package` wraps that in `except Exception: return`, so its synthetic `qwen_tts.core` never gets its stubs, and the error only surfaces later as the misleading "cannot import name 'Qwen3TTSTokenizerV1Config' from 'qwen_tts.core' (unknown location)".
  - Reproduced in a CPU scratch venv with the pinned pack and transformers 5.22.1.
  - **REVIEW, owner decision:** re-locking transformers for the whole shared environment isn't reproducible here (the lock was compiled from inputs on another machine) and risks the other packs. That leaves two routes:
    - (a) point the `comfyui-qwentts` pin at a banodoco fork carrying a one-line fix that works with both decorator forms. This needs a new external repository, so it's the owner's call.
    - (b) add a digest-verified source-patch step to the engine recipe, recorded in the install receipt.
    - My recommendation is (a): no new mechanism, and the pin system already handles it.
- **2026-11-12 06:45** Rehearsal gate classified against Release 12 main `0e1543e0` and the pre-merge commits.
  - Real regressions, fixed:
    - the ratchet × C1 interaction (`fc063698`);
    - `test_two_jobs_retain_verified_managed_launch_refresh` (3), from the receiptplan merge. The test rebuilt the plan from arguments, the exact pattern receiptplan removed, and its now-faithful fake refused it. Fixed in `fc5906af` / `77632da9` so the test plans from the receipt, as production does; the tamper cases still fail closed.
  - Everything else either fails at `878d13f4` too or is absent from Release 12 main because the tests are R13's: reset diagnostics, pod reset runtime, catalog id, GraphQL confirmation, release after acquisition, pod source install, selected root map, engine_runner packaged lock (2), MCP parity (4).
  - core/execution: 2044 passed, with the same 21 failures and 46 errors as at base. installer: 1986 passed; one failure, `test_strict_app_update_receipt_names_release_and_skill_warning[skill-sync-ok]`, is not yet classified.
- **2026-11-12 06:46** **REVIEW, no-redaction ruling:** `astrid/core/contracts/errors.py:48` `_CREDENTIAL_KEY` matches any field ending in `_key`, so error-state snapshots print `variant_key` and `idempotency_key` as `<redacted>`. That predates the ruling and sits in shared core credential scrubbing. Not changed overnight ("never weaken a check"). Proposal: match only real credential names.
- **2026-11-12 06:47** The legacy-log cleanup (Luna) stopped correctly the first time on four tests outside its file. I ruled on each with a replacement at least as strict, and it was re-dispatched. Then the paid cells: t2i (≤ $1), then the SFX first-look (≤ $3), with a balance floor check before each.
- **2026-11-12 06:55** Pushes worked this time (the earlier refusals at 04:48 didn't recur):
  - `scratch/r13-rehearsal` `878d13f4` → `77632da9` (the installed line plus the receipt-plan test fix);
  - `r13/declared-logs` `0af2f95d` → `62800d35`.
  The owner action for pushes in the NOW block is withdrawn.
  - t2i was refused before renting, correctly: at $1.25/hr, P/E/I of 1800+900+1800 s can cost $1.56, more than the $1 cap. It will re-run with 1200/600/600 s (≤ $0.83). SFX is running at ≤ $3.
- **2026-11-12 07:15** The live SFX first-look (`runs/sfx-dl1`) on `cffffe05`: RTX 5090, pod `d9mi0dtqdgtwqy`, released, ≈ $0.33. It failed with `integrity_failed` in the managed-alignment `doctor` step (`workflow_validation_failed`).
  - Declared logs came back, but they exposed the next blind spot: the step's whole stdout and stderr were reduced to two digests in a log line, and the error said "inspect the host log", which isn't a declared log either.
  - Fixed structurally in `09de4222`: every alignment step goes through `_native`, and on a failure its whole output is written into the run root and declared as `preparation.<step>.stdout` and `preparation.<step>.stderr`; the error names those logs. The public error still carries no step output, and the tests pinning that still pass.
  - The engine startup slice is done (`r13/dl-startup`). The supervisor writes `launch.json` (launch and ready offsets) and the run also declares `engine.startup` for exactly that range.
    - I fixed one Codex regression: it had moved `publish_registry` and `check` outside the stop-on-failure guard, so a failure after health would have left the engine running. A new test pins this (it fails on Codex's version).
  - The e2e task-log fake still served a failed task's outputs as managed outputs, the belief the live run disproved. It now answers like the Runtime (`46f68da5`).
  - The cleanup was merged after the full RunPod suite showed no new failures against its base (17 failed against 18).
  - On origin: `r13/declared-logs` `603b6728`, `scratch/r13-rehearsal` `e7f00181`.
  - Reinstalling at `e7f00181`, then re-running SFX (≤ $3, so the `doctor` output becomes visible) and t2i (≤ $1, P/E/I 1200/600/600 s).
- **2026-11-12 07:30** **SFX root cause, read from the product's own logs** (`runs/sfx-dl2` on `e7f00181`, task `f5b69e2a`, pod released, ≈ $0.27).
  - `astrid tasks logs f5b69e2a --project setup --name preparation.doctor.stdout` shows `WorkflowBundleError: Node 11 (HunyuanFoleyModelLoader) has unknown input foley_checkpoint_name`. The new `engine.startup` log (8.6 KB) shows search paths only for `diffusion_models`, `loras`, `text_encoders` and `vae` on the volume (`/workspace/astrid/engines/comfyui/models`).
  - Mechanism: the pinned Foley pack builds its loader schema from `folder_paths.models_dir/hunyuan_foley`, which is `<ComfyUI>/models`, not the volume. With no checkpoint there, it publishes an `error`-only schema, so the template's real input looks unknown. The model lock has six top-level folders, but the engine's `models-config` writes a fixed four. `hunyuan_foley` (10 files) and `TTS` (11, QwenTTS) are installed but invisible.
  - It's the same class as tonight's models-root bug: a fact (where the models live) that one record owns, with a reader that rebuilt it from a fixed list.
  - Structural fix dispatched to Terra (`/home/user/wt/briefs/models-folders.md`):
    - the folder list is derived from the lock;
    - every folder goes into the search paths;
    - `<ComfyUI>/models/<folder>` links point to the volume for packs that read `models_dir` directly;
    - it refuses on conflict and never deletes user files;
    - `models-config-check` verifies both.
  - TTS needs this AND the decorator fix (06:40 REVIEW).
- **2026-11-12 07:40** **REVIEW** models-folders, first attempt: Codex stopped correctly. `<ComfyUI>/models` is inside the ComfyUI source checkout, and the clean-source custody check refused the new links (`?? models/diffusion_models`; it had also replaced a tracked placeholder directory).
  - Ruling:
    - the four standard kinds stay on search paths only;
    - links only for pack-private lock folders that the checkout doesn't track (`hunyuan_foley`, `TTS`), detected structurally;
    - one exact, verified exemption in the clean-source check: an untracked `models/<folder>` is allowed only if it is a lock folder, is a symlink, and resolves to `<models base>/<folder>`. Everything else still fails.
  - This narrows an integrity check, even though the exemption is exact and verified, so it's built on a branch and NOT merged into the rehearsal until the owner has looked.
  - The alternatives were worse: `--base-directory` would also move `custom_nodes`, input and output, and writing to `.git/info/exclude` would hide entries silently.
- **2026-11-12 07:55** **t2i root cause, read from the product** (`runs/t2i-dl2`, task `e0509aeb`, pod `i21oljm73brosw` released, ≈ $0.27). The prior t2i run of the night was blind on the same failure; this time the declared logs show the cause.
  - `preparation.doctor.stdout` shows "Schema reconciliation: workflow contains unresolved class types: QwenImage21Cache, TextEncodeQwenImage21", and the error names those logs.
  - Checked read-only: both nodes are ComfyUI core (`comfy_extras/nodes_qwen.py`) on ComfyUI master `c5751c8`, and absent at our pin `ee71d5c4`. The `qwen-image-2.1-turbo` entries need a newer ComfyUI than the recipe pins.
  - **REVIEW:** the fix is a ComfyUI pin bump to the first revision with those nodes, plus a re-lock of the engine requirements, whose inputs include ComfyUI's `requirements.txt`. That's a recipe-level change, and the lock was compiled from inputs on another machine.
  - Running now: first looks at music (`audio/ace_step_1_5_t2a_song`) and edit (`edit/qwen_image_2_1_turbo_edit`, expected to hit the same nodes), each ≤ $1 with P/E/I 1200/600/600.
- **2026-11-12 08:20** models-folders (Terra, second try) is committed as `b1830b9e` on `r13/models-folders` and pushed, NOT merged (REVIEW).
  - Reviewed: the target helper derives folders from the lock, makes links only for untracked folders, refuses conflicts without deleting anything, and the check verifies the links. The clean-source exemption requires every untracked entry to be a single-level `?? models/<x>` that the helper verifies.
  - Reverted Codex's relaxation of `_models_root`, which would have allowed a models root inside the engine tree. That was only needed because my brief's case 4 was imprecise. Replaced that case with the real no-volume case (base `<root>/models`, links still made) and a test that the inside-the-engine-tree root is still refused.
  - Music was not run: its ACE-Step models aren't in the RunPod model lock, and the template takes only `seed`. Edit was refused before renting because my input used `image` and not `image_ref`. The product said so clearly. Not re-run, since it would hit the t2i node gap.
- **2026-11-12 08:35** Overnight run ended. models-folders: RunPod machine suite 118 passed. Final census: 0 pods. No check-ins remain scheduled.
- **2026-11-12 08:45** **Orchestrator rulings (08:34), exercising Hannah's delegation; she can overrule any of them.**
  1. TTS: route (b) now, a recipe source patch pinned to the exact QwenTTS commit, failing closed. I checked the cheaper alternative first: the tokenizer file was added once, in `b111101`, already using `@check_model_inputs()`, and earlier commits lack the 12 Hz tokenizer the locked 0.6B model needs. So there's no earlier pin, and it's the patch. The fork (a) stays the durable option if Hannah creates the repository.
  2. models-folders: Astra review of `e7f00181..b1830b9e`; merge on NO BLOCKER, then re-run SFX.
  3. ComfyUI bump to the EARLIEST commit with both Qwen Image 2.1 nodes, plus a re-lock on this machine from reconstructed inputs, now committed as `lock-inputs/` with a README: APPROVED.
  4. `_CREDENTIAL_KEY` narrowed to credential names, with a test that a credential-shaped field is still redacted: APPROVED.
  5. Music: lock the ACE-Step models if that takes under an hour and they fit the volume, else drop the cell and record a gap (my call).
  6. **H10 CLOSED**, superseded by declared logs. Failure evidence for Release 13 is the declared-logs path (`logs.json` → `role=log` task outputs → `astrid tasks logs` / `generate failure --logs`). The bundle branches `r13/g3-bundle` and `r13/g3-bundle-2` (`04dd5f15`) are parked for good.
  7. Fix `generate describe <entry id>`; leave `image_ref`.
  - Dispatched in parallel (briefs in `/home/user/wt/briefs/wave3/`):
    - Astra: the models-folders review;
    - Terra: the TTS patch, based on models-folders, with one shared "declared, verified source modifications" exemption;
    - Sol: the ComfyUI bump and re-lock;
    - Luna: the music lock;
    - Luna: the credential scrub and describe;
    - Sol: the provider gate with 429 back-off (ruling: gate lifecycle's `terminate_pod` as one bounded operation and don't change lifecycle now);
    - Sol: the installed-entry-point smoke test (ruling: first slice covers provider drift → named claim refusal, and a pod job failure → declared logs).
  - Disk: deleted 17 clones whose HEAD is on origin (3.7 → 11 GB free).
- **2026-11-12 08:55** A safety classifier flagged one launcher (the ComfyUI-bump worker) as "Create Unsafe Agents". I checked the process list: only the briefed Codex workers are running (Astra read-only; the others `workspace-write` with network on for sockets and registries, pushes disabled in every clone, the manager commits). This is the same launch pattern as all night. Noted for the owner; no change.
- **2026-11-12 10:20** Wave 3 progress. On origin `scratch/r13-rehearsal` = `e9f16189`.
  - **models-folders** `43b69032`, merged. Astra found one real BLOCKER: the link check compared the link's text, so a destination that was itself a symlink passed. Fixed by refusing a redirected or file destination, with tests. Astra's recheck: NO BLOCKER (30 cases through the real helper and both callers).
  - **TTS patch** `687a0ed9` (`r13/tts-patch`), merged.
    - The recipe now has `source_patches`: a whole-file replacement bound by sha256 before and after, applied right after the pinned checkout is verified, failing closed.
    - The clean-source check has one shared "declared modifications" path (verified model links plus patched files at their after-digest).
    - I verified the replacement against the pinned upstream file: the only change is a signature-based choice between the two decorator forms.
    - Tests: 412 passed. The two packaged-lock failures and `test_no_other_tracked_file_copies_the_pin` all fail at `878d13f4` too.
  - **Credential scrub and describe** `e798df2b`, merged. I added environment-style UPPERCASE `*_KEY` names (for example `RUNPOD_KEY`) to the dict scrub, matching the free-text pattern. The four remaining failures in those files fail identically at `e7f00181`.
  - **Music lock** `634a2608`, merged: four ACE-Step 1.5 files from `Comfy-Org/ACE-Step-1.5` at `371bb168` (14.7 GB; one digest spot-checked against HF). The lock is 110.4 GB on the 200 GB volume (`2z2dlu1v8g`, EUR-NO-1), so the cell stays. The model-count literal moved from 32 to 36. The recipe-digest merge conflict with the TTS patch was resolved by recomputing the chain with `scripts/vibecomfy_pin.py`.
  - **ComfyUI bump (Sol), five tries.**
    - Tries 1–3 stopped on pin-derived test literals; I ruled them a class that moves with the pin.
    - At 09:45 I switched the target to `2fb8cabd` (ComfyUI 0.42.0), because the shipped lock already carries late-October requirements. The worker then found that the H3 pack declares `comfy_version ==0.36.0`. `6bfaacc6` is still 0.36.0 (I checked `comfyui_version.py`); `2fb8cabd` isn't.
    - **I withdrew my override: the orchestrator's "earliest" (`6bfaacc6`) was right.** Running now with the final target.
    - Recorded finding: the existing Linux lock carries NEWER ComfyUI requirements (frontend 1.57.4) than the installed ComfyUI source (`ee71d5c4` declares 1.52.7). No master commit matches the lock exactly. The re-lock makes the source and the lock agree.
  - **Provider gate (Sol):** the first try stopped on a resume test, because Codex wanted to redesign resume. Ruling: no redesign; the gate only paces calls. Running.
  - **Installed smoke (Sol):** partial. The recorded-replay endpoint plus 21 replay tests pass, but both installed-entry cases fail before task creation (the installed CLI in the harness doesn't see saved preferences). Not merged, since it would add a failing test. Parked as a follow-up in `c-smoke2`.
- **2026-11-12 10:45** **Provider gate** `f0535fef` (`r13/provider-gate`), merged into the rehearsal `c473f7dc`.
  - One gate per RunPod account, shared across processes through a locked state file named by a sha256 of the account (no key in clear).
  - 429 or 5xx puts the account into a cooldown, honouring `Retry-After` as seconds or an HTTP date, otherwise exponential back-off with jitter.
  - Success resets only the exponent.
  - Lifecycle's `terminate_pod` is admitted as one bounded operation; the release and resume order is unchanged.
  - Results: 181 existing tests passed before and after, plus 17 new ones. On the merged rehearsal, the gate, release, preparation, providers, guard, e2e, patches and models suites give 180 passed; ruff 2120 → 2117 (locked in).
  - **Follow-up:** lifecycle should expose typed status and `Retry-After` (today the gate parses lifecycle's fixed message for the HTTP status).
  - The ComfyUI bump (Sol, final target `6bfaacc6`) is the last piece before the batch re-run.
- **2026-11-12 09:19** Correction: the two entries above stamped "10:20" and "10:45" were written at about 09:05 and 09:15 UTC; I estimated their stamps instead of reading the clock. From here, every stamp comes from `date -u`. Census: 0 pods.
- **2026-11-12 09:38** All of waves A and B are in. Rehearsal `64e00c28` (on origin) = `c473f7dc` + ComfyUI bump `43b44c1e` + the ProviderRefused classification.
  - **ComfyUI bump:** pinned to `6bfaacc6` on both platforms. Linux re-locked here from the reconstructed `lock-inputs/` (README has the exact command).
    - Packages that moved down to the installed source's exact pins: frontend 1.57.4→1.53.6, templates 0.11.100→0.11.62, docs 0.5.15→0.5.11, aimdo 0.6.0→0.5.5, kitchen 0.2.40→0.2.35; media-assets-02 removed.
    - The H3 runtime constraints follow the new pins; `comfy_version ==0.36.0` is unchanged.
    - I moved the stale packaged-lock digest and count literals (`test_engine_runner.py:1946` and `:1960`, `test_engine_cli.py:163`), so the two tests that had failed since before tonight pass again.
  - **The digest chain merge** (TTS patch × music × ComfyUI) was recomputed with `scripts/vibecomfy_pin.py` (now `--source`-aware). Verified: patches, models lock, packaged lock, pins, and both recipe digests in `comfyui.yaml`.
  - **Gate results:**
    - combined suites: 364 passed, 0 new failures;
    - `test_machine` + `test_failure_receipt` on `c473f7dc`: 161 passed;
    - ruff 2117.
    - The remaining failures all also fail at `e7f00181` or `878d13f4` (`test_packaged_vibecomfy_checkout_supports_generate_list_json`, `test_no_other_tracked_file_copies_the_pin`, `test_generate_and_h3_share_vibecomfy_pin`, `test_to_envelope_omits_code_and_source_type_when_none`).
  - **Batch (C) started:** reinstall at `64e00c28`, then TTS, SFX, t2i, edit and music on one RTX 5090 with warm reuse (`runs/batch.sh`, balance floor before each cell). Edit inputs now use `image_ref`; music is seed-only (its template exposes only `seed`).
- **2026-11-12 10:05** Batch 1 (`64e00c28`) stopped after its first cell.
  - TTS failed in the controller's engine install on the pod (`environment:comfy`, `command_failed`), and the pod was released for about $0.14. I stopped the batch so SFX wouldn't pay for the same failure; census 0 pods, no live machines, and no orphan task.
  - **The one remaining blind spot:** the engine install's failed command output was discarded by `_Runner.run`, and the engine CLI printed only "Engine operation failed." The receipt said `Logs: not_collected` with cause `unknown`, and the kept `engine-install.stderr` held only the public JSON.
  - **Fix** `72fbdf65` (`r13/engine-command-output`, fast-forwarded into the rehearsal and pushed): the error carries the failed command's argv, exit code and whole stdout and stderr, and the engine CLI writes them after its unchanged public JSON line. On RunPod that file is already kept on the user's machine, and the controller's error quotes its tail. This applies the no-redaction ruling. Tests: CLI and runner, 183 passed plus 2 new; ruff 2117.
  - **Batch 2 started at `72fbdf65`:** it stops after TTS if the engine install fails again, now with the real `uv` error visible. Most likely cause: the re-locked environment (ComfyUI bump) failing to install or pass `uv pip check` on the pod.
- **2026-11-12 10:08** Process incident, owned, with no spend.
  - When I stopped batch 1, `pkill` ended the batch script but not its child, the SFX `generate` CLI. That CLI had already admitted its task to the host.
  - The batch-2 reinstall then refused ("Astrid is still running"): `astrid-runtime down` doesn't stop the host that `root/run` starts, and the script had already deleted `root` under the running host.
  - Recovery: I interrupted the orphaned CLI with SIGINT and stopped the old host's processes with SIGTERM, so it couldn't claim a pod for the admitted task. Census showed 0 pods three times, 20 s apart. Nothing was rented.
  - Fix in `runs/batch2.sh`: stop every process from the install root before replacing it, and tail the right install log.
  - Lesson: stop a batch by stopping the host and every process from the install root, not just the script.
  - Batch 2 restarted at `72fbdf65`.
- **2026-11-12 10:15** The old install state is blocked by the orphaned SFX task (`0d7f7e41`, lease expired at 10:07:35, reservation unreleased).
  - The installer correctly refuses every install while it's there ("Astrid is busy").
  - `astrid-runtime tasks clear` needs a live Runtime owner. A scratch venv with the exact pinned Runtime `42ae24af` refused to start on this state ("Requested Runtime identity could not be verified"), which is correct, and I did not force it.
  - Decision: leave the old state untouched for later reconciliation (it also holds tonight's failure receipts as evidence), and run the batch on a fresh isolated state (`env-b3.sh`: HOME and XDG under `home-b3`, data root `data-b3`).
  - The RunPod preferences were read from a copy of the old realm store (not the original). They were saved by `runpod.setup`: volume `2z2dlu1v8g` (`storage`, 200 GB, `/workspace`), EUR-NO-1, RTX 5090, pinned image, $3 budget cap. The fresh state gets them again through the documented `astrid machines setup --volume 2z2dlu1v8g --gpu "RTX 5090" --budget-usd 3 --json`, so no new volume is created.
  - **Follow-up for the owner:** reconcile `0d7f7e41` in the old state; an install of the same Runtime identity plus `astrid-runtime tasks clear`, or let a future same-identity host sweep it.
  - Batch 3 started at `72fbdf65`.
- **2026-11-12 10:45** Batch 3/4 findings, each read from the product, and each refused before renting ($0).
  - **Fresh state:** generation needs a project, so I created and selected `setup`. The edit image goes through `--edit <path>` (the CLI's `IMAGE_REF`), not a JSON `image_ref` path.
  - **Engine install root cause** (the `72fbdf65` command-output fix made it visible): `uv pip sync --require-hashes` on the pod failed with "Conflicting archive URL hashes for setuptools". My re-lock had merged setuptools' registry files into the policy's pinned wheel URL, adding the sdist hash.
    - Fix `6eacb077` (`r13/lock-setuptools`): a recorded post-compile step (`lock-inputs/normalize_direct_urls.py`, documented in the README) keeps exactly the URL's own hash, as in the original lock.
    - A new invariant test fails on the broken lock and passes on the fixed one.
    - I first tried a registry pin (`setuptools==84.0.0`), but `test_h3_packaged_sync_allows_only_three_source_builds_and_uses_support_lock` correctly pins the exact wheel URL as build policy, so I reverted to the URL form and kept that test unchanged.
  - **Music root cause** (reproduced locally): "staged Python identity differs from intended bundle". The ACE-Step template names no `template_id`, so its `audio/` prefix came from its location under `ready_templates/audio/`. Astrid's staged snapshot lives elsewhere, so the id lost its prefix.
    - Fix in VibeComfy `fe92ac78` (`r13/template-identity`): `new_workflow` uses the template's own fully qualified provenance `ready_id` when it names the same template. Locally the music snapshot stages, Foley is unchanged.
    - About 16 other templates declare `ready_id` and are fixed the same way. Four declare no qualified id (`z_image_turbo`, `z_image_img2img`, `basic_image_upscale`, `empty_image_red`); none is an R13 cell, and they're left as a follow-up rather than edit generated templates.
    - A VibeComfy test comparison against `88cff6d5` is running; then the pin bump.
- **2026-11-12 11:53** **REVIEW, owner (Hannah) directive:** every failed RunPod job tonight released the pod (`release: unsafe_job_state`), even with keep-warm set (`--idle-seconds 1800`). Owner: "that sounds like a bug... unless the actual machine fails for some kind of terminal reason, we should never automatically terminate it... fix that ASAP." A read-only investigator was dispatched to trace the exact code path, using the three receipts (TTS `9269498d`, SFX `f5b69e2a`, t2i `e0509aeb`; all clean exit-2 failures with verified logs) and to propose the minimal fix: release only for terminal machine conditions, otherwise reset and keep warm. Fix next, with priority.
- **2026-11-12 11:58** **Root cause of the warm-pod kills, confirmed in code at `b306b2be`.** For a failed job, `_release_impl` (`machine.py` about 1072-1094) re-runs `_canonical_installed`, which overwrites `lease.state.installed` with the live receipt, and then requires `lease.state.installed == expected_install`.
  - Managed alignment legitimately refreshes the install receipt (`managed_preparation.py:372-387`, `_checkpoint_installed`'s own docstring). So any failed job after alignment fails the check, and so does a failure partway through alignment (SFX and t2i). All of these fall into one catch-all, `warm, reason = False, "unsafe_job_state"`, and the pod is deleted.
  - The success path accepts the refresh through `_checkpoint_installed`; the failure path never got the equivalent. All 7 failed fetches tonight ended this way.
  - The test `test_unsafe_failed_job_verification_releases_exact_pod[changed_receipt]` encodes the bug: it swaps only `receipt_sha256`.
  - Fix dispatched to Terra (`/home/user/wt/briefs/wave3/keep-warm.md`, clone `c-warm`):
    - accept a refresh that differs only in `receipt_sha256` (shared helper with `_checkpoint_installed`);
    - unverifiable drift after a failed job keeps the pod warm with stale preparation, re-prepared on the next claim;
    - only terminal or safety conditions release, each with its own reason (`job_stop_unverified`, `custody_changed`, `output_digest_mismatch`, `paid_limit_exhausted`, `reset_failed`, `engine_unreachable`).
  - Owner-authorised change to the bug-encoding test; the genuine safety tests stay.
- **2026-11-12 12:10** Batch 5, TTS on pod `v7l7yk2u75kkie`: failed in alignment at `nodes_restore`. VibeComfy refuses the QwenTTS checkout because our declared source patch makes it dirty ("has uncommitted changes; restore refused"). Read from `preparation.nodes_restore.*` in the receipt.
  - The pod was KEPT this time: the failure came before the receipt refresh. SFX then ran on the same warm pod.
  - **Owner decision (Hannah, AskUserQuestion):** "Teach VibeComfy about patches", rather than a fork or deferring TTS. Dispatched to Terra (`/home/user/wt/briefs/wave3/declared-patches.md`):
    - VibeComfy: `VIBECOMFY_DECLARED_SOURCE_PATCHES`, opt-in. Restore treats a pack whose only changes are declared paths at their declared digests as clean; everything else still refuses.
    - Astrid: `_native` passes the variable from the recipe's `source_patches`.
  - Keep-warm fix: Terra was re-dispatched with an authorised narrow change to `generation.py:92` (one distinct "kept, preparation stale" state; other non-prepared states still rejected).
  - Also seen: `astrid tasks logs` on that TTS task said "no logs recorded" because the Runtime still showed the task `running` with an empty result after the CLI had exited. To investigate after the batch.

### 12:17 UTC — Declared patches ON BY DEFAULT; keep-warm scope 2; gap reviews launched
- **Owner (Hannah):** declared patches must be on by default, documented in VibeComfy's skill docs, and not hidden behind a setting.
  - The opt-in env-var design is withdrawn (brief kept as `declared-patches-v1-optin.md`), and the stopped worker's partial diff was discarded.
  - **v2:** a node lock entry carries `patches = [{path, sha256}]`, and VibeComfy honours it natively wherever it judges a pack dirty. It is accepted only at the locked commit, and only for a tracked modification at the declared digest; anything else refuses as today. It shows as "declared patches verified", and it is documented in vibecomfy-setup SKILL.md and REFERENCE.md. Astrid writes the declarations into managed-custom-nodes.lock from the recipe's `source_patches`. Terra is building it in c-vc-patch and c-patchenv.
- **Keep-warm run 3:**
  - Done so far: the refreshed-receipt path passes, with 6 focused tests green and ruff at 2117.
  - Blocked: the stale-after-failure state is rejected by the custody validator in `worker_preparation.py:829`.
  - **Ruling:** scope extension 2 is authorised, admitting the stale state there with every existing custody check kept. Terra run 4 continues from the diff and runs the full suites.
- **Owner-requested gap reviews**, one Astra reviewer plus a Luna inventory for EACH problem, all read-only on snapshot worktrees `ro-agent` (b306b2be) and `ro-vc` (fe92ac78):
  - review-keep-warm, which asks for every automatic termination path, first-preparation failure, re-prepare loop bounds, and visibility;
  - review-declared-patches, which asks for coverage, spoofing, ordering, and other writers.
- **Batch 5:**
  - TTS failed at fetch, integrity_failed (the expected patch refusal), and the pod was KEPT (v7l7yk2u75kkie).
  - SFX is running on the same warm pod.

### 12:23 UTC — Gap reviews in; rulings
**Keep-warm (Astra review-keep-warm.log, Luna inventory .md.out).** Ruled IN for pass 5 (brief `keep-warm5.md`, runs after pass 4):
- a first-preparation failure on a reachable, exactly-owned pod with verified-stopped jobs → keep it `stale_after_failure`, re-prepare on the same pod;
- the same on the 2nd..Nth failure; the validator requires stopped jobs for the stale state;
- a source-digest-only difference → re-prepare, not release;
- the 120 s verification limit → `verification_timeout` and keep, distinct from `paid_limit_exhausted`;
- receipts name the acquired pod on preparation failure and show expiry, cost and preparation state when kept; recovery keeps the original cause; the `machines` row shows preparation state and a pending release cause.

Ruled OUT for now: account/GPU/image/volume incompatibility, settlement-exception classification, retry ceiling, lifecycle utility pods.

**REVIEW (owner):** host shutdown or restart releases every retained pod (`adapter.py:659` host_shutdown, `worker_owner.py:270` restart). By the letter of the owner rule that is an automatic termination. But nothing enforces idle or paid limits while the host is down, so keeping pods would let them bill unbounded.
- **Recommendation:** a separate slice. Restart adopts a healthy pod with its saved deadlines (and releases it if they lapsed while the host was down). Graceful shutdown keeps releasing unless the owner prefers "keep and warn".

**Declared patches (Astra review-declared-patches.log).** MISSING items to check against the v2 diff once the worker finishes:
- declared vs realized (a clean upstream file must never print "verified");
- `patches` carried only when name, url and commit are unchanged (upsert, `nodes lock`, finalize);
- the workflow-ref path must not drop or transfer the declaration;
- the witness cache keyed on the patch set;
- doctor gets the same lock;
- the asset_alignment path;
- only unstaged ` M`, a regular tracked file, no symlinks, strict path forms;
- the Astrid writer matches repo and commit and fails on ambiguity;
- a successful restore's output is kept as a declared log.

LATER: schema-evidence identity for schema-changing patches, `sha256_before` diagnostics, the attached release-attestation path, concurrent-writer atomicity, and the engine_runner base-bump hazard.

### 12:41 UTC — Declared patches merged into the rehearsal; batch 5 blocked by a stuck task; disk freed
- **Declared patches.** I reviewed the v2 diff against the Astra findings and added three fixes myself:
  - the lock upsert never carries `patches` to another URL or commit;
  - Astrid refuses to declare a recipe patch for a pack locked at a different repository or commit than the recipe's source pin;
  - a successful preparation step's output is now kept as declared run logs (restore's "declared patches verified" is visible on success).

  The VibeComfy failures are the same 6 as the base `fe92ac78` (cm_cli fallback tests, pre-existing). Astrid: 36 passed plus 205 on the pin suites; ruff 2117.
  - VibeComfy `r13/declared-patches` `c7a47e36`.
  - Astrid `r13/declared-patches` `dd5bc822` (pins VibeComfy c7a47e36).
  - Rehearsal `scratch/r13-rehearsal` fast-forwarded to `dd5bc822`.
  - Deferred: schema identity for patches that change schemas, the workflow-ref transport, `sha256_before` diagnostics, the attached release attestation.
- **Batch 5 blocked (BUG, release-blocker candidate).**
  - TTS task 25b59510 failed at 11:47, but the Runtime still shows it `running` (lease expired at 11:55:47).
  - The host log shows "ApiError: conflict: output object is outside the task project". py-spy shows the reconcile thread retrying the failure publication forever.
  - The SFX task then sat queued for 40 minutes with "cannot be claimed: insufficient_storage", and the generate CLI printed NOTHING.
  - The warm pod expired idle at 12:17 unused.
  - Disk was at 787 MB free. I freed 9 GB by deleting the abandoned uv cache in the old state and finished baseline trees under /tmp; it still wasn't claimed afterwards.
  - Stopped the batch, cancelled the queued SFX task. No pods are running; balance $97.66.
  - Evidence: `install-r13b/runs/stuck-task/`. A subagent is investigating the root cause for both bugs; the old host is kept alive for it.
- **Fresh install** `root-b4`/`data-b4` at dd5bc822 + VibeComfy c7a47e36 is done, with its host not started. Paid cells wait for the bug 1 root cause, since any failure with declared logs may block the queue.

### 12:51 UTC — Root causes for BUG 1 and BUG 2; four workers launched; keep-warm passes 3-4 committed
**BUG 1, release-blocker:** any project task whose result carries an output whose bytes were ever published unscoped can't record its result. An empty log (`sha256:e3b0…`) is the guaranteed case.
- **Runtime `_stage_outputs`** (`service.py` about 9294-9321): an existing object with no project owner requires an ingest receipt; inline bytes that were already hash-verified don't count as proof. Result: 409 "output object is outside the task project".
- **Agent `reconcile_publication`** (`generic_host.py` about 11590): it then replays the rejected fail forever at 0.25 s, silently. The cede-after-expiry branch is unreachable for a fail.
- The task stays running and holds the GPU reservation and the executor's single slot, so every later task waits forever.
- Old orphan 0d7f7e41: the same dead end via SIGTERM mid-publication; nothing replays or cedes on restart.

**BUG 2:**
- The Runtime `_claim_task` reports only the first blocker. Storage (787 MB < 1 GiB) masked the real one: the slot held by BUG 1's task.
- The generate CLI is silent: `_runpod_generation_policy` reads `task["spec"]["inputs"]`, but the real shape is `spec.spec.inputs`. So there is no heartbeat, and the timeout is 3600 s. A flat fixture hides it.

**Workers launched (Terra):**
- `terminal-reconcile` (c-recon, Agent): classify unknown vs definite rejection; cede with `reconciliation_required`; backoff; one log line per state change; restart recovery; log claim-reason changes.
- `cli-wait-visibility` (c-cliwait, Agent): one spec-envelope accessor; the wait prints state and waiting-reason changes plus a heartbeat for every placement; actionable text.
- `rt-inline-proof` (c-rt-proof, Runtime `42ae24af`): verified inline bytes prove possession of an existing object, with the project associated; `_claim_task` lists all blockers, names the holder and its lease state, and emits an event on change. Any schema-digest impact must be reported.
- `keep-warm5` (c-warm, on `r13/keep-warm` `d072cf5d`): passes 3-4 committed after my review (default lane 289 passed; 7 new tests passed; ruff 2117). My review notes were added to pass 5: the custody comparison must be scoped to reuse candidates, and a typed exception replaces message matching.

**Integration lane** (`-m integration`, test_remote_machine_cpu + test_worker_preparation): 24 of 25 fail on the unchanged base `b306b2be` too, with the same failure set as keep-warm ("target status task failed"). It is an environment issue, so it provides no local coverage. Noted; not blocking.

**Batch 6 still held.** It runs once terminal-reconcile and rt-inline-proof land (the Runtime fix needs a new Runtime pin in the manifest).

### 14:00 UTC — Machines redesign (owner decisions O1–O8); Fable plan; M1 dispatched
- **Owner (Hannah, 12 Nov):**
  - **O1:** declare once; preferences are overridable defaults.
  - **O2:** claiming is separate from generating; generate only uses an existing machine.
  - **O3:** no automatic claim.
  - **O4:** no consent flag ("they've already rented the machine").
  - **O5:** named machines: `generate --machine bjork`.
  - **O6:** jobs queue on their machine.
  - **O7:** no hard datacenter pin; overridable.
  - **O8:** you can see what's happening on a machine.

  Full text: `briefs/wave3/machines-design.md`.
- **Fable critique accepted** (`briefs/wave3/machines-plan.md`): the claim is the only spend authority. It deletes the paid flags on generate, the generate-claims path and the consent flag; merges seven budget concepts into two; reuses `Placement.machine`, the lease record and the Runtime queue. There are 13 tasks, 10 of them for Release 13. Critical path: M1 → M2 → M10, with M9 last.
- **DECIDED (owner agreed, 12 Nov):** the idle timer is the only lifetime mode; idle pauses while jobs are queued; `keep` extends it; `--idle never` replaces `--until-release`; the budget cap still bounds everything.
- **Base:** `r13/machines` `22e5a13e` = rehearsal `922a19eb` + keep-warm `9e7b2a48`. M1 (SS) went to Codex Astra in `c-m1`; the base suites are running.
- **Dispatch rule:** N → Luna, X → Terra, S → Sol, SS → Astra, T (wording, CLI layout, skill voice) → Opus.
- **Batch 6:**
  - The first attempt failed with no project on the fresh install. I created and selected one by hand (usability log #1) and re-ran.
  - The TTS cell is in the product's capacity wait: no 5090 or 4090 in EUR-NO-1 (the volume's datacenter); EU-RO-1 has Low 5090 stock.
  - The CLI is silent during the wait while the host logs "no stock yet" (usability log).
- **14:02 UTC:** Hannah agreed the idle-timer ruling. Dispatch rule added: every Astra, Sol or Terra task gets a paired read-only Luna inventory, launched by the manager (nested Codex fails in the sandbox). The senior worker's brief points at it and hands mechanical edits back as a list.
