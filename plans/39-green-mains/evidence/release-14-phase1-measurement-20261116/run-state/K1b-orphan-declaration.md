# K1b — remove an orphan declaration for an already deleted test

Manager `/root`; follow-ups are part of the brief. Route N (`gpt-6-luna`, high), local additive commits only, no remote writes, never ask user questions.

Runtime repo `/workspace/scratch/cd53b069f320/p39-repair/astrid-runtime`, exact base `a05d360c50b35c6803d710909c87b51daf5e84b2`, tree `0291fadcde521650fdc71257a9ec2fd61b7226a4`, identical to merged plan head `359e2d7e55369562ca9513557282ea8aff7645bc`. Start `p39/k1b-orphan-declaration`. Do not publish while the new plan-head CI/Nightly is in flight.

Read evidence `p39-g2-evidence/runtime/k1b-inventory.md` group3 and primary commit `925a7dd1c648a7632ba5b44a53566329ad947564`: it already removed the retired-only combined shot/reference journey while retaining the live project-reference idempotency test and refusal controls. Confirm no current test body exists for `tests/test_runtime_exact_idempotency.py::test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting`.

Allowed source: remove only `runtime-exact-idempotency` from `tests/lanes.py` and the exact mirrored declaration in `tests/test_skip_guard.py`. Do not delete/skip a test, alter a guard implementation/cap, add or fabricate metadata, or touch any other declaration. The immutable semantic pin continues validating every remaining declaration. Preserve the live project-reference test's restart replay, changed-payload409, overwrite409 and stored-value assertions; no edits to that file.

Exact focused before/after proof:

```sh
bash scripts/worker-env/runtime-pytest.sh -q tests/test_skip_guard.py::test_xfail_declarations_are_immutable_and_semantic tests/test_skip_guard.py::test_xfail_reasons_carry_no_session_path tests/test_skip_guard.py::test_the_pin_catches_a_repointed_or_widened_xfail tests/test_runtime_exact_idempotency.py::test_project_reference_creation_is_keyed_durable_and_non_overwriting
```

If baseline fails, stop and report rather than change test expectations outside scope. The real K1b inventory remains invalid (expected20to19 exact IDs,9remaininggroups still missing metadata); do not claim the guard/file passes or raise the cap. No full suite or full skip-registry run is needed for this isolated removal. Record exact counts statically, live test/contract preservation, complete raw logs/exits, patch and commit/tree under `p39-g2-evidence/runtime/k1b-orphan-declaration/`. Independent review before any publication; formal RS1 stays0/1.
