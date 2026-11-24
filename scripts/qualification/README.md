# Release 15 qualification scripts

Each Tier 1 installed journey ([qualification.md](../../releases/15/qualification.md)) is one command. Status on 24 November 2026, on `release/15/main` (Agent `514499de`, App `d53685f3`, Runtime `24e2c929`):

| Item | Command | State |
| --- | --- | --- |
| 1c App per-file counts and failing tests | `app_test_ids.py extract LOG > cand.tsv` then `app_test_ids.py diff base.tsv cand.tsv --strict` | works; proved on a mutated copy |
| 2a Heavy timeline, N runs | `SAVE_LOOP_CHROME=/abs/chrome heavy_timeline.sh --app <App> --ref <sha> --out <dir> --runs 2` | preflight proven; a full run is in progress (see the Qualifier's STATUS) |
| 2b/2c Render output check | `render_verify.py OUT.mp4 --duration S [--width W --height H --fps F --audio --color T=#rrggbb]` | works, positive and negative cases (silent audio, wrong colour, truncated file fail); the render itself waits for Plan 87 (RN-15 open) |
| 2d Generate on a GPU | [generate_runpod.md](generate_runpod.md) | prepared, not run: needs the owner's go and budget |
| 2e Update and rollback | `data_fingerprint.py snap/diff` is the data check; the driver waits for the Lead's definition of "rolled back" | partly built |
| data check for 2a and 2e | `data_fingerprint.py snap DATA --out before.json`, then `diff before.json after.json` | works; confirm `--realm-glob` on the build under test |

## What "byte-identical" means

The App's save-loop compares the Runtime's `content_digest` after a guarded restore and a browser-computed SHA-256 of the saved payload (`scripts/save-loop/lib.mjs`, `assert.mjs`), not a file hash of the data root. That is the meaning used for item 2a. `data_fingerprint.py` adds a whole-tree byte comparison for a stopped stack.

## What exists on the release branch and what does not

- No 300-clip builder: `build-fixture.mjs` refuses fewer than 616 clips; Plan 77's and 89's 300-clip projects were restored archives.
- `--variant film-shaped` is on App `release/15/plan-88`, not `release/15/main`.
- No R15 to R14 downgrade command. `astrid install --rollback` reverses only the Release 0 to 1 storage handoff. The only R15 rollback is the installer's update-transaction rollback (extended by Plan 89's P89-06).
- `journey_fresh_update.py` serves a synthetic "release+1" manifest, not the real candidate.
