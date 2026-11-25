# Inputs — Optional Dev rename: plans to projects

[Plan](plan.md) · [Tasks](tasks.md)

## Planning evidence

**Scope decision:** Pending — On 24 November 2026 the owner cut this plan down: the resolver and per-workspace ID and path policy moved to [Plan 95](../95-composable-agentic-workspaces/plan.md), and what remains is an optional Dev-only physical rename after Plan 95. Earlier record: the owner asked to call the unit of work a project and to keep existing identities. Next: after Plan 95 lands, the owner decides D2, whether to do the rename at all.

**Prior art:** [Plan 48](../48-one-record-model/plan.md), [Plan 51](../51-astrid-dev-clean-up/plan.md), [glossary](../../agent/shared/glossary.md), [project-format](../../docs/project-format.md), [project_contract.py](../../scripts/project_contract.py), [records.py](../../scripts/records.py), [pack_shape.py](../../scripts/pack_shape.py), [views.py](../../scripts/views.py), [issue_intake.py](../../scripts/issue_intake.py), [release_branches.py](../../scripts/release_branches.py) and [docs CI](../../.github/workflows/docs.yml), inspected at `83ab5c0ec2842023f9227451fbb0d71adfee428c` and rechecked at `0b1c9fd0e3bd063caa4b412e8bf3e90bf02ab2c4`. `PLAN_FOLDER` is imported by about ten modules; `auto_merge.py` allowlists the `plans` folder; the public feed carries project `githubUrl` paths. Couplings are listed [below](#actual-coupling-and-alternatives).

**Approach:** Keep `plans/` until Plan 95 has made paths configuration, then, only if the owner wants it, move the packs and Dev's consumers in one candidate, keep numeric IDs and history, and allow only narrow read-only aliases.

**Challenge:** An independent direction review on 24 November 2026 found that renaming before extraction put 3–6 risky days on Otto's critical path for no gain to Marketing, and that 97 and 98 changed the same modules and packs. The owner agreed; see [Plan 95's dispositions](../95-composable-agentic-workspaces/inputs.md#direction-review-and-dispositions).

**Proof and limits:** One-to-one pack inventory; unchanged verdicts; export JSON differing only in enumerated paths, schema and IDs unchanged; App consumer check; rollback rehearsal. Not every external link to an old path can be found; history pins cover the repository's own.

**Review rounds:** Pending — Recommend one final R and no review stop, now that the resolver contract has moved to Plan 95. Next: the owner confirms if D2 chooses the rename.

**Run start:** Pending — No run is authorized. Next: if the owner chooses the rename after Plan 95, record the run, its accountable session and the authority for trusted-automation changes.

### Actual coupling and alternatives

- project_contract.py derives numeric identity from numbered plan folder and recognizes relative gap links. records.py fixes project fields, release plan links and release branch/repository semantics. checks.py, planning/pack-shape/completion/boundary checks and views use paths and IDs; check catalog and golden fixtures are affected.
- release_issues.py, boards.py, release_branches.py, issue/review intake, claim_project.py and auto_merge.py route by plan number/path/label, with security-sensitive trusted-main and ruleset boundaries. Existing branches and frozen issue/release receipts are facts, not rename targets.
- export_public_vision.py and App consumer depend on stable schema and paths; strategy and generated view markers reference current source paths. Record intended diff and keep schema/IDs, not merely cosmetic feed parity.
- Run state in plans/<project>/.otto/runs and instructions in active release packets may reference original paths. Preserve their custody and revision-pinned paths; do not repoint active runs.
- Terminology-only change (lowest cost but leaves confusing path/ID coupling); mass search/replace (unsafe and loses semantics/history); separate source resolver plus one coordinated move (recommended then; the resolver is now Plan 95's OT-7). If external compatibility or active writers make the physical rename unreasonably risky, record the narrower alternative and bring it to the owner rather than silently force it.

Coordinate with Plan 95 (base; Plan 97 is cancelled and absorbed into it); Plan 71/72/73/53 (consume accepted results); Plan 52 (issue intake), Plan 31/58 (release/strategy) and Plan 44 (evidence) for current and future source ownership. Recheck actual overlap, choose wait/stack/separate at dispatch; do not demand completion of unrelated future product release work just for naming.

## Owner decisions

- **D1 (decided, 24 November 2026):** project is the unit of work; existing identities are kept; Marketing may use slugs. The resolver and ID policy belong to Plan 95.
- **D2 (open): do the rename at all?** Options: rename Dev to `projects/<NN-slug>/project.md` after Plan 95, or keep `plans/` permanently and say "project" in prose only. **Recommend** deciding after Plan 95 lands: the cost is then about 3 days and the benefit is cosmetic, so keeping `plans/` is a sound answer.
- **D3 (open, only if D2 is yes):** the cutover window, and whether any read-only `plan:NN` alias is needed for active runs. Recommend no bulk label or branch changes.

## Source identities

Planning snapshot: astrid-dev `main` `0b1c9fd0e3bd063caa4b412e8bf3e90bf02ab2c4` (24 November 2026). At dispatch, record the post-95 `main` SHA, the Otto tag it pins, and the candidate branch. No new repository, run, merge or release is authorized by this pack.

## References

[Plan 95](../95-composable-agentic-workspaces/plan.md) · [Plan 48](../48-one-record-model/plan.md) · [Plan 51](../51-astrid-dev-clean-up/plan.md) · [Planning skill](../../agent/shared/workstreams/plan.md) · [Run contract](../../agent/shared/run-contract.md).
