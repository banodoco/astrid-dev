# VibeComfy PR #182 range record — 22 November 2026

## Revision range

PR [#182](https://github.com/banodoco/VibeComfy/pull/182), base `48b5fa9e45630e1bc502651975ec0ef3a5e74c4c` → head `36ea976ffa24ac3ab5b5e48b7b279af7565d5c41` (4 files, +192/−3): `vibecomfy/porting/object_info/consume.py`, `vibecomfy/workflow_bundle.py`, `tests/test_bundle_class_memo.py`, and `tests/test_bundle_identity_memo.py`. The change scopes a class lookup memo to bundle emission using a context variable, with separate tests for class memo and bundle identity memo behavior.

## Recorded proof

- The PR description reports 53 templates with identical bundle bytes, warnings, refusals, and revisions. Across those 53 templates it reports **1,727,684 witness calls and 630,488,716,236 bytes before**, versus **37,190 calls and 13,676,980,048 bytes after**. These are PR-reported aggregate counts, not independently reproduced in this record.
- The PR reports 194 existing IDs matched (188 pass and six same failures), 15 new focused cases, and three unchanged same-metadata passing cases. The exact Astrid W candidate count was not reproduced here.
- The installed A/B candidate tuple includes this VibeComfy head; see [`2026-11-22-installed-attribution-review.md`](2026-11-22-installed-attribution-review.md) and `/root/codex/installed-baseline/evidence/ab-run-1/`. Agent and Runtime changed in the same A/B, so that run does not isolate PR #182’s effect.
- Source-harness attempts 01 and 02 waited without producing samples. Attempt 03 failed closed at attestation; it did not attest `consume.py` execution in host/descendants and produced no source A/B result. The limits and attempt record are in [`2026-11-22-attribution-completeness.md`](2026-11-22-attribution-completeness.md) and `/root/codex/plan-81m/run/witness-attempts-2026-11-22.tar.gz`.

## Not established by these records

The source harness did not produce a measured before/after result. CLI-process witness counts do not cover host/Runtime or establish a complete cross-process/global hashing budget; the observer can miss events. The installed A/B is joint across repositories and cannot quantify a PR-specific speed effect. The PR-reported template and ID counts have not been independently reproduced here.

## Inherited CI context

Astrid-dev issue [#1311](https://github.com/banodoco/astrid-dev/issues/1311) tracks the inherited VibeComfy gate failure. The host identified this as inherited context; this record does not assign it to PR #182.

Source notes: host record `/root/codex/plan-81m/run/to-codex.md` (16:12 UTC, 22 November 2026); PR [#182](https://github.com/banodoco/VibeComfy/pull/182); evidence PRs [#1422](https://github.com/banodoco/astrid-dev/pull/1422) and [#1423](https://github.com/banodoco/astrid-dev/pull/1423).
