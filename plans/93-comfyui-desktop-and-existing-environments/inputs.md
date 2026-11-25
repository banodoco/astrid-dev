# Inputs — ComfyUI Desktop and existing environments

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — on 24 November 2026 the owner asked for ComfyUI Desktop support and for this plan and [Plan 94](../94-dependable-environment-setup-and-recovery/plan.md) to be in Release 16 (in the planning chat behind astrid-dev #1847, then in session https://claude.ai/code/session_011EzfW1C63rxLXsL6TkHHVV). On 25 November she asked for both plans to deliver one end state, which is the one plan.md now describes: one honest state, one next step and one consent, so neither the person nor the agent improvises. That is release intent, not a go to implement. Next: the owner confirms the split and D2–D5.

**Prior art:** [Plan 20 phase 4](../20-zero-to-first-image/plan.md#phase-4-local-first) shipped the first-image flow and excluded Desktop discovery and stopped installs. [Plan 32](../32-generation-placement-targets/plan.md) owns placement and the generation path, and [Plan 34](../34-real-gpu-proof/plan.md) the GPU evidence format. At Agent `b934555c`:
- `astrid/core/generation/preflight.py:90-99`: `readiness_envelope` reads `ready` whenever no issue was raised;
- `astrid/sdk/generation.py:1335`: `targets` "inspect[s] selection without probing";
- `astrid/packs/vibecomfy/local.py:282`: ordinary scan ports skip the ComfyUI-shape check;
- `astrid/core/generation/targets.py:27`: the record already names the `desktop`, `git`, `portable` and `pinokio` layouts;
- `astrid/core/generation/target_launch.py:115,273`: the native launch observer is Linux-only, and launch expects a Python `main.py`.

The VibeComfy guide already handles denied loopback access, changed ports and several servers. The tester report [#1848](https://github.com/banodoco/astrid-dev/issues/1848) and its [frozen handoff](https://github.com/banodoco/astrid-dev/blob/501e34de4503994b75c602ede6108a8e69a1c4e0/releases/15/tester-run/exploratory-build-a09ea669.md) found Desktop 0.7.2 registered with its executable and data folder gone. The scan returned no servers and no errors, and the image came from isolated Portable 0.46.0, which is not Desktop qualification.

**Approach:** extend the existing readiness envelope and `generate targets` into the readiness ladder, add the existing-install rungs, and give each state one next action, with the person opening Desktop themselves.

Rejected:
- **Docs only:** they can't tell a broken Desktop from none.
- **A separate environment registry or manager:** it duplicates ownership.
- **Astrid launching Desktop natively:** the launch boundary is Linux-only and expects a Python `main.py`, Desktop owns its own lifecycle, and asking the person to open it is safer and smaller (D3).
- **Broad discovery of stopped layouts:** only Desktop is qualified first.

**Challenge:** Reviewed — an independent Astra review with three Luna helpers checked the draft against the code ([critique](./evidence/critique.md)). Accepted:
- **No greenlight as written;** the plan is narrowed to one supported Desktop journey: find it, tell the person to open it, re-probe, and deliver an image.
- **The native launch card and its review stop are cut** (D3).
- **`generate targets` emitting `ready` with no observations,** and the missing ComfyUI-shape check, are CD-1's and CD-2's.
- **The responder is tied to the install,** for another server on the old port.
- **The handoff with Plan 94 is re-cut:** Plan 93's disposition is consumed, and Plan 94 doesn't re-qualify Desktop.
- **The consented Windows baseline moves into CD-0.**
- **The scan's `servers`/`errors` contract** is kept, under the whole-response tests.
- **Functional skill wiring sits in CD-3;** Route T (CD-4) is wording only.
- **CD-5 ties the Desktop job to its image** and keeps an unrelated job alive.

The estimate follows the critique's 4–6 days, plus the ladder contract, which Plan 94 also uses.

**Proof and limits:** plan.md's [Completion](plan.md#completion), on one declared Windows NVIDIA machine and Desktop version, through the installed CLI and the matching editor. CPU fixtures prove classification and refusal only. Running Portable, Git and Pinokio installs are regression checks, not qualification.

**Review rounds:** Pending — recommend RS1 at most 1 on the ladder, because CD-2 to CD-5 and Plan 94 build on it, and R at most 1. Next: the owner confirms (D4).

**Run start:** Pending — no implementation is authorized. Next: the owner names the accountable orchestrator, confirms the user test request's limits and the matching build (D2, D5), and the base; then record the date and limits here.

## Owner decisions

Each is a recommendation until the owner confirms it in writing.

| # | Decision | Recommendation |
| --- | --- | --- |
| D1 | Release | **Decided (owner, 24 November 2026):** Release 16. This is release intent, not a go to implement. |
| D2 | What is qualified | One Windows NVIDIA machine and one ComfyUI Desktop version, proved with a real image. Running Portable, Git and Pinokio stay regression checks; anything else is labelled unqualified. |
| D3 | Who starts ComfyUI Desktop | The person, when Astrid asks. Astrid never launches, restarts, updates or replaces Desktop or Pinokio. Native launch is cut from this plan; revisit only if the witness shows asking is not enough. |
| D4 | The split and the reviews | Keep two plans with the handoff in plan.md: this plan defines the ladder and owns existing installs, and Plan 94 owns the separate install when nothing usable is left. One review stop on the ladder, and one final review. |
| D5 | The base and the tester | `release/16/main` once it is cut, or an owner-approved early start on `release/15/main`, with the SHA recorded. A tester through [user test request #1952](https://github.com/banodoco/astrid-dev/issues/1952), within its Limits and consent, which the owner confirms; no lane tests on the owner's machine. |

## Source identities

- **Planning reads:** astrid-dev `main` `80a55701`; Agent `release/15/main` `b934555c`; VibeComfy `2e1b603f`.
- **The tester's tuple** (#1848): Agent `a09ea669a35a104451e48679e242aeb390a4df58`, App `d53685f3adfc4ed725936b4a9d7ebc435dedbcc0`, Runtime `24e2c9291d5bcaface78324696286f2dc896debc` and VibeComfy `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`. These are historical, not bases.
- **Destination:** `release/16/plan-93` in astrid-agent, and in astrid-app only for CD-4, cut from the D5 base. Before dispatch, run the planning skill's overlap check for Plans 38, 56, 90 and 94, and record wait, stack or disjoint for each. No branch is cut yet.

## References

- [#677](https://github.com/banodoco/astrid-dev/issues/677): discovery and launch leads.
- [#725](https://github.com/banodoco/astrid-dev/issues/725): onboarding.
- [#733](https://github.com/banodoco/astrid-dev/issues/733), [#1380](https://github.com/banodoco/astrid-dev/issues/1380), [#683](https://github.com/banodoco/astrid-dev/issues/683): diagnostics.
- [#816](https://github.com/banodoco/astrid-dev/issues/816): capability readiness.
- [Release 16](../../releases/16.md); [Plan 20](../20-zero-to-first-image/plan.md); [Plan 56](../56-workflow-setup/plan.md); [Plan 38](../38-one-process-identity/plan.md).
