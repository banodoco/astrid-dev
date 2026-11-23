# Astrid on Windows: Release 15 main technical test run

**Give this entire guide to your coding agent.** This is for testing *unpublished* Release 15, **not** the public installer target. Core generation downloads about 32 GB of models, removed after the test.

| | |
|---|---|
| Your issue | `{{ISSUE_URL}}` |
| Build under test | Frozen full SHAs of Agent and Runtime from `release/15/main`, and VibeComfy source pinned by that Agent; fill `{{AGENT_SHA}}`, `{{RUNTIME_SHA}}`, `{{VIBECOMFY_SHA}}` from Part 0 |
| You need | Dedicated Windows 10/11 test host, NVIDIA GPU, working ComfyUI, Git for Windows, Python 3, at least 40 GB free for core run |

## What this is

Verify the **exact Release 15 development heads**, not merely whichever build `astrid.haus` currently serves. Release 15 is not yet published. The public `install.ps1` **without a candidate manifest** may still install Release 14. This guide freezes `release/15/main` source SHAs and supplies a locally served install manifest. Do not claim Release 15 passed if source identity is unknown or mismatched.

Use a **dedicated test machine or disposable VM**. Custom program/data roots do not guarantee isolation of Windows login services, scheduled tasks or command registration. Do not update someone's everyday Astrid installation. For an upgrade test, create a test-owned installation of the published version first. Failure is valid evidence; never bypass checks, skip a failing test, or quietly substitute a published build.

Done means frozen source identity, machine and installer evidence, core cells A/A2/B/C and refusal checks D/E, then cleanup/report. Part 5 is optional. Do not spend more than 15 minutes debugging a failed cell (downloads excluded). Record when a cell used a local patch; that is not proof the unmodified head passes.

## Ground rules

1. **Download what the test needs without asking each time,** and delete it at the end. Tell the person the total once, before you start, and check there is disk space. Never delete a model that was there before.
2. **Never install node packs or Python packages into the person's ComfyUI.** Adding model files to it is fine.
3. **Spend no money.** Never use a RunPod or other paid option, even if Astrid offers one.
4. **Fix small Astrid problems that block you, and share the fix.** If a small change to Astrid's installed code gets a step working (a wrong path, a quoting bug, a missing Windows case), make it, keep going, and add the exact diff to `fixes.diff` straight away. Keep fixes minimal, and say in the cell table which cells ran on patched code. If Astrid then refuses to run because its own files changed, undo the change and report both. If it needs more than a small change, report it and move on. Don't work around an Astrid problem by changing the person's ComfyUI. A fix here lasts only until the next update, so it must be in the report to count.

**Shell.** Use Windows PowerShell, not WSL. No admin rights are needed. If your shell doesn't keep variables between commands, or isn't PowerShell, put each block in a `.ps1` file and run `powershell -NoProfile -ExecutionPolicy Bypass -File <file>`. The install, the downloads and the video cells run longer than most command time limits: run them in the background and poll.

**Records.** Everything goes in one folder, `C:\astrid-test\report`, which you zip and attach at the end:

- `report.md`: your notes as you go. For anything that fails or surprises you: the command, the exact error and the task ID. Also a plain list of **every file or folder this test adds outside `C:\astrid-test`;** the clean-up works from that list.
- `log.txt`: every command you run and its full output, appended as you go.
- `fixes.diff`: any change you made to Astrid.
- the diagnostics bundle and the images from A and B (part 6).

Ask our agent on the GitHub issue by starting a comment with `QUESTION:`, and carry on without waiting. If you can't post (`gh auth status` fails), the person pastes for you. Keep tokens out of everything in the folder.

## Part 0: Freeze the unpublished Release 15 source tuple

Use **Windows PowerShell**, not WSL. Record the full Git SHAs **before** installing. The branch can move during the run; the evidence applies to the frozen commits, not an unfrozen moving name.

```powershell
$ref = 'refs/heads/release/15/main'
$agentSha = ((git ls-remote https://github.com/banodoco/astrid-agent.git $ref) -split '\s+')[0]
$runtimeSha = ((git ls-remote https://github.com/banodoco/astrid-runtime.git $ref) -split '\s+')[0]
if ($agentSha -notmatch '^[0-9a-f]{40}$' -or $runtimeSha -notmatch '^[0-9a-f]{40}$') { throw 'Could not freeze Release 15 source SHAs' }
New-Item -Type Directory -Force C:\astrid-test\manifest, C:\astrid-test\report | Out-Null
Invoke-WebRequest https://astrid.haus/install-manifest.json -OutFile C:\astrid-test\manifest\published.json
$m = Get-Content C:\astrid-test\manifest\published.json -Raw | ConvertFrom-Json
if (!$m.agent -or !$m.runtime -or !$m.tools) { throw 'Unexpected manifest schema: stop' }
$m.agent.sha = $agentSha
$m.runtime.sha = $runtimeSha
$pinFile = Invoke-RestMethod "https://raw.githubusercontent.com/banodoco/astrid-agent/$agentSha/astrid/packs/vibecomfy/pins.json"
$vibeSha = $pinFile.sources.vibecomfy.revision
if ($vibeSha -notmatch '^[0-9a-f]{40}$') { throw 'Missing candidate VibeComfy revision' }
if ($null -ne $m.vibecomfy) { $m.vibecomfy.sha = $vibeSha }
$json = $m | ConvertTo-Json -Depth 64
[IO.File]::WriteAllText('C:\astrid-test\manifest\local-install-manifest.json', $json, (New-Object Text.UTF8Encoding($false)))
"Agent=$agentSha Runtime=$runtimeSha VibeComfy=$vibeSha" | Tee-Object C:\astrid-test\report\source-pins.txt
```

This preserves the **complete** tool/assets manifest from the served release and changes the candidate source pins, following the [Agent's source-install qualification recipe](https://github.com/banodoco/astrid-agent/blob/release/15/main/docs/setup/local-source-install.md#developer-qualification-with-local-git-sources). Check the resolved manifest's source repositories and VibeComfy identity against the pinned Agent recipe. If any source is unavailable or incompatible, stop; never remove manifest integrity checks.

In a **separate PowerShell window**, serve the manifest and keep this process running until the installer completes:

```powershell
py -3 -m http.server 17605 --bind 127.0.0.1 --directory C:\astrid-test\manifest
```

Do not alter the manifest while the test runs. Save the JSON in the final report. If the remote branch moves later, report the old frozen SHAs alongside the newer heads.

## Part 1: The machine

Record: Windows and PowerShell versions; GPU, VRAM and driver (`nvidia-smi`); RAM; free disk; how ComfyUI is installed (portable, desktop app, Stability Matrix, Pinokio, git), its version and its address; whether Astrid was already installed; which agent you are.

## Part 2: Install or update the frozen Release 15 build

**Never update the owner's normal Astrid home.** Choose **fresh install** or **published-to-Release-15 update**, both using only dedicated test roots. An update is best tested by first installing the published release into those roots with the manifest override **unset**, creating a test project, and recording its identity and doctor result.

```powershell
$root = 'C:\astrid-test\program'
$data = 'C:\astrid-test\data'
# Run this first ONLY for the upgrade scenario, on a dedicated test host:
Remove-Item Env:ASTRID_INSTALL_MANIFEST_URL -ErrorAction SilentlyContinue
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --root $root --data-root $data --yes --autostart on --command off --skills off --skill-copies off
```

Now install Release 15 from the local candidate manifest (server from Part 0 running). **For a test-owned existing installation**, use:

```powershell
$env:ASTRID_INSTALL_MANIFEST_URL = 'http://127.0.0.1:17605/local-install-manifest.json'
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --root $root --data-root $data --update
```

**For a fresh Release 15 installation only**, use the following instead of `--update`:

```powershell
$env:ASTRID_INSTALL_MANIFEST_URL = 'http://127.0.0.1:17605/local-install-manifest.json'
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --root $root --data-root $data --yes --autostart on --command off --skills off --skill-copies off
```

**Confirm installed identity.** Do not mistake an old retained version for the selected version. Compare the selected installed manifest's Agent and Runtime SHAs against `$agentSha`/`$runtimeSha`, and VibeComfy against `$vibeSha` if present; retain the manifest and the doctor's output. If any identity cannot be confirmed, **stop and report**, not a passing test.

```powershell
$astrid = Join-Path $root 'run-astrid.cmd'
Get-ChildItem (Join-Path $root 'versions\*\manifest.json') | ForEach-Object {
  $entry = Get-Content $_.FullName -Raw | ConvertFrom-Json
  [pscustomobject]@{ Path = $_.FullName; Agent = $entry.agent.sha; Runtime = $entry.runtime.sha; VibeComfy = $entry.vibecomfy.sha }
} | Format-List
& $astrid doctor --json
Remove-Item Env:ASTRID_INSTALL_MANIFEST_URL -ErrorAction SilentlyContinue
```

Record the result (`fresh` / `updated` / `refused` / `failed`), installed source and logs, and whether the old test project survived an update. Stop on mismatch or install failure, preserving complete output. Keep every existing user project untouched. Do not run the default installer to 'fix' a candidate result.

## Part 3: Connect ComfyUI

With the person's ComfyUI running, use its actual loopback port. Do not modify its Python or node packs:

```powershell
$url = 'http://127.0.0.1:8188' # change to actual detected port
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

**Release 15:** No Release 13 latency or behavior is pre-accepted. Record both A/A2 timings, all missing-model/refusal diagnostics, and any changed CLI flags discovered through `--help`. If the source expects different model files, record the pinned source's actual requirements rather than silently treating this older list as normative.

**Two free checks.** Run cells D and E from part 5 against `$url`, using the image from A for E. They should refuse, because the person's ComfyUI lacks their nodes. Record the exact messages: we want to know whether they say clearly what is missing.

**For each cell record:** `cell | ran / refused / failed / skipped | wall time | task ID | note`. For "ran", look at the image yourself; for audio and video give the file size and duration, or ask the person to play it. For "failed", add `& $astrid tasks show <task id> --json`. If a job shows no sign of progress for 10 minutes (20 for video), cancel it with `& $astrid tasks cancel <task id>` and record that.

## Part 5 (optional): speech, sound effects and video

These need custom node packs, and video needs an exact ComfyUI environment. They must not go into the person's ComfyUI.

**Goal:** a throwaway ComfyUI inside `C:\astrid-test`, on port 8199, with the packs and models below, used with `--placement http://127.0.0.1:8199`. Delete it at the end.

**Constraints:**

- Use the official Windows portable build. Node packs and models go in its inner `ComfyUI` folder; install pack requirements with its own `python_embeded\python.exe`.
- Video must match the **frozen Agent's** actual `astrid/packs/vibecomfy/pins.json`, `environment.windows-nvidia.json` and `recipe.windows-cu130.json`. Do not reuse the Release 13 ComfyUI version assumption; the Release 15 Windows recipe includes Python 3.12.10 and PyTorch 2.10.0+cu130. A readiness/version refusal is a test result, not something to bypass.
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

The optional model sizes and example node revisions above originated in the Release 13 guide; check them against the frozen Release 15 pins **before** large downloads. If the environment differs or VRAM is insufficient, report `skipped` or `refused` and the exact cause.

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
3. **Do not leave an unpublished candidate as somebody's everyday installation.** Restore or remove only the dedicated test-owned program/data after consent. Inventory service/scheduled-task/command registration and do not delete unrelated installations or projects.
4. **Stop the manifest HTTP server**, clear `ASTRID_INSTALL_MANIFEST_URL`, and delete the test ComfyUI and verified test-added files. Keep the report and manifest until acknowledged on the issue.

Never delete a whole `models`, `custom_nodes`, `input` or `output` folder, and never delete a file you didn't add.

**Finish `report.md`** with a summary at the top: the frozen Agent/Runtime/VibeComfy SHAs, installed selected manifest, current branch heads at report time, fresh-versus-update path, machine facts and cell table; the problems, worst first; the fixes you made; what was downloaded and what the clean-up removed or kept. If you can export this agent session, add it to the folder: it shows what really happened.

**Then zip the folder and attach it to the issue,** with the summary pasted as the comment:

```powershell
Compress-Archive -Path C:\astrid-test\report\* -DestinationPath C:\astrid-test\astrid-test-report.zip -Force
```

Check the zip for tokens first. GitHub takes attachments up to 25 MB; if yours is larger, leave out the session export and say so. Keep `C:\astrid-test` until we confirm on the issue that we have what we need.


**Scope limit:** This guide tests the CLI and a tester's own ComfyUI. It does not establish a Release 15 `astrid-app` browser build, a published Release 15 installer, or release readiness. No test run has been performed by merely updating this guide.
