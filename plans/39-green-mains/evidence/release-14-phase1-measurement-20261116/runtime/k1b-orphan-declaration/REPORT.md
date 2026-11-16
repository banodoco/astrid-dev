# K1b orphan declaration removal

Base: `a05d360c50b35c6803d710909c87b51daf5e84b2` (tree `0291fadcde521650fdc71257a9ec2fd61b7226a4`). Branch: `p39/k1b-orphan-declaration`.

## Historical verification

Primary commit `925a7dd1c648a7632ba5b44a53566329ad947564` deleted the retired-only `test_timeline_shot_and_reference_creation_are_keyed_durable_and_non_overwriting` body from `tests/test_runtime_exact_idempotency.py` while retaining `test_project_reference_creation_is_keyed_durable_and_non_overwriting`. The K1b inventory group 3 independently records the same distinction.

## Scope and static counts

Only the `runtime-exact-idempotency` entry was removed from `tests/lanes.py` and its exact mirrored `_PINNED_XFAILS` entry from `tests/test_skip_guard.py`. No metadata was added, no guard implementation or cap changed, and no test body was edited.

Static AST counts from the base and worktree: exact quarantine IDs `20 -> 19`; declaration groups `10 -> 9`; semantic pins `10 -> 9`. This addresses the single orphan only. It does not make the overall quarantine inventory valid: the nine remaining groups still lack required metadata and the count remains over the limit.

The live project-reference test remains intact, including restart replay, changed-payload 409, overwrite 409, and the stored name assertion. No edits were made to `tests/test_runtime_exact_idempotency.py`.

## Focused proof

The exact focused command from the card ran before and after the edit. Complete raw outputs are in `focused-before.log` and `focused-after.log`; each ended with `6 passed` and exit code `0`.

`git diff --check` passed. The only product files in the patch are `tests/lanes.py` and `tests/test_skip_guard.py`; the exact patch is `patch.diff`.

One initial evidence write used the mistaken path under `p39-repair/p39-g2-evidence`; both logs were moved to the workspace-absolute evidence directory specified by the manager, and the mistaken directory was removed.

## Local commit

Commit: `2777051c06c3d15e14d3e8d13de26b19f875c4bc`
Tree: `2749ee50447b2082b198cf561c895796a6d09444`
Committed product paths: `tests/lanes.py`, `tests/test_skip_guard.py` only. Working tree is clean. No publication was performed.
