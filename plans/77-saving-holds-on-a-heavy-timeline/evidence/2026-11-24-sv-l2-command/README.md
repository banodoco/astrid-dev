# Plan 77 SV-L2 installed App mark measurement

Status: static checks only; this package has not been run. It reuses the retained stopped sandbox (no fresh restore) and measures one repetition on data copies. The measurement tuple is App `7705ebd478368e8de82b80523c2a3eb87868b710`, Agent `096a2fb3536192785fabd33e6673ba8ab4ef5ead` (the existing two-file overlay), and a Runtime SHA supplied as the first command argument, expected to be `eb4e8644e3549c88d5d836cd5738ca75e76d311a`.

## Build the App artifact

The App worktree must already be at the exact SHA, with `node_modules` symlinked to the requalification checkout and `package.json` plus `package-lock.json` byte-identical. No install is needed. Build CPU-only and stop the build if free space drops below 16 GiB; require at least 18 GiB free before starting:

```bash
app=/home/user/codex-run/wt/astrid-app-p77-svl2-7705ebd4
ref=/home/user/codex-run/wt/astrid-app-p77-r7-firstcut-requalification-install
git -C "$ref" worktree add --detach "$app" 7705ebd478368e8de82b80523c2a3eb87868b710
[[ "$(git -C "$app" rev-parse HEAD)" == 7705ebd478368e8de82b80523c2a3eb87868b710 ]]
ln -s "$ref/node_modules" "$app/node_modules"
cmp "$app/package.json" "$ref/package.json"
cmp "$app/package-lock.json" "$ref/package-lock.json"
(( $(df -Pk /home/user | awk 'NR==2 {print $4}') >= 18*1024*1024 ))
cd "$app"
setsid --wait bash -c 'npm run build' >build.log 2>&1 &
build_pgid=$!
while kill -0 "$build_pgid" 2>/dev/null; do
  free_kib=$(df -Pk /home/user | awk 'NR==2 {print $4}')
  if (( free_kib < 16*1024*1024 )); then
    kill -- "-$build_pgid" 2>/dev/null || true
    wait "$build_pgid" || true
    echo "Stopped App build below 16 GiB free: ${free_kib} KiB" >&2
    exit 1
  fi
  sleep 2
done
wait "$build_pgid"
```

The package rechecks these App identities, computes `dist-files.sha256` from this build (not the old App inventory), verifies served assets against it, and recomputes the inventory after the run. The build worktree and dist are about 170 MB. During build and run, stop below 16 GiB free.

## Run once

On the fixture box, from the package directory, with the candidate Runtime ref available in the candidate mirror:

```bash
SV3_APP_DIR=/home/user/codex-run/wt/astrid-app-p77-svl2-7705ebd4 \
SV3_SIGNED_BACKUP=<canonical-signed-v30-backup-directory> \
SV3_RUNTIME_REF=<ref-resolving-to-eb4e8644e3549c88d5d836cd5738ca75e76d311a> \
SV3_AGENT_REF=<ref-resolving-to-096a2fb3536192785fabd33e6673ba8ab4ef5ead> \
SV3_REPETITIONS=1 \
bash run-sv3-overlay.sh eb4e8644e3549c88d5d836cd5738ca75e76d311a <approved-package.sha256-digest>
```

The package itself checks the exact Runtime ref, App SHA, Agent SHA, package digest, and minimum free-space floor before it starts. Output is unique to this App/Runtime tuple at `run/evidence/plan-77/round7-acceptance/sv-l2-app-7705ebd4-runtime-<runtime-sha>/`; an existing output is a refusal. The normal owned stack wrapper starts one copied-data Runtime and preview. No stack build or dependency install is part of the package.

## Fixture, scope and acceptance

The starting data is the retained stopped sandbox from the signed v30 SQLite fixture (300 clips; fixture SHA-256 begins `c0b27bb0`). The retained original is read-only. Each measurement repetition gets a fresh copy. The selected realm is `201c0486-58d8-4d23-b05d-9220c1762120`; starting public head is revision `authoring-parent-revision-5357f6c0f85f6b1edbe53275043432abf63a33f56582ae6f300b06519436acaa`, publication `txn-45427064f4d34b9a840005c774956763`, digest `sha256:75f9d65814ba3b48ca0d0422bf04f28a07178f25931a8c3bd57d582ff06cbaae`. The profiled clip is `fixture-video-0190` on V6, initially at 191.3667 s.

Read scope: retained App/Runtime/Agent source identities, signed backup, retained stack and fixture. Write scope: package output, disposable App build worktree, and fresh per-repetition copies of the fixture data; the retained stack's program and original data are not intentionally changed. Named receipts include `versions.json`, `dist-files.sha256` and `.after.sha256`, `browser-sv3-measure.json`, `measurements.jsonl`, `summary.tsv`, logs, boundary receipts and `SHA256SUMS`.

Before any saves, the browser must open the timeline, become writable within 120 seconds, and read the exact starting verified head. A 409, refusal, wrong head or failure to become writable stops that attempt before scenarios; this is the early wire-compatibility refusal for the unverified App/Runtime pair. HTTP 200 is accepted only when the existing harness also observes the accepted commit and verifies the resulting public head. The four bounded App marks are captured after each sequential Saved as raw `{name,t}` entries and grouped by correlation counter: `astrid.save.<n>.gesture-end`, `.post-sent`, `.200`, `.saved-badge`. The receipt records missing or multiple group ambiguity rather than inferring HTTP acceptance from a mark. Burst marks are snapshotted after the burst settles, with raw entries retained.

The run uses the existing S0, cold/warm save and B5/B10 scenarios, the two-file Agent overlay, one fresh browser profile and owned stack, a 120-second writable deadline, an 18 GiB start floor and a 16 GiB stop floor. Cleanup stops only processes owned by this run, requires idle-safe shutdown, verifies ports and original-data boundary, removes copied data, and writes hashes. It does not replace or consume the retained head.

This is a MEASURE command: the package SHA-256 and full package contents are in this committed directory (`package.sha256` and its referenced files). The command is intended for one box attempt; raw receipts and their hashes return through the host lane.

## Package coverage

`run-sv3-overlay.sh` compares the sorted manifest paths with every regular file in this package directory, excluding only `package.sha256` (the manifest) and `package-digest.txt` (the digest of that manifest). It then verifies the manifest hashes before doing any work. The package files that are executed or imported are:

- `run-sv3-overlay.sh` — entry point.
- `verify-overlay.py` — executed by the shell for boundary checks, preparation, and receipts.
- `overlay-direct.py` — executed as the Runtime CLI wrapper.
- `overlay-guard/sitecustomize.py` — imported by the Runtime Python during startup; witnesses daemon imports and checks overlay selection.
- `browser-sv3-measure.mjs` — browser measurement driver.
- `arm-free-space.mjs` — imported by the browser driver.
- `profile-save-hook.mjs` — imported by the browser driver.
- `reused-trace-helpers.mjs` — imported by the browser driver for pinned browser and fixture helpers.

`approved-input.json` is read as fixed configuration, and `README.md` documents the command; both are hashed as package files. The App, Runtime, Agent, browser tooling checkout, and installed interpreter are external inputs whose identities are checked and recorded by the package.
