# One generation placement and target lifecycle

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Dependable creative execution](../../vision/gaps/F-003-creative-execution.md) (primary).

## Outcome and scope

Every generation, from any pack or slot, decides where it runs exactly once and then runs through one target lifecycle. That removes the inconsistent routing found while proving `astrid generate --target runpod` live on 7-8 Nov 2026: voice and music reached the pod but on the default `comfyui` engine, because the pipeline chose the engine without regard to the entry's models (their models are pinned only for `vibecomfy-h3`); h3_av through `generate` never reached the RunPod pod route (only the CLI `--placement runpod` does); and the dry run reported "ready" for both because its readiness check returns nothing without a client.

The design has three pieces, each owned by one layer:

1. **Job**, owned by packs: what to run (workflow, inputs, needs). Packs never choose placement or own pod commands.
2. **Placement**, owned by the generation task pipeline (`GenerationFacade._generate_on_target`, astrid-agent `astrid/sdk/generation.py`): a frozen value `{kind: local|attached|managed|runpod, device or endpoint, policy (budget, consent, lifetime)}`. It is computed once, passed down and never re-inferred. The dry run computes the same Placement.
   - **Default and override:** the user (or project) sets a default placement, for example "local GPU 1", "attached server", or "RunPod 5090 in EUR-NO-1 on storage `storage`". Any single generation can override it. The producer resolves request override → project default → user default → built-in default, in that order and in one place. Choosing *which* local GPU is part of the Placement (`device`), so multi-GPU machines get the same default and override mechanism as remote targets. The first version may ship the default + override for target kinds already supported and build towards device selection; the Placement shape carries `device` from the start.
3. **Target**, one implementation per kind: `prepare(placement)` returns a session, `run(session, job)` returns artifacts, `release(session)` is always called. Local ComfyUI, attached ComfyUI and RunPod implement it.
   - **Sessions are leases, not job-scoped.** A session (for RunPod, a pod) may outlive the job that started it: a warm session can be reused by later jobs, and a session someone spun up explicitly lives until they release it. What it can never do is outlive its lease. Every session has an owner and an idle timeout (a default that extends beyond the job, overridable per Placement policy); when the lease expires with no job running, the Target releases it. "Release" after a job means "return to the lease", not necessarily "terminate". An orphan, meaning a running session with no owner or lease, is a bug by construction.

- **Included:**
  - the Placement producer and its propagation through `workflow()`, the `vibecomfy.run` inputs schema (`pack.yaml`) and host parsing;
  - deleting every re-inference site, with one refusal site;
  - a dry run identical to the live run;
  - a Target interface with local, attached and RunPod implementations;
  - moving pack-specific pod commands out of the runpod pack (h3_av becomes a Job);
  - release-always semantics in the Target;
  - keeping and extending the guard-rail tests that land with [Plan 02](../02-consistent-generation/plan.md): the invariant test over every default slot x {auto, local, runpod}, dry run == live, and no pod unless execution happens on it.
- **Not included:** new providers; new model routes ([Plan 12](../12-multiple-inference-routes/plan.md) owns Wan2GP); splitting `generic_host` into modules ([Plan 13](../13-execution-host-refactor/plan.md)).

## Existing work and decision

The source is the merge run's routing map, `merge-run/review/generation-routing-map.md` in `banodoco/astrid-overnight-2026-11-05`, branch `merge-run/2026-11-07`. It found:

- **Six placement decision points:**
  - `sdk/generation.py` `_generate_on_target`;
  - `core/generation/preflight.py` `_select_generation_target`;
  - `packs/h3_av/actions/transform/run.py` (about lines 2936, 1952 and 1303, a copy of the vibecomfy logic);
  - `packs/vibecomfy/actions/run/run.py` lines 709-758 and about 1083;
  - `core/execution/generic_host.py` lines 12093-12125 (`target_policy` binding);
  - a CLI probe in `core/generation/cli.py` lines 36-40.
- **Two remote mechanisms:** `run.py` chooses the route from the endpoint checkout, while `generic_host` binds `target_policy`.
- **The dry run diverges from the live run in five places,** including a hard-coded h3_av `parent_target: default` (`sdk/invocation.py` about line 4913).
- **Duplicated sfx/foley RunPod refusals** in three places.
- **The RunPod pack's `remote_placement.py` owns an h3_av-specific pod job command.**

About 43 test references are affected. The Placement half alone was estimated at 6-10 hours of engineering. The fix is to decide once and pass the result down, not to patch each site. Details and the choice are in [inputs.md](inputs.md#planning-evidence).

## Sequence and readiness

Plan 02 lands first: its guard-rail tests and targeted routing fix are the starting characterization. Then:

1. Extend the invariant tests to every capability that calls generation (T1).
2. Add the Placement producer, propagate it and delete the re-inference (T2).
3. Add the Target interface and its three implementations with release-always (T3).
4. Make h3_av a Job and remove pack-specific pod commands from the runpod pack (T4).
5. Prove the same matrix live on RunPod and locally (T5), then complete (T6).

Hardware, budget and consent for the live proof are not yet decided; T5 needs an explicit authorized start. See [tasks.md](tasks.md).

## Interfaces and handoff

- **Consumes:** [Plan 02](../02-consistent-generation/plan.md)'s guard-rail tests and targeted routing fix. The exact merged revision is recorded in [inputs.md](inputs.md#source-identities) when Plan 02 lands.
- **Produces:** the frozen Placement value and the Target interface (local, attached, RunPod). [Plan 12](../12-multiple-inference-routes/plan.md)'s shared inference lifecycle consumes these Targets, so this project is its foundation. [Plan 25](../25-cloud-assist-v1/plan.md) (cloud-assisted) would reuse Placement and Target, including the network-volume model cache follow-up.

## Completion

- Every default slot and h3_av, under {auto, local, runpod}, decides placement once; no re-inference site remains and there is one refusal site.
- The dry run equals the live run for the same inputs.
- No pod is created unless execution happens on it. Every session is held by a lease with an owner and an idle timeout, and is released when the lease ends; no orphaned session can exist, while warm and explicitly started sessions may outlive individual jobs.
- A default placement can be set (user or project) and overridden per generation, resolved in one place; the Placement shape includes the local device.
- The runpod pack holds no pack-specific pod command.
- A live proof runs the same matrix (six default slots plus h3_av) on RunPod, plus local.

This proof does not cover new providers, Wan2GP routes or the `generic_host` split. [F-003](../../vision/gaps/F-003-creative-execution.md) does not close automatically on completion.
