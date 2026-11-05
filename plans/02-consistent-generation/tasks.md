# Tasks: consistent generation path

[Project explanation](plan.md) · [Inputs and branch rules](inputs.md) · [Current project status](../../README.md)

These are the existing four completion items and seven integration steps, not eleven new features. Click an item for its instructions below. The historical phase names Plan 02 and Plan 03 mean completion and integration respectively. Recorded evidence must be rechecked against the actual candidate; it does not mark a task done.

## Task index

| Phase | Task | What it does |
|---|---|---|
| Complete | [PINS](#pins) | Finish dependency/build-path proof on the retained implementation. |
| Complete | [DEFAULTS](#defaults) | Finish default selection and its focused checks. |
| Complete | [INSTALLED-TEST](#installed-test) | Prove the installed package without claiming real model readiness. |
| Complete | [END](#end) | Complete the existing acceptance review. |
| Integrate | [GEN-VFIX](#gen-vfix) | Combine the VibeComfy resource/template changes. |
| Integrate | [GEN-LIFE](#gen-life) | Qualify the lifecycle dependency. |
| Integrate | [GEN-RUNTIME-STOP](#gen-runtime-stop) | Include the Runtime stop change only if required. |
| Integrate | [GEN-AGENT](#gen-agent) | Combine Agent work and regenerate dependency pins. |
| Integrate | [GEN-APP-PINS](#gen-app-pins) | Update the App to the verified Agent/Runtime versions. |
| Integrate | [GEN-REVIEW](#gen-review) | Review the exact combined candidates. |
| Integrate | [GEN-PROMOTE](#gen-promote) | Promote the reviewed commits to `pre-main`. |

## Completion tasks (historical Plan 02)

### PINS

**Outcome and action:** finish candidate-only pin/closure acceptance on retained Agent candidate `1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`; retain its implementation and do not rebuild old broad selectors.

**Dependencies:** Existing Agent/VFIX sources. Implementation and verification can proceed after initiative start, independently of installer publication.

**Lead / class:** Terra / X: Linux x86_64 closure, strict process-custody, and multi-source pinned dependency proof interact; deploy bounded Luna helpers.

**Reuse and focused evidence:** Reuse the 231 generation checks, 28 asset/installed-child checks, pin/recipe/ancestry checks, and source-policy/closure investigation recorded in [local-only source evidence](../../references/evidence-summary.md). Latest verifier ended with exit 143 after setup and lifecycle identity; it produced **no final verdict**, so cancellation is not a product failure. Focus only current PINS candidate-only selectors: retained failure nodes, the three named CPU integration nodes, asset/installed-child checks, and real fresh-cache Linux x86_64 closure. CORE/CPU/closure returning ENV 3 for missing `VERIFY_SIDE` remain unexecuted, not passed. The complete retained card corpus and logs are not bundled here; at normal task setup, recover the exact retained card/check identities and evidence from the referenced source evidence and task materials. This is setup for the existing task, not an added approval gate. Do not treat a named test file as authorization for its entire suite, and do not invent missing node IDs.

**Done condition:** Exact candidate head gets complete required Linux evidence and the existing LB-PINS load-bearing review; any real failure follows the existing orchestrator reproduce/repair/targeted-retest flow. No BASE rerun.

### DEFAULTS

**Outcome and action:** finish the retained local merge `3fe46b90e4081b20bfb5e6face00520eddafbebd` (PINS plus donor `9d3bb24831676cbfc2a0d3dd1c7769f1937569c3`), including dirty SDK/CLI-GOLD work; it is an unpublished checkpoint, not accepted code.

**Dependencies:** PINS candidate. Implementation/checks can proceed independently after initiative start; final composition waits for installer increment 01.

**Lead / class:** Terra / X: CLI dispatch/default selection crosses SDK, generation entries and dry-run behavior; deploy bounded Luna helpers.

**Reuse and focused evidence:** Reuse the local merge and two prompt-only video-refusal checks. Finish `astrid/sdk/generation.py` and `tests/core/generation/test_cli_gold_075b.py`; focused proof: six defaults on `auto` and RunPod dry-run, Foley RunPod refusal, prompt-only video refusal, no-GPU/no-RunPod guidance, K-owned bytes unchanged, existing SDK defaults test and saved-output journey node.

**Done condition:** Complete implementation, targeted checks and evidence on the exact PINS descendant; do not count the local checkpoint as passed.

### INSTALLED-TEST

**Outcome and action:** amend DEFAULTS step 6, this card and END to an honest installed-package proof. This is a test-contract mismatch; no installed runtime failure has been observed.

**Dependencies:** Completed PINS and DEFAULTS.

**Lead / class:** Terra / X: the proof spans isolated package installation, CLI behavior and a separate real child/protocol boundary; deploy bounded Luna helpers.

**Reuse and focused evidence:** Reuse fresh-install/import/CLI/defaults coverage and `tests/packs/vibecomfy/test_installed_child_path.py::test_installed_qwen_managed_child_path` for the separate installed-child `/prompt`→`/history`→`/view` protocol-fixture boundary. Assert managed-unavailable/fail-closed at the actual gate reached; assert missing-model-specific refusal only if legitimate receipt prerequisites allow reaching that check. Never fabricate a receipt or bypass readiness.

**Done condition:** Fresh non-editable package install, import origins, CLI inventory/defaults/dry-run, installed-child boundary, and honest managed-unavailable/fail-closed result are evidenced on the exact tuple. **The full fresh-install→managed-model-generation→gallery journey and real model readiness/execution remain explicitly unproven and deferred.** No weights, GPU, or provider call.

### END

**Outcome and action:** perform the existing scoped final review after all required rows are verified; update its DONE MEANS/remainder to match the revised proof.

**Dependencies:** PINS, LB-PINS, DEFAULTS, INSTALLED-TEST and VFIX/QV evidence; all required source pins finalized.

**Lead / class:** Astra independent review (not an implementation tier).

**Reuse and focused evidence:** Reuse the current END review procedure and exact candidate/evidence links.

**Done condition:** Review records each required item and any blockers; managed model readiness/execution are listed as deferred, not silently dropped or reported complete.

## Integration tasks (historical Plan 03)

### GEN-VFIX

**Outcome and action:** compose VibeComfy resource/template donor; resolve its single template-index conflict, preserving Foley and current entries.

**Dependencies:** Implementation may proceed after start; final composition waits for installer increment 01. Freeze the current target at composition. If no pre-main ref exists, record that and use observed main as merge base; create only the immutable candidate lane.

**Lead / class:** Luna / N (normal).

**Reuse and focused evidence:** Donor `1b2e242ce7396442c85395d3220a2481216b57c1`. Focused current RI-V selectors: `tests/test_ready_templates.py`, `tests/test_template_roundtrip.py`, `tests/test_installed_resources.py`, `tests/test_installed_wheel_execution.py`, `tests/test_packaging.py`, `tests/test_packaged_ready_trust.py`, `tests/test_repo_relative_path_installed.py`.

**Done condition:** Candidate preserves current template entries and passes targeted resource/package/template checks.

### GEN-LIFE

**Outcome and action:** qualify adopted lifecycle source/API; carry the final source pin into Agent composition.

**Dependencies:** CPU qualification may proceed after start; final composition waits for installer increment 01. Freeze lifecycle target; if no pre-main ref exists, record absence and use observed main as merge base.

**Lead / class:** Luna / N (normal); known source and prescribed CPU contract checks.

**Reuse and focused evidence:** Source `c47fa76be6e7c0aa661d044a0de5b3b73f6fdbac`. Run current RI-L selected CPU/fake-provider nodes: `tests/test_https.py`; `tests/test_engine_bridge.py`; `tests/test_session_engine_proxy.py::test_session_enable_binary_http_and_no_bearer_projection`, `::test_session_enable_and_ws_auth_before_upstream`, `::test_session_enable_rejects_invalid_conflicting_and_observation_claims`, `::test_session_websocket_frames_ping_close_and_header_filtering`, `::test_session_enable_transport_rejections_are_specific_and_sanitized`, `::test_session_prompt_relay_never_retries_or_exposes_transport_secrets`; `tests/test_observation_policy.py`, `tests/test_engine_startup_config.py`, `tests/test_api.py`, `tests/test_provider_mounts.py`; and RI-L’s three named K27 regressions in `tests/test_https.py` (completed-job eviction, sequential capacity reuse, delete/retire).

**Done condition:** Exact source/API identity passes these selected CPU checks. No real provider, pod or GPU run.

### GEN-RUNTIME-STOP

**Outcome and action:** compose Runtime stop/ownership `b005394b06602c84e2abd4ba7eec8fa2f1dd8e94` only if source comparison proves the retained included Agent behavior depends on it; otherwise omit it.

**Dependencies:** Start after initiative start; freeze current Runtime target. Include only on named dependency evidence, before canonical locks are generated.

**Lead / class:** Luna / N.

**Reuse and focused evidence:** RI-R focused checks only: `tests/test_astrid_product_down.py` and `tests/test_local_cli.py`, narrowed to the changed stop/ownership behavior. Keep separate CAS `1e60e3b746c37c1fd22c14f0ceeb1218dc36b373`, lease `33e9195a8ac57c4ba61f372ef6f25139c37eaa97`, healthfold `2870…` and custody `103f97803f7f391e2c810ebdf086f798326cd75a` deferred unless an independently named included dependency is proven.

**Done condition:** Record the actual source-level dependency decision and exact check result. Never pin an unverified Runtime tuple; if stop is not required, preserve current Runtime source.

### GEN-AGENT

**Outcome and action:** compose the completed Agent generation sources after producers; preserve PINS and completed DEFAULTS once, then generate canonical pins/locks against final VibeComfy, lifecycle and Runtime heads.

**Dependencies:** PINS, DEFAULTS, INSTALLED-TEST accepted; GEN-VFIX/GEN-LIFE qualified; any required GEN-RUNTIME-STOP qualified; installer increment 01 accepted before composition/publication.

**Lead / class:** Terra / X: multi-repository producer ordering and coupled canonical pins/lock require integration decisions; Luna helpers required.

**Reuse and focused evidence:** Agent PINS `1608dbbf7036ad3c3b2b5e10956a726921bd4f9f`; DEFAULTS `3fe46b90e4081b20bfb5e6face00520eddafbebd` is an unpublished incomplete checkpoint, reuse only after completion. Run only affected selectors: recover the current PINS card exact candidate-only TEST block at task setup; DEFAULTS `tests/core/generation/test_cli_gold_075b.py`, existing SDK defaults file and saved-output journey node; revised installed-package proof.

**Done condition:** Combined Agent candidate has reviewed producer pins/lock and all affected focused checks pass; no stale historical lock.

### GEN-APP-PINS

**Outcome and action:** refresh App’s canonical Agent/Runtime manifest and lock; no App feature donor.

**Dependencies:** GEN-AGENT candidate verified; retain installer-consent work.

**Lead / class:** Luna / N (normal).

**Reuse and focused evidence:** No App feature SHA. Reuse current focused manifest/lock and installer-consent checks.

**Done condition:** App identifies the exact verified Agent/Runtime candidate heads; final tuple acceptance occurs at GEN-REVIEW. No concurrent-editing source imported.

### GEN-REVIEW

**Outcome and action:** independently review exact composed candidate heads/evidence; do not publish in this row.

**Dependencies:** All included rows verified; immutable candidate refs and evidence available.

**Lead / class:** Astra independent review, separate from implementation tiers.

**Reuse and focused evidence:** Use existing scoped review process and row evidence; no broad suite.

**Done condition:** Review is clear or blockers return through the existing reproduce/repair/targeted-retest flow.

### GEN-PROMOTE

**Outcome and action:** promote the exact Astra-reviewed immutable candidates to current `pre-main` with ordinary fast-forward/create operations and record receipts.

**Dependencies:** GEN-REVIEW clear; installer increment 01 already on `pre-main`; target has not moved incompatibly.

**Lead / class:** Luna / N (normal).

**Reuse and focused evidence:** Use the exact reviewed candidate heads/manifest from GEN-REVIEW; recapture current target immediately before promotion.

**Done condition:** `pre-main` resolves to the reviewed heads and promotion receipts match them; if target moved, reconcile and rerun only affected checks/review before promotion.

## Shared execution rules

Use the [composition/publication rules and evidence interpretation](inputs.md) for every task. Adapt the retained cards and runner inputs in place after start; add no new framework or approval gate. The orchestrator owns technical contract corrections and reproduce → repair → targeted retest. Keep row evidence separate from the original deliverable count; these integration steps do not rewrite original completion. See the [initiative handoff](../MANAGER.md) for execution ownership and existing run controls.
