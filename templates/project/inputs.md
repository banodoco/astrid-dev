# Inputs: <project name>

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

This is the **single reviewable record** of why this project should exist and why this approach was chosen. Use exact sources or clearly scoped pending questions, not assertions that research happened. The [project-planning skill](../../skills/astrid-dev-plan/SKILL.md) defines the required process. For a draft, each pending subsection must state **why it remains unknown and the next action**; do not silently imply the owner has accepted the scope.

**Scope decision:** Pending — Owner end-state agreement has not yet been established. Next: obtain the owner's selected outcome and record its dated source before treating the scope as accepted.

### Prior art and behavior traced

Pending — Prior-art coverage and current behavior have not yet been established. Next: search relevant repositories, existing projects and comparable approaches, pin useful revisions, and trace actual input → behavior → output, including reuse opportunities and negative findings.

### Reuse and placement decision

Pending — No evidence-backed placement choice has been made. Next: compare extending a current pack, creating a pack, changing shared core and simpler/no-build alternatives; record the smallest justified option and its tradeoffs.

### Independent simplification challenge

Pending — The independent simplification challenge has not been conducted. Next: obtain distinct high-judgment critique, record specific removals/consolidations, the source of that critique and the accepted/rejected suggestions.

### End-state options and owner choice

Pending — Ten end-state alternatives and the owner's selection have not yet been recorded. Next: present the options, preserve them or their source, and capture the actual decision and rejected tradeoffs; do not infer approval.

### Assumptions and evidence limits

Pending — Evidence limits and implementation unknowns have not yet been distinguished. Next: separate observed capabilities from assumptions, unavailable sources, and questions that need resolution before task dispatch.

## What we build on

Record the sources this project actually uses: existing work, a brief, design references, a dataset, accepted decisions, or a predecessor's verified output. Identify what each establishes and what remains unknown. Link the original where possible.

| Input | Version, identity, or link | Why it matters / limits |
|---|---|---|
| | | |

## For projects that change code

Before implementation, identify each product repository, actual base branch and SHA, retained commits and unpublished work, verified predecessor output, fresh candidate branch, and intended merge destination. Distinguish the base from donors and historical observations. Verify `pre-main` where intended; preserve any project-specific branch or publication rule. Omit this section when code is not an input.

## Supporting material

Link design, source assets, evidence, and relevant constraints where they live. Add a supporting folder only if the material needs one. Keep credentials, private logs, and machine-specific paths out of published plans. See [how project folders grow](../../docs/project-format.md).
