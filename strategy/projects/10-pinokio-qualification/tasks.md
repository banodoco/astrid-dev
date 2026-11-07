# Tasks: Pinokio qualification

[Plan](plan.md) · [Inputs](inputs.md) · [Project status and owner](../../../README.md)

## Task index

| ID / outcome | Route | Depends on | Progress |
|---|---|---|---|
| [PIN-0 — Freeze and reconcile sources](#pin-0--freeze-and-reconcile-sources) | N / Luna | Start of plan | |
| [PIN-1 — Preserve launcher interface and Task L behavior](#pin-1--preserve-launcher-interface-and-task-l-behavior) | X / Terra + Luna helpers | PIN-0 | |
| [PIN-2 — Establish engine controls and Stop/Quit refusal](#pin-2--establish-engine-controls-and-stopquit-refusal) | S / Sol + Luna helpers | PIN-0; deployed Pinokio fixture/version and supported API | |
| [PIN-3 — Reconcile direct-custody provider](#pin-3--reconcile-direct-custody-provider) | X / Terra + Luna helpers | PIN-2 contract; current Agent/Q adapter and process observer heads | |
| [PIN-4 — Focused validation and scoped review](#pin-4--focused-validation-and-scoped-review) | X / Terra + Luna helpers; Astra review | PIN-1 through PIN-3; exact candidate frozen | |
| [PIN-END — Record disposition](#pin-end--record-disposition) | N / Luna | PIN-4 | |
| [PIN-PROMOTE — Publish accepted launcher increment](#pin-promote--publish-accepted-launcher-increment) | N / Luna | Scoped acceptance of the launcher increment's exact head; mutation authorization | |

## Task details

### PIN-0 — Freeze and reconcile sources

- **Route:** N / Luna.
- **Work and done:** Record exact repo/remotes/branches/heads and clean/dirty state for the chosen Pinokio base, intended `pre-main` target, and proposed donors. Resolve target existence, base, and create-or-fast-forward policy. Map Task L environment/lifecycle changes and M4-4a/M4-6 inputs to current ancestry and paths; mark each reusable, superseded, absent, or incompatible. Do not select an arbitrary latest branch.

### PIN-1 — Preserve launcher interface and Task L behavior

- **Route:** X / Terra + Luna helpers. **Depends on:** PIN-0.
- **Work:** Reconcile scripts against the focused interface contract: install modes, manifest/ref selection, foreground ownership, readiness-before-Open, stop ordering, recovery-before-pull, local update, reset/data-safe uninstall, platform quoting, and environment isolation.
- **Focused checks:** After source composition, run only `node --test tests/launcher.test.mjs tests/lifecycle.test.mjs tests/environment.test.mjs tests/process.test.mjs`. Run `node tests/check-bootstrap.mjs <selected bootstrap path>` only if bootstrap bytes or manifest handling change. Retain per-platform CI evidence; fake fixtures do not qualify native Pinokio/OS behavior.
- **Done:** Required interface behavior and focused results are recorded; retain per-platform CI evidence.

### PIN-2 — Establish engine controls and Stop/Quit refusal

- **Route:** S / Sol + Luna helpers. **Depends on:** PIN-0; deployed Pinokio fixture/version and supported API.
- **Work:** Establish the actual engine/API contract from supported deployed source/dependencies. Bind `start.js`, `stop.js`, `update.js` and resolved helper bytes, selected app/mode, engine/action/session identity, and owned cleanup. Invoke immutable Stop/Update through the actual engine, await terminal settlement, and prove busy/unknown refusal leaves process/listener/health/session identity unchanged before same-session retry.
- **Done / limit:** If engine, settlement/readback, or refusal-veto semantics are absent, stop this implementation row at a concrete NEEDS report. Do not invent a wrapper, run descriptors with Node, substitute disposable commands, or claim success. Native OS qualification requires the exact deployed version and each supported OS.

### PIN-3 — Reconcile direct-custody provider

- **Route:** X / Terra + Luna helpers. **Depends on:** PIN-2 contract; current Agent/Q adapter and process observer heads.
- **Work:** Adopt only source-backed pieces still matching current interfaces. Keep Pinokio custody distinct from direct slots; bind immutable action graph and selected app; distinguish queued from settled; refuse errors, timeout, disconnect, missing readback, source drift, ambiguous session, observer gap/overflow, or unbound execution before authorization/receipt.
- **Focused checks and done:** Select provider/observer/request-settlement tests from the current owning repo. Require authenticated context, engine-backed terminal readback, independent gap-free custody observation, and action-specific postconditions. Historical fail-closed tests alone do not satisfy this row.

### PIN-4 — Focused validation and scoped review

- **Route:** X / Terra + Luna helpers; Astra review. **Depends on:** PIN-1 through PIN-3; exact candidate frozen.
- **Focused checks:** Run only changed-boundary launcher/provider tests and explicitly required native canaries. For launcher changes retain PIN-1's selectors. For custody use exact current provider/observer/adapter selectors frozen in the task brief. Native acceptance covers hosted and fully-local flows, busy/unknown Stop and Quit, readiness, interrupted install/update recovery, port conflicts, data-safe reset/uninstall, and platform-specific command handling.
- **Review and done:** Review exact source heads, diffs, test output, skipped cases, and unresolved native gaps; no broad suites or GPU/model execution. Existing Astra END review stays scoped to the exact candidate and evidence; no new approval flow or review rounds are added here.

### PIN-END — Record disposition

- **Route:** N / Luna. **Depends on:** PIN-4.
- **Done:** Report only demonstrated outcomes and remaining NEEDS. If native refusal-veto or custody settlement is unresolved, mark that release boundary blocked/unqualified and preserve the specific evidence gap. Historical `BLOCKED` snapshots are not current status.

### PIN-PROMOTE — Publish accepted launcher increment

- **Route:** N / Luna. **Depends on:** Scoped acceptance of the launcher increment's exact head; mutation authorization.
- **Authority and done:** Publish only the reviewed immutable Pinokio candidate and promote that same head to the resolved `pre-main` by ordinary create/fast-forward rules. Recheck the target immediately before mutation; if it moved, retain the reviewed candidate and reconcile on a fresh base. The launcher increment may be delivered independently of engine/custody rows only if it makes no unsupported native Stop/Quit safety or qualification claim. Full native qualification/release remains gated by PIN-2/3 evidence.

## Constraints and retained limits

- This documentation plan authorizes no product edits, test execution, commit, push, worker launch, hosted action, schedule change, install, daemon launch, GPU/model work, or broad suite.
- Task L's 12 native checks guide eventual qualification. Its known render-smoke omission, manual-only fully-local journey, and upstream diagnostics hint are revisited only when a changed boundary or qualification owner selects them.
- Native Stop/Quit refusal veto is a hard unsatisfied requirement: adapter-side lifecycle ordering, fake kernel tests, POSIX child fixtures, and pinned historical engine source cannot establish deployed veto behavior.
- M4-6's historical provider had no success-producing authorization path. Do not weaken fail-closed ownership for a passing test or infer that old Q coordination, provisional `TrustedCollectorContext`, hosted rows, or receipts are current.
