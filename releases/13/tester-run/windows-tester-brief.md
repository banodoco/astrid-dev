# Astrid on Windows: technical test run

**Give this whole document to your coding agent.** It is written for the agent. You stay nearby to approve downloads and answer its questions.

| | |
|---|---|
| Your GitHub issue | `{{ISSUE_URL}}` |
| Build under test | `{{BUILD_NAME}}`: Agent commit `{{AGENT_SHA}}` |
| Install manifest | `{{MANIFEST_URL}}` |
| You need | Windows 10 or 11, an NVIDIA GPU, a working ComfyUI, PowerShell, git |
| Disk | 25 GB for the core run; about 95 GB for everything |
| Time | 1 to 2 hours for the core run; longer with the video cells |

## What this is

A technical check that a pre-release of Astrid installs and generates on a real Windows machine with a real GPU. Nobody has done that yet. You install one exact build, connect it to ComfyUI, and run Astrid's default workflows one by one: two image cells, three audio cells, three video cells.

Everything runs from the command line through your agent. **The browser editor is not part of this test;** skip any step that asks you to open astrid.haus.

We are not judging the design. We want to know **what works, what fails, and the exact error when it fails.** A failure is a useful result. Don't spend more than 15 minutes fighting any one cell: report it and move on.

## Rules

1. **Keep a ledger of everything this test adds to the machine** (part 1), and remove all of it at the end (part 7), except what was already there.
2. **Ask the person before each download over 1 GB.** Say the size and the folder.
3. **Don't change the person's own ComfyUI environment.** Adding model files to it is fine, with their yes. Installing custom node packs or Python packages into it is not: those go into the separate test ComfyUI in part 5.
4. **Spend no money.** Never use a RunPod or other paid option, even if Astrid offers one.
5. **Don't edit Astrid's code or settings files** to get past a problem. Report it. Use a workaround only from Astrid's own help or from our agent on the issue.
6. **No secrets in the issue:** no tokens or keys. Replace the Windows user name in paths with `<user>`.
7. **Native Windows PowerShell only.** Not WSL, not Git Bash. No admin shell is needed.
8. **Don't update Astrid during the run.**

All Astrid commands below use the launcher. Define it once per PowerShell window:

```powershell
$astrid = "$env:LOCALAPPDATA\Astrid\run-astrid.cmd"
```

If a command below is rejected, run the same command with `--help`, use what the help says, and report the difference. The commands were written from the source code, not from a Windows run.

## Reporting

Post to the GitHub issue as you go. Our agent watches it and answers there.

- **A start comment** with the machine facts from part 1.
- **A comment whenever something fails or surprises you:**

  ```
  PROBLEM <number>: <one line>
  Step: <part and cell>
  Command: <exact command>
  Output: <the exact error, trimmed to the relevant lines>
  Task ID: <if there is one>
  Got past it: <how, or "blocked">
  ```

- **`QUESTION:`** at the start of a comment asks our agent. Carry on with whatever doesn't depend on the answer.
- **A final comment** with the report from part 8.

## Part 1: Record the machine and start the ledger

Post in the start comment:

- Windows version; PowerShell version (`$PSVersionTable.PSVersion`).
- GPU, VRAM and driver (`nvidia-smi`); system RAM; free disk space.
- ComfyUI: how it is installed (portable build, desktop app, Stability Matrix, Pinokio, git checkout), its version, its address and port, and the path of its folder.
- Whether Astrid was already installed, and how.
- Which agent you are (name and model).

Create a folder for this test, for example `C:\astrid-test`, and in it:

```powershell
$test = "C:\astrid-test"; New-Item -ItemType Directory -Force $test | Out-Null
$comfy = "<path to the person's ComfyUI folder>"
Get-ChildItem -Recurse -File "$comfy\models" | Select-Object FullName, Length | Export-Csv "$test\models-before.csv" -NoTypeInformation
Get-ChildItem -File "$comfy\input", "$comfy\output" -Recurse | Select-Object FullName | Export-Csv "$test\io-before.csv" -NoTypeInformation
```

Start `ledger.md` in that folder. Add a line each time you download or create something outside `C:\astrid-test`: what, where, how big, and whether it replaced anything.

## Part 2: Remove any existing Astrid, then install the test build

**Remove.** If Astrid is installed, tell the person this deletes their Astrid workspace (projects made in Astrid), and ask. Their ComfyUI is not touched.

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall --delete-data
```

If it was installed through Pinokio, use Pinokio's own Uninstall for it instead. Then check, and report anything left behind:

```powershell
Test-Path "$env:LOCALAPPDATA\Astrid", "$env:LOCALAPPDATA\Astrid Runtime", "$env:LOCALAPPDATA\Astrid Installer"
Get-ScheduledTask -TaskName "Astrid Runtime" -ErrorAction SilentlyContinue
Get-Command astrid -ErrorAction SilentlyContinue
```

Leave `%LOCALAPPDATA%\Astrid GPU` alone if it exists; just tell us.

**Install.** In a new PowerShell window:

```powershell
$env:ASTRID_INSTALL_MANIFEST_URL = '{{MANIFEST_URL}}'
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --yes --autostart on --command on --skills on --skill-copies off
```

Report the time taken and the last 20 lines of output.

**Confirm the build.** This is the check that matters most: without it we don't know what you tested.

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Astrid\versions\*\manifest.json" | ForEach-Object { $_.FullName; (Get-Content $_ -Raw | ConvertFrom-Json) | Select-Object release, @{n='agent';e={$_.agent.sha}}, @{n='runtime';e={$_.runtime.sha}}, @{n='vibecomfy';e={$_.vibecomfy.sha}} }
```

The Agent commit must be `{{AGENT_SHA}}`. If it is anything else, **stop** and post a `QUESTION:`. Then:

```powershell
$astrid = "$env:LOCALAPPDATA\Astrid\run-astrid.cmd"
& $astrid doctor --json
& $astrid status --json
```

Post both outputs, with the user name replaced.

## Part 3: Connect ComfyUI

Make sure the person's ComfyUI is running.

```powershell
& $astrid generate scan --json
```

If it finds nothing, pass the port: `& $astrid generate scan --ports 8188,8000,<port> --json`. Report what it found against what is really there. Then save the address and look at what is ready:

```powershell
& $astrid generate settings set placement http://127.0.0.1:<port>
& $astrid generate defaults --json
& $astrid generate list --json
```

Post the `defaults` output. It shows, for each default, whether this ComfyUI is ready for it and why not.

## Part 4: Core cells on the person's own ComfyUI

These three need only model files, no custom node packs. `$url` is the ComfyUI address.

```powershell
$url = "http://127.0.0.1:<port>"; Set-Location $test
```

**Models for A and B** (about 17 GB, three files, shared by both). Astrid plans the download and writes nothing until you confirm:

```powershell
& $astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url $url --json
```

Show the person the files, sizes and folder. On yes, run it again with `--apply <plan_sha256 from the plan>`. Then run the same pair for `qwen-image-2.1-turbo-edit edit`; it should find nothing left to fetch. Add the files to the ledger.

**Cell A, image from text:**

```powershell
& $astrid generate image --entry qwen-image-2.1-turbo --mode t2i --prompt "A red bicycle leaning against a white wall in soft morning light" --width 768 --height 768 --seed 7 --placement $url --out "$test\A" --json
```

**Cell A2, the same again** with `--seed 8` and `--out "$test\A2"`, straight after A. Report both wall times; the second should be clearly faster.

**Cell B, image edit,** using the image A produced:

```powershell
& $astrid generate image --entry qwen-image-2.1-turbo-edit --mode edit --prompt "Repaint the bicycle frame a deep cobalt blue; keep the wall, light, shadows and everything else unchanged" --edit "<the image from A>" --placement $url --out "$test\B" --json
```

**Cell C, music.** It uses nodes built into ComfyUI. Astrid can't fetch its models, so first run it and report the exact message:

```powershell
& $astrid generate audio --entry audio/ace_step_1_5_t2a_song --mode music --prompt "A calm instrumental piece with soft piano and light strings" --seed 7 --placement $url --out "$test\C" --json
```

If it reports missing models and the person agrees to 6.3 GB more, download these three files from the Hugging Face repository `Comfy-Org/ACE-Step-1.5` into the ComfyUI models folder, keeping the subfolder names, then run it again:

- `diffusion_models/acestep_v1.5_turbo.safetensors`
- `vae/ace_1.5_vae.safetensors`
- `text_encoders/qwen_0.6b_ace15.safetensors`

For every cell, record the row described in part 6.

## Part 5: The remaining cells on a separate test ComfyUI

Speech, sound effects and the video cells need custom node packs with their own Python packages, and the video cells need a specific recent ComfyUI. Installing those into a working ComfyUI can break it and can't be cleanly undone. So these cells run on a **second, throwaway ComfyUI inside `C:\astrid-test`**, which is deleted at the end.

Before anything else in this part, run each cell once against the person's own ComfyUI and post the exact refusal. We want to see what Astrid says when the nodes are missing. Then:

1. **Install a portable ComfyUI** into `C:\astrid-test\ComfyUI` (the official Windows portable build for NVIDIA). The video cells were proven on ComfyUI 0.36.0; use that version if you can, and report the version you used. Check it has the video model's nodes after starting it: `http://127.0.0.1:8199/object_info/MiniMaxH3ReferenceToVideo` must return a definition.
2. **Share the models already downloaded:** add an `extra_model_paths.yaml` pointing at the person's ComfyUI models folder, so nothing is downloaded twice.
3. **Start it on another port,** for example 8199, and leave the person's ComfyUI as it is (stop it if the GPU can't hold both).
4. **Install the node packs** each cell needs into `C:\astrid-test\ComfyUI\custom_nodes`, at the commit given, with the portable build's own Python (`python_embeded\python.exe -m pip install -r requirements.txt`), then restart the test ComfyUI.
5. **Download each cell's models** into `C:\astrid-test\ComfyUI\models`, keeping the subfolders, with the person's yes each time.
6. Point Astrid at it for these cells with `--placement http://127.0.0.1:8199`.

Do the cells in this order, and stop where disk, VRAM or time runs out. Say where you stopped.

| Cell | What | Node packs (commit) | Models |
|---|---|---|---|
| D | Speech | `1038lab/ComfyUI-QwenTTS` (`d8122a8b`) | 2.5 GB: Hugging Face `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice`, the whole repository, into `models/TTS/Qwen3-TTS/Qwen3-TTS-12Hz-0.6B-CustomVoice/` |
| E | Video from an image | `seitanism/ComfyUI-H3-Motion-Context-MultiRef` (`361624fb`), `Kosinkadink/ComfyUI-VideoHelperSuite` (`4ee72c06`) | 53.5 GB: Hugging Face `Comfy-Org/MiniMax-H3`, five files (below) |
| F | Video from a video | as E | as E |
| G | Video edit | as E | as E |
| H | Sound effects for a video | `BobRandomNumber/ComfyUI-HunyuanVideo_Foley` (`b94f7aca`) | 10.6 GB: `tencent/HunyuanVideo-Foley`, `google/siglip2-base-patch16-512`, `laion/larger_clap_general`, under `models/hunyuan_foley/` |

The five video model files, each into the subfolder shown:

- `diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors` (21.0 GB)
- `text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors` (27.1 GB)
- `vae/minimax_h3_video_vae_int8_convrot.safetensors` (2.8 GB)
- `vae/minimax_h3_audio_vae_fp32.safetensors` (0.6 GB)
- `loras/minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors` (2.0 GB)

The video cells have only been run on a 32 GB RTX 5090. On a smaller card they may run slowly or run out of memory. Try cell E anyway if the person has the disk space, and report exactly what happens; that is one of the things we most want to learn. If the model file names Astrid asks for differ from the ones above, trust Astrid's message and tell us.

```powershell
$t = "http://127.0.0.1:8199"
# D, speech
& $astrid generate audio --entry audio/qwen3_tts_custom_voice --mode tts --prompt "The weather is calm and clear this morning." --placement $t --out "$test\D" --json
# E, video from the image A made: 3 seconds, 8 steps
& $astrid generate video --entry h3 --mode i2v --prompt "camera slowly pushes in, warm afternoon light shifts across the wall, breeze stirs the dust; quiet street ambience, distant birds, no speech or music" --image-ref "<the image from A>" --frames 72 --steps 8 --seed 7 --placement $t --out "$test\E" --json
# F, video from the video E made
& $astrid generate video --entry h3 --mode v2v --prompt "The same scene at dusk, with long warm shadows" --video-ref "<the video from E>" --steps 8 --seed 42 --placement $t --out "$test\F" --json
# G, video edit of the video E made
& $astrid generate video --entry h3 --mode video-edit --prompt "Gently brighten the scene, keeping the composition" --video-ref "<the video from E>" --steps 8 --placement $t --out "$test\G" --json
# H, sound effects for the video E made
& $astrid generate audio --entry audio/hunyuan_video_foley --mode sfx --prompt "Soft footsteps on a quiet path, with a light breeze in the background" --video-ref "<the video from E>" --placement $t --out "$test\H" --json
```

If a cell needs an input by another name, `& $astrid generate describe --entry <entry> --mode <mode>` lists the inputs it declares.

## Part 6: What to record for each cell

```
Cell | Result | Wall time | Peak VRAM | Task ID | Notes
```

Result is one of:

- **ran:** an output file exists. Open it. Say whether it matches the prompt, and for video and audio whether it plays;
- **refused:** Astrid declined before generating. Paste the message, and say whether it named exactly what is missing;
- **failed:** an error, a hang or an out-of-memory. Paste the error and attach `& $astrid tasks show <TASK_ID> --project <project> --json` and `& $astrid tasks logs <TASK_ID> --project <project>`;
- **skipped:** say why (disk, VRAM, time, the person declined a download).

Keep every output file in `C:\astrid-test` until the report is posted. Attach the image from A, the image from B, and one video if there is one.

If a generation shows no progress for 10 minutes: `& $astrid tasks cancel <TASK_ID> --project <project>`, report it as a problem, and move on. Don't kill ComfyUI unless cancel fails; if you must, say so.

## Part 7: Clean up

Do this after the final report is drafted, and include the result in it.

1. **Models added to the person's ComfyUI:** list the files now under `$comfy\models` that are not in `models-before.csv`. Show the person the list. Delete them, unless the person wants to keep some; record which were kept.
2. **Inputs and outputs:** the same comparison for `$comfy\input` and `$comfy\output` against `io-before.csv`. Delete only the new files.
3. **The test ComfyUI:** stop it, then delete `C:\astrid-test\ComfyUI`.
4. **Astrid:** ask the person whether to keep the test build. The default is to remove it, because it is not a release:

   ```powershell
   & ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall --delete-data
   ```

   Then repeat the three checks from part 2 and report what is left. Also report whether Astrid's skills are still present in your agent's skills folder.
5. **Everything else in the ledger.** Remove it, or say why it stays.
6. Keep `C:\astrid-test\ledger.md` and the output files until we confirm on the issue that we have what we need. Then delete the folder.

Never delete a whole `models`, `input`, `output` or `custom_nodes` folder, and never delete a file that is in the before lists.

## Part 8: Final report

One closing comment with:

1. **The build:** the manifest line from part 2.
2. **The cell table** from part 6.
3. **Install and uninstall:** time taken, and anything left behind each time.
4. **Problems,** worst first, by number.
5. **Downloads:** total size fetched, and what the clean-up removed and kept.
6. **The diagnostics bundle.** Run `& $astrid doctor --bundle "$test\astrid-doctor.zip"` before uninstalling. User names and secrets are already removed from it. Look through it once, then attach it.
7. **Your conversation.** Export this whole agent session (your messages, the commands and their output) and attach it as a file. Check it for tokens first. This is the most useful thing you can send: it shows what really happened.
