---
description: Independently judge whether a proposed or delivered project or release achieves its outcome simply, coherently and with source-backed evidence.
skill: true
---

# Sense check a project or release

## When to use

For consequential scope/design judgment or a holistic completion judgment beyond ordinary line review. Scale effort to impact and uncertainty.

## Outcome

A grounded verdict on the smallest sound way to achieve the goal, with concrete improvements and evidence.

## Inputs

Goal and constraints, exact proposed or delivered source identities, original evidence, related issues/projects and prior reviews. The [run contract](../run-contract.md) governs independence, routes and authority.

## Procedure

Distinguish scope (proposed design against current code) from completion (actual candidate against goal and proof). Trace real entry points, owners, state and outcomes. Read original evidence, not only summaries.

- Necessity: what remains unsolved? Could reuse, a bounded fix or no change suffice?
- Reuse and ownership: overlapping projects, divergent implementations, confusing paths, competing authorities or wrong layers? Legitimate entry points need not be collapsed.
- Simplicity: what can disappear? Does each abstraction, process, migration or test earn its cost? Preserve data, safety and supported behavior.
- Experience and cost: would creators and weaker agents understand choices, failures and recovery? Avoid unnecessary computation, storage and steps; distinguish estimates from measurements.
- Correctness: missing failure, concurrent edit, custody, consent, compatibility or recovery case? Trace issues to actual evidence and proof.
- Sequencing: compare genuine dependencies and alternate orderings. For a release inspect the brief, proposed run board and task records together: critical path, shared resources, early integrated proof, safe migration and pin order, feasibility.

### Assemble a review packet

Write one short Markdown assignment in the owning project or release's existing packet/evidence location, or link the existing assignment. Name review kind, question, route, independence and permissions, exact base/head or source register, canonical records, original evidence and prior judgments, expected verdict and return location. For scope review provide the actual proposed diff and baseline; for completion provide exact candidate and proof. Use immutable Git references. Assemble a temporary attachment bundle only if needed; it is transport, not a second source.

Return one report with reviewed identities, limitations, verdict and numbered BLOCKING/FOLLOW-UP/NOTE findings: evidence, impact, smallest amendment, owner and verification. Preserve disagreement and negative evidence. Store the original in the owning project's or release's evidence and link accepted changes from canonical records. Recheck material fixes independently without reopening unrelated settled questions.

## Completion

SOUND, SOUND WITH FOLLOW-UPS, REWORK or BLOCKED on the exact reviewed identity. A reviewer judges, not approves scope or publication. No mutation or execution authority is granted by this procedure.
