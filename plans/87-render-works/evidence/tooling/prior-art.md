# Prior art: "canonical registry asset '...' contains retired media locator field(s): file"

Read-only research. No repo modified; only `git log`, `git branch`, `git ls-tree`, `git blame`, `git show`, greps.
Labels: [fact] = read or run; [inference] = my reasoning.

## 1. Git history

Repos checked (common git dirs): `~/Developer/astrid-release-src/agent-src`, `runtime-src`, `astrid-app`, `~/Developer/astrid-dev`, `~/Developer/astrid-pinokio`. Worktrees (`wt-*`, `*-plan18*`, `runtime-commit-cost`, etc.) share these object stores, so `--all` covers them. `~/Developer/astrid-video` and `astrid-site-journey` are not git repos under `.git` at the top level; not searched further.

- [fact] `git log --all -S "retired media locator"` in agent-src returns `708b9c0f6`, `e080c1dc7`, `5b8381d39` (archive commit, 2026-11-03, not a real change). runtime-src, astrid-app, astrid-dev, astrid-pinokio: no hits.
- [fact] Introducing commit: **708b9c0f6, 2026-08-31, POM ([email redacted]), "cut over live media to runtime-managed objects"**. It is an ancestor of `origin/main` (`git merge-base --is-ancestor` true) and of `release/14/*` branches. `git blame` on origin/main line 630 of the file attributes it to this commit. Same commit adds the `("url", "file", "path", "source_path", "locator", "realm")` tuple.
- [fact] Companion commit `e080c1dc7` (2026-08-31, "adapt supported rendering and reshape tests to runtime boundary") also in origin/main.
- [fact] Path history: the file was renamed `packs/rendering/executors/render/managed_timeline.py` -> `packs/rendering/actions/render/managed_timeline.py` in **71d43e003** ("Preserve validated A23 combined integration before latest review merge", R098). Release/14 branches all carry the `actions/` path. [inference] The later rename does not change the check's content.
- [fact] `--grep=locator` / `--grep=retired` hits are mostly unrelated (e.g. `ca8c9cd20`, `3255421b9 fix(timeline): apply Rendering v5 locator correction`, `0fac4b9f3 Render: editor metadata on registry entries never reaches the strict schema`, `7c8aefcd0 chore: hard-break cleanup of retired paths`). `0fac4b9f3` is the closest in topic (registry strict schema) and is worth reading. No commit in any repo mentions issue numbers 1238, 748 or 1253 in its message.
- [fact] `-S "RETIRED"` restricted to `*managed_timeline*` / `*registry*` returns nothing.

Branches whose names match locator/registry/visualize/retired/media/1238/748/1253 (local + remote, agent-src), with `in origin/main` status:
- not in origin/main: `release/14/media-association`, `origin/release/14/media-association`, `origin/p59/media-crop`, `origin/p59/media-hold`, `origin/p59/media-ids`, `origin/p59/media-mask`, `origin/p59/visualize-readable`, `origin/codex/handover-timeline-r4-20261019-wip-sdk-d-registry`
- in origin/main: `origin/plan32/h3-blank-media`, `origin/r13/machines-medialist`
- [fact] `release/14/*` branches containing 708b9c0f6: commit-loads, legacy-basis, legacy-probes, media-association, oracle-freeze, plan-59, plan-66-wip/*, plan-69 (installed version's line), runtime-pin-66, runtime-pin-d725811; also `merge/main-into-plan-59-20261118`, `merge/r14-main-into-p59-agent(-2)`.
- [fact] `origin/main` in agent-src = 959da7326.

## 2. Where the check lives and its callers (installed tree)

Installed root: `~/astrid-release/release-14-plan-69/program/versions/5bf20639e293`

- Check: `a/astrid/packs/rendering/actions/render/managed_timeline.py:630-638`. The field tuple is **inline**, not a named constant: `("url", "file", "path", "source_path", "locator", "realm")`. Raised as `ManagedRenderValidationError`, `validator="managed_media_locator"`. Enclosing function: `_runtime_snapshot_registry` (line 584).
- Sibling checks, which differ in field lists:
  - `a/astrid/core/rendering/assets.py:267-276` (`ValueError`, same message text). Lists `url, sourceUrl, remoteUrl, thumbnailUrl, thumbnail_url, path, source_path, locator, realm`. Rejects `file` only if `not self.allow_derived_files` (line 271). The constructor flag at 161/170 is set `True` by ffmpeg `support.py:969` and `remotion/root_preparation.py:279` (`materialized_root is not None`) and `remotion/run.py:1574`, `threejs/run.py:368`.
  - `a/astrid/core/timeline/resolution.py:136` (returns `unsupported`, message "media locators are retired", no `file`).
  - `a/astrid/core/execution/generic_host.py:564` `_MANAGED_ASSET_LOCATOR_KEYS` includes `file`.
  - Runtime: `r/runtime_protocol/store.py:2490-2505` includes `file` in its list but exempts it when it is a same-origin object route `/v1/objects/<id>` matching the media_id. Runtime test `r/tests/test_canonical_render_admission.py:383` parametrizes `url, uri, sourceUrl, remoteUrl, path, source_path, locator, realm` (no `file`).
- Callers of `_runtime_snapshot_registry`:
  - `managed_timeline.py:1151` (snapshot builder; `stored_registry` comes from the Runtime timeline read after `_render_compatible_projection`)
  - `a/astrid/sdk/invocation.py:1485` (expanded registry for shot occurrences)
  - `a/astrid/sdk/authoring_render_preview.py:170`
  - `a/astrid/sdk/timeline_filmstrip.py:867`
- Tests that pin the message: `a/tests/packs/rendering/test_managed_timeline_render.py:519-525` (`file: /tmp/hero.mp4` expects "retired media locator"); `a/tests/core/rendering/test_assets.py:119`.
- [fact] Introducing commit for the check: `708b9c0f6` (above). Its diff adds the message and tuple (lines +111..+114 of the commit diff, with `"file"` in the tuple).

## 3. Who writes a `file` key into a registry (writers / importers)

Python (installed tree):
- `a/astrid/core/execution/generic_host.py:9336`: `entry["file"] = str(destination)` in a "derived" registry built from `fetch_object` (attempt-local materialization, child-process side, around 9322-9340).
- `a/astrid/core/rendering/assets.py:330`: `entry["file"] = asset.local_url` in the render-time registry clone (`materialized` path, line ~318-332).
- `a/astrid/packs/rendering/actions/render/task_adapter.py:385`: `asset["file"] = str(destination)` on a private copy of `assets.json` for the renderer.
- `a/astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py:125`: writes `render_source.file` on a clip audio object (not the registry).
- `r/runtime_protocol/asset_identity.py:45` reads `file` into identity fields (does not write the registry).
- `a/astrid/core/rendering/fixtures/renderer_parity/assets.json` and `remotion_backend_wrapper.py:53`: fixtures.

[inference] The Python writers above all operate on derived/attempt-local copies after the canonical snapshot is taken. The check in managed_timeline runs on the canonical stored registry, so these writers would not trip it unless their output is fed back in as canonical. I did not find such a feed-back path in the installed tree.

Editor (TypeScript), `~/astrid-release/release-14-plan-69/editor/src/tools/travel-between-images/`:
- `components/shotTimelineDataProvider.ts:393, 1216, 1304, 1632, 1832`: `file: entry.file ?? entry.media_id ?? entry.url` on registry copies. When the entry has no `file`, this sets `file` to the bare `media_id` (not a route). [fact for the code; inference for the effect]
- `pages/localTimelineShotModel.ts:199`: `file: canonicalAsset.object_id` on a synthesized canonical asset entry. [fact]
- Tests `components/shotTimelineDataProvider.a3.test.ts:195, 217, 323, 457, 496, 558` assert `file` is present on registry entries. [fact]
- Git history (astrid-app repo): earliest `file: canonicalAsset.object_id` is `00094410b` (2026-09-19, "Wire canonical shot composition through Runtime"; not on origin/main). Earliest `entry.file ?? entry.media_id ?? entry.url` is `1315fe2ed` (2026-09-23, "Integrate imported media catalog with timeline baseline"; not checked for origin/main membership beyond the first hit).

[inference] Current editor code paths can still produce `file` on registry entries. Whether those in-memory registries reach a render request (vs. only the view model) was not traced to the save/render boundary in this pass.

Importers: no importer was found that writes `file` from an external source into the canonical registry; the Runtime `.astrid` import path was not searched for `"file"` key writes.

## 4. Coordination notes and other mentions

- `~/Developer/astrid-video/astrid-local/live-main/Astrid/docs/testing/astrid-exhaustive-qa/findings/timeline-registry-restore-portability-fix.md` and `.../waves/replay-restored-visualization-locators-3.md`, `.../waves/final-live-acceptance-6.md`, `.../waves/live-backup-restore-1.md`, `.../waves/replay-backup-restore-2.md` (and same under `~/Developer/astrid-video/astrid-local/Astrid/docs/testing/...`): QA findings about registry locators on restore/replay.
- `~/Developer/astrid-video/response-video-20261121/investigations/2.log:104`: "Ambiguous changed registry media locators; set local_path explicitly".
- `~/Developer/astrid-video/production/review/optimization/fleet/{w3b-replay-identity,p2-frame-speed,w1-render-range,swarm/s06-backups-clones}.jsonl`: fleet review logs mentioning the phrase (agent transcripts).
- `~/Developer/astrid-video/astrid-local/labs/tl-*` (tl-fx9-agent, tl-fx10-agent, tl-skill-agent, tl-merge-agent): lab copies of the same managed_timeline/assets files, all carrying the check (not separate prior art).
- `~/.codex/sessions/2026/11/21/rollout-2026-11-21T23-39-21-01a20043-...jsonl` and `rollout-2026-11-21T13-11-56-01a1fe05-...jsonl`: Codex sessions quoting the phrase.
- `~/astrid-release/*/state`: no hits.
- `/private/tmp/claude-501/.../scratchpad/r6/tooling/gh/issue-1238.json`: GitHub issue 1238 (banodoco/astrid-dev), "bug: timelines visualize fails the whole timeline on one stale asset open", state recorded in file.
- `/private/tmp/claude-501/.../scratchpad/r6/tooling/gh/timeline-748.json`: timeline events for issue 748: labeled 2026-11-16T16:30:49Z; cross-referenced 2026-11-16, 2026-11-21 (x3); commented 2026-11-21T19:56:36Z; all by AstridPseudon.
- `/private/tmp/claude-501/.../scratchpad/r6/probe/REPORT.md` and probe stderr files: earlier probes of this session (prior work, not external prior art).
- Issue 1253: no hit in any repo log or notes found by grep.

## Open points / not verified
- Whether the installed `release-14-plan-69` tree equals release/14 branch content exactly (only the managed_timeline path was compared at ref level).
- Whether any Runtime importer writes `file` into canonical registries (not searched beyond the runtime `store.py` check).
- Whether editor in-memory registries with `file` reach the render request body.
