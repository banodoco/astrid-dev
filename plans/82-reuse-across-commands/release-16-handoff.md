# Plan 82: Release 16 handoff (written 25 November 2026)

Release 15 landed Plan 82's **stage 1** and moved **stage 2** to Release 16 (Release 15 Lead ruling r15-lead-p82-0007, [#1824](https://github.com/banodoco/astrid-dev/issues/1824)). This note says what is landed, what is accepted but held, what is blocked, and what is owed. Source of truth for the cards stays [tasks.md](tasks.md); the board is #1824.

## What Release 15 claims for `generate`

**Not slower; approval compile faster.** Installed `generate` to "task queued", stand-in ComfyUI: base 5.56 to 5.65 s, stage-1 candidate 5.48 s; the approval compile is down about 0.16 s ([evidence](evidence/2026-11-24-stage1-installed/README.md), measured on `e254d780`; the landed head differs only in the receipt verifier and the SDK preflight, which run before that stage). **The ~3 s target is missed and moves to Release 16.** The estimate after the measurements (RA-0a) was about 3.1 s (2.8 to 3.4) with every cache in ([RA-0a record](evidence/2026-11-24-ra-0a-measurements/README.md)); stage 1 has no cache, so it is expected to move the number only a little.

## Landed (stage 1)

| Card | Where | What |
| --- | --- | --- |
| RA-6 | astrid-agent `release/15/main` `edfc2dc9` (PR #642, plan branch merged at `3d8a25d6`) | The host (`generic_host.py`, before placement and engine preparation) recomputes `workflow_content_digest`, `revision_id` and `api_digest` from the admitted bytes and refuses a stale or forged receipt/companion (`VIBECOMFY_INVOCATION_RECEIPT_MISMATCH`); a direct POST is covered. Receipt-less legacy single-file UI tasks and Runtime-owned delegated children are unchanged. |
| RA-6 lane fixes | #640 | An H3 prepared source may pair with its archive `source_video` asset only if the archive row's lineage kind is `h3_source_conform` and the staged file is a regular file with the asset's bytes; the no-archive SDK preflight no longer derives an expected prompt from workflow inputs. Two adversarial strictness reviews, every finding fixed. |
| RA-1b | same | Lazy imports in `dispatch.py` and `backends/__init__.py`; VibeComfy `vibecomfy/porting/edit/ops.py` loads provider exceptions lazily (VibeComfy `release/15/main` `2e1b603f`, PR #215). `import vibecomfy.porting.edit.ops`: 467 to 92 modules. |
| Counters | same | `cache_event(cache, outcome, reason=None)` in `astrid/sdk/command_timing.py` (`cache_events` in `--json`, `cache <name>: <outcome> (<reason>)` under `--timings`). Read them before trusting any timing. |
| Pin | same | VibeComfy `901fc611` (an ancestor of landed `2e1b603f`), generator-written. |

Gate evidence: Lanes run 45493009546 on the landing head against base Lanes 45351510868, whole run by id: 0 new failing ids; the 8 regressions pass; old-head `ci.yml` 45440748647 by id against `agent-ci-baseline-8807f820` clean ([#1824, DONE of 24 Nov](https://github.com/banodoco/astrid-dev/issues/1824#issuecomment-7147484655)). The `release/15/main` push runs (CI 45510560565, Lanes 45510560629) are the backstop; the Release 15 Lead compares them.

## Accepted on proof, not merged (keep open; Release 16 rebases)

| PR | Head | State |
| --- | --- | --- |
| VibeComfy [#208](https://github.com/banodoco/VibeComfy/pull/208) `p82/RA-2a` (P82-03, VibeComfy half: prepared template contract, key and store) | `40afa618aba523611a37ae4e3555efce346bafd8` | Proof accepted: the two prepared-template files 87 passed (root and uid 65534) on a scratch merge with VibeComfy `release/15/main` `2e1b603f`; the packet's red control makes `[sections]` fail with `workflow.py bytes differ`; the VibeComfy approval and parity files fail only on baseline ids. High-judgment review passed with three conditions, all met by the packet. |
| astrid-agent [#633](https://github.com/banodoco/astrid-agent/pull/633) `p82/RA-2a` (Agent half) | `911614c1680a1f95b82ac2a66053d1e94e88f75c` | Proof accepted on scratch merges: default lane 379 passed and 10 failed (all 10 fail on the base), new files 59 + 5 + 8 passed, integration lane 41 passed, new tests 72 passed as uid 65534. It is written against VibeComfy `8da59eea`; #208's new head only fixes one test fixture. |
| astrid-agent [#623](https://github.com/banodoco/astrid-agent/pull/623) `p82/RA-0b-stamp` (P82-06: install stamp and read-only install) | `91daa8936b490c037452d28bbb78645e870dcb59` | Proof accepted (default lane identical to the base's failures; new stamp tests pass as uid 65534 and root; update, rollback and uninstall pass). Still owed: the high-judgment review of the stat-token check, the installed measurement of `install_stamp()` against `verify=True`, and the rule that it ships nothing until P82-07 uses it. |

Order for #208 and #633: VibeComfy #208 lands first (merge commit), then the Agent is re-pinned by the generator (`scripts/vibecomfy_pin.py <sha> --checkout <path>`, which rewrites six pin manifests plus the literal in `tests/test_windows_path_budget.py`), then #633. VibeComfy stage 1 is already landed, so #208 is unblocked on its side.

## Blocked packets (briefs exist, not started)

| Packet | Needs |
| --- | --- |
| [P82-04](../../releases/15/packets/R15-P82-04.md) (RA-2 second seam: structural approval cache) | P82-03 merged and re-pinned |
| [P82-05](../../releases/15/packets/R15-P82-05.md) (RA-2 third seam: the 53-template differential and four mutation checks) | P82-03 and P82-04 merged |
| [P82-07](../../releases/15/packets/R15-P82-07.md) (RA-0b second half: shipped discovery and registry caches under the stamp) | P82-06 merged and Plan 87's RN-4 (pack roots from one place, PB-7b) on the base branch; it must run the duplicate-name admission and the pending-transaction check on every persistent hit (PB-7c) |
| R (final review, on the high-judgment role) | P82-03 to P82-07 |

## Notes to carry

- **A warm prepared-template hit needs an installed VibeComfy distribution** (`key_context` refuses without a version, so a source-only checkout records `entry_invalid` and builds in full). Measure RA-2a on an installed build, not a source tree.
- **Custody of the cache:** digests are not a MAC; the store has the same custody as the template sources (data root, owner-only, entries owned by the current user). A residual risk is recorded in #633.
- **Measurements still owed** (installed, on the exact head, counters read first): the RA-2a key stage at most 0.1 s warm and the builder skipped; the warm approval compile; `install_stamp()` against `verify=True`; the discovery and registry stage with a warm cache (the floor experiment put pack discovery near 2.3 s); the full chain against the 3 s target.
- **Test lanes:** the integration lane is deselected by default (`ASTRID_CI_JOB=lanes-integration -m "integration and not opt_in and not app_checkout"`). The `local-managed` integration variants cannot run in the cloud sandbox (they fail on the base the same way); the hosted Lanes run is their check. Run the unprivileged tests with `setpriv --reuid=65534 ...`. A test must not skip in its body (the repo's `_SkipGuard` fails undeclared skips); use `@pytest.mark.non_root`.
- **Follow-ups:** the RA-6 backlog is [#1855](https://github.com/banodoco/astrid-dev/issues/1855) (the Runtime validator seam is Plan 92 and Release 16); tasks.md "Dispatch decisions" records the rulings.
- **Process rules that applied:** packets never merge, never edit tasks.md and never dispatch CI; code and test fixes are written in ChatGPT packets, not by the orchestrator (r15-lead-0015).
