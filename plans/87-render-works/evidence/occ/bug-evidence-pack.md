# Occurrence media swap evidence — 2026-11-22

## Result

Product fix committed and pushed; neither film swap was published. The installed Agent commit provider inside Runtime refused the film's unchanged word declaration. We stopped at that verified boundary, without changing the installation, restarting, modifying SQLite, or rendering.

- Branch: `release/14/fix-occurrence-media-swap`
- Worktree: `~/Developer/astrid-release-src/wt-r14-occurrence-swap`
- Exact stack base: `83d5f8fe382e2573deee39ffb6036cf2c834b1f7`
- Fix: `53833fd304f34160b348530609450a7b6921e503`
- Draft PR: https://github.com/banodoco/astrid-agent/pull/526
- Cause/timing comment: https://github.com/banodoco/astrid-dev/issues/1403#issuecomment-7081688027
- Admission/capture comment: https://github.com/banodoco/astrid-dev/issues/1404#issuecomment-7081688325
- Legacy/follow-up comment: https://github.com/banodoco/astrid-dev/issues/1405#issuecomment-7081688685

The requested target `release/14/main` has diverged from the stack pin (504 target commits versus 21 stack commits since merge base). The draft comparison includes inherited stack commits: 22 commits and 31 files overall. The implementation delta is the single fix commit above, eight files. Integration/base review remains required before merging.

## Cause and source changes

Agent occurrence codecs reject footage element types and require old catalog pins; asset changes also invalidate the timing dependency shape for otherwise unchanged legacy word declarations. Detached document patches do not by themselves admit newly referenced media, and combining patch/admission in one semantic step causes capture mismatch on successor internal revisions.

The shared `astrid/sdk/timeline/media_swap.py` captures guarded authored differences and explicit Runtime media admission, preserving the original detached provenance. `commit_session.py`, ordinary `cli_native.py --swap-asset`, and rendering's `timeline_document.py` use it. The timing validator retains the existing exemption only for unchanged fixed-duration visual timing, classifying media from the owning registry; audio, intrinsic duration, and timing changes retain their dependencies. Native occurrence media commands accept footage element replacements and retain legacy old entries. SDK preview capture/hydration is repaired.

New object identities must agree, media kinds must match, occupied aliases cannot be silently rebound, and new inputs are resolved against project objects or exact catalog selections. Runtime independently re-verifies those inputs. New occurrence word-anchor capture, full legacy same-alias/check-publish parity, and the digest-only legacy replace-parent-media adapter remain follow-up work on #1405.

## Enforcement boundary (verified)

Runtime source at `b2ea261f36f5f39c5f9964b02c8012c420e0b359`:

- `runtime_protocol/timeline_commit_provider.py:70-93` imports Agent's provider at daemon startup.
- `daemon.py:289-305` registers it.
- `timeline_commit_execution.py:549-556` invokes it for commit requests.

Thus Agent command, timing, and capture guards run in both the client and the Runtime-hosted provider. A worktree on the caller's import path cannot update the already-running provider. Neutral Runtime code additionally authenticates capture, project CAS custody/catalog selections, expected heads, and publication. Its existing interfaces support the new admission route; no neutral Runtime repository change was identified. Loading the updated Agent provider into Runtime is required to exercise word-anchored swaps on the live stack (deployment not performed).

## Tests and live probes (verified)

`tests-final-verified.log`: **146 passed, 14 deselected in 81.41s**, foreground exit zero; `git diff --check` passed. The deselections are repository integration lane exclusions. The focused files are listed in the PR. Coverage includes word-anchored am-footage image/video, pack footage, still holds, legacy entries without pins, exact outgoing scope, verification refusals, timing/audio dependencies, provider roundtrip, actual SDK capture/preview, CLI adapter routing, and detached document behavior.

The fixed wrapper `stackpy-fixed.sh` uses the stack Python/environment with the source worktree first on the import path and a private outbox. `sdk-sandbox-preview.py` exercised actual `Clip.swap_asset` against the running stack: accepted preview, only one clip asset field and one new registry entry, `doc.patch` and `media.admit` in separate semantic steps. Evidence: `sdk-sandbox-request.json`, `sdk-sandbox-result.json`, `sdk-sandbox-preview-3.log`. The live sandbox clip had literal timing; live word-anchored sandbox success was not established. Word-anchored behavior is covered by the fixed-provider tests.

## Film state and outgoing scope (verified)

Project `801a01b3a87941a1ab25958c488afdbf`; timeline `77f906f3242c48179ab86ca7c3e62eb4`.

`prepare.py` matched imported media against file digests and compared authored fields. The cream T2 source used the corrected recorded import in `cream/t2-corrected-import.json`; the older prepared digest did not match the current requested file. No film imports were performed by this run.

- Hair: **not done**. Prepared and preview head `authoring-parent-revision-18e0ce9a688d9b132af999d922dbc91202ed3f289f01a76d43ee8d9e8fe0ecd6` → same readback head. Outgoing request listed only asset fields of `c28-seq0-00` through `-03`, plus four new R6-RW registry entries (8 authored patch fields). `-04`/`-05` retained RW3-04. Actual publications: zero.
- Cream: **not done**. Prepared at `authoring-parent-revision-4790999801251fdcc139889343b30d12d0e7ff4d2194d56678061dfc5bbe5c58`; readback at the above `18e0ce…` head after other-agent changes. No cream request was sent following the hair refusal. Prepared outgoing listed only the seven target asset fields plus five new R6-TOUR registry entries (12 authored patch fields). Actual publications: zero.

Hair's expected-head dry run returned `validation_error / invalid_document`: `candidate.timing: missing exact word binding for ('occ-77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66-occ', '77f906f3242c48179ab86ca7c3e62eb4-55940497dcea0a1f1f66', 'c28-seq0-00').on`. Base=current, no conflicts. See `hair-runtime-preview.json` and private `hair-runtime-preview.outbox.json`. Stale-head attempts were re-read/reprepared before sending.

`readback-diff.json`: all eleven target clips exactly equal to their pre-swap authored dumps, including frame timing. `revisions.log` records both sets, outgoing paths, heads, and zero publications. This run did not touch the other agent's 10.5–16.4s clips.

## Editor verification (verified unchanged state)

`verify/current-capture-evidence.json` records read-only real-editor PlayerRef frame seeks at 77.5, 77.9, 78.3, 78.7, 79.1, 105, 109.5, 116, 123, 130, and 137 seconds. Timeline/project mutations were blocked; only read-only inspect and operational handshake POSTs were allowed. No timeline render was used.

All eleven PNGs in `verify/current-*.png` are pixel-identical to `land/verify/current-*.png`; the contact sheet was visually inspected. They show the existing pictures and framing, not the requested replacements. The old UI has a black preview area at 116s already present in the baseline. These stills prove unchanged state, not successful swaps or new-media playback. See `verify/contact-sheet.jpg` and `verify/run.log`.

Routes used: X coordination, implementation and review; N bounded parallel investigation, adapter work, focused checks and editor captures. No credentials are included in this evidence pack.
