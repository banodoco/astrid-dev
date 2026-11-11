# Release 13 decision log

Append-only. The NOW block is replaced; entries below it are never edited. Entries flagged **REVIEW** are user-visible changes, scope-vs-time trades, named exceptions or anything touching Release 12.

## NOW (2026-11-11 23:00 UTC)

- **Rehearsal head:** Agent `scratch/r13-rehearsal` `0560e34d06269d058056e6ee4087c5ec9d544bd7`, which is Release 12 candidate `c5370a86` + generation candidate `1439ccc6` (G5 ruling) + g1-wait-wording + g2-launchers + g3-graph-facts + tool-catalog + g4-pins-2 + g3-receipt + the staged-recipe read fix + the removed-name cleanup.
- **Running:**
  - G3 slice 3, the bundle, redactor and collect-before-reset (`r13/g3-bundle`).
  - Generated-output swap-then-commit (`r13/task-handle-swap`).
  - Merging the four ready branches into the rehearsal, one at a time, with ruff and focused proof after each.
  - G4 review follow-ups (`r13/g4-followups`).
  - The `test_generation_preparation[datacenter]` hang diagnosis (`r13/prep-hang`).
  - Rehearsal CI run 43102625660 on `246cad0f`.
- **Ready to merge into the rehearsal:**
  - `r13/placement-overrename` `1206322a`, which contains `r13/generate-routing` `08a2f038`.
  - `r13/update-inputs` `86889894`.
  - `r13/test-runpod-guard` `a9e1f2c0`.
  - `r13/ruff-debt` `1702f244`.
  - Being merged now. After every merge: `make ruff` (exact count 2128) and focused proof against `c5370a86`.
- **Blocked:** nothing outside the preconditions below.
- **Preconditions for paid work:**
  - (a) Receipt, bundle and collect-before-reset in the build: building.
  - (b) Tests cannot reach RunPod: guard accepted, not yet merged.
  - (c) Credential via the private form: not requested.
  - (d) Dedicated environment "Astrid Release 13 GPU": not created. Design agreed: unrestricted network, credential on `api.runpod.io` and `rest.runpod.io` only.
  - Review (1), bundle and redactor: not sent.
  - Review (2), pins and installer: no blocker. Clears once `test_pod_install_route` is fixed (in `r13/g4-followups`).
  - Five receipt-swallow (c) fixes plus the `EXCEPTIONS` allowlist addition: queued, stacked on `r13/g3-bundle`.
  - Isolated install of the tuple: works, to be redone on the final head.
- **Workers:** Codex signed in (ChatGPT). Tiers confirmed by a trivial read-only call: Luna `gpt-6-luna`, Terra `gpt-6.1-terra`, Sol `gpt-6.1-sol`, Astra `gpt-6-astra`. New tasks run on Codex; Claude workers already running finish where they are. Fallbacks used: none.
- **Money:** spent $3.41 of $40 at the last Release 12 record (11 Nov 06:41 UTC), plus about $0.46 a day of storage. No rental this release. To be reconciled against the account before the first rental.

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
