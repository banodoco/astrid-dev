# Plan 55: code, notes and proof on GitHub

Publication checkpoint: 16 November 2026. This file records the owner's request to put the existing code on its relevant product branches and the project notes and materials on astrid-dev main. This is documentation publication, not Release 14 publication or product-main promotion.

**Same run:** `2026-11-15-local-speed`. **Accountable manager:** `chatgpt-workspace-6ee41b0f0cca/root`. The original ignored run configuration and unfinished observer worktree are not replaced. No task or formal review round is completed by this publication.

## Start with the current record

Read [tasks.md](tasks.md) and the latest owner replies first. [Progress PR #774](https://github.com/banodoco/astrid-dev/pull/774) is the existing tasks-only update to main; there is no second progress PR. It records D9's CPU-first order, the later decision record [#765](https://github.com/banodoco/astrid-dev/pull/765), renamed branches and newer CPU evidence. Its required checks must pass; queued is not green.

The [developer handoff](developer-handoff.md) and evidence copied here are dated source records from dev commit `315cb95025dc7c1498c8b9b5c664dc48bae3171d`, not a new assertion that every earlier blocker or approval hold is current. In particular, read the later progress/decision records before acting on its older Windows hold, re-pin request or scope request. Historical reports remain intact, not silently rewritten. The measured floor source-plan update remains in [#756](https://github.com/banodoco/astrid-dev/pull/756); this notes-only publication does not replace plan.md, inputs.md, tasks.md or review.md with older branch copies.

## Code is already published: reuse it

| Contribution | GitHub location | Publication state |
| --- | --- | --- |
| Safe cancellation and Python hash observation | [Agent #355](https://github.com/banodoco/astrid-agent/pull/355), branch `p55/d9-hash-observer-20261116`, commit `5d600a7cf77ec57799449b8241122b99af04167c` | Published task candidate; target `release/14/plan-55`, not product main |
| Real ComfyUI CPU-floor runner | [Agent #353](https://github.com/banodoco/astrid-agent/pull/353) | Existing task candidate; do not build another runner merely because an older chat says source access failed |
| Standing meter and Windows continuation | [Agent #359](https://github.com/banodoco/astrid-agent/pull/359) | Separate evolving candidate; inspect its current head and checks |
| Cheaper discovery fingerprint | [Agent #361](https://github.com/banodoco/astrid-agent/pull/361) | Separate candidate; not the whole of LS-12 |
| VibeComfy connection work | [VibeComfy #172](https://github.com/banodoco/VibeComfy/pull/172), `release/14/plan-55` | Existing plan branch; no new VibeComfy code is present in the local D9 bundle |
| Plan integration | [Agent #358](https://github.com/banodoco/astrid-agent/pull/358), [dev #753](https://github.com/banodoco/astrid-dev/pull/753) | Watching drafts; not completion submissions |

The local D9 bundle's complete production file `comfy_target.py` has Git blob `2cff478692805b9b4c114c6fc95a87daca17d830`; `tests/_local_speed_hashes.py` has blob `b2381716c3d5be99dcb6ec7e8f8648f59d61754c`. Both were checked against Agent #355 and match exactly. Publishing duplicate product changes would not advance the run.

The requested installed-wheel upload fix is already present in [Agent release/14/main lanes.yml](https://github.com/banodoco/astrid-agent/blob/release/14/main/.github/workflows/lanes.yml): `include-hidden-files: true`, plus a receipt-manifest guard. Preserve it through normal integration; do not add a competing fix or reopen old artifact archaeology. This is a release branch, not product main.

## Evidence available in this publication

- [Continuation proof index](evidence/continuation-20261116/proof-index.json), [Linux meter result](evidence/continuation-20261116/linux-meter-43918996289.json), [local checks](evidence/continuation-20261116/local-checks.txt), and [fingerprint benchmark](evidence/continuation-20261116/ls12-fingerprint-benchmark.json).
- [Focused comparisons and their limitations](evidence/tests/README.md), including the original per-test comparison files. These remain scoped evidence, not a whole-suite pass.
- [Floor scripts, original measurements and reproduction instructions](../../releases/14/evidence/ls1/README.md), plus the [real CPU summary](../../releases/14/evidence/ls1/real-cpu-20261116.json). Copying these files does not rerun the measurements.
- The original chat D9 bundle has SHA-256 `b53cc913ffb12cec9931ad7527638a019e37c4426440197ecf785689bb74dd31`; its patch has SHA-256 `997481bdf3dc33e51bb540993f786bd837ec94c4ce6cc0944f5f04aeed6b43cb`. Selected original raw proof is retained under `evidence/d9-chat-proof-20261116/` with its own manifest. These earlier logs must not be presented as a new hosted run or the latest product tuple.

The original 40-case local check was partial-source proof: 23 cancellation tests, 16 observer calibrations and one copied LS-6 reproduction. Its limitations are preserved in the command record. The later [affected-file hosted proof on Agent #355](https://github.com/banodoco/astrid-agent/pull/355#issuecomment-6921791393) is a different, more complete check; Windows was still failed there. Neither test-suite duration is generation-speed evidence.

## Boundaries

Only LS-11 retains its completed status. Code publication is not task completion; D9 still requires merged code and its focused/meter proof. No new dependency pin, Runtime change, product-main merge, paid action, tester engagement, GPU run, release publication, RS1 round or final R round is performed here. Do not reconstruct the ignored run configuration. Plan 54 remains queued.

This publication uses existing immutable Git objects for the carried-forward handoff and evidence, preserving their bytes. The current session verified the supplied bundle manifest and selected source identities; it did not rerun the earlier product tests. Local network access cannot retrieve the complete repository in this session, so no new local full-repository check is claimed. The notes PR must pass hosted repository checks before merging to main. That limitation is not a GPU gate and does not make other CPU work wait.

Routes used: Unknown — original bindings unavailable; bounded manager publication and provenance checking, not independent review.
