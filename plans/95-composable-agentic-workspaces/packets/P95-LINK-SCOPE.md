# P95-LINK-SCOPE — opt-in link anchor target scope

**Route:** N (normal ChatGPT High). **Repository:** public `banodoco/otto`. **Branch:** `p95/ot-link-scope` from Otto main `2ad2550201d0593893459ffebcbfe528df0ef48c`, draft PR to `main`. **Authority:** run.md on astrid-dev main `edd6029f9ee4808fddd280977edfc0b75b7eb15a`; owner-delegated decision issue #1886 comment 7245203000. Packet source is this immutable commit on the Lead's draft progress branch, under the previously recorded source exception 7222210215.

## Outcome

Allow a workspace to opt into a validated regex narrowing the built-in `link-anchors` check's resolved Markdown **target** paths; absence remains strict across all relative Markdown targets. This implements Dev-owned target policy in the RS1 contract; do not change anchor recognition, diagnostics, heading semantics, other checks, releases, Dev, or add dependencies. No assertions in existing tests may change.

## Step 1 — inventory and stop

Before edits post an exact schema, allowed file/function list, default and regex validation behavior, and a test matrix to issue #1886 as `p95-P95-LINK-SCOPE-1`; wait for Lead decision. Proposed schema: optional `[link_anchors] target_pattern = '...'`, independent of `[checks]` adapter registration. Reject malformed types, empty values and invalid regex with source-aware config errors; absent option uses `None`. Match normalized repository-relative *target* with `re.fullmatch`, not source; ensure configuration can only narrow the default `.md` domain, while preserving any contractual direct helper API. Preserve check IDs/order, exclusions and outputs.

Tests must cover default strictness, standalone configuration without adapter, invalid/unknown config, in-scope target linked from out-of-scope source and reverse, same-file links, nested/top-level paths, non-Markdown targets, exclusions, real Dev regex behavior in synthetic fixtures, and unchanged default list and diagnostics. Keep public Otto free of private data. Lead runs all tests, fixture checks and proof; Dev's actual config and parity belong to OT-20.

Post early STATUS and draft PR, then `READY-PROOF <repo> <PR> <head> <selectors>` and stop. Do not clone, run tests/build/CI, merge, edit plan records or perform another packet.
