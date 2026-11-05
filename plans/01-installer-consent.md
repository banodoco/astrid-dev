# 1 — Merge completed installer consent

**Start here:** read [AGENTS.md](../AGENTS.md), choose a workflow in the [skills guide](../skills/README.md), follow the [run contract](../skills/astrid-dev-shared/run-contract.md), and look up terms in the [glossary](../docs/glossary.md).

[README queue](../README.md) · [Initiative handoff](MANAGER.md). First release slice; it does not depend on generation, CE or Packs and does not authorize product execution. Source evidence: [Astra merge plan](../references/PLAN.md), [exact manifest](../references/donor-manifest.json), [IC END acceptance](../references/evidence-summary.md).

## Goal

Let users choose what Astrid installs and enables, with clear consent, saved preferences, and predictable behavior.

Preserve the accepted known nonblocking skills-off rendering limitation; do not silently claim it fixed.

## Starting code and branch policy

Historical bases recorded in the 4 Nov 2026 audit (observations only): Agent `e50d9a6daf2124a21f9cdf78826253ddadec7f83` (`pre-main`), App `878c28df7a6c80fa9aaa6540c5fccad95473e7c1` (`pre-main`), Runtime `9fc53b771134940aaac901e4cfc5d03c1db1a20a` (`pre-main`), VibeComfy `e2905d068d5851b9c32856d32b8251852a01d6dd` (`main`; no pre-main observed), lifecycle `db79345536985c701b7aff2eb5eec36667aae204` (`main`; no pre-main observed). These are dated audit facts, not execution bases. At execution freeze the then-current target in each changed repo; do not assume any recorded SHA is still current.

Merge Agent donors in order `6087e0fbe7e2bd45c9911ff5cf1093614d715863` → `19229d2325879c12e01c6bcdc604fd743b158ece`; App donors `e97450cff0ed570cfaa077369b28c269b562bd1e` → `9ddff8efbc9e914efbe04cb49da2648c4feb4db4`. These four accepted donors are the only feature inputs. Runtime/VibeComfy/lifecycle are unchanged producers, not merge inputs. The later candidate must be a fresh isolated create-only branch from the frozen destination base; after independent review, promote the exact candidate to `pre-main` using the destination's ordinary fast-forward/create procedure. Never overwrite an earlier candidate or use main/int/r1 as publication destination.

## Inputs and tasks

Accepted Agent donors: `6087e0fbe7e2bd45c9911ff5cf1093614d715863`, `19229d2325879c12e01c6bcdc604fd743b158ece`. App donors: `e97450cff0ed570cfaa077369b28c269b562bd1e`, `9ddff8efbc9e914efbe04cb49da2648c4feb4db4`. Both sibling tips are required; their sibling merge probes passed. Freeze current pre-main anew; observed Agent `01eceda...` and App `878c28...` are research snapshots, not permanent targets.

| ID | Work / output | Depends on | Lead | Completion evidence |
|---|---|---|---|---|
| I-01 | Freeze current Agent/App pre-main, four accepted donors and unchanged producer identities; adapt RI-0 to installer-only selection. | M-00/01 | N / Luna | Exact source manifest, preserved acceptance, executable RI assertions match only this slice. |
| I-02 | Merge Agent donors onto frozen base, resolve installer consent/handoff interaction and three known conflict paths. | I-01 | X / Terra + Luna | Candidate preserves both installer contracts; focused Agent tests below pass. |
| I-03 | Merge App donors, regenerate manifest from the verified Agent candidate, refresh canonical locks without adding producer features. | I-02 | N / Luna | Matching argv fixture, exact Agent source, App checks below pass. |
| I-04 | Independent scoped END review of actual Agent/App tuple and evidence. | I-02/03 | Review / Astra | No blocking findings; no unexplained lost behavior or changed producer payloads. |
| I-05 | Publish immutable candidates and fast-forward/create pre-main at exactly reviewed heads; record promotion. | I-04 | N / Luna | Remote head checks and promotion manifest; only Agent/App updated. |

I-02 is very hard because the new base can return from `boundary_handoff.handle(...)` before IC policy/summary processing. Resolve saved/explicit policy and preserve uninstall receipts, protected roots, exact-realm and foreign-owner checks. R0 is an existing installation: no blanket first-install prompt. Completed handoff must apply requested policy or explicitly refuse it. Keep the required gate before legacy staging. Give Terra bounded Luna source/test helpers; design/integration stays with Terra.

Known conflicts are `astrid/installer/backend.py`, `astrid/installer/cli.py`, `tests/test_installer_bootstrap_refusals.py`; inspect current targets for additional affected seams. App conflict is `public/install-manifest.json`; use canonical `scripts/installer/pin.mjs`, never copy an old manifest or lower release semantics.

## Explicit acceptance

Agent: `tests/test_installer_ic_done2.py`, `tests/test_installer_app_argv_fixture.py`, `tests/test_installer_bootstrap_refusals.py`; exact affected consent/autostart/shim nodes from the existing IC-1A/IC-2A cards. Preserve/check both runtime locks. For the handoff seam run `tests/test_boundary_handoff.py::test_cli_serializes_boundary_and_never_calls_legacy_paths`, `::test_cli_uninstall_completed_handoff_orders_services_and_preserves_r1`, `::test_uninstall_rechecks_realm_at_file_removal`, `::test_cli_uninstall_handoff_refuses_uncertain_or_failed_steps`; add a small deterministic explicit/saved-policy and summary regression if these do not exercise that new intersection.

App: the exact paths in [IC-1P](../references/evidence-summary.md) and [IC-2P](../references/evidence-summary.md) for `SetupBlock.done2.test.tsx`, `WelcomeRunMode.test.tsx`, `WelcomeFlow.test.tsx`, `installArgv.fixture.test.ts`, `SetupBlock.test.tsx`, `copy.test.ts`; `scripts/installer/manifest.test.mjs` and `release.test.mjs`, plus canonical pin check and cross-repo argv fixture byte equality. Freeze final selectors in I-01; no whole UI/SDK suite.

Reuse accepted donor evidence. Recheck only affected behavior on the composition and final immutable tuple; no historical base replay. Runtime contract artifacts were unchanged between lock2776ba and observed9fc53, but confirm against the actual frozen target. Keep VibeComfy/lifecycle pins unchanged in this increment. No CPU generation or CE tests are acceptance for this slice.

## Existing runner mapping

Use RI-0/A/P/END/BRANCH with the explicit installer-only contract from the source audit. Preserve/archive old full-release cards. Remove old unconditional generation/CE/K27/five-repo tests and DEPS from this increment only. Mark unused RI-V/L/R composition rows out-of-scope (not verified) so `end_ready()` does not wait forever; preserve their later ownership in plans3/5. Amend MINT/PROGRAM DONE wording: this is one delivered increment, not the whole initiative. No extra owner/advisor approval once execution starts.

Scope of I-02 edits includes the exact handoff/installer production and regression files necessary for this intersection, frozen in its card before launch. Other failures return to the orchestrator with source evidence for a bounded correction. No broader hardening.
