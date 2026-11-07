# Astrid Dev — repository policy

**Start:** [the contributor skill](skills/astrid-dev/SKILL.md) for the one contribution process, [domain map](skills/astrid-dev/references/domains.md) to find product owners, and [contributor workflow](docs/contribution-workflow.md) for GitHub claims, proposals and submissions. The [design principles](docs/contribution-design-principles.md) guide changes to this system.

## Authority and source of truth

- [The project catalog](plans/index.md) alone owns project status, priority, accountable owner and estimate. The [project pack](docs/project-format.md) owns outcome (`plan.md`), inherited facts (`inputs.md`) and tasks (`tasks.md`). Bugs and small fixes use issues, **not projects**. Reuse existing projects and [vision gaps](visions/gaps.md) before creating another.
- A claim, queued plan or passing test does **not** accept unresolved scope, authorize execution or allow publishing. Follow existing owner decisions, pause/STOP controls, budgets, repository-specific instructions and the [shared run contract](skills/astrid-dev-shared/run-contract.md). Do not restart a stopped run or reset a review budget because the contributor changed.
- Freeze real base, donor and integrated candidate SHAs. Preserve user changes and private data. Never publish credentials, private logs, local `.otto/` state or user projects; no unapproved external calls, compute or deployments.
- Use actual focused checks and source-bound evidence; missing proof is not success. Review and integration follow the owning product repository's controls. A green PR in one repo does not qualify an assembled Runtime/Agent/App tuple.

## Changes requiring specific review

- **New/redefined vision gap:** Follow the [gap boundary contract](visions/gaps.md#reviewing-a-new-or-redefined-gap); include its first-principles PR assessment and exact primary/supporting vision relationships. CI checks the record; reviewers judge its distinct outcome.
- **New project scope:** Use [project planning](skills/astrid-dev-plan/SKILL.md) and the three-file pack; a maintainer accepts the scope through PR review. Starting, spending and shipping remain separate decisions.
- **Project completion:** Use the [completion PR template](.github/PULL_REQUEST_TEMPLATE/project-completion.md). Include the integrated candidate, all implementation PRs, actual check receipts, models used or an honest unknown, unproven cases and dispositions for every linked gap. A project marked `done` does not close a gap automatically.
- **Self-claim:** Only the authenticated author's single `Unassigned` owner-cell change may auto-merge, and only under protected branch controls. Other catalog changes follow normal review.

## Mechanical checks

[Documentation CI](.github/workflows/docs.yml) validates links, catalog/project relationships, required PR receipts and public feed structure. It **does not** validate the truth of research or product test claims. Locally run `python3 scripts/check_docs.py` and `python3 scripts/export_public_vision.py`; after changes affecting the top-ten project preview run `python3 scripts/check_docs.py --sync`. The public feed is generated from validated `main` only.
