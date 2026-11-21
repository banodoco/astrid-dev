# Plan 72 PD-8 — independently reproduced fixed-revision public-feed bytes

**Evidence only; not an independent RS1 design verdict, current-head acceptance, or release approval.**

## Source custody and exact serialization

- Original source: `banodoco/astrid-dev` `4b3e3841af3921d9846389a4cd744f027c1db0b3` (pre-reader `main`).
- Corrected reader source: `banodoco/astrid-dev` `577034321cdfc8c2e8d554cacc5d3b563ab8ddb3` ([reader PR #1076](https://github.com/banodoco/astrid-dev/pull/1076)). The additional Vision-role candidate was **not** part of this source pair.
- **Fixed revision argument on both sides:** `4b3e3841af3921d9846389a4cd744f027c1db0b3`.
- Native independent scratch: [PR #1132](https://github.com/banodoco/astrid-dev/pull/1132) at `98824c0a5efd59df7794ad2f7c70e9ed000c11fa` (source script `scripts/test_plan72_fixed_feed_pair.py`), [GitHub Actions run 44852832010 / documentation job 136687970363](https://github.com/banodoco/astrid-dev/actions/runs/44852832010/job/136687970363).
- The scratch test independently used `git archive` to extract **both actual Git trees**, imported each source tree's own existing `export_public_vision.build` implementation, and serialized `json.dumps(page, ensure_ascii=False, indent=2) + "\n"` as UTF-8. It did not use Plan 72's proposed relationship reader to build either public feed.

## Actual independently measured bytes (not copied from the supplied report)

| Fixed `--revision` argument on both sources | Base bytes | Reader bytes | Base and reader SHA-256 | Exact byte comparison |
| --- | ---: | ---: | --- | --- |
| `0000000000000000000000000000000000000000` | 161,224 | 161,224 | `bf486591a268d6c5004d720dc67fef9419e75c288f72dfb400c8cf2f57299ec9` | **Equal** |
| `4b3e3841af3921d9846389a4cd744f027c1db0b3` | **161,224** | **161,224** | **`df1a3a245f88e0771464ac586802b4c9c7b5b4a7056e1e2e02787de94fe3faf1`** | **Equal** |
| `577034321cdfc8c2e8d554cacc5d3b563ab8ddb3` | 161,224 | 161,224 | `6124f77de5916b33084e8c9ef54fbecf64606c9cf3cf420baa454364619bdf41` | **Equal** |

The native log independently printed `PLAN72_REPORTED_DIGEST_MATCHED=True` for the middle fixed revision. The reported 161,224-byte size and SHA-256 are therefore corroborated **for this explicit source pair and revision**, not assumed.

**Whole-job limitation:** The scratch PR was tested while its base branch carried the separately reproduced test-only unresolved-Vision-role regression. Consequently [run 44852832010](https://github.com/banodoco/astrid-dev/actions/runs/44852832010) ended with two unrelated role-test failures (471 tests total), **not a fully green CI verdict**. The parity test's three direct byte comparisons succeeded; do not use the overall job as an all-green qualification. A later additive source correction and full-suite run is needed to qualify the combined candidate.

## Outstanding

This evidence compares **source trees `4b3e3841` and `57703432`** only. It cannot prove that subsequent shared-parser role changes, future Goals-authoring PR #1059 or the final integrated Release 15 head produce byte-identical feeds. PD-8/PD-11 must rerun the same fixed-revision comparison on the final exact candidate. No planned source or assertion change is authorized by this evidence; independent architecture RS1 and Release 15 manager/branch custody remain open.
