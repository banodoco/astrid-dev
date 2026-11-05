# Glossary

Plain definitions for terms used across the plans and skills. Plan-specific terms are defined in that plan's own `plan.md`. If a term here disagrees with the [run contract](../skills/astrid-dev-shared/run-contract.md) or [AGENTS.md](../AGENTS.md), those win.

## Product repositories

| Name | URL | Owns |
|---|---|---|
| Agent | https://github.com/banodoco/astrid-agent | Python package and CLI, SDK, generation, packs, skills, installer. Pins Runtime in `runtime.lock.json`. |
| Runtime | https://github.com/banodoco/astrid-runtime | Workspace service: projects, media, timelines, tasks, runs, receipts. |
| App | https://github.com/banodoco/astrid-app | Editor app and the user-facing install manifest. Pins Agent and Runtime. |
| Pinokio launcher | https://github.com/banodoco/astrid-pinokio | Pinokio install, start, stop and update scripts. Follows the published tuple. |
| VibeComfy | https://github.com/banodoco/VibeComfy | ComfyUI workflow and template library that Agent uses as its inference route. Also reachable as `banodoco/VibeComfy`. |
| runpod-lifecycle | https://github.com/banodoco/runpod-lifecycle | Library that provisions, runs and tears down RunPod pods. Agent depends on it. |

The normal pin order is Runtime, then Agent, then App, then Pinokio (see the [dev skill](../skills/astrid-dev/SKILL.md)).

## Branches and refs

- **main**: the repository's default branch. Plans never publish to it directly.
- **pre-main**: the rolling integration branch this initiative lands work on in Agent, Runtime and App before anything reaches `main`. Some producer repositories (VibeComfy, runpod-lifecycle) have no `pre-main`; the plan then says what to use instead.
- **int/r1**: the Release 1 integration branch in each product repository (see [Plan 08](../plans/08-release1-install-update.md)). Landed work is mirrored fast-forward to `pre-main`.
- **release-1**: the Release 1 release branch. Like `main` and `int/r1`, it is never force-pushed or published to by an ordinary plan task.
- **lane**: a branch holding one piece of unmerged work, for example `lane/M-GPU/...`. A lane is a work location, not a destination. Commits that exist only on a lane are not safe to pin until they land on a protected branch.
- **donor**: a retained commit or branch whose changes are merged into a candidate. A donor is an input, not an accepted result.
- **base**: the frozen commit a candidate is built from. Distinct from donors. In a check, "base" also means the unchanged side used to classify a failure as pre-existing.
- **candidate**: the composed branch and exact commit under test. A proof applies only to the candidate it names.

## Run vocabulary

- **source identity**: the repository, ref, commit SHA and dirty state of a base or donor. Confirm it at the start; never assume a branch exists.
- **custody**: who holds a source or a running process. For source, it records where the working copy lives and who may change it. For engines, it means which process owns a started engine and may stop it.
- **freeze**: record the exact SHAs of the base and donors at a point in time. Later movement of a branch does not change a frozen record; if the destination moves, reconcile and repeat only the affected checks.
- **tuple**: the set of exact versions that must work together, here Runtime, Agent, App (and Pinokio) SHAs. A tuple is qualified together, not per repository.
- **pin / repin**: a pin fixes a dependency to an exact commit in a lock or manifest. Repinning updates it, using the repository's own script, after the producer has landed.
- **card**: a self-contained task brief from the earlier M-GPU run. Cards in the retained run materials are evidence for what to do, not instructions to run blindly.
- **focused check**: a test or command explicitly named for the work, with an exact selector. Never a broad or auto-discovered suite.
- **closure**: a check that a fresh install pulls in a complete, pinned set of dependencies and the expected pieces actually import.
- **PASS / FAIL / RETRYING / NO-RESULT**: proof statuses defined in the run contract. NO-RESULT means evidence is missing; it is not a pass and not a product failure.
- **promotion**: moving the exact reviewed commits to the destination branch with ordinary fast-forward or create operations. Publication and deployment are separate, explicitly authorized steps.

## Routing and review

- **routes N / X / S**: capability bands for tasks. N is the default and covers everything below very hard, including ordinary hard work. X is very hard. S is super hard. Plans name the route, never a model.
- **model families**: each route maps to a default model per host, set in the [run contract](../skills/astrid-dev-shared/run-contract.md#routing-and-bindings): N is Haiku (Claude) or Luna (Codex), X is Sonnet or Terra, S is Opus or Sol. Exact model IDs are recorded in `run.yaml`.
- **completion reviewer**: the independent role that does the single integrated final review after required scoped checks, at most five rounds.
- **run.yaml**: the per-run file recording model IDs, role bindings, source identity and review counters. Template: [run.yaml](../skills/astrid-dev-shared/templates/run.yaml).
- **Otto / `.otto/`**: the local orchestration tool used for runs. `.otto/` holds local run state and is never committed here.
- **M-GPU**: the earlier generation and GPU merge run. It is stopped; its handoff is summarized in [plans/MANAGER.md](../plans/MANAGER.md), and its retained cards are evidence only.
