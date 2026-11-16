Date: 2026-11-16
Kind: fix
Source: the owner, Hannah, decided in the advisor's session on 16 November 2026
Resolved by: 2026-11-16-release-branch-checks

From Release 14 on, every release has one canonical branch per product repository, `release/<NN>/main`, cut from the served release when the release starts. Plan branches are `release/<NN>/plan-<PP>` and fix branches for work outside a plan are `release/<NN>/<topic>`; all merge into `release/<NN>/main`. Tester builds and release candidates are cut only from it, and publication fast-forwards `main` to the reviewed commit on it. The release page lists them in a `## Branches` table that the documentation check validates for structure only. This replaces `int/<project>` for new work; Release 13 and earlier, and their plans, are left as they are. Once a release's branches exist its number is fixed.
