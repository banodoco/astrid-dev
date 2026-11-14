# Offline managed i2v catalog evidence

Inspected the already-fetched VibeComfy checkout at revision `46251c8cc5565e555356e74e3179223a40f978f7` (`/home/user/wt/engrows.env/vibecomfy`). No network was used, no model weights were opened or downloaded, and no repository files were changed.

## Declaration and missing identity

The affected checkpoint identifier is `ltx-2.3-22b-dev.safetensors`. Its VibeComfy ready-template requirement has no exact digest or exact byte count. The source URL is `https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-dev-fp8.safetensors`.

Excerpt from `ready_templates/video/ltx2_3_i2v.py:45-49`:

```python
requirements={'models': [{'name': 'ltx-2.3-22b-dev.safetensors',
         'subdir': 'checkpoints',
         'url': 'https://huggingface.co/Lightricks/LTX-2.3-fp8/resolve/main/ltx-2.3-22b-dev-fp8.safetensors',
         'sha256': None,
         'size_bytes': None},
```

The same ready-template file repeats the source artifact at line 55, again with `sha256: None` and `size_bytes: None`.

## Ownership

The ready-template `requirements.models` records are the declaration home for this explicitly URL-backed workflow asset. `docs/templates/adding_templates_models.md:148-154` assigns embedded model URLs to workflow metadata or ready-template requirements; it assigns `vibecomfy/registry/models.yaml` the separate role of node-pack-specific layouts and staging.

The registry row at `vibecomfy/registry/models.yaml:257-268` provides source repo/file, a minimum-size threshold, target location, and alias, but no exact SHA-256 or exact size:

```yaml
  - id: ltx_2_3_22b_dev_fp8
    source:
      kind: huggingface
      repo: Lightricks/LTX-2.3-fp8
      filename: ltx-2.3-22b-dev-fp8.safetensors
    min_size: 20_000_000_000
    targets:
      - node_pack: ltx
        path: checkpoints/ltx-2.3-22b-dev-fp8.safetensors
    aliases:
      - ltx-2.3-22b-dev.safetensors
```

The registry supports optional exact pins (`vibecomfy/registry/models_loader.py:60-80,371-389`), and registry fallback resolution copies them into inferred asset records (`vibecomfy/model_assets.py:436-465`). This ready template instead supplies explicit requirement records at `ready_templates/video/ltx2_3_i2v.py:42-56`; VibeComfy preserves those authored records through build (`vibecomfy/templates.py:1317-1355,1607-1710`) and reconciliation retains matching authored entries (`vibecomfy/model_assets.py:394-429`). Updating only the registry therefore does not populate the two null fields in the explicit template requirement witness.

The ready policy copies these requirements into `workflow.metadata['model_assets']` through `_merge_requirements` / `_append_model_asset` (`vibecomfy/registry/ready_template.py:165-207`). Astrid consumes those asset records at `astrid/packs/vibecomfy/extensions/generation.engine/comfyui_engine.py:145-174`; its fallback model-lock lookup cannot supply this artifact's identity because the Agent declarations contain no matching checkpoint row. The fail-closed judge was introduced by `731c27b0db1c08e7a6f31280d02e7f8e9ed8c5e2` and checks both digest and size at `astrid/core/generation/managed_preparation.py:277-280`.

## Offline limit

The inspected pinned declarations provide neither exact `sha256` nor exact `size_bytes`. The registry's `min_size` is only a lower bound. The pinned repository has no checked-in model weight or matching LFS pointer to hash/stat. Exact values require authoritative upstream metadata or the exact artifact bytes from a trusted source.
