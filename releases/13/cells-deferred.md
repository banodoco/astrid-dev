# Release 13 cells: deferred root causes

Rule: a narrow fix names its deeper cause here (or in an astrid-dev issue) at once. Append-only. Not needed for working generation: Plan 39.

| # | Narrow fix (commit) | Deeper cause | Proposed root fix | Owner/plan |
|---|---|---|---|---|
| 1 | `r13/rows-ir-bridge` `3573a5b85`: test setup and three machines-ruled expectation changes | Tests duplicate or mock around the product's owned-preparation path instead of sharing one prepared-engine fixture | One shared prepared-engine fixture used by all production-engine tests | Plan 39 |
| 2 | `r13/rows-packs-census` (54 to 49): pinned executor count | A hard-coded count goes stale at every pack change | Derive the expected set from pack manifests; keep a short allow-list for deliberate changes | Plan 39 |
| 3 | `r13/sfx-default` `29e41fc05`: preexisting `test_audio_preferred_row_owns_its_error[sfx-audio/hunyuan_video_foley]` (explicit-only Foley makes `hunyuan-foley-local` unknown to the dry-run catalog; test expects the preferred-workflow-dependency error) | The test names a specific entry that the explicit-only ruling (8395174a5) removed from defaults: the expectation was not updated with the ruling | Parametrise over the default entry per slot, read from the pack defaults | Plan 39 (test lane) |
| 4 | same: preexisting `test_runpod_preferences_live_under_machines_runpod` (RunPod preferences missing budget_cap_usd after M2) | The test fixture predates M2's claim/generate separation (budgets belong to the claim) | Rewrite the fixture to the claim path | Plan 39 (machines/test lane) |
| 5 | h3 inputs: six-frame duration instead of the five-frame minimum | Rational `5/24` duration fails canonicalization for source-backed modes (spec.py:218, request_v2.py:62-84): normalization emits a float that is rechecked exactly | One duration representation (card `h3dur`) | in flight |
