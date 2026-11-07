# Inputs: <project name>

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

This is the **single reviewable record** of why this project should exist and why this approach was chosen. Use exact sources or clearly scoped pending questions, not assertions that research happened. The [project-planning skill](../../skills/astrid-dev-plan/SKILL.md) defines the required process. For a draft, each pending subsection must state **why it remains unknown and the next action**; do not silently imply the owner has accepted the scope.

**Scope decision:** Pending — Owner end-state agreement has not yet been established; capture the decision and its source before treating the scope as accepted.

### Prior art and behavior traced

Pending — Search the relevant repositories, existing project packs, documentation and comparable approaches; pin useful source revisions and trace actual input → existing behavior → observed output. Record both reuse opportunities and negative findings.

### Reuse and placement decision

Pending — Compare extending a current pack, creating a pack, modifying shared core, and simpler/no-build alternatives against the observed prior art; record the smallest justified option and its tradeoffs.

### Independent simplification challenge

Pending — Obtain a distinct high-judgment critique of the chosen approach. Record concrete proposed removals/consolidations, source of the critique, and which suggestions were accepted or rejected with reasons.

### End-state options and owner choice

Pending — Present ten meaningful end-state alternatives to the owner, then record the actually selected outcome and meaningful rejected tradeoffs with a dated decision/source. Do not invent acceptance.

### Assumptions and evidence limits

Pending — Separate directly observed capabilities from unverified inferences, unknown repositories/platforms, unavailable evidence and questions that must be resolved before tasks are ready.

## What we build on

Record the sources this project actually uses: existing work, a brief, design references, a dataset, accepted decisions, or a predecessor's verified output. Identify what each establishes and what remains unknown. Link the original where possible.

| Input | Version, identity, or link | Why it matters / limits |
|---|---|---|
| | | |

## For projects that change code

Before implementation, identify each product repository, actual base branch and SHA, retained commits and unpublished work, verified predecessor output, fresh candidate branch, and intended merge destination. Distinguish the base from donors and historical observations. Verify `pre-main` where intended; preserve any project-specific branch or publication rule. Omit this section when code is not an input.

## Supporting material

Link design, source assets, evidence, and relevant constraints where they live. Add a supporting folder only if the material needs one. Keep credentials, private logs, and machine-specific paths out of published plans. See [how project folders grow](../../docs/project-format.md).
