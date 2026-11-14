# Astrid on Windows with your own ComfyUI: tester run

**Give this whole document to your coding agent.** It is written for the agent. You stay nearby to answer its questions and approve downloads.

| | |
|---|---|
| Your GitHub issue | `{{ISSUE_URL}}` |
| Build under test | `{{BUILD_NAME}}`, Agent commit `{{AGENT_SHA}}` |
| Install manifest | `{{MANIFEST_URL}}` |
| Time needed | About 1 hour for parts 1 to 4. Parts 5 and 6 are optional and can take longer |

## What this run is for

Astrid has never been run on a real Windows machine with a real person's ComfyUI. You are the first. We want to know two things:

1. Does a fresh install lead you, without outside help, to a first image made on this person's own ComfyUI?
2. Which of Astrid's default workflows run here, and when one can't, does Astrid say clearly why and what to do?

**A problem is a result, not a failure of the test.** We learn most from the places where you had to guess, search, retry or work around something. Record every one.

## Rules

1. **Do not change the person's ComfyUI.** Don't restart it, update it, install node packs into it, or move its models, unless the person says yes to that specific action. Astrid itself should never do these things; if it does or tries to, report it.
2. **Ask before any download over 1 GB**, and say the size and the folder first.
3. **Spend no money.** Don't rent machines, and don't use any RunPod or paid-provider option, even if Astrid offers one.
4. **Don't fix Astrid.** Don't edit its code or settings files to get past a problem. Report the problem, then use a workaround only if the product or our agent on the issue gives you one.
5. **Keep secrets out of the issue.** No tokens, keys or passwords. Replace the Windows user name in paths with `<user>`.
6. **Use native Windows PowerShell,** not WSL and not Git Bash.
7. **Follow the product first.** For setup, do what Astrid's own output and its `astrid-setup` skill tell you. This document deliberately does not list the setup commands. If you can't tell what to do next from the product, that is a finding: report it, then ask on the issue.

## How to report

Post to the GitHub issue as you go, not only at the end. Our agent watches the issue and will answer questions there.

- **One comment at the start** with the machine facts (part 1).
- **One comment for each friction**, at the moment it happens, in this shape:

  ```
  FRICTION <number>: <one line>
  Step: <which part of this document, or which Astrid step>
  What I did: <the exact command or action>
  What happened: <the exact output or error, trimmed to the relevant lines>
  What I expected:
  How I got past it: <workaround, or "blocked">
  Severity: blocker / slowed me down / confusing / cosmetic
  ```

- **A question for our agent:** start the comment with `QUESTION:`. Carry on with any step that doesn't depend on the answer.
- **One comment at the end** with the final report (part 7).

Friction includes: an unclear message, a command that didn't work as documented, a wrong path for Windows, a step where you had to read source code, a long wait with no sign of progress, a result you didn't expect, and anything the person found odd.

## Part 1: Record the machine

Post these in your first comment:

- Windows version, and PowerShell version (`$PSVersionTable.PSVersion`).
- GPU model and VRAM (`nvidia-smi`), and the driver version.
- Free disk space on the drive that holds the ComfyUI models folder.
- How ComfyUI is installed: portable build, the ComfyUI desktop app, Stability Matrix, Pinokio, a git checkout, or something else. Its version, the address and port it listens on, and whether it is running now.
- Roughly how many custom node packs and saved workflows it has.
- Whether Astrid was already installed, and how (the install script, Pinokio, or a source checkout).
- Which agent you are (name and model).

Make sure ComfyUI is running before part 3.

## Part 2: Remove any existing Astrid, then install the test build

**Remove.** If Astrid is installed, tell the person that this deletes their Astrid workspace (projects made in Astrid) and ask. Their ComfyUI, its models and its workflows are not touched. Then run:

```powershell
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --uninstall --delete-data
```

If Astrid was installed through Pinokio, use Pinokio's own Uninstall for it instead. Then check that these are gone, and report anything left behind:

- the folders `%LOCALAPPDATA%\Astrid`, `%LOCALAPPDATA%\Astrid Runtime` and `%LOCALAPPDATA%\Astrid Installer`;
- the scheduled task named `Astrid Runtime` (`Get-ScheduledTask -TaskName "Astrid Runtime"`);
- an `astrid` command on PATH (`Get-Command astrid`).

Leave `%LOCALAPPDATA%\Astrid GPU` alone if it exists, and tell us it was there.

**Install the test build.** In a new PowerShell window:

```powershell
$env:ASTRID_INSTALL_MANIFEST_URL = '{{MANIFEST_URL}}'
& ([scriptblock]::Create((irm https://astrid.haus/install.ps1))) --yes --autostart on --command on --skills on --skill-copies off
```

Record how long it took and the last 20 lines of output.

**Confirm the build.** Run `astrid doctor --json` (if `astrid` is not found, use `& "$env:LOCALAPPDATA\Astrid\run-astrid.cmd" doctor --json`, and report that as a friction). Check that the Agent commit it reports is `{{AGENT_SHA}}`. If you can't find the commit in the output, or it differs, stop and post a `QUESTION:`.

**Do not update Astrid during the run,** even if something offers to.

## Part 3: Set up generation, guided only by the product

The installer's last lines should tell you what to do next. Do that. It should lead you to the `astrid-setup` skill, and the skill should take you through:

1. finding the running ComfyUI;
2. saving it as the place Astrid generates;
3. showing what is ready and what is missing;
4. choosing defaults: Astrid's, or the person's own recent workflows;
5. offering to download missing models for Astrid's default, with a list of files, sizes and the folder, before anything is written;
6. a first image;
7. a link to see the image in the Astrid editor.

For each of the seven, report: did the product lead you there by itself (yes / with guessing / no), the exact commands you ran, and how long it took. Open the final link with the person and report whether the image is there.

Two choices to make with the person:

- **The model download.** If Astrid offers to download its default image model and the person has the disk space and bandwidth (it is about 17 GB), say yes: it tests the download path on Windows. If they prefer not to, decline and let Astrid use one of their own workflows. Report which you did.
- **The Hugging Face token.** If a download asks for one, the person provides it in their own terminal. It must never appear in the issue.

## Part 4: The person's own workflows

This is the part we know least about.

1. Ask Astrid to list the person's saved ComfyUI workflows. Report how many it found against how many they have, and whether the most recent are listed first.
2. With the person, pick two they use often: one simple, one complicated. Run each through Astrid **by name**.
3. Offer to make one of them the person's default for its kind, then generate once using only the default.

For each workflow report: its custom node packs, whether it ran, how the result compares with running it in ComfyUI directly, and the exact message if Astrid refused it.

## Part 5: Astrid's default workflows (the matrix)

Run each cell below through Astrid's generation skill, on the person's own ComfyUI. **Use the skill to work out the command**; post the exact command you ended up with. The cells chain: each uses an earlier output, so no test files are needed.

Many cells will not run on a given machine, because the ComfyUI lacks a node pack or a model, or the GPU is too small. That is expected. **For those, what we need is the exact message Astrid gave, and whether it told you precisely what is missing and what to do.** Don't install node packs to make a cell pass unless the person wants that workflow anyway; if you do, report every step it took.

| # | Cell | Input | Prompt and settings |
|---|---|---|---|
| A | Image from text | none | "A red bicycle leaning against a white wall in soft morning light", 768×768, seed 7 |
| B | Image from text, again | none | The same, seed 8, straight after A. Report both times: the second should be clearly faster |
| C | Image edit | the image from A | "Repaint the bicycle frame a deep cobalt blue; keep the wall, light, shadows and everything else unchanged" |
| D | Speech | none | "The weather is calm and clear this morning." |
| E | Music | none | Defaults, 30 seconds, an instrumental prompt of your choice, seed 7 |
| F | Video from an image | the image from A | "camera slowly pushes in, warm afternoon light shifts across the wall, breeze stirs the dust; quiet street ambience, distant birds, no speech or music", 3 seconds, 8 steps, seed 7 |
| G | Sound effects for a video | the video from F, or any short clip | "Soft footsteps on a quiet path, with a light breeze in the background" |
| H | Video from a video | the video from F, or any short clip | "Keep the composition; shift the scene to dusk with long shadows", 8 steps, seed 42 |
| I | Video edit | the video from F, or any short clip | "Gently brighten the scene, keeping the composition" |

Order: A, B and C first. Then D and E. F to I are the video cells: they need about 53 GB of models, recent ComfyUI nodes and a large GPU, so run them only if the person has the disk space and at least 24 GB of VRAM, or already has the models. Otherwise try F once without downloading anything, to capture the message, and skip the rest.

Record one row per cell:

```
Cell | Result | Wall time | Command | Notes
```

where Result is one of:

- **ran**: an output was produced. Look at it or listen to it, and say whether it matches the prompt;
- **refused, clear**: Astrid named what is missing and what to do, and you could have acted on it;
- **refused, unclear**: it refused, and you couldn't tell what to do from the message alone;
- **failed**: an error, a hang, or an out-of-memory. Include the task ID and the output of `astrid tasks show <TASK_ID> --json`;
- **skipped**: say why.

For timings, Astrid has only been measured on a rented RTX 5090, where a first image took about 13 minutes including preparation and the next about 4 and a half. On your own running ComfyUI we expect much less. Tell us what you see.

If a generation shows no progress for 10 minutes, don't kill ComfyUI. Report it as a friction with the task ID, try Astrid's own cancel, and move on.

## Part 6: Optional extras

Only if there is time and the person is willing:

- Stop ComfyUI, ask Astrid for an image, and report what it says. Start ComfyUI again and retry.
- Restart Windows, then generate an image without doing any setup again.
- Run a generation from the Astrid editor in the browser instead of from the agent.

## Part 7: Final report

Post one closing comment with:

1. **Summary table:** for each of parts 2 to 5, done / partly / blocked, and the time it took.
2. **The matrix table** from part 5.
3. **Top five frictions,** worst first, by number.
4. **Three questions answered in a sentence or two each:**
   - Could a person who had never seen Astrid have got to the first image with only their agent and the product's own guidance?
   - What was the most confusing moment?
   - What one change would have saved the most time?
5. **The person's own words:** anything they found odd, good or annoying.
6. **The doctor bundle.** Run `astrid doctor --bundle`. It saves a file to the Desktop with user names and secrets already removed. Look through it once, then attach it to the issue.
7. **Your conversation.** Export or copy this whole agent session (your messages, the commands and their output) and attach it to the issue as a file. Check it for tokens and keys first. This is the most useful thing you can give us: it shows what actually happened, including the parts nobody thought to report.

**Afterwards.** The test build is not a release. When the person is done with it, either uninstall it with the command in part 2, or leave it and expect to reinstall when the release is published. Ask the person which they want, and say which you did.
