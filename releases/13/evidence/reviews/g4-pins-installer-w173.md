**APPROVE — G4 at A′ `f709407cb10cc56bafebae51080832386bca3a44`.**

No demonstrated R13 money, custody, or generation failure—or secret leak in a bundle/message—meets the GATE. The earlier URL-secret refusal blocker is fixed. The remaining findings are NOTES.

These rows are ready to paste into `deferred.md`; Agent references are at A′ unless stated otherwise.

| Item | Source |
|---|---|
| **1. NOTE — Next release:** Remove user-specific absolute paths from missing/malformed installed-manifest errors. Pin-mismatch messages are sanitized, but missing/unreadable manifests, non-object manifests, missing Agent/Runtime fields, and missing lifecycle entries still print `manifest_path`. No credential exposure demonstrated. | `astrid/packs/runpod/managed_sources.py:117`, `:119`, `:125`, `:129` |
| **2. NOTE — Next release:** Make the pin-check coverage explicit. It checks shared pin files, recipe/environment digests, lifecycle declarations, Python workflow ComfyUI literals, and Runtime lock equality; it does not validate every H3 literal or historical fixture/provenance revision. Preserve historical identities as provenance rather than presenting them as current-release qualification. | `tests/core/generation/test_pin_single_source.py:35`, `:64`; `tests/fixtures/h3_cpu/object_info_h3_runpod.provenance.json:8`; `astrid/packs/runpod/lock-inputs/README.md:48` |
| **3. NOTE — Next release:** Add Windows R12→current upgrade and retained-engine/machine uninstall evidence. The named tester job proves fresh installation, doctor-bundle creation, and folder/task removal. It records a process census but does not assert that census is empty; neither regular Windows job exercises a paid pod. | Tester `cd7892b74`, `.github/workflows/windows-manifest-proof.yml:47`, `:57`, `:69`, `:94`; A′ `.github/workflows/ci.yml:39` |
| **4. NOTE — Next release:** Remove author-specific local paths from shipped provenance and lock comments. These files appear in the release wheel’s build listing. They are metadata/comments, not demonstrated executable dependencies or credentials. | `astrid/packs/h3_av/workflows/lanpaint_h3_av_generalized/workflow.py:45`; `astrid/packs/runpod/requirements.linux-cu130.lock:2`, `:1155`, `:1165`, `:2810`, `:3757`; `astrid/packs/runpod/lock-inputs/README.md:48`, `:73` |

The canonical release identities are:

| Component | Pin | Declaration |
|---|---|---|
| Lifecycle | `7f0b025e9391baac9f5c2fb7393617ea6fef0704`, version `0.3.1.dev0` | `astrid/packs/runpod/pins.json:6` |
| VibeComfy | `dba38f8644c46f652376f2cd5112ea161e40f09b` | RunPod `pins.json:15`; VibeComfy `pins.json:10` |
| Runtime | `6855dfa8df65cf8ae4c002b57134d6505493c17c` | `runtime.lock.json:71`; `astrid/resources/runtime.lock.json:71` |
| H3 node pack | `361624fb406b63eb6694442eac6c895fc1533a70` | RunPod `pins.json:19`; VibeComfy `pins.json:14` |
| ComfyUI | `6bfaacc67c2103481e5f0c84d75257cd0581d86a` | RunPod `pins.json:11`; VibeComfy `pins.json:6` |

The two pin files agree on shared sources. The packaged Runtime lock is **byte-identical** to the root lock.

The declaration/copy inventory from the tracked-source search follows. Paths sharing a directory prefix are grouped.

| Location | Declaration or copy |
|---|---|
| `pyproject.toml:78` | Literal lifecycle repository/revision. |
| `astrid/packs/runpod/pack.yaml:194,346,473,577,811` | Lifecycle version requirement `>=0.3.1.dev0,<0.4`. |
| `astrid/packs/runpod/recipe.linux-cu130.json:5`; `astrid/packs/vibecomfy/recipe.windows-cu130.json:5` | Digest-bound references to canonical RunPod pins; named source bindings rather than additional revisions. |
| `astrid/packs/runpod/environment.linux-cu130.json:10`; `astrid/packs/vibecomfy/environment.windows-nvidia.json:10,26` | Named ComfyUI, VibeComfy and node-pack references; Windows environment binds the second pin file. |
| Both packs’ `extensions/generation.engine/comfyui.yaml` | Recipe digests, checked against recipe bytes. |
| `astrid/packs/h3_av/shared/generation.py:275` | Current H3 pack revision. |
| `astrid/packs/h3_av/workflows/native_h3_continuation/workflow.py:62,63`; `native_h3_continuation_refs/workflow.py:81,82` | Current ComfyUI/H3 declarations. |
| `workflows/astrid_intro_h3_anchor_chain/workflow.py:28,33`; `workflow_cuda13.py:27,32` | Current ComfyUI/H3 declarations. |
| `workflows/seitanism_h3_av_extension_fixed/workflow.py:78,79`; `…_repaired/workflow.py:62,63`; `…_verified/workflow.py:82` | Current ComfyUI and, where explicitly declared, H3 revisions. |
| `workflows/seitanism_h3_av_extension_end_frame/workflow.py:84`; `…_end_frame_reference/workflow.py:48` | Current H3 revision constants. |
| `astrid/packs/runpod/lock-inputs/README.md:4,47` | Current ComfyUI revision; `:48` records the older VibeComfy lock-generation input `88cff6d5…`. |
| `guides/anchor-to-anchor-video-generation.md:227`; `astrid-intro-animation-execution.md:114`; `astrid-intro-cuda13-relaunch-20260918.md:83`; `matrix-minkhole-extension-video-generation.md:99`; `workflows/seitanism_h3_av_extension/PROVENANCE.md:5,6` | Current H3 revision references. The anchor guide also distinguishes an investigated upstream workflow revision. |
| `tests/core/generation/test_engine_recipe.py:109,123,125`; `test_engine_release.py:188`; `test_one_engine.py:13`; `backends/test_qwen_21_turbo.py:197,198`; `fixtures/qwen3-tts-tiny/README.md:79` | Current ComfyUI/H3 assertion or fixture copies. |
| `tests/integrations/test_pinned_source_cpu.py:30,35`; `tests/packs/h3_av/test_release_runtime_guard.py:28`; `test_runtime_declaration_sync.py:27`; `tests/packs/runpod/test_h3_release.py:501,505` | Current ComfyUI assertions. |
| `tests/fixtures/h3_cpu/object_info_h3_runpod.provenance.json:11`; `…_graph_closure.provenance.json:11`; `…_overlay.provenance.json:10`; `tests/helpers/h3_cpu_runtime.py:1027`; `tests/packs/h3_av/fixtures/source_fit_start_contract.py:4` | Current H3 revision in captured/adapted test provenance. |

There are also **historical identities**, so “every revision literal equals canonical” would be false:

- The H3 CPU provenance files above retain ComfyUI `ee71d5c4…` and VibeComfy `01f38461…`; the original capture additionally records mounted VibeComfy `eff47eda…`. See their `:8–14` fields, `tests/helpers/h3_cpu_runtime.py:45`, and `source_fit_start_contract.py:6`.
- Embedded import provenance retains H3 `ee38f3dd…` and `75432bdb…` in the native continuation workflow at `:78`, continuation-refs at `:89,98`, and the fixed/repaired/verified authoring workflows at `:86,95`, `:78`, and `:89`. Their explicit restore declarations use the canonical pin.
- `tests/core/generation/test_generate_target_journey.py:39` pins a historical VibeComfy fixture pairing; `test_engine_release.py:27–29` declares historical build bases.
- Historical Runtime identities remain in `tests/editing_conformance/test_authenticated_legacy_restore.py:24`, `test_inverse_stage_runtime_regressions.py:32`, `tests/helpers/run_wc6_completion_capture.py:26`, `tests/sdk/test_timeline_editing_acceptance_runtime.py:17`, `tests/test_installer_pinokio_integration.py:505`, `tests/test_skills_installed_composition.py:32`, `tests/test_vendor_lock.py:76`, and `tests/timeline/test_authoring_media.py:935`.
- Upgrade/release fixtures retain older Runtime/VibeComfy identities in `tests/upgrade/releases.json:21,59,62,79,82`, `tests/fixtures/upgrade/identity_aware_version_v1.json:6,9`, `diagnostic_identity_41809494741.json:32`, `r0-legacy-timeline/expected.json:2`, `tests/fixtures/release0/provenance.json:35`, and `tests/fixtures/windows-r0-owner-41775575452/provenance.json:6`. `tests/test_verify_installed.py:256` preserves the older default.
- ComfyUI protocol captures retain `426f5eea…` in `tests/fixtures/comfyui_protocol/object_info.json:26` and subsequent node records. `test_release_runtime_guard.py:18` deliberately supplies a differing ComfyUI revision.

The runtime/script readers derive their identities rather than declaring another current SHA: `canonical_pins.py:23`, `vibecomfy_dependency.py:14`, `engine_recipe.py:519`, `managed_sources.py:109`, `_local_schema.py:151`, installer `tools.py:36`, `backend.py:425`, and scripts `ci_install_runtime.py:13`, `vibecomfy_pin.py:63`, `regenerate_runtime_pins.py:106`. The worker setup and CI workflows likewise read the pin files/Runtime lock. The regeneration script writes both Runtime lock copies.

**The first-frame revert leaves no newly required pin dangling.** The first-frame merge did not alter either pin file or the Runtime lock. A′ restores `shared/generation.py` and `fixtures/spec_min.json` to their pre-merge bytes; the first-frame-specific graph test and reference fixture are absent. W164’s earlier review independently records restoration across all 17 affected paths. The H3 pin already existed before that feature.

The live restore evidence is narrower than all five identities: `releases/13/evidence/live/final-A/h3-i2v-failure/preparation.nodes_restore.stdout.log:1,2` explicitly reports:

- H3 pack refreshed to `361624fb406b63eb6694442eac6c895fc1533a70`.
- VideoHelperSuite refreshed to `4ee72c065db22c9d96c2427954dc69e7b908444b`.

Both equal canonical. That log does **not** independently attest restoration of Runtime, lifecycle, VibeComfy or ComfyUI, and it belongs to A’s failed round, not a new A′ run.

At RunPod prepare, lifecycle repository/revision/version and an explicitly different VibeComfy revision are refused. The formatter prints only validated repository identity, SHA and version fields; URL userinfo, query strings, fragments, malformed hosts and header-like strings become `<invalid>`. It does not print arbitrary manifest headers. See `managed_sources.py:50–100,138–152` and installer `backend.py:401–438`. The pin-mismatch message contains no local manifest path; finding 1 concerns the separate malformed/missing-manifest branches.

The message tells users:

> Install a release manifest whose pins match this Agent

It also includes checkout-editing advice. For an installed user, the usable recovery is installation/update with a matching release manifest.

An R12 manifest can be refused if retained beside a separately replaced R13 Agent. The R12 source reviewed at `0e1543e0` has older lifecycle, VibeComfy, Runtime and ComfyUI pins. **Normal managed upgrade does not retain that old version manifest:** the installer downloads the selected manifest (`cli.py:938`), dispatches a higher release to update (`core.py:237,670`), stages the new version, checks its pins and writes its manifest (`backend.py:1340–1347`), then switches the current version through the update transaction (`core.py:769–837`). I found no unavoidable refusal-without-remedy in that path. Missing lifecycle remains tolerated during legacy staging but is refused by RunPod prepare; the selected test confirms that distinction.

Uninstall performs removal preflight and the Runtime stop fence **before** unregistering or deleting files (`core.py:680–702`; `backend.py:1001,1096`). Active/unreconciled work blocks Runtime interruption. Host shutdown closes managed sessions and target bindings; the RunPod binding requests release (`generic_host.py:7478,7496`; `adapter.py:770–783`). Uncertain stop propagates instead of proceeding with normal removal.

Workspace data remains unless `--delete-data` is supplied; ownership and overlap checks protect removal (`backend.py:1876,1931,1953`). Per-install service configuration disappears with the program tree. I found no demonstrated broken-settings or abandoned-machine path, but the named Windows evidence does not prove live pod cleanup.

The reviewed installer constructs its persisted service environment from tool paths and selected settings, rather than copying ambient provider credentials (`tools.py:663`; `backend.py:1374`; `service.py:41`). **The manifest itself is persisted whole** at `backend.py:1347`; this is not a general sanitizer for a custom manifest containing secrets. The reviewed tester manifest uses public source/download identities and matches A′’s dependency pins.

The CI evidence establishes:

| Evidence | Actual assertions |
|---|---|
| [Tester run 43664846375](https://github.com/banodoco/astrid-agent/actions/runs/43664846375) | Fresh public-line install of Agent `9acb55b6…`; selected manifest’s Agent SHA matches; doctor returns success and creates a ZIP; uninstall with `--delete-data`; three installation/support folders absent and root Scheduled Task absent. No R12 predecessor is installed. |
| [A Windows job](https://github.com/banodoco/astrid-agent/actions/runs/43693935046/job/132750234912) and [A′ Windows job](https://github.com/banodoco/astrid-agent/actions/runs/43705081374/job/132784319339) | Each reports **15 + 40 + 36 + 21 passed**: PowerShell task cleanup, Windows host/service binding, rendering admission/source handoff, and native process/permission/stdin behavior. These are not full upgrade/install journeys. |
| [A′ release-wheel job](https://github.com/banodoco/astrid-agent/actions/runs/43705081374/job/132784318967) | One wheel, hashed dependency installation, Runtime installation, `pip check`, installed-wheel smoke and toolchain validation. Both Python 3.11 and 3.12 release-wheel jobs succeeded. |

Installer, packaging and relevant CI files have no diff between the tester Agent head and A′. This supports carrying their unchanged-source evidence forward, without claiming the tester installed A′ itself.

For wheel contents, I inspected the A′ build’s **1,338 archive-member listing**, artifact metadata, tracked filenames and packaging configuration. Neither tests/test-named files, `.env` files, golden directories, bytecode caches nor private-key filenames appeared. `pyproject.toml:105–133` disables implicit package data and excludes test/golden packages. The wheel includes both engine pin files and `astrid/resources/runtime.lock.json`.

The artifacts are `release-wheel-3.11` and `release-wheel-3.12`; each upload contains the wheel and `toolchain.json`. I did find the shipped local-path metadata in finding 4. This was a build-listing/source inspection, **not a downloaded-wheel byte-for-byte secret audit**.

After `bash scripts/worker-env/agent-setup.sh`, one `agent-pytest.sh -q` process ran 15 explicit selectors: eight consistency checks from `test_pin_single_source.py`, four refusal selectors from `test_pod_install_route.py`, and three installer lifecycle/legacy selectors from `test_installer_sources.py`. Parameterization produced **21 passed in 1.19 seconds**. A separate stdlib-only formatter probe omitted all six supplied synthetic URL/header/path payloads.

I read the specified G4 decisions and relevant earlier review evidence. I did **not** read `.env` files, credential files or `~/.codex`; inspect a user’s installed settings; inspect doctor ZIP contents; download the wheel archive; read the complete App PowerShell bootstrap source; or execute a Windows upgrade/uninstall or live generation. No RunPod/provider calls, pushes, or tracked-file edits occurred. The detached worktree was clean before removal; **worktree, temporary environment and setup log were removed**.