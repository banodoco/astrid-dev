# Astrid on Windows: technical test run

**Give this whole document to your coding agent.** It is written for the agent. You stay nearby to approve downloads.

| | |
|---|---|
| Your GitHub issue | `{{ISSUE_URL}}` |
| Build under test | `{{BUILD_NAME}}`: Agent commit `{{AGENT_SHA}}` |
| Install manifest | `{{MANIFEST_URL}}` |
| You need | Windows 10 or 11, an NVIDIA GPU, a working ComfyUI, 40 GB free disk |

## What this is

A technical check that a pre-release of Astrid installs and generates on a real Windows machine. Nobody has done that yet. You install one exact build, point it at the person's running ComfyUI, and run Astrid's default workflows. Everything is command line; **skip any step that asks you to open a browser or astrid.haus.**

We want to know what works, what fails, and the exact error when it fails. A failure is a useful result.

- **Done** means parts 1 to 4 and the clean-up. Part 5 is optional.
- **If the install fails, or the installed commit is wrong:** post the output and stop. That is the result.
- **If the person is away:** skip anything that needs their yes, and mark it skipped.
- **Don't fight one cell for more than 15 minutes** (downloads don't count). Report it and move on.

## Ground rules

1. **Ask the person before any download over 1 GB.** Say the size and where it goes.
2. **Never install node packs or Python packages into the person's ComfyUI.** Adding model files is fine, with their yes.
3. **Spend no money.** Never use a RunPod or other paid option, even if Astrid offers one.
4. **Don't patch Astrid** to get past a problem. Report it instead.

**Shell.** Use Windows PowerShell, not WSL. No admin rights are needed. If your shell doesn't keep variables between commands, or isn't PowerShell, put each block in a `.ps1` file and run `powershell -NoProfile -ExecutionPolicy Bypass -File <file>`. The install, the downloads and the video cells run longer than most command time limits: run them in the background and poll.

**Reporting.** Keep one file, `C:\astrid-test\report.md`, and write to it as you go: for anything that fails or surprises you, the command, the exact error and the task ID. Post it to the GitHub issue if you can (`gh auth status`); otherwise the person pastes it. Ask our agent on the issue by starting a comment with `QUESTION:`, and carry on without waiting. Keep tokens and the Windows user name out of what you post.

Keep a plain list in the report of **every file or folder this test adds outside `C:\astrid-test`.** The clean-up works from that list.

## Part 1: The machine

Record: Windows and PowerShell versions; GPU, VRAM and driver (`nvidia-smi`); RAM; free disk; how ComfyUI is installed (portable, desktop app, Stability Matrix, Pinokio, git), its version and its address; whether Astrid was already installed; which agent you are.

## Part 2: Install the test build

**Remove any existing Astrid first.** This deletes the person's Astrid projects, so ask. Their ComfyUI is not touched. (If Astrid came from Pinokio, use Pinokio's Uninstall instead.)

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall --delete-data
```

**Install:**

```powershell
$env:ASTRID_INSTALL_MANIFEST_URL = '{{MANIFEST_URL}}'
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --yes --autostart on --command on --skills on --skill-copies off
```

**Confirm the build.** Without this we don't know what you tested.

```powershell
Get-ChildItem "$env:LOCALAPPDATA\Astrid\versions\*\manifest.json" | ForEach-Object { (Get-Content $_ -Raw | ConvertFrom-Json).agent.sha }
```

It must print exactly one line, `{{AGENT_SHA}}`. Anything else: stop and post a `QUESTION:`.

Every Astrid command below goes through the launcher, written here as `$astrid`:

```powershell
$astrid = "$env:LOCALAPPDATA\Astrid\run-astrid.cmd"
& $astrid doctor --json
```

Record the install time and the doctor output. If a command in this document is rejected, run it with `--help`, use what the help says, and note the difference: the commands were written from the source code, not from a Windows run.

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

Show the person the plan before the second command. If it is interrupted, run it again; it resumes.

```powershell
# A: image from text
& $astrid generate image --entry qwen-image-2.1-turbo --mode t2i --prompt "A red bicycle leaning against a white wall in soft morning light" --width 768 --height 768 --seed 7 --placement $url --out C:\astrid-test\A --json
# A2: the same with --seed 8 and --out C:\astrid-test\A2, straight after A. It should be clearly faster.
# B: edit the image from A
& $astrid generate image --entry qwen-image-2.1-turbo-edit --mode edit --prompt "Repaint the bicycle frame a deep cobalt blue; keep everything else unchanged" --edit "<image from A>" --placement $url --out C:\astrid-test\B --json
# C: music (uses nodes built into ComfyUI)
& $astrid generate audio --entry audio/ace_step_1_5_t2a_song --mode music --prompt "A calm instrumental piece with soft piano and light strings" --input "lyrics=[instrumental]" --seed 7 --placement $url --out C:\astrid-test\C --json
```

Astrid can't fetch the music models. Run C once and record the message. If the person agrees to 14.7 GB more, fetch these four files from `Comfy-Org/ACE-Step-1.5` into the ComfyUI models folder, in the subfolders shown, and run C again:

`diffusion_models/acestep_v1.5_turbo.safetensors`, `vae/ace_1.5_vae.safetensors`, `text_encoders/qwen_0.6b_ace15.safetensors`, `text_encoders/qwen_4b_ace15.safetensors`

A resumable download that ships with Windows (in the repository these files sit under `split_files/`):

```powershell
curl.exe -L -C - -o "<models folder>\<subfolder>\<file>" "https://huggingface.co/Comfy-Org/ACE-Step-1.5/resolve/main/split_files/<subfolder>/<file>"
```

**Two free checks.** Run cells D and E from part 5 against `$url`, using the image from A for E. They should refuse, because the person's ComfyUI lacks their nodes. Record the exact messages: we want to know whether they say clearly what is missing.

**For each cell record:** `cell | ran / refused / failed / skipped | wall time | task ID | note`. For "ran", look at the image yourself; for audio and video give the file size and duration, or ask the person to play it. For "failed", add `& $astrid tasks show <task id> --json`. If a job shows no sign of progress for 10 minutes (20 for video), cancel it with `& $astrid tasks cancel <task id>` and record that.

## Part 5 (optional): speech, sound effects and video

These need custom node packs, and video needs an exact ComfyUI environment. They must not go into the person's ComfyUI.

**Goal:** a throwaway ComfyUI inside `C:\astrid-test`, on port 8199, with the packs and models below, used with `--placement http://127.0.0.1:8199`. Delete it at the end.

**Constraints:**

- Use the official Windows portable build. Node packs and models go in its inner `ComfyUI` folder; install pack requirements with its own `python_embeded\python.exe`.
- Video refuses a mismatched environment: ComfyUI `0.36.0`, torch `2.10.0+cu130`, `comfy-kitchen` `0.2.35`, `comfy-aimdo` `0.5.5`, started with `--use-ck-attention --disable-comfy-compiler`.
- Start it as a background process with its output in a log file; the bundled `.bat` waits for a key press.
- To reuse models already downloaded, point an `extra_model_paths.yaml` at the person's models folder.
- Stop the person's ComfyUI while video runs (with their yes) and start it again afterwards; one GPU won't hold both.
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

1. **Make the diagnostics bundle first;** it can't be made after uninstall: `& $astrid doctor --bundle C:\astrid-test\astrid-doctor.zip`.
2. **Models added to the person's ComfyUI:** show them your list. Delete what they don't want to keep.
3. **Uninstall Astrid** with the command from part 2, unless the person wants to keep the test build. Note anything left behind: the folders under `%LOCALAPPDATA%` that start with `Astrid`, the `Astrid Runtime` scheduled task, an `astrid` command.
4. **Delete the test ComfyUI** and everything else on your list.

Never delete a whole `models`, `custom_nodes`, `input` or `output` folder, and never delete a file you didn't add.

**The final report** goes on the issue: the commit from part 2; the machine facts; the cell table; the problems, worst first; what was downloaded and what the clean-up removed or kept; the doctor bundle and the images from A and B attached. If you can export this agent session, attach it too, after checking it for tokens: it shows what really happened. Keep `C:\astrid-test` until we confirm on the issue that we have what we need.
