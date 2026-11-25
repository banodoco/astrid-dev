# Inputs — Astrid Marketing organisation

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — On 24 November 2026 the owner chose an Otto-powered Marketing workspace kept to projects, tasks, issues, shared templates and optional campaigns, with declared `strategy` and `intake` pipelines, built on a tagged Otto release after Plan 95's framework work ([direction](../95-composable-agentic-workspaces/inputs.md#owner-direction-24-november-2026)). Next: the owner approves this scope by merging its scope PR, and answers D2–D4 (MK-0).

**Prior art:** [Plan 95](../95-composable-agentic-workspaces/plan.md) owns Otto, its pipeline and template contract, its guidance and a synthetic Marketing fixture. [Vision](../../vision/README.md), [strategy](../../strategy.md), [Plan 52](../52-issue-intake/plan.md), [Plan 77](../77-saving-holds-on-a-heavy-timeline/plan.md) and [Plan 89](../89-heavy-saves-in-seconds/plan.md) are sources and precedents, not procedure to copy. On astrid-dev `main` `0b1c9fd0e3bd063caa4b412e8bf3e90bf02ab2c4` no campaign, audience or channel concept exists; the project pack fits Marketing's project shape except Dev's vision lines and catalogue paths. A lookup of `banodoco/astrid-marketing` returned 404, which shows neither absence nor availability; no private strategy or analytics was inspected.

**Approach:** Use Otto's pinned framework, templates and guidance; add one campaign kind, two pipeline files, a few views, issue forms and a short overlay. Prove it on two small real projects and a campaign. Let real use create later kinds and integrations.

**Challenge:** The independent direction review of 24 November 2026 ([dispositions](../95-composable-agentic-workspaces/inputs.md#direction-review-and-dispositions)) found the earlier plan started too late and risked writing Marketing roles from scratch; both are addressed by waiting only on the tag and by the overlay. A separate review of this plan would add little before Otto's contract is reviewed (Plan 95 RS1); the final R covers it.

**Proof and limits:** Real bounded standard and loop projects, a short campaign, `otto check` with planted violations, and a fresh-agent trial. Setting up the workspace is not marketing success; no audience data, account permission or real project has been chosen yet. If publication is withheld, the record shows a held draft, not a live result.

**Review rounds:** Pending — Recommend one final R, and no review stop: Otto's contract is reviewed in Plan 95, and this plan's own risk is permissions, which the final review checks. Next: the owner confirms.

**Run start:** Pending — No run is authorized. Next: after Otto v0.1.0 and MK-0, the owner records the run, its accountable session, the repository go and the external-action limits.

### What changed

- **From PR #1868:** the large record graph (audiences, objectives, experiments, content, results) and the live distribution gate are gone. Those are documents within projects or knowledge until real demand shows otherwise.
- **From the first Otto revision:** this plan waits on a tag, not on Plan 95's completion; MK-0 gathers the owner's decisions early; MK-2 and MK-3 use declared pipelines; MK-4 overlays Otto's guidance instead of writing roles from scratch; Plan 95's fixture is Otto's test and this plan is the real workspace, so nothing is built twice. The estimate moved from 2–4 to about 3.5 days because the pipelines and overlay are now real work here.

Alternatives: clone Dev (wrong release, numbering and approval rules); an elaborate marketing platform (premature); an unstructured folder of drafts (loses project and idea context); a minimal Otto workspace with shared templates, two declared pipelines and an overlay (recommended).

## Owner decisions

- **D1 (decided, 24 November 2026):** a simple independent Astrid Marketing on Otto, with projects, tasks, issues, the `standard` and `loop` templates, optional campaigns, local skills and declared pipelines.
- **D2 (decided, 25 November 2026): scope, brand, voice and audience.** One project only: announcement videos for Reddit (`projects/reddit-announcement-videos/`), audience Reddit users. Brand and voice are taken from the Astrid video skill in `banodoco/poms_packs`: branch `pack/astrid-video-v0.12`, commit `0d25d41821e02d26314277813e947f2d926b8f31`, entry `astrid_video/docs/SKILL.md` and `astrid_video/docs/skills/directing-astrid-videos/SKILL.md` (visual language in `astrid_video/docs/references/visual-language.md`: "Sophisticated editorial design. Playful pixelated physics."). That skill states no product positioning, no tone guide and no announcement structure, and its own catalogue calls the pack a review candidate that is not admitted; the owner said to leave such fields empty rather than invent them. The workspace references that skill at the pinned commit; it does not copy it. No second project, no loop project and no campaign.
- **D3 (decided, 25 November 2026): repository.** `banodoco/astrid-marketing`, private, owned by the `banodoco` organisation, slug IDs; Otto is public, so a private workspace installs it by git tag without tokens. Product sources: Astrid's public repositories only. Creating the repository needs repository administration: the owner (or an organisation admin) creates it empty when card MK-1 asks.
- **D4 (decided, 25 November 2026): external permissions.** None. No publication, contact or spend; the video is a draft or review deliverable until the owner separately authorizes posting.
- **D5 (decided, 25 November 2026): review budget and manager.** No review budget is set; the manager arrangement is the same as every other run. No formal review stop: the owner accepts the deliverable (owner direction on 25 November 2026).

## Source identities

Planning snapshot: astrid-dev `main` `0b1c9fd0e3bd063caa4b412e8bf3e90bf02ab2c4` (24 November 2026). At MK-1, record the Otto tag and its commit, the new repository's URL and first commit, and the approved source revisions. No repository creation or external access is implied by this pack.

## References

[Plan 95](../95-composable-agentic-workspaces/plan.md) · [Plan 48](../48-one-record-model/plan.md) · [Plan 51](../51-astrid-dev-clean-up/plan.md) · [Planning skill](../../skills/shared/workstreams/astrid-dev-plan/SKILL.md) · [Run contract](../../skills/shared/run-contract.md) · [Design principles](../../docs/contribution-design-principles.md).
