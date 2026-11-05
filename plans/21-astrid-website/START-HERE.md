# Astrid homepage journey: hand-off

This folder holds everything an executor needs to build the scroll journey below the hero of the Astrid homepage, on top of the existing app. The plan is ready. Nothing has been built yet. The plan was written against astrid-app at the pins it states (`main` at `17e46de99`, 20 Oct 2026); Step 0 re-checks its pointers.

**Build only once Hannah says go.** Until then, read only.

## Read in this order

1. This file.
2. `PLAN.md`. Read the executor brief and Step 0 first. Where anything else in this folder disagrees with the plan, the plan wins.
3. `mockups/full-page-night.jpg` and `mockups/full-page-day.jpg`, which show the whole page end to end. The frames for each section are in `mockups/night/` and `mockups/day/`. They guide composition and tone; they aren't specs.
4. `evidence/`, which holds the code read and the two Opus reviews the plan was built from. Open these only when a task needs the background.

## The repo

| | |
|---|---|
| Repo | `banodoco/astrid-app`: https://github.com/banodoco/astrid-app |
| Where the work goes | Branch `feat/home-journey` off `main`, with one worktree and branch per task (`../hj-<id>`, `hj/<id>`); see plan 9.1 |
| Homepage code | `src/pages/Home/` (route `/home`) |
| The editor the hero runs | `src/tools/video-editor/` |
| Astrid source for the build | Vendored at `vendor/astrid-browser`, so no other checkout is needed (`ASTRID_CHECKOUT` overrides it) |
| Production | Merging into `main` deploys it. That happens only at R4, after Hannah says go |

Clone it into a folder of its own so the task worktrees sit beside it, then follow Step 0:

```sh
mkdir -p <work-folder>/home-journey && cd <work-folder>/home-journey
git clone https://github.com/banodoco/astrid-app.git
cd astrid-app   # Step 0 starts here: git fetch origin && git switch -c feat/home-journey origin/main
```

Any other astrid-app checkout on the owner's machine belongs to separate rename work. Don't build in it.

**Not needed:** `banodoco/astrid-runtime` and `banodoco/astrid-agent`. The homepage editor runs browse-only with no backend, and Playwright boots its own Vite and a fake Runtime.

### Main has moved since the plan was pinned

The plan's code pointers were checked against `main` at `17e46de99` (20 Oct 2026). When this zip was made, `main` was at `bebadd0e1`, 11 commits later. Step 0's pointer re-check exists for exactly this. Three of those commits touch ground the plan stands on:

- **`c447c6f89`** removed the sky review panel from `PublicAstridSky.tsx`, `PublicAstridSky.css` and `publicAstridSkySession.ts`. The sky calls the plan uses (`setManualHours`, `controlsSnapshot`, `patchSettings`) are all still there, but their line numbers moved: `setManualHours` is now at `publicAstridSkySession.ts:486`, where the plan says `:511`.
- **`8a8a32186`** (Video | Inspector | Extensions tabs on touch) and **`2fa200ce1`** (the editor's preview overlay, and seeking on touch) change the touch editor. Re-check part 2's touch and phone facts before the phone work starts.

## Other places

| What | Where |
|---|---|
| The interactive prototype: the mockups as a page you can scroll, plus this plan under "Engineering guide" | https://claude.ai/artifact/9VCoPoenac3Gs8foHTCYR2 (private to Hannah, so ask for it to be shared) |
| The mockup workspace: every round of frames, the briefs, and the build script that makes the prototype | The owner's Mac, outside this repository (not a git repo). Its round 4 brief has the copy intent for each section; PLAN part 5 holds the copy |
| A preview of the build | A Claude Artifact that the coordinator republishes (task P1). The fallback is `vite preview --host` on the LAN (plan 9.2) |

## Tools

- **Node 20.19.x for vitest.** Node 26 fakes hundreds of failures. Use a local Node 20.19.4 install: `export PATH=<path to Node 20.19.4>/bin:$PATH`.
- **Playwright.** The iPhone and iPad projects run on WebKit, so install it locally with `npx playwright install webkit`. CI installs only Chromium; task T26 deals with that.
- **Codex CLI 0.163 or later.** Use `gpt-6-luna`, `gpt-6.1-sol` (with `-c model_reasoning_effort='"xhigh"'`) and `gpt-6-astra`. If `gpt-6.1-sol` is refused, fall back to `gpt-6-sol`. Pass the repo's `.git` with `--add-dir` so that workers can commit (plan 9.2).
- **Claude Code** with Opus 5.5, Sonnet 5.5 and Haiku 5.5.

## Who does what

| Work | Model | Hands the legwork to |
|---|---|---|
| NORMAL tasks | Codex `gpt-6-luna` | more Luna |
| XHARD tasks | Codex `gpt-6.1-sol`, xhigh | Luna |
| TASTE-HIGH tasks; the desktop (R2-D) and phone (R2-P) iteration passes | Claude Opus 5.5 | Haiku |
| TASTE-LOW tasks | Claude Sonnet 5.5 | Haiku |
| R1, the performance pass | Codex `gpt-6-astra` | Luna |
| ASSET tasks | Placeholders only | |

The rule covers fixers as well. The coordinator, and every senior agent, keeps the judgment. Subagents' results are evidence to check, not verdicts.

## The rules that matter most

- **Two priorities.** Each section feels alive while you rest on it, and every transition between sections is really nice. When time is short, spend it on these two.
- **Bound by the experience, free in the implementation** (see the plan's executor brief).
- **No flags or hidden modes.** The work lives on `feat/home-journey` until R4.
- **Placeholders for all assets.** Nothing made in this phase claims to be real.
- **Scripted edits never save.** Scripted edits on the homepage never save, make drafts or write history.
- **Stop and ask Hannah at R4:** may the placeholders ship, and may the branch merge into `main`?

## What's in this folder

```
START-HERE.md            this file
PLAN.md                  the plan: v3, 34 tasks, then R1–R4. Commit it as docs/plans/home-journey/ in astrid-app (Step 0.3)
mockups/                 night/ and day/ frames for each section, and the two full-page JPGs
evidence/                DEEP-PASS-RESULT.md (Astra's code read), OPUS-REVIEW-RESULT.md, OPUS-CRAFT-RESULT.md
```
