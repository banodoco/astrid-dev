# Tasks: installer consent

**Landed 7 Nov 2026.** Agent `main` = `c5a970aa3c048db1ee9c5100d1db2b4444358592` (was `0b6a7aef0`); App `main` = `ae6c777ca8f4afa4c98a0319b58963d2f4bbe4f8` (was `5fa4c0909`); Runtime pin unchanged. Donor work credited to Dylan (@matlowai); plan owner @AstridPseudon. Evidence is for the installer-choice slice only, not F-002's broader outcome.

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../index.md)

First release slice; it does not depend on generation, concurrent editing (CE), or Packs. It does not authorize product execution. Source identities and donor order are in [inputs.md](inputs.md); the named checks below must be rerun on the actual candidate.

## Task index

| ID / outcome | Route | Depends on | Progress |
|---|---|---|---|
| [I-01](#i-01) Freeze current Agent/App bases and accepted inputs; adapt RI-0 to this slice. | N / Luna | M-00/01 | Done 7 Nov 2026: bases frozen (Agent `0b6a7aef0`, App `5fa4c0909`); deviations in ledger M01-1..M01-27. |
| [I-02](#i-02) Integrate Agent donors and resolve consent/handoff behavior. | X / Terra + Luna | I-01 | Done 7 Nov 2026: Agent landed at `c5a970aa3c048db1ee9c5100d1db2b4444358592`. |
| [I-03](#i-03) Integrate App donors and pin to the verified Agent candidate. | N / Luna | I-02 | Done 7 Nov 2026: App candidate `7165b6e7f`, manifest pins the landed Agent; pin check passed. |
| [I-04](#i-04) Independently review the exact Agent/App tuple. | Review / Astra | I-02, I-03 | Done 7 Nov 2026: independent completion review, round 3, PASS. |
| [I-05](#i-05) Publish immutable candidates and promote the reviewed heads. | N / Luna | I-04 | Done 7 Nov 2026: fast-forwarded to `main`. Agent `c5a970aa3c048db1ee9c5100d1db2b4444358592`; App `ae6c777ca8f4afa4c98a0319b58963d2f4bbe4f8` (merge of `7165b6e7f` with 4 vision commits). Runtime pin `9fc53b771134940aaac901e4cfc5d03c1db1a20a` unchanged. |

## Task details

### I-01

**Freeze sources and acceptance.**

- **Outcome:** Record exact current Agent/App `pre-main` targets, four accepted donors, and unchanged producer identities; adapt RI-0 to installer-only selection and freeze final test selectors.
- **Route:** N / Luna.
- **Dependencies and inputs:** M-00/01; see [inputs.md](inputs.md). Use the source audit and accepted donor evidence linked above.
- **Work:** Freeze targets anew; historical audit SHAs are observations only. Establish executable RI assertions for this slice, preserve/archive old full-release cards, remove unconditional generation/CE/K27/five-repository tests and DEPS from this increment, mark unused RI-V/L/R composition rows out-of-scope (not verified), and amend MINT/PROGRAM DONE wording to describe one delivered increment. Generation integration belongs to [Plan 02](../02-consistent-generation/plan.md), and the remaining fixes belong to [Plan 05](../05-remaining-fixes/plan.md).
- **Focused checks:** Freeze the exact selectors listed in I-02/I-03; no whole UI/SDK suite. No historical base replay.
- **Done:** Exact source manifest and scoped assertions are recorded; acceptance is preserved. This is setup, not authorization to execute product work.

### I-02

**Compose Agent consent and handoff behavior.**

- **Outcome:** Merge both accepted Agent donors onto the frozen base while preserving installer contracts and protections.
- **Route:** X / Terra + Luna; very hard because `boundary_handoff.handle(...)` can return before installer-consent policy/summary processing. Terra owns design/integration; Luna may provide bounded source/test helpers.
- **Dependencies and inputs:** I-01; Agent donor order and historical bases in [inputs.md](inputs.md).
- **Work:** Resolve saved/explicit policy at the handoff seam; preserve uninstall receipts, protected roots, exact-realm and foreign-owner checks. R0 is an existing installation, so do not add a blanket first-install prompt. A completed handoff must apply requested policy or explicitly refuse it. Keep the required gate before legacy staging. R1 finding: non-TTY fresh installs exit 2 without `--yes`; decide whether to announce or default. Known conflict paths: `astrid/installer/backend.py`, `astrid/installer/cli.py`, and `tests/test_installer_bootstrap_refusals.py`; inspect frozen targets for additional affected seams.
- **Focused checks:** `tests/test_installer_ic_done2.py`, `tests/test_installer_app_argv_fixture.py`, `tests/test_installer_bootstrap_refusals.py`; exact affected consent/autostart/shim nodes from existing IC-1A/IC-2A cards; preserve/check both runtime locks. Also run `tests/test_boundary_handoff.py::test_cli_serializes_boundary_and_never_calls_legacy_paths`, `::test_cli_uninstall_completed_handoff_orders_services_and_preserves_r1`, `::test_uninstall_rechecks_realm_at_file_removal`, and `::test_cli_uninstall_handoff_refuses_uncertain_or_failed_steps`. Add a small deterministic explicit/saved-policy and summary regression if these do not exercise the new intersection.
- **Done:** Candidate preserves both installer contracts and focused checks pass. Scope is the exact handoff/installer production and regression files frozen before launch; return other failures with source evidence for bounded correction, with no broader hardening.

### I-03

**Compose App against verified Agent.**

- **Outcome:** Merge both accepted App donors, regenerate the manifest from the verified Agent candidate, and refresh canonical locks without adding producer features.
- **Route:** N / Luna.
- **Dependencies and inputs:** I-02; App donor order in [inputs.md](inputs.md). The known conflict is `public/install-manifest.json`.
- **Work:** Use canonical `scripts/installer/pin.mjs`; do not copy an old manifest or lower release semantics. Keep VibeComfy/lifecycle pins unchanged. R1 findings: the App emits `--yes` and choice flags that the release Agent rejects, so align the App argv with the Agent CLI; the donor manifest drops the ffmpeg pin, so carry it via `scripts/installer/pin.mjs`, not by hand.
- **Focused checks:** Exact affected paths in the accepted scope recorded in [inputs.md](inputs.md) and the check names below for `SetupBlock.done2.test.tsx`, `WelcomeRunMode.test.tsx`, `WelcomeFlow.test.tsx`, `installArgv.fixture.test.ts`, `SetupBlock.test.tsx`, and `copy.test.ts`; `scripts/installer/manifest.test.mjs`, `release.test.mjs`, canonical pin check, and cross-repo argv fixture byte equality. No whole UI/SDK suite.
- **Done:** Matching argv fixture, exact Agent source, and scoped App checks pass.

### I-04

**Independent scoped review.**

- **Outcome:** Review the actual Agent/App candidate tuple and its evidence independently.
- **Route:** Review / Astra.
- **Dependencies and inputs:** I-02 and I-03; reuse accepted donor evidence and recheck only affected behavior on the composition and final immutable tuple.
- **Work:** Apply the existing scoped END review. Runtime contract artifacts were unchanged between `lock2776ba` and observed `9fc53b771134940aaac901e4cfc5d03c1db1a20a`, but confirm against the frozen target. No historical base replay.
- **Focused checks:** Review the evidence and selectors from I-02/I-03; no CPU generation or CE tests are acceptance for this slice.
- **Done:** No blocking findings, unexplained lost behavior, or changed producer payloads. No additional owner/advisor approval is required once execution starts.

### I-05

**Promote reviewed candidates.**

- **Outcome:** Publish immutable candidates and promote exactly the reviewed heads to `pre-main`.
- **Route:** N / Luna.
- **Dependencies and inputs:** I-04; frozen destination and branch policy in [inputs.md](inputs.md).
- **Work:** Use the destination's ordinary fast-forward/create procedure. Never overwrite an earlier candidate or publish to `main`, `int`, or `r1`.
- **Focused checks:** Verify remote heads against the reviewed candidates and record the promotion manifest.
- **Done:** Promotion evidence records exact heads; only Agent and App are updated.
