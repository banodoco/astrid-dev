# Release 12 gate record

State: DRAFT, with no gate yet.

## Tuple

| Component | Full SHA / value |
|---|---|
| App | `{{FILL}}` (re-pin SHA) |
| Agent | `c5370a862d0b374afa412dd071418070e76f834c` |
| Runtime | `42ae24aff8d2cb854f874ce134161077a3ba3641` |
| harness (`harness/29-r12`) | `{{FILL}}` |
| VibeComfy | `e65f4941d09b1cb4d1dd5aae6171c73e648706f4` |
| ComfyUI (RunPod) | `ee71d5c4` — FULL SHA TO FILL |
| runpod-lifecycle | `f2948817eeb94af8dee76be21f6d673724f1606e` |
| Pinokio | `{{FILL}}` |
| OMP source | `https://github.com/banodoco/oh-my-pi` @ `78f0e0960f471c2c62b943272a48c33366f239fe` |
| Manifest sha256 | `{{FILL}}` |
| `public/install` sha256 | `{{FILL}}` |
| `public/install.sh` sha256 | `{{FILL}}` |
| `public/install.ps1` sha256 | `{{FILL}}` |

## Gate items

### 1. Matrix

Full `journey.yml` matrix, row=direct. All 11 rows must be green, including native Windows.

| # | Row | Run / result |
|---:|---|---|
| 1 | `{{FILL}}` | {{run link}} / {{result}} |
| 2 | `{{FILL}}` | {{run link}} / {{result}} |
| 3 | `{{FILL}}` | {{run link}} / {{result}} |
| 4 | `{{FILL}}` | {{run link}} / {{result}} |
| 5 | `{{FILL}}` | {{run link}} / {{result}} |
| 6 | `{{FILL}}` | {{run link}} / {{result}} |
| 7 | `{{FILL}}` | {{run link}} / {{result}} |
| 8 | `{{FILL}}` | {{run link}} / {{result}} |
| 9 | `{{FILL}}` | {{run link}} / {{result}} |
| 10 | `{{FILL}}` | {{run link}} / {{result}} |
| 11 | `{{FILL}}` | {{run link}} / {{result}} |

### 2. Agent CI

Frozen Agent run: [attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43085262585). Compare complete test IDs with [Release 10](https://github.com/banodoco/astrid-agent/actions/runs/43081197187) and [Release 11, attempt 2](https://github.com/banodoco/astrid-agent/actions/runs/43082578330), using `env/baseline-diff.py`. Check non-pytest jobs by name too.

- Bucket counts (regression, no-baseline, missing): `{{FILL}}`
- Rulings and unaddressed regressions: `{{FILL}}`

### 3. App Tests and Direct Journey

- App Tests run link and result/counts: `{{FILL}}`
- Direct Journey run link and result/counts (0 failures and no skipped tests, except listed expected failures): `{{FILL}}`

Named expected failures (approved by the orchestrator, registry `config/testing/direct-journey-expected-failures.json`):

- `id`: `P39-R12-DUP-SHOT`; `title`: `M2 native occurrence duplicate: lost ACK, Agent label, local label, restart, exact retry and guarded undo`; `issue`: `https://github.com/banodoco/astrid-app/issues/249`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-EXT-BATCH`; `title`: `M2 ordinary extension batch: move and hold, Agent label, lost ACK, restart, exact retry and guarded undo`; `issue`: `https://github.com/banodoco/astrid-app/issues/250`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-TASK-SWAP`; `title`: `render R, publish R+1 before it runs: the render is R's, it plays, and it is the film the App showed`; `issue`: `https://github.com/banodoco/astrid-app/issues/251`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.
- `id`: `P39-R12-VIDEO-DROP`; `title`: `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data`; `issue`: `https://github.com/banodoco/astrid-app/issues/252`; `owner`: `Plan 39 manager`; `expiry`: `2026-11-25`.

### 4. Review

- Agent candidate review range and verdict (no open blocker): `{{FILL}}`
- App candidate review range and verdict (no open blocker): `{{FILL}}`

## Not run / limits

- No GPU proof is part of this gate; generation, machine controls and GPU proof are outside Release 12.
- Editor data-loss fixes #252–#255 moved to Plan 39; their work in progress remains on branches.
- The Mypy gate stays red: the recorded counts are 2338 on the fixed candidate, 2325 on Release 10, and 2350 on Release 11/main. Refreshing the stale baseline is Plan 39 work.
- The R11 baseline comparison uses attempt 2 because unit shards 1 and 5 were cancelled in attempt 1 during a GitHub Actions outage; attempt 2 reran the failed and cancelled jobs on the same ref and code.
- The Windows Git-source repair evidence covers the five repair tests and `test_update_stages_recorded_git_from_restricted_service_environment`; the other installer-source cases noted in the decision log are pre-existing Plan 39 failures.
- A passing baseline comparison does not establish parity for missing or uncollected tests; non-pytest jobs also require review by name.

## Known issues shipped

- [#249](https://github.com/banodoco/astrid-app/issues/249): “Duplicate shot” fails with an error.
- [#250](https://github.com/banodoco/astrid-app/issues/250): the ordinary extension batch journey remains a known failure.
- [#251](https://github.com/banodoco/astrid-app/issues/251): the Agent cannot swap a generic task output into a timeline and commit it.
- [#252](https://github.com/banodoco/astrid-app/issues/252): a video dropped onto the timeline appears on screen but is not saved and is gone after reload.
- [#253](https://github.com/banodoco/astrid-app/issues/253): after a refused edit, later edits in the same session are refused too.
- [#254](https://github.com/banodoco/astrid-app/issues/254): the recovery “Save them” action is a Plan 39 issue.
- [#255](https://github.com/banodoco/astrid-app/issues/255): an upload in progress is lost at reload.
