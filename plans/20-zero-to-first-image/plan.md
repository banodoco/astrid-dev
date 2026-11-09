# Zero-to-first-image onboarding

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

## Direction (owner, 9 Nov 2026)

Hannah gave this direction on 9 Nov in two parts. The source is in [inputs.md](inputs.md#planning-evidence).

**Earlier the same day: the first image.** The route is **an attached ComfyUI** (the user's own), reached through [Plan 32](../32-generation-placement-targets/plan.md) S2's guided generation setup. After Connected, the App's welcome flow shows a **"Set up generation" card** with a "Copy for your agent" brief. Its proof is a real first image from a saved workflow.

**Later: one onboarding skill, from the first install line to the first image.**

1. Every place where a person can start installing Astrid points to the onboarding skill and tells them, or their agent, to use it. That means the Agent README and every App screen where they copy the install line or an agent brief. Installing the skill is optional.
2. If they use it, the skill guides them through the whole process.
3. The skill looks for an existing inference setup (ComfyUI, Wan2GP or similar). If it finds one, it uses it. If not, and the machine is capable (for example it has a suitable GPU), it points them to that engine's install. If the machine isn't capable, it points them to a remote machine: RunPod, through Plan 32's generation-machine route.
4. On the agent path, the user still sees the setup choices (start at sign-in, the `astrid` command, coding-agent skills, skill copies) and can change them. An agent-led install never silently takes the recommended defaults.
5. **This is part of this plan, not a new one** (owner, relayed 9 Nov). Some users will already have chosen setup choices in the App, so the skill handles each entry route by the [choices rule](#the-choices-rule).

## Outcome and scope

A person on macOS, Linux or Windows starts at any install entry point: the Agent README, astrid.haus's setup screens, or the fully local setup. They, or their agent, follow one skill. It installs Astrid with choices they saw and could change, connects astrid.haus, finds or sets up a place to generate, and ends with a real generated image on a timeline.

- **Included:**
  - **The onboarding skill** is `docs/setup/SKILL.md` (`astrid-setup`), extended end to end rather than replaced. Its public URL is already in the README banner (`scripts/render_readme.py:12-14`) and in every App install brief (`SETUP_GUIDE_URL`, App `copy.ts:294`, used at `:338`). Shipped App builds carry that URL, so the path stays.
  - **Distribution:** the skill works from its public URL without being installed. After Astrid is installed with skills on, the skill is also in the synced skill view (`astrid/skills/view.py`), so "set up my generation" and re-onboarding work offline. An optional pre-install puts the same file where `astrid skills sync` later adopts it, not beside it (owner decision D2).
  - **Every entry point names it** ([list](tasks.md#entry-points)): the README banner and its generator, the App's hosted and fully local install briefs, the install disclosure on the Connect card, the "stopped" card, and the welcome flow's setup screen.
  - **The setup choices on the agent path**, by the [choices rule](#the-choices-rule).
  - **Finding a place to generate:**
    - an existing setup through Plan 32 S2's read-only discovery;
    - a read-only machine check (OS, CPU architecture, NVIDIA devices with memory, Apple silicon and memory, and whether Astrid has a managed engine for this platform);
    - the engine install where Astrid manages one, as its own step with its own yes;
    - otherwise RunPod, through Plan 32's `generation.machine` route with paid consent.
  - **A step shape that a weaker agent can follow:** one command per step, an explicit success check, and one fallback: run the installer's `--doctor` and give the user the file path.
  - **The App side from the earlier direction:** the "Set up generation" card after Connected.
  - **Proof** of what a fresh user sees on each OS, and the measured effort.
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
| **Choices supplied:** an App brief for a fresh install (hosted or fully local) | `copy.ts:321` asks one yes/no question ("May I install Astrid with these setup choices?"). `:322` lists all four values; the fully local brief has the same lines at `:173-174`. The command is `--yes` plus a flag **only for each value that differs from the recommendation** (`installCommand` `:287-291`, `setupChoiceFlags` `:95-98`). For example, an untouched setup is just `--yes` (shared fixture case `untouched`) | Show the four values back as the user's decision and offer a change. On no change, run the command exactly as given. On a change, run the same line with every flag explicit. Never silently replace the values, re-ask from scratch, or drop a flag |
| **No choices supplied:** the README banner, a bare install line, or the public URL alone | The banner (`render_readme.py:9-19`) carries no choices. The bare line `curl -fsSL https://astrid.haus/install \| sh` without `--yes` in an agent's shell (not a terminal) stops at `consent-required` and prints the plan and an exact rerun (`installer/cli.py:793-800`, `choices.py:68-79`) | Present the four choices with the recommended values (`choices.py:9-14`) and let the user change any of them. Then run one command with `--yes` and all four flags explicit |
| **Already set up:** the "I've already set up Astrid" checkbox, an update, a repair or Settings | No consent line and no choice line (`copy.ts:318-322`). The command is the plain line or `--update` (`:284-286`), so the Agent applies the saved choices (`choices.py:45-65`: explicit > saved > prompt or `--yes` > recommended) | Keep the saved choices. Change one only when the user asks, by adding just that explicit flag. Explicit flags win over saved ones (`choices.py:62`) |

The rule is enforced by tests, one per route, in both repositories: the cross-repo argv fixture (App `installArgv.fixture.json`, Agent `tests/fixtures/installer/app_argv.fixture.json`) gains a `route` field and the cases above. See O2 and O3 in [tasks.md](tasks.md).

## Existing work and decision

- **Placement: this plan, not a new one** (owner). Plan 20 already owns the first-image journey, and its earlier direction already reaches into Plan 32 S2. A separate onboarding plan would split one journey across two plans that edit the same skill file and the same brief line.
- **Coordinating with [Plan 32](../32-generation-placement-targets/plan.md) S2.** S2 keeps the generation side: the "Set up my generation" section of the generation skill, the Wan2GP folder probe and the `--as-entry` preview, all read-only. Two items in S2's scope, the `docs/setup/SKILL.md` step and the one line in the App's `agentInstructions`, move to this plan's O1 and O3. One pointer line in the brief then names the onboarding skill, and that skill routes to "Set up my generation". This avoids two pointers and two plans editing the same text. Hannah needs to confirm this move (D7); S2's row records the pointer.
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

There are two phases, and each is useful alone.

1. **Phase 1, after release 12 is published. It does not depend on Plan 32.**
   - O1: the skill's install half and the shape of every step.
   - O2 and O3: the choices rule in the Agent and the App, with one test per route.
   - O4: the README and App entry points.
   - O5: the read-only machine check.

   Users then get one guided, consented install that ends with an honest "here is what you can generate with, and how". The first image itself still uses today's generation skill.
2. **Phase 2, after Plan 32 S2, T5d and T6d:**
   - O6: the skill's generation half (use, install or rent);
   - O7: the App's "Set up generation" card;
   - O8: proof on each OS and the effort measurement;
   - the review rounds, then completion.

Owner decisions D1–D9 are listed in [inputs.md](inputs.md#owner-decisions-needed). See [tasks.md](tasks.md). Recording this plan authorizes no product work.

## Interfaces and handoff

- **Consumes:**
  - release 12 as published, with its exact revisions recorded in [inputs.md](inputs.md#source-identities) at the start;
  - Plan 32's S2 skill section, the `generation.machine` RunPod contribution (T5, T5d) and the generation settings document (T6d).
- **Produces:**
  - one onboarding skill at a stable public URL;
  - the choices rule as a tested cross-repo fixture;
  - a read-only machine-check command that Plan 32 S2 and Plan 12 can reuse;
  - an install brief and a README that point to the skill.

## Completion

- **Fresh users.** A fresh user on each OS starts from the README and from astrid.haus and sees:
  - the four choices, which they can change;
  - one install command;
  - Connected;
  - a generation route that fits their machine: their existing ComfyUI, a managed engine install, or RunPod;
  - a real generated image on a timeline.
- **The three routes.** Each choices route has a passing test in both repositories. An App brief with changed choices installs with exactly those choices, and an already-set-up install keeps its saved ones.
- **Negative cases:**
  - the agent declines to change choices without asking;
  - the installer fails, and the skill stops after `--doctor` with the file path;
  - no GPU and no RunPod key, and the skill stops with what is missing;
  - an existing ComfyUI is never launched or restarted.
- **Effort.** Total agent tokens from the first instruction to the visible image are recorded per run, including retries, against the ~50,000 target.
- **Limits.** The proof uses real inference on the hardware recorded in O8. Unsupported combinations (for example, a managed engine on macOS) are listed, not implied. Wan2GP and providers are not proven here. F-003 does not close automatically.
