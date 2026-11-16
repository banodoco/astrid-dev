# Tasks — Say where a generation goes, in the generate request

[Plan](plan.md) · [Inputs](inputs.md)

**Draft.** Dispatch waits for the owner's scope decision, decisions D1–D9 and the advisor critique ([inputs.md](inputs.md#planning-evidence)). The cards below assume each recommendation; a different decision changes only the named card.

**Checks.** All checks run in the Agent repository on CPU:
- `PYT <selectors>` means `bash scripts/worker-env/agent-pytest.sh -q <selectors>` ([env README](../../env/README.md)).
- Integration-marked files need `PYT -m integration <selectors>`.
- The in-process Runtime comes from the Agent's pinned Runtime, through `agent-setup.sh`.
- The Runtime fixture is `media_realm` (`tests/editing_conformance/test_commit_runtime_parent_media.py:102`), which gives real managed outputs, generations, variants and a timeline.
- A fake executor settles the task. No GPU or RunPod is used.

**Base.**
- G1–G3 start from Plan 32's Agent integration head.
- G4 onwards start from the head with Plan 32 T6 landed.
- Record both SHAs in [inputs.md](inputs.md#source-identities) before each starts.

| Task / outcome | Route | Depends on | Scope | Focused proof | Progress |
| --- | --- | --- | --- | --- | --- |
| [G1](#g1-characterize-today) Characterize today: lineage, promotion and media add, as strict `xfail` or passing cases | N | — | New `tests/sdk/test_generation_destination_today.py` | `PYT -m integration tests/sdk/test_generation_destination_today.py`, with each case's result recorded in the commit body | [ ] |
| [G2](#g2-the-destination-value-and-lineage) The `Destination` value: schema, parser and lineage resolution | N | — | New `astrid/core/generation/destination.py` (`Destination`, `SCHEMA`, `parse`, `resolve_variant`); `astrid/sdk/invocation.py:_resolve_generation_variant`, `_validate_variant_controls` (moved into it); new `tests/core/generation/test_destination.py` | Schema and refusal cases (below) | [ ] |
| [G3](#g3-timeline-checks-before-admission) Timeline checks before admission, read-only | N | — | `astrid/core/generation/destination.py:preflight_timeline` (new function); new `tests/core/generation/test_destination_timeline.py` | Each refusal on the in-process Runtime, with no task row created | [ ] |
| [G4](#g4-apply-the-destination-on-the-one-generate) Apply the destination on the one `generate`, with partial failure | X | G2, G3, Plan 32 T6 | `astrid/sdk/generation.py` (the single `generate` and aliases: `destination=`; `_resolve_invoke_destination` → `_resolve_invoke_project`); `astrid/sdk/invocation.py` (the publication effect from a `Destination`; the top-level `variant_of`/`primary` deleted); `astrid/packs/generation/pack.yaml` (`generation_publication` declarations); `astrid/core/generation/destination.py:land` (new); new `tests/sdk/test_generate_destination.py` | The journey and the partial-failure cases on the in-process Runtime (below) | [ ] |
| [G5](#g5-cli-generate-land-and-the-skill-commands) CLI flags, `generate land`, exit codes and the skill section's commands | N | G4 | `astrid/core/generation/cli.py` (`_parser`, `_controls`, a new `land` subcommand); `astrid/core/generation/delivery.py:deliver_generation` (prints the destination block); `astrid/packs/generation/docs/SKILL.md` ("Append a generation variant", lines 179-215, becomes "Say where the result goes"); `astrid/packs/generation/docs/generate-image.md:142`; `astrid/core/resources/skills/references/SKILL.md:67-68`; one pointer line in `astrid/packs/timeline/docs/SKILL.md`; new `tests/core/generation/test_cli_destination.py` | CLI journey, `land` idempotence and exit codes; every command in the skill section runs as a test node | [ ] |
| [G6](#g6-wording-refusals-partial-failure-help-and-skill) Wording: refusal and partial-failure messages, CLI help and the skill section's voice | T | G5 | The message strings in `astrid/core/generation/destination.py`, the help strings in `astrid/core/generation/cli.py`, and the skill section written in G5. Wording only, no behaviour | The exact before and after of every message and help string, checked against the rules on its card; G2–G5's tests unchanged and green (they assert codes, not prose) | [ ] |
| R Review rounds (at most 2 recommended; the owner's number is pending, and it becomes 3 if D7 adds a Runtime task) | S | all other tasks | read-only | Rounds per the [run contract](../../skills/astrid-dev-shared/run-contract.md): findings become rows `R<round>.<n>` added directly below this one, each with route, scope, dependencies and proof; publishing or closing waits for them | [ ] |

**Critical path:** Plan 32 T6 → G4 → G5 → G6 → R. G1, G2 and G3 run now, in parallel with each other and with Plan 32. G2 and G3 add different functions to the same new file, so they merge G2 first. G2 moves two functions out of `sdk/invocation.py`, and Plan 32 T6 changes a different symbol there (the modality resolution near `:4853`), so they can run in parallel; merge Plan 32 T6 first.

**Estimate:** about 5–6 days. G1 0.5, G2 0.75, G3 0.75, G4 1.5, G5 0.75, G6 0.5, and the review rounds about 0.5–1. A Runtime task under D7 would add about 1–1.5 days.

**Conditional (only if G1 shows a lost output under D7):** D7r, Runtime (X): a `preserve` append re-reads the generation version at settlement, and the last `promote` wins. Scope: `runtime_protocol/store.py:_validate_generation_variant_append_effect` and `_apply_settlement_effect` (the append branch), and their tests. It is planned with the owner's go and the advisor's review, because it changes a cross-repository settlement contract.

## G1 Characterize today

**Outcome:** a recorded baseline, so each later task flips a known case. **Authority:** CPU only; no product change.

The cases, each a test node:
1. **Catalog route:** `generate.image(model=<catalog entry>, variant_of={generation_id, variant_id}, primary="promote")` on the in-process Runtime with a fake executor. The new variant has `source_variant_id` and is the only primary. Expected to pass.
2. **Workflow/target route** (`target="auto"` with a fake attached ComfyUI, as in Plan 33's CPU tests): the same `variant_of`. Record whether it is refused, ignored or applied. The source suggests it is not carried (`astrid/sdk/generation.py:1325-1356`).
3. **Stale version:** admit a `variant_of` task, append another variant to the same generation before settlement, then settle. Record the settlement error and whether the output object and its managed association survive (D7).
4. **Media add:** `TimelineSession.add_media(source={asset, generation_id, variant_id}, on=2.0, duration=5.0, track="V1")` with a fresh generation's variant lands one clip. Expected to pass.
5. **Missing track:** the same call with `track="V9"` creates the track (`media_add.py:121-125`). Recorded, because D3 changes this for destinations only.

**Proof:** `PYT -m integration tests/sdk/test_generation_destination_today.py`. Cases 2 and 3 are strict `xfail` with the observed reason if they fail; the commit body lists every case's result.

## G2 The destination value and lineage

**Outcome:** one typed `Destination` (frozen dataclass plus a JSON Schema `SCHEMA`, version `1`), used by the SDK, the CLI and `land`. **Authority:** CPU only.

1. **Shape:** `{variant_of: str | {generation_id, variant_id}, primary: "preserve" | "promote", timeline: {timeline, track, at: number | "end", for?: number}}`. Every field is optional; unknown keys are refused.
2. **`parse(value)`** validates against `SCHEMA` and returns `Destination`. `primary: "promote"` without `variant_of` is refused.
3. **`resolve_variant(client, project, destination)`:** move `_resolve_generation_variant` and `_validate_variant_controls` here from `sdk/invocation.py:2449-2562`, unchanged except for D9: a bare generation id resolves to its primary variant.
4. **Stable refusal codes:** `unknown_generation`, `unknown_variant`, `other_project`, `promote_needs_variant_of`, `invalid_destination`. G2 writes plain working messages; G6 sets their final wording.

**Proof:** `PYT tests/core/generation/test_destination.py tests/sdk/test_generation_variant_publication.py`. The new nodes:
- `test_schema_rejects_unknown_keys_and_promote_without_variant_of`;
- `test_bare_generation_id_resolves_its_primary_variant`;
- `test_unknown_generation_and_variant_refuse_with_codes`.

`test_generation_variant_publication.py` stays green: its callers still use the old controls until G4 deletes them.

## G3 Timeline checks before admission

**Outcome:** `preflight_timeline(client, project, destination, *, modality, output_count)` reads the timeline once and refuses before any task exists. **Authority:** CPU only.

It reads the current bundle through `TimelineSession.open(...)._bundle(...)` and the `State` view, as `media_add.add_media` does, and writes nothing. It refuses with these codes:
- `unknown_timeline`;
- `unknown_track`, naming the existing tracks (D3);
- `track_kind_mismatch` (audio onto a visual track, or the reverse; reuses the kind rule at `media_add.py:110-116`);
- `inactive_track`;
- `time_out_of_range`: `at` not finite, below 0 or beyond the timeline's current end, naming the end (D4);
- `single_output_required`, when `output_count != 1`.

It returns the resolved `at`, with `"end"` becoming the end of that track, and the default length: 5 s for an image, the output's duration otherwise (D4).

**Proof:** `PYT -m integration tests/core/generation/test_destination_timeline.py`, one node per refusal plus `test_end_resolves_to_track_end` and `test_preflight_writes_nothing` (the timeline head and the outbox are unchanged).

## G4 Apply the destination on the one generate

**Outcome:** `generate(..., destination=...)` and its image, video and audio aliases apply all three parts from one call. **Authority:** CPU only. **Delegate to N helpers:** the caller census for the deleted controls, the mechanical edits and running the checks.

1. **Before admission:** `parse`, `resolve_variant` and `preflight_timeline`. Any refusal returns before a run or task row exists. `wait=False` with a `timeline` part is refused, pointing to `generate land` (D5).
2. **Lineage and promotion:** the publication effect is built from the `Destination`: `generation.variant.append` with `primary_policy`, or `generation.publish_v1`. This happens on the single route Plan 32 T6 leaves, so default slots get it too (G1 case 2 flips). Delete the top-level `variant_of`/`primary` controls (`sdk/invocation.py:4508-4526`) and their `generation_publication` declarations in `pack.yaml`. `git grep -n "variant_of=\|primary=" -- astrid` shows only the destination code.
3. **After settlement:** `land(client, task_id, destination)` reads `generation_variant` or `generation_publish_v1` from the task result (Runtime `store.py:6209-6218`). It then calls `TimelineSession.add_media(source={asset: variant_id, generation_id, variant_id}, on=at, duration=length, track=track, idempotency_key="generate-destination:" + task_id)`. That call is told not to create tracks: one keyword on `media_add._placement_commands`, default unchanged for other callers.
4. **The result block:** `destination: {variant: {generation_id, variant_id, primary}, timeline: {status, clip_id, revision_id, reason, retry}}`.
5. **Partial failure:** the generation is never rolled back. If the commit is refused or conflicts after the session's normal rebase, or its outcome is unknown, then `timeline.status` is `failed`, with the timeline error code as `reason` and the exact `astrid generate land TASK_ID --timeline … --track … --at …` as `retry`. An unknown outcome keeps the outbox flight, so `land` resends the same flight.

**Proof:** `PYT -m integration tests/sdk/test_generate_destination.py tests/sdk/test_generation_variant_publication.py`. The new nodes:
- `test_one_call_makes_a_promoted_variant_and_places_it`: the variant has `source_variant_id` and is the only primary, and the head has one clip at T on X referencing it;
- `test_new_generation_placed_without_lineage`;
- `test_refusals_create_no_task`: one parameter per G2 and G3 code;
- `test_track_deleted_during_run_keeps_generation_and_reports_failed`;
- `test_land_after_failure_places_once_and_twice_is_a_no_op`;
- `test_no_wait_with_timeline_is_refused`.

## G5 CLI, generate land and the skill commands

**Outcome:** the CLI matches the SDK, and the skill shows the one-call form. **Authority:** CPU only.

1. **Flags** on `generate image|video|audio` and `generate workflow`:
   - `--variant-of GEN[:VARIANT]`;
   - `--promote`;
   - `--timeline TL --track ID --at SECONDS|end [--for SECONDS]`;
   - `--destination-json FILE`, exclusive with the flags.
   All of them go through `Destination.parse`.
2. **`astrid generate land TASK_ID --timeline … --track … --at …`** runs only the timeline step, idempotent by task id.
3. **Exit codes:** 0 when everything requested was applied; a distinct code (proposed 4, D6) when the generation is saved but the timeline step failed, printing the saved ids and the retry.
4. **The skill:** rewrite the generation skill's "Append a generation variant" section as "Say where the result goes", with one SDK and one CLI example of each part and the partial-failure retry. Update the two references lines and add one pointer in the timeline skill. Land it after Plan 32 S1.

**Proof:** `PYT -m integration tests/core/generation/test_cli_destination.py`. The new nodes:
- `test_cli_flags_and_json_parse_to_the_same_destination`;
- `test_cli_partial_failure_exit_code_and_retry_line`;
- `test_land_is_idempotent`;
- `test_skill_section_commands_run`, which runs each command in the section on the fake executor.

## G6 Wording: refusals, partial failure, help and skill

**Surface:** every refusal message from G2–G4 (the codes listed there), the partial-failure message and its retry line, the help strings of G5's flags and `land`, and the "Say where the result goes" skill section. **Intent:** a creator or agent reading any one message knows what was wrong and what to type next. Nothing changes behaviour.

**Rules:**
- plain words, and the user's own values quoted back;
- never claim something happened that did not ("saved" only once settlement succeeded);
- always one concrete next step: the valid tracks, the timeline's end, or the exact `land` command;
- one meaning per term: destination, variant, primary, timeline;
- no internal names (effect types, outbox, CAS).

**Proof:**
- a table of every message's exact before and after, checked against the rules, in the PR;
- the owner sees the partial-failure message and the skill section before merge;
- `PYT -m integration tests/core/generation/test_destination.py tests/core/generation/test_destination_timeline.py tests/sdk/test_generate_destination.py tests/core/generation/test_cli_destination.py` is unchanged and green.
