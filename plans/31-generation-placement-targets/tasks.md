# Tasks — One generation placement and target lifecycle

[Plan](plan.md) · [Inputs](inputs.md)

Outline with unknowns; routes and exact selectors are set at dispatch, after the source identities in [inputs.md](inputs.md#source-identities) are recorded. Plan 02 must land first.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| T1 Characterize current routing with the invariant tests | TBD | Plan 02 landed | Plan 02's guard-rail tests, extended to every capability that calls generation | Done when the invariant test (every default slot x {auto, local, runpod}), dry run == live, and no pod unless execution happens on it cover every capability that calls generation, and any current failure is recorded | [ ] |
| T2 Placement producer, propagation, and deleting re-inference | TBD | T1, and an independent review of the Placement and Target lease design | Placement resolution order (request override → project default → user default → built-in) with a `device` field; `GenerationFacade._generate_on_target`; `workflow()`; the `vibecomfy.run` inputs schema (`pack.yaml`); host parsing; `core/generation/preflight.py`; `core/generation/cli.py`; `core/execution/generic_host.py` target_policy binding; `sdk/invocation.py` | Done when a default placement can be set and overridden per generation, Placement is computed once and passed down, no re-inference site remains, one refusal site replaces the sfx/foley duplicates, and the dry run computes the same Placement as the live run | [ ] |
| T3 Target interface and implementations with release-always | TBD | T2 | Target interface with local ComfyUI, attached ComfyUI and RunPod implementations | Done when each kind passes `prepare`, `run` and `release`; sessions are leases with an owner and idle timeout (default beyond the job), reusable when warm; `release` returns the session to its lease on success, failure and cancellation; an expired lease terminates the session; no pod is created unless execution happens on it, and no orphaned session can exist | [ ] |
| T4 h3_av as a Job; remove pack-specific pod commands from the runpod pack | TBD | T3 | h3_av pack actions; runpod pack `remote_placement.py` | Done when h3_av supplies only a Job, honours `--target runpod`, and the runpod pack holds no h3_av-specific pod command | [ ] |
| T5 Live proof: six default slots plus h3_av on RunPod, plus local | TBD | T4, and an authorized start with budget | The same matrix as the invariant test, run for real | Done when every slot and h3_av generates on RunPod and locally, each pod is released, and the results are recorded with the revisions tested | [ ] |
| T6 Completion | TBD | T1-T5 | Astrid-dev completion PR | Done when the completion PR links the implementation PRs, the integrated revision, the T5 evidence, and a disposition for F-003 | [ ] |

Local device selection (which GPU) is carried in Placement from T2; implementing selection across several local GPUs may land in T3 or a follow-up, but the shape must not need to change. Plan 12's shared inference lifecycle consumes these Targets; changes to the Target interface after T3 need Plan 12's owner informed.
