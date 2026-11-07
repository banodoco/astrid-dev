# Astrid — A tool to unlock the collective artistic ambition of the open-source community

<!-- Ambition and participation live here; pillar, principle and gap summaries are derived from their own documents. -->

## Ambition

Astrid aims to help individuals and the community as a whole pursue artistic work beyond what they thought possible.

The collective inspires ambitious work; adaptable tools and shared knowledge help realize it; results raise the bar and improve the foundation for everyone. The stated goal is **100% ownership of the company behind the collective by those advancing its mission**. The actual allocation and legal structure remain to be designed.

The information on this page is pulled from the Astrid Dev repository. If you'd like to contribute, visit [the contribution guide](https://github.com/banodoco/astrid-dev#want-to-contribute-give-this-to-your-agent).

## Four pillars

### [A Tool for Artistic Ambition](pillars/artistic-ambition.md)

We want to make it easier for artists to push their work—and themselves—toward more ambitious projects.

**Give people the creative power and control to make work beyond what they previously thought possible.**

### [Agent-Powered Liquid Software](pillars/liquid-software.md)

In the age of agents, we believe every layer of software should adapt to the needs of the artist and the work.

**Tools should adapt to creative work as people and agents create, not force the work into fixed interfaces.**

### [Intelligence That Compounds](pillars/compounding-intelligence.md)

We want everything artists and their agents learn to help others push their work further.

**Creative agents should benefit from what they and others have learned—and help make that knowledge more useful over time.**

### [A Shared Creative Endeavor](pillars/shared-endeavour.md)

We want to build a culture of people pushing AI—and themselves—beyond their creative limits.

**Give people a reason, encouragement and a genuine stake in attempting more ambitious creative work.**

## Four creator principles

### [Local-first, cloud-capable](principles/local-first-cloud-capable.md)

Create on your own machine, including offline, with your files and projects under your control. When you need more power or convenience, choose cloud models, agents, rendering or a fully hosted workspace. Moving between local and cloud should feel natural, with clear choices about where work runs, where files live and what it costs.

### [Open by design](principles/open-by-design.md)

Everything about our tools, models and even ideas should be open to inspect, adapt, fork and share. We build on open-source software and open models so artists and developers can build on one another's work, contribute their own tools and knowledge, and choose the providers that suit them.

### [In the creator's control](principles/in-the-creators-control.md)

Everything about Astrid is designed to give creators control. They can change even its core workings, choose which features and services to opt into, set agent permissions, and decide what data stays private or gets shared. We present all those choices as simply and clearly as possible.

### [Eliminate needless technical wrangling](principles/eliminate-needless-technical-wrangling.md)

Artists should spend their time creating, not installing models or troubleshooting environments. Agents should handle choosing and setting up tools, managing dependencies, running jobs and recovering from errors. Technical choices, permissions and costs should be easy to understand without becoming the focus of the creative experience.

## Gaps — 15 assessed outcomes

Each gap describes a result that remains independently verifiable even if its proposed implementation changes. Follow its link for the full current assessment, sources and closure evidence. Project completion never closes a gap automatically.

- **[AA-001 — Artists can't yet sustain ambitious work end to end](gaps/AA-001-sustained-creative-work.md)** — Open. A real artist-led project is completed through repeated revision, with demonstrable continuity, editable results, preserved creative intent and serious creator/peer assessment.
- **[CA-001 — Astrid lacks its own creative challenge culture](gaps/CA-001-creative-challenge-culture.md)** — Open. Run a bounded challenge with clear artistic intent and fair participation; document artists' goals, feedback, completed work and whether it enabled more ambitious efforts.
- **[CA-002 — No implemented contributor-ownership model](gaps/CA-002-contributor-ownership.md)** — Open. An explicit owner decision and qualified legal/tax review of a concrete model covering eligible contributions, grants/allocations, governance, vesting, changes over time, financing and participant protections; then evidence of its authorized implementation.
- **[CI-001 — Agents don't yet reliably learn from creative work](gaps/CI-001-agent-learning-loop.md)** — Open. Two real agent sessions: the first retrieves applicable knowledge and produces an observed, locally retained result; a subsequent session demonstrably uses that finding.
- **[CI-002 — Independent Hiveminds don't yet work together](gaps/CI-002-federated-knowledge.md)** — Open. Two separately owned datasets can exchange a scoped, independently attributed reference or approved sanitized result, preserving revision identity, provenance and access decisions; denied, stale and revoked cases do not leak source content.
- **[F-001 — Reliability isn't proven across supported setups](gaps/F-001-platform-reliability.md)** — Partially evidenced. A declared and version-pinned OS/device/deployment matrix demonstrates clean installation, launch, stop, update, interruption recovery, rollback and removal with preserved work and meaningful negative tests.
- **[F-002 — User control and recovery aren't fully proven](gaps/F-002-safe-user-control.md)** — Open. Representative real workflows show clear and enforceable grant/deny/revoke permissions, correctly scoped file/network/spend access, handling of concurrent edits, inspectable changes, refusal and undo/recovery after failed or conflicting operations.
- **[F-003 — Creative execution isn't yet dependable end to end](gaps/F-003-creative-execution.md)** — Open. On a stated supported setup, run real creative generation or processing and inspect the resulting editable artifact for correct content, project identity, output settings and usable timeline/workspace integration.
- **[F-004 — Pack installation and upgrades aren't yet reliable](gaps/F-004-pack-lifecycle.md)** — Open. Install a supported pack, discover its declared actions/UI, use it on project data, update and roll back safely with exact pinned source identity; show missing dependencies, rejected/untrusted cases, recovery and no loss of project references.
- **[F-005 — Local-first projects can't yet use cloud execution seamlessly](gaps/F-005-local-files-cloud-assist.md)** — Open. With one approved provider/configuration and a declared local project, a user or their agent launches remote work (including image generation and a video render), watches status and costs, cancels/retries as appropriate, and receives correctly linked editable local artifacts with the **local database still authoritative**.
- **[F-006 — Creators can't yet work in Astrid entirely from the cloud](gaps/F-006-fully-hosted-workspace.md)** — Open. A new user can open a hosted Astrid workspace in a browser, create a project, save and reopen across sessions/devices, run a generation and render, and observe durable, permission-scoped data; accounts are isolated.
- **[F-007 — Running Astrid in a sandbox isn't yet a first-class option](gaps/F-007-first-class-sandbox.md)** — Open. On a declared supported platform, a user can choose the sandbox mode, start the required stack, perform an approved creative job, stop and restart, and recover their project.
- **[LS-001 — Creative components can't yet move freely](gaps/LS-001-portable-components.md)** — Open. Rearrange the **real** player, inspector and timeline; retain playback, editing, selection and recovery state; save/restore the layout.
- **[LS-002 — Agents can't yet reconfigure the workspace](gaps/LS-002-agent-workspace-control.md)** — Open. An agent arranges the same real components as a user, binds the correct timeline/selection/clock, offers reversible operations, does not clobber user edits, and restores a prior workspace from a saved representation.
- **[LS-003 — Frontend and backend extensions don't yet compose](gaps/LS-003-full-stack-contributions.md)** — Open. An installed/trusted music capability yields a typed beat-grid result used in a real timeline view and music control surface.

## Projects and participation

The [project catalog](../plans/index.md) owns current priority, status and accountability; project packs contain their own scope, sources, tasks and proof. [How to contribute](../docs/contribution-workflow.md) covers issues, claims, scope review, PRs, writing and completion. Individual gap records hold their own evidence and closure criteria.

## Build Astrid with us

You and your agents can contribute to Astrid's tools, knowledge and creative community. We want people who meaningfully advance the mission to share in ownership of the company behind it, though the legal and allocation model still needs to be worked out.

[Give these instructions to your agent](../README.md#want-to-contribute-give-this-to-your-agent)
