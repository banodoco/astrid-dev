# Fresh fast-checks comparison

## Run identity and sources

- Fresh run: GitHub Actions run **44447425471**, job **135302866190** (`fast checks`), checkout `banodoco/astrid-agent` commit `513204189161c4f72abc73e4fe7d46d7e97ac534` (`release/14/plan-65`). Source log: `run/ci-44447425471-fast.log`.
- Comparison base: `run/ci-release14-baseline-fast.log` in `/home/user/work/managers/plan-64` (the saved release/14 baseline, checked out at `b50371baf101d6f706269fab38cdf3a7a5eb2013`).
- The logs use the same fast-check gate commands and relevant pins. Comparison below is of logged outcomes, not a rerun.

## Gate outcomes

| Gate | Fresh run | Base | Classification |
|---|---|---|---|
| Dependency/setup steps (checkout, install project/dev deps, install runtime and VibeComfy) | Completed; Ruff starts at fresh log line 1676 | Completed; Ruff starts at base line 1675 | No newly logged setup failure. |
| Ruff (`make ruff`) | `✓ ruff baseline (no lint regression)` (line 1749) | Same result (line 1743) | Pass; no new lint regression. |
| mypy (`make mypy`) | `✓ mypy baseline (no type regression)` (line 1973) | Same result (line 1956) | Pass by the gate's baseline comparison; no new type regression declared. Fresh output still reports per-file diagnostic counts, including `astrid/installer/runtime_lifecycle.py | assignment: baseline=0 current=1` (line 1823), so this means the configured gate passed, not that mypy has zero diagnostics. |
| Import cycles (`make cycles`) | `cross-package 2-cycles: 8`; `OK: no new cycles (fixed 0, remaining 8)` (lines 1989, 2002) | Same count and result (lines 1972, 1985) | Pass; 8 existing cycles remain, no new cycles. |
| TLS policy regression pytest | `157 passed, 1 deselected in 16.29s` (line 2193) | `157 passed, 1 deselected in 16.36s` (line 2176) | Pass; same test count. |
| Separately run TLS error-contract test | **Fails**: `tests/test_astrid_error_contract.py::test_to_envelope_omits_code_and_source_type_when_none`; assertion says `'code' not in {... 'code': None ...}` (fresh lines 2222–2224). | **Same failure and assertion** (base lines 2205–2207). | Pre-existing, not introduced by this run relative to the saved base. This is the sole pytest failure reported in either log. |
| Test collection (`make collection`) | `Collection gate passed` (line 2310) | `Collection gate passed` (line 2293) | Pass; no collection regression. |
| Upload test artifacts | Both `tls-policy-regressions` and `tls-error-contract` uploaded successfully (fresh lines 2258, 2293). | Both uploaded successfully (base lines 2241, 2276). | Pass; failure did not prevent artifact capture. |

## Classification

The fresh fast-check log reproduces the base's exact single failing test, with the same assertion that `code: None` is present in the envelope. There is **no new failing test ID**. Ruff, mypy's configured baseline gate, cycle detection, the 157-test TLS policy suite, and collection all have the same pass outcome as the base. The cycle count remains 8. Therefore this fast job has a pre-existing failure, but no newly introduced fast-gate regression is evidenced by the direct log comparison.

The fresh log ends after cleanup with an Actions Node.js 20 deprecation warning (line 2368); the base has the same warning (line 2351). That warning is not a gate failure. Because the separately run pytest step exited 1 (`##[error]Process completed with exit code 1`, fresh line 2224; base line 2207), this job should not be described as wholly passing.
