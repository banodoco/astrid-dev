# Zero-to-first-image onboarding

**Project:** Zero-to-first-image onboarding

**Goal:** One onboarding skill, named at every install entry point (the Agent README and the App's install briefs), takes a person or their agent from the install line to a generated image on the timeline. Setup choices stay visible and changeable on the agent path. The skill uses an existing ComfyUI, installs an engine on a capable machine, or rents RunPod otherwise.

**Status:** active

**Owner:** Plan 20 manager

**Estimate:** 10–11: phase 1 (fast path, live on merge) 1, phase 2 (next App release) 1, phase 3 3–4, phase 4 (local-first) about 6

**Waiting on:** release 12 published, then the owner's go to merge the Agent `main` group; the App group rides the next App release; the generation group waits on Plan 32 S2, T5d and T6d; phase 4 runs now, with work on release 13 code landing only after release 13 publishes; OD1, OD2, OD4 and OD5 are built at their recommendations, flagged for the owner

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

## Direction (owner, 9 Nov 2026)

Hannah gave this direction on 9 Nov in two parts. The source is in [inputs.md](inputs.md#planning-evidence).

**Earlier the same day: the first image.** The route is **an attached ComfyUI** (the user's own), reached through [Plan 32](../32-generation-placement-targets/plan.md) S2's guided generation setup. After Connected, the App's welcome flow shows a **"Set up generation" card** with a "Copy for your agent" brief. Its proof is a real first image from a saved workflow.

**Later: one onboarding skill, from the first install line to the first image.**

1. Every place where a person can start installing Astrid points to the onboarding skill and tells them, or their agent, to use it. That means the Agent README and every App screen where they copy the install line or an agent brief. Installing the skill is optional.
2. If they use it, the skill guides them through the whole process.
3. The skill ends at Connected. Looking for an existing inference setup (ComfyUI, Wan2GP or similar) and the step after it live in Plan 32 S2's guided generation setup, in the same skill file: see the S2 row in [Plan 32's tasks](../32-generation-placement-targets/tasks.md) (D7, reversed by the owner on 9 Nov). Phase 3 adds an engine install on a capable machine and RunPod otherwise, on top of that step.
4. On the agent path, the user still sees the setup choices (start at sign-in, the `astrid` command, coding-agent skills, skill copies) and can change them. An agent-led install never silently takes the recommended defaults.
5. **This is part of this plan, not a new one** (owner, relayed 9 Nov). Some users will already have chosen setup choices in the App, so the skill handles each entry route by the [choices rule](#the-choices-rule).

## Direction (owner, 14 Nov 2026): local-first

Hannah asked the advisor to map the path for someone running ComfyUI locally, and to make the onboarding local-first. Her words are in [inputs.md](inputs.md#phase-4-local-first-14-nov-2026). In short: RunPod gets a one-line mention, and the rest of the skill is for people running locally. This is **phase 4**. OD3, OD6, OD7 and OD8 are decided. OD1, OD2, OD4 and OD5 are Pending, built at their recommendations and flagged. Once OD1 is confirmed it supersedes point 3 above (the skill ends at Connected) and D7's split with Plan 32 S2, for the local path only.

## Outcome and scope

A person on macOS, Linux or Windows starts at any install entry point: the Agent README, astrid.haus's setup screens, or the fully local setup. They, or their agent, follow one skill. It installs Astrid with choices they saw and could change, connects astrid.haus, and goes on into generation setup (Plan 32 S2's step, see the S2 row in [Plan 32's tasks](../32-generation-placement-targets/tasks.md)) to a real generated image on a timeline.

- **Included:**
  - **The onboarding skill** is `docs/setup/SKILL.md` (`astrid-setup`), extended end to end rather than replaced. Its public URL is already in the README banner (`scripts/render_readme.py:12-14`) and in every App install brief (`SETUP_GUIDE_URL`, App `copy.ts:294`, used at `:338`). Shipped App builds carry that URL, so the path stays.
  - **Distribution:** the skill works from its public URL without being installed. After Astrid is installed with skills on, the skill is also in the synced skill view (`astrid/skills/view.py`), so "set up my generation" and re-onboarding work offline. An optional pre-install puts the same file where `astrid skills sync` later adopts it, not beside it (owner decision D2).
  - **Every entry point names it** ([list](tasks.md#entry-points)): the README banner and its generator, the App's hosted and fully local install briefs, the install disclosure on the Connect card, the "stopped" card, and the welcome flow's setup screen.
  - **The setup choices on the agent path**, by the [choices rule](#the-choices-rule).
  - **Finding a place to generate:** Plan 32 S2's guided step (existing setup, read-only discovery), see the S2 row in [Plan 32's tasks](../32-generation-placement-targets/tasks.md). Phase 3 (P3.1) adds, around it, the engine install where Astrid manages one (its own yes) and RunPod through Plan 32's `generation.machine` route with paid consent.
  - **A step shape that a weaker agent can follow:** one command per step, an explicit success check, and one fallback: run the installer's `--doctor` and give the user the file path.
  - **The App side from the earlier direction:** the "Set up generation" card after Connected.
  - **Proof** of what a fresh user sees on each OS (hosted runners on CPU, plus one real GPU image), and the measured effort.
- **Not included:**
  - Wan2GP as a usable engine. Plan 12 adds it, and an attached Wan2GP is deferred there (no endpoint). The skill reports a found Wan2GP and moves on.
  - Provider APIs (fal, OpenAI, Wavespeed) as a placement, which is Plan 32's providers follow-up. Discovery lists their keys by presence only, as S2 does.
  - Changing setup choices from the App after install. That would be App state, so it belongs with [Plan 35](../35-one-home-for-user-state/plan.md).
  - The sandbox ([Plan 15](../15-openshell-safe-execution/plan.md)) and agent sign-in ([Plan 16](../16-streamlined-agent-experience/plan.md)).
- **Not in release 12.** Release 12's candidate (`cand/29-r12`) is frozen under [Plan 29](../29-update-and-release/plan.md). Nothing here starts until release 12 is published, and App tasks check with Plan 29's orchestrator first.

## The choices rule

The App's brief carries choices only for a fresh install, and the skill must keep what it carries. Source: App `cand/29-r12` at `3274a9c07`.

| Entry route | What the brief or command carries today | What the skill does |
|---|---|---|
| **Choices supplied:** an App brief for a fresh install (hosted or fully local) | `copy.ts:321` asks one yes/no question ("May I install Astrid with these setup choices?"). `:322` lists all four values; the fully local brief has the same lines at `:173-174`. The command is `--yes` plus a flag **only for each value that differs from the recommendation** (`installCommand` `:287-291`, `setupChoiceFlags` `:95-98`). For example, an untouched setup is just `--yes` (shared fixture case `untouched`) | Show the four values back as the user's decision and offer a change. A brief from a shipped App build still asks the yes/no question; the skill asks it as "install with these choices, or change one?" and waits. On no change, run the command exactly as given. On a change, run the same line with every flag explicit. Never silently replace the values, re-ask from scratch, or drop a flag |
| **No choices supplied:** the README banner, a bare install line, or the public URL alone | The banner (`render_readme.py:9-19`) carries no choices. The bare line `curl -fsSL https://astrid.haus/install \| sh` without `--yes` in an agent's shell (not a terminal) stops at `consent-required` and prints the plan and an exact rerun (`installer/cli.py:793-800`, `choices.py:68-79`) | Present the four choices with the recommended values (`choices.py:9-14`) and let the user change any of them. Then run one command with `--yes` and all four flags explicit |
| **Already set up:** the "I've already set up Astrid" checkbox, an update, a repair or Settings | No consent line and no choice line (`copy.ts:318-322`). The command is the plain line or `--update` (`:284-286`), so the Agent applies the saved choices (`choices.py:45-65`: explicit > saved > prompt or `--yes` > recommended) | Keep the saved choices. Change one only when the user asks, by adding just that explicit flag. Explicit flags win over saved ones (`choices.py:62`) |

The rule is enforced by tests in both repositories. **Agent (phase 1):** the guide test checks that the skill states the three routes in order with the command shape each one uses; the installer's own tests already prove each route's behaviour (`tests/test_installer_choices.py`). **App (phase 2):** one `copy.test.ts` case per App route, built from the existing shared argv fixture's case ids (App `installArgv.fixture.json`, mirrored by Agent `tests/fixtures/installer/app_argv.fixture.json`), with no schema change. See P1.1 and P2.1 in [tasks.md](tasks.md).

## Existing work and decision

- **Placement: this plan, not a new one** (owner). Plan 20 already owns the first-image journey, and its earlier direction already reaches into Plan 32 S2. A separate onboarding plan would split one journey across two plans that edit the same skill file and the same brief line.
- **Coordinating with [Plan 32](../32-generation-placement-targets/plan.md) S2.** S2 keeps the generation side: the "Set up my generation" section of the generation skill, the `docs/setup/SKILL.md` generation step after Connected, the Wan2GP folder probe and the `--as-entry` preview (D7: the owner reversed the earlier move of that step to this plan, 9 Nov; see the S2 row in [Plan 32's tasks](../32-generation-placement-targets/tasks.md)). This plan's skill ends at Connected. Whether S2's App line in `agentInstructions` stays in S2 beside P2.1's pointer line is not settled by the reversal; the two edits merge in order (P2.1, then S2).
- **Coordinating with [Plan 12](../12-multiple-inference-routes/plan.md).** Wan2GP rows come later and add no new step.
- **Reused, not rebuilt:**
  - the installer's choice resolution and consent stop (`astrid/installer/choices.py`, `cli.py:793-800`), with its success and failure first lines (`outcome.py:137-159`);
  - `--doctor` (`installer/cli.py:472`, `:920`);
  - the stable launcher path (`docs/setup/SKILL.md:91-97`). Every Astrid command in the skill uses it, because the user may have turned the `astrid` command off;
  - the ComfyUI scan (`astrid/packs/vibecomfy/local.py:386-417`);
  - `detect_nvidia()` (`astrid/core/generation/gpu_environment.py:46-63`);
  - the engine index (`astrid/packs/engine-index.json`);
  - the App's weaker-agent brief pattern: an exact command, its success words, a doctor fallback and "don't try other fixes" (`autostartOffAgentBrief`, `copy.ts:108-113`).
- **Alternatives considered** are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

**Re-planned around a fast path (owner, 9 Nov 2026).** Hannah asked why onboarding took 9–11 days. The writing is the small part; the time was in real-OS proof, App release cycles, a new machine-check command and review rounds. The skill and the README banner are read from Agent `main` on GitHub by every install path, including shipped App builds (`SETUP_GUIDE_URL`, App `copy.ts:294`), so skill and README text goes live when it merges to Agent `main`, with no release. She accepted re-planning on that basis ([inputs.md](inputs.md#planning-evidence)). There are three phases, each useful alone, and a proposed fourth (14 Nov).

| Phase | What lands | Goes live | Waiting on | Estimate |
|---|---|---|---|---|
| **1. Fast path** | The skill rewritten for the whole guided install, with the [choices rule](#the-choices-rule), the step shape and a skill that ends at Connected. The README and Getting Started point at it and drop the "`--yes` without a prompt" advice. Agent docs, the README and its generator, and the guide tests only | When the PR merges to Agent `main` | Release 12 published: the skill quotes installer first lines that exist only in release 12 (`outcome.py:137-166` on `cand/29-r12`, absent on Agent `main` at `a105de3a48`) | 1 day |
| **2. Next App release** | The App brief's yes/no consent line becomes "show these choices and offer a change", with the four flag spellings and a pointer to the skill, in both install briefs; the entry screens show the pointer; the "Set up generation" card after Connected links Plan 32 S2's "Set up my generation" section | With the next ordinary App release; no release of its own | Phase 1 merged; Plan 29's orchestrator for the App branch; for the card, Plan 32 S2's section on Agent `main` | 1 day, plus the wait for the release |
| **3. Generation half** | On top of Plan 32 S2's generation step, the skill does it rather than points: use an existing setup, install a managed engine (its own yes), or rent RunPod (paid consent and a cap). The skill reaches the synced skill view. Lighter per-OS proof with one real GPU image. Completion | Skill text on merge to Agent `main`; the synced-view change with the next Agent release | Plan 32 S2, T5d and T6d in a published release | 3–4 days |
| **4. Local-first** (14 Nov) | The skill carries on past Connected to a first image from the person's own running ComfyUI and models, in about 100 lines: install and connect; see what you have (one readiness report); one yes saves the connection; a project exists; a first image from a ready shipped entry or the person's own saved workflow; defaults after the win. RunPod and the managed engine are one line each, linking their own skills. The App card, the installer's success output and Pinokio's README all end at the same next step. See [phase 4](#phase-4-local-first) | Skill text on merge to Agent `main`; the Agent code (P4.1, P4.3, P4.4, P4.6, P4.8, P4.10, P4.11a) with the next Agent release; the App card with the next App release | Runs now (14 Nov). Work on release 13 code branches from Agent `r13/compose` and lands after release 13 publishes. OD1, OD2, OD4 and OD5 are built at their recommendations and flagged | about 6 days |

Users get value after phase 1: an agent following the README or a shipped App brief gets one guided install with choices they saw, ending at Connected.

**Not built, and why** (the Challenge note asked whether to cut these):

- **The machine-check command (earlier O5) is deferred out of this plan, and the skill has no machine look in phase 1** (D7). Phase 3's capability read is one `nvidia-smi` query (P3.1). A command adds an Agent release, a new CLI surface and a schema test for one consumer. Reopen it when Plan 32 T2's manifest declares per-entry requirements, when Plan 12 needs it, or when phase 3's proof shows a weaker agent misreading the query.
- **The "Set up generation" card (earlier O7) is kept, and moved to phase 2.** On the agent path the install brief already leads to generation through the skill, but a person who installed by hand from the README, or stopped at Connected and came back, has no other way in, and the owner's earlier direction names it. Moving it to phase 2 lets it ride the same App release as the brief, so phase 3 needs no App release: the card links Plan 32 S2's "Set up my generation" section (not a heading in this plan's skill, D7), and the text behind it improves live when that merges. It shows in the post-Connected welcome flow only; knowing whether generation is already set up waits for Plan 32 T6d's settings document.
- **The per-OS proof (earlier O8) is lighter.** Hosted macOS, Windows and Linux runners on CPU cover install, choices, Connected and branch selection, ending at each branch's first command against a fake. One real GPU image comes through RunPod. The limits are stated in [Completion](#completion) and [tasks.md](tasks.md).
- **The `route` field in the shared argv fixture is dropped.** The Agent's installer tests already cover each route's behaviour (`tests/test_installer_choices.py`: precedence, the unattended consent stop, saved policy on update), and the fixture's existing case ids (`untouched`, `edit-*`, `already-set-up`) name the App's routes. A new field would have to be mirrored in two repositories for no new check. The old O2 folds into phase 1's guide test.

**Reviews:** R1, R2 and R3, one final review per phase ([tasks.md](tasks.md)); their round counts are the agreed D9 (1, 1 and 2). Copy and wording are their own small `T` tasks, separate from the functional `N` tasks that give each surface its structure and tests. Owner decisions D1–D9 are in [inputs.md](inputs.md#owner-decisions-needed): D3, D5, D6, D7 and D9 are decided; D1, D2, D4 and D8 are Pending: owner to confirm. See [tasks.md](tasks.md) for routes and the critical path. Recording this plan authorizes no product work.

### Phase 4: local-first

**Outcome.** A person who already runs ComfyUI points Astrid at it and gets an image from it within a few minutes, without Astrid changing anything on their ComfyUI, using the models they already have. The setup skill reads as a local path from install to that image. RunPod and Astrid's managed engine are one line each for people with no local GPU or ComfyUI.

**Why a new phase.** The advisor's map ([draft](phase-4-local-first-draft.md), 14 Nov) found that install works but the path stops at Connected, and the rest is unproven. There is no single report of what is ready. The saved placement and `generate targets` can disagree. The agent path has no project. Shipped image entries are ready only with exact model files. A missing-model refusal points to the managed engine. Running a saved workflow is a hand fetch, and its custom nodes may not resolve. Saved workflows are not listed newest first. Every live run so far was on RunPod. The tasks are in [tasks.md](tasks.md), and the critique and what it changed are in [inputs.md](inputs.md#phase-4-local-first-14-nov-2026).

**Not in phase 4:** a new store or a migration for the saved ComfyUI (P4.2 saves it in the existing Runtime settings); finding a workflow's prompt automatically; one home per concept beyond the onboarding docs (that stays with [Plan 19](../19-first-principles-documentation/plan.md)); adopting a ComfyUI that is not running; sharing its models folder with the managed engine; discovering ComfyUI Desktop; downloading models into the person's ComfyUI (OD4); Wan2GP (Plan 12); the RunPod path itself (Plan 40 and the machines work).

**Completion.** P4.0's walk, repeated on the new path (P4.9), on a hosted CPU runner against the fake ComfyUI: minutes to the admitted generation command and the number of commands, compared with the first walk. The result gives one link that opens the project with the image in the Generations pane (OD7). The CPU branch test is green on hosted CI. A negative case: no step launches, restarts or writes to the person's ComfyUI. Limits: no GPU and no rentals (D8, reaffirmed by OD3). The real first image on a person's own ComfyUI is one row requested from Plan 34.

## Interfaces and handoff

- **Consumes:**
  - release 12 as published, with its exact revisions recorded in [inputs.md](inputs.md#source-identities) before phase 1 merges;
  - the next ordinary App release (phase 2);
  - Plan 32's S2 skill section, the `generation.machine` RunPod contribution (T5, T5d) and the generation settings document (T6d).
- **Produces:**
  - one onboarding skill at a stable public URL, ending at Connected;
  - the choices rule, tested per route in both repositories against the existing shared argv fixture;
  - an install brief and a README that point to the skill.
- **No longer produced here:** the machine-check command (deferred; see [Sequence](#sequence-and-readiness)).

## Completion

- **Fresh users.** A fresh user on each OS (hosted runners, P3.5) starts from the README and from astrid.haus and sees:
  - the four choices, which they can change;
  - one install command;
  - Connected;
  - a real generated image on a timeline (once, through RunPod; the other branches end at their first command against a fake). The route to it is Plan 32 S2's generation step, not a section of this plan's skill.
- **The three routes.** Each choices route has a passing test: the guide test and installer tests in the Agent, and a `copy.test.ts` case per App route. An App brief with changed choices installs with exactly those choices, and an already-set-up install keeps its saved ones.
- **Negative cases:**
  - the agent declines to change choices without asking;
  - the installer fails, and the skill stops after `--doctor` with the file path;
  - no GPU and no RunPod key, and the skill stops with what is missing;
  - an existing ComfyUI is never launched or restarted.
- **Effort.** Total agent tokens from the first instruction to the end of each proof row (the visible image on the RunPod row) are recorded per run, including retries, against the ~50,000 target.
- **Limits.** No live GPU tests in this plan (owner, 10 Nov; D8). Every branch, the RunPod one included, is proven on hosted CPU runners up to its first command against a fake, not with real inference. Real inference is [Plan 34](../34-real-gpu-proof/plan.md)'s. On a headless runner "Connected" is the Runtime's health line, not the browser page. Unsupported combinations (for example, a managed engine on macOS) are listed, not implied. Wan2GP and providers are not proven here. F-003 does not close automatically.
