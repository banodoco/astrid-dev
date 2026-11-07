# Vision, gaps, plans and evidence

Start with **[A tool to unlock the collective artistic ambition of the open-source community](vision.md)**.

The vision contains four [pillars](vision.md#four-pillars)—**A Tool for Artistic Ambition, Agent-Powered Liquid Software, Intelligence That Compounds, A Shared Creative Endeavor**—and four [guiding principles](principles.md): **local-first/cloud-capable, open by design, creator-controlled, eliminate needless technical wrangling**.

**[Gaps](gaps.md) → [Plans](../plans/) → Evidence → reassessment.** A gap may apply to one or several pillars and principles. The files live in **one** [`gaps/` directory](gaps/); they are not duplicated beneath their conceptual owners.

The current gaps are [F-005](gaps/F-005-local-files-cloud-assist.md), [F-006](gaps/F-006-fully-hosted-workspace.md), [AA-001](gaps/AA-001-sustained-creative-work.md), [LS-001](gaps/LS-001-portable-components.md), [LS-002](gaps/LS-002-agent-workspace-control.md), [LS-003](gaps/LS-003-full-stack-contributions.md), [CI-001](gaps/CI-001-agent-learning-loop.md), [CI-002](gaps/CI-002-federated-knowledge.md), [CA-001](gaps/CA-001-creative-challenge-culture.md), [CA-002](gaps/CA-002-contributor-ownership.md), and cross-cutting [F-001](gaps/F-001-platform-reliability.md), [F-002](gaps/F-002-safe-user-control.md), [F-003](gaps/F-003-creative-execution.md), [F-004](gaps/F-004-pack-lifecycle.md).

Existing gaps should be reused before proposing new ones. For example, **local/cloud deployment** is already partly addressed by F-001 and F-003; assess whether their closure criteria really need another independent gap before introducing one.

[Reference documents](references/) preserve the original Liquid Software philosophy, component/source maps, the proposed Hivemind protocol and a [dated assessment of current plans](references/plan-gap-assessment-2026-11-06.md). Plans own their gap links and the [plan catalog](../plans/index.md) alone owns status, priority and ownership. The documentation and public-content integrity checks run in CI; evidence-based gap reassessment still requires review.

## Public vision page (GitHub-authored)

The public Astrid vision page reads **one published JSON projection** of this repository. The editorial sources remain here: `vision.md` owns the headline and pillar descriptors, `pillars/*.md` the details, `principles.md` the operating principles, `gaps/*.md` the assessed outcomes, and `../plans/index.md` the complete project catalog. Each `plan.md` owns its gap links. No duplicate descriptions or project statuses live in Astrid App.

Astrid App owns only its layout, animation, and featured-item selection. The [public feed exporter](../scripts/export_public_vision.py) validates structural relationships, includes a source SHA and GitHub permalinks, and emits schema v1. Adding a project or closing a gap does not require an Astrid App PR or rebuild.

## Live public vision feed

After merging validated content to `main`, [the documentation workflow](../.github/workflows/docs.yml) publishes a **generated, versioned JSON feed** to the `vision-published` branch. The branch is seeded for preview, but normal updates come only from validated `main` pushes. The public endpoint is `https://raw.githubusercontent.com/banodoco/astrid-dev/vision-published/vision.json`. The published branch is **generated output only**: contributors edit the Markdown and plan catalog on `main`, never `vision-published`.

The exporter provides `schemaVersion: 1`, the exact source commit, pillar/operating-principle/gap content and the complete plan catalog with GitHub permalinks. Publication runs only after the documentation validator and content-contract tests pass. A failed validation leaves the previous published feed unchanged. A browser's normal HTTP cache may delay visibility briefly; this is not instant real-time updating. Astrid App reads the feed at runtime and owns only presentation. **No cross-repository sync PR or copied editorial snapshot is required.**

The public feed changes independently of Astrid App releases. Breaking schema changes must use a new version or be deployed compatibly; existing clients must not be silently broken.
