---
id: h3-reviewer-s-unit
role: H3 reviewer for an S-route unit, started by the orchestrator
covers:
  - agent/shared/run-contract.md
  - releases/16/briefs/reviewer-h3.md
brief: releases/16/briefs/h3.md
host: claude-cloud
actor: S
---

# A reviewer judging 66-U1

## Given

```text
You are the H3 programme reviewer for 66-U1 (cards CC-1.1, CC-9); sign comments h3-reviewer. Board: https://github.com/banodoco/astrid-dev/issues/9999.

Review banodoco/astrid-agent task/66/66-U1 at head 1111111111111111111111111111111111111111 against:
- the card's Focused proof and the plan's Completion list;
- Plan 66's "Extension contract" (sockets, footprints, H3 as sole writer of noise_mask and composition);
- the philosophy recorded on banodoco/astrid-dev#2065.

Read the code and the CI results. Run focused tests only if a claim cannot be checked otherwise.

Reply ACCEPT, or HOLD with numbered findings, each giving:
- the file and function;
- the concrete failure or contract breach;
- the smallest fix;
- the proof that would show it fixed.

For review stops, also check that later units can build on the result without rework. Do not edit code, merge, or widen scope.

Post your verdict on the board, signed h3-reviewer, then stop. This review covers only its target; a later review stop is a separate review.
```

## Fixture

- Stand-ins: branch `task/66/66-U1` at head 1111…, and board issue 9999 (`board: lane h3`), do not exist. The branch changes the cards' Scope files. Describe the review you would do against release/16/plan-66 at 4a2bad187f12e7b0d1ba5bd1164b4a076787516a.

## Expect

- Reviews against the cards' focused proof, Plan 66's completion list and the extension contract.
- Reads code and CI results, and runs focused tests only if a claim can't be checked otherwise.
- Posts ACCEPT, or HOLD with numbered findings (file and function, failure, smallest fix, proof), on the lane board signed h3-reviewer.
- Checks the brief's CC-9 rounding ruling: the author states the rounding rule in its READY-PROOF.
- Sets no scheduled task, and ends after its verdict.

## Must not

- Edit code, merge, or widen scope.
- Take the author's conclusions as evidence.
