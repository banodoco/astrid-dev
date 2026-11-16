# Newly red Nightly source-closure selector

Observed on Runtime Nightly [43954031460](https://github.com/banodoco/astrid-runtime/actions/runs/43954031460), job [133603706731](https://github.com/banodoco/astrid-runtime/actions/runs/43954031460/job/133603706731), Runtime `359e2d7e55369562ca9513557282ea8aff7645bc` with published R12 Agent `0e1543e0da2215db9cb3320cfd1083174c3c62a9`.

`tests/test_verified_host_launch.py::test_nine_component_measurement_parity_without_importing_astrid` is the sole `passed -> failure` transition among the same 667 Nightly testcase IDs. It fails with `KeyError: 'source_checkout_closure'` before comparing any closure values.

## Cause established by source and history

The test parses only top-level function definitions from `astrid/core/execution/generic_host.py`, then indexes the resulting namespace for `source_checkout_closure`. Agent commit [4e6e8c9fa71c1b869e419c0104ffad50619f805d](https://github.com/banodoco/astrid-agent/commit/4e6e8c9fa71c1b869e419c0104ffad50619f805d) intentionally moved the source measurement functions into `astrid/core/source_identity.py` and imported them into `generic_host.py`. At the selected published R12 pin, the new module defines the function and generic_host imports it. The stale AST extraction ignores that import. This observed KeyError is a stale test-location assumption; it does not establish a failing product measurement or safe closure parity.

## Ownership and disposition

Plan 38 P2r and A3 own the source-closure definition, the two independent measurers and their parity vectors. This selector is not listed by exact name in the plan's older inventory, but it directly tests that owned contract. Mark **WAITING — Plan 38 closure-contract ownership** and retain the failure unchanged. Do not restore duplicate measurement code, import unverified product modules in the test, bypass closure checks, or weaken the parity assertion. A future owner repair should extract or load only the agreed measurement boundary and prove both the existing source-checkout vector and installed-pair vectors.

This is read-only diagnosis. No test or product source was changed, and no new test execution was used. The complete per-ID comparison remains in `comparison.md` and `status-comparison.json`.
