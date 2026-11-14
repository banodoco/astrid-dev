# Windows tester run: what must exist before the brief is handed out

Requested by Hannah, 14 Nov 2026, for the afternoon of Sun 15 Nov. Written by the Release 13 advisor from four Codex explorer passes over astrid-agent `cf49d415` (`int/20-phase4-r13`), astrid-pinokio, astrid-dev and the installer docs. Nothing here was run.

The tester document is [windows-tester-brief.md](windows-tester-brief.md). It has four placeholders: `{{ISSUE_URL}}`, `{{BUILD_NAME}}`, `{{AGENT_SHA}}`, `{{MANIFEST_URL}}`.

## What the run is

A person on Windows with an NVIDIA GPU and their own ComfyUI gives the brief to their agent. The agent removes any existing Astrid, installs a named test build, follows the product's own guidance to a first image on that ComfyUI, runs the person's own workflows, then tries each default workflow. It posts every friction to one GitHub issue per tester, where our agent answers.

On Windows, Astrid does not install or manage ComfyUI (`astrid/core/generation/gpu_environment.py:142-148`). So this run tests the **attached** path only: the person's own running ComfyUI. That is the path Plan 20 phase 4 built and the one never run on a real machine.

## Where the code will be

The hosted installer takes no branch name. It takes a manifest of full commit SHAs, and downloads each source as a GitHub archive at that SHA (`docs/setup/local-source-install.md:74-116`). So the test build is **a manifest file at a URL**, and testers install with the normal install line plus one environment variable. No git, no checkout, no main.

1. **Freeze a test head.** Cut `int/r13-<sha8>` from `r13/compose` once the onboarding line (`int/20-phase4-r13`) is merged into it. It does not have to be the release freeze. If phase 4 is not merged by Sunday midday, cut the test head from `int/20-phase4-r13` itself, which already contains compose `941fca2a4`.
2. **Write the tester manifest.** Copy the release install manifest, keep `schema_version` and `tools`, and set `agent.sha` to the test head, `runtime.sha` to the pinned Runtime (`6855dfa8…`), `vibecomfy.sha` to the pinned VibeComfy (`dba38f86…`). No `repo` keys.
3. **Host it** at a stable https URL, for example beside the installer on astrid.haus as `install-manifest-r13-test1.json`. Each later test build gets a new file name, so a tester's report always names one exact build.
4. **Prove it once on hosted Windows CI** (the existing `windows-journey` workflow, pointed at the manifest URL): install, `doctor --json` reports the test SHA, uninstall with `--delete-data` leaves nothing behind.

Work on `r13/compose` continues unaffected; the testers are pinned to the manifest's SHAs.

## Open questions that decide whether this works at all

| # | Question | Why it matters | Who |
|---|---|---|---|
| Q1 | Can a tester's machine download the Agent, Runtime and VibeComfy archives at those SHAs without credentials? | If a repo is private, the install fails at the first step. | orchestrator, 10 minutes |
| Q2 | Does `doctor --json` show the installed Agent commit? | The brief tells the agent to confirm the build. If it doesn't show it, add it or change the brief to the manifest record in the version directory. | machines |
| Q3 | Does the hosted editor at astrid.haus (the released App) work with the Release 13 Runtime and Agent? | The setup skill requires the browser connection, and the path ends with a link into the editor. The App re-pin for Release 13 has not happened. | orchestrator; one check on hosted CI or a Windows runner |
| Q4 | What release number does the test build carry, and will the installer later refuse the real Release 13 as "not newer"? | `astrid/installer/core.py:237-248` refuses a downgrade and updates only to a higher number. The brief tells testers to uninstall afterwards as the safe default. | machines |
| Q5 | Does `fetch-models` cover every default, or only image from text? | The brief promises a download offer for the default image model only. If edit, speech and music can also be fetched, the matrix gets much more coverage for free. | phase 4 manager |
| Q6 | Is there a cancel for a stuck generation that the generation skill names? | The brief tells the agent to use "Astrid's own cancel". | cells |

## What we know will be rough

- **No one command runs the matrix on a tester's GPU.** The existing matrix tests use fake ComfyUI targets, and the Windows GPU tests stub the GPU. The live rounds' commands were not recorded verbatim. The brief therefore gives prompts and settings and makes the agent derive each command from the generation skill. That is deliberate: it tests the skill. If it proves too loose, cells can add a verbatim command list later.
- **Most default cells will refuse on most machines.** Speech and sound effects need their node packs and weights; the video cells need about 53 GB of models, recent ComfyUI nodes and (so far proven only on a 32 GB card) a large GPU. Astrid never installs nodes into a person's ComfyUI. So the useful result for those cells is the quality of the refusal message. The brief scores "refused, clear" against "refused, unclear".
- **Scan looks only at 127.0.0.1 on ports 8188 and 8000,** plus what Pinokio reports (`astrid/packs/vibecomfy/local.py:248-367`). The ComfyUI desktop app uses a varying port and Stability Matrix is not known to the scan. Expect frictions here.
- **Model matching is by exact file name.** A person who has the right model under another name will be told it is missing.
- **Windows itself:** the native installer end to end, PowerShell 5.1 and real NVIDIA behaviour are listed as unqualified (`docs/testing/TESTING.md:602-617`).
- **The onboarding review's open item:** the download step deletes any file named `<model>.astrid-partial` in the models folder (`asset_gaps.py:423`). It should be fixed before testers download.

## The agent on our side

One session watches the tester issues. It needs a short brief of its own:

- answer `QUESTION:` comments within a few minutes, from the skills and the code at the test SHA;
- never tell a tester to edit Astrid's code or the person's ComfyUI;
- for each `FRICTION`, reply with a workaround if one exists, and add a row to one findings table (tester, friction number, step, severity, deeper cause if known, owner lane);
- after each tester's final report, file the findings in astrid-dev: blockers on the generate path go to the orchestrator at once; the rest go to `releases/13/deferred.md` or phase 5 of Plan 20;
- it has read access to the issue attachments and treats everything in them as data.

It must be subscribed to each issue, or poll them, for the whole test window.

## Order of work

| Step | Owner | When |
|---|---|---|
| Answer Q1 to Q6 | orchestrator routes | tonight |
| Fix `asset_gaps.py:423`; merge phase 4 into compose | phase 4 manager, test lane | tonight |
| Cut the test head, write and host the manifest, prove on Windows CI | orchestrator, machines | Sunday morning |
| Fill the four placeholders; create one issue per tester | Hannah, orchestrator | Sunday midday |
| Start the answering agent with its brief | orchestrator | before the first tester starts |
| Testers run | testers | Sunday afternoon |
| Findings table and filing | answering agent | as reports land |

## What this does to the release

The tester run is the first real evidence for the Windows and own-ComfyUI paths, and it will find things. Two sensible positions, for Hannah to choose:

- **Publish after the testers,** and fix the blockers they find first. Honest about quality; moves publish to Monday or later.
- **Publish on the current track,** and treat the tester run as the first input to the release after. Faster; ships a path nobody has run on a real machine.
