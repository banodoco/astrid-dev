# Astrid Release 15 — exploratory Windows tester snapshot (24 November 2026)

**Give this entire page to your coding agent.** This is a frozen **unpublished experimental build** for someone who volunteered to test Astrid and give detailed feedback. It is **not** the public release and **not** a green/Release-Lead-qualified official tester build. Things may fail. We want to learn what actually happens.

**Your coding agent should:** download and verify this frozen build, obtain the tester's consent, follow the [Windows feedback guide](windows-tester-brief.md) and [technical matrix](windows-test-matrix.md), create one GitHub issue for the whole session, and open/link separate issues for independently actionable bugs or friction. Capture positive reactions too. Fixes are optional. **For this specifically requested exploratory run, use this page as the installer/build handoff instead of the tester guide's qualified-bundle requirement; all other consent, protection, baseline, issue, spending and cleanup rules still apply.** Never call this a qualified Release 15 test or claim that the unreleased App UI was tested.

## What is frozen

| Source | Full immutable commit |
| --- | --- |
| App repository supplying installer and manifest (not the tested UI) | [`d53685f3adfc4ed725936b4a9d7ebc435dedbcc0`](https://github.com/banodoco/astrid-app/commit/d53685f3adfc4ed725936b4a9d7ebc435dedbcc0) |
| Installed Agent | [`a09ea669a35a104451e48679e242aeb390a4df58`](https://github.com/banodoco/astrid-agent/commit/a09ea669a35a104451e48679e242aeb390a4df58) |
| Installed Runtime | [`24e2c9291d5bcaface78324696286f2dc896debc`](https://github.com/banodoco/astrid-runtime/commit/24e2c9291d5bcaface78324696286f2dc896debc) |
| VibeComfy pinned by Agent | [`c0e910caab9734a551fb2c1a455fff72c3a1b1cb`](https://github.com/banodoco/VibeComfy/commit/c0e910caab9734a551fb2c1a455fff72c3a1b1cb) |

The App's Release 15 manifest, **at the frozen App commit**, declares release **15**, and its Agent/Runtime/VibeComfy pins agree with the Agent's runtime lock and VibeComfy pin. This is the App's *existing pinned integration snapshot*, **not** a promise that the Agent's moving `release/15/main` branch has no later commits. At snapshot creation the Agent branch was 68 commits ahead; Runtime's release head matched its pinned commit. **No Release 15 green tester-build evidence or real Windows installation proof is claimed here.**

**Pinned source files:**
- [Windows installer `install.ps1`](https://github.com/banodoco/astrid-app/blob/d53685f3adfc4ed725936b4a9d7ebc435dedbcc0/public/install.ps1) — SHA-256 `ea581d5d7c2d02f9f062dc15affabe1f7c3e38d641984cecf4797f13ac58b3a9`.
- [Install manifest `install-manifest.json`](https://github.com/banodoco/astrid-app/blob/d53685f3adfc4ed725936b4a9d7ebc435dedbcc0/public/install-manifest.json) — SHA-256 `d23b2aa8331aca539e9b0aceea676d84297a9f27d5488bca1b16f53010d9a63c`.

## Agent steps

1. **Check first.** Confirm Windows PowerShell, Git for Windows, free disk, GPU and the tester's existing ComfyUI. Detect an existing Astrid/Pinokio install with the [setup skill at the frozen Agent commit](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/packs/setup/docs/SKILL.md). For an existing non-Pinokio install, record version and doctor output, back up work, and obtain explicit consent to install an *unpublished update*. **Do not overwrite a Pinokio-managed install.** If the machine is shared or already in use, first agree on isolation. Do not install without consent, and do not touch pre-existing ComfyUI custom nodes or models.

2. **Download only, then inspect.** In a Windows PowerShell session:

```powershell
$ErrorActionPreference = 'Stop'
$dir = Join-Path $env:TEMP 'astrid-r15-exploratory-a09ea669'
New-Item -ItemType Directory -Force $dir | Out-Null
$base = 'https://raw.githubusercontent.com/banodoco/astrid-app/d53685f3adfc4ed725936b4a9d7ebc435dedbcc0/public'
$installer = Join-Path $dir 'install.ps1'
$manifestFile = Join-Path $dir 'install-manifest.json'
Invoke-WebRequest -UseBasicParsing "$base/install.ps1" -OutFile $installer
Invoke-WebRequest -UseBasicParsing "$base/install-manifest.json" -OutFile $manifestFile
$expected = @{
  'install.ps1' = 'ea581d5d7c2d02f9f062dc15affabe1f7c3e38d641984cecf4797f13ac58b3a9'
  'install-manifest.json' = 'd23b2aa8331aca539e9b0aceea676d84297a9f27d5488bca1b16f53010d9a63c'
}
foreach ($name in $expected.Keys) {
  $hash = (Get-FileHash (Join-Path $dir $name) -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($hash -ne $expected[$name]) { throw "Digest mismatch for $name; stop and report" }
}
$m = Get-Content -Raw -Encoding UTF8 $manifestFile | ConvertFrom-Json
if ($m.release -ne 15 -or
    $m.agent.sha -ne 'a09ea669a35a104451e48679e242aeb390a4df58' -or
    $m.runtime.sha -ne '24e2c9291d5bcaface78324696286f2dc896debc' -or
    $m.vibecomfy.sha -ne 'c0e910caab9734a551fb2c1a455fff72c3a1b1cb') {
  throw 'Manifest source identity mismatch; stop and report'
}
"Verified frozen experimental Release 15 snapshot in $dir"
```

3. **Install with consent, not automatically.** Read the downloaded script and present the plan. Use a normal PowerShell window, **not Astrid's own chat**, so restarting Astrid cannot terminate the operation. Do *one* route:

   - **Existing ordinary Astrid install, after consent and backup:** `powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer --update --manifest $manifestFile`.
   - **No existing install, after consent and setup choices:** `powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer --manifest $manifestFile --yes --autostart on --command on --skills on --skill-copies off`.

   The choices in the fresh-install example are Astrid defaults; present them to the tester first and honor requested changes. **Do not use the normal astrid.haus install command**: that installs the published release. On any installer error record the exact message and log path, don't silently fall back. After installation, verify that the **active** Agent/Runtime/VibeComfy tuple matches the three commits above; a retained old folder or a successful installer exit alone does not establish this.

4. **Use and report.** Follow the [short tester guide](windows-tester-brief.md) and the [technical matrix](windows-test-matrix.md), with the frozen Agent's [setup](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/packs/setup/docs/SKILL.md), [generation](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/packs/generation/docs/SKILL.md) and (only if paid use is separately approved) [RunPod](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/packs/runpod/docs/SKILL.md) skills. Record test cells separately from free-form creative exploration; include timing, awkward moments, successes, failed or skipped steps and exact active SHAs. Clearly mark the issue **"Exploratory pre-release build, not formally qualified; served App UI not tested"**. Search before opening separate issues. Show the tester all redacted public submissions before posting.

5. **Finish safely.** Collect diagnostics, issues and optional patches; preserve the unmodified build as the baseline. Ask whether the tester wants to keep the experimental installation or restore their earlier one via the supported route. Don't delete existing data or models. If RunPod was approved, verify billing really stopped before finishing.

**If the download, SHA-256 check, install or active-source verification fails, STOP that path and report it on the tester's session issue. That is useful evidence, not permission to bypass verification.**
