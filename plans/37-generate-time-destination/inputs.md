# Inputs — Say where a generation goes, in the generate request

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — The owner (Hannah) gave the direction on 9 Nov 2026, paraphrased from speech by the coordinator: reduce creative friction. The caller must be able to say, in the generate request itself, that the result is a variant of an existing generation, that it is promoted to main, and that it goes on the timeline at time T on track X, so no follow-up calls are needed. Proof is CPU tests only, with no GPU or RunPod run. There is no traceable record of that direction yet, and the design choices D1–D9 below are not yet agreed. Next: the owner confirms the end state and D1–D9 in this scope PR, and the PR records that decision with its link.

**Prior art:** Read at Agent `origin/cand/29-r12` = `ff40f2c684fc7ce22e42a5cacda5c63a0c8800a9`, Runtime `744cf24874ea851f95949a706725aba19d18222f` and App `cand/29-r12` = `3274a9c0756f2950929d7881795c3c7e97e74aa2`. Findings are in [Prior art in detail](#prior-art-in-detail). In short:
- lineage and promotion exist on the catalog generation route and settle atomically in the Runtime;
- they are missing from the workflow route that default slots use, and from the CLI;
- the timeline step exists only as a separate `add_media` call;
- an unused completion auto-placement builder exists;
- there is no separate promote call for generations.
Plans 32, 18, 17, 24 and 35 were read for overlap ([Coordination](#coordination-with-other-plans)).

**Approach:** One optional `destination` block on the generate request: `variant_of`, `primary` and `timeline`. It has one typed schema, shared by the SDK and the CLI, and works in three phases:
1. **Check before admission** (read-only, no spend).
2. **Lineage and promotion** are applied by the Runtime's existing settlement effects, in the same transaction as the output landing.
3. **The timeline step** is applied by the Agent right after settlement, through `TimelineSession.add_media`, with an idempotency key from the task id. If it fails, the generation is kept and the result names the reason and the exact `generate land` retry.

It replaces the top-level `variant_of`/`primary` controls in the same change. There is no Runtime and no App change. Alternatives:
- **(a) Do less:** add only CLI flags for the existing `variant_of`/`primary` and document `add_media` as the follow-up. Rejected: it keeps the follow-up call the owner wants gone.
- **(b) A new Runtime settlement effect for the timeline:** rejected for now. Timeline semantics live in the Agent's commit provider, outside the Runtime store's lock, so the timeline step cannot share the settlement transaction without a new cross-repository contract.
- **(c) Durable Runtime post-settlement placement** through the existing producer guard: deferred, as owner decision D2.
- **(d) Reuse `auto_place_completion`:** rejected as the main path. It places by anchor and fallback for shot occurrences, while the owner asked for an explicit time and track. Its 5-second image hold is reused as the default length.

**Challenge:** Pending — The plan changes a user-visible flow (generate to gallery to timeline) and is estimated at about 5–6 days, so the planning skill asks for an advisor critique. It has not happened yet. Next: brief the advisor (Orchestrate, advise path) to build as little as possible and to verify in code:
- that the Agent-side timeline step is right (D2);
- the refusal set and the time range (D3, D4);
- the stale-version risk (D7);
- the dependency on Plan 32 T6.
Record its findings here, with what was accepted or rejected.

**Proof and limits:** CPU only, with the Agent's in-process Runtime fixture (`media_realm` in `tests/editing_conformance/test_commit_runtime_parent_media.py`) and a fake executor. The observable results:
- one SDK call and one CLI command produce a variant with `source_variant_id`, make it primary, and place one clip at T on X, read back from the Runtime;
- every refusal happens before a task row exists;
- an induced timeline failure keeps the generation, reports `timeline.status: failed`, and `generate land` then places exactly one clip, idempotently.
Not proven:
- real inference, GPU or RunPod;
- how the App displays the result;
- placement after a caller crash without `generate land` (D2);
- attached or RunPod placements beyond what Plan 32's CPU fakes cover.

## Why F-003

- **[F-003 Creative execution](../../vision/gaps/F-003-creative-execution.md)** (chosen). Its gap names "artifact identity and usable output", and its closure evidence asks for an editable artifact with correct "project identity … and usable timeline/workspace integration". This plan makes the result land with the right identity (lineage and primary) in the right place on the timeline, from one request. F-003 has no route to closure yet, and [strategy.md](../../strategy.md) defers writing new routes, so the plan has no `Contributes to closure:` line.
- **[AA-001 Sustained creative work](../../vision/gaps/AA-001-sustained-creative-work.md)** benefits: lineage and promotion support repeated revision. Its closure evidence, though, is a real artist-led project, which no implementation plan delivers. So it is not named as the gap closed.
- **[LS-002 Agent workspace control](../../vision/gaps/LS-002-agent-workspace-control.md)** is about placing and binding UI components in the workspace (Plan 24), not where media lands. Rejected.

## Prior art in detail

**Lineage and promotion (Agent).**
- **Validation:**
  - `variant_of={generation_id, variant_id}` and `primary: preserve|promote` are validated in `astrid/sdk/invocation.py:2543-2562` (`_validate_variant_controls`);
  - they are popped from the inputs at `:4508-4526`;
  - they are resolved against the Runtime after the project is known, at `:2449-2540` (`_resolve_generation_variant`, called at `:4663-4670`).
- **The effect:** `:2392-2425` builds `generation.variant.append` with `primary_policy`, and refuses more than one output (`:2408-2412`).
- **Refusals that exist today:**
  - "generation lookup failed" (`:2444`);
  - "generation variant … was not found" (`:2523`);
  - "primary='promote' requires variant_of" (`:2562`);
  - a different-project source (`:2504`).
- **Declarations:** capabilities opt in through `generation_publication` in `astrid/packs/generation/pack.yaml:164-171, 407-414, 1709-1716`.
- **Docs:** the skill documents it at `astrid/packs/generation/docs/SKILL.md:179-215`.
- **Gaps:**
  - the workflow/target route builds its own `generation_intent` with no variant context (`astrid/sdk/generation.py:1325-1356`), so default VibeComfy slots probably cannot take `variant_of` (G1 confirms);
  - the CLI has no flag for either (`astrid/core/generation/cli.py:147-223`).

**Lineage and promotion (Runtime 744cf248).**
- **Effect kinds:** `generation.publish_v1`, `generation.create_with_variant`, `generation.variant.append`, `generation.thumbnail.attach` and `project.update` (`runtime_protocol/store.py:4516-4525`).
- **The append:**
  - inserts the variant with `source_variant_id`;
  - on `promote`, clears every other `is_primary` and sets the new one;
  - returns `variant_id`, `new_primary_variant_id` and `previous_primary_variant_id` (`:5680-5750`).
- **Settlement:** publication and the effect run in one transaction, and the effect's result is written into the task result as `generation_variant` or `generation_publish_v1` (`:6175-6218`). So the Agent can read the new ids after settlement.
- **Risk:** the append checks the generation's version captured at admission (`:5127-5132`, `:5689-5693`). If the generation changes while a long job runs, settlement is refused (D7).
- **No set-primary route for generations:** the only primary route is `set_primary_reference` (`runtime_protocol/service.py:4516`, `server.py:1185`), which is for references.

**Timeline (Agent).**
- **The one call that adds generated media:**
  - `TimelineSession.open` (`astrid/sdk/timeline/sync.py:407`) and `add_media` (`:715-720`, `media_add.py:130-187`);
  - a mapping source `{asset, generation_id, variant_id}` is verified as a catalog selection (`media_add.py:35-37`);
  - the intent is saved in the outbox before the commit, and a repeat with the same idempotency key replays (`:152-185`).
- **What it does with tracks:**
  - it creates a missing track (`media_add.py:121-125`);
  - it refuses a track of the wrong kind or an inactive track (`:110-116`);
  - it checks only `on >= 0` (`:140`).
- **`clip.add` v1 takes no media** (`_clip_commands.py:25`).
- **`auto_place_completion`** places one completed generation by anchor or fallback, with a 5-second hold (`native_auto_placement.py:61, 95-151`). Only tests call it (`tests/editing_conformance/test_commit_runtime_parent_auto_completion.py`, `test_commit_runtime_m1.py:562`).
- **Runtime side:** the timeline commit provider is the Agent's (`runtime_protocol/timeline_commit_provider.py:18`), and provider execution is outside the Runtime store's lock (`timeline_commit_store.py:1-6`). The producer guard (`timeline_commit_producer.py:76-93`, `200-285`) commits a settled task's proposal, but only on the requester's own later request (`astrid/packs/rendering/shared/runtime_stitch.py:97-140`).

**CLI and delivery.** `deliver_generation` already reports a partial outcome as "Generation completed, but local output delivery failed" with code `output_delivery_failed` (`astrid/core/generation/delivery.py:62-68`). The timeline failure follows the same pattern.

**App (3274a9c0).**
- "Make primary" throws `bridgeCapabilityUnavailable` (`src/shared/hooks/variants/useVariants.ts:194-202`).
- "Add to timeline" is a separate gallery action (`src/features/gallery/components/GenerationsPane/GenerationsPane.tsx:98-101`).
- `getGenerationId` (`src/shared/lib/media/mediaTypeHelpers.ts:26-34`) and the App CLAUDE.md rule (generations are gallery items, variants are per-generation alternates, `based_on` for lineage) match this design: the result names the generation and its variant separately, and the Runtime's `source_variant_id` is the lineage.

**Negative findings.** None of these exists in any of the three repositories:
- a generate-time timeline field;
- `based_on` in the Agent's generation code;
- a CLI `--variant-of` flag.

## Coordination with other plans

| Plan | Overlap | Handling |
|---|---|---|
| [32](../32-generation-placement-targets/plan.md) | "Placement" means where a job runs; its T6 rewrites `generate` in `sdk/generation.py` and `sdk/invocation.py` and edits `delivery.py`; S1 rewrites the generation skill | This concept is named `destination`. G4 waits for Plan 32 T6. G2 and G3 are new functions that run in parallel. The skill section lands after S1 |
| [18](../18-timeline-editing/plan.md) | Timeline primitives | Only the existing `add_media` is used; no new primitive |
| [17](../17-vibecomfy-extensibility/plan.md) | "Variant" means a workflow variant chosen by intent | The destination says `variant_of` for generation variants only, and the docs say so |
| [24](../24-liquid-workspace/plan.md) | Place, attach and bind UI components | Different subject (layout, not media); nothing shared |
| [35](../35-one-home-for-user-state/plan.md) | Saved preferences | No saved default destination here. A later one is a Runtime user or project document under Plan 35 |

## Owner decisions needed

| # | Decision | Recommendation |
|---|---|---|
| D1 | Name of the block | `destination`, with `variant_of`, `primary` and `timeline` inside. Not "placement" (Plan 32 and timeline `placement.create`) and not "target" (`--target`). Rename the internal `_resolve_invoke_destination` to `_resolve_invoke_project` |
| D2 | Where the timeline step runs | In the Agent's `generate` call, after settlement, idempotent per task, with `generate land TASK_ID` as the retry. A Runtime-durable step (through the producer guard) needs a new cross-repository contract; defer it until a caller that does not wait needs it |
| D3 | An unknown track | Refuse, naming the existing tracks. Today's `add_media` creates a missing track; a typo should not make a stray track |
| D4 | The time range | Accept a finite `at` with 0 ≤ `at` ≤ the timeline's current end, plus `at: "end"` (the end of that track). Refuse anything beyond the end, naming the end, so seconds-versus-milliseconds mistakes are caught. The length defaults to 5 s for an image (`COMPLETION_SECONDS`) and to the output's duration for video and audio; `for` overrides it |
| D5 | `--no-wait` with a timeline destination | Refuse, and point to `generate land`. Lineage and promotion still work without waiting, because the Runtime applies them |
| D6 | How partial failure is reported | The generation result stays `ok`; `destination.timeline.status` is `failed`, with the reason and the exact retry. The CLI exits with a distinct non-zero code (proposed 4) and prints the saved generation and variant ids |
| D7 | The generation changes while a long job runs | G1 characterizes what happens to the output. If the output is lost, add a Runtime task: re-read the version at settlement for `preserve`, and let the last promote win. That makes the plan cross-repository, with 3 review rounds |
| D8 | Place in [strategy.md](../../strategy.md) | F-003 is under "Not now". Recommend a `Next` row on F-003 after Plan 32 T6. This PR does not change strategy.md until the owner decides |
| D9 | `variant_of` given as a bare generation id | Accept it: it means that generation's primary variant. The `{generation_id, variant_id}` form stays |

Agreed review rounds: pending. The recommendation is **2** (an ordinary Agent-only project with a user-visible flow); **3** if D7 adds the Runtime task.

## Source identities

| Repository | Ref | SHA | Role |
|---|---|---|---|
| astrid-agent | `origin/cand/29-r12` | `ff40f2c684fc7ce22e42a5cacda5c63a0c8800a9` | Read for this plan; not the build base |
| astrid-agent | `origin/main` | `a105de3a4852cb61b9647dfe2c920118bd29f272` | Same `variant_of` code (`sdk/invocation.py:2453`) |
| astrid-runtime | — | `744cf24874ea851f95949a706725aba19d18222f` | Read only; unchanged by the recommended scope |
| astrid-app | `cand/29-r12` | `3274a9c0756f2950929d7881795c3c7e97e74aa2` | Read only; unchanged |

Before G1: record the Agent base. That is Plan 32's integration head for G1–G3, and the head with Plan 32 T6 landed for G4 onwards.

## References

The owner's direction of 9 Nov 2026 reached this planner through the coordinator; there is no written source yet (see Scope decision).
