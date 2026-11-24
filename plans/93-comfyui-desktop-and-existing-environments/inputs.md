# Inputs — ComfyUI Desktop and existing environments

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — Owner, 24 November 2026, planning chat: asked whether the next phase covers ComfyUI Desktop and getting it working, then requested “could you add both of these to release? It's release number 16”. Recorded release intent: include existing-ComfyUI/Desktop support and broader environment setup/recovery. Proposed split: this plan owns already-existing user environments; [Plan 94](../94-dependable-environment-setup-and-recovery/plan.md) owns provisioning/fallback and full recovery journey. The split and exact support/launch boundary remain for scope review; no execution go. Next: the independent scope critique, then the owner confirms the split and the open decisions.

**Prior art:** [Plan 20 phase 4](../20-zero-to-first-image/plan.md#phase-4-local-first) excludes Desktop discovery and stopped ComfyUI adoption. [P4.9 re-walk](../20-zero-to-first-image/evidence/walk-2r.md) used a fake and simulated downloads; its real first-image proof was delegated to [Plan 34](../34-real-gpu-proof/plan.md). [Plan 32](../32-generation-placement-targets/plan.md) supplies one execution path and Runtime-owned placement. Source at tested Agent `a09ea669a35a104451e48679e242aeb390a4df58`: [setup skill](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/packs/setup/docs/SKILL.md#L148-L214), [scan](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/packs/vibecomfy/local.py#L434-L465), [target records](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/core/generation/targets.py#L25-L57), [launch preparation and execution](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/core/generation/target_launch.py#L257-L368), [Linux-only native observer](https://github.com/banodoco/astrid-agent/blob/a09ea669a35a104451e48679e242aeb390a4df58/astrid/core/generation/target_launch.py#L115-L123). These boundaries remained in inspected R15 Agent head `514499debc902643a03aee3f0ed68b710c5d3ead`. The public [exploratory Windows report #1848](https://github.com/banodoco/astrid-dev/issues/1848) and [frozen exploratory handoff](https://github.com/banodoco/astrid-dev/blob/501e34de4503994b75c602ede6108a8e69a1c4e0/releases/15/tester-run/exploratory-build-a09ea669.md) now document the exact exploratory tuple and scope: Desktop 0.7.2 was still registered but both recorded executable and data directory were missing; scan returned no servers and no errors. Isolated Portable 0.46.0 succeeded with a real GPU; this is not Desktop qualification. The handoff explicitly permits this exploratory snapshot in place of the normal qualified tester bundle, without changing the other consent rules. No Release Lead qualification or matching R15 editor success is claimed. Raw diagnostics and images remain with the tester.

**Approach:** Extend existing discovery and target facts, use supported third-party launch/repair and the existing generation path. A docs-only fix cannot distinguish a broken Desktop from no installation. A new separate engine manager/registry duplicates ownership; auto-launch via guessed paths is unsafe. Prefer a verified human-start instruction before implementing automatic native launch; if automation is necessary, reuse target-launch and Plan 38 rather than weakening custody.

**Challenge:** Pending — mandatory independent high-judgment critique of the written plan/tasks against actual code because this changes a user-facing flow and lifecycle/consent. Next: critique reuse, smallest supported layout matrix, Plan 38 overlap and the independent boundary with Plan 94. No independent advisor was available in the planning chat. Do not treat this draft as greenlit.

**Proof and limits:** Real Desktop generation and gallery/editor result, exact versions, plus negative cases in plan.md; CPU fixtures prove classification and refusal, not hardware or third-party repair. The report did not establish Desktop success or approved release qualification.

**Review rounds:** Pending — recommend one final independent review plus one early review stop if a native launch/ownership contract is changed, because a late safety finding would invalidate downstream setup. Next: owner confirms.

**Run start:** Pending — no implementation run authorized. Next: name accountable manager, exact scope, permitted machines/cost, destination and advisor, with explicit consent for live hardware.

## Owner decisions

- D1 — Release 16 assignment requested by owner on 24 Nov 2026; recorded in the release brief. This is scope intent, not go to execute or publish.
- D2 — Pending: support Windows Desktop as a first-class proven attached layout; recommend require real Desktop proof, not substitute Portable. Decide other OS/layout qualification breadth after inventory, with honest unsupported labels.
- D3 — Pending: human-led official start/repair versus verified agent launch. Recommend supported manual path first, auto-launch only where exact native ownership can be verified and the owner approves; never replace the user's installation without consent.
- D4 — Pending: accept two separately useful scopes (existing attachment vs provisioning) or combine them if independent critique finds no useful separation.

## Source identities

Planning snapshots: astrid-dev main `c0732aa66252bc097f6cdcdeff4d6bf20f78ec7a`; tester Agent `a09ea669a35a104451e48679e242aeb390a4df58`, App `d53685f3adfc4ed725936b4a9d7ebc435dedbcc0`, Runtime `24e2c9291d5bcaface78324696286f2dc896debc`, VibeComfy `c0e910caab9734a551fb2c1a455fff72c3a1b1cb`. Historical, not future work bases. Intended branches `release/16/plan-93` in Agent and App if needed, from each actual `release/16/main` once cut. Before dispatch run the planning skill's overlap check for Plan 38, Plan 56, Plan 94 and other overlapping active plans; wait/stack/disjoint decision is pending exact branch evidence. No product branches cut here.

## References

[#677](https://github.com/banodoco/astrid-dev/issues/677) discovery/launch leads; [#725](https://github.com/banodoco/astrid-dev/issues/725) onboarding; [#733](https://github.com/banodoco/astrid-dev/issues/733), [#1380](https://github.com/banodoco/astrid-dev/issues/1380), [#683](https://github.com/banodoco/astrid-dev/issues/683) diagnostics; [#816](https://github.com/banodoco/astrid-dev/issues/816) capability readiness. [Release 16](../../releases/16.md); [Plan 20](../20-zero-to-first-image/plan.md); [Plan 56](../56-workflow-setup/plan.md); [Plan 38](../38-one-process-identity/plan.md).
