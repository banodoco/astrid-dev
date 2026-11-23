# Plan 73 MS-7/MS-9 — D5 decision and integration preflight

**Status: proposal only, no active-source migration, old package deletion or D5 approval.**

## Current evidence base

The [MS-7 reference inventory](https://github.com/banodoco/astrid-dev/actions/runs/45189627989) at prior verified candidate `491fbfd77b75451404c7e8ce298c6e79a0f1ca73` identified **73 literal references in 18 active-consumer files** (49 known source mappings, 24 manual/command reviews). The same inventory also preserves historical, release-owner, plan-owner, protected-test and legacy-authority categories. These counts belong to that source snapshot and can change; **use the newly added exact-head MS-9 preflight artifact for the current candidate**, not old row numbers.

The new `scripts/ms9_cutover_preflight.py` inspects an **exact PR-head SHA** in a disposable checkout. It records the 20 primary old-to-new mappings, tracked legacy authored `SKILL.md` files and aliases, all tracked consumer locations, required action, responsible owner and explicit `HOLD_PENDING_D5_AND_INDEPENDENT_ACCEPTANCE`. It never edits any source.

## Decision classes that must not be collapsed

| Category | Rule before D5 | Owning decision |
| --- | --- | --- |
| Authored old `skills/` documents and symlink aliases | Preserve; the current source of truth | Plan 73 owner and MS-9 reviewer |
| Mapped README, CONTRIBUTING, templates and contribution docs | Prepare exact rewrite only; do not activate until handoff | Document owner at cutover |
| `scripts/astrid_dev.py sync` | **Retain where used for generated Markdown/vision views**; this is distinct from the historical `sync.sh` installer | Views/checks owner |
| `sync.sh` (root script, installer documentation and old tests) | Retire only after installation destinations and replacement CLI have been qualified | MS-9 and installation owner |
| `scripts/workstreams.py` role/shared indexes, `scripts/views.py` old generated references | Migrate the owning contracts and **preserve replacement regression oracles**; never globally replace paths in literals | MS-8/MS-9 check owner |
| Active release briefs, packets and mailbox instructions | D5 decision by named Release Lead; no retrospective edits to active handoffs without owner custody | Release Lead |
| Active and historic plans | Split current authority from historical receipts; preserve or revision-pin old claims | Plan owner |
| Evidence, ledgers and old CI receipts | Remain historically accurate; prefer immutable SHA links for provenance | Historical record custodian |
| Pinned tests/fixtures | Name each intentionally superseded old-layout assertion; preserve behavior and negative checks before replacing | Validator reviewer |

## D5 owner packet — questions requiring rulings

1. Which active release/packet sessions can be safely restarted, and who confirms their current custody? What is the exact date, source SHA and stop/go point for changing instruction paths?
2. Which consumer sets are included in a single coordinated change and which historical receipts are deliberately left immutable? Who owns decisions for old release packets and release-specific procedural copy?
3. Will currently supported clients accept the generated **symlinked** packages and repository-relative `repo` references on the actual target host? Record each confirmed host/client or NO-RESULT.
4. Do the old generated role/shared indexes have replacement checks with **same failure detection**? List each test/fixture by name and the postcutover gate that substitutes it; no silent deletion.
5. Which installations are in scope? Foreign files/symlinks, legacy owned aliases and repeated installs must be explicitly checked in disposable environments before real-authority change.
6. Who provides independent final R and the separate maximum-two-round Astra High whole-project sense check? The original RS1 BLOCK and bounded six-finding disposition are not erased.

## Source integration and promotion order

1. Retain current `skills/` and existing protected CI; qualify stacked [#1390](https://github.com/banodoco/astrid-dev/pull/1390) and [#1627](https://github.com/banodoco/astrid-dev/pull/1627) under exclusive custody and appropriate independent review. Current recovery branches are not a shortcut to project/main.
2. Run the exact-head MS-9 preflight artifact, resolve its manual/owner queues, and preserve the 20-source crosswalk and semantic policy proofs. Capture active customer/agent consumers outside this repository as **read-only external dependencies**; do not mutate other repositories.
3. After explicit D5 authority, stage the narrow MS-7 consumer rewrites and MS-9 legacy removal with source-by-source compatibility tests. Do not rewrite unrelated historical receipts or weaken oracles.
4. Have a separate genuinely fresh agent execute [the independent task](ms10-fresh-agent-assignment-20261123.md) while its proctor uses [the held-back client verifier](ms10-client-discovery-protocol-20261123.md). Client selection is independent proof, not inferred from `SKILL.md` file readability.
5. Qualify MS-11 on the **integrated** exact head: source manifest, runtime clients, package hashes, dangerous negatives, foreign-collision recovery, link/anchor checks, full unit suite and hosted CI. Record macOS, Windows and untested claims individually.
6. Run independent final R, request explicit owner project-to-main GO and only then permit authorized integration. Preserve final project-wide sense-check rounds separately from R.

**The current result is deliberately HOLD** until those decisions and independently reviewed proofs exist. There has been no D5 cutover, legacy removal or merge.
