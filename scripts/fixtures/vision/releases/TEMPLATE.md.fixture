# Release NN — Short descriptive title

**Release:** NN
**State:** Draft

## Highlight

One sentence describing the most important change creators will notice. This is the single-line summary used by [Strategy](../strategy.md).

## Intent

Explain what this release is trying to achieve, why it matters now, and what a good outcome looks like. This is the living strategic brief, not a changelog of every commit.

## Approach

Describe the intended sequence, key trade-offs, dependencies, qualification, and things deliberately excluded. Update this as the work evolves. Do not imply that listing a plan authorizes its implementation or publication.

## Included plans

- [Plan NN](../plans/index.md) — One sentence saying what this plan contributes to the release.

Only list plans actually intended for this release. Replace the example link with each real `plans/<id>/plan.md` link. The plan catalog remains the source for ownership, priority, status and estimates.

## Publication

Not pinned. A Draft is a strategy document, never an instruction to publish.

When approved for final publication, change **State** to **Final** and replace this paragraph with a fenced `json` block containing the exact version, kind, required-update decision and complete pinned product/installer tuple. The Release skill and CI validate these against the currently served release and product repositories. The release integer comes from **Release**, while the rationale and included plan links come from the sections above, so they are not copied into a second file. The final, owner-approved transition publishes; after it is published this document is immutable. See [Plan 31](../plans/31-releases-from-astrid-dev/plan.md).
