# Registry `file` investigation: timeline 77f906f3242c48179ab86ca7c3e62eb4 (read-only)

Stack: ~/astrid-release/release-14-plan-69. All reads from a copy of the realm DB (record/db/realm.sqlite3 + -wal/-shm), opened `mode=ro`. No writes to the stack. Scripts: record/q1.py..q4.py and inline checks (outputs in record/*.json).

## 1. Where the registry lives (verified)
- Realm DB: data/runtime/realms/221335d5-722e-48d0-a0ab-d9fde94b2277/realm.sqlite3 (copy: record/db/).
- The timeline asset registry is `registry.assets` inside the composition revision payload: `parent_composition_revisions.payload_json` (keys: clips, config, occurrences, registry).
- Head pointer: `parent_composition_heads` where timeline_id=77f906... -> revision_id authoring-parent-revision-7c5aefc4b203b6676e5a13e98236e7d6030b9296ef35ca6c819e349255abaad5 (publication txn-1389030768d44b5e889ff010f5ec4673, 2026-11-21T16:42:13.650Z).
- Commit log: `timeline_commit_history` (9 publications, project_seq 785..883).
- Blobs: `objects` table has NO row for digest sha256:4ab84c...; the blob exists in CAS at data/runtime/realms/221335.../cas/sha256/4a/b84c47567ab892fe2e8620042523c2f9a242d495793c5c590cc448046d625d (PNG, 1672x941 RGB).
- Entry of a09025f7 at head (record/before-state-a09025f7.json):
  - file: "/v1/objects/sha256%3A4ab84c47567ab892fe2e8620042523c2f9a242d495793c5c590cc448046d625d"
  - media_id: "sha256:4ab84c47567ab892fe2e8620042523c2f9a242d495793c5c590cc448046d625d"
  - generationId: "generation-f45da2428177cd70b6dcf8d874d5e8d97fbf70de838856c3fce1ab0ba3cdc2c9"
  - thumbnailUrl: "/api/runtime/v1/objects/sha256%3Ac0efc003046c485f8b58d97b7c2847a96f20f6e65c8b91b594aa64fbacb8ac79"
  - type: "image/png"
  - No object_id, no content_sha256, no digest field. media_id is the only identity (= the CAS digest).
  - `file` is a relative managed route for media_id (= the `/v1/objects/<encoded media_id>` form).

## 2. Registry key stats (head, 440 entries)
- Entries with any of url/file/path/source_path/locator/realm: 2. Keys found: `file` only (both entries). Second entry: a1336a48-2721-4cd0-b0c1-81b71fc1ecb9, same digest, has variantId, unreferenced.
- Other key counts: media_id 440, type 440, content_sha256 438, filename 116, resolution 91, source 95, handle 81, duration 12, generationId 2, thumbnailUrl 2, variantId 1.
- Referenced by clips at head: 4 keys (a09025f7, R5-VO-N19-D2, R5-ROOMTONE-D2, R5-MUSIC-MIX-B8S3). Unreferenced: 436 of 440.
- Note (code reading, not run): rendering/assets.py:266-275 rejects `thumbnailUrl`, `file` (unless allow_derived_files) and other locator fields when materializing the registry. Both file-key entries also carry thumbnailUrl. Inference: a render that materializes this registry without allow_derived_files would refuse it.

## 3. History (verified from DB)
- First appearance: project_seq 785, publication txn-72383d4f85e44b80b9d4cac89e1fc207, revision authoring-parent-revision-969b5e412077e717f6cfb40d62eaea9be3351ca1dd1ed23a6e985f28119ff3b4, 2026-11-15T23:02:49.344Z. Intent bootstrap, metadata {"label":"Imported timeline","source":{"via":"cli"}}, publisher none. timeline_events id 3/4 at 23:02:44 and 23:02:49.
- `file` was present from the first revision (identical value at every later revision, 785..883). clip-1 (asset a09025f7, at 196.5667, hold 5, track type) is also present in that first revision.
- Later revisions 876..883 (2026-11-21 16:31-16:42): "Place element" x8 (publisher astrid-dfc6526ce6e8378c550c5971, via python, recorder_abi 2) and "Publish authoring candidate" (seq 883). They carry the registry forward unchanged; they do not write a09025f7.
- Runs for the project (runs list, record/runs-list.json): earliest run 2026-11-17T19:10. No run exists for the 2026-11-15 import (inference: that import ran outside the runs/task table). runtime.media.import.v1 runs on 11-17 (fbd112fd..., 4671b3cc..., 18ba7c53...) and 11-22 14:14 (x5) have input digests that do not include 4ab84c...; no commit in the timeline after 21 Nov 16:42 exists, so the 11-22 imports did not reach this registry.

## 4. Writers of `file` (code)
- editor/src/integrations/runtime/dataProvider.ts:1805: `file: client.objectContentUrl(imported.asset_id)` in toPreparedMediaImport (1762). Absolute origin URL `${baseUrl}/v1/objects/<id>` (client.ts:1216-1218). Current path: prepareMediaImport (1361) <- prepareAsset (1430, AssetPanel/external drops) <- uploadAsset (1451); also tools/video-editor/data/AssetResolver.ts:160/168.
- editor/src/integrations/runtime/dataProvider.ts:1659-1661 withManagedFileRoute: rewrites absolute `file` to the relative route `/v1/objects/<encoded media_id>`; applied via normalizeRegistry (1664-1679) on reads and saves (lines 850, 1033, 1054, 1142, 1236, 1350). This is the form stored at head. Current path.
- editor/src/tools/video-editor/commands/media.ts:294 and 661: swap and prepared-import commands take `getAssetImmediateSource(entry)` and store the entry verbatim (661-675 writes payload.asset.entry into the registry). Current path for swap; carries whatever `file` the entry has.
- a/astrid/core/rendering/assets.py:330 `entry["file"] = asset.local_url` is render-time only (deepcopy in resolved_registry, 317-333). Not persisted. Not a source of stored values.
- a/astrid/sdk/timeline_import_prepare.py:336 and rendering pack timeline_prepare_import/run.py:46 set only the name; they copy the registry from the source manifest. Source of the 785 `file` is NOT determined: no source manifest exists on disk (grep of data/, home/, logs/, state/ for the asset id: no hits outside the DB). Inference: the 785 entry came from an earlier editor/import path that wrote `file` before the managed route normalization.
- Python SDK: no writer of a persisted `file` found (only reads: sdk/authoring_media.py:25 _PATH_FIELDS, 88-100 _source: a changed `file` requests an import).

## 5. Other timelines (verified)
- Head registries of all 7 timelines in the project+Main: only 77f906 holds a09025f7 (9 of 9 revisions containing the key belong to 77f906). 55ef205e, e4f205bd: 75 entries, no file keys. 31215be1 (Timeline 6, 3 revisions): no a09025f7. Main 1ae00c73: empty registry.
- So the bad asset did not reach other timelines.

## Inferences (not verified)
- The stored relative `file` at head is the output of withManagedFileRoute (dataProvider.ts:1661) applied after an absolute `file` was written at dataProvider.ts:1805.
- The 2026-11-15 import origin: unknown. Source file no longer on disk.
