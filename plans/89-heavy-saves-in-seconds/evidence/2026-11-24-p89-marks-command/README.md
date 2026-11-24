# Plan 89 installed save measurement (SV-L2 marks, SV-L5..L10 Runtime)

Status: static checks only; this package has not been run. It reuses the retained stopped sandbox (no fresh restore) and measures one repetition on data copies. The measurement tuple is App `092013f3b88e9d49e48102630951a40a450c4868`, Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` (the existing two-file overlay), and a Runtime SHA supplied as the first command argument, expected to be `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1`.

## Build the App artifact

From this package directory, the App worktree must already be at the exact SHA, with `node_modules` symlinked to the requalification checkout and `package.json` plus `package-lock.json` byte-identical. No install is needed. Build CPU-only and stop the build if free space drops below 16 GiB; require at least 18 GiB free before starting:

```bash
app=/home/user/codex-run/wt/astrid-app-p89-092013f3
ref=/home/user/codex-run/wt/astrid-app-p77-r7-firstcut-requalification-install
git -C "$ref" worktree add --detach "$app" 092013f3b88e9d49e48102630951a40a450c4868
[[ "$(git -C "$app" rev-parse HEAD)" == 092013f3b88e9d49e48102630951a40a450c4868 ]]
ln -s "$ref/node_modules" "$app/node_modules"
cmp "$app/package.json" "$ref/package.json"
cmp "$app/package-lock.json" "$ref/package-lock.json"
(( $(df -Pk /home/user | awk 'NR==2 {print $4}') >= 18*1024*1024 ))
bash ./build-app-svl2.sh "$app" "$ref"
```

The build helper pins the App commit and original Vite config hash, checks the reference checkout and dependency symlink, then temporarily adds only a `cacheDir` override pointing inside the disposable App worktree. Vite is 5.4.21 per the App lockfile; its config bundler's temporary module is written beside the config file in the disposable App worktree and removed after loading, before the cache setting is available. The original config is restored on success, failure, interrupt, or termination and its pinned hash is checked. The helper snapshots the reference `node_modules` tree (entry type, size, symlink target, and ctime/mtime for every entry) before and after the build and fails if it changed; before and after digests are recorded in `build-node-modules-guard.json`. It logs to `build-svl2.log`, enforces the same 18 GiB start and 16 GiB stop floors, and removes its temporary cache after build. No install is run. The package rechecks these App identities, computes `dist-files.sha256` from this build (not the old App inventory), verifies served assets against it, and recomputes the inventory after the run. The build worktree and dist are about 170 MB. During build and run, stop below 16 GiB free.

## Run once

On the fixture box, from the package directory, with the candidate Runtime ref available in the candidate mirror:

```bash
SV3_APP_DIR=/home/user/codex-run/wt/astrid-app-p89-092013f3 \
SV3_SIGNED_BACKUP=<canonical-signed-v30-backup-directory> \
SV3_RUNTIME_REF=<ref-resolving-to-c8b861c770aa58fd0392fe2dcefbda9ce23c84d1> \
SV3_AGENT_REF=<ref-resolving-to-096a2fb3536192785fabd33e6673ba8ab4ef5ead> \
SV3_REPETITIONS=1 \
bash run-sv3-overlay.sh c8b861c770aa58fd0392fe2dcefbda9ce23c84d1 <approved-package.sha256-digest>
```

The package itself checks the exact Runtime ref, App SHA, Agent SHA, package digest, and minimum free-space floor before it starts. Output is unique to this App/Runtime tuple at `run/evidence/plan-77/round7-acceptance/p89-app-092013f3-runtime-<runtime-sha>/`; an existing output is a refusal. The normal owned stack wrapper starts one copied-data Runtime and preview. No stack build or dependency install is part of the package.

## Fixture, scope and acceptance

The starting data is the retained stopped sandbox from the signed v30 SQLite fixture (300 clips; fixture SHA-256 begins `c0b27bb0`). The retained original is read-only. Each measurement repetition gets a fresh copy. The selected realm is `201c0486-58d8-4d23-b05d-9220c1762120`; starting public head is revision `authoring-parent-revision-5357f6c0f85f6b1edbe53275043432abf63a33f56582ae6f300b06519436acaa`, publication `txn-45427064f4d34b9a840005c774956763`, digest `sha256:75f9d65814ba3b48ca0d0422bf04f28a07178f25931a8c3bd57d582ff06cbaae`. The profiled clip is `fixture-video-0190` on V6, initially at 191.3667 s.

Read scope: retained App/Runtime/Agent source identities, signed backup, retained stack and fixture. Write scope: package output, disposable App build worktree, and fresh per-repetition copies of the fixture data; the retained stack's program and original data are not intentionally changed. Named receipts include `versions.json`, `dist-files.sha256` and `.after.sha256`, `browser-sv3-measure.json`, `measurements.jsonl`, `summary.tsv`, logs, boundary receipts and `SHA256SUMS`.

Before any saves, the browser must open the timeline, become writable within 120 seconds, and read the exact starting verified head. A 409, refusal, wrong head or failure to become writable stops that attempt before scenarios; this is the early wire-compatibility refusal for the unverified App/Runtime pair. The SV-4 harness tape was written against App 148eaf38 and has not been verified against App #377 (9f26112d), including its changed toolbar/badge DOM and `data-timeline-save-status`. If the tape cannot arm or its first drag fails, the run stops at the cold save and retains only the S0 and App build receipts; it does not proceed to warm or burst scenarios. HTTP 200 is accepted only when the existing harness also observes the accepted commit and verifies the resulting public head. The four bounded App marks are captured after each sequential Saved as raw `{name,t}` entries and grouped by correlation counter: `astrid.save.<n>.gesture-end`, `.post-sent`, `.200`, `.saved-badge`. The receipt records missing or multiple group ambiguity rather than inferring HTTP acceptance from a mark. Burst marks are snapshotted after the burst settles, with raw entries retained.

The run uses the existing S0, cold/warm save and B5/B10 scenarios, the two-file Agent overlay, one fresh browser profile and owned stack, a 120-second writable deadline, an 18 GiB start floor and a 16 GiB stop floor. Cleanup stops only processes owned by this run, requires idle-safe shutdown, verifies ports and original-data boundary, removes copied data, and writes hashes. It does not replace or consume the retained head.

This is a MEASURE command: the package SHA-256 and full package contents are in this committed directory (`package.sha256` and its referenced files). The command is intended for one box attempt; raw receipts and their hashes return through the host lane.

## Package coverage

`run-sv3-overlay.sh` compares the sorted manifest paths with every regular file in this package directory, excluding only `package.sha256` (the manifest) and `package-digest.txt` (the digest of that manifest). It then verifies the manifest hashes before doing any work. The package files that are executed or imported are:

- `run-sv3-overlay.sh` — entry point.
- `build-app-svl2.sh` — isolated App build helper; temporarily overrides only Vite's cache directory and guards/restores the shared dependency tree.
- `verify-overlay.py` — executed by the shell for boundary checks, preparation, and receipts.
- `overlay-direct.py` — executed as the Runtime CLI wrapper.
- `overlay-guard/sitecustomize.py` — imported by the Runtime Python during startup; witnesses daemon imports and checks overlay selection.
- `browser-sv3-measure.mjs` — browser measurement driver.
- `arm-free-space.mjs` — imported by the browser driver.
- `profile-save-hook.mjs` — imported by the browser driver.
- `reused-trace-helpers.mjs` — imported by the browser driver for pinned browser and fixture helpers.

`approved-input.json` is read as fixed configuration, and `README.md` documents the command; both are hashed as package files. The App, Runtime, Agent, browser tooling checkout, and installed interpreter are external inputs whose identities are checked and recorded by the package.

## Plan 89 changes from the SV-L2 package (24 November 2026)

This package is the SV-L2 command package with only these edits: App `092013f3b88e9d49e48102630951a40a450c4868` (release/15/plan-89 with #377 merged; `package.json`, `package-lock.json` and `config/vite/vite.config.ts` byte-identical to the SV-L2 App `7705ebd4`: sha256 of the Vite config begins `b5a636d3`), Runtime `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1` (release/15/plan-89: history guards, covers index, deferred history scan with its authority fix, subtree validation memo; `pyproject.toml`, `uv.lock` and `contract/` have an empty diff against the retained Runtime `77c38d03`), the output directory name `p89-app-092013f3-runtime-<sha>`, and the pinned SHAs in `build-app-svl2.sh`, `run-sv3-overlay.sh` and `browser-sv3-measure.mjs`. The Agent overlay stays the proven two-file `096a2fb3` overlay: Agent `release/15/plan-89` (`e3da121f`) changes 25 files beyond those two (an installer rollback hook, pins and docs), so this run measures the Runtime and App changes plus the Agent capture fix, not the Agent rollback hook.
Expected effect: warm save POST-to-200 and gesture-end-to-Saved shorter than the 24 November baselines (5.1 s and 6.15 s); SV-L10 removes about half of the PreparedCommit schema time. S0 now includes the startup path of the new Runtime: if the realm's history scan finishes inside the 120 s admission deadline it behaves as before; if not, the editor opens read-only (`/v1/health` lists the service `realm-history-verification` with "(N/M history rows checked)", and a write returns 409 `realm_admission_failed` "verification in progress, retry in a moment") and the 120-second writable deadline then fails the attempt as a refusal result; that is a finding, not a retry. The PreparedCommit schema time per save is not emitted in the timing line; only the profile variant (`SV3_PROFILE=1`) can attribute it.

## Variant for per-stage attribution of the editor save (SV-L13), 24 November 2026

Same package as `2026-11-24-p89-measure-command` (the 54-save Release 15 measurement), with ONLY the App SHA changed to astrid-app draft PR #395 head `092013f3b88e9d49e48102630951a40a450c4868` (SV-L2 marks plus about 40 additional instrumentation-only User Timing marks for the pre-POST and post-200 stages; base `release/15/plan-89` 9f26112d; `package.json`, `package-lock.json` and `config/vite/vite.config.ts` byte-identical to 9f26112d) and the output directory name `p89-app-092013f3-runtime-<sha>`. The driver already retains the raw `{name,t}` entries of every `astrid.save.*` mark after each Saved (`captureSaveMarks`, `raw`), including the new phase names, so no driver change is needed; the per-stage analysis reads the raw entries. Runtime stays `c8b861c770aa58fd0392fe2dcefbda9ce23c84d1` (command argument), Agent the two-file `096a2fb3` overlay. One repetition (19 saves) is enough: the analysis takes per-stage medians over the 18 warm saves; marks are bounded to 16 correlations, so the raw entries must be read after each save, as the driver does.
