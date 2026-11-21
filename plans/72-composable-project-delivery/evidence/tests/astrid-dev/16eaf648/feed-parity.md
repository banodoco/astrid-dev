# Plan 72 RS1 snapshot — fixed-revision public feed byte comparison

**This is source-byte evidence, not an RS1 architecture verdict, runtime reviewer binding, final Release 15 integration or completion record.**

## Exact source identities

- Original Astrid Dev source: `banodoco/astrid-dev` commit `4b3e3841af3921d9846389a4cd744f027c1db0b3`.
- Prospective independent review candidate: [draft PR #1161](https://github.com/banodoco/astrid-dev/pull/1161), `p72/rs1-integrated-review-snapshot`, commit `16eaf64899f2dde82c7cb79ad92b88928afbd374`, tree `d156c7314bd1b1505fb5e8b93330a7dedb3459fb`.
- Composed candidate parents: parity `eda2c972faf8a8ac7ff34680b446c1223bc08057`, guide `1b996a73bfc0d64a57659abf3d2105e04705d82b`, both descended from corrected reader `2bef3d9b295008733ae672204ebf728c1a069ed5` and typed core `06c0ce64bb86e7524bb80208388c0d7147d8f511`. The candidate is **not** `release/15/main` or `release/15/plan-72`.

## Independent native source-tree comparison

The isolated, **unmerged** scratch [PR #1166](https://github.com/banodoco/astrid-dev/pull/1166), head `e41d37af729a9a791c68180c9bdfa393d3b60c4d`, ran the existing source-pair test with the reader SHA changed to the composed candidate. Its [GitHub Actions run 44874051137](https://github.com/banodoco/astrid-dev/actions/runs/44874051137) passed **482/482 selected tests** in [documentation job 136754704594](https://github.com/banodoco/astrid-dev/actions/runs/44874051137/job/136754704594) and the [App vision-consumer contract 136754981716](https://github.com/banodoco/astrid-dev/actions/runs/44874051137/job/136754981716) **success**. The [actual measured-values receipt](https://github.com/banodoco/astrid-dev/pull/1166#issuecomment-7058424232) is on that closed scratch PR.

The test extracted each immutable Git source with `git archive`, imported **each tree's own original `export_public_vision.build`**, serialized with `json.dumps(..., ensure_ascii=False, indent=2) + "\n"` encoded as UTF-8, and directly compared all output bytes. It did **not** derive the public feed from the new relationship graph.

| Explicit fixed revision argument, used identically on both trees | Original bytes | Snapshot bytes | SHA-256 on both trees | Entire byte stream equal? |
| --- | ---: | ---: | --- | --- |
| `0000000000000000000000000000000000000000` | 161,224 | 161,224 | `bf486591a268d6c5004d720dc67fef9419e75c288f72dfb400c8cf2f57299ec9` | **Yes** |
| `4b3e3841af3921d9846389a4cd744f027c1db0b3` | 161,224 | 161,224 | **`df1a3a245f88e0771464ac586802b4c9c7b5b4a7056e1e2e02787de94fe3faf1`** | **Yes** |
| `16eaf64899f2dde82c7cb79ad92b88928afbd374` | 161,224 | 161,224 | `147dd4388a7a07bb7f99d114e58e4c74d10d67636411301fff70db5693a1a659` | **Yes** |

All three byte comparisons passed; this is a *new combined source pair*, not an assertion copied from the prior reader-only parity proof.

## Review and release boundaries

The integrated read-only [RS1 source candidate #1161](https://github.com/banodoco/astrid-dev/pull/1161) has its own native full test and App compatibility run; the scratch source pair also passed. The independent high-judgment Astra reviewer is **prospective only**, requested in [Plan 72 inputs](../../../inputs.md) under [PR #1162](https://github.com/banodoco/astrid-dev/pull/1162). Exact model binding, supported high reasoning, separate principal/session, source permissions, actual invocation and case-cited verdict remain **unverified**. No RS1 round was consumed.

Release 15 manager and Astrid-dev integration branch custody are not accepted ([handoff #1098](https://github.com/banodoco/astrid-dev/pull/1098)). This evidence cannot substitute for final exact-head CI, source pairing or the final independent review once the release-integrated head exists. Keep all existing acceptance and merge rules unchanged.
