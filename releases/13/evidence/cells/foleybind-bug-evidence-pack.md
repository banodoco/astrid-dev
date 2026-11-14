# Foley catalog binding investigation

Result: requires an upstream VibeComfy public-input change. No product files changed and no commit created. Agent remains clean on r13/foley-binding at 5fb5f13a5e47ac15784b865ad5d320b327bbd97b. VibeComfy /home/user/vibecomfy was read-only throughout. Its working HEAD is b3f20f33f2ea72e3d1dd491382e6a8754a9f2a57, so all installed CLI probes used a separate verified checkout at the actual Agent pin 46251c8cc5565e555356e74e3179223a40f978f7.

## What differs

There is exactly one local catalog row for audio/hunyuan_video_foley: hunyuan-foley-local, astrid/core/model_catalog/models.yaml:1171-1185. The similarly named hunyuan-video-foley is a separate hosted cloud endpoint (:1151-1165). sound-effects is a test-slot label (tests/core/generation/test_cli_gold_075b.py:114), not a catalog ID. The pack default is the ready-template ID audio/hunyuan_video_foley (astrid/packs/generation/extensions/generation.defaults/builtin.yaml:14). entries.py:119-124,163-170 projects its registry_id association with hunyuan-foley-local; that projection is not another authoritative catalog declaration.

Two differences explain the evidence:

1. **Agent revision:** gold-followup.txt describes 562d753d6. At that revision, SDK generation.py:1615-1624 redirects a selected workflow with registry_id through _prepare_catalog_target_workflow. An attached auto request consequently entered the same catalog binder as the explicit catalog ID. Commit 946e405c168320f06dc04fa91d363e20290e525c, already in the assigned 5fb5f13a5 base, removes this redirect. Current auto selection uses the workflow's own preparation (generation.py:1489-1494,1647-1649) and target_schema (entries.py:998-1048). It does not call _bind_target_model_roles.
2. **Placement:** an explicit catalog selection uses generation.py:1476-1482,1602-1606 -> _prepare_catalog_target_workflow :657-670 -> VibeComfyBackend.prepare_catalog_workflow, vibecomfy.py:493 onward. For attached placement, a target client exists (:1555), resolve_target=True (:668), a resolution plan is captured (backend :510-528), and :571-572 calls _bind_target_model_roles (:215-228). The missing public diffusion_model endpoint raises the observed error. RunPod placement instead sets target_client=None (SDK :1555) and defer_target=True (:1606), leaving backend plan=None (:509-510). The binder conditional is not entered (:571-572).

## Why the real pod passed

/home/user/astrid-dev/releases/13/cells-log.md:259-261 records Agent 941449eaf with VibeComfy f3bb6f27, SFX success in 23m48s. At that Agent revision, scripts/live_cells.json:3 selects hunyuan-foley-local. The same remote placement deferral exists at historical SDK :1553-1557,1602-1606,667-670 and backend :509-510,571-572. The SDK ships the frozen workflow at :1813-1829. The pod's local_job.py:200-216 validates public inputs and resolves the catalog name to its template; :222-229 explicitly preserves the prepared graph instead of rebuilding/rebinding it. local_server_engine.py:213-218 compiles the bundle against target schema, without invoking the Agent catalog role binder.

Thus explicit entry selection has no exemption from the binder. Remote preparation never exercised it; attached explicit preparation does. The live pass proves the graph/default weights can run, not that its catalog public-picker interface is valid. A read-only git diff f3bb6f27 46251c8c -- ready_templates/audio/hunyuan_video_foley* is empty.

## Which declaration is invalid, and the root repair

The only invalid local catalog interface is hunyuan-foley-local.model_roles (:1183-1185): it refers to public diffusion_model and vae inputs absent from the pinned template. Commit c4b01ec2b562192d9d28af5fbaa88feba58d04fc switched its template from audio/hunyuan_foley_v2a to audio/hunyuan_video_foley while retaining these role declarations. The loader class and widget targets are correct; the public template API is incomplete for that contract.

The complete fix belongs in VibeComfy ready_templates/audio/hunyuan_video_foley.py:34: declare two optional public picker InputSpecs there, using the existing FOLEY_CHECKPOINT_NAME and VAE_NAME constants. Agent's existing catalog bindings then reference that public authority. Do not create another row, infer node targets in the binder, or special-case SFX. Merely removing model_roles is not a complete catalog repair: comfy_target.py:665-666 deliberately rejects catalog role resolution without roles (catalog_roles failure).

Exact proposed diff: /home/user/cells/evidence/foleybind-template.diff. It adds only:

- diffusion_model -> hunyuanfoleymodelloader.foley_checkpoint_name (HunyuanFoleyModelLoader, node 11), optional COMBO, default FOLEY_CHECKPOINT_NAME.
- vae -> loaddachunyuanvae.vae_name (LoadDACHunyuanVAE, node 12), optional COMBO, default VAE_NAME.

The patch was syntax-checked in memory and git apply --check passed against the verified pinned checkout. It was not applied or runtime-tested. The upstream owner must preserve canonical companion/index consistency using the repository's template editing workflow; any regenerated template bytes determine the final pin hash.

## Exact Agent pin consequences

After the upstream commit exists, use the existing pin updater against that full 40-character revision and its checkout:

    python scripts/vibecomfy_pin.py <upstream-commit> --checkout <upstream-checkout>

It must update these seven Agent files through the existing digest chain:

1. astrid/packs/runpod/pins.json: sources.vibecomfy.revision.
2. astrid/packs/vibecomfy/pins.json: sources.vibecomfy.revision.
3. astrid/packs/runpod/recipe.linux-cu130.json: pins.sha256 for packs/runpod/pins.json.
4. astrid/packs/vibecomfy/recipe.windows-cu130.json: pins.sha256 for packs/runpod/pins.json.
5. astrid/packs/vibecomfy/environment.windows-nvidia.json: pins.sha256 for packs/vibecomfy/pins.json.
6. astrid/packs/vibecomfy/extensions/generation.engine/comfyui.yaml: both recipe sha256 digests.
7. astrid/core/model_catalog/models.yaml: hunyuan-foley-local template_hash, currently sha256:d31fc21886192c3c23565d6a54b2d8444e16e7d63948f5c906fdf35db6e7749e. For exactly the supplied two-line diff, the new value is sha256:2ed29a2186a6e6a67019df79a54a0658434839bda6dfc328026c4538fadba7ed. If upstream emission changes other source bytes, compute the actual committed file hash instead. Other catalog hashes change only if their template bytes differ in the chosen upstream commit.

Catalog role mappings, parameter map, filenames, model byte hashes and defaults need no change for this interface repair. There is no source-code revision constant to edit: VIBECOMFY_ENGINE_REVISION derives from the digest-verified recipe. A new upstream SHA and the associated manifest digests cannot be stated before that commit exists. No old revision literals were found in scripts/tests/.github. Hosted install-manifest.json, if used by release, must name that same upstream revision or defer to the packaged pin.

## Installed CLI evidence

Command: bash /home/user/cells/evidence/foleybind-probe.sh
Driver: /home/user/cells/evidence/foleybind-path-probe.py
Raw completed log: /home/user/cells/evidence/foleybind-path-probe.log
Environment setup: /home/user/cells/evidence/foleybind-setup.log

One environment, Python 3.13.18; installed editable Agent at the supplied base; Runtime 6855dfa8df65cf8ae4c002b57134d6505493c17c; VibeComfy 46251c8cc5565e555356e74e3179223a40f978f7; lifecycle 7f0b025e9391baac9f5c2fb7393617ea6fef0704. Each CLI runs from an empty directory with a fresh isolated HOME and only explicit non-secret environment variables. No credentials were read or inherited.

Every generation invocation was python -m astrid generate audio 'Footsteps on gravel.' --mode sfx --input video_ref=<placeholder-video> --placement <target> --dry-run --json, optionally --entry hunyuan-foley-local. RunPod dry-runs additionally used the existing CLI fixture's required declaration flags: --consent paid --max-usd 1 --deadline 2099-01-01T00:00:00Z. These were planning declarations only; no paid operation occurred.

| Placement | Selection | CLI exit | Observed result |
|---|---|---:|---|
| Loopback attached stand-in | auto | 0 | Selects audio/hunyuan_video_foley and prepares successfully |
| Same attached stand-in | explicit hunyuan-foley-local | 2 | catalog role 'foley' does not match its pinned template input |
| runpod --dry-run | auto | 0 | Selects audio/hunyuan_video_foley; host readiness pending |
| runpod --dry-run | explicit hunyuan-foley-local | 0 | Selects catalog entry; host readiness pending; binder deferred |

The stand-in recorded exactly four GET requests, two /system_stats and two /object_info, and zero writes. No task was admitted. The probe initially had an import setup error (tests.core is not an importable package); the completed driver loads the existing helper file using runpy. No product behavior was changed to obtain these results.

No proposed template runtime pass, live generation proof, focused-suite baseline-diff, or zero-regression claim is made. The brief's upstream-change stop branch applies; the Agent-only implementation/test/commit branch was not taken. No tests or assertions were changed. The existing auto failure from gold-followup is already repaired in the supplied base, while the explicit attached defect remains reproduced.

## Follow-up fix card

Owner: VibeComfy. Apply the supplied optional-picker interface change, retain canonical companion/index consistency, prove both role bindings point to the declared loader widgets with unchanged defaults, and commit upstream. Then pin that exact revision through scripts/vibecomfy_pin.py in Agent and run the specified CLI-GOLD/catalog checks plus an explicit attached dry-run regression against the same stand-in. This investigation grants no live generation, paid workload, publication or merge authority.

Cleanup complete: /home/user/wt/foleybind.env removed and verified absent. Agent branch remains clean at the supplied base SHA. Initial free disk: 4.3 GB, above the 1.5 GB requirement.
