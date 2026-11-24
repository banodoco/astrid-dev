# Golden path: run any ComfyUI workflow in Astrid (custom nodes + models)

Report by an Opus subagent (read-only investigation of Astrid Release 15 as installed at /home/user/work/recast/install-8/program/versions/dd02e367bc24, plus ./sam-audio-node). No machine, pod or GPU used; nothing under install-8 changed. The subagent could not write this file itself, so the content was saved here by the main session from its hand-back.

Path prefixes: `A/` = .../dd02e367bc24/a/astrid/ (Astrid source), `V/` = .../py/lib/python3.11/site-packages/vibecomfy/, `N/` = ./sam-audio-node/.
Evidence labels: [code] read in code; [probe] ran VibeComfy's own `import_workflow_bytes` + `draft_entry` on both SAM files, offline on CPU; [inferred] reasoning, not verified.

## 0. TL;DR

1. The audio-mode string bug is real but fixing it does not unblock SAM. [probe] The API file gets a second blocking need, `unknown loader role`: VibeComfy maps any `model_name` field to `diffusion_models` (V/model_assets.py:45), but SAM's `model_name` is a Hugging Face repo id stored under `models/sam_audio/` (N/sam_audio_comfy/runtime.py:37-38, 393-415). `target_schema` refuses on any need with an ambiguity (A/core/generation/entries.py:1205-1207).
2. Behind those blocks, a RunPod dry run would wrongly say "ready". [code+probe] With no target client `target_schema` returns None before any node check (entries.py:1208-1209). `judge_declarations` (A/core/generation/managed_preparation.py:275-306) reads only `requirements.custom_node_refs` and `metadata.model_assets`, both empty for SAM. The `requirements.missing_nodes: [SAMAudioPipelineLoader, SAMAudioTextSeparator]` that VibeComfy records is read by nobody in Astrid's generate path.
3. The plumbing exists; the link between the pieces is missing. Bundles carry `custom_node_refs` (url, commit, class_set, pip_packages; V/workflow.py:118-131, V/custom_node_refs.py:375-434) and `model_assets`. The engine turns them into `extra.nodes`, a managed lock, `nodes restore` and `fetch` (A/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py:150-170, 212-215; managed_preparation.py:74-95, 495-497). Nothing turns a missing class or model into a declaration, asks for consent, and writes it back into the bundle.
4. SAM-specific gaps: (a) VibeComfy's installer never runs `install.py` or reads `requirements.txt` (V/node_packs/_install.py:985-1066); SAM's `install.py` pip-installs three Meta git packages with `--no-deps` (N/install.py:16-20, 36-38). (b) SAM's T5 support model goes to the Hugging Face cache, which Astrid model rows cannot express (N/sam_audio_comfy/runtime.py:461-487).
5. Source of truth: per-workflow lock = the VibeComfy bundle; the known-pack catalog only proposes refs; Astrid `pins.json` stays the baked base image.

## 1. Ingest today: `astrid generate workflow FILE`

Trace (API or UI JSON, `--placement runpod --dry-run`):
- CLI `_workflow_command`; `--replace` and `--no-run` each require `--as-entry` (A/core/generation/cli.py:501-531).
- Facade `generate.workflow(...)` (A/sdk/generation.py:1581-1597); the file is copied to a temp dir (generation.py:175-200, 1599-1604). Source retention only on a real run (1606-1611).
- Describe: `resolve_workflow_inputs` -> `describe_workflow` -> `load_workflow_path`. Any JSON not in `{template_id, bindings}` form goes to `_canonicalize_ui_workflow`, i.e. VibeComfy `import_workflow_bytes`, for API and UI alike; it writes `workflow.py`, `workflow.vibe.json`, `source.json` into a temp dir (conversion #1), then `draft_entry` (entries.py:642-665; A/packs/vibecomfy/production_engine.py:275-401).
- "workflow build" = `workflow_entries.prepare` (conversion #2 plus input binding) (generation.py:2033-2042; entries.py:1033-1043). "entry needs" = `draft_entry` again; it filters the OLD string `'... tts, music, or sfx'`, which no longer matches (generation.py:2047-2055; V/entries.py:110-111).
- "target node list": `target_schema` raises `entry requires review: audio mode is unknown...`, reported as `input_rejected`. The run stops here (entries.py:1205-1207; generation.py:2083-2085).
- Never reached: "workflow emission", "approval compile", `judge_declarations`, `_offline_invocation_preflight` (generation.py:2061-2073, 2152-2183).

Conversion results [probe]:
- API file: SAM inputs keep their names; outputs 2 x SaveAudio; `requirements.missing_nodes` = both SAM classes; `custom_node_refs` = []; `model_assets` = []; needs = audio-mode ambiguity AND "unknown loader role".
- UI example: SAM inputs become positional `widget_0..7` (diagnostic `widget_alias_unresolved`); outputs are PreviewAudio, not SaveAudio; needs = audio mode only.
- Both: `modes` = []; `report.readiness` = conversion_validated / run_readiness not_assessed; diagnostics include `unresolved_runtime_class ... Run 'nodes lookup X' ... then 'nodes install <slug>'`. Astrid discards the import report (production_engine.py:323-345), so VibeComfy's hint never reaches the user.
- Risk: `import_as_entry` never passes a schema (V/entries.py:132), so a saved UI entry with custom nodes stays positional [inferred].

Storage: entries live at `${VIBECOMFY_ENTRIES_DIR:-~/.vibecomfy/entries}/NAME/{entry.json, bundle/{workflow.py, workflow.vibe.json, source.json}}`; `entry.json` has id, kind, modes, bundle, needs, binds, defaults (V/entries.py:45-51, 119-154). `--as-entry --dry-run` previews only; `--as-entry` saves and runs; `--no-run` saves only (cli.py:532-575). `--replace` is broken: `import_as_entry` has no `replace` parameter (V/entries.py:119), so the CLI raises `missing_dependency` (cli.py:548-553); the skill documents it as working (A/packs/generation/docs/SKILL.md:211-213). A saved SAM entry keeps its ambiguity needs and is refused forever unless hand-edited [inferred]. Kept of the original: byte-identical `source.json` (V/porting/import_service.py:65-81), a project media member on real runs, and the generated `workflow.py` (`READY_METADATA.requirements` holds only `missing_nodes`).

## 2. Official ingest path?

None that goes from "JSON" to "runnable entry with packs and models declared".
- `astrid vibecomfy` has no CLI commands. `vibecomfy.import/inspect/edit/validate/run` are Astrid executors (import, inspect, validate marked external-escape-hatch; A/packs/vibecomfy/pack.yaml). Import emits the trio plus `edit-report.json`; it creates no entry and resolves no packs or models.
- Generation skill: `generate workflow FILE --as-entry NAME --dry-run`, then `--no-run`, then `defaults set` (generation SKILL.md:66-75, 207-213).
- VibeComfy skill "Missing nodes and models": attached ComfyUI only and manual: `vibecomfy nodes install SLUG --yes`, `pip install -r custom_nodes/PACK/requirements.txt`, restart, `vibecomfy fetch WORKFLOW`; forbids `prepare`, `run --ensure-*`, `nodes ensure`. Wrong for SAM (requirements.txt holds only light deps; the Meta packages come from install.py).
- VibeComfy offers but Astrid does not expose: `nodes lookup` (Comfy Registry, Manager node map, GitHub search; V/registry/pack_resolver.py:19-22), `nodes install NAME [--repo URL]` (no `--commit`; V/commands/nodes.py:1301-1304), `install-plan`, `coverage`, `restore --lockfile`, `lock`, `fetch`, `validate`, `doctor`, `prepare --deps sync`, `ensure_env` (resolves UI `cnr_id`/`aux_id`/`ver`, V/runtime/ensure_env.py:179-300; useless for SAM, whose nodes carry none: `resolver_kind: unprovenanced`).

## 3. The missing connector

1. Extract node requirements from the JSON. Exists: `requirements.missing_nodes`, `unresolved_runtime_class` diagnostics, `missing_packs_for_workflow` (V/node_packs/_install.py:666-676). Missing: generate never calls these; unknown classes never become a structured ref.
2. Extract model requirements. Exists: `_referenced_model_values`, `LOADER_ROLES`, unresolved records with `url: None` (V/model_assets.py:232-297, 575-597; V/entries.py:20-29). Missing: a way to declare a repo-id loader and its folder; today it yields a false diffusion_models need.
3. Store them. Bundles already have the fields (`WorkflowRequirements{models, custom_nodes, missing_models, missing_nodes, unsupported, runtime, custom_node_refs}`, V/workflow.py:118-131; emission V/porting/convert.py:853-880). Missing: any write-back of the owner's answer; entries cannot be re-emitted; `--replace` is broken.
4. Consume on managed engine and pod. Exists: `workflow_requirements` -> `judge_declarations` -> managed lock -> `nodes restore` / `fetch`. Missing: `install.py` and `requirements.txt` are ignored; no consent gate (`restore_pack` has no `require_confirmation`, _install.py:372-412).
5. Consume on an attached ComfyUI. Exists: `attached_asset_readiness` prints clone/checkout/pip commands (A/core/generation/asset_gaps.py:105-181). Missing: only for catalogued packs; unknown packs get "part of ComfyUI itself; update ComfyUI" (asset_gaps.py:163-167), which is wrong.
6. Consume through local `generate align`. Exists: report plus `--apply --consent user_env` (A/core/generation/asset_alignment.py:521-668). Missing: it refuses saved user entries (asset_alignment.py:365-369).

Gap in one sentence: between `import_workflow_bytes`, which knows what is missing, and `workflow_requirements`, which knows how to install declared refs, nothing resolves, shows, takes consent for and records the refs in the bundle.

## 4. Golden path (proposed)

Reuses the `fetch-models` plan-digest-then-`--apply` shape (asset_gaps.py:438-458) and the readiness envelope `{status, issues, fixes[argv]}` (A/core/generation/preflight.py:90-102). The bundle is the lock. Ingest is the front of the path; `generate` reruns readiness.

(a) SAM, known pack, gated model with a public mirror:
```
$ astrid generate workflow sam-audio-separation.api.json --as-entry sam-separate --project P --placement runpod --dry-run
Imported (API, 5 nodes) as entry sam-separate (audio, mode: separate). Nothing written.
Readiness on runpod: BLOCKED (1 node pack, 3 model files; 0 unknown)
Node packs
  ComfyUI-SAM-Audio  known  https://github.com/ethanfel/ComfyUI-SAM-Audio @ <sha> (MIT)
    provides SAMAudioPipelineLoader, SAMAudioTextSeparator
    install: clone; pip -r requirements.txt (torch protected); pip --no-deps dacvae@414c207, perception-models@e72b681, sam-audio@bb4c699
Models
  sam_audio/sam-audio-large/checkpoint.pt  13.8 GiB  hf mrfakename/sam-audio-large@497809f  sha256 ca55418b...  (public mirror of gated facebook/sam-audio-large; Meta SAM License)
  sam_audio/sam-audio-large/config.json    same revision, sha256 <tbd>
  hf-cache google-t5/t5-base@a9723ea       ~0.9 GB support model
  not needed: span predictor 5.8 GiB (predict_spans=false), Judge 5.7 GiB (reranking=1)
Pod disk ~15 GiB models; ephemeral unless a network volume is attached.
Plan sha256 9c1e...   Approve: astrid generate workflow ... --placement runpod --apply 9c1e...
```
With `--apply`: saves the entry and its lock; on the pod restores the pack at its sha, runs the declared install steps, fetches the verified files, starts ComfyUI, checks `object_info` for the classes, then queues target and residual (48 kHz mono). Second run, no flag: `astrid generate audio --entry sam-separate --mode separate --audio-ref clip.wav --placement runpod` -> `Readiness: ready (locked 1 pack, 3 files; 3/3 on volume)`. Local managed engine: same flow behind `--consent user_env`. Attached ComfyUI: same report but the fixes are commands the user runs with their own Python, then restarts ComfyUI (asset_gaps.py:129-135).

(b) Unknown pack and unknown model, declared by flags:
```
$ astrid generate workflow foo.json --as-entry foo --placement runpod --dry-run
BLOCKED: FooSampler - no known pack. Candidates (unverified; Comfy Registry/Manager map): someone/ComfyUI-Foo
  Declare: --node-pack https://github.com/someone/ComfyUI-Foo@<40-hex>
FooLoader.ckpt = foo_v2.safetensors (checkpoints) - no declared source
  Declare: --model checkpoints/foo_v2.safetensors=https://.../resolve/<rev>/foo_v2.safetensors#sha256=<hex>
$ ... --node-pack ...@1a2b... --model ...#sha256=...
BLOCKED: ComfyUI-Foo user-declared @1a2b... (class list from pinned tree; unverified until object_info);
  requirements.txt will run (torch protected); install.py present - will NOT run without --allow-install-script
Plan sha256 77ab...   Approve: ... --apply 77ab...
```
Flags have the same shape for packs and models. Known items are filled from the catalog; unknown items must carry a commit sha (packs) or a sha256 (models).

## 5. Seams to reuse, and where the two worlds disagree

Reuse: `custom_node_refs` and `model_assets`; `workflow_requirements` -> `extra.nodes`; `judge_declarations`; the managed lock with `nodes restore`/`fetch`; `fetch-models` plan + `--apply` (asset_gaps.py:367-660); `--consent user_env` (cli.py:131; asset_alignment.py:568-570); readiness `fixes[argv]`; `missing_packs_for_workflow`; `pack_resolver` for candidates; torch protection via `_pip_plan_conflict` (_install.py:943-982); `attached_asset_readiness`; the models-lock row `{repository, revision, path, destination, bytes, sha256}` (A/packs/runpod/models.lock.json; engine_contracts.py:676-684).

Two worlds: VibeComfy "known packs" are a class -> pack resolver (23 static packs without commits, V/node_packs/_defs.py:26-453, plus the shipped `custom_nodes.lock`, 16 entries with commits). Astrid `pins.json` holds base-image sources (ComfyUI, VibeComfy, H3, VHS, Foley, QwenTTS, Whisper, lifecycle), wired into the recipe's `source_bindings`. Where they overlap, commits agree, kept in sync by hand [inferred].

Bugs in the known-pack world: the cwd-relative lock default (`get_known_node_packs`, `missing_packs_for_workflow`, `install_pack`, `_pack_by_name` default to `Path("custom_nodes.lock")`: _defs.py:515; _install.py:203-214, 666-667, 839; Astrid repeats it in asset_gaps.py:142), so "known" by default means the 23 static packs with no commits; the shipped lock contains an `ExamplePack` test fixture (V/custom_nodes.lock:175-181); the brief's "none audio-related" was wrong (Whisper, MelBandRoformer, comfy_mtb audio, Qwen TTS, Foley are there; none is SAM).

Recommendation: (1) per-workflow truth = the bundle (refs with url, commit, class_set, install recipe, schema hash; model rows with digest and size); (2) the catalog only proposes refs and should be commit-pinned lock entries only; (3) `pins.json` stays the baked base; a ref matching a baked pin means "already on the image"; generate one file from the other in CI.

## 6. Change list, in order (S < 1 day, M = a few days, L = a week or more)

0. Audio-mode filter (astrid-agent, S): A/sdk/generation.py:2052-2053; A/core/generation/cli.py:570-571. Filter on a machine code on the need (e.g. `code: audio_mode_unknown`) instead of the exact sentence; stopgap: match the prefix. Add a test that uses VibeComfy's real string.
0b. Loader-role need and audio mode (vibecomfy + astrid, S-M): V/entries.py:20-29, 57, 107-115; V/model_assets.py:45; A/core/generation/cli.py:47. (i) a bare `model_name` on an unknown class becomes a readiness item, not a blocking ambiguity, and is not called diffusion_models; (ii) add an audio mode `separate`, or let raw mode `workflow` reach `generate audio`.
1. Report missing nodes on every placement (astrid, M): production_engine.py:275-349; generation.py ~2047-2057. Keep the import report; turn `missing_nodes` and `unresolved_runtime_class` into `missing_node_pack` issues (known or unknown) on every placement, including pod dry runs.
2. Fix the known-pack catalog (vibecomfy, S): _defs.py:471-547; _install.py:203-214, 558-570, 666-676, 838-839; A/core/generation/asset_gaps.py:142. Fix the cwd-relative lock default, drop `ExamplePack`, add a SAM-Audio lock entry with url, commit, class_set and install recipe.
3. Install recipe on lock entries and refs (vibecomfy, M): _lockfile.py:37-54; _install.py:372-412, 985-1066; custom_node_refs.py. Add `requirements_txt`, `pip_packages`, `pip_no_deps` (pinned git/url) and `install_script {path, sha256}` (opt-in); run all of it under the dry-run/torch-protection preflight; `restore_pack` should use the lock entry's own pip packages (today an unknown pack restored from a lock gets no Python dependencies).
4. Richer model declarations (vibecomfy, M): model_assets.py; workflow.py; commands/fetch.py. HF repo/revision/path, `destination` (directory rows allowed), `cache: models|hf_cache`, `gated`, `license`, mirror `fallback`; let an unknown class's loader declare its folder.
5. Plan, flags and write-back (astrid, L): cli.py:299-316, 501-575; new A/core/generation/workflow_readiness.py; asset_gaps.py. `generate workflow --dry-run` prints the plan with a sha256; flags `--node-pack URL@SHA`, `--model DEST=URL#sha256` (repeatable), `--apply PLAN_SHA256`, `--allow-install-script`; on `--apply` re-emit the entry bundle with refs and model rows and clear the ambiguity needs.
6. Entry replace and schema (vibecomfy, M): V/entries.py:119-154. `import_as_entry(..., replace, schema_provider, requirements)` fixes `--replace`; after install, re-convert UI JSON against the live schema.
7. Pod enforcement (astrid, M): managed_preparation.py:74-95, 264-267, 275-306, 480-510; comfyui_engine.py:105-133, 157-182. Let `extra.nodes` carry the install recipe (today anything but `{repo, commit}` is refused); require the approved plan digest before restoring or fetching anything not in the catalog or the baked pins; verify `object_info` after restore.
8. Align for saved entries (astrid, S): asset_alignment.py:351-420.
9. Attached ComfyUI report (astrid, S): asset_gaps.py:129-181. Declared unknown packs get clone/checkout/recipe commands; stop saying "part of ComfyUI itself".
10. Disk and cache (runpod pack / lifecycle, M): A/packs/runpod/adapter.py:108-176; storage_probe.py. Recommend a network volume above ~10 GiB of models, put `HF_HOME` on the volume, report cache hit or miss.
11. Docs (S): vibecomfy SKILL "Missing nodes and models"; generation SKILL.md:207-213. One golden-path section; fix the requirements.txt and `--replace` claims.

Order: 0/0b -> 1/2 (honest report) -> 3/4 (packs and models fully declarable) -> 5/6 (UX + lock) -> 7 (pod enforcement) -> 8-11.

## 7. Design questions and risks

- Declaring an unknown pack: only `repo@<40-hex>`; branches and tags resolved to a sha once, in the plan. `install_pack` already supports `checkout_ref` + `expected_commit` (_install.py:203-218, 909-940). The class list from the tree is a guess [inferred]; verify through `object_info` and record `class_schema_sha256`.
- `install.py` is arbitrary code: off by default, allowed only with `--allow-install-script`, with the script's sha in the plan. SAM's `install.py` can be expressed declaratively (`-r requirements.txt` + three `--no-deps` pins), so its catalog entry needs no script. Only torch is protected (_install.py:943-955); SAM may upgrade `transformers` to >=4.54, which could break other packs [inferred].
- Rented-pod security: a cloned pack runs with whatever the pod holds [inferred; pod credentials not inspected]. Today the managed lock is built straight from the workflow's declarations with no gate (managed_preparation.py:495-497; `restore_pack` has no gate), so a workflow from a stranger could clone code onto the pod unprompted [inferred, not exercised]. Item 7 fixes this. Approval should cover the digest of `{repo, commit, recipe, script sha}`; pods have no egress rules, so pinning, digests and consent are the whole defence.
- Gated and large models: each model row needs url or repo@rev, path, destination, bytes, sha256, gated, license, optional fallback. SAM's node already pins the mirror's revision, size and sha (N/sam_audio_comfy/runtime.py:63-100); if Astrid pre-places `models/sam_audio/sam-audio-large/{config.json,checkpoint.pt}` the node uses it as is (runtime.py:337-345, 403-415). Astrid's downloader has no token or gating handling (no matches in A/core/generation/model_downloader.py), so prefer mirrors. Sizes: SAM-large checkpoint 14,861,356,211 B (13.8 GiB); T5 about 0.9 GB [inferred]; span predictor 5.8 GiB and Judge 5.7 GiB only when enabled; total for this graph about 15 GiB. Ephemeral pod disk means paying the download on every claim; a network volume fixes that.
- Where the lock lives: in the saved entry's bundle. `generate workflow FILE --apply` without `--as-entry` should refuse ("save as an entry to keep the lock").
- Local targets: managed engine same as the pod behind `--consent user_env`; attached ComfyUI: Astrid prints commands only (asset_gaps.py:129-135; local_server_engine.py:578-585).

## 8. Smallest first slice

Items 0, 0b(i), 1, 2 (with the SAM catalog entry), 3 (declarative `pip_no_deps` only), and SAM's model rows from item 4. Persist via `--as-entry`; no new flags yet.

Free checks on CPU: (1) a test that repeats the probe: the needs on both SAM files no longer block; (2) `generate workflow sam.api.json --placement runpod --dry-run --json`: without a lock `blocked`, listing the SAM pack and three model rows plus `fixes`; with a lock `ready`, and `readiness.entry.requirements.extra.nodes` includes SAM (dry runs already run `judge_declarations`, generation.py:2152-2178); (3) `install_required_packs` against a temp tree with a fake runner to check the order (clone, checkout, pip -r, then --no-deps x3), then a real throwaway venv (pip resolution is CPU-only [inferred]); (4) the SAM node's own tests (N/tests) with a pre-placed model folder.

One short pod claim: the ~14 GiB fetch; ComfyUI start with the classes in `object_info`; one 10-second clip end to end, on a network volume so later runs cost only GPU time.

## 9. Conflicts with the owner's description and the brief

Owner's description vs today's Astrid: "generate X": an audio entry needs `--mode` from music, tts, sfx or transcribe (cli.py:47, 252-253; V/entries.py:57) and `--audio-ref` is the transcription input (cli.py:266-268), so separation has no mode. "Shows the install command": on an attached ComfyUI Astrid only prints commands and the user restarts ComfyUI. "Works for unknown packs": unknown packs also need a dependency recipe; today the installer only clones and pip-installs the catalog's `pip_packages`.

Brief vs code: "known packs prepare an environment": only through cm-cli or clone + catalog `pip_packages`, and by default without the shipped lock; "`--mode sfx` doesn't clear it": correct, the need comes from VibeComfy; "the string fix makes it run": no, the loader-role need blocks next, then the false "ready" on a pod dry run; "SaveAudio on both outputs": true only for the API file, the UI example uses PreviewAudio and converts to positional `widget_N`; "local_server_engine tells the user to install and restart ComfyUI themselves": confirmed (local_server_engine.py:176-205, 578-583).

## 10. Not verified

Ticket #1731 (not read by the subagent); whether `_offline_invocation_preflight` (generation.py:318-) refuses unknown classes on a pod dry run (likely not); the pod-side cwd for `nodes restore`; `config.json` and T5 digests and sizes; whether the pack is listed on Comfy Registry; the flag spellings in section 4 are a proposal. Probe scripts: /tmp/claude-0/-home-user/147d9c2d-d162-594a-abc0-e50a18b46d5e/scratchpad/scripts/probe.py and probe2.py.
