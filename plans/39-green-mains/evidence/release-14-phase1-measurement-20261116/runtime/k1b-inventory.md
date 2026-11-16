# K1b quarantine inventory (read-only)

**Candidate:** `ac9e6d2e7f6a0a6961d7a2d924040f61832925d1`, tree `3fff009d7cb8c46a1a1df21f3f541596b98480bd`. The exact quarantine list is in [tests/lanes.py](https://github.com/banodoco/astrid-runtime/blob/afbd1c93922e581ad4fadd48e6fd162388666601/tests/lanes.py#L133). Its ten groups contain **20 exact node IDs** against a limit of ten; all ten groups omit issue URL, owner, and expiry. The central exact node declaration table arrived in [afbd1c9](https://github.com/banodoco/astrid-runtime/commit/afbd1c93922e581ad4fadd48e6fd162388666601). This review did not poll CI after the saved queued snapshot, did not run tests, and changed no source or remote state.

The user request named four classifications. I used **(a)** for a candidate still-valid product behavior gap, **(b)** for an old API test to port or a stale declaration, **(c)** for a missing cross-repo capability dependency (none of these is a history-fetch failure), and **(d)** for exact behavior owned by Plan 38.

## Group-by-group trace

### 1. runtime-domains-publication — 1 ID — (b)

`tests/test_runtime_domains.py::test_generated_python_client_timeline_publication_is_retired_pending_commit_replacement`

Current body: [lines 272–290](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_runtime_domains.py#L272-L290). It creates a timeline, expects a legacy PATCH to be accepted and advance its version, then expects a stale version to return 409. The wrapper recognizes only the exact legacy 410 retired-route contract. [42ff8ff](https://github.com/banodoco/astrid-runtime/commit/42ff8ff13e2f9a80e36bb25592e15476ace9e121) narrowed that sentinel and added refusal controls. **Follow-up:** RT4 should keep exact 410 assertion(s) and port publication, replay and stale-version behavior to the retained commit API.

### 2. runtime-domains-update — 1 ID — (b)

`tests/test_runtime_domains.py::test_generated_direct_timeline_shot_reference_writers_remain_retired`

Current body: [lines 564–600](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_runtime_domains.py#L564-L600). The first legacy timeline update raises the strict xfail; subsequent body assertions are unreachable, but specify history/diff, archive/recover and direct shot/reference mutation behavior. [59d88ac](https://github.com/banodoco/astrid-runtime/commit/59d88ac4e109256451de73f91ae1ffd95b75f6eb) categorized legacy direct writers; [42ff8ff](https://github.com/banodoco/astrid-runtime/commit/42ff8ff13e2f9a80e36bb25592e15476ace9e121) added exact retirement sentinel/refusal controls. **Follow-up:** RT4 should separate explicit no-write 410 assertions from positive replacement-path assertions and preserve 409/refusal semantics.

### 3. runtime-exact-idempotency — 1 ID — (b, stale declaration)

`tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`

There is **no current test body** at that node ID. [59d88ac](https://github.com/banodoco/astrid-runtime/commit/59d88ac4e109256451de73f91ae1ffd95b75f6eb) added the combined shot/reference test as a strict xfail. [925a7dd](https://github.com/banodoco/astrid-runtime/commit/925a7dd1c648a7632ba5b44a53566329ad947564) deleted that retired-only journey, explicitly retaining the live project-reference test and existing refusal controls. Current file still has `test_project_reference_creation_is_keyed_durable_and_non_overwriting` with restart replay, changed-payload 409, overwrite 409 and stored-value assertions. **Follow-up:** remove only this orphan declaration and mirrored `tests/test_skip_guard.py` pin after review; preserve the live control tests.

### 4. second-client-core — 1 ID — (b)

`tests/test_second_client_e2e.py::test_second_client_core_journey_is_executable`

Current body: [lines 61–87](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_second_client_e2e.py#L61-L87). It builds/runs an independent TypeScript actor with explicit credentials and checks ordered journey steps and project/object/task IDs. [59d88ac](https://github.com/banodoco/astrid-runtime/commit/59d88ac4e109256451de73f91ae1ffd95b75f6eb) notes the actor’s shot creation and old composition publication receive 410. **Follow-up:** port actor writes/publication to the current commit API while retaining explicit credentials, ordered steps and typed legacy-refusal controls.

### 5. snapshot-legacy-certification — 2 IDs — (c, dependency gap)

`tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[genuine-ref]`

`tests/test_snapshot_legacy_certification.py::test_already_admitted_capture_after_upgrade[genuine-inline]`

Both parameterizations share [lines 78–90](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_snapshot_legacy_certification.py#L78-L90). They use historical Runtime `4bb1d0f` and Agent `321cef4` source snapshots, admit then reopen a legacy capture, and distinguish genuine captures from fields that must remain uncertified. The genuine cases raise `LegacyGenuineUncertified` if `canonical_source` is absent. [5a78d1e](https://github.com/banodoco/astrid-runtime/commit/5a78d1ea7a47a5aeda206fcebdd1a4e385e079b1) added the current refusal behavior; [3b3ac10](https://github.com/banodoco/astrid-runtime/commit/3b3ac10f54b887303d01c3932ed582f7a6c65083) added the ledger note without changing bodies. **Follow-up:** coordinate Runtime claim-time recertification with Agent `project_capture`; keep uncertified/forged capture refusal assertions. This is a missing cross-repo capability, not a demonstrated archive-fetch failure and not exact Plan 38/55 ownership.

### 6. stage1-runtime-contract — 1 ID — (b)

`tests/test_stage1_runtime_contract_completion.py::test_timeline_update_archive_recover_replay_the_same_committed_receipt`

Current body: [lines 57–70](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_stage1_runtime_contract_completion.py#L57-L70). It calls legacy `update_timeline`, expecting a durable event receipt, exact same-key replay, archive, and recover. [c6a4167](https://github.com/banodoco/astrid-runtime/commit/c6a4167247ff276fe72fb3c83dd1e2b7d186732e) split this retired writer tail into an individual strict xfail. **Follow-up:** RT4 should test receipt replay and archive/recover through the retained commit API while explicitly retaining the legacy endpoint’s refusal contract.

### 7. timeline-clip-replacement — 10 IDs — (b)

- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_rejects_cross_project_source`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_rejects_malformed_source_without_mutation`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_rejects_tampered_cas_without_mutation`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_rejects_wrong_stream_without_mutation`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_rejects_too_short_source_without_mutation`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_requires_source_to_reach_authored_end`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_generic_visual_media_requires_video_stream`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_replays_after_intervening_edit_and_reopen`
- `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_public_http_route`

Current bodies: [lines 749–918](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_timeline_clip_replacement.py#L749-L918). They check atomic CAS/idempotency/replay; cross-project, malformed input, tampered CAS, wrong stream, too-short source and authored-end refusals; unchanged state on refusal; replay after intervening edit/reopen; and the public HTTP path. [c6a4167](https://github.com/banodoco/astrid-runtime/commit/c6a4167247ff276fe72fb3c83dd1e2b7d186732e) says all ten direct `replace_timeline_clip` tests were strict-xfailed because D04/RT02 retired direct replacement and no commit-path replacement existed then. Later commits strengthened various test contracts.

**Minimum-cardinality cap reduction:** one RT4 card for these ten exact IDs alone could reduce the inventory from 20 to 10. This is a lower-bound proposal, not proof that the card is feasible: the old endpoint is retired and this trace did not establish a one-to-one mapping for every case in the retained commit API. A port must preserve each error distinction, replay assertion and no-write guarantee. If a replacement invariant is absent, record a product-contract bug; do not replace the tests with only 410 assertions.

### 8. timeline-public-s2-historical-audio — 1 ID — (a, candidate capability gap)

`tests/test_timeline_public_s2_mixed_cli_journey.py::test_public_cli_stale_trim_rebases_label_lost_ack_restart_retry_and_undo[historical-audio]`

Current body: [lines 238–476](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_timeline_public_s2_mixed_cli_journey.py#L238-L476). It covers public CLI trim, concurrent SDK label, stale rebase, lost acknowledgement/no duplicate POST, restart retry and undo. The historical audio variant refuses before POST with `clip.trim applies to media clips`; the xfail catches the named `HistoricalAudioCaptureGap`. [4ea982d](https://github.com/banodoco/astrid-runtime/commit/4ea982d215e172c6fe9c47c4240c665f9959cecd) adds the integration journey; [2ccaf31](https://github.com/banodoco/astrid-runtime/commit/2ccaf3199a62efd0b10f12429ee96902a1ae93b9) makes the held behavior explicit. **Follow-up:** Agent-side capture of the original audio film before POST, with all the journey’s replay and refusal assertions retained. This matches stated intent but is not proven a regression against a linked released contract; no owner issue was found.

### 9. installed-pair-source-closure — 1 ID — (d)

`tests/test_installed_pack_custody_spawn.py::test_real_custody_spawn_launches_granted_installed_pack_and_refuses_ungranted`

Current body: [lines 128–256](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_installed_pack_custody_spawn.py#L128-L256). It verifies granted installed-pack execution and refusal of a forged ungranted capability. The xfail specializes only the installed-pair source-closure mismatch. [49a062c](https://github.com/banodoco/astrid-runtime/commit/49a062c7754038f83f9554004531dfa7ed4d15ad) introduced the exact xfail; [2ccaf31](https://github.com/banodoco/astrid-runtime/commit/2ccaf3199a62efd0b10f12429ee96902a1ae93b9) expands its reason and cites Plan 38.

**Plan 38 exact match:** this node is expressly listed in Plan 38’s test inventory; closure parity is assigned to P2r/A3 and the custody spawn acceptance to E1. Its behavior is **WAITING for Plan 38**. Plan 38’s general owner is unassigned, and this supplies no issue URL, owner or expiry. Keep the Plan 39 K1b metadata-only obligation separate; do not guess metadata or treat Plan 38’s ownership as proof the test passes.

### 10. p1-top-level-text-hook — 1 ID — (a, candidate product behavior gap)

`tests/test_timeline_visual_fields.py::test_supported_top_level_type_on_retains_original_roundtrip_expectations`

Current body: [lines 84–98](https://github.com/banodoco/astrid-runtime/blob/ac9e6d2e7f6a0a6961d7a2d924040f61832925d1/tests/test_timeline_visual_fields.py#L84-L98). It commits top-level type `on` and asserts exact stored data, `clip_fields.read` round-trip, and `clip_fields.describe` text. [09a106f](https://github.com/banodoco/astrid-runtime/commit/09a106f0a8b9050e151939ba55cd4aaaba481130) explicitly preserves these original acceptance checks and says P1 must restore the top-level text hook. **Follow-up:** RT6 product fix at the field normalization/read path; retain all three assertions.

## Ownership and issue/metadata finding

- **Plan 38:** exactly one node above, the installed-pair custody spawn, is explicitly inventoried and is WAITING.
- **Plan 55:** its tasks file names only “Runtime tests for task lifecycle and publication” without exact paths or node IDs. None of these 20 IDs can be proven Plan 55-owned from that generic line; do not mark WAITING by name resemblance. Several groups touch timeline publication, but that is not an exact test inventory mapping.
- GitHub issue searches in Runtime and astrid-dev for RT02 timeline commit, historical audio, clip replacement, text hook, `project_capture`, and Plan 38 closure returned no matching issue records. This is limited search evidence, not proof an issue is absent elsewhere. No issue/owner/expiry was inferred.

After the proposed ten-ID RT4 port, ten exact IDs remain. **Numerical compliance alone would not make K1b pass:** every remaining quarantine entry still needs issue URL, owner, expiry, strictness, current exact node ID, and a count at or below ten. The test behavior for Plan 38 and the K1b metadata requirement are separate.

