# Release NN — Short descriptive title

**Release:** NN
**State:** Draft
**Kind:** patch
**Release manager:** not yet named

## Highlight

One sentence describing the most important change creators will notice. This is the single-line summary used by [Strategy](../strategy.md).

## Intent

Explain what this release is trying to achieve, why it matters now, and what a good outcome looks like. This is the living strategic brief, not a changelog of every commit.

## Approach

Describe the intended sequence, key trade-offs, dependencies, qualification, and things deliberately excluded. Update this as the work evolves. Do not imply that listing a plan authorizes its implementation or publication.

## Included plans

- [Plan NN](../plans/index.md) — One sentence saying what this plan contributes to the release; the strategy page shows it.

Delete this paragraph once the list is written; only plan bullets or `None yet` may stay in this section. Replace the example with one bullet for each real `plans/<id>/plan.md` link, or write `None yet` for a draft with no plans. List only plans intended for this release. Kind may be omitted (default `patch`), or set to `minor` or `major`. Each plan's own `plan.md` holds its status, owner and estimate, and `plans/priority.md` holds the order; the [plan catalog](../plans/index.md) is generated from them.

## Plan status snapshot

Run `python3 scripts/astrid_dev.py release status <N> --refresh` once the brief is created, at Lead check-ins and before publication; run it with `--check` to verify the snapshot. This section is generated from included plan records, not edited by hand. The Final brief retains the last snapshot. See [release reconciliation](../agent/shared/workstreams/release.md#reconcile-plan-status).

## Branches

One release branch per repository the release changes, `release/<N>/main`, which every plan and fix branch of the release merges into ([How a release runs](../agent/shared/workstreams/release.md#how-a-release-runs)); delete this paragraph once the table is written. Repository is a product repository or `astrid-dev`; every plan under Included plans has a `plan <PP>` row in each repository it changes, `astrid-dev` for a plan that changes only this repository. Role is `release`, `plan <PP>` or `fix #<issue>`, the astrid-dev issue the fix answers (for example `fix #721`); Cut at is the 40-character commit the branch was cut from, or `not yet cut`; State is `open` or `published` for a release row, and `open` or `merged` (contained in that repository's `release/<N>/main`) for a plan or fix row.

| Repository | Branch | Role | Cut at | State |
| --- | --- | --- | --- | --- |
| astrid-agent | `release/<N>/main` | release | not yet cut | open |

## Included pull requests

Optional. Open pull requests brought into this release that belong to no listed plan, usually from outside contributors: one line each with the link and what it contributes. The [Release skill](../agent/shared/workstreams/release.md#take-stock-of-open-pull-requests) says how they are chosen and ordered. Remove this section if there are none.

The optional Issues section is computed, not written: `python3 scripts/release_issues.py <N>` places it between this section and Publication. How an issue joins a release, how to refresh the list and how to freeze it are in [Pull and freeze issues](../agent/shared/workstreams/release.md#pull-and-freeze-issues).

## Publication

Not pinned. A Draft is a strategy document, never an instruction to publish.

When approved for final publication, change **State** to **Final** and replace this paragraph with a fenced `json` block containing the exact version, kind, required-update decision and complete pinned product/installer tuple; set the release rows in `## Branches` to `published` once `main` is at the pinned commits. The Release skill and CI validate these against the currently served release and product repositories. The release integer comes from **Release**, while the rationale and included plan links come from the sections above, so they are not copied into a second file. If the release ships with a known ledger, link `releases/<N>/ledger.md` and the owner's acceptance in `decisions.md`. The final, owner-approved transition publishes; after it is published this document is immutable. See [Plan 31](../plans/31-releases-from-astrid-dev/plan.md).
