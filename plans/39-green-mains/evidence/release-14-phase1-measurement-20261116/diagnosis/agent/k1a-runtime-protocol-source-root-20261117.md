# Plan 39 K1 — Runtime package provenance split: 95 setup failures

**17 November 2026 UTC. N-class evidence/source trace; X-class coupled resolution hold.** This is a new diagnosis, **not** an accepted fix, an independently submitted review, or an additional 95 failures. The identity and import-root assertions remain unchanged.

## Exact hosted evidence

At Agent PR369's exact merged head `6bbda788c1a62abcdda242f85c7a1cae86c57d3d` and reviewed tree `c0a0cc55b363fa71a27fedcaa57b08076d9ae180`, [CI 43967861168](https://github.com/banodoco/astrid-agent/actions/runs/43967861168) attempt **1** finished failing; [Lanes 43967861160](https://github.com/banodoco/astrid-agent/actions/runs/43967861160) attempt **1** also finished failing. The pre-existing checked, complete JUnit inventory (compressed JSON SHA-256 `729e8a833061dc0b29c6cc345aef8b61d740ba83f004d969923398fc3a9c5426`) has one **identical literal XML error string**, SHA-256 `9955b76881fd4a298a92e7917ee1d4be8a4bfd0b0ff1bff62a40709b6c598b0b`, in two unit-shard jobs:

| Exact CI job | Exact full-message occurrences | JUnit artifact | Previously verified artifact ZIP SHA-256 | Inner XML SHA-256 |
| --- | ---: | --- | --- | --- |
| [unit shard 7, job 133651924616](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924616) | **92** | [14281865130](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14281865130) | `3d208e420b35370e7b153a3f6349a64c415df126e87d3f5d97b7b1b9c8c0693a` | `3bd9218c3830caf27bc2502a50ebc7293c19012bad01a2e890b1f31c703b993b` |
| [unit shard 6, job 133651924641](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/job/133651924641) | **3** | [14283023095](https://github.com/banodoco/astrid-agent/actions/runs/43967861168/artifacts/14283023095) | `74811e80afd29518a356b8f2dd4b4794b4a34f5ea375412dc5ad11cab0ea7d47` | `b397f917a9ef5f01734ff06fcaeb7b7e39d8a35d3064f4d610977fc97168f89a` |

The full literal message is:

```text
failed on setup with "AssertionError: assert PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages') == PosixPath('/home/runner/work/astrid-agent/astrid-agent/astrid-runtime')
 +  where PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages') = PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol').parent
 +    where PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol') = PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py').parent
 +      where PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py') = resolve()
 +        where resolve = PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py').resolve
 +          where PosixPath('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py') = <class 'pathlib.Path'>('/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py')
 +            where '/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py' = <module 'runtime_protocol' from '/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/site-packages/runtime_protocol/__init__.py'>.__file__
 +  and   PosixPath('/home/runner/work/astrid-agent/astrid-agent/astrid-runtime') = resolve()
 +    where resolve = PosixPath('/home/runner/work/astrid-agent/astrid-agent/astrid-runtime').resolve"
```

Representative exact testcase IDs from the actual shard-7 XML message group: `tests.sdk.test_timeline_helper_capture::test_genuine_anchor_capture_has_exact_source_scope_and_base_pair`, `tests.sdk.test_timeline_helper_capture::test_missing_or_forged_anchor_binding_never_writes[missing-pin]`, and `tests.sdk.test_timeline_helper_capture::test_missing_or_forged_anchor_binding_never_writes[forged-word]`. The exact 95 occurrences are **already within the historic 882 CI failures / 398 errors**. This note does **not** claim to have rechecked each ID's earlier baseline counterpart; absent old IDs are never classified as regressions.

## Source trace at the exact tested commit

1. [`.github/workflows/ci.yml`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/.github/workflows/ci.yml) unit-shard sets `ASTRID_RUNTIME_CHECKOUT` to the sibling checkout, checks out the lock SHA, installs the Agent editable (`pip install -e '.[dev]'`) and then runs `python scripts/ci_install_runtime.py` before pytest.
2. [`scripts/ci_install_runtime.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/scripts/ci_install_runtime.py) deliberately installs Runtime **non-editably**, via two GitHub source-archive package references at exactly the lock commit, into the interpreter's `site-packages`. This is not the same mechanism as the Darwin job, which uses `pip install --no-deps -e ./astrid-runtime -e ./astrid-runtime/packages/python`. The installed package can have the correct *revision* while failing an assertion that its import came from the *checkout path*.
3. [`tests/helpers/runtime.py`](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/helpers/runtime.py) resolves the checkout and `use_runtime()` prepends it to `sys.path`, but does **not** evict or verify a previously imported `runtime_protocol` in `sys.modules`. Its documented rule says the first imported Runtime tree wins. Whether pytest collection preimports the installed module remains unmeasured here; do not assert the import order from the failure string alone.
4. [`tests/sdk/test_timeline_restructure.py` lines 427–443](https://github.com/banodoco/astrid-agent/blob/6bbda788c1a62abcdda242f85c7a1cae86c57d3d/tests/sdk/test_timeline_restructure.py#L427-L443) defines the shared `restructure_runtime` fixture. It calls `use_runtime()`, imports `runtime_protocol`, then asserts `Path(runtime_protocol.__file__).resolve().parent.parent == runtime.resolve()` before building real Runtime service/provider tests. Multiple SDK modules import this fixture. That source-authentication assertion is meaningful and **must not be weakened**.

**Established:** CI provides a noneditable Runtime install in the same process where source checkout provenance is asserted; the observed module was actually from site-packages. **Not established:** whether the first import occurred at collection time, which package or fixture imported it first, whether these 95 would pass after changing import provenance, or whether noneditable-install parity for other tests is required by Plan 39's runner contract. This is a runner/test-harness isolation question with a possible real source-authority bug; do not label all 95 stale tests.

## Bounded next proof and review gate

Route initial read and mechanical source/fixture inventory as **N**. The resolution is **X** until the coupled installed-package/checkout-import contract is separated; an alteration affecting source identity or security requires **S** design/review. Actual distinct reviewer/model provenance is unavailable in this turn; no independent review is claimed.

In a real Agent worker checkout, run focused existing exact testcase selectors in the *same documented unit-shard environment* and record `sys.modules['runtime_protocol'].__file__` (if loaded), `importlib.util.find_spec`, `sys.path`, checked-out Runtime HEAD and installed distribution provenance **before and after collection**, without changing production imports or assertion semantics. Compare with a separately provisioned source-editable environment; protect the noneditable packaging/upgrade checks with their own executable proof. Only then decide between splitting the source-required cohort/process and changing the CI environment or fixing genuine early import contamination. Any candidate must get an independent X/S review and same-ID focused/hosted proof, not a blanket `sys.modules` purge, skip/xfail, or altered provenance assertion.

The distinct 68 E14 locked-SHA fixture failures in [draft PR377](https://github.com/banodoco/astrid-agent/pull/377) are **not** this cluster; changing that constant will not demonstrate source-root correctness. The 26 missing pod-bootstrap script cases and Plan55 generic-host tests remain separately held. Plan38/55 **WAITING**, Release15 excluded, Runtime clip patch **uncommitted 25 passed / 2 failed** on the replay/CAS-history owner decision. Formal **G1/G2 incomplete; RS1 0/1**. No branch is advanced, no product PR is merged and no other-session workflow is dispatched, rerun or cancelled here.
