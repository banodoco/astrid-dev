# Astrid's vision

**A tool to unlock the collective artistic ambition of the open-source community.**

Astrid helps individuals—and the community together—pursue artistic work beyond what they thought possible. This is the readable overview of the [vision](vision.md), its [four pillars](vision.md#four-pillars), [creator principles](principles.md) and [missing outcomes](gaps.md). Those documents hold the detail; this page should make the whole direction understandable without becoming a second source of truth.

## The four pillars

1. **[A Tool for Artistic Ambition](pillars/artistic-ambition.md).** Help artists make serious, original work with continuity, creative control and room to experiment—not just produce isolated generations. Agents should expand human judgment rather than replace it.
2. **[Agent-Powered Liquid Software](pillars/liquid-software.md).** Make the tools themselves adaptable while people create. Build on a small, reliable common foundation of media, timelines and actions, then compose opinionated tools from extensible packs, views and reusable capabilities. A creator or agent should be able to reshape the workspace and its behavior without losing state or control.
3. **[Intelligence That Compounds](pillars/compounding-intelligence.md).** Let creators and agents benefit from earlier work, with lessons tied to real evidence and the conditions under which they apply. Local and shared knowledge can reinforce each other without assuming that everything is public, correct or safe to execute.
4. **[A Shared Creative Endeavor](pillars/shared-endeavour.md).** Grow a community that challenges, mentors and inspires people to attempt more ambitious work. The aim is for people advancing the mission to own 100% of the company behind the collective; eligibility, allocation and legal structure are still to be designed.

The pillars reinforce one another: ambitious creative work requires adaptable tools; work produces knowledge; knowledge and a genuine collective raise what people can attempt next.

## The principles that drive us

These are the four cross-cutting [creator principles](principles.md), not additional pillars or contributor-process rules.

- **Local-first, cloud-capable:** work locally, including offline, or choose cloud agents, models, rendering and eventually a hosted workspace—with clear custody and cost choices.
- **Open by design:** keep software, models, tools and ideas inspectable, adaptable, forkable and shareable.
- **In the creator's control:** let creators shape even core behavior, permissions, providers and the boundaries of what stays private.
- **Eliminate needless technical wrangling:** let agents handle setup, dependencies and recovery so artists can concentrate on the work.

Pillars have their own pages because their ideas require depth. The four concise principles share [one page](principles.md); neither needs a manufactured folder hierarchy.

## What's missing, and how we make progress

**[Vision → Gaps → Plans → Evidence → Reassessment.](gaps.md)** A gap is a creator-facing result we cannot yet demonstrate, not a synonym for a project or a technology choice. Every gap has a desired state, an honest current assessment, and an independent closure test; the [gap index](gaps.md#current-gaps) links all current outcomes.

The gaps span ambitious sustained work; portable components and agent-shaped workspaces; learning and shared knowledge; creative challenges and ownership; and the cross-cutting foundations of reliability, permissions, generation, packs, local/cloud execution, hosted workspaces and safe sandboxes. A gap may advance several pillars and principles, but has one primary relationship. It stays open until the real evidence supports closure—even when a related project is finished.

The [plan catalog](../plans/index.md) is the **only** place for project priority, status, owner and estimate. Each project's `plan.md` explains its outcome, `inputs.md` preserves relevant source decisions and reuse, and `tasks.md` defines scoped work and proof. Plans link to the gaps they address. Gap records do not maintain reverse project queues.

## Improve the vision or build with us

Changes to vision, pillar detail, principles and gap evidence belong in their documents here. New or substantively changed gaps require the [first-principles boundary assessment](gaps.md#when-to-add-or-change-a-gap); evidence-only updates do not. Project scope, ownership and work use the existing [contribution workflow](../docs/contribution-workflow.md) and [agent entrypoint](../skills/astrid-dev/SKILL.md). Product API and implementation manuals stay with their product repositories. Small writing improvements need ordinary review, not a project.

The public [Astrid vision page](https://astrid.haus/vision) reads a generated versioned feed from these editorial sources. [Documentation CI](../.github/workflows/docs.yml) validates every PR and every `main` push, then publishes the feed after successful validation. The feed is a projection, **not** a second place to edit the vision. External evidence and gap assessments still require human judgment; a successful CI run cannot automatically prove or close a gap.
