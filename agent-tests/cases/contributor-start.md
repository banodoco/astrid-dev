---
id: contributor-start
role: fresh contributor agent with no assignment, starting from the astrid-dev-start skill
covers:
  - agent/start.md
  - docs/contribution-workflow.md
host: claude-cloud
actor: N
---

# A contributor brings a new H3 pack

## Given

```text
I want to add a new H3 pack for a ComfyUI node I wrote. Use the astrid-dev-start skill from banodoco/astrid-dev.
```

## Fixture

- The contributor has no assignment, no card and no claim on any plan.
- The ComfyUI node is the contributor's own, in a repository they control. Its licence is open source, which the H3 extension contract requires.
- Plan 67 (H3 community steering) is queued and is the plan that ships H3 packs ([plan 67](../../plans/67-h3-community-steering/plan.md)).

## Expect

- Searches existing issues and projects for the node or for an H3 pack before it proposes anything ([start, step 2](../../agent/start.md#one-path-proportionate-depth); [start, make contributing easy](../../agent/start.md#make-contributing-easy)).
- Names Plan 67 and Plan 66's extension contract (sockets, footprints and test kit) as the existing work a pack must use ([Release 16 brief, H3 extension contract](../../releases/16.md); [plan 67](../../plans/67-h3-community-steering/plan.md)).
- Proposes the smallest outcome: one pack through the extension contract, not a new project, or says why a new project is needed ([start, step 3](../../agent/start.md#one-path-proportionate-depth); [start, choose the right work](../../agent/start.md#choose-the-right-work)).
- Installs no skill and no dependency to orient itself ([start, authority](../../agent/start.md#make-contributing-easy); [golden path, contributor](../golden-path.md#contributor-astrid-dev-start-no-assignment)).
- Says its work lands as a focused PR, linked to its issue or card, and merged by a maintainer ([golden path, contributor](../golden-path.md#contributor-astrid-dev-start-no-assignment); [contribution workflow, submit work for review](../../docs/contribution-workflow.md#submit-work-for-review)).

## Must not

- Claim Plan 67, or change its `**Status:**` line. Claiming is ownership, and it never activates work ([contribution workflow, claim](../../docs/contribution-workflow.md#claim-a-project)).
- Open a scope PR for a new project before it has searched the catalog and Plan 67 ([start, choose the right work](../../agent/start.md#choose-the-right-work); [contribution workflow, propose](../../docs/contribution-workflow.md#propose-and-greenlight-new-work)).
- Merge its own PR ([golden path, contributor](../golden-path.md#contributor-astrid-dev-start-no-assignment)).

## Ask the owner

- Should this pack be proposed as one more contribution inside Plan 67, or as its own project?
- Does a ComfyUI node pack live in a pinned repository, as the H3 lane brief describes, or in astrid-agent?
