# Say where a generation goes, in the generate request

**Project:** Say where a generation goes, in the generate request

**Goal:** One optional `destination` on the generate request (SDK and CLI) makes the result a variant of an existing generation, promotes it to main, and places it on the timeline at a given time and track, with no follow-up calls; refusals come before any work, and a failed timeline step keeps the generation and names the exact retry.

**Status:** paused

**Owner:** Unassigned

**Estimate:** about 5–6

**Waiting on:** the owner's go to queue it (ready, held by the owner on 9 Nov); scope agreement; owner decisions D1–D9; advisor critique; Plan 32 T6 (G1–G3 can start now)

**Start:** [Astrid contributor skill](../../skills/astrid-dev/SKILL.md) and [domain map](../../skills/astrid-dev/references/domains.md). Project owner, priority, status and estimate live **only** in the [catalog](../../plans/index.md).

**Vision gaps:** [Creative execution](../../vision/gaps/F-003-creative-execution.md) (primary). Why F-003 and not AA-001 or LS-002 is in [inputs.md](inputs.md#planning-evidence).

**Draft; not ready for execution.** Owner direction on 9 Nov 2026; the scope decision and the advisor critique are pending (see [inputs.md](inputs.md#planning-evidence)).

## Outcome and scope

A person or agent says, in the generate request itself, where the result goes. No follow-up calls are needed:

- **as a variant of an existing generation** (lineage: the new variant records its source variant);
- **promoted to main:** it becomes that generation's primary variant;
- **on the timeline:** a clip at time T on track X of timeline Y.

These are three parts of one optional `destination` block on the generate request. It is checked before any work starts, so a typo costs nothing, and it is applied once the outputs land.

```python
astrid.generate.image(
    entry="flux-dev", prompt="warmer light", image_ref="./shot.png",
    destination={
        "variant_of": "gen-123",           # or {"generation_id": ..., "variant_id": ...}
        "primary": "promote",              # default "preserve"
        "timeline": {"timeline": "main", "track": "V1", "at": 12.5},   # "for": seconds, optional
    },
)
```

```text
astrid generate image "warmer light" --edit shot.png \
  --variant-of gen-123 --promote --timeline main --track V1 --at 12.5
```

- **Included:**
  - one typed `Destination` value (schema plus parser) shared by the SDK and the CLI;
  - its read-only checks before admission;
  - lineage and promotion through the Runtime's existing settlement effects;
  - the timeline step through the timeline pack's existing media add;
  - one result block that says what was applied;
  - a `generate land` command that retries only the timeline step;
  - the generation skill section and the CLI help.
- **Deleted in the same change:** the top-level `variant_of=` and `primary=` generation controls, which `destination` replaces. They are the only part that already exists.
- **Not included:**
  - App changes: the App's own "Make primary" stays unavailable (`useVariants.ts:194-202` at App `3274a9c0`);
  - a saved default destination: if wanted later, it is a user or project document under [Plan 35](../35-one-home-for-user-state/plan.md);
  - new timeline primitives ([Plan 18](../18-timeline-editing/plan.md));
  - workspace layout ([Plan 24](../24-liquid-workspace/plan.md));
  - a Runtime-side timeline step (owner decision D2).

**Naming.** "Placement" already means where the job runs ([Plan 32](../32-generation-placement-targets/plan.md)), and the timeline code uses it for clip placement (`placement.create`). "Target" means the run target (`--target`). So this concept is called **destination**, and nothing else is. The internal `_resolve_invoke_destination` (`astrid/sdk/generation.py:513`), which picks the output folder and project, is renamed `_resolve_invoke_project` in the task that adds `destination`. "Variant" here always means a generation variant, not a [Plan 17](../17-vibecomfy-extensibility/plan.md) workflow variant.

## Existing work and decision

What already exists, with file:line evidence, is in [inputs.md](inputs.md#planning-evidence). In brief:

- **Lineage and promotion are half done.** `variant_of` and `primary="promote"` exist on the catalog generation route (`astrid/sdk/invocation.py:2449-2562`). The Runtime applies them in the same transaction as the output landing (`runtime_protocol/store.py:5680-5750`, `6175-6218`). They are missing on the workflow route that default slots use (`astrid/sdk/generation.py:1325-1356`), and from the CLI.
- **The timeline step exists as a separate call.** `TimelineSession.add_media` (`astrid/sdk/timeline/sync.py:715`) accepts a generation variant selection and retries exactly through its outbox (`media_add.py:130-187`).
- **There is no separate promote call for generations:** only `references.set_primary`, which is for reusable references.

**Decision:**
- Lineage and promotion stay Runtime settlement effects. They are atomic with the output landing, so they never partly fail.
- The timeline step runs in the Agent, in the same `generate` call, right after settlement. It is idempotent per task.
- The timeline step cannot share the settlement transaction. Timeline commits go through the Agent's commit provider, outside the Runtime store's lock (`runtime_protocol/timeline_commit_store.py:1-6`, `timeline_commit_provider.py:18`).
- **No Runtime or App change** in the recommended scope.

## Sequence and readiness

1. G1 characterizes today's behaviour.
2. G2 (the value and lineage) and G3 (the timeline checks) run in parallel with each other and with Plan 32.
3. G4 applies the destination on the one `generate`. It waits for Plan 32 T6, which rewrites the same facade and invocation symbols.
4. G5: the CLI, `generate land` and the skill commands.
5. G6: the wording.
6. The review rounds.

**Critical path:** Plan 32 T6 → G4 → G5 → G6 → R. All proof is on CPU, with an in-process Runtime. See [tasks.md](tasks.md). Recording this plan authorizes no implementation.

## Interfaces and handoff

- **Consumes:**
  - Plan 32 T6's single `generate(entry, inputs, placement)` (its landed Agent revision, recorded in [inputs.md](inputs.md#source-identities) before G4);
  - the Runtime's `generation.publish_v1` and `generation.variant.append` effects, unchanged at Runtime `744cf248`;
  - the timeline media add.
- **Produces:**
  - the `Destination` schema (a typed contract, versioned `1`);
  - the `destination` result block: `{variant: {generation_id, variant_id, primary}, timeline: {status: placed|failed|not_requested, clip_id, revision_id, reason, retry}}`;
  - `astrid generate land TASK_ID`.
- **Coordination:**
  - Plan 32 S1 rewrites the same generation skill, so this plan's skill section lands after S1;
  - Plan 32 T6 also edits `astrid/core/generation/delivery.py`; G5's CLI delivery change merges after it.

## Completion

- One SDK call and one CLI command, on the in-process Runtime with a fake executor:
  - produce a variant of an existing generation;
  - make it primary;
  - place it on the timeline at the given time and track.
- Reading back:
  - the generation lists the new variant with `source_variant_id` and `is_primary`;
  - the timeline head has the clip at T on X, referencing that variant.
- **Refusals, before any task is admitted** (no run or task row created): unknown generation, unknown variant, unknown timeline, unknown track, a track of the wrong kind, a time out of range, `promote` without `variant_of`, and a timeline destination on a request with several outputs.
- **Partial failure:** the timeline head moves so the clip cannot land, or the track is deleted during the run. The generation and its variant are kept. The result says `timeline.status: failed`, with the reason and the exact `generate land` command, and that command then places the clip once. Running it twice adds no second clip.
- `git grep` finds no top-level `variant_of=` or `primary=` generation control left in `astrid/`.
- **Limits:**
  - CPU only: no real inference, GPU or RunPod;
  - the App's display of the result is not proven here;
  - if the caller dies between settlement and the timeline step, the clip is placed only by `generate land` (D2);
  - [F-003](../../vision/gaps/F-003-creative-execution.md) does not close automatically.
