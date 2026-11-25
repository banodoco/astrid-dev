# Prepare the current Release 15 testing build

**For the tester's coding agent:** Start at the [tester brief](windows-tester-brief.md), then use this self-service procedure before the [technical matrix](windows-test-matrix.md). No separate maintainer-provided manifest, write credential or old tester branch is needed. Preparation is read-only; get the tester's consent before changing their machine or publishing feedback. A self-prepared build is exploratory unless its exact tuple has recorded qualification and explicit tester-build approval.

## Resolve and freeze

1. For a fresh session resolve the full current heads of `release/15/main` in [astrid-app](https://github.com/banodoco/astrid-app/tree/release/15/main) and [astrid-agent](https://github.com/banodoco/astrid-agent/tree/release/15/main), e.g. `git ls-remote https://github.com/banodoco/astrid-app.git refs/heads/release/15/main`. Use full immutable commits for all subsequent downloads. For a resumed session use the saved manifest/receipt, not the latest heads. If the release branches have been retired, report that and use a recorded exact snapshot only with the tester's agreement; check whether it has since published.
2. Download the selected App commit's `public/install-manifest.json` and matching `public/install.ps1` (Windows) or `public/install` (Linux) into a new scratch directory. Obtain `scripts/installer/pin.mjs` at the same App SHA. Read the scripts before running them. Raw file URL format: `https://raw.githubusercontent.com/banodoco/astrid-app/<full-app-sha>/<path>`. Do not use the public site's manifest or the old `windows/tester-*` branches.
3. Verify the manifest's integer release is 15, its full Agent SHA is on the selected Agent release branch, the Runtime SHA matches the Agent's `runtime.lock.json`, and VibeComfy/lifecycle match the Agent's `astrid/packs/runpod/pins.json`. Verify pack/tool/installer compatibility against the pinned sources. App's `runtime.lock.json` must agree for an integrated claim. Use Node to run the pinned existing checker in the scratch directory:

   ```text
   node pin.mjs --in install-manifest.json --check
   ```

   Obtain consent for any prerequisite installation. A missing validator, inconsistent pins or unavailable source is a blocker, not permission to bypass checks.
4. If the App manifest already pins the current Agent head and is coherent, use its exact bytes. If it lags, tell the tester and default to the latest coherent App-pinned snapshot. If the tester explicitly prefers the newest Agent head, prepare a separate **installed-side-only exploratory snapshot** using the Release 15 base manifest (copy it as `base-install-manifest.json`) and the pinned generator:

   ```text
   node pin.mjs --in base-install-manifest.json --out install-manifest.json <full-agent-sha>
   node pin.mjs --in install-manifest.json --check
   ```

   This derives the Agent's Runtime/schema/VibeComfy/lifecycle pins; it does not set the release integer, all pack/tool pins or certify App compatibility. Verify those separately; do not install if coherence cannot be established. Do not manually change the release integer or required-update policy to make a build work.
5. Save the exact manifest, platform bootstrap, their SHA-256 hashes, all source pins, observed branch heads/time, and qualification status in the session receipt. Keep the installed test unmodified. Never write a tester artifact into public installer locations or claim the served editor is the unreleased UI.

### Verified starting point, 25 November 2026

At inspection, the App and Agent release heads matched the [Lead's named candidate](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7170081785): App `cc1d48f016fde55ad6b0609c619d8a4bcec56823`, Agent `dc45d97c6bc2734cbfb9b2a25b43cb40ed5757e5`, Runtime `686ca695469bda48cd40a70824c4ccef2a137284`, VibeComfy `55c3948212d23cf037fae8a4c6faad77d33e7279`. The manifest declares 15 and its source pins match the Agent locks. The [qualification verdict](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7172609349) reports Tier 1 met, with Windows tester evidence not run. The files are directly available:

- [Manifest](https://raw.githubusercontent.com/banodoco/astrid-app/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install-manifest.json)
- [Windows installer](https://raw.githubusercontent.com/banodoco/astrid-app/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install.ps1)
- [Linux installer](https://raw.githubusercontent.com/banodoco/astrid-app/cc1d48f016fde55ad6b0609c619d8a4bcec56823/public/install)

This is a recorded reference, not a moving latest pointer. Resolve fresh heads for new sessions. No new local tester run or separate approved tester bundle is claimed here.

## Install after consent

Use the [setup skill](https://github.com/banodoco/astrid-agent/blob/release/15/main/astrid/packs/setup/docs/SKILL.md) at the exact selected Agent commit for ownership detection, choices, backups and safe restoration. Never overwrite Pinokio or use a custom root as supposed service isolation. Show the plan, ask explicit permission, record pre-install doctor and backup. Run from a native terminal outside Astrid chat, in the directory with the verified files.

Windows PowerShell, existing normal install:
```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 --update --manifest .\install-manifest.json
```

Linux shell, existing normal install:
```sh
sh ./install --update --manifest ./install-manifest.json
```

For a fresh install on either platform, omit `--update` and present the normal setup choices; keep the explicit `--manifest`. Do not use fresh flags on an existing install. Record exit/output, elapsed time, log location and actual active identities. If a second snapshot with release number 15 is reported already current but active SHAs differ, record BLOCKED and the exact receipt; never force a version bump, uninstall data or bypass installer verification. If the active tuple is wrong or unverified, stop before claiming a generation test.

## Test the pinned frontend

The manifest installs Agent/Runtime, not the editor code. After verifying the active tuple, follow [the frontend testing guide](frontend-testing.md) using the exact compatible App SHA in this receipt. This is the supported local editor route, not the macOS-only isolated release-stack developer tool. Record any blocker independently; CLI-only success is not full-stack success.

## Linux test adapter

Use a native Linux shell. Record distribution, kernel, GPU/VRAM/driver, RAM, storage, Python/ComfyUI environment, service state and exact placement. Use a new scratch directory, for example `mktemp -d "$HOME/astrid-test.XXXXXXXX"`, with a `report` subdirectory. Keep the same test cell IDs, inputs, seeds, timing and result semantics as the matrix. Replace its Windows paths and PowerShell launcher syntax with native paths and shell quoting. For a normal install:

```sh
astrid="${XDG_DATA_HOME:-$HOME/.local/share}/astrid/run-astrid"
"$astrid" doctor --json
"$astrid" generate scan --json
"$astrid" generate targets --json
"$astrid" generate defaults --json
```

Inspect the selected active version's manifest and installer receipt under the actual program root; do not accept an inactive version directory as proof. Inspect service/log state using doctor and the actual installed user service (systemd where available). Record local source proof and selected ComfyUI URL. For example, the matrix's A/A2 uses `"$astrid" generate image` with its exact arguments and native `--out` paths. Use `curl -L -C - -o <file> <url>` for approved resumable downloads. Optional disposable ComfyUI/audio/video must use a separately verified native environment; skip cells if no compatible recipe is established. Remote results do not prove local Linux or Windows.

For cleanup, run `"$astrid" doctor --bundle <report-directory>/astrid-doctor.zip` before uninstall or restoration; preserve the exact manifest/receipt and redacted logs. Use the supported platform restore/uninstall route only with consent, keeping data. Record remaining program files, service/launcher, models added or retained and any unresolved billing. Create a ZIP of the redacted report (e.g. with Python's shutil.make_archive), review it with the tester and attach to the session issue. Never delete pre-existing models or projects.

The standing testing procedure is to be made release-independent in [Plan 31](../../../plans/31-releases-from-astrid-dev/plan.md), RL-1e.
