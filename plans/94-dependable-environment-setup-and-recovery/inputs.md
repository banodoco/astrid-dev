# Inputs — Dependable environment setup and recovery

> **Draft reconciliation:** The dated Release 16 proposal below supersedes conflicting historical scope or dependency wording for review only. Existing statuses, decisions and delivery authority remain the historical record until the owner accepts a change.

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 24 November 2026 the owner asked for broader environment setup and recovery, and for this plan and [Plan 93](../93-comfyui-desktop-and-existing-environments/plan.md) to be in Release 16 (in the planning chat behind astrid-dev #1847, then in session https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV). On 25 November she asked for both plans to deliver one end state: one honest state, one next step and one consent, with the agent never improvising. plan.md describes this plan's branch of it. That is release intent, not a go to implement. Next: the owner confirms the split and D2–D6.

**Prior art:** the tester report [#1848](https://github.com/banodoco/astrid-dev/issues/1848) and its [frozen handoff](https://github.com/banodoco/astrid-dev/blob/501e34de4503994b75c602ede6108a8e69a1c4e0/releases/15/tester-run/exploratory-build-a09ea669.md), 24 November: Windows 11, RTX 5070 Ti Laptop.
- **Install:** the candidate installed in 622.5 s, including 219 s of silence.
- **Desktop:** its registration was stale.
- **GPU:** the system PyTorch listed the GPU but failed a real CUDA calculation.
- **The image:** isolated official Portable succeeded. An outside downloader fetched 17.28 GB, which Astrid verified. Astrid's own transfer and resume were skipped, not failed.
- **Other findings:** receipts recorded zero duration, and the published editor refused the new schema and recommended an impossible update.
- **Limits:** the App SHA in that tuple supplied only the installer and manifest, and no matching editor was tested.

At Agent `b934555c`:
- `astrid/core/generation/engine_runner.py:336`: the runner refuses Windows;
- `astrid/core/generation/engine_local_endpoint.py:94`: the endpoint root is POSIX-only;
- `astrid/core/generation/gpu_environment.py:174-224,272-297`: the candidate provisioner needs admitted source checkouts, checks availability and versions rather than a computation, and refuses any existing destination;
- `astrid/core/generation/asset_gaps.py:415-428,461-475` and `asset_alignment.py:191-200`: planning writes temporary hard-link probes before the space check, which budgets model bytes plus a margin;
- VibeComfy `vibecomfy/fetch.py:635-641` at `2e1b603f`: the staging file can coexist with the resume file.

[Plan 20](../20-zero-to-first-image/plan.md#phase-4-local-first) shipped the setup flow, [Plan 32](../32-generation-placement-targets/plan.md) placement and [Plan 34](../34-real-gpu-proof/plan.md) the GPU evidence format.

**Approach:** extend Plan 93's readiness ladder with one branch, an install offered as the next action when nothing usable is left, plus the `computes` rung and Astrid's own download as a resumable task. The route is chosen once at ER-0 (D3).

Rejected:
- **Docs only:** they can't install or recover.
- **Two routes:** that doubles the work for one outcome.
- **A new engine manager or installer:** it duplicates what exists.
- **Re-qualifying Desktop here:** Plan 93 owns it.
- **A Runtime download task now:** D5.

**Challenge:** Reviewed — an independent Astra review with three Luna helpers checked the draft against the code ([critique](./evidence/critique.md)). Accepted:
- **No greenlight as written;** the plan is narrowed to one isolated fallback, one supported combination, and recovery after interruption.
- **"Interrupted setup resumes" overstated the proof,** because ER-3 interrupted only a model download. ER-2 now covers an install interrupted after its files are written, and fixes the provisioner's blanket refusal.
- **The "disk shortage before writing" claim** is now ER-4's: count the peak space and check before the probes.
- **Desktop requalification is removed** from the live loop; Plan 94 consumes Plan 93's disposition.
- **ER-0 recommends the route.** ER-1 has a pinned matching build, an approved host and a resettable fixture.
- **The setup-skill change has its own card** (ER-5).
- **Test paths are corrected** to `tests/core/generation/`.
- **Routes:** ER-2 is `S` for its new write and consent boundary, the repeatable checks are `N`, and RS1 and R are the high-judgment role's.
- **Each round has two cold journeys,** each followed by a warm image.
- **The tester's other findings** go to their owners, off the critical path.

The critique estimated only the inventory and baseline (1–2 days); the rest is estimated after ER-1.

**Proof and limits:** plan.md's [Completion](plan.md#completion), two consecutive live rounds on the declared Windows NVIDIA combination through the installed CLI and the matching editor, plus the focused tests. CPU fixtures prove classification, refusal and resume logic only. Wall-time differences in #1848 are unattributed and aren't a performance finding.

**Review rounds:** Pending — recommend RS1 at most 1 on the install's write and consent boundary, and R at most 1. Next: the owner confirms (D6).

**Run start:** Pending — no implementation, hardware use or real download is authorized. Next: the owner names the accountable orchestrator, confirms the user test request's limits and zero paid spend (D4) and the base (D6); then record the date and limits here.

## Owner decisions

Each is a recommendation until the owner confirms it in writing.

| # | Decision | Recommendation |
| --- | --- | --- |
| D1 | Release | **Decided (owner, 24 November 2026):** Release 16. This is release intent, not a go to implement. |
| D2 | The end state and the split | Plan 93 owns the ladder and existing installs, including Desktop's witness. This plan owns the install offered when nothing usable is left, the `computes` rung, and Astrid's own download as a resumable task. The ten statements in plan.md hold for the declared combination only. |
| D3 | The install route | Official ComfyUI Portable into an isolated destination, started the supported way, unless ER-0 shows finishing Astrid's Windows recipe is smaller. One route only. |
| D4 | The support matrix and limits | Qualify the tested Windows 11 / RTX 5070 Ti Laptop combination first, labelling everything else unqualified. A tester through [user test request #1952](https://github.com/banodoco/astrid-dev/issues/1952), with its proposed destination, disk reserve (40 GB), download (25 GB) and time (about 3 hours per round) limits, and zero paid spend, as the owner confirms. |
| D5 | A Runtime download task | Not now. Use the existing verified, resumable download, and decide from the live loop's evidence, keeping #722's and Plan 90's ownership. |
| D6 | Reviews and the base | RS1 at most 1 and R at most 1. The base: `release/16/main` once it is cut, or an owner-approved early start on `release/15/main`, with the SHA recorded. |

## Source identities

- **Planning reads:** astrid-dev `main` `80a55701`; Agent `release/15/main` `b934555c`; VibeComfy `2e1b603f`.
- **The tester's tuple:** Agent `a09ea669a35a104451e48679e242aeb390a4df58`, App `d53685f3adfc4ed725936b4a9d7ebc435dedbcc0`, Runtime `24e2c9291d5bcaface78324696286f2dc896debc` and VibeComfy `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`. These are historical, not bases.
- **Destination:** `release/16/plan-94` in astrid-agent, and in astrid-app only if ER-5 needs it, cut from the D6 base. Before dispatch, run the planning skill's overlap check for Plans 09, 29, 30, 38, 56, 90 and 93, and record wait, stack or disjoint and the producer pins. No branch is cut yet.

## References

- [#1848](https://github.com/banodoco/astrid-dev/issues/1848): the tester report.
- [#722](https://github.com/banodoco/astrid-dev/issues/722), [#721](https://github.com/banodoco/astrid-dev/issues/721), [#1213](https://github.com/banodoco/astrid-dev/issues/1213): verified download.
- [#727](https://github.com/banodoco/astrid-dev/issues/727), [#580](https://github.com/banodoco/astrid-dev/issues/580): design rules.
- [#816](https://github.com/banodoco/astrid-dev/issues/816), [#1729](https://github.com/banodoco/astrid-dev/issues/1729), [#683](https://github.com/banodoco/astrid-dev/issues/683): readiness and diagnostics.
- [#1206](https://github.com/banodoco/astrid-dev/issues/1206): compatibility.
- [Release 16](../../releases/16.md); [Release 17](../../releases/17.md); [Plan 20](../20-zero-to-first-image/plan.md); [Plan 32](../32-generation-placement-targets/plan.md); [Plan 34](../34-real-gpu-proof/plan.md); [Plan 56](../56-workflow-setup/plan.md); [Plan 90](../90-workflow-setup-exact-plan/plan.md).

## Proposed Release 16 reconciliation — 25 November 2026

Draft pending independent review and owner scope agreement; preserve existing task progress and accepted decisions. Source: [SYN-01 original](https://github.com/banodoco/astrid-dev/blob/4259785be40565ba940ecb076ca8c9889742d7cf/releases/16/evidence/scoping/SYN-01.md).

ER-0/D3 compares Windows Portable and recipe by actual work/provenance/custody/rollback; select one. D4 adopts physical compute cells and full journey subset in §7. D5 defaults to existing foreground resumable operation, not a new Runtime scheduler absent evidence. Require per-volume peak additional bytes including archive/extraction/wheels/model partial+stage coexistence, previous working version, concurrent reservations and cleanup reserve. Unknown peak cannot be represented as a safe exact cap. A revised plan that increases source/root/cost/write scope requires renewed approval.
