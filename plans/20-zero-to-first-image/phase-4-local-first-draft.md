# Onboarding: the local-first path to a first image

Draft for Plan 20 (Zero-to-first-image onboarding), phase 4. Written by the Release 13 advisor on 14 Nov 2026 at Hannah's request. Not committed; the orchestrator lands it through a scope PR.

**Sources:** my own read of the setup and generation skills on Agent `r13/compose` `176e5ba1`, and nine read-only Codex explorer passes over Agent, App `d6ee9af`, Pinokio `d15c58b`, VibeComfy `r13/cells-vc-10` and Plan 20. Nothing was run live. Code claims carry the explorers' file:line citations and should be re-checked at dispatch.

## Owner direction (Hannah, 14 Nov 2026)

> "In general, it should probably point to RunPod, but it should only have like a one-line mention of RunPod, and the other general should just be focused on people who are running locally and setting it up."

> "Map out the path for actually connecting and launching your local ComfyUI instance. Is it easy to connect to it? Does it have an intuitive way to run to it? Does it use their existing models? Does it generate via that?"

This changes two things in Plan 20's 9 Nov layout: the skill carries on past Connected to a first image, and RunPod and the managed engine shrink to one line each with a link to their own skills.

## The path today

| Step | What happens | Friction |
|---|---|---|
| 1. Entry | README, App brief or Pinokio point at the `astrid-setup` skill (Pinokio's docs do not) | Three entry points; only two name the skill |
| 2. Install | One installer command with four visible choices | Works; this half is in good shape |
| 3. Connected | Installer prints "Astrid installed" and "Open https://astrid.haus"; the App shows Connected and creates "My first project" | Install and the App both stop here. Neither mentions generation |
| 4. Find ComfyUI | `python3 -m astrid.packs.vibecomfy.local scan` probes ports 8188 and 8000, read-only; reports base folder, model folder paths, saved workflow names, Pinokio | Reports folder paths but not which models exist, nor GPU. ComfyUI Desktop is not found (its port varies) |
| 5. Save the connection | Check out a settings JSON, edit `placement`, check it in | No single command. Two stores hold related facts: the target in `~/.vibecomfy/config.toml`, the placement in Runtime settings; `generate targets --save` cannot save a discovered server |
| 6. Project | None exists on the agent path; generation refuses "project is required" | The App creates one; the agent path does not |
| 7. Defaults | One question per slot, from `generate list --json` readiness | Readiness needs exact filenames. Only two shipped image entries (Qwen Image 2.1 Turbo, Z-Image) declare local model files, so a user with SDXL or FLUX.1-dev has nothing ready |
| 8. First image | "Offer one test generation", step 6 of the generation skill | Optional, late and unspecified. With defaults it is refused for missing models, and the refusal suggests a command that installs into Astrid's managed engine, not the user's ComfyUI |
| 9. Own workflow | Fetch the workflow JSON by hand, `generate describe FILE`, write an inputs file, `generate workflow FILE --placement URL --project P` | Works and uses the user's nodes and models. No command fetches a saved workflow by name; the prompt input may be `node:20.text` |

**Answers to the four questions:**
- **Easy to connect?** Yes when ComfyUI is running on 8188: Astrid uses it with nothing configured. Saving that choice is clumsy.
- **Intuitive to run?** Not yet. No command says what is ready or what to run first.
- **Uses their existing models?** Yes. An attached run queues on the user's server and uses what it has. Astrid checks names against the server's own lists and never downloads into it.
- **Generates via that?** Yes, and it never starts, stops or changes the user's ComfyUI. `generate launch` can start a selected ComfyUI with a per-call yes.
- **Proven?** No. Every live run in Release 13 was on RunPod, and Plan 20's own live proof (P3.5) is still open.

The setup skill is 404 lines. About half is the RunPod claim walkthrough, written out for three operating systems, which the RunPod skill already covers. The setup skill calls Astrid by its launcher path; the generation skill uses `python3 -m astrid`. The generation section says "never install anything during setup" while the setup skill directs an engine install.

## The path we want

One promise: **point Astrid at the ComfyUI you already run and get an image from it in a few minutes, without changing anything on it.**

1. **Install and connect.** As today.
2. **See what you have.** One command reports: ComfyUI found and where, project, saved placement, each default slot ready or not with the reason, and the next command.
3. **Use it.** One yes saves the connection. A project is created if there is none, and the user is told.
4. **First image.** From evidence: a shipped entry whose models are present, otherwise one of the user's own saved workflows, run by name. Show the file and where it landed. This is the success moment.
5. **Make it yours.** Defaults per kind, and saved workflows as entries. Optional, after the win.
6. **No local GPU or ComfyUI?** One line each: install Astrid's own engine (link), or rent a GPU through RunPod (link to the RunPod skill).

The skill becomes about 100 lines: each command once, one way of calling Astrid, one fallback (`--doctor`).

## Decisions for Hannah

| # | Decision | Recommendation |
|---|---|---|
| OD1 | The skill continues past Connected to a first image; RunPod and the managed engine are one line each (supersedes the 9 Nov "ends at Connected" layout and D7's split) | Decided by today's direction; confirm |
| OD2 | When no shipped entry is ready, the first image comes from the user's own saved workflow (matches the 9 Nov line "its proof is a real first image from a saved workflow") | Yes |
| OD3 | Plan 20's D8 forbids live GPU tests. The walk-through needs one real run on a machine with ComfyUI and a GPU (no rental) | Allow local runs; rentals stay excluded |
| OD4 | May Astrid download a missing model into the user's own ComfyUI models folder, on a per-file yes? VibeComfy's `fetch` can already do it | Not now. Name the file and the folder; revisit after the walk-through |
| OD5 | Create a default project when none exists, at first generation, and say so (the App already does) | Yes |
| OD6 | Timing | P4.0 now; everything else after Release 13 publishes |

## Tasks (Plan 20, phase 4)

Task ids continue Plan 20's `P` series. Routes per the run contract: `N` default, `X` very hard, `S` deepest reasoning, `T` taste. **Critical path:** P4.0 → P4.1 → P4.5 → P4.9. **Estimate:** about 5 days. **Test inventory:** Agent `tests/test_setup_skill_pack.py`, `tests/test_setup_skill_branches.py`, `tests/test_installer_maintained_guides.py`, `tests/core/generation/test_cli*.py`, `tests/test_cli_surface*.py`; App `src/shared/components/RuntimeConnection/copy.test.ts`. Re-check every path and line below against the code at dispatch.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| **Before the release (no code)** | | | | | |
| P4.0 Walk the path once and record it: an agent given only the skill URL, on a machine with ComfyUI running and a GPU, from install to an image on disk | N | OD3 | astrid-dev evidence only (`plans/20-zero-to-first-image/evidence/walk-1.md`); findings become rows `P4.0.<n>` | Live/manual; a cloud worker cannot run it. Record minutes to first image, every command run, every refusal with its text, and where the agent had to guess. Run once on the user's own workflow and once on a shipped entry | [ ] |
| **After Release 13 publishes** | | | | | |
| P4.1 One readiness report for generation: project, placement and its source, target reachable, engine installed, each default slot ready or not with the reason, a suggested first image (a ready shipped entry, else the server's saved workflows), and the next command | X | P4.0 | Agent `astrid/core/generation/cli.py` (new subcommand under `generate`, or `doctor --generation`; the card picks one and says why), `preflight.py`, `listing.py` (reuse, no second readiness logic), `astrid/packs/vibecomfy/local.py:scan` (reuse); `cli-surface.json` regenerated; new `tests/core/generation/test_readiness_report.py` | New test fails first: against the existing fake ComfyUI, the report names each missing piece and exactly one next command for (a) nothing running, (b) ComfyUI on 8188 with no project, (c) ready. One entry-point subprocess test. No new readiness rule: the test asserts its per-slot result equals `generate list` | [ ] |
| P4.2 One command makes a ComfyUI the saved default, and one store holds it | X | P4.1 (shares `cli.py`; different functions) | Agent `astrid/core/generation/cli.py`, `settings.py`, `targets.py:save_target`, `placement.py`. **Contract card:** today the target lives in `~/.vibecomfy/config.toml` and the placement in Runtime settings; this makes the Runtime placement the one saved choice and derives the target from it. List every test that pins the TOML write or `targets --save` and say how each changes | New test fails first: after `generate use http://127.0.0.1:8188` (name decided by the card), `generate targets` and the settings document agree; a discovered server can be saved; an old TOML selection is read once and not rewritten. Undo is one command and is tested | [ ] |
| P4.3 A project exists when a person first generates | N | OD5 | Agent `astrid/sdk/generation.py` (project resolution, about `:585-607`), `astrid/core/project/guidance.py`; tests beside them | New test fails first: with no project, generation creates and selects "My first project" (the App's name, `prepareStarterProject.ts`), prints one line saying so, and proceeds. With a project selected, nothing changes | [ ] |
| P4.4 Run a saved workflow from the user's server by name, with the prompt found for them | X | P4.1 | Agent `astrid/core/generation/cli.py` (`generate workflow`), `workflows.py`, `entries.py` (input naming, about `:433-464`), `astrid/packs/vibecomfy/local.py` | New test fails first, on the fake ComfyUI: `generate workflow --from-server NAME "a prompt"` fetches read-only into scratch, binds the prompt to the declared text input or refuses naming the candidates, and runs. Nothing is written to the server. `describe` marks which input is the prompt | [ ] |
| P4.5 The skill, rewritten local-first | N | P4.1–P4.4 (it names their commands) | Agent `astrid/packs/setup/docs/SKILL.md` (the source; `docs/setup/SKILL.md` regenerated by `scripts/generate_setup_skill_mirror.py`), `astrid/packs/generation/docs/SKILL.md` "Set up my generation". **Contract card:** `tests/test_setup_skill_branches.py` extracts fenced commands per branch, and `tests/test_installer_maintained_guides.py` pins headings and quoted installer lines; list each assertion the rewrite invalidates | The skill is the six steps above in about 100 lines: each command once, the launcher path defined once, RunPod one line linking the RunPod skill, the managed engine one line linking its section. The RunPod claim walkthrough is deleted here, not copied. One way of calling Astrid in both skills; the "never install during setup" contradiction is gone. Branch test: every fenced command parses and runs against the fakes; no step launches, restarts or writes to a ComfyUI | [ ] |
| P4.6 A missing model on the user's ComfyUI is explained truthfully | N | — | Agent `astrid/core/generation/backends/comfy_target.py` (about `:606-628`), `asset_gaps.py` (about `:52-73`); their tests | New test fails first: on an attached target the message names the file, its role and the folder from the server's own folder paths, and does not suggest `align --apply` (which writes to the managed engine). The managed-target message is unchanged | [ ] |
| P4.7 The skill's wording | T | P4.5 | Agent `astrid/packs/setup/docs/SKILL.md` wording only | Plan 20's taste rules; before and after shown to Hannah; P4.5's tests still pass | [ ] |
| P4.8 Every entry point ends at the same next step | N | P4.5 | Agent `astrid/installer/outcome.py` (one added line after the existing first lines, which the skill quotes; none changed); App: land the staged "Set up generation" card and its repairs (P2.3, R2.1, R2.2) and align its brief; Pinokio `README.md` | The installer's success output, the App card's brief and the Pinokio README each name the skill and the same sentence to give an agent. Installer outcome tests; `copy.test.ts`; a grep test that the three strings match | [ ] |
| P4.9 Proof and completion | N | all rows above | astrid-dev evidence and completion PR; repair rows `P4.9.<n>` | P4.0 repeated on the new path: minutes to first image and the count of commands, against walk 1. The CPU branch test green on hosted CI. Disposition for F-003 | [ ] |
| R4 Review, 1 round | S | P4.1–P4.8 | read-only | One round on the integrated branch per the run contract; findings become `R4.<n>` | [ ] |

**Deliberately not in this phase:** adopting a ComfyUI install that is not running; sharing its models folder with the managed engine; discovering ComfyUI Desktop; downloading models into the user's ComfyUI (OD4); Wan2GP (Plan 12); the RunPod path itself (Plan 40 and the machines work).

## Critique

The planning skill requires an independent critique before greenlight for a change to a user-visible flow. I wrote this draft, so I cannot be its critic. A fresh reviewer should check the tasks against the code, with a brief to build as little as possible, and in particular: whether P4.1 can be a mode of the existing `doctor` instead of a new command, whether P4.2 conflicts with Plan 35 (one home for user state), and whether P4.4 is needed for the first image or only convenient.
