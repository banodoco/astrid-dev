# Astrid Marketing organisation

**Project:** Astrid Marketing organisation

**Goal:** Astrid has a small independent Otto-powered marketing workspace in which people and agents can find ideas, create standard or loop projects, coordinate optional campaigns and improve their work from evidence.

**Status:** queued

**Owner:** Unassigned

**Estimate:** About 3.5 engineering days (3–4) after Otto v0.1.0, for the workspace and its two proof projects; excludes ongoing marketing work and waiting for audience response.

**Waiting on:** a tagged Otto v0.1.0 from [Plan 95](../95-composable-agentic-workspaces/plan.md) (its OT-23), not Plan 95's completion; owner decisions D2–D4, gathered by MK-0 at any time before; a named manager.

**Start:** [Astrid contributor skill](../../agent/start.md) and [domain map](../../agent/shared/domains.md). The six lines above are this project's row in the [catalog](../../plans/index.md): change them here, one line each; the catalog refreshes itself on `main` after merge. Its priority is its place in [priority.md](../../plans/priority.md); a plan not listed there comes after the listed ones.

**Vision role:** Foundational enabler — establishes a simple independently operated workspace for communicating and learning about Astrid; not a new product capability or gap closure.

## Outcome and scope

Keep the first operational workspace small: a strategy document, projects with tasks, GitHub issues (ideas, observations, questions, problems), optional campaigns, ordinary knowledge documents, and a Marketing overlay on Otto's guidance. It pins Otto by tag and uses Otto's `standard` and `loop` templates and slug identities. It is not a marketing schema or an analytics platform.

Layout: `README.md`, `otto.toml`, `strategy.md`, `projects/`, `campaigns/`, `knowledge/`, `pipelines/`, `agent/`, and `.github/ISSUE_TEMPLATE/` forms. Positioning, brand voice, audiences, competitors, content briefs, evidence and learnings are ordinary Markdown in `knowledge/` or inside projects, not record kinds. A campaign is an optional, locally defined collection of projects and issues serving one objective. It coordinates; the linked projects own status and task lists. A small campaign may simply be a project.

**Declared pipelines.** Two Otto pipeline files, checked by `otto check` on every PR:

- **`strategy`:** goal (from `strategy.md`) → project → campaign, with the campaign stage optional;
- **`intake`:** issue or idea → project.

The same project can sit in both pipelines with one owner, task list and evidence. Neither pipeline moves work; they say what a well-formed link is, and the check holds the workspace to it.

**Included:**

- The workspace itself: `otto.toml` (slug IDs, its own skill namespace), local record kinds and relations, the two pipelines, a project catalogue and a campaign view, issue forms, and CI running `otto check`.
- Strategy and product knowledge agreed with the owner. Product claims cite exact Dev releases or capabilities by link and revision, never a copy.
- **A Marketing guidance overlay,** following Otto's stand-up playbook. It links Otto's run-contract core, roles and workstreams, and adds only what is Marketing's own: creating, critiquing, campaign coordination and publication authority. It ships as local skills.
- **Scoped authority:** drafts by default; publishing, contact, spend, accounts and personal data each need the owner's or an authorized actor's separate approval of the exact item, channel and action. Merged Markdown and project status never grant authority. No private analytics, contact lists or secrets in Git.
- **Proof on real work:** one bounded standard project and one bounded loop project, chosen with the owner (D2), linked to a short campaign, plus one ungrouped project or idea routed through `intake`. The loop has a baseline, a comparable method, at least one round and a stop or next decision; it never claims a fabricated growth number. One source-linked learning informs the next action. Publication and audience metrics are optional; if a live action is withheld, the record says so.

**Not included:** automated publishing, outreach or spend; a scheduler; a campaign or asset database; analytics integration; funnel schemas; mandatory hierarchy; sync to Dev; proving sustained growth; any change to Otto or Dev (a missing primitive becomes an Otto issue).

## Existing work and decision

On 24 November 2026 the owner chose a separate Astrid Marketing workspace on Otto, kept to projects, tasks, issues, shared templates and optional campaigns, with several declared pipelines ([Plan 95 direction](../95-composable-agentic-workspaces/inputs.md#owner-direction-24-november-2026)). Plan 95 proves the framework on a synthetic Marketing fixture; this plan builds the real workspace, and starts from that fixture only as an example. The earlier proposal in [PR #1868](https://github.com/banodoco/astrid-dev/pull/1868) had a large record graph and a live-distribution gate; both are gone. See [inputs](inputs.md#planning-evidence).

## Sequence and readiness

MK-0 gathers the owner's decisions on sources, repository and permissions whenever convenient, before Otto is tagged if possible. Once Otto v0.1.0 is tagged: create the repository, design and configure the workspace with the stand-up playbook, write the overlay, then run the standard project, the loop project and the campaign, and finish with a fresh-agent trial and review. [Tasks](tasks.md). Recording this plan authorizes no repository, account or external action.

## Interfaces and handoff

**Consumes:** Otto at tag `v0.1.0` or a later patch tag: `otto.toml`, the pipeline and template contract, the `standard` and `loop` templates, the guidance skills and the stand-up playbook, and Plan 95's Marketing fixture as an example. Owner-approved brand and product sources. Verified Dev release references by revision.

**Produces:** the Astrid Marketing repository, pinned to an Otto tag; strategy and knowledge documents; two declared pipelines; a project catalogue and campaign view; the Marketing overlay and its skills; two small real projects and a campaign with their evidence; and a list of Otto issues found on the way.

## Completion

1. A new agent starting at the repository finds strategy, knowledge, issue intake, the project catalogue, templates, the overlay and the campaign, and creates a small standard project with tasks without writing code.
2. A real standard project and a real loop project share one structure and differ by template. The loop shows a baseline, a method, a round and a stop or next decision. Both can sit in one campaign without duplicated status or tasks; an ungrouped project is valid.
3. `otto check` passes on the workspace through the pinned Otto, and fails on a planted invalid link, unknown template, campaign including a goal, and a project with no goal in `strategy`. Marketing adds a skill and a template or pipeline without changing Otto or Dev.
4. No outbound action happens without its recorded approval. A missing approval is a safe hold, not a failed setup or an invented outcome. No personal data or secrets are in Git.
5. A recorded learning from the real projects informs a next action a fresh agent can take. One final review accepts the minimal organisation, the exact pin and the stated limits. Sustained growth is later Marketing work.
