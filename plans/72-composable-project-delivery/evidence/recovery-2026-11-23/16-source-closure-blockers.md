# Plan 72 — exact historical-row and transitive source-closure proof

**Source-only / disposable Release15 worktrees, 23 November 2026.** **Release HOLD remains.** These are **conditional source selections**, not permission to copy newer release branches, overwrite frozen historical records, rewrite canonical Plan72 authoring or dispatch formal RS1.

## Native results: original full repository checker, not a mock

[GitHub-hosted CI 45274022639](https://github.com/banodoco/astrid-dev/actions/runs/45274022639) on isolated [draft #1624](https://github.com/banodoco/astrid-dev/pull/1624), test head `3a2925caf71f6b4081860d80812631a5cee5fc86`: **COMPLETED SUCCESS**, **533/533 Python** including the disposable native rehearsal, original repository/view checks, and **13/13 real App consumer tests**. The test suite is GREEN *because it verifies and reports actual outcomes*; the **separate composited scratch full check is still RED**.

| Original scratch check stage | Actual checker exit | Actual diagnostics | What changed, scratch only |
| --- | ---: | ---: | --- |
| Frozen release15 + selected 01–05/08/09 code + Plan72 authored pack and five Release15 branch rows | 1 | **22** | Prior validated baseline (7 historical branch rows + 15 Plan72 missing link occurrences) |
| Add pinned canonical historical branch rows to releases 14, 16 and 17 | 1 | **15** | All 7 historical `release-documents` errors disappear; direct Plan72 links still missing |
| Add nine pinned *direct* dependencies cited by Plan72 records | 1 | **40** | All 15 prior Plan72-record broken-link occurrences disappear, but new imported skills/evidence introduce 40 *transitive* `markdown-links` diagnostics |

The [stored, bounded three-file historical patch](15-historical-release-row-selection.patch) contains **three additive hunks / 22 rows only**: Release14 +5 (Plan52 and needed Astrid-dev release row); Release16 +15 (Plans 29, 30, **09**, 38, 31 and Astrid-dev release row); Release17 +2 (Plan19 and needed Astrid-dev release row). It was applied with **native `git apply --check` and `git apply`** against the exact frozen files, and the **original generic branch parser returned seven missing-plan errors before, zero afterward**. The proposed rows were copied verbatim from pinned newer canonical release blobs; they **have not** been approved as the frozen release's historical cut/state truth. The release/Plan48 owner must adjudicate that before any live use. The original source files are restored after each test.

## Forty remaining diagnostics → fifteen distinct missing linked targets

Every listed file exists on canonical main at the shown Git blob. These are *next-hop dependencies* of the three newer shared skills and one historical Plan72 evidence report brought into the disposable checkout. Their presence on main does **not** approve importing their contents into an older release branch. Counts are *occurrences*, not files.

| Next missing target (repository-relative) | Exact canonical blob | Error occurrences |
| --- | --- | ---: |
| `plans/72-composable-project-delivery/evidence/tests/astrid-dev/57703432/feed-parity.md` | `93bf66590b03af717e22bb096667997f7ab61999` | 1 |
| `skills/shared/glossary.md` | `3c4b50950653baee779b2d95f3cb5fcbd7b440c4` | 9 |
| `skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md` | `c1aeb5b8cbc9e2b135dd1749ada12dad75fc3e65` | 3 |
| `skills/roles/astrid-dev-orchestrate/SKILL.md` | `da8974236c29923cf169a147dd81ad192b5c5cf8` | 5 |
| `skills/roles/astrid-dev-manage/workstreams/whole-project.md` | `26dfaeba846853f04f4dabb0d17ace0129a7e76f` | 1 |
| `skills/shared/workstreams/astrid-dev-gpu-validate/SKILL.md` | `983f69f7cf07733c9fcdb4a8a4673a74bc276281` | 2 |
| `skills/shared/templates/decisions-ledger.md` | `66ab4fe1f4681145e59c314d07db667643ae0a77` | 1 |
| `skills/shared/workstreams/astrid-dev-green/SKILL.md` | `4f1d3e689c1943c2f6f6af302643ceb523968a7f` | 7 |
| `skills/shared/templates/run.yaml` | `42c6e83ec02596c8f74e6de70940cdc4d50c3283` | 1 |
| `skills/roles/astrid-dev-manage/workstreams/live-loop.md` | `8c66b11c5e77b808ed2c9a7c81a03a7859322863` | 1 |
| `skills/shared/workstreams/astrid-dev-gap/SKILL.md` | `e74d7a8fb3d37e35a79349ed5d8114d314105d14` | 1 |
| `skills/shared/workstreams/astrid-dev-iterate/SKILL.md` | `6b3caa177acb78e29e87bf736ee175efc1c83473` | 2 |
| `skills/roles/astrid-dev-lead/SKILL.md` | `acfa7b8718e2bec4491591998c900ca4e43eab30` | 2 |
| `skills/roles/astrid-dev-manage/SKILL.md` | `649da4ba24532351001de5e43088a266581dac38` | 2 |
| `skills/shared/workstreams/astrid-dev-merge/SKILL.md` | `07b1498175983c570ba4e8681344ff68d6fdee06` | 2 |

**Boundary:** The original `markdown-links` check scans every Markdown source included in a checkout, so adding one newer skill can create further required links. There is already a following wave of links in the newer workstream tree; **15 files are *not* claimed to be the whole closure**. Copying arbitrary newer `skills/` or `plans/` directories, removing Plan72 evidence links, replacing local references with unchecked URLs, or suppressing the original check to force green is not an authorized Plan72 repair.

## Owner-directed action that actually moves the release

1. **Release/Plan48 shared parser and release-brief owner:** decide if/where the stricter parser's all-included-plan requirement applies on old release snapshots, and authorize the exact historical row patch (or a compatible tested alternative) with verified branch cut/state semantics. The native patch is prepared, **not approved/merged**.
2. **Plan72 authored-record + shared skills owners, coordinated by the existing Release15 Lead:** choose a bounded, link-complete source closure for the canonical Plan72 pack, including its evidence and skill dependencies. Re-pin each approved source blob. The nine direct source files and fifteen next-hop targets are concrete inputs, not an authorization to bulk transplant main.
3. **Actual authorized plan branch, once the owner's scope/Challenge decision, Lead custody/cut and enforced release-main protections are recorded:** select approved sources into the *real* integrated head, run untouched `python3 scripts/astrid_dev.py check` until it genuinely exits **0**, then native source tests, generated views and fixed-authored-input feed parity. Independent formal RS1 follows the accepted pre-RS1 integration, before downstream checker/view changes. Final R/landing/publication remain separately gated.

See the [single Release15 HOLD-to-integration execution packet](14-release15-lift-hold-execution.md). The current run board still says Plan72 **HOLD**; no Lead GO, release ref edit, branch protection change, RS1 dispatch or merge occurred during these checks.
