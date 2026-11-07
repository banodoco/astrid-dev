# Astrid vision and public publishing

**[Vision](vision.md) → [Pillars](vision.md#four-pillars) and [guiding principles](principles.md) → [Missing outcomes](gaps.md) → [Projects](../plans/index.md) → Evidence and reassessment.**

The four pillars explain why Astrid exists; the four guiding principles define the creative experience we want. [Gaps](gaps.md) record what is *not yet demonstrated*, each with one primary vision relationship and only justified supporting connections. Projects are independently useful ways to narrow those gaps; completing a project does not automatically close a gap.

## Write in the authoritative source

| You're changing | Edit here | Review requirement |
| --- | --- | --- |
| The public ambition or pillar summaries | [vision.md](vision.md) | Editorial review; keep existing pillar references valid |
| One pillar's explanation | [pillars/](pillars/) | Review meaning and consistency with the other pillars |
| Creator-facing operating principles | [principles.md](principles.md) | Editorial review; don't duplicate contribution/process rules |
| Missing outcome or its evidence | [gaps/](gaps/) | A **new or redefined gap** needs the [boundary assessment](gaps.md#reviewing-a-new-or-redefined-gap); an evidence-only update does not |
| Project status, owner or priority | [project catalog](../plans/index.md) | Follow the [contributor process](../docs/contribution-workflow.md) |
| Project scope, tasks and inherited sources | Its [project folder](../plans/) | Scope changes follow the project owner and review rules |

Small copy edits need a normal PR, not a new project. Product API documentation belongs with the corresponding [product repository](../skills/astrid-dev/references/domains.md), not in a duplicate Astrid-dev manual.

## Publishing

These Markdown sources are authoritative. [The documentation workflow](../.github/workflows/docs.yml) validates them and publishes a **generated JSON projection** only after a validated merge to `main`. The public [Astrid vision page](https://astrid.haus/vision) reads the published feed at runtime; don't edit copies of its editorial content in Astrid App.

The exporter [`scripts/export_public_vision.py`](../scripts/export_public_vision.py) maintains `schemaVersion: 1`, source-commit identity, pillar/principle/gap data and the complete project catalog. Its output lives only on the generated `vision-published` branch at `https://raw.githubusercontent.com/banodoco/astrid-dev/vision-published/vision.json`. A failed validation leaves the prior feed unchanged. Breaking schema changes require compatible migration or a new version.

**Full contributor instructions:** [How to contribute](../docs/contribution-workflow.md) · [Development skill](../skills/astrid-dev/SKILL.md).
