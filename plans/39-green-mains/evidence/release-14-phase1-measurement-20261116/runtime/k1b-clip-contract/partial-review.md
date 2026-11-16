# Independent review of held clip-replacement test port

**Verdict: HOLD. The partial patch is not ready for approval as preservation of all ten legacy invariants, independently of the already-held replay/history contract.** Three source-supported coverage blockers are identified below. Several API/expectation ports are intentional and acceptable; the review does not decide or change the corrupt-history replay contract.

Reviewed Runtime HEAD `2777051c06c3d15e14d3e8d13de26b19f875c4bc`, the uncommitted diff in `tests/test_timeline_clip_replacement.py`, its saved `partial.patch`, the K1b card, paired XML/log evidence, and `../k1b-replay-contract/assessment.md`. The saved patch is byte-identical to current `git diff`, SHA-256 `63e1dbf0f0331dc6bbae0362492a929b8acd95e333092702c8d331f140c71bee`. Only that test file is modified. Relevant pinned Agent source was read at `0e1543e0da2215db9cb3320cfd1083174c3c62a9` under `astrid-runtime.env/agent`.

No tests, collection, product edits, contract changes, commits or remote actions were performed. This review is the sole written artifact. Formal RS1 remains 0/1. Line references below name the current partial working file unless explicitly marked Git HEAD/base.

## Blocking findings

### P2 — R1: atomic preservation wrapper drops populated sibling, effect and registry-metadata coverage

Legacy `test_replace_timeline_clip_is_atomic_cas_and_exactly_replayable` previously used `_composition`: a target containing `effects: [{"id": "grade"}]`, a same-composition `untouched` text sibling, and nonempty registry `metadata: {"keep": True}`. Its assertions explicitly preserved the entire target except asset, the sibling, registry metadata, and the old asset entry.

The wrapper at lines 721–722 delegates to `test_native_clip_swap_is_atomic_cas_and_exactly_replayable`. Its bootstrap at lines 130–164 creates one internal target clip with timing and `opaque`, but no effects, no second clip in that internal composition, and no sentinel registry metadata. The parent media clip is in a different owner scope. `_assert_native_swap_result` at lines 252–277 compares the full internal payload and parent fields, which is valuable, but cannot detect deletion/alteration of an absent effects field, absent same-owner sibling, or absent populated metadata. A regression that preserves this sparse target while dropping those populated values can pass the replacement assertions.

This loses original semantic cases; changing to a current canonical API does not require their removal. Before treating the atomic legacy ID as ported, retain valid current-schema populated counterparts of those fixtures and their exact preservation assertions. If one old field is intentionally unsupported in the modern contract, that requires an explicit source/owner disposition rather than silently substituting the unrelated `opaque` field. The old registry asset binding and target `at/from/to` preservation *are* covered by the current full-payload equality and should remain.

For precision: the legacy fixture also contained config metadata, but the old atomic test did not explicitly assert that config metadata; the concrete lost metadata assertion here is **registry metadata**.

### P2 — R2: delegated negative tests no longer prove the intended refusal category

Four legacy IDs now delegate to older modern helpers whose assertions are materially broader than the removed legacy checks:

- Cross-project wrapper at 725–726 delegates to lines 399–407: `pytest.raises(RuntimeErrorBase)` with no message, code, status or reason. The old test required `NotFoundError` identifying the timeline project. Current Runtime `_selected_project_media` (`runtime_protocol/timeline_commit_port.py:967–988`) filters by project/generation/variant and raises `NotFoundError("selected media is not a managed project generation/variant/object")` when that identity is absent. The fixture does create a foreign project/selection, but a provider-unavailable, retired-route or unrelated protocol failure also satisfies the new assertion with unchanged rows. The blanket base exception cannot establish project-bound selection refusal.
- Wrong-stream wrapper at 746–747 delegates to lines 479–488: base exception plus `media|stream|kind`. It can pass on an unrelated media-selection failure instead of rejecting audio for a video target. The pinned Agent `_swap` explicitly emits `CommandError("media swap preserves media kind", kind="unsupported_media")` (`native_occurrence_media_commands.py:247–257`), and the commit adapter carries semantic failure details. That intended cause is available for an exact assertion.
- Short and authored-end wrappers at 750–755 delegate to lines 493–504: base exception plus `short|duration|window|extent|source`. That accepts unrelated source failures without proving the duration guard. The fixture correctly distinguishes duration 1 from 3.5 against authored `from=1,to=4,hold=3`, but the assertion must distinguish that guard from generic source refusal. The pinned Agent checks `right > value['duration_seconds']` and emits `unsupported_timing` with `source window differs from hold or exceeds media` (`native_occurrence_media_commands.py:191–199`). Its commit error machinery maps base `unsupported_*` failures to validation status/code and preserves reason (`_commit_errors.py:74–122`; `commit.py:1457–1472`).

The exact public exception class may legitimately differ from the retired direct API. The blocker is not a demand to preserve obsolete wording; it is the loss of a precise, source-backed refusal cause. Keep the full no-write/head comparisons, but bind each negative case to its current intended error code/status/reason and suitable exact message. Broad catches in pre-existing modern tests become a new coverage loss when used as the sole replacement for these more specific legacy assertions.

### P2 — R3: restart/intervening-edit wrapper uses an unchanged value and does not pin the retained intervening head

The legacy replay test performed a genuine intervening metadata change before closing/reopening and required timeline version 3 to remain after replay. Its replacement at 762–763 delegates to lines 546–569. The native bootstrap seeds `hold=3` (154–160), and the replacement command requests a media swap, whose unchanged-hold result is checked by the separate atomic test's full-payload assertion. The replay test itself does not establish a different hold before its alleged intervening edit, which sets `hold` to **3 again** (551–555). This exercises a later publication but not replay across an actual changed authored value.

The post-reopen assertion only requires `head_publication_id != first receipt ID` (561). It does not compare against the saved result of the intervening commit or check that a changed value survived. For example, a wrong head that is neither the first swap nor the intended intervening head would satisfy that inequality; aggregate ledger/event counts do not establish which head remains selected.

Use a genuine supported intervening content change, retain its accepted head/document, and verify that exact head and changed value remain after exact replay. This is a test-preservation correction independent of the unresolved old-CAS-corruption contract; it does not choose either side of that contract. The current clean restart replay equality and receipt/event counts remain useful and should be retained.

## Per-legacy-ID disposition

Names below are suffixes of `tests/test_timeline_clip_replacement.py::test_replace_timeline_clip_...`.

| Legacy suffix | Original invariant / current coverage | Disposition |
| --- | --- | --- |
| `is_atomic_cas_and_exactly_replayable` | Accepted replacement, target timing/fields, sibling/effect/metadata/old-binding preservation, receipt/event uniqueness, exact retry, same-key mismatch, stale refusal. Current full payload/receipt/event checks retain much of this, but populated sibling/effect/registry-metadata cases are absent. Corrupt-old-CAS replay fails before subsequent mismatch/stale checks execute. | **HOLD: R1 plus existing owner-contract hold.** Do not count unreachable tail assertions as proved. |
| `rejects_cross_project_source` | Foreign project selection still constructed; full DB dump equality is stronger than the old version-only no-write check. Refusal accepts any Runtime error. | **HOLD: R2.** Foreign selection semantics are preserved in setup, not sufficiently pinned by the assertion. |
| `rejects_malformed_source_without_mutation` | Malformed *bytes*, not merely a malformed selection, are refused by supported `import_media`; exact validation code/status/message and full DB/head equality are checked at 729–739. | **Acceptable intentional port.** The K1b card expressly moves this boundary to import admission. Production decoder refusal is at `service.py:5685–5706`. |
| `rejects_tampered_cas_without_mutation` | Selected new media is corrupted after valid capture; concrete integrity conflict, 409/code and full DB/head preservation asserted at 425–439. | **Acceptable intentional port.** Distinct old/new IDs remove the previous accidental shared-object ambiguity. |
| `rejects_wrong_stream_without_mutation` | A valid imported audio selection is submitted to a video replacement; full DB/head unchanged. | **HOLD: R2's overly broad error assertion.** |
| `rejects_too_short_source_without_mutation` | Duration 1 is still submitted against the authored window; full DB/head unchanged. | **HOLD: R2's overly broad error assertion.** |
| `requires_source_to_reach_authored_end` | Duration 3.5 exceeds the three-second span but does not reach authored end 4, preserving this separate boundary. | **HOLD: R2's overly broad error assertion.** |
| `generic_visual_media_requires_video_stream` | Local canonical clip is changed to `clipType=media`, then Agent capture refuses audio with exact `unsupported_media` kind/message. | **Acceptable under the explicit precommit ruling, with the limitation below.** |
| `replays_after_intervening_edit_and_reopen` | Clean accepted envelope replays after reopening; fixed receipt/event counts are asserted. Intervening operation reassigns the existing hold and head is only checked unequal to first. | **HOLD: R3.** |
| `public_http_route` | Authenticated `WorkspaceClient` uses the supported public commit route; valid media selection, accepted canonical result, concrete receipt identity/hash/event counts and exact replay asserted at 650–716. | **Acceptable intentional route port.** Direct retired-route refusal belongs to unchanged legacy-authority controls. |

## Acceptable changes and explicit limits

The card explicitly authorizes current `merged` status in place of `rebased`, exact verified duration in the new canonical media binding, and distinct old/new encoded content. Those changes are supported by the current contract and fix earlier fixture/expectation mismatches without loosening the successful-result assertion: `_assert_native_swap_result` now demands one exact expected status. Distinct-color media and explicit different object IDs are stronger than the former identical-byte fixture. Exact selected-input corruption errors and no-write checks are likewise improvements.

The generic-media wrapper's Runtime snapshot at 517/524 is **vacuous as Runtime refusal coverage**: the operation between snapshots is pure Agent capture against a locally copied/modified document and never calls Runtime commit. It does, however, exercise the exact precommit refusal the card's ruling 4 explicitly permits. I therefore do not classify this as an unauthorized port or separate blocker. The artifact must describe it as client/precommit coverage; it cannot claim that this case proves a malicious uncaptured generic-media command is refused by Runtime. The exact typed capture refusal itself is substantive, not vacuous.

The malformed-bytes import refusal also intentionally occurs before a replacement command, but unlike the capture-only case it calls the Runtime import admission boundary and checks full database/head state. That is the expressly authorized modern location for malformed-byte rejection and preserves the key invariant.

The media helper's new default image color changes red to blue, but no inspected test relies on the former color and the image pair now differs explicitly. The audio generator ignores color, yet both native editing fixtures call only video/image; no new identical-audio pair is silently asserted as distinct.

## Selection, evidence and outstanding holds

All ten exact legacy function names remain. They have no integration/default-off decorator; calling an integration-marked function as ordinary Python does not attach its pytest marker to the wrapper. `native_editing` has no dynamic integration classification, and `tests/lanes.py` only adds the existing platform skip in its top-level collection hook. The 17 modern selected cases retain their existing integration marks. Registry/workflow/pin files are unchanged. Thus no hidden selection reduction or newly default-off legacy ID was found.

The wrappers do acquire the native fixture's Agent checkout/provider requirements. The default unit workflow already provisions `ASTRID_CHECKOUT`, installs the pinned Agent and ffmpeg on Ubuntu/macOS (`.github/workflows/ci.yml:96–165`), so this is not an identified unscheduled dependency. Ordinary local runs lacking the required checkout will fail rather than skip. The provided proof overrides the default marker expression to execute all 27 cases, so it is not itself an empirical default-selector proof; default eligibility here is established by source inspection.

Independent parsing confirms before XML has 27 cases: 11 passed, 6 failed, 10 skipped/xfail representations; after has the same 27 cases: 25 passed, 2 failed. The two failures are the native atomic test and its legacy wrapper at the same corrupt-history replay assertion. The assessment already documents that conflict; this review neither removes the assertion nor endorses a bypass. The declaration/mirror removal and later guard proofs were intentionally not completed. Retaining the old declaration in this partial state is not a green K1b result.

**Severity: low, non-blocking mechanical issue:** line 733 uses a non-raw regex string with `\(`, producing the recorded `SyntaxWarning`. Correct its string spelling when the held test patch is finalized; it is unrelated to the substantive findings.

The owner should receive both decisions separately: the unresolved product replay/history rule, and the three test-coverage blockers above. Deciding the former alone would not make this partial invariant port ready for publication.
