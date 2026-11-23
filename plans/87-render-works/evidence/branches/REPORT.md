# Astrid release branch and test-stack investigation

**Scope and safety.** Read-only source/runtime inspection. No existing working tree was checked out or reset, no GitHub posts were made, and the running stack at `~/astrid-release/release-14-plan-69` was not changed, stopped, or rebuilt. Remote-tracking refs were fetched in the source clones only. “Verified” means supported by checked source, Git history/diff, or captured local state. “Inferred” is labeled.

## 1. Origin branch heads and ancestry

Heads below are from the fetched origin refs on 22 Nov 2026. The complete inventory of `main`, every `release/14/*`, and every `release/15/*` head (12-character SHA, committer date and subject) follows in the appendix.

| Repo | `main` / `release/14/main` head | `release/15/main` head | Pinned stack commit | Pinned…14/main `rev-list --left-right --count` | Pinned…15/main |
|---|---|---|---|---:|---:|
| astrid-app | `e0da794ac9d2`, 2026-11-22; same as main | `c5ba8cd92d8c`, 2026-11-22 | `e0c6f7cdbb94` | `10 146` | `10 156` |
| astrid-agent | `c0ad6b54aadd`, 2026-11-22; same as main | `8807f820eb47`, 2026-11-22 | `83d5f8fe382e` | `21 504` | `0 597` |
| astrid-runtime | `5120462d6747`, 2026-11-22; same as main | `23310dc82876`, 2026-11-22 | `b2ea261f36f5` | `5 64` | `0 92` |

In `rev-list --left-right --count pinned...target`, the first number is commits reachable only from the pin, and the second only from the target. Evidence: `git rev-list --left-right --count <pin>...origin/<branch>`; head subjects and exact timestamps from `git show -s --format='%H %cI %s'`.

**Plan 69 merge status (verified):** `release/14/plan-69` is not fully merged into `release/14/main`: its pinned App/Agent/Runtime commits have 10/21/5 pin-only commits, respectively. It is also not fully merged into `release/15/main` because the App pin has 10 pin-only commits. Agent and Runtime pins are ancestors of 15/main (`0` pin-only), so those producer commits have landed there. The app, agent and runtime 14/main heads are ancestors of their corresponding 15/main heads: 14…15 counts are `0 10`, `0 114`, and `0 33`. Thus **14/main is merged into 15/main across all three repos**; Plan 69 as a complete tuple is not.

**Branch inventory:** generated from fetched `refs/remotes/origin/main`, `.../release/14/*`, and `.../release/15/*`. Branches are listed verbatim, including WIP refs, because they exist on origin. The primary heads above are exact; the inventory uses 12-character hashes for readability.

## 2. Defect review

Compared cited source at the pinned state with `origin/release/14/main` and `origin/release/15/main`; findings below are **verified source comparisons**, not fresh reproductions. “Fix status inferred” marks rows where a relevant diff exists but does not prove resolution. **FIXED (verified)** means the target change addresses the reported failure as described. **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** means relevant code changed but evidence does not prove the observed failure is solved. **UNCHANGED (verified)** means the cited failure condition remains or there is no relevant fix.

| # | Defect from scratchpad | 14/main | 15/main | Evidence / relevant change |
|---:|---|---|---|---|
| 1 | Dry-run transport failure reported as `CommitOutcomeUnknown`; failed preview leaves a durable/in-flight record (`sync.py`, demo §1b, edits §7) | **FIXED (verified)** | **FIXED (verified)** | Agent commit `5b98c1bcad14` (2026-11-17), “Timeline dry runs leave no durable state”: unanswered/refused dry-run previews are released and don't leave durable pending state. The same commit is in 15/main. |
| 2 | SDK `Timeline.commit` one-field edits re-derive/rewrite unrelated clips; `push=None` silently no-ops (`commit_session.py`, demo §1c; edits §5) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | `_cmd_edit` remains a working-copy route; no matching fix in `git log -L :_cmd_edit`. `commit_session.py` changes only an 8-line canonical shot-ID fallback; no evidence it prevents broad reflow. |
| 3 | CLI `timelines edit --draft` changes unrelated formula clips during an element edit (`packs/timeline/cli.py::_cmd_edit`, demo §1c; hair §6) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | Same working-copy/re-derivation behavior remains; no fixing commit found. |
| 4 | Parent clip delete refused whenever parent config declares `app.astrid.slots` (`_delete_commands.py`, edits §3) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | File is byte-identical to pinned source; the timeline-wide semantic-dependency guard remains. |
| 5 | SDK cannot resolve project-pack element for a parameter write (`ElementPackNotInstalled`, edits §4) | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | Project-pack/admission implementation changed substantially; no source proof that this exact schema lookup now sees the project pack. No clear fixing subject. |
| 6 | `nudge()` invokes timeline-wide retiming and changes hundreds of start/hold values (edits §5) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | Model/retiming implementation is unchanged from the pin; no relevant fix found. |
| 7 | Failed commit leaves pending state that blocks the next request (`sync.py`, edits §6) | **FIXED (verified)** for failed dry-run previews | **FIXED (verified)** for failed dry-run previews | `5b98c1bca` “Timeline dry runs leave no durable state.” Scope is dry-run preview cleanup; this does not imply every non-dry-run unknown outcome is recoverable. |
| 8 | Shared per-timeline outbox can replay another agent's flight; stale `Timeline.open().head` / private outbox KeyError (sync/outbox, sweep §4, hair §§8,10) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | Dry-run cleanup is not per-process outbox isolation. 15 adds `53c2a382` “Guard element lost-ack flight reconciliation,” a narrow reconciliation guard, not isolation or a general stale-head fix. |
| 9 | `doc.patch + media.admit` on an occurrence clip raises false `capture_mismatch` (hair §4) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | `_commit_patch.py` is unchanged at both targets. |
| 10 | Imported/mapping media handles rejected as not Runtime-verified; local-path and media-handle routes conflict (hair §5) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | No matching fix identified in the Agent/Runtime commit history. |
| 11 | Word-anchored occurrence clip media swap refused because exact timing binding is absent (hair §3) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | The cited timing evaluator/ownership constraints remain; no fixing commit found. |
| 12 | Native media swap rejects legacy registry identities (`generationId/variantId`, `source/content_sha256`, `image/png`) (hair §7) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | No relevant change found for this legacy identity codec. |
| 13 | Timeline document `check` passes but `publish` refuses newly admitted media or legacy pins (hair §7b) | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | Project-pack/media admission code has changed; no evidence that this specific publish gap for new media keys and legacy registry entries is closed. |
| 14 | Composed `visualize` validates the whole timeline and fails on unrelated/bad media; retired `file` locator error (managed_timeline.py, demo §1, probe) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | The explicit retired-locator refusal remains in both targets (14 lines 555–558; 15 lines 579–582). It still reports `contains retired media locator field(s)`; there is no cited fix that limits validation to the frame's active clips. |
| 15 | `timelines elements` requires undocumented `--realm`; project-pack root defaults outside stack data (sweep §§1,5) | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | `project_packs.py` changed in 14 with `9c7152de4`, “FIX-25: R13 transitions and phase effects open, edit, render and time in R14 (#481)”; does not establish automatic realm/root selection. Stack-specific root behavior remains unproven. |
| 16 | `timelines elements` omits elements inside shot occurrences (sweep §2) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | The code still enumerates only parent clips; no occurrence traversal fix found. |
| 17 | `update-element` cannot target occurrence child; `place-element` cannot write params (sweep §3) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | No combined target+params operation found in the changed source. |
| 18 | `pack validate` passes descriptor that `project-pack admit` rejects (>500-char description); admit gives traceback (sweep §6) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | Agent `core/element/cli.py` and `schema.py` are byte-identical to the pin; validator/admit inconsistency persists. |
| 19 | `timelines history --json` lacks a `head` field (sweep §7) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | No corresponding CLI output change found. |
| 20 | Video assets have unknown dimensions; `am-footage` falls back to box aspect, preview/render disagree on RAW-H3 (demo §2; am-footage/component.tsx) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | App commit `2ee2951c3` (2026-11-21), “Restore footage inset and Discord camera behavior,” adds inset/feather behavior. The cited resolution fallback remains; no video-dimension probing or `videoWidth/Height` use. |
| 21 | Editor Remotion preview has subpixel motion jitter/flickering edge; no direct frame seek handle (`RemotionPreview.tsx`, demo §1d and editor-preview report) | **UNCHANGED (verified)** for the reported defect | **UNCHANGED (verified)** for the reported defect | App changes `6b36530a9` “Reveal preview after decoded video frame” and `9d69998ea` “Preserve preview migration diagnostics and refuse mismatched shots” improve load/migration state only. No direct seek URL/handle or demonstrated fix for device-pixel layer snapping. |
| 22 | No public CLI route for source media bytes/path; manual CAS traversal needed (demo §3) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | No matching media-export/path route found in the cited product changes. |
| 23 | Audio generation cloud action does not declare required FAL/WaveSpeed secrets (`generation/pack.yaml`, sfx §1) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | `generate_audio` still has `env: [FAL_KEY, WAVESPEED_API_KEY]` without `secrets_required`; `generate_image` declares it, demonstrating the difference. |
| 24 | No text-to-SFX mode; `sfx` is unwired (sfx §3) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | Generation action still reserves `sfx`; no matching mode/model implementation found. |
| 25 | No audio-understanding capability installed/advertised by this release tuple (sfx §4) | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | Capability inventory and pack catalog changed across releases, but no evidence confirms `understanding.audio_understand` becomes ready on these target tuples. |
| 26 | No timeline audio excerpt/mixdown route without a full render (sfx §5) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | No excerpt/mixdown CLI route found. |
| 27 | Pack preview loading times out under heavy load and error blames revision (sweep §8) | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | **CHANGED BUT UNCLEAR (verified code change; fix status inferred)** | Pack install/admit paths changed, but no source or commit evidence specifically addresses long/retried preview fetches or timeout wording. |
| 28 | Timeline document/working-copy film swap would flatten shots and rewrite other formula clips (hair §6) | **UNCHANGED (verified)** | **UNCHANGED (verified)** | Same `_cmd_edit`/working-copy behavior; no fix for occurrence-safe element/media edits found. |

**How to read this table:** a fix in an unreleased topic branch does not count as fixed on `release/14/main` or `release/15/main`. In particular, the visible App/Agent/Runtime `release/14/*` topic branches include unmerged work, but the question asks specifically about `main`.

### Representative Git evidence excerpts (verified)

These excerpts show why “fixed” is limited to the stated defect and why other rows remain open. The direct comparisons used the full pinned commit IDs above.

- Agent `sync.py` diff, Release 14: commit `5b98c1bca` adds `PreviewUnanswered` with headline “The dry run got no answer; nothing was committed” and `_release_preview(...)`; in `_flush`, `if dry_run and isinstance(exc, (WorkspaceClientError, OSError, TimeoutError))` releases the flight and raises `PreviewUnanswered`. `git log` subject/date: `5b98c1bca 2026-11-17 Timeline dry runs leave no durable state`.
- Agent `managed_timeline.py` Release 14 diff changes media-selector projection and placement normalization, but the retained lines are still: `forbidden = [field for field in ("url", "file", "path", "source_path", "locator", "realm") if field in entry]`; if present, it raises `canonical registry asset ... contains retired media locator field(s)`. That is the exact `file`-locator failure in probe/REPORT.md.
- Agent `_delete_commands.py`: `git diff --quiet <pin>..origin/release/14/main -- astrid/sdk/timeline/_delete_commands.py` returns success (empty diff). The guard still checks `('sequences', 'formulas', 'slots')` before parent clip deletion.
- Agent `generation/pack.yaml`: at Release 14 `generate_audio` lines 193–195 list `env: FAL_KEY, WAVESPEED_API_KEY`; there is no `secrets_required` in that action. The later `generate_image` action has `secrets_required: [FAL_KEY]`. Same manifest shape at Release 15.
- App `am-footage` diff: commit `2ee2951c3` adds `insetKeys` and `feather` parameters and interpolates inset rectangles; the existing resolution fallback remains `parseSize(resolution) ?? parseSize(p.sourceSize) ?? {w: boxW, h: boxH}`.
- App preview diff: commits `6b36530a9` and `9d69998ea` add decoded-first-frame gating, a preparing placeholder, and caught retry errors. They do not add a frame query parameter or preview seek API.
- App git-log excerpt: `9d69998ea 2026-11-16 Preserve preview migration diagnostics and refuse mismatched shots`; `6b36530a9 2026-11-16 Reveal preview after decoded video frame`; `2ee2951c3 2026-11-21 Restore footage inset and Discord camera behavior`.
- Project-pack/admit code is the unclear case: `9c7152de4 2026-11-22 FIX-25: R13 transitions and phase effects open, edit, render and time in R14 (#481)` changes project-pack architecture, but validator CLI/schema files are unchanged and the commit does not claim to resolve the >500-character mismatch.

## 3. Switching cost, data, and film appearance

### Driver behavior (verified from source)

The driver is `~/Developer/astrid-release-src/astrid-app/scripts/astrid-release/astrid-release`. For `astrid-release release/14/main` or `astrid-release release/15/main`:

- Slug/root would be `~/astrid-release/release-14-main` or `~/astrid-release/release-15-main`. These are new stack directories, separate from the current `release-14-plan-69`; both paths were absent at inspection, so the driver would take its new-stack path.
- Resolves App and Agent heads via `git ls-remote` (branch, then same release's `main`, then `main` fallback); derives Runtime and other pins from the Agent's manifest locks. The driver does not run `git fetch` itself for that resolution. It fetches/clones the App source into the new root, then runs the official installer, which downloads the pinned program. For an existing App checkout it fetches that branch; here the new roots don't exist.
- Chooses available ports: editor 2400–2499, proxy and Runtime door 17500–17599, skipping protected live ports 17340/2222/17336/17391. Current stack uses 2400/17500/17501, so an adjacent stack would currently take 2401 and 17502/17503: read-only `lsof` found those ports free at inspection. This remains conditional on availability when the command runs.
- The build path installs the program and npm dependencies, snapshots the **live** realm into the new root's `data/`, and starts the App/runtime there. The current stack data is not copied as part of this new-build path. Script comments and README state a changed-pin `update` refuses, since installer update isn't supported for these roots.
- Log evidence for last install: `last-run.json` says start 2026-11-21 16:26:23 UTC and finish 16:28:34 UTC, **131 s**. The shell `logs/install.log` itself has no timestamps; 131 s is the installer-reported interval, not an end-to-end stack build duration.
- Actual current sizes: `df -h ~` reports 228 GiB total, 181 GiB used, **4.6 GiB available**. Current stack: **8.1 GiB**, its `data/`: **2.2 GiB**. The driver requires roughly 5 GiB plus twice the live realm database before installation, and then separately requires 2 GiB before `npm ci`; the README estimates about 10 GiB for a new stack. Therefore a parallel fresh build **cannot pass its current disk floor** with 4.6 GiB free. APFS clones make realm bytes cheap, but program/editor/npm dependencies still occupy space.

### Project data and migrations

- Current `state/realm-id` is `221335d5-722e-48d0-a0ab-d9fde94b2277`, with project “Almost Ready” and its project-pack files in `data/project-packs/<realm>/<project>/...`. The film's edited timeline, project pack, CAS media, and the unresolved timeline outbox are inside this copied realm/data root. The copy is one-way relative to live: current edits do not flow back to the live installation.
- Driver first-run behavior snapshots the existing **live installation's** realm; it does not point a new directory at `release-14-plan-69/data`. A manual reuse/attach route is only safe when the target Runtime's `SCHEMA_VERSION` matches the existing realm. The Release 14 driver README/Plan 61 instructions explicitly say keep the data clone, attach its realm through `workspace attach`, and require the database schema version to equal the target `SCHEMA_VERSION`; if Runtime refuses it, stop and do not hand-migrate. Current driver README states moving a built stack to new commits is unsupported and data carry-over is only by attaching a kept clone when schemas match.
- Runtime `SCHEMA_VERSION` is 33 at pinned `b2ea261`, 14/main, and 15/main (verified in `runtime_protocol/store.py`); this indicates no 14-to-15 schema-version migration is required by the branch delta. It is **not** proof that every stored record/payload is compatible, nor does the current driver implement a one-command attach from this plan-69 root to a new target. Runtime has migration/operator-upgrade journals, but that is distinct from a verified cross-release stack-switch procedure.
- **Do not point 15/main directly at the only copy of the active data.** A clone/backup must precede attach or migration. Keep the current stack untouched until a parallel stack is built and independently verified.

### Film appearance / source compatibility

- The project pack `ar-discord`, `ar-footage`, and `ar-type-sweep` is data-root content, not automatically replaced by switching product branches. Attaching the same data would retain those exact project-pack sources and schemas; a fresh snapshot from the live stack might instead bring live's project data, not the active edits.
- Agent test fixture `tests/fixtures/packs/astrid_motion` (including `am-footage`, schemas and helpers) is byte-identical from the pinned Agent commit to both main targets. Runtime schema version is also identical.
- The App's `am-footage` does change on both targets: `2ee2951c3` adds inset keyframes/feather-mask behavior; its cited unknown-video-resolution fallback is unchanged. App `RemotionPreview.tsx` changes preview loading/migration diagnostics, not the measured film-vs-preview pixel snapping.
- Consequently, if “Almost Ready” uses only its `ar-*` project-pack renderers in those clips, those branch changes alone do not directly change their component code. **Inferred visual risk:** if any film clip resolves to the changed built-in `am-footage` implementation or depends on new admission/schema metadata, its output/preview can change. Capture a before/after render or frame comparison on a disposable clone before adopting either target. No render was performed as part of this investigation.

## 4. Recommendation and safe sequence

**Recommendation (inferred from verified state): stay on the running stack for now.** Neither main branch fixes most of today's defects, and a parallel stack does not fit the available disk. The one confirmed fix, Agent dry-run cleanup, is on both main targets; it does not resolve the broader edit safety, shared outbox, rendering, or legacy-media failures. Avoid a branch switch while the film is actively edited.

When a switch is useful and there is enough disk:

1. Wait for current editors to finish, then take a verified backup of the entire current `data/` root (including the runtime realm, CAS, project packs and timeline outbox). Preserve the current stack as rollback; do not run `update` on it.
2. Free enough disk or use a separate volume. Build `release/14/main` beside the current stack first; the script's first-run snapshot defaults to live data, so keep its fresh copy separate from the film's active data.
3. To carry the film's current edits, use a clone of the current stack data root as attach input. Check target and source `runtime_schema.version` read-only and confirm the new Runtime accepts the exact realm id through supported `workspace attach/inspect`; do not let an installer overwrite or migrate the sole source. The current driver docs describe a same-schema attach, but this plan-69 data-to-new-main route has not been exercised end to end.
4. Open “Almost Ready” and confirm the correct timeline head, clips, project-pack revision/admission, media availability and editor preview on that disposable clone. Compare representative frames/render output for affected footage elements and confirm no in-flight outbox has been replayed.
5. Only after verification decide whether to use 14/main or 15/main. 15/main is 14/main plus later commits, but offers no extra fix for most listed defects. Preserve the old stack/data until the new one has survived the work session.

**Risks by choice (inferred):**
- **Stay:** lowest risk to film data and active editors; defects remain, but dry-run cleanup is improved only if the agent pin is moved (it is not in the current stack).
- **Move to 14/main:** same-schema version makes reuse plausible, but the driver creates a fresh live snapshot and has no direct active-stack data switch; 14/main lacks the measured fixes besides dry-run handling.
- **Move to 15/main:** same schema and broader heads; App/Agent/Runtime plan-69 content is not all merged as a tuple. Film data/revision remains at risk if attached without a full backup, and the observed defects mostly remain.

## Evidence notes

- Running stack facts came from `state/heads.tsv`, `state/realm-id`, `state/ports`, `home/Library/Logs/Astrid Runtime/last-run.json`, and read-only `du`/`df`.
- Branch ancestry and differences came from the three fetched source clones under `~/Developer/astrid-release-src/`; no existing working tree was checked out or reset.
- Topic-branch heads are not evidence of mainline fixes; only the target main refs were classified above.
- No tests, renders, stack start/stop/update, data writes, or GitHub writes were performed.

## Appendix A — origin release branch inventory


### astrid-app

| Origin branch | Head | Date | Subject |
|---|---|---|---|
| main | `e0da794ac9d2` | 2026-11-22 | Merge pull request #338 from banodoco/release/14/int-59-64-65 |
| release/14/973-editor-contract-tests | `f2b110f92139` | 2026-11-19 | Revert "test(e2e): align the named Keep journey with #295 (astrid-dev#973)" |
| release/14/app-transport | `cde12450cbc7` | 2026-11-18 | Warm each audio URL once per session; forward proxy stderr to the editor log |
| release/14/app-vitest-proof | `7dde73ee913f` | 2026-11-19 | Capture the native App and SDK IDs for the two Plan 61 sync trees |
| release/14/at4-installer-proof | `f915d469bc01` | 2026-11-19 | test(plan39): pin the reviewed Windows installed tuple for isolated proof |
| release/14/ci-triggers | `bfaa2e89da1e` | 2026-11-16 | CI: run on release/<N>/main as it does on int/** |
| release/14/diag-417 | `82e94e366c82` | 2026-11-22 | Capture sanitized recovery action state |
| release/14/diag-gate5-recovery | `39f8695432f2` | 2026-11-22 | DIAG record sanitized Gate 5 recovery metadata |
| release/14/drop-error-parks | `6976b017c9a8` | 2026-11-18 | Park a dropped file that was not added instead of removing it: placeholder stays with the reason, Try again / Discard |
| release/14/drop-placement | `a55ee1227dae` | 2026-11-18 | Reuse a registry key only when it is exactly the Agent's binding; otherwise take a new key |
| release/14/edit-refusals | `7b9cdee529e2` | 2026-11-18 | Merge pull request #292 from banodoco/task/839-track-settings |
| release/14/fix15-release-tuple | `e6ca6e8032fc` | 2026-11-20 | Merge pull request #320 from banodoco/release/14/plan-61 |
| release/14/fix16-rejected-saves | `1c8b70d939ef` | 2026-11-21 | test(fix16): assert the recovery retry is bound to its offered snapshot |
| release/14/fix21-restore-prompt | `526f585fe61a` | 2026-11-21 | Disable Restore while timeline saves are pending |
| release/14/fix32-recovery-slot-race | `4be44de85511` | 2026-11-22 | Tombstone acknowledged timeline recovery drafts |
| release/14/fix33-rename-after-move | `8664495021c5` | 2026-11-22 | Keep accepted timeline data across duplicate publication polls |
| release/14/gesture-registry-read | `25c5672d545a` | 2026-11-18 | Gesture reads declare the registry entry's duration, not the whole optimistic entry |
| release/14/int-59-64-65 | `cb84ce93b7d4` | 2026-11-22 | Merge pull request #357 from banodoco/release/14/int-fix-transition-display |
| release/14/int-final-repin | `b94dd9b1615f` | 2026-11-22 | Pin Agent with regenerated tool catalog |
| release/14/int-fix-app-landing | `7e5f2e50e259` | 2026-11-22 | Keep the authored display basis when reopening a refused track rename |
| release/14/int-fix-clip-size | `0e591c19656a` | 2026-11-21 | Hold render until clip dimensions are ready |
| release/14/int-fix-journey-digest-all | `387cb42d995d` | 2026-11-22 | Use bare digests in native clip fixture registries |
| release/14/int-fix-three-products-seed | `53c1c8678df2` | 2026-11-22 | Match move dependency expectation to duration leaf |
| release/14/int-fix-transition-display | `ed24b1d8dfcc` | 2026-11-22 | Merge bootstrap placement expectation |
| release/14/int-fix-transition-id | `a46cb5032113` | 2026-11-22 | Merge commit 'b93e1faa605576827ba829c29a2c414f0d0c2e89' into release/14/int-fix-transition-id |
| release/14/int-fix-vendor-lock | `f33fb3076fe3` | 2026-11-22 | Sync Agent public boundary to landed release |
| release/14/int-merge-main-fix16 | `a6a594ea2d64` | 2026-11-21 | test(app): assert canonical edit and suffix survive drain |
| release/14/landing-branch-rule | `5f0d79fa4fe0` | 2026-11-16 | CI: a pull request into a release branch must come from a branch of that release |
| release/14/landing-reference | `39f2091b6bfb` | 2026-11-16 | CI: unit tests and a landing reference on pull requests into a release branch |
| release/14/live-fixes | `e133304a5a78` | 2026-11-18 | Live fixes: a draft whose base is gone says so, Discard and start remove stale rows, one fewer full-record read per edit |
| release/14/main | `e0da794ac9d2` | 2026-11-22 | Merge pull request #338 from banodoco/release/14/int-59-64-65 |
| release/14/media-association | `a9f2e09b09fb` | 2026-11-18 | Converge pinned-group sync over variant-less images |
| release/14/outbox-rows | `ffc09d024cf9` | 2026-11-18 | Outbox: a claim that ends with nothing to send deletes its row; the startup prune can no longer be stopped by another timeline's record |
| release/14/plan-39 | `e3497c3a545e` | 2026-11-21 | Merge pull request #321 from banodoco/p39/app-inventory-reconciliation |
| release/14/plan-52 | `0b6ef16152dc` | 2026-11-16 | Merge pull request #277 from banodoco/release/14/landing-branch-rule |
| release/14/plan-59 | `2ffc0a300009` | 2026-11-18 | Merge pull request #309 from banodoco/release/14/drop-error-parks |
| release/14/plan-61 | `7125857797e2` | 2026-11-19 | Merge pull request #317 from banodoco/release/14/sync-fix14-plan-61 |
| release/14/plan-66 | `36d2b82582e5` | 2026-11-18 | Plan 66: seed the save-loop harness from the 18 Nov sweep and profiler |
| release/14/plan-66-wip/wt-app-concurrent-drops-registry | `2402b1d97e6a` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from wt-app-concurrent-drops-registry on release/14/concurrent-drops-registry |
| release/14/plan-66-wip/wt-shot-trim | `11ee51c1e5be` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from wt-shot-trim on task/plan59-shot-trim |
| release/14/plan-69 | `e0c6f7cdbb94` | 2026-11-21 | Pin Agent 83d5f8fe and Runtime b2ea261 |
| release/14/quick-edits | `ff34621e9e8e` | 2026-11-18 | Watchdog counts progress: each accepted intent resets it |
| release/14/rejected-discharge | `2c4d14f68f6c` | 2026-11-18 | Editor: no automatic stale_head rebase; discharge only from the Use latest choice |
| release/14/runtime-pin-66 | `9fa8618ae679` | 2026-11-18 | Pin Runtime release/14/plan-59 4c18af59 (clip list.remove passes commit authentication) |
| release/14/same-file-drop | `90e4640390cb` | 2026-11-18 | Merge pull request #308 from banodoco/release/14/gesture-registry-read |
| release/14/save-recovery | `c0750f500d10` | 2026-11-18 | One save bar, total Discard, retry with backoff, position fields commit at the end of an edit |
| release/14/save-recovery-2 | `584333bedd62` | 2026-11-18 | Update the persistence refusal test for the removed duplicate toast |
| release/14/save-rejections | `6b5d75562525` | 2026-11-16 | Merge release/14/ci-triggers into release/14/save-rejections |
| release/14/staged-candidate | `69d034d7cc55` | 2026-11-22 | Merge commit 'c07c13753b0cc7e8ec81faaaa500a371886d7a65' into HEAD |
| release/14/sync-fix14-plan-39 | `75daac1cc8e1` | 2026-11-19 | Merge remote-tracking branch 'origin/release/14/plan-39' into release/14/sync-fix14-plan-39 |
| release/14/sync-fix14-plan-61 | `e44b58366e53` | 2026-11-19 | Integrate the certified Plan 61 editor and tool in the Release 14 sync |
| release/15/forward-14 | `6683b1943d7e` | 2026-11-18 | Release 15: bring Release 14 plan-59 forward (today's save and transport fixes) |
| release/15/forward-14-2 | `a36a10f7650c` | 2026-11-21 | Pin the Agent and Runtime on release/15/main (04f3f123, 1758a6df) |
| release/15/forward-14-5 | `8567319d3468` | 2026-11-22 | Release 15: bring the published Release 14 forward |
| release/15/main | `c5ba8cd92d8c` | 2026-11-22 | Merge pull request #369 from banodoco/release/15/forward-14-5 |
| release/15/plan-69 | `d53964f1bd2c` | 2026-11-22 | Merge pull request #366 from banodoco/p69/r23-final-pins |
| release/15/plan-69-app-landing | `47ef5507d5af` | 2026-11-22 | Pin Plan 69 App to the forwarded release producers |
| release/15/plan-77 | `5607d00f727e` | 2026-11-22 | Merge pull request #367 from banodoco/p77/round6-current-app |
| release/15/plan-77-quick-indicator | `e6296b68a049` | 2026-11-22 | Add verified quick sweep backup workflow |
| release/15/plan-77-tooling | `0915355d6a17` | 2026-11-22 | Clarify save-loop tooling writes and results |

### astrid-agent

| Origin branch | Head | Date | Subject |
|---|---|---|---|
| main | `c0ad6b54aadd` | 2026-11-22 | Skills: ask agents to report, fix and PR Astrid problems (#512) |
| release/14/926-retry-durable-logs | `dbb7152e4e14` | 2026-11-19 | test(installer): refresh independently measured Runtime path witness to 8e8711fd |
| release/14/964-tls-policy-package | `0a83a7b545d9` | 2026-11-19 | evidence(FIX-13): retain paired TLS and GL.2 qualification |
| release/14/baseline-gates | `52aa9a4f170c` | 2026-11-16 | Allow resolved structure entries in baseline test |
| release/14/ci-triggers | `cf51c9c62799` | 2026-11-16 | CI: run on release/<N>/main as it does on int/** |
| release/14/cleanup-ack-during-activation | `44da078c13a2` | 2026-11-19 | test(host): stop pack-refresh polling before terminal shutdown (#905) |
| release/14/commit-loads | `ca58583fda1b` | 2026-11-18 | Keep the reservation memo on the provider instance and narrow its fallback |
| release/14/download-rerun | `6c7c0d1dcc40` | 2026-11-16 | Verify confirmed model files on download rerun (#722) |
| release/14/edit-refusals | `d308161f8cd3` | 2026-11-18 | Merge pull request #386 from banodoco/task/edit-refusals-scope |
| release/14/fix-1238-stale-registry-asset | `1951cfe438b1` | 2026-11-22 | Drop the editor's own-object route before managed render validation |
| release/14/fix-check-local-span | `5c578c4b703f` | 2026-11-22 | Keep unresolved local timeline coverage advisory |
| release/14/fix-tool-catalog | `ed9e9775b3b0` | 2026-11-22 | Regenerate whole tool catalog for rendering pack |
| release/14/fix15-vibecomfy-pin | `dd298901225f` | 2026-11-21 | Refresh release defaults and path witnesses |
| release/14/fix17-diag | `9b5f78083d80` | 2026-11-21 | Probe FIX-17 Windows recovery and live Runtime browser skew |
| release/14/fix17-r13-update-matrix | `37857d16106d` | 2026-11-22 | Fix guarded reload recovery observation |
| release/14/fix18-r13-differences | `d6e1221357f8` | 2026-11-21 | Expose renderer subprocess diagnostics |
| release/14/fix19-windows-task-cmdline | `7520b10e972f` | 2026-11-21 | Bound Windows scheduled task reconciliation arguments |
| release/14/fix22-open-after-update | `5a7aeccd2d24` | 2026-11-21 | http policy guard: refresh the audited entry for the moved Backend.verify opener |
| release/14/fix23-scheduled-task-name | `7af80410194d` | 2026-11-21 | Fix scheduled task action reconciliation |
| release/14/fix25-legacy-transitions | `bac02549f844` | 2026-11-22 | Preserve canonical transition timing for Agent references |
| release/14/fix28-runtime-repin | `ddb8f55490af` | 2026-11-22 | FIX-28: move the Runtime pin assertions to 3f9c0ca3 |
| release/14/fix29-agent-green | `f6f18c81b7b4` | 2026-11-22 | FIX-29: pin the final Runtime 5120462d |
| release/14/fix31-sdk-reader-compat | `b48a79fed08d` | 2026-11-22 | Preserve exact SDK timeline rates through render |
| release/14/installer-browser-control | `a525e87e4bf6` | 2026-11-16 | Respect unattended installs and show runnable setup hints (#723) |
| release/14/installer-mypy | `04fbdc16ca03` | 2026-11-18 | fix(release): repair the six authorized inherited import findings |
| release/14/int-59-64-65 | `2e8524abc83b` | 2026-11-21 | Merge Agent release/14/main for R14-FIX-22 |
| release/14/int-fix-opaque-key | `b57d5db6bc52` | 2026-11-21 | Apply compatibility only in reader views |
| release/14/int-fix-structural-undo | `2d0e6a3a04bf` | 2026-11-21 | Preserve legacy track rows during timeline document edits |
| release/14/int-fix-whisper-windows | `70159fd5a03f` | 2026-11-22 | Pin landed VibeComfy and audit Whisper download |
| release/14/int-task-h3-error-provenance | `5b321a8c0601` | 2026-11-21 | Preserve selected entry on workflow input rejection |
| release/14/int-whisper-agent | `eab04f2cff0e` | 2026-11-21 | Sync Whisper temporary audio cleanup patch |
| release/14/landing-reference | `36c37a2db848` | 2026-11-16 | CI: a pull request into a release branch must come from a branch of that release |
| release/14/legacy-basis | `6b878066927c` | 2026-11-18 | Build each bundle's reference bases once instead of deep-copying the document per declaration |
| release/14/legacy-probes | `6c5b314e9db7` | 2026-11-18 | Freeze the old probe as the test oracle and compare over real fixture heads |
| release/14/ls12-darwin-audio-20261119 | `f8abdb9ed8b1` | 2026-11-20 | Observe one LS-12 SDK first job per immutable source on one Mac |
| release/14/main | `c0ad6b54aadd` | 2026-11-22 | Skills: ask agents to report, fix and PR Astrid problems (#512) |
| release/14/media-association | `5369ea9ed21c` | 2026-11-18 | Judge an incomplete catalog association only when a change introduces or touches it |
| release/14/oracle-freeze | `60f82b3ada69` | 2026-11-18 | Freeze the pre-#400 reference basis in the legacy-probe oracle |
| release/14/p39-picks | `c1530f710450` | 2026-11-21 | test(ci): fetch pinned release-0 Agent archive in unit shards (#376) |
| release/14/plan-13 | `9a98aacab3ad` | 2026-11-21 | Merge pull request #456 from banodoco/release/14/main |
| release/14/plan-39 | `2ef74155a1a9` | 2026-11-21 | Merge pull request #444 from banodoco/p39/bun-launcher-inventory |
| release/14/plan-52 | `fc391dea696e` | 2026-11-16 | Merge pull request #372 from banodoco/release/14/baseline-gates |
| release/14/plan-55 | `e37956564141` | 2026-11-19 | Merge pull request #410 from banodoco/p55/ls-6-remainder |
| release/14/plan-59 | `ec758a9b86a4` | 2026-11-18 | Merge remote-tracking branch 'origin/release/14/plan-59' into p59/recast-rubric |
| release/14/plan-64 | `ed397b266eef` | 2026-11-19 | Merge pull request #440 from banodoco/p64/r1-integrated |
| release/14/plan-65 | `513204189161` | 2026-11-19 | Merge timeline still canvas repair |
| release/14/plan-66 | `ec758a9b86a4` | 2026-11-18 | Merge remote-tracking branch 'origin/release/14/plan-59' into p59/recast-rubric |
| release/14/plan-66-wip/agent-src-main-clone | `15ca752d1da0` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from agent-src-main-clone on task/plan59-shot-trim |
| release/14/plan-66-wip/wt-r14-agentbase | `ed0c6c6e481b` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from wt-r14-agentbase on detached@ec758a9b8 |
| release/14/plan-66-wip/wt-r14-validate-trim | `2bb8c10958c1` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from wt-r14-validate-trim on release/14/validate-trim |
| release/14/plan-69 | `83d5f8fe382e` | 2026-11-21 | Pin the Runtime that verifies CAS objects once per process |
| release/14/pr-template | `360d7533925b` | 2026-11-16 | Add a pull request template that asks which plan or issue the work belongs to |
| release/14/release-tooling | `802377e94de3` | 2026-11-16 | Release tooling follows release/<N>/main |
| release/14/repins | `08b89f0f07da` | 2026-11-18 | test(installer): refresh approved producer path witness identities |
| release/14/runtime-folder-cleanup | `10351e60360a` | 2026-11-17 | test(cleanup): exercise runtime paths on the native host |
| release/14/runtime-pin-66 | `e2a5000720d6` | 2026-11-18 | Pin Runtime release/14/plan-59 4c18af59 (clip list.remove passes commit authentication) |
| release/14/runtime-pin-d725811 | `126f7f26da73` | 2026-11-18 | Pin Runtime commit-cost fix (#59) for Release 14 |
| release/14/runtime-pin-r14b | `ae9c3bb44805` | 2026-11-18 | Pin Runtime release/14/plan-59 e6f4d5c2 and re-vendor its client (selection digest, ancestry proofs, transport) |
| release/14/scene-by-reference | `02c529e5a7f9` | 2026-11-16 | Scene by reference: hand the stored scene to every renderer, keep the snapshot Runtime-owned |
| release/14/short-install-paths | `1e17fc09a547` | 2026-11-16 | Shorten installation directories and project VibeComfy source (#672) |
| release/14/short-result-manifest | `c73043bf8436` | 2026-11-16 | Shorten content-addressed generation manifest paths (#671) |
| release/14/skills-feedback-rubric | `fbe9a5df9f58` | 2026-11-22 | Skills: ask before posting, scrub logs, PR only with the user's OK |
| release/14/sync-plan-39-1119 | `96296e6af5f9` | 2026-11-19 | Sync release/14/main into release/14/plan-39 |
| release/14/task-stall-diagnostics | `1cb63140fb01` | 2026-11-17 | Decouple stall diagnostics from task lease timing |
| release/14/tester-fixes | `71f9f19cf6e8` | 2026-11-16 | Merge release/14/main into release/14/tester-fixes |
| release/14/tls-policy | `a54ce8fbdca1` | 2026-11-18 | Guard raw TLS openings and retain independent contract failure |
| release/14/whisper-disable-fallback | `7a1e919e9132` | 2026-11-21 | Preserve saved transcription defaults during the release holdout |
| release/14/windows-path-budget | `51a74074fb90` | 2026-11-16 | Test default Windows path budgets (#673) |
| release/15/fix-runpod-model-lock-pin | `d35f6d4298e1` | 2026-11-21 | fix RunPod Linux model lock digest pin |
| release/15/forward-14 | `0f118d057fed` | 2026-11-18 | Release 15: bring Release 14 plan-59 forward (today's save and transport fixes) |
| release/15/forward-14-2 | `2b99afde5b5f` | 2026-11-21 | Pin the Runtime on release/15/main (1758a6df) |
| release/15/forward-14-3 | `04af1d2c1cc9` | 2026-11-21 | Release 15: bring release/14/main forward again (R14-FIX-15) |
| release/15/forward-14-4 | `3caced9ac556` | 2026-11-22 | Release 15: keep release/14/main's Runtime pin |
| release/15/forward-14-5 | `14efcd7a7910` | 2026-11-22 | Release 15: bring the published Release 14 forward |
| release/15/main | `8807f820eb47` | 2026-11-22 | Merge pull request #523 from banodoco/release/15/forward-14-5 |
| release/15/plan-13 | `1087ad8d5ab3` | 2026-11-22 | Merge pull request #499 from banodoco/p13/r1-8 |
| release/15/plan-69 | `ac91c9d607bf` | 2026-11-22 | Merge pull request #513 from banodoco/p69/forward-r15-execution-host |
| release/15/plan-69-agent-landing | `ffe659dd5f0b` | 2026-11-22 | Pin Agent locks to landed Release 15 Runtime |
| release/15/plan-77 | `fda019773c55` | 2026-11-22 | Merge pull request #515 from banodoco/p77/round6-current-agent |
| release/15/plan-81 | `9c95c680e645` | 2026-11-22 | Merge pull request #524 from banodoco/p81/attribution-a3-integrated |
| release/15/timeline-archive-copy | `bd28753d23ce` | 2026-11-16 | Merge the cross-project timeline archive import fix (astrid-agent #346) for Release 15 |

### astrid-runtime

| Origin branch | Head | Date | Subject |
|---|---|---|---|
| main | `5120462d6747` | 2026-11-22 | FIX-30: align the media-selection lifecycle test with PR #61 (#93) |
| release/14/926-retry-durable-logs | `bb53f8f67647` | 2026-11-19 | Retain FIX-12 focused, public-log-read, and combined P55-12 proof |
| release/14/ancestry | `efba3b2777e0` | 2026-11-18 | Keep verified history across unrelated writes so an import never forces a re-walk |
| release/14/ci-triggers | `e2f8ef43cc10` | 2026-11-16 | CI: a pull request into a release branch must come from a branch of that release |
| release/14/commit-cost | `3813c8f102df` | 2026-11-18 | Confirm media pins by file identity; one CAS store per commit store; equal stats at 3 and 30 |
| release/14/commit-hook | `cb05b1ef75d5` | 2026-11-18 | Drop the authorizer and tagged-query recheck; keep the hook move |
| release/14/fix25-legacy-transitions | `bcb17ab1af5d` | 2026-11-22 | Distinguish clip IDs from nested effect roles |
| release/14/fix30-commit-port-test | `8239737fca37` | 2026-11-22 | FIX-30: align the media-selection lifecycle test with PR #61 |
| release/14/int-59-64-65 | `0af5af11d710` | 2026-11-21 | Merge commit '7869eb4e472d3d38f21659f6ec3dc3d5e8c4a35e' into release/14/int-59-64-65 |
| release/14/int-fix-commit-wal | `7869eb4e472d` | 2026-11-21 | Re-read once when the counters move after the read snapshot |
| release/14/main | `5120462d6747` | 2026-11-22 | FIX-30: align the media-selection lifecycle test with PR #61 (#93) |
| release/14/member-list-remove | `5f740643557b` | 2026-11-18 | fix(timeline): authenticate member-scoped list.remove effects |
| release/14/plan-39 | `804f87c79416` | 2026-11-21 | Merge pull request #71 from banodoco/p39/runtime-native-inventory |
| release/14/plan-52 | `2537fed24385` | 2026-11-16 | Merge pull request #51 from banodoco/release/14/pr-template |
| release/14/plan-55 | `b35c93ad92cf` | 2026-11-19 | Merge pull request #68 from banodoco/p55/ls-6-remainder |
| release/14/plan-59 | `ee235d39dffa` | 2026-11-18 | Merge pull request #67 from banodoco/release/14/revert-62-retention |
| release/14/plan-66 | `ee235d39dffa` | 2026-11-18 | Merge pull request #67 from banodoco/release/14/revert-62-retention |
| release/14/plan-66-wip/runtime-src-main-clone | `1b3f360837b7` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from runtime-src-main-clone on task/plan59-shot-trim |
| release/14/plan-66-wip/wt-rt-media-digest | `a3acdc5fcf79` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from wt-rt-media-digest on release/14/media-digest-diagnostic |
| release/14/plan-69 | `b2ea261f36f5` | 2026-11-21 | Verify CAS objects once per process; stop re-hashing timeline history |
| release/14/plan-77 | `ee235d39dffa` | 2026-11-18 | Merge pull request #67 from banodoco/release/14/revert-62-retention |
| release/14/plan-77-wip/runtime-src-main-clone | `1b3f360837b7` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from runtime-src-main-clone on task/plan59-shot-trim |
| release/14/plan-77-wip/wt-rt-media-digest | `a3acdc5fcf79` | 2026-11-18 | WIP (handover 18 Nov): uncommitted work from wt-rt-media-digest on release/14/media-digest-diagnostic |
| release/14/pr-template | `50b3e764c0b8` | 2026-11-16 | Add a pull request template that asks which plan or issue the work belongs to |
| release/14/revert-62-retention | `05d1ad887e01` | 2026-11-18 | Revert "Keep verified history across unrelated writes so an import never forces a re-walk" |
| release/14/scene-by-reference | `1c060830b336` | 2026-11-16 | Live-scene clips may omit the inline HTML |
| release/14/selection-digest | `51a417d06cb3` | 2026-11-18 | Re-seed the V33 existing-pins test for identity-only pins |
| release/14/transport | `ad9a052dd9bb` | 2026-11-18 | Runtime transport: reply writer closed flag; e2e serialization test probes /v1/realm |
| release/14/windows-db-mode | `038e0e8cb375` | 2026-11-15 | Trust the timeline memo on Windows by checking the DACL, not POSIX mode bits |
| release/15/forward-14 | `5e46ed2a3f03` | 2026-11-18 | Release 15: bring Release 14 plan-59 forward (today's save and transport fixes) |
| release/15/forward-14-2 | `3f673707209b` | 2026-11-21 | Release 15: bring release/14/main forward |
| release/15/forward-14-4 | `b51d4e56b9d9` | 2026-11-22 | Release 15: bring release/14/main forward (Plans 59, 64 and 65) |
| release/15/forward-14-5 | `3c28211f3cb7` | 2026-11-22 | Release 15: bring the published Release 14 forward |
| release/15/main | `23310dc82876` | 2026-11-22 | Merge pull request #100 from banodoco/release/15/forward-14-5 |
| release/15/plan-69 | `a2b017f1036c` | 2026-11-22 | Merge pull request #95 from banodoco/p69/r23-scoped-element-asset |
| release/15/plan-77 | `0dc004be6131` | 2026-11-22 | Merge pull request #99 from banodoco/p77/checkpoint-loaded-identity |
| release/15/plan-81 | `72b129e5a229` | 2026-11-22 | Merge remote-tracking branch 'origin/release/15/main' into p81/r14-forward |
