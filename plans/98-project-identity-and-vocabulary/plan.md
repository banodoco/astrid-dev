# Optional Dev rename: plans to projects

**Project:** Optional Dev rename: plans to projects

**Goal:** If the owner chooses it, Astrid Dev's authored structure uses one word, project, in its paths and documents (`projects/<NN-slug>/project.md`), with the same numeric identities, working links and labels, and truthful history.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 3 engineering days (2–4), if the owner chooses to do it. After Plan 95, Dev's paths and ID policy are configuration, so the work is the move, its links, and the Dev consumers that still hard-code `plans/`, `plan.md` or `plan:NN`.

**Waiting on:** [Plan 95](../95-composable-agentic-workspaces/plan.md) landed (Dev on Otto with configurable paths); the owner's decision D2 whether to do this at all.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — removes the remaining plan/project double vocabulary from Astrid Dev's own structure; cosmetic for the product and for other Otto workspaces.

## Outcome and scope

On 24 November 2026 the owner cut this plan down. Its resolver and per-workspace ID and path policy moved to [Plan 95](../95-composable-agentic-workspaces/plan.md) (OT-7), which makes Dev's paths configuration. Marketing starts with its own paths and needs nothing from this plan. What remains is optional: a physical rename inside Astrid Dev only.

If chosen:

- `plans/<NN-slug>/plan.md` becomes `projects/<NN-slug>/project.md`, with `inputs.md`, `tasks.md` and supporting files moved alongside; `plans/index.md` and `plans/priority.md` move with them; the common template `templates/project/plan.md` becomes `project.md`; `otto.toml` changes to match.
- Numeric identities stay: Project 77 stays 77. No renumbering.
- Dev's own consumers move in the same candidate: checks, views and the public vision export (whose `githubUrl` values change; the schema and IDs do not); `auto_merge.py`'s allowed top-level folders; `claim_project.py`, `review_intake.py`, `issue_intake.py`, `release_issues.py` and `boards.py`; workflows and required check names; active skills and documents.
- History stays true. Old branch names, `plan:NN` labels, issue and release records and evidence keep their original text. Live links that would break point to a pinned revision. A narrow read-only alias (for example, `plan:NN` still resolving) is allowed where an active run or external link needs it; no alias becomes a second editable source.

**Not included:** renumbering, renaming historical branches or labels in bulk, changing release authority, rewriting receipts, any product-repository change, and any change in Otto or in Marketing.

## Existing work and decision

The earlier version of this plan carried a resolver, an identity contract and a Dev-wide migration on Otto's critical path, at 3–6 days. An independent direction review on 24 November found the rename unnecessary for Marketing once paths are configurable. The owner agreed: the resolver moves to Plan 95, and the rename becomes optional and later. The inventory of affected consumers recorded earlier is kept in [inputs](inputs.md#actual-coupling-and-alternatives).

## Sequence and readiness

After Plan 95 lands, the owner decides D2: do the rename, or keep `plans/` permanently (a cosmetic cost only). If chosen: inventory the consumers on the post-95 tree, move and relink in one candidate with its consumers, rehearse the cutover and rollback, then review. [Tasks](tasks.md). Recording this plan authorizes no run.

## Interfaces and handoff

**Consumes:** astrid-dev `main` after Plan 95, its `otto.toml`, the Otto tag it pins, and the App's public vision consumer contract (read-only).

**Produces:** the renamed authored structure, the updated Dev consumers, the list of allowed output deltas, and any narrow read-only aliases with their removal conditions.

## Completion

1. A new Dev project is authored, catalogued, checked and exported at `projects/<NN-slug>/project.md`, with the same identity rules and template as before. Every existing pack maps one-to-one; no status, owner, task or relationship changes.
2. The public vision JSON keeps schema version 1 and every ID; the only differences are the enumerated path and link values. The App's `vision-consumer-contract` passes.
3. Old links in history resolve at pinned revisions. Active branches, labels and published releases are unchanged. A rollback rehearsal on the candidate restores the previous tree and passes `check`.
4. If the owner declines D2, the plan is cancelled with that reason, and nothing else changes.
