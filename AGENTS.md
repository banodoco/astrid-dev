# Repository rules

**Start at [astrid-dev](skills/astrid-dev/SKILL.md)** for every contribution. Apply the [contribution design principles](docs/contribution-design-principles.md) when changing workflows, data contracts or evidence rules. Its [domain map](skills/astrid-dev/references/domains.md) is the one index to repositories, reference materials and specialist workflows. The [shared run contract](skills/astrid-dev-shared/run-contract.md) owns source identity, model routing, proof, retries, review and authority.

For claiming, proposing, asking questions, submitting cross-repository PRs and completing work, use the [single contributor workflow](docs/contribution-workflow.md). The claim bot may merge **only** a verified one-cell owner change; every other scope/implementation/completion change follows normal review.

## Scope and authority

- **Bugs and small improvements are issues or existing tasks—not projects.** Keep reproduction, source evidence, user-safety precautions, focused checks and a linked PR. [Bug fixing](skills/astrid-dev-bugfix/SKILL.md) covers recovery; [Iterate](skills/astrid-dev-iterate/SKILL.md) covers scoped repairs. A fact-finding incident can produce an issue without code changes.
- **Projects** require independently useful outcomes; use the [project planning skill](skills/astrid-dev-plan/SKILL.md) only for genuinely new scope. The [catalog](plans/index.md) alone owns project status, priority, accountable owner and estimate. The [project pack](docs/project-format.md) owns outcome (`plan.md`), prior art/decisions (`inputs.md`), and tasks/proof (`tasks.md`). Never invent research, owner agreement or source identity.
- A plan, skill install, queued status or green CI does **not** authorize implementation, spending, deployment or release. Respect existing run authorization and STOP/pause controls. When authorized, use the actual base and intended integration destination (including `pre-main` where prescribed), retain local changes and avoid unauthorized data access. Preserve the current project run's accepted decisions rather than resetting them.
- Keep credentials, user projects, machine-local `.otto/` state, private logs and tokens out of public issue/PR evidence. Run only documented, explicitly scoped checks; planning does not run product tests unless requested.

## Vision, gaps and plans

The [vision](visions/vision.md) defines the ambition, the [gap contract](visions/gaps.md) defines independently assessable missing outcomes, and a project is one approach to narrowing a gap. Use existing gaps and projects before adding new ones. Plans own their gap links; gap files do not repeat plan status or maintain reverse project lists. Evidence may justify a reassessment but finishing a plan never closes a gap automatically.

## Creating or redefining a vision gap — first-principles boundary gate

For a new, retired or materially redefined gap, follow [the gap boundary contract and example PR receipt](visions/gaps.md#reviewing-a-new-or-redefined-gap). In the PR description, provide one **Gap boundary assessment — ID** with Decision, Outcome, Existing alternatives, Why this level, Independent closure, Primary connection, Supporting connections and Evidence. Explain why the missing outcome survives replacing its planned implementation; compare concrete existing gaps/projects and justify the primary vision relationship.

CI compares the receipt against changed gap definitions and the explicitly declared primary/supporting links. It checks structure, not the quality of reasoning; the reviewer must challenge duplication, forced links and insufficient closure criteria. Updating only current evidence and assessment does not require another boundary review.

## Completing a plan: one decision gate

When a PR moves an entry in [the catalog](plans/index.md) to **done**, include a concrete completion assessment against the project's actual proof and **every linked gap**, or explain that a foundational enabler has no direct gap impact.

```md
## Completion assessment — Plan 20

Evidence: [real task result](https://github.com/example/repo/actions/runs/123)
Completion: Yes — A real result met the stated criteria on the named candidate.
Gap F-003: Partially evidenced — This route worked, but other supported routes need proof.
```

Use **Gap ID: Closed / Partially evidenced / Unchanged / Needs recheck — reason** for each linked gap. For a no-gap enabler use **Gap impact: None — reason**. CI enforces presence and linkage, not the truth of proof. An independent reviewer judges completeness; completion is not authorization to publish.

## Local documentation checks

The [documentation workflow](.github/workflows/docs.yml) checks project-pack structure, scope evidence for new/opted-in projects, gap boundary decisions, completion receipts, source links and the published vision feed. Run `python3 scripts/check_docs.py` and `python3 scripts/export_public_vision.py` after documentation changes; catalog edits require `python3 scripts/check_docs.py --sync` to regenerate the README preview. The workflow does not change the author's sources and publishes the feed only after validated `main` pushes. Use the [run contract](skills/astrid-dev-shared/run-contract.md) and product-owned runbooks for executable work.
