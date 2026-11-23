# SFX / credential / understanding gaps on release/14/main

Source: ~/Developer/astrid-release-src/wt-r14-fix-1238 (branch release/14/fix-1238-stale-registry-asset, HEAD 9f614dff7; read only).
Tags: [fact] = read in code or GitHub; [inference] = my reading, not run.

## 1. Credential declarations

Action `env` vs `secrets_required` (pack.yaml, parsed with PyYAML; script at tooling/envcheck.py):

| Action (pack.yaml line) | env | secrets_required | mismatch |
|---|---|---|---|
| generation.generate_audio (56; env 193-195) | FAL_KEY, WAVESPEED_API_KEY | none | both |
| generation.generate_image_upscale (1431; env 1485-1486) | FAL_KEY | none | FAL_KEY |
| generation.generate_video (1576; env 1738-1739) | FAL_KEY | none | FAL_KEY |
| training.search_loras (211; env 271) | HF_TOKEN, HUGGING_FACE_HUB_TOKEN | none | both |

Correct: generate_image (436-439), generate_image_cloud_i2i (601-604), generate_image_edit (944-947), generate_image_openai (1185-1215), generate_image_codex (env [] / secrets []).
No other pack (developer, h3_av, local, rendering, runpod, setup, timeline, vibecomfy, wan2gp) declares an env or secrets_required that mismatches. vibecomfy/pack.yaml:665 `env:` is a process env var (VIBECOMFY_HEADLESS), not a credential.

Host allowlist (fact):
- generic_host.py:2055-2060: for `action_invocation` records, `_required_secret_names` returns ONLY `metadata.declared_secrets`. Comment says canonical action manifests are the authority.
- actions.py:106: `declared_secrets = list(declaration.get("secrets", ()))`, i.e. the ACTION-LEVEL `secrets:` key, not `secrets_required`.
- No pack.yaml in astrid/packs has an action-level `secrets:` key (grep `^ *secrets:` = 0 hits). So the allowlist is [] for every bundled action.
- generic_host.py:10062-10063 sets ASTRID_ACTION_ID and ASTRID_ACTION_ENV_ALLOWLIST (json of the list above) for action records.
- generic_host.py:2079-2080 (`secrets_required` union) applies only to non-action records.
- credentials_scope.py:76 (`_ACTION_SECRETS_ENV`), :79-110: `_injected_worker_credential` raises `undeclared_secret` at :110 when ASTRID_ACTION_ID is set and the reference is not in the allowlist. Called at :167 from the worker-side credential resolver.
- subprocess_env.py:96 propagates ASTRID_ACTION_ENV_ALLOWLIST; :167-169 raises SubprocessEnvPolicyError for undeclared secret values.
- runner.py:944-950 (command executors): declared secret env = executor isolation.secrets_required + metadata.secrets_required + metadata.required_env + metadata.env. So on the runner path the `env` list IS honoured; the mismatch is not enforced there.
- schema.py:241-245: SafetyDeclaration.secrets_required = isolation + metadata.secrets_required. This is what the capability handle reports, so generate_audio shows secrets_required=() (test_capability_handle.py:284-288 pins the union behaviour).

Implication [inference]: on release/14/main, adding `secrets_required` to generate_audio (the FRICTION.md fix) would fix the handle/readiness report but would NOT by itself change ASTRID_ACTION_ENV_ALLOWLIST, because the action-record branch ignores metadata.secrets_required. A real fix needs an action-level `secrets:` key (or a code change to generic_host.py:2055-2060). Whether generate_image hits the same undeclared_secret path is unverified: the same code applies to it (no `secrets:` key), so either its dispatch avoids the ASTRID_ACTION_ID path or it fails too. FRICTION.md was written against an older commit and did not test generate_image in cloud mode.

Tests:
- tests/integrations/test_generation_runtime_composition.py:1627 and :1885 assert metadata["secrets_required"] == ["FAL_KEY"] for generate_image_cloud_i2i. These load the shipped manifest through _shipped_executor_definition (:69, reads astrid/packs/<pack>/pack.yaml with yaml) and _write_action_pack (:93).
- tests/test_provider_manifest_readiness.py:37-40 and tests/test_capability_handle.py:284-288, 490 touch the secrets union.
- tests/test_pack_action_census_ratchet.py:16 globs `*/pack.yaml` from a pack root (uncovered_pack_actions).
- tests/test_structure_contracts.py, tests/test_capability_matrix_sync.py, tests/core/pack/*.py (e.g. test_definitions_record.py, test_r8_prod_cli_discovery.py, _manifest helpers), tests/core/test_executor_api_keys.py.
- No existing test compares pack.yaml env with secrets_required. Best host: tests/test_pack_action_census_ratchet.py (already globs */pack.yaml over every bundled pack) or a new test next to tests/integrations/test_generation_runtime_composition.py using _shipped_executor_definition. Pack manifests are loaded via PyYAML (yaml.safe_load) in tests; there is no shared manifest-loader helper for this check.

## 2. generate_audio modes (fact)
- generate_audio/run.py:117 `_UNWIRED_MODES = {"tts", "sfx"}`; :116 `_VALID_MODES = {"music"}`; :120-130 `_validate_mode` raises SystemExit "Mode 'sfx' is not wired this sprint".
- generate_audio/STAGE.md:13-15: "The direct executor backend loop is `music`... `sfx` remains reserved for a future action."
- Catalog (core/model_catalog/models.yaml) entries with an `sfx` mode:
  - hunyuan-video-foley (1146-1165): cloud fal-ai/hunyuan-video-foley, requires video_ref, prompt maps to text_prompt. Video-to-audio.
  - hunyuan-foley-local (1166-1181): local, requires video_ref, licence excludes EU/UK/KR. Video-to-audio.
  - lava-sr (1237-1252): cloud fal-ai/lava-sr, requires audio_ref. Audio enhancement.
  - deepfilternet3 (1253+): cloud fal-ai/deepfilternet3, requires audio_ref. Denoise.
- None is text-to-SFX. The catalog has no ElevenLabs or sound-effects text model.

## 3. Understanding capability (fact)
- No `understanding` pack in astrid/packs (packs: _core, developer, generation, h3_av, local, rendering, runpod, setup, timeline, training, vibecomfy, wan2gp).
- config/astrid-beta-capabilities.json:1102-1165: five rows with external_pack "understanding" (audio_understand 1102, scene_describe 1117, understand 1132, video_understand 1147, visual_understand 1162). Disposition "optional"; evidence_reason "Moved to poms_packs; install with `astrid packs add understanding`". audio_understand requires OPENAI_API_KEY.
- Gate: executor/registry.py:139-158 marks an executor unavailable when a dependency namespace is not installed ("requires pack ... (install from poms_packs)").
- training/pack.yaml:122, 185, 314-315 and training dataset_build caption_providers/understanding.py depend on understanding.* ids.
- Installed-stack gate: the external pack is not installed (FRICTION.md item 4).

## 4. GitHub (banodoco org, issues incl. PRs; raw JSON in tooling/gh/sfx-*.json)
(a) generate_audio FAL_KEY not in secrets_required: EXISTS. banodoco/astrid-dev #1254 "bug: generate_audio fails: FAL_KEY is not declared for the action", open, opened 21 Nov, label bug. Reports the same error and "running unledgered"; says the code cause is Unverified. Our code read above adds detail (action-level `secrets:` key, not secrets_required). Nothing in the search matched a fix.
(b) no text-to-SFX mode: NO dedicated issue found. Related: #344 (banodoco/astrid-agent, closed 12 Nov): catalog lava-sr/deepfilternet3 audio_ref not typed; #626 (open, 12 Nov): foley sfx test fails "No ready local audio model supports mode 'sfx'"; #610 (open): param maps declared twice (mentions hunyuan-foley-local sfx).
(c) no understanding/listening capability on an installed stack: PARTIAL. #799 (open, 17 Nov) notes skill/catalog tests expect packs `media` and `understanding`, which are not in astrid/packs. No issue on "listening" as a user-facing gap. "listen" hits are unrelated (#724, #167, #796).
(d) failure output buries the useful line / misleading "running unledgered" banner: PARTIAL. #1254 mentions the banner. No issue on repeated tracebacks found (search "traceback" returned unrelated Windows/Dough/Steerable-Motion items).
(e) synced astrid skill hard-codes a specific install's python path: EXISTS. banodoco/astrid-dev #1234 (open, 21 Nov) "skill points at an old client; error suggests a reinstall" (`<checkout>/.venv/bin/python -m astrid` from an older checkout). Release/14/main's _core SKILL.md uses the run-astrid launcher (astrid/packs/_core/docs/SKILL.md:20-21, 108-110) rather than a venv path. Related: #758 (running from source undiscoverable), #799 (Runtime start message).
(f) no run-astrid python (SDK script in install's own python): NO issue found. Searches "run-astrid python", "SDK launcher", "run-astrid" (37 hits) returned no matching request. #758 is the nearest (running from source). Launcher source not found in release/14/main beyond shell/python snippets; no `python` subcommand found in the search.

Other GitHub hits noted: #1266 (Whisper transcription fixed in Release 14), #1385 (prove installed Whisper on Windows) relate to transcription, not understanding.
