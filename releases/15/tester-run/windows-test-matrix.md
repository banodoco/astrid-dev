# Release 15 Windows and Linux technical matrix (coding-agent reference)

**Start with the [short tester guide](windows-tester-brief.md).** This appendix preserves the detailed test cells, with Windows command examples and a Linux adapter; it is **not** a second onboarding or issue-reporting process. Create one session issue before testing, collect qualitative feedback throughout, and file separate actionable problem issues as the guide says. Use the frozen Agent's skills for normal setup/generation; this file governs Release 15 source identity and explicit test cells. The currently served web editor is outside this Agent/Runtime qualification.

**Start with [self-service build preparation](prepare-build.md).** A verified release-branch snapshot is sufficient for opt-in exploratory testing; formal qualification still requires the Lead's exact approved tuple. Never substitute the published build. The setup skill owns detection, consent, connection and first use; its normal published installer and preinstall helper do not apply to this test. Read skills at the frozen Agent SHA.

## Ground rules

1. **Get one explicit approval** before installing an unpublished build, updating an existing installation or downloading large model files. State the disk/download budget, check free space and clean up only test-added files. Never delete any pre-existing models.
2. **Never install node packs or Python packages into the person's ComfyUI.** Adding model files to it is fine.
3. **RunPod is permitted, but optional and paid.** The agent may claim a RunPod machine after the person approves a dollar ceiling, hourly rate and UTC deadline (Part 5A). Do not buy other cloud services, launch an uncapped pod, or claim RunPod work as proof of local generation. Record actual costs. A spending estimate is **not** a provider-side cap: independently monitor the account and verify termination.
4. **Preserve the original baseline.** Do not edit an installed Astrid build or the person's ComfyUI to make a test pass. If you find a fix, reproduce and implement it on a separate branch from the frozen Release 15 SHA, capture its regression proof, and open an issue-linked PR or supply a patch for the Release Lead. Keep candidate results and patched-source results clearly separate.

**Shell.** Windows: use native PowerShell, not WSL. Linux: use the native shell and the [Linux adapter](prepare-build.md#linux-test-adapter) for launcher, scratch paths, downloads, logs and cleanup; the same cell IDs, arguments and evidence requirements apply. The PowerShell examples below are Windows examples. No admin rights are needed. If your shell doesn't keep variables between commands, or isn't PowerShell, put each block in a `.ps1` file and run `powershell -NoProfile -ExecutionPolicy Bypass -File <file>`. The install, the downloads and the video cells run longer than most command time limits: run them in the background and poll.

**Records.** Everything goes in one folder, `C:\astrid-test\report`, which you zip and attach at the end:

- `report.md`: the GitHub issue URL, frozen Agent/Runtime/VibeComfy SHAs and manifest hash, plus notes as you go. For anything that fails or surprises you: the command, the exact error and the task ID. Also a plain list of **every file or folder this test adds outside `C:\astrid-test`;** the clean-up works from that list.
- `log.txt`: every command you run and its full output, appended as you go.
- `fixes.diff`: an optional patch from a separate checkout based on the frozen Release 15 source; never edits made to the installed tester build.
- the diagnostics bundle and any images actually produced by A and B (part 6).

Keep tokens out of everything in the report folder. Do not keep raw credentials in the logs.

## Part 1: The machine

Record: OS/distribution and shell versions; GPU, VRAM and driver (`nvidia-smi`); RAM; free disk; how ComfyUI is installed (portable, desktop app, Stability Matrix, Pinokio, git), its version and its address; whether Astrid was already installed; which agent you are.

## Part 2: Install or update to frozen Release 15 main

**Use the exact Release 15 snapshot prepared in [the preparation guide](prepare-build.md).** Check whether it is still unpublished and record that status; never use the public manifest to select a tentative build. The old manual local-source route below remains maintainer-authorized Windows developer qualification only. No shortened SHA or branch name is a valid source pin.

**Before changing an existing install:** use the [setup skill](https://github.com/banodoco/astrid-agent/blob/release/15/main/astrid/packs/setup/docs/SKILL.md#0-work-out-the-entry-route) at the frozen Agent SHA to detect the existing launcher and its ownership, record doctor output and active version, request explicit consent for an **unpublished in-place update**, and back up existing projects using Astrid's supported method. An installer with a custom program root may still register the platform login service (Windows scheduled task or Linux systemd user service); **do not assume it is isolated** from an existing installation. If permission is refused, or this is a Pinokio-managed installation without a separately approved migration or isolation plan, record SKIPPED or BLOCKED on the session issue and stop. Never overwrite Pinokio-managed files. Never delete projects or uninstall to make the test pass.

### Route A — Self-service release-branch snapshot (normal)

Follow [prepare-build.md](prepare-build.md) for resolution, validation and consented installation on Windows or Linux. An approved frozen bundle may also be used if it matches the selected exact tuple. Keep the generated or downloaded manifest and bootstrap hashes, active identity, backup and installer output. If no coherent snapshot is available, record the specific blocker. Skip 2A–2C and continue at **Verify the active installed tuple**; Linux uses the adapter's commands.

### Route B — Lead-authorized local-source qualification only

The following 2A–2C procedure is retained for explicit developer investigations, not the default tester experience. The Lead must authorize the exact tuple and record why the frozen tester bundle was unsuitable. The sample copies the published manifest as a **template**, so independently verify its `release` field and full candidate identity against what the installer actually accepts; a manifest still declaring the published release cannot be represented as a verified Release 15 tester build. Stop and report any mismatch instead of altering verification or claiming a passing official tester build.

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
if ($m.release -ne 15) { $m.release = 15 }  # Only on the Lead-authorized unpublished test manifest
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

Verify `release` is **15**, all three full source pins and absolute local paths. Record the local manifest SHA-256 and the original published source pins. If validation fails, report and stop; never disable installer verification or change locked tool versions to make it proceed.

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

### Verify the active installed tuple (both routes)

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

Follow the **exact frozen Agent SHA** of the [astrid-setup skill](https://github.com/banodoco/astrid-agent/blob/release/15/main/astrid/packs/setup/docs/SKILL.md#4-set-up-generation) and [generation skill](https://github.com/banodoco/astrid-agent/blob/release/15/main/astrid/packs/generation/docs/SKILL.md#set-up-my-generation) for read-only discovery, consent to connect the person's existing running ComfyUI, and setting placement. These branch links help locate files; read the instructions at the approved Agent commit. Setup's browser Connected/gallery steps concern the currently published App and do **not** qualify the unpublished Release 15 App. Do not launch, restart or add custom nodes to their ComfyUI. On Windows use the installed `run-astrid.cmd` launcher, not WSL.

Record the `generate scan --json`, `generate targets --json` and `generate defaults --json` results, the actual selected local ComfyUI URL/port and whether each relevant model is ready. If the connection is missing or unusable, record the exact refusal. A paid or remote fallback is not evidence that local discovery passed.

## Part 4: The core cells

**Minimum baseline: A then A2**, after the verified install and ComfyUI connection, where hardware and models allow. **B (image edit) and C (music) are recommended extensions, not prerequisites for a useful feedback session.** Record explicit SKIPPED/BLOCKED with reasons; never pretend a remote result fills a local cell.

`$url` is the ComfyUI address. Work in `C:\astrid-test`.

**Models for A and B** (about 17 GB, shared). The setup skill selects first-use defaults from installed `generate defaults`; these explicit-entry tests are **additional comparable test cells**, not a reason to change the person's saved defaults. Check installed Release 15 `--help`/entries first. Astrid plans the download and writes nothing until you confirm:

```powershell
& $astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url $url --json
& $astrid generate fetch-models qwen-image-2.1-turbo t2i --comfy-url $url --apply <plan_sha256> --json
```

Record the plan (files, sizes, folder) in your list of added files. If the download is interrupted, run it again; it resumes.

```powershell
# A: image from text
& $astrid generate image --entry qwen-image-2.1-turbo --mode t2i --prompt "A red bicycle leaning against a white wall in soft morning light" --width 768 --height 768 --seed 7 --placement $url --out C:\astrid-test\A --json
# A2: same entry with a second seed, immediately after A; compare both timings
& $astrid generate image --entry qwen-image-2.1-turbo --mode t2i --prompt "A red bicycle leaning against a white wall in soft morning light" --width 768 --height 768 --seed 8 --placement $url --out C:\astrid-test\A2 --json
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

**Do not inherit Release 13 exemptions.** Record A/A2 cold and warm wall times, overhead, download coverage and image-to-video first-frame behavior. Report real problems even if they were known in Release 13. Check entry IDs and CLI flags against the **installed** Release 15 --help/defaults; if an example was removed, report its replacement rather than silently using another model or paid backend. Approved RunPod cells belong in a **separate remote-results column**; they do not replace the local evidence.

**Optional no-download preflight checks.** If exploring D or E from Part 5, run their no-download preflight against `$url` first (use A for E). Record whether they run or refuse and whether the actual messages name missing nodes/models correctly. Otherwise record SKIPPED. Do not assume Release 15 must refuse just because Release 13 did.

**For each cell record:** `cell | ran / refused / failed / skipped | wall time | task ID | note`. For "ran", look at the image yourself; for audio and video give the file size and duration, or ask the person to play it. For "failed", add `& $astrid tasks show <task id> --json`. If a job shows no sign of progress for 10 minutes (20 for video), cancel it with `& $astrid tasks cancel <task id>` and record that.

## Part 5 (optional): speech, sound effects and video

These need custom node packs, and video needs an exact ComfyUI environment. They must not go into the person's ComfyUI.

**Goal:** a throwaway ComfyUI inside `C:\astrid-test`, on port 8199, with the packs and models below, used with `--placement http://127.0.0.1:8199`. Delete it at the end.

**Constraints:**

- Linux: use a separate disposable Python environment only if the pinned Agent's platform-compatible recipe and all dependencies can be verified; otherwise skip those optional cells with the reason. Do not treat the RunPod Linux recipe as proof of native Linux compatibility. Windows: use the official Windows portable build. Node packs and models go in its inner `ComfyUI` folder; install pack requirements with its own `python_embeded\python.exe`.
- For video, use the **frozen Release 15 Agent's** `astrid/packs/vibecomfy/recipe.windows-cu130.json` and `astrid/packs/runpod/pins.json` as the source of truth for ComfyUI, nodes, torch and related versions. The old Release 13 ComfyUI pin is not an instruction for this build. Record actual versions and arguments; report and skip if the matching environment cannot be prepared without modifying the person's ComfyUI.
- Start it as a background process with its output in a log file; the bundled `.bat` waits for a key press.
- To reuse models already downloaded, point an `extra_model_paths.yaml` at the person's models folder.
- **Do not stop or restart the person's own ComfyUI as part of automated setup.** The optional test ComfyUI is a separate disposable instance. If one GPU cannot run both, ask the tester to stop and later restart their instance themselves, or obtain separate explicit permission for the agent to do this; otherwise skip optional video and record why.
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

## Part 5A (optional): RunPod GPU generation

**RunPod is allowed, but not required.** A tester may use a paid RunPod GPU for supported Astrid generation, especially H3 video, after recording the person's explicit consent, maximum total spend, hourly ceiling and hard UTC deadline **on their Part 0 issue**. A RunPod success does not replace Part 2's native OS update/install check, Part 3's own-ComfyUI discovery, or Part 4's local cells. Record each cell's actual placement separately: own ComfyUI, disposable local ComfyUI or RunPod. Do not label inference on a RunPod Linux host as successful local generation on either tester OS.

**Use Astrid's supported retained-machine path** in the exact frozen Release 15 Agent commit's [RunPod machine skill](https://github.com/banodoco/astrid-agent/blob/release/15/main/astrid/packs/runpod/docs/SKILL.md#runpod-generation-machines). The branch URL is for discovery, not the evidence-pinned instructions. For supported H3 video generation, the placement is --entry h3 --placement runpod. Other model entries must be checked against the installed Release 15 CLI and [execution matrix](https://github.com/banodoco/astrid-agent/blob/release/15/main/docs/reference/where-things-run.md); not every image, speech or ComfyUI workflow supports RunPod. Do not use low-level provisioning scripts for ordinary generation, invent an unsupported command or substitute a different paid provider.

**Before any claim:** the person must approve a maximum USD amount, maximum USD/hour rate, near-term UTC deadline, GPU/datacenter and the specific cells. The person or agent must actively supervise billing. With no approved ceiling, skip RunPod. Do not read or paste raw RunPod API keys. If another claim or cleanup is unresolved, reconcile it; never start an extra pod around uncertain custody.

~~~powershell
# Commands from the installed Release 15 $astrid launcher:
& $astrid credential set runpod     # prompts securely for the key
& $astrid machines setup            # choose GPU, datacenter/volume, budget
& $astrid machines setup --show
& $astrid generate describe --placement runpod --json
~~~

Use --help to confirm the installed flags. **Illustrative only**: the person must substitute their approved GPU, dollar ceiling, rate and future UTC deadline; the values shown here are examples, *not* authorization.

~~~powershell
& $astrid machines claim --gpu "RTX 4090" --max-hourly-usd 1 --max-usd 3 --deadline FUTURE_UTC_DEADLINE --for 30m --consent paid
& $astrid machines --json
# Run a supported H3 generation cell, adapting Part 5's inputs,
# with --entry h3 --placement runpod instead of the local ComfyUI URL.
~~~

Claiming is billable. Saving preferences alone is not approval to spend. Record actual claim ID, pod ID, GPU, region, hourly rate, task ID, timestamps, progress and accrued cost from machines --json and the provider. Check before and after each cell. Do not leave a pod idle between tests without monitoring. After a failed job, it may **continue billing**; stop unsafe retries, cancel the task if appropriate, and release the pod.

**Cost safety is part of the test.** A locally enforced timer can stop working if the tester's computer sleeps, loses connection or the Astrid host exits, so never promise a provider-side spending cap. Keep the computer awake and independently inspect the RunPod account while charges are possible. End the claim before stopping the host or the approved test window:

~~~powershell
& $astrid machines --json
& $astrid machines release MACHINE_ID   # use the exact claimed ID
& $astrid machines --json
~~~

A release command returning is **not yet proof that billing stopped**. Confirm that the *same* pod is terminated in the provider account and record the release/termination receipt. Look for any remaining paid network volumes/storage. If termination is uncertain, immediately alert the person, do not create another pod, and preserve custody records while reconciling the original claim.

Add a separate RunPod table to report.md: frozen build pins, cell, GPU/region/pod ID, claim/lease ID, task ID, start/end UTC, approved caps, estimated vs observed billed cost, result, exact termination evidence, and any uncertainty. Share redacted evidence on the same issue. Never count this as proof of the tester's local GPU or ComfyUI.

## Part 6: Clean up and report

1. **Make the diagnostics bundle first;** On Linux, use the [adapter](prepare-build.md#linux-test-adapter) for paths, service inspection and ZIP creation. it can't be made after uninstall: `& $astrid doctor --bundle C:\astrid-test\report\astrid-doctor.zip`. Copy the images from A and B into the report folder too, if those cells produced them.
2. **Delete every model this test added to the person's ComfyUI,** from your list. If the person asks to keep some, keep those and say which.
3. **Do not silently leave unpublished Release 15 installed.** Ask whether to keep the development build, restore the previous published version using the supported rollback/update route, or remove a new test install without deleting any pre-existing data. Any restore/uninstall requires explicit consent. Record the selected final version, backup/rollback result, folders under `%LOCALAPPDATA%` that start with `Astrid`, the `Astrid Runtime` scheduled task, and any `astrid` command remaining.
4. **Delete the test ComfyUI** and everything else on your list. If RunPod was used, release the exact pod and verify its termination independently in RunPod before closing the test; list any billed volumes or unresolved charges.

Never delete a whole `models`, `custom_nodes`, `input` or `output` folder, and never delete a file you didn't add.

**Finish `report.md` and the testing-session issue** with the issue URL; all three frozen Release 15 SHAs, installed/manifest identity and hash, active-build proof, fresh-install or update-from version, machine facts, cell table, problems in severity order, fixes, and exactly what was added/removed/kept/restored. **Add the user's experience:** positive moments, confusing or slow moments, expectations vs reality, workarounds, the tester's feedback after setup/first creation/end, plus links to every distinct problem issue and PR (or an existing issue it reproduced). Distinguish quotes from the agent's interpretation, and local Windows/Linux from RunPod results (approved spend, actual cost and verified teardown). Label served App/UI **NOT TESTED FOR RELEASE 15**. If you can export this agent session, add it to the folder: it shows what really happened.

**Then zip the folder and attach it to the testing-session issue**, after showing the tester the redacted contents and obtaining their approval to post; paste the summary as the final issue comment:

```powershell
Compress-Archive -Path C:\astrid-test\report\* -DestinationPath C:\astrid-test\astrid-test-report.zip -Force
```

Check the zip for tokens first. GitHub takes attachments up to 25 MB; if yours is larger, leave out the session export and say so. Keep `C:\astrid-test` until we confirm on the issue that we have what we need. **The run is not complete until the issue contains exact pinned build identities, observed pass/fail/skips, caveats and diagnostic evidence (or a documented reason evidence could not be attached).**
