# Astrid on Windows: Release 15 main technical test run

**Give this whole document to your coding agent.** It tests the **unpublished** Release 15 development branches (not the public installer release). It downloads about 32 GB of models in the core run and optionally much more. **First create a GitHub issue for the test (Part 0)**. Delete only files this test added.

| | |
|---|---|
| Your GitHub issue | **Create your own before starting** (Part 0); record the URL |
| Build under test | Agent and Runtime at **release/15/main** (exact frozen commits); VibeComfy from the Agent's pinned revision |
| You need | Windows 10/11, NVIDIA GPU, ComfyUI, Git for Windows, Python 3, GitHub access, 40 GB free disk |

## What this is

A technical check that the latest Agent and Runtime **release/15/main** development heads install or update and generate on a real Windows machine using the person's own ComfyUI. **The standard astrid.haus installer alone does NOT install Release 15:** it selects the published release. We use the real Windows installer with an explicit candidate manifest selecting frozen development sources. This guide tests the CLI and ComfyUI; it does **not** qualify the Release 15 App or public website. Aside from creating the issue, testing is command line; skip browser or astrid.haus onboarding prompts.

We want to know what works, what fails, and the exact error when it fails. A failure is a useful result.

- **Done** means Part 0 (issue), Parts 1–4, clean-up and a posted final issue report. Part 5 is optional.
- **If issue creation, source pin resolution, installation, or active-build verification fails:** report the exact blocker on the issue and stop the affected path. A default published-release run does not count as Release 15.
- **Don't fight one cell for more than 15 minutes** (downloads don't count). Report it and move on.

## Ground rules

1. **Get one explicit approval** before installing an unpublished build, updating an existing installation or downloading large model files. State the disk/download budget, check free space and clean up only test-added files. Never delete any pre-existing models.
2. **Never install node packs or Python packages into the person's ComfyUI.** Adding model files to it is fine.
3. **Spend no money.** Never use a RunPod or other paid option, even if Astrid offers one.
4. **Fix small Astrid problems that block you, and share the fix.** If a small change to Astrid's installed code gets a step working (a wrong path, a quoting bug, a missing Windows case), make it, keep going, and add the exact diff to `fixes.diff` straight away. Keep fixes minimal, and say in the cell table which cells ran on patched code. If Astrid then refuses to run because its own files changed, undo the change and report both. If it needs more than a small change, report it and move on. Don't work around an Astrid problem by changing the person's ComfyUI. A fix here lasts only until the next update, so it must be in the report to count.

**Shell.** Use Windows PowerShell, not WSL. No admin rights are needed. If your shell doesn't keep variables between commands, or isn't PowerShell, put each block in a `.ps1` file and run `powershell -NoProfile -ExecutionPolicy Bypass -File <file>`. The install, the downloads and the video cells run longer than most command time limits: run them in the background and poll.

**Records.** Everything goes in one folder, `C:\astrid-test\report`, which you zip and attach at the end:

- `report.md`: the GitHub issue URL, frozen Agent/Runtime/VibeComfy SHAs and manifest hash, plus notes as you go. For anything that fails or surprises you: the command, the exact error and the task ID. Also a plain list of **every file or folder this test adds outside `C:\astrid-test`;** the clean-up works from that list.
- `log.txt`: every command you run and its full output, appended as you go.
- `fixes.diff`: any change you made to Astrid.
- the diagnostics bundle and the images from A and B (part 6).

Keep tokens out of everything in the report folder. Do not keep raw credentials in the logs.

## Part 0: Create the GitHub test issue — required

**Do this before changing Astrid or downloading models.** Each tester creates one issue for their own Release 15 Windows test in [banodoco/astrid-dev](https://github.com/banodoco/astrid-dev/issues). Reuse your existing issue if resuming the same run; **do not create one issue per failed cell**.

1. Run gh auth status and gh issue list --repo banodoco/astrid-dev --search "Release 15 Windows test". If you already own an issue for this run, reuse it.
2. Otherwise, create the issue with this command (install and authenticate the GitHub CLI first):

~~~powershell
New-Item -ItemType Directory -Force 'C:\astrid-test\report' | Out-Null
@'
### What I saw

Beginning a real-Windows test of unpublished Release 15 Agent and Runtime branches.
Exact source pins, test results, failures and diagnostics will be added here.

### Astrid version

Release 15: release/15/main (exact pinned SHAs to follow).
'@ | Set-Content 'C:\astrid-test\report\issue-body.md'
gh issue create --repo banodoco/astrid-dev --title "observation: Release 15 Windows test started" --body-file 'C:\astrid-test\report\issue-body.md'
~~~

3. Record the returned issue URL at the top of report.md. If the CLI cannot create issues, ask the person to create an [observation issue](https://github.com/banodoco/astrid-dev/issues/new?template=observation.yml) in their browser and give you its URL. **Do not proceed until an actual issue URL exists.**
4. Post a STARTED comment with Windows edition, GPU/VRAM, fresh-install or update, and planned scope. Do not disclose private names or paths. After Part 2, add the frozen SHAs and manifest digest. Keep all results, exact errors, task IDs and the final ZIP on **this same issue**.

For questions, post a comment beginning QUESTION:. If the agent cannot post, the person can paste the comment. Keep tokens and personal data out of issue text and logs.


## Part 1: The machine

Record: Windows and PowerShell versions; GPU, VRAM and driver (`nvidia-smi`); RAM; free disk; how ComfyUI is installed (portable, desktop app, Stability Matrix, Pinokio, git), its version and its address; whether Astrid was already installed; which agent you are.

## Part 2: Install or update to frozen Release 15 main

**The published manifest is not Release 15.** Select development commits explicitly, using the [documented local-source installer route](https://github.com/banodoco/astrid-agent/blob/release/15/main/docs/setup/local-source-install.md#developer-qualification-with-local-git-sources). No branch name or shortened SHA is a valid installer source pin.

**Before changing an existing install:** record its doctor output and active version, request the person's explicit permission for an **unpublished in-place update**, and back up existing projects using Astrid's supported method. An installer with a custom program root still registers the Windows background service/scheduled task; **do not assume it is isolated** from an existing installation. If permission is refused, or this is a Pinokio installation without an approved migration, record SKIPPED on the test issue and stop. Never delete projects or uninstall to make the test pass.

### 2A. Obtain and freeze exact source commits

Use Windows PowerShell with Git for Windows. This creates scratch clones and captures their current Release 15 heads. The pinned revisions remain constant throughout this test, even if the branches move.

~~~powershell
$root = 'C:\astrid-test'
New-Item -ItemType Directory -Force "$root\source", "$root\serve", "$root\report" | Out-Null
$agentRepo = "$root\source\astrid-agent"
$runtimeRepo = "$root\source\astrid-runtime"
$vibeRepo = "$root\source\VibeComfy"

git clone --branch release/15/main --single-branch https://github.com/banodoco/astrid-agent.git $agentRepo
if ($LASTEXITCODE -ne 0) { throw 'Agent clone failed' }
git clone --branch release/15/main --single-branch https://github.com/banodoco/astrid-runtime.git $runtimeRepo
if ($LASTEXITCODE -ne 0) { throw 'Runtime clone failed' }

$agentSha = (git -C $agentRepo rev-parse HEAD).Trim()
$runtimeSha = (git -C $runtimeRepo rev-parse HEAD).Trim()
$vibePin = (Get-Content "$agentRepo\astrid\packs\runpod\pins.json" -Raw | ConvertFrom-Json).sources.vibecomfy
$vibeSha = $vibePin.revision
git clone $vibePin.repository $vibeRepo
if ($LASTEXITCODE -ne 0) { throw 'VibeComfy clone failed' }
git -C $vibeRepo checkout --detach $vibeSha
if ($LASTEXITCODE -ne 0) { throw 'VibeComfy checkout failed' }
if ((git -C $vibeRepo rev-parse HEAD).Trim() -ne $vibeSha) { throw 'VibeComfy pin mismatch' }
"Agent: $agentSha"
"Runtime: $runtimeSha"
"VibeComfy: $vibeSha"
~~~

Confirm each is a **full 40-character commit** in the expected repo, and record exact SHAs, remotes, observation time and clean/dirty state in report.md and a comment on the issue. The App head is separate: this command-line test does **not** validate App or UI. Stop if any clone or pin validation fails; do not substitute the published-release source.

### 2B. Build a local candidate installer manifest

Download the published install manifest **only as a template**. Retain its schema_version, tools, dependency hashes and other unrelated fields. Replace the source entries with the exact frozen local checkouts. This does not change the published manifest or its users.

~~~powershell
Invoke-WebRequest 'https://astrid.haus/install-manifest.json' -OutFile "$root\report\published-install-manifest.json"
$m = Get-Content "$root\report\published-install-manifest.json" -Raw | ConvertFrom-Json
if (-not $m.schema_version -or -not $m.tools -or -not $m.agent -or -not $m.runtime) {
    throw 'Unexpected installer manifest schema; stop and report'
}
$m.agent.sha = $agentSha
$m.agent | Add-Member -NotePropertyName repo -NotePropertyValue $agentRepo -Force
$m.runtime.sha = $runtimeSha
$m.runtime | Add-Member -NotePropertyName repo -NotePropertyValue $runtimeRepo -Force
if ($null -eq $m.vibecomfy) {
    $m | Add-Member -NotePropertyName vibecomfy -NotePropertyValue ([pscustomobject]@{}) -Force
}
$m.vibecomfy | Add-Member -NotePropertyName sha -NotePropertyValue $vibeSha -Force
$m.vibecomfy | Add-Member -NotePropertyName repo -NotePropertyValue $vibeRepo -Force
$json = $m | ConvertTo-Json -Depth 60
[System.IO.File]::WriteAllText("$root\serve\local-install-manifest.json", $json, (New-Object System.Text.UTF8Encoding($false)))
Get-FileHash "$root\serve\local-install-manifest.json" -Algorithm SHA256
~~~

Verify the three full source pins and absolute local paths. Record the local manifest SHA-256 and the original published source pins. If validation fails, report and stop; never disable installer verification or change locked tool versions to make it proceed.

### 2C. Run the supported installer with the candidate override

Start a **separate PowerShell window** and leave the manifest server running:

~~~powershell
python -m http.server 17605 --bind 127.0.0.1 --directory C:\astrid-test\serve
~~~

In the test PowerShell session, set the override, then run **exactly one** installer command below, from the terminal and not from inside an Astrid chat:

~~~powershell
$env:ASTRID_INSTALL_MANIFEST_URL = 'http://127.0.0.1:17605/local-install-manifest.json'

# ONLY on a computer with no existing Astrid install:
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --yes --autostart on --command on --skills on --skill-copies off

# INSTEAD, for an existing non-Pinokio install after consent and backup:
# & ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --update
~~~

For an update use --update, not fresh-install flags, to preserve saved choices and exercise backup/rollback. Record first summary line, install duration, errors, backup state and exact log paths (normally under %LOCALAPPDATA%\Astrid Runtime\logs). Do **not** remove ASTRID_INSTALL_MANIFEST_URL before the install; the override is what makes this a Release 15 run. Stop the local manifest server after installation.

**Verify the ACTIVE installed tuple, not just a retained old version folder.** Collect the installed doctor output, the selected version's manifest/installer receipt, and all manifest paths:

~~~powershell
$astrid = "$env:LOCALAPPDATA\Astrid\run-astrid.cmd"
& $astrid doctor --json
Get-ChildItem "$env:LOCALAPPDATA\Astrid\versions\*\manifest.json" -ErrorAction SilentlyContinue | ForEach-Object {
    [pscustomobject]@{ Path = $_.FullName; Manifest = (Get-Content $_ -Raw | ConvertFrom-Json) }
} | ConvertTo-Json -Depth 20
~~~

Compare the **active** Agent, Runtime and VibeComfy installed source identities with the exact frozen SHAs. A matching commit in an *inactive* old version directory is not sufficient. If the active tuple cannot be established, mark UNVERIFIED, post diagnostic evidence to the issue, and do not run generation claiming Release 15. If an installed CLI command differs from this guide, capture --help and the difference; never silently switch to a cloud backend.

## Part 3: Connect ComfyUI

With the person's ComfyUI running:

```powershell
& $astrid generate scan --json                     # add --ports 8188,8000,<port> if it finds nothing
& $astrid generate settings set placement http://127.0.0.1:<port>
& $astrid generate defaults --json
```

Record what the scan found against what is really there, and the `defaults` output: it says which defaults this ComfyUI is ready for.

## Part 4: The core cells

`$url` is the ComfyUI address. Work in `C:\astrid-test`.

**Models for A and B** (about 17 GB, shared). Astrid plans the download and writes nothing until you confirm:

```powershell
& $astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url $url --json
& $astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url $url --apply <plan_sha256> --json
```

Record the plan (files, sizes, folder) in your list of added files. If the download is interrupted, run it again; it resumes.

```powershell
# A: image from text
& $astrid generate image --entry qwen-image-2.1-turbo --mode t2i --prompt "A red bicycle leaning against a white wall in soft morning light" --width 768 --height 768 --seed 7 --placement $url --out C:\astrid-test\A --json
# A2: the same with --seed 8 and --out C:\astrid-test\A2, straight after A. Record both times.
# B: edit the image from A
& $astrid generate image --entry qwen-image-2.1-turbo-edit --mode edit --prompt "Repaint the bicycle frame a deep cobalt blue; keep everything else unchanged" --edit "<image from A>" --placement $url --out C:\astrid-test\B --json
# C: music (uses nodes built into ComfyUI)
& $astrid generate audio --entry audio/ace_step_1_5_t2a_song --mode music --prompt "A calm instrumental piece with soft piano and light strings" --input "lyrics=[instrumental]" --seed 7 --placement $url --out C:\astrid-test\C --json
```

Astrid can't fetch the music models. Run C once and record the message. Then fetch these four files (14.7 GB) from `Comfy-Org/ACE-Step-1.5` into the ComfyUI models folder, in the subfolders shown, and run C again:

`diffusion_models/acestep_v1.5_turbo.safetensors`, `vae/ace_1.5_vae.safetensors`, `text_encoders/qwen_0.6b_ace15.safetensors`, `text_encoders/qwen_4b_ace15.safetensors`

A resumable download that ships with Windows (in the repository these files sit under `split_files/`):

```powershell
curl.exe -L -C - -o "<models folder>\<subfolder>\<file>" "https://huggingface.co/Comfy-Org/ACE-Step-1.5/resolve/main/split_files/<subfolder>/<file>"
```

**Do not inherit Release 13 exemptions.** Record A/A2 cold and warm wall times, overhead, download coverage and image-to-video first-frame behavior. Report real problems even if they were known in Release 13. Check entry IDs and CLI flags against the **installed** Release 15 --help/defaults; if an example was removed, report its replacement rather than silently using another model or paid backend.

**Two no-download preflight checks.** Run cells D and E from Part 5 against `$url`, using A for E. Record whether they run or refuse and whether the actual messages name any missing nodes/models correctly. Do not assume Release 15 must refuse just because Release 13 did.

**For each cell record:** `cell | ran / refused / failed / skipped | wall time | task ID | note`. For "ran", look at the image yourself; for audio and video give the file size and duration, or ask the person to play it. For "failed", add `& $astrid tasks show <task id> --json`. If a job shows no sign of progress for 10 minutes (20 for video), cancel it with `& $astrid tasks cancel <task id>` and record that.

## Part 5 (optional): speech, sound effects and video

These need custom node packs, and video needs an exact ComfyUI environment. They must not go into the person's ComfyUI.

**Goal:** a throwaway ComfyUI inside `C:\astrid-test`, on port 8199, with the packs and models below, used with `--placement http://127.0.0.1:8199`. Delete it at the end.

**Constraints:**

- Use the official Windows portable build. Node packs and models go in its inner `ComfyUI` folder; install pack requirements with its own `python_embeded\python.exe`.
- For video, use the **frozen Release 15 Agent's** `astrid/packs/vibecomfy/recipe.windows-cu130.json` and `astrid/packs/runpod/pins.json` as the source of truth for ComfyUI, nodes, torch and related versions. The old Release 13 ComfyUI pin is not an instruction for this build. Record actual versions and arguments; report and skip if the matching environment cannot be prepared without modifying the person's ComfyUI.
- Start it as a background process with its output in a log file; the bundled `.bat` waits for a key press.
- To reuse models already downloaded, point an `extra_model_paths.yaml` at the person's models folder.
- Stop the person's ComfyUI while video runs and start it again afterwards; one GPU won't hold both. Tell the person first.
- **Before the 53 GB video download,** run E once against the test ComfyUI. Continue only when the refusal is about missing models, not about versions.

Do them in this order and stop where disk, memory or time runs out.

| Cell | Node packs (commit) | Models |
|---|---|---|
| D, speech | `1038lab/ComfyUI-QwenTTS` (`d8122a8b`) | 2.5 GB: all of `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` into `models/TTS/Qwen3-TTS/Qwen3-TTS-12Hz-0.6B-CustomVoice/` |
| H, sound effects for a video | `BobRandomNumber/ComfyUI-HunyuanVideo_Foley` (`b94f7aca`) | 10.6 GB under `models/hunyuan_foley/`: the three `.pth` files of `tencent/HunyuanVideo-Foley`; `google/siglip2-base-patch16-512` in `siglip2/`; `laion/larger_clap_general` in `clap/` |
| E, video from an image | `seitanism/ComfyUI-H3-Motion-Context-MultiRef` (`361624fb`), `Kosinkadink/ComfyUI-VideoHelperSuite` (`4ee72c06`) | 53.5 GB from `Comfy-Org/MiniMax-H3`: `diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors`, `text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors`, `vae/minimax_h3_video_vae_int8_convrot.safetensors`, `vae/minimax_h3_audio_vae_fp32.safetensors`, `loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` |
| F and G, video from a video, video edit | as E | as E. Only if E ran |

Video has only been run on a 32 GB card. On a smaller one, try E anyway if the disk allows and record what happens. If Astrid's messages name different files from the ones above, trust Astrid and tell us.

```powershell
$t = "http://127.0.0.1:8199"
# D
& $astrid generate audio --entry audio/qwen3_tts_custom_voice --mode tts --input "text=The weather is calm and clear this morning." --placement $t --out C:\astrid-test\D --json
# H: any short mp4 will do
& $astrid generate audio --entry audio/hunyuan_video_foley --mode sfx --prompt "Soft footsteps on a quiet path, with a light breeze" --video-ref "<a short mp4>" --placement $t --out C:\astrid-test\H --json
# E: 3 seconds, 8 steps
& $astrid generate video --entry h3 --mode i2v --prompt "camera slowly pushes in, warm afternoon light shifts across the wall; quiet street ambience, distant birds" --image-ref "<image from A>" --frames 72 --steps 8 --seed 7 --placement $t --out C:\astrid-test\E --json
# F and G, on the video from E
& $astrid generate video --entry h3 --mode v2v --prompt "The same scene at dusk, with long warm shadows" --video-ref "<video from E>" --steps 8 --seed 42 --placement $t --out C:\astrid-test\F --json
& $astrid generate video --entry h3 --mode video-edit --prompt "Gently brighten the scene, keeping the composition" --video-ref "<video from E>" --steps 8 --placement $t --out C:\astrid-test\G --json
```

## Part 6: Clean up and report

1. **Make the diagnostics bundle first;** it can't be made after uninstall: `& $astrid doctor --bundle C:\astrid-test\report\astrid-doctor.zip`. Copy the images from A and B into the report folder too.
2. **Delete every model this test added to the person's ComfyUI,** from your list. If the person asks to keep some, keep those and say which.
3. **Do not silently leave unpublished Release 15 installed.** Ask whether to keep the development build, restore the previous published version using the supported rollback/update route, or remove a new test install without deleting any pre-existing data. Any restore/uninstall requires explicit consent. Record the selected final version, backup/rollback result, folders under `%LOCALAPPDATA%` that start with `Astrid`, the `Astrid Runtime` scheduled task, and any `astrid` command remaining.
4. **Delete the test ComfyUI** and everything else on your list.

Never delete a whole `models`, `custom_nodes`, `input` or `output` folder, and never delete a file you didn't add.

**Finish `report.md`** with the issue URL; all three frozen Release 15 SHAs, local manifest hash, active-build proof, fresh-install or update-from version, machine facts, cell table, problems in severity order, fixes, and exactly what was added/removed/kept/restored. Label App/UI **NOT TESTED**. If you can export this agent session, add it to the folder: it shows what really happened.

**Then zip the folder and attach it to the Part 0 issue,** pasting the summary as the final issue comment:

```powershell
Compress-Archive -Path C:\astrid-test\report\* -DestinationPath C:\astrid-test\astrid-test-report.zip -Force
```

Check the zip for tokens first. GitHub takes attachments up to 25 MB; if yours is larger, leave out the session export and say so. Keep `C:\astrid-test` until we confirm on the issue that we have what we need. **The run is not complete until the issue contains exact pinned build identities, observed pass/fail/skips, caveats and diagnostic evidence (or a documented reason evidence could not be attached).**
