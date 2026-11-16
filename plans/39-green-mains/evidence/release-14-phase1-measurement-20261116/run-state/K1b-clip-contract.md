# K1b — clip replacement contract and quarantine repair

Manager /root; follow-ups are part of this brief. Route X (gpt-6.1-terra high), using completed N research and X diagnosis. Never AskUserQuestion. Local additive commits only; no remote action. Sole Runtime writer. Repository /workspace/scratch/cd53b069f320/p39-repair/astrid-runtime at 2777051c06c3d15e14d3e8d13de26b19f875c4bc, tree2749ee50447b2082b198cf561c895796a6d09444; branch p39/k1b-clip-contract.

Outcome: retain and execute all ten legacy clip-replacement invariant tests through supported current APIs, remove their obsolete strict-xfail declaration only after their positive/refusal/replay invariants pass, and repair six known stale expectations in existing modern counterparts. This is a K1b acceptance prerequisite allowed by the readiness ruling, not formal phase2 completion. All other quarantine metadata and Plan38/55 holds remain.

Read evidence:
- runtime/k1b-clip-port-assessment.md (corrected current17-case results)
- runtime/k1b-clip-diagnosis/diagnosis.md and actual hosted XML/full log
- Runtime commits c6a4167, cd6e9c7, 1f75756,3021a5b,739228c; pinned Agent0e1543 command binding and error contracts. Do not trigger broad git history walks/lazy fetch. Available local source or GitHub read connector is enough.

Allowed product paths:
- tests/test_timeline_clip_replacement.py
- tests/lanes.py (only timeline-clip-replacement declaration after proof)
- tests/test_skip_guard.py (only exact mirror of that removed declaration)
No product implementation, pins, workflow, provider readiness bypass, other registry/cap or other test changes. Do not delete or skip any live test. Preserve ten existing node IDs and default unit eligibility: adding integration/default-off marks to old tests is forbidden. Existing modern integration marks stay intact.

Specific manager rulings:
1. Whole expected canonical payload equality stays. Include exact verified duration in new media binding as current intentional command contract requires; keep every unrelated field/receipt/event/idempotency check.
2. Modern moved-head commit status is merged. Prefer explicit expected_status on shared result helper rather than a loose union of accepted statuses; retain rebased_onto and all concurrent edits.
3. Fix test-media ambiguity: old and selected new media currently encode identical bytes and share one CAS object. Generate distinct valid media content (same requested kind/duration, e.g. explicit different colors), assert their CAS identities differ, and keep tampered-selected-source rejection exact. Do not merely permit arbitrary unavailable errors to make that test pass. Add a separate bounded old-history-corruption control only if needed to retain the observed intentional outcome-unknown boundary; assert exact code/status and no mutation, not any exception.
4. Selected-input CAS corruption must retain concrete integrity refusal (actual CAS object failed hash verification), same failure type/status and complete no-write checks. Generic visual audio must retain exact unsupported_media kind/message, precommit refusal and existing positive image support.
5. Port all ten old invariant tests onto canonical project/occurrence media/commit fixtures, preserving atomicity, cross-project refusal, malformed BYTES refusal at import admission, CAS tamper, wrong stream, short/end-short duration, visual audio rejection, restart/intervening-edit replay, public authenticated commit route. The old malformed-pin modern test is not a substitute for malformed-byte admission. Keep intentional legacy writer 410/no-write controls unmodified.
6. If a previously unexecuted assertion now exposes a real product bug or an untraced contract difference, stop that repair and report a cause card. Never weaken it or change product code under this test-only card.

Exact proofs (one pre and one post, no broad suites):
A. PYTEST_ADDOPTS=-rA bash scripts/worker-env/runtime-pytest.sh -q -m "not darwin_native and not live" --junitxml=/workspace/scratch/cd53b069f320/p39-g2-evidence/runtime/k1b-clip-contract/before.xml tests/test_timeline_clip_replacement.py
   Post identical except after.xml. This deliberately executes this single file's existing17 integration cases and10 default cases together; production lane selection is unchanged. Expect initial known red/xfail, record rather than pretend pass.
B. PYTEST_ADDOPTS=-rA bash scripts/worker-env/runtime-pytest.sh -q tests/test_timeline_legacy_authority.py -k replace_timeline_clip
   Before/after retained retired-route refusal controls. The original -m integration selector selected zero because these exact tests have no integration mark; root verified module/fixtures/central lane source and removed only that erroneous local proof filter. This changes no test marker or CI selection. Preserve the first exit5/80deselected evidence, and do not repeat proofA. If corrected selector selects zero, stop and report rather than expand arbitrarily.
C. bash scripts/worker-env/runtime-pytest.sh -q tests/test_skip_guard.py::test_xfail_declarations_are_immutable_and_semantic tests/test_skip_guard.py::test_xfail_reasons_carry_no_session_path tests/test_skip_guard.py::test_the_pin_catches_a_repointed_or_widened_xfail
   After declaration/mirror removal (existing base passing guard proof already retained by orphan card).

No package/environment changes. Preserve installed R12 Agent provenance and source checkout qualification. Save raw stdout/stderr/exits, per-ID XML comparison, invariant mapping, exact patch and commit/tree only under /workspace/scratch/cd53b069f320/p39-g2-evidence/runtime/k1b-clip-contract/. Do not claim nine remaining exact quarantine IDs have valid metadata; overall K1b stays blocked until they do. Independent review before publication; formal RS1 stays0/1.
