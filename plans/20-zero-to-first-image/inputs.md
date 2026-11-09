# Inputs: zero-to-first-image onboarding

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** this is the owner's direction, not yet an agreed end state.

- **Source.** Hannah gave it on 9 Nov 2026. It was relayed in planning session `session_011EzfVzreGCJJQnTuXpbib9`, in two messages:
  - the onboarding-skill direction (items 1-4 in the [plan](plan.md#direction-owner-9-nov-2026));
  - two additions: put it in Plan 20, and handle the three choices routes.
- **The earlier direction the same day** (an attached ComfyUI through Plan 32 S2, and the App's "Set up generation" card) is kept.
- **Next:** Hannah answers D1–D9 below. A scope PR then records her answers here.

**Prior art.** Read at Agent `origin/cand/29-r12` `ff40f2c684` and App `cand/29-r12` `3274a9c07`.

| Area | Finding | Source |
|---|---|---|
| The setup skill exists and is already linked | `docs/setup/SKILL.md` (`name: astrid-setup`) is the README banner's target and the App brief's "Setup guide". It stops at Connected, and local engines are "not covered here yet" | Agent `docs/setup/SKILL.md:1-4,45-47`; `scripts/render_readme.py:9-19`; App `copy.ts:294,338` |
| It is not a synced skill | It is not a pack skill. Only pack `docs/**/SKILL.md` resources and `_CORE_FILES` reach the harness view. Sync links are named `astrid-<id>` and adopt only Astrid-managed targets | `astrid/skills/discovery.py:1-11`; `view.py:39-45`; `harnesses/base.py:19,115`; `harnesses/claude.py:30-36` |
| What the App brief carries | **Fresh install:** a yes/no consent line, all four values, and a command of `--yes` plus only the flags that differ from the recommendation. **Fully local:** the same. **Already set up, update or repair:** no choice line, and a plain or `--update` line. Choices are saved per browser in `localStorage` (`astrid:pending-setup-v1`) | `copy.ts:56-61,63-85,95-98,173-175,279-292,316-322`; `SetupBlock.tsx:33-68` |
| Where a user can change choices | Before copying, in the App's Customize panel (fresh install only). In a terminal, the installer's `[Y/n/c]` prompt. After install, only by rerunning the install line with an explicit flag. The installer prints each way back. The App has no surface for this after install | `SetupBlock.tsx:53-68`; `installer/cli.py:60-92,201-224`; `choices.py:45-65` |
| An agent's shell without `--yes` | Not a terminal, so the installer stops at `consent-required` and prints the plan and the exact rerun | `installer/cli.py:793-800`; `choices.py:68-79` |
| Shared contract | The App's `installArgv.fixture.json` mirrors the Agent's `tests/fixtures/installer/app_argv.fixture.json` | both files |
| Installer success and failure lines | `Astrid installed:`, `Astrid is installed and running`, `Astrid is already up to date`, `Astrid was NOT installed.` | `installer/outcome.py:137-159` |
| Doctor | The installer's `--doctor` writes a bundle and works even when the `astrid` command is off. `astrid doctor --bundle` needs the CLI | `installer/cli.py:472,920`; `core/gateway/dispatch.py:231-275` |
| A brief pattern that suits weaker agents | An exact command, its success words, a doctor fallback and "Don't try other fixes" | App `copy.ts:108-113` |
| Engine discovery | `scan` finds only *running* loopback ComfyUI (ports 8188 and 8000) and Pinokio apps. It finds no stopped ComfyUI and no Wan2GP (S2 adds a Wan2GP folder probe) | `packs/vibecomfy/local.py:386-417,459-467` |
| Capability | `detect_nvidia()` reads only GPU names (no memory). It is used only in the Windows preflight. Nothing detects Apple silicon or AMD | `core/generation/gpu_environment.py:46-99` |
| Managed engines | `engine-index.json` has Linux `comfyui` (cu130), Windows `vibecomfy` (cu130), `vibecomfy-h3` and Windows `wan2gp`, and nothing for macOS. The Windows environment plan says Astrid doesn't install ComfyUI on Linux or macOS "yet", although `astrid engines install comfyui` exists for Linux | `packs/engine-index.json`; `gpu_environment.py:130-153`; `core/engine_cli.py:33-50` |
| RunPod | The key is read from `RUNPOD_API_KEY` (by reference). Paid consent applies per claim, with `runpod.setup` | `packs/runpod/docs/SKILL.md:38-45,70-108` |
| Plan 32 S2 | Guided generation setup is read-only ("Never … download or install during setup"). Its scope includes the `docs/setup/SKILL.md` step and one `agentInstructions` line | [Plan 32 tasks](../32-generation-placement-targets/tasks.md) S2 row |

**Approach.** Extend the existing setup skill in place. Make the choices rule a shared fixture with a test per route. Add one read-only machine-check command. Leave generation discovery to Plan 32 S2. Alternatives considered:

| Alternative | Why not |
|---|---|
| A new `astrid-onboarding` skill beside `astrid-setup` | Two skills would cover the same install, and shipped App builds already link `docs/setup/SKILL.md`. Burn-down rule |
| A separate onboarding plan | The owner put it in Plan 20, and it would split one journey across two plans that edit the same file |
| Have the agent reuse the installer's interactive `[Y/n/c]` prompt | Agent shells are not terminals (`cli.py:795`). Choices must travel as flags |
| Put capability detection in the skill text (`nvidia-smi` and so on, per OS) | Too many commands per step for a weaker agent, and it would drift. One JSON command is testable |
| Fold the machine check into S2 | S2 is the existing-setup path. The machine check also decides the install and RunPod branches, and Plan 12 reuses it |
| Wait for Plan 32 for everything | Phase 1 (consent, entry points, doctor and the machine report) is useful now and touches nothing in Plan 32 |

**Challenge.** Pending. The plan touches a user-visible flow, consent and a cross-repo contract, so it needs the advisor's critique. That critique was not run, because this planning brief excluded session tools. **Next:** the planner or orchestrator runs the advisor ([Orchestrate](../../skills/astrid-dev-orchestrate/SKILL.md)) before dispatch. Brief it to cut O5 or O7 if S2 or the existing brief can carry them.

**Proof and limits.** See O8. Real inference is proven only on the hardware recorded there. macOS has no managed engine, so its proof is the pointer-and-RunPod branch. Wan2GP and providers are excluded.

## Owner decisions needed

| # | Decision | Recommendation |
|---|---|---|
| D1 | The skill's name and path | Keep `docs/setup/SKILL.md`, `name: astrid-setup`. Shipped App builds and the README already link it. Retitle it "Set up Astrid, from install to first image" |
| D2 | How to install it optionally, before Astrid exists | Use it from its URL by default. The optional pre-install is one line per OS that saves it under the agent's skills folder as an Astrid-managed copy (with the `.astrid-managed-skill.json` marker, `harnesses/base.py:19`), so that skills-on sync adopts it and leaves one copy |
| D3 | Does the skill run a managed engine install, or only link to it? | Run it, as its own step with its own yes, where Astrid has a managed engine (Linux and Windows NVIDIA). Link only where it has none (macOS). S2's read-only rule stays for "Set up my generation" |
| D4 | What counts as "capable" | The default image entry's declared requirement, once Plan 32 T2's manifest declares one. Until then, an NVIDIA GPU with at least 12 GB on Linux or Windows, as one constant. On macOS: not capable for a managed engine; offer ComfyUI's own installer, then attach, or RunPod |
| D5 | RunPod during onboarding | Use paid consent per claim, plus a low budget cap for the test generation (Plan 32 T6d's `machines.runpod` cap; suggest $2), and release the machine afterwards unless the user keeps it warm |
| D6 | The App's consent line | Replace "May I install Astrid with these setup choices?" with "show and offer a change" (O3), with the flag spellings in the brief |
| D7 | The overlap with Plan 32 S2 | Move S2's `docs/setup/SKILL.md` step and its App brief line to this plan (O1, O3). S2 keeps the generation skill section, the Wan2GP probe and `--as-entry` |
| D8 | Proof hardware, budget and the weaker agent | One Linux NVIDIA machine, or a RunPod pod used as a local machine. Hosted macOS and Windows runners for everything up to the generation branch. Up to $10 of RunPod for the real images. Pick one smaller model as the "weaker agent" |
| D9 | Review rounds | 2: a user-visible consent flow and a cross-repo fixture, but no data migration |

## Source identities

| Repository | Planning read | Base at start | Candidate branch | Destination |
|---|---|---|---|---|
| astrid-agent | `origin/cand/29-r12` `ff40f2c684` (read-only) | the release 12 published revision, recorded before O1 | one Agent branch for Plan 20 | Agent `main`, through the release process |
| astrid-app | `cand/29-r12` `3274a9c07` (read-only) | the release 12 published revision, recorded before O3 | one App branch for Plan 20, after Plan 29's orchestrator agrees | App `main`, through the release process |
| astrid-dev | `origin/main` `d1de270` | — | `plans/onboarding-skill` | `main` through a scope PR |

## References

- [Plan 32](../32-generation-placement-targets/plan.md): S2, T5, T5d and T6d are consumed. [Plan 12](../12-multiple-inference-routes/plan.md): later Wan2GP rows. [Plan 29](../29-update-and-release/plan.md): owns release 12. [Plan 35](../35-one-home-for-user-state/plan.md): App-side choice state after install. [Plan 15](../15-openshell-safe-execution/plan.md) and [Plan 16](../16-streamlined-agent-experience/plan.md): out of scope.
- [Liquid Software vision](../../vision/pillars/liquid-software.md): good defaults, choices people understand, and user control.
