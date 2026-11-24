# Repair routes for a retired `file` locator in a timeline registry

Root: `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293/` (paths below relative to `a/` unless marked `r/`). Read-only; only grep and read were run, no CLI commands.

## Where the rejection happens

- `astrid/packs/rendering/actions/render/managed_timeline.py:630` forbids `("url", "file", "path", "source_path", "locator", "realm")` in each registry entry; raises `managed_media_locator` at :633-637 ("Import the bytes into the runtime and reference its object_id/digest").
- Called from `resolve_managed_render_snapshot` at :1146-1155: `_render_compatible_projection` (:45) runs first, then `_runtime_snapshot_registry` (:584).
- `_render_compatible_projection` (:45-70) strips only `EDITOR_ASSET_METADATA_KEYS` (`astrid/core/timeline/banodoco_schema.py:426`: `handle, filename, pixel_provenance, source, size, size_bytes`), `media_type`, and rewrites `origin: managed-local` to `opaque-foreign`. It does NOT strip `file` or `url`. The schema comment says "Retired locators (file/url/path) are not here".
- Other retired-locator checks, which disagree with each other: `astrid/core/rendering/assets.py:264-275` (`file` allowed only with `allow_derived_files`); `astrid/core/execution/generic_host.py:564` (`_MANAGED_ASSET_LOCATOR_KEYS` includes `file`, `uri`); `astrid/core/timeline/resolution.py:19,136`. `astrid/core/timeline/validators/registry.py` `_ASSET_ENTRY_ALLOWED` (~line 40) still lists `"file"`.

## 1. Removal and replacement verbs

No CLI or SDK verb removes a single registry asset key. The native command vocabulary (`clip.*`, `media.*`, `timeline.*`, `parent.after-clip`) has no asset-delete command. Registry changes happen only as side effects of clip or media commands.

| Route | Effect on the registry entry | Needs unreferenced? | Undoable revision? |
|---|---|---|---|
| `timelines edit REF --clip ADDR --swap-asset KEY=HANDLE` (`core/cli/domain_timelines.py:476`) | Adds or rebinds one clip's key via `sdk/timeline/edits.py:709` `_register_asset`. `replace=False` refuses an existing key | n/a | yes (commit) |
| `timelines edit REF --replace-asset KEY=HANDLE` (`domain_timelines.py:480`) → `sdk/timeline/model.py` `Timeline.replace_asset(key, asset)` | Rewrites the entry in every shot registry holding KEY (`_register_asset(sid, {"key": key, **new_entry}, replace=True)`). `new_entry` is built only from `media_id, content_sha256, type, resolution, size, size_bytes` plus `source`, so `file` is dropped by construction | Refuses if no clip uses the key ("no clips use asset key") | yes |
| `timelines edit REF --clip ADDR --clear-asset` (`domain_timelines.py:518`) → `sdk/timeline/native_checkout.py:416` `clear_asset` (`clip.set` clearing `asset`) | Clears the clip's asset only; the registry entry stays | n/a | yes |
| `timelines undo REF --commit` / `redo` (`domain_timelines.py:624`; `--dry-run` previews) | Reverses an accepted commit | n/a | itself a revision |

`timelines assets REF [KEY]` (`domain_timelines.py:189`) is read-only.

## 2. Does clip removal prune the registry?

No. Native `clip.delete`: `sdk/timeline/_delete_commands.py` `delete()` ends with `ctx.clear(ref, [])` (clip row only). `_unreferenced()` refuses only declared relations (`RELATIONS`, transition, pinnedShotGroups) and never touches `asset:` entries. Legacy `sdk/timeline/model.py:812` `Clip.remove()` does `clips[:] = ...` with no registry change. `sdk/timeline/capture.py:264` `capture_clip_delete` wraps the same native command.

## 3. Normalization and migration of locator fields

- Commit path: no stripping found in `sdk/timeline/commit*.py`. `_commit_patch.py:157` maps `parent/asset:KEY` to `['config','registry','assets',KEY]`.
- `sdk/timeline/_command_state.py:562` pops `registry.assets` only when the whole container is absent (inverse of creation), not per key.
- `core/timeline/authoring_feedback_residual.py:148` pops `config.registry.assets` only when it equals the effective parent assets.
- `core/timeline/expand_shots.py:89` still reads `entry.get("file")` (legacy path).
- `sdk/timeline/native_timeline_duplicate.py:142-160` `adopt_parent_assets` copies only referenced parent aliases into a duplicate's child registry, verbatim, so `file` would be copied if referenced.

## 4. Direct registry edit in a commit callback

- `Timeline.assets(key=None)` (`sdk/timeline/edits.py:585`) is read-only. There is no `t.asset(key)` setter.
- The write surface is `Timeline.replace_asset(key: str, asset: Any) -> list[str]` (`model.py`, around line 194), used inside a commit callback:

```python
tl = Timeline.open("PROJECT", "TIMELINE")   # sdk/timeline/commit_session.py:1099
def fix(t):
    t.replace_asset("HERO", "sha256:<64-hex>")  # handle must be a project media handle (run:, task:, ref:, sha256:)
tl.commit(fix, label="Repair HERO registry locator", dry_run=True)  # commit_session.py:603; drop dry_run to publish
```

- `dry_run` is a parameter of `commit(...)` (commit_session.py:603) and of the CLI `timelines commit --dry-run` and `timelines edit --dry-run`.
- Caveats: the key must be used by at least one clip, and the replacement kind must match (video/audio/image).
- Unverified: whether `Timeline.open` is exported from the package `__init__`; I did not check.

## 5. Existing tests

`a/tests/packs/rendering/test_managed_timeline_render.py`:
- `:521 test_retired_locator_is_rejected_before_runtime_materialization` puts `{"file": "/tmp/hero.mp4", "media_id": "media-1"}` into `runtime.timeline["registry"]` and expects `ManagedRenderValidationError` matching "retired media locator".
- `:612 test_snapshot_validation_rejects_missing_registry_asset` shows the config-clip pattern.
- Helpers: `_Runtime` (:68); `_snapshot(runtime)` (:163) calls `resolve_managed_render_snapshot(project_ref="demo", timeline_ref="main", client=runtime)`.

Other locator tests:
- `a/tests/core/rendering/test_assets.py:116` `test_registry_rejects_retired_locators_and_requires_runtime_identity`
- `a/tests/packs/rendering/test_render_registry_editor_metadata.py:28` `test_retired_locators_and_unknown_keys_still_fail` (its `path` case fails on "unknown key" in `validate_registry`, not on the locator message)

Tests that monkeypatch `_runtime_snapshot_registry`: `a/tests/sdk/test_capture_closure_source.py:49`, `a/tests/packs/rendering/test_scene_source_carry.py:120`, `a/tests/sdk/test_timeline_filmstrip.py:402`.

`r/tests`: the grep hits were generic words. No dedicated `_runtime_snapshot_registry` test was found there.

Run: `Makefile:79` `test: $(PY) -m pytest -q`. From `a/`: `python -m pytest -q tests/packs/rendering/test_managed_timeline_render.py -k retired_locator`. `pyproject.toml:278` configures `[tool.pytest.ini_options]`, with a 120s per-test timeout at :288-300. `r/pyproject.toml:19` has the same section. Not run.

## Recommended route (for the main thread to decide)

1. Repoint the affected clip(s) with `timelines edit REF --replace-asset KEY=HANDLE --dry-run`, then apply. This rewrites the entry without `file` and is undoable with `timelines undo`.
2. If the key is orphaned (no clip uses it), there is no public removal verb. The options are to bind a clip to it via replace, or to rebuild the timeline. Both need the main thread's decision.
