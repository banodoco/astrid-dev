# Plan 72 — original-versus-corrected-reader public feed byte parity

**Scope:** independent exact-source-pair validation of a read-only Plan 72 reader at a fixed revision. **Not** the final integrated Release 15 qualification or architecture verdict.

## Source pair and native method

- **Original:** `banodoco/astrid-dev` `4b3e3841af3921d9846389a4cd744f027c1db0b3` (prior to Plan 72 code).
- **Corrected reader:** `banodoco/astrid-dev` `915761c49341aea3eefd383386951b1aad804a5b` ([reader #1076](https://github.com/banodoco/astrid-dev/pull/1076)).
- **Experiment:** closed **without merge** [scratch PR #1148](https://github.com/banodoco/astrid-dev/pull/1148), head `92fcda65c8cc4a827e73634b229411354c4cb3b2`. [Native Actions run 44864339456](https://github.com/banodoco/astrid-dev/actions/runs/44864339456): **477/477 unit tests PASS** and [App vision-consumer contract](https://github.com/banodoco/astrid-dev/actions/runs/44864339456/job/136724782299) **success**. See [raw measured-value receipt](https://github.com/banodoco/astrid-dev/pull/1148#issuecomment-7057048276).
- The original `test_plan72_fixed_feed_pair.py` was reused unmodified except to set the reader commit to `915761c4`. It used `git archive` to extract each pinned tree, imported each tree's **own existing** `export_public_vision.build`, then independently serialized canonical JSON using `json.dumps(..., ensure_ascii=False, indent=2) + "\n"` and compared complete UTF-8 bytes. It **did not** call the new relationship reader to construct either public feed.
- Both sides received the **identical explicit revision string** for each row below, avoiding spurious revision metadata differences.

| Fixed revision passed to both exporters | Original bytes | Reader bytes | SHA-256, identical on both sides | Byte-equal |
| --- | ---: | ---: | --- | --- |
| `0000000000000000000000000000000000000000` | 161,224 | 161,224 | `bf486591a268d6c5004d720dc67fef9419e75c288f72dfb400c8cf2f57299ec9` | **Yes** |
| `4b3e3841af3921d9846389a4cd744f027c1db0b3` | 161,224 | 161,224 | **`df1a3a245f88e0771464ac586802b4c9c7b5b4a7056e1e2e02787de94fe3faf1`** | **Yes** |
| `915761c49341aea3eefd383386951b1aad804a5b` | 161,224 | 161,224 | `ca9c34fb3bea2f59efc02112376f74c223d6c02bf0ba318ff73e5c7fb83693c5` | **Yes** |

## Related exact-head controls

- Tests-first reproduction `8e745182` in [CI 44863623760](https://github.com/banodoco/astrid-dev/actions/runs/44863623760): 476 tests, six failures for malformed gap-heading / duplicate Release declarations.
- Corrected reader source `915761c4` in [CI 44863786568](https://github.com/banodoco/astrid-dev/actions/runs/44863786568): **476/476 PASS**, native App consumer **success**. See [red/green regression record](summary.md).
- Dependents: [parity probe #1106](https://github.com/banodoco/astrid-dev/pull/1106) is `6907d14f`; [extension guide #1079](https://github.com/banodoco/astrid-dev/pull/1079) is `77550748`. Both have their own native green CI and were advanced additively without rewriting history.

## Limits and authority

This verifies byte equality on the **named original-vs-reader source pair** and three stated fixed revision inputs. It does not validate future Goals authoring PR #1059, complete the check registry integration, or prove byte equality at a later merged Release 15 head. Independent architecture **RS1** review has not been submitted; Release 15 Lead custody and its Astrid-dev integration branches are unresolved. No product source, acceptance assertion or task completion is changed by this evidence.
