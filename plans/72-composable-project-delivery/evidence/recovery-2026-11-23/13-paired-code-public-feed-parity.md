# Plan 72 — paired frozen-code versus selected-code public feed proof

**23 November 2026 · source-only disposable integration rehearsal · Release 15 HOLD.** This is a test of public-feed invariance under changing the reader code while holding authored data *constant*, not an approval to merge, a cross-revision real publication, RS1, a Lead GO or final Release 15 qualification.

## Exact test identity and method

The native test [`scripts/test_project_delivery_release15_scratch.py`](../../../../scripts/test_project_delivery_release15_scratch.py), blob `adc85205bb2ded4dfa177eb0dd6558af5a5c0a66`, gained one `test_paired_frozen_and_selected_code_export_same_authored_feed` method at code head `9e9466738bf9261ba8eaa4a3708a83263891fed9`. This extends, rather than replaces, the earlier unchanged original real-repository traversal, missing-Plan72-authored-source negative, and same-code before/after traversal tests.

The test constructs **two detached temporary Git worktrees**:

1. **Frozen-code side:** exactly `321523e52bddbbd13477634b05974a16b54b825b`, without modifying its parser or public exporter. Copies the canonical Plan72 `plan.md`, `inputs.md` and `tasks.md` by their exact pinned blob contents and the temporary composed `releases/15.md` from the selected side.
2. **Selected-code side:** the existing disposable frozen Release15 checkout after native `git apply --check` and `git apply` for source patches **01–05**, **08** and **09**, with the same three canonical authored Plan72 files and the same temporary composed release brief (the original frozen 39/50/40 plans plus the canonical Plan72 membership and five verbatim branch-table rows).

**Equality precondition:** The test computes SHA-256 on **every `*.md` authored file in both trees**, requiring identical paths *and* identical hashes, not merely equal file counts. **416 Markdown files** were paired. It verifies the source SHA and revision are pinned, builds `export_public_vision.build(root, "0" * 40)` separately in each checkout with imports from that checkout's `scripts/`, serializes identically with UTF-8 / `json.dumps(..., ensure_ascii=False, indent=2) + "\n"`, and requires **byte-for-byte equality** and `schemaVersion == 1`. Both inventories are rechecked afterward to reject unintended source mutation. The baseline detached worktree is removed in `finally` with no remote Git mutation.

This controls for authored-record drift while testing the effect of **selected code change** on actual publisher output. It does **not** assume equal public content for the *different* real historical documents in frozen Release15 versus newer canonical main, nor compare served release 14 outputs.

## Hosted evidence (complete)

| Source head | Hosted native result | Verdict |
| --- | --- | --- |
| `9e9466738bf9261ba8eaa4a3708a83263891fed9` | [Documentation integrity + App consumer 45243346189](https://github.com/banodoco/astrid-dev/actions/runs/45243346189) | **COMPLETED SUCCESS**. Python documentation job `137933550289`: **527/527 tests**, native scratch `01–05, 08, 09` patch application, repository checks, generated views current. Actual App `vision-consumer-contract` job `137934440652`: **13/13 tests passed**. Refresh-generated/publish-vision skipped as expected. |

The hosted Python log printed this exact receipt:

```text
P72 PAIRED FEED PARITY: bytes=150702 sha256=38b04ed594662eaafdf54f95e599f0a6136f31d3729f2b59b4eaf929bdcef658 authored_files=416
Ran 527 tests in 76.591s
OK
```

**Byte count: 150,702. SHA-256: `38b04ed594662eaafdf54f95e599f0a6136f31d3729f2b59b4eaf929bdcef658`.** Both sides emitted identical schema-v1 JSON at fixed revision `0000000000000000000000000000000000000000`. The number/hex are particular to the *rehearsed identical authored inputs* and should not be used as a global golden for another release source.

## Earlier original traversal and missing-source cases remain preserved

- The original, unchanged `test_project_delivery.DeliveryCompositionTests.test_actual_repository_delivery_traversal` passed when invoked from the patched frozen release worktree: [run 45232107837](https://github.com/banodoco/astrid-dev/actions/runs/45232107837), with authentic `gap:AA-001`, `project:72`, authored `goal:pillar:artistic-ambition/finished-artistic-work` and a goal→release path; **Plan72 remains a gapless Foundational enabler**, not a fabricated project→gap edge.
- Removing only the canonical `plans/72-composable-project-delivery/plan.md` from the disposable worktree forces the **same unchanged original traversal** to exit nonzero with `Plan 72 names unknown folder`. File bytes are restored in `finally` and canonical SHA rechecked: [run 45232564315](https://github.com/banodoco/astrid-dev/actions/runs/45232564315).
- Querying the real graph does not mutate the schema-v1 public feed in one composed checkout: [run 45233070565](https://github.com/banodoco/astrid-dev/actions/runs/45233070565). The current two-code paired test adds a stricter invariance guarantee rather than substituting for those earlier negative and real-source tests.

For full native patch and composed authored-record construction, consult [11-disposable-release15-result.md](11-disposable-release15-result.md) and [12-native-real-traversal-and-feed.md](12-native-real-traversal-and-feed.md).

## Release and ownership disposition

The canonical [Release 15 run board on main](https://github.com/banodoco/astrid-dev/blob/main/releases/15/run.md) still records Plan72 **HOLD**, manager not yet accepted and owner bounded-scope decision pending. The already named Lead is `session_011EzfW1gtAhRQwk8pgJMzhG`; the latest [#1245 ownership request](https://github.com/banodoco/astrid-dev/pull/1245#issuecomment-7106544471) had **no newer response** at this observation. The actual `release/15/plan-72` branch remains absent. Generic parser/branch-table ownership, exact integrated authored records, Release15-main protections, formal RS1, final review and publication remain separate gates.

**Not done:** no writes to release refs, no changes to GitHub branch protection, no merge, no formal reviewer/RS1 dispatch, and no claim that this rehearsal exercises the *entire later Lead-accepted Release15 combined head*. All original tests and fixtures remain unchanged.
