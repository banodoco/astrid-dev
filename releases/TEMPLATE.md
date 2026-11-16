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

## Branches

One release branch per repository the release changes, `release/<N>/main`, which every plan and fix branch of the release merges into ([How a release runs](../skills/astrid-dev-release/SKILL.md#how-a-release-runs)); delete this paragraph once the table is written. Repository is a product repository or `astrid-dev`; every plan under Included plans has a `plan <PP>` row in each repository it changes, `astrid-dev` for a plan that changes only this repository. Role is `release`, `plan <PP>` or `fix #<issue>`, the astrid-dev issue the fix answers (for example `fix #721`); Cut at is the 40-character commit the branch was cut from, or `not yet cut`; State is `open` or `published` for a release row, and `open` or `merged` (contained in that repository's `release/<N>/main`) for a plan or fix row.

| Repository | Branch | Role | Cut at | State |
| --- | --- | --- | --- | --- |
| astrid-agent | `release/<N>/main` | release | not yet cut | open |

## Included pull requests

Optional. Open pull requests brought into this release that belong to no listed plan, usually from outside contributors: one line each with the link and what it contributes. The [Release skill](../skills/astrid-dev-release/SKILL.md#take-stock-of-open-pull-requests) says how they are chosen and ordered. Remove this section if there are none.

The optional Issues section is created by `python3 scripts/release_issues.py <N>`, which places it between this section and Publication. It is the release's computed list of issues by label: an issue is in the release by `plan:<P>` of an included plan or by `release:<N>`, and a fix row in Branches must name one of them. It lists each candidate issue's linked number, type, state and the label that brought it in, and no text from the issue. Refresh it when the release is first planned and at check-ins. Before the freeze the list is the whole candidate set: a row removed by hand comes back at the next run while its issue is open and still carries the `release:<N>` label or the label of an included plan. To drop an assorted ticket, remove its `release:<N>` label and its row. Run `--freeze` before the brief becomes Final, then remove by hand the rows that are not shipping, since the command no longer rewrites a frozen block.

## Publication

Not pinned. A Draft is a strategy document, never an instruction to publish.

When approved for final publication, change **State** to **Final** and replace this paragraph with a fenced `json` block containing the exact version, kind, required-update decision and complete pinned product/installer tuple; set the release rows in `## Branches` to `published` once `main` is at the pinned commits. The Release skill and CI validate these against the currently served release and product repositories. The release integer comes from **Release**, while the rationale and included plan links come from the sections above, so they are not copied into a second file. The final, owner-approved transition publishes; after it is published this document is immutable. See [Plan 31](../plans/31-releases-from-astrid-dev/plan.md).
