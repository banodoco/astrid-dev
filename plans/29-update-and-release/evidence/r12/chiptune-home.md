# Chiptune not ready after update: HOME mismatch (fixed in r12/pack-home-update-handoff)

[Handoff](../../handoff.md) · [Tasks](../../tasks.md)

# Run 42835188782: Chiptune registration diagnosis

Candidate: Agent 313bbd46f1e24bfe635655d78b27ab0b321145d5, harness 0e3c456ee,
Runtime 42ae24aff, App ecd0b0cf1. Receipts were read as data, never executed.
The change is local and uncommitted; harness and the protected pack/import,
readiness-marker, and Windows removal surfaces are untouched.

## Observed legs

- **direct-linux-fresh:** initial R12 install/add/registration succeeds
  (`ev/direct-linux-fresh/before-cleanup/journey-pack-registration.json:311`),
  and hot refresh succeeds in the same PID 4514
  (`journey-pack-hot-refresh.json:18`). The later hosted-button **R12→R13**
  update succeeds through health and verification, but the restarted host fails
  the **existing-pack gate before the update task**
  (`journey-result.json:137`, `:150`, `:217`). The task-prefixed receipt is
  the failing observation, not the unprefixed initial success:
  `journey-task-fresh-update-task--journey-pack-registration.json:281` has
  Runtime epoch 2, `:286` mode existing, `:289` a clear outbox, `:295` the
  missing-ready problem, and `:299` the new Runtime identity. Chiptune is
  entirely absent from its capabilities, rather than merely marked unavailable.
- **direct-macos:** the R0 handoff and subsequent R9→R12 candidate update
  complete. The candidate task newly adds Chiptune, then fails the **added-pack
  hot-refresh gate**, before executing the task. This is not the existing-pack
  gate: `ev/direct-macos/before-cleanup/journey-task-candidate-working-task--journey-pack-registration.json:286`
  says added, `:289` retains the committed Chiptune refresh, and `:304` says
  registered false. The hot-refresh receipt has no after observation and false
  at `journey-task-candidate-working-task--journey-pack-hot-refresh.json:11`.
- **direct-macos-fresh:** initial add/hot refresh and the post-update existing
  gate both pass. The updated service explicitly retains the isolated HOME at
  `ev/direct-macos-fresh/before-cleanup/unit-file-before-cleanup.txt:53`.
  The post-update registration retains Chiptune, reports epoch 2, and passes
  after one poll (`journey-task-fresh-update-task--journey-pack-registration.json:17`,
  `:296`, `:309`, `:311`).

## First causal events and code

Both failures split the CLI's personal collection from the service's collection
by running under different HOME values.

**Linux:** the update worker starts under the user systemd manager's actual
account home. The first visible consequence is the browser cache moving from the isolated
home (`ev/direct-linux-fresh/before-cleanup/install.log:1008`) to the account
home (`update-bootstrap.log:1013`). The manager environment is independently
logged as `HOME=/home/runner` at `update-bootstrap.log:1053`.
The updated unit then persists that HOME at
`ev/direct-linux-fresh/before-cleanup/unit-file-before-cleanup.txt:29`,
while the installed pack remains under the isolated journey home
(`journey-pack-chiptune.log:10`, task-prefixed `journey-pack-outbox.log:1`).
`astrid/installer/update_job_platform.py:285` launches systemd-run without
passing the durable descriptor's recorded home (fixed at line 288).
`astrid/installer/service.py:1307` only retains an old service HOME on darwin,
so the Linux update renders its ambient account home into the new service.
`GenericPackHost` correctly resolves the personal root from that home
(`astrid/core/execution/generic_host.py:6621`; `astrid/personal_packs_root.py:21`).
The candidate CLI still discovers the installed Chiptune tree after the update
(`journey-task-fresh-update-task--journey-packs-list.json:25078`), ruling out
source deletion by publication or snapshot cleanup. There is no committed refresh
to replay after restart: the earlier transaction was already acknowledged, under
the original home.

**macOS handoff:** the handoff service uses the fixed `program/bin/runtime`
launcher with no HOME in the entire 30-line plist
(`ev/direct-macos/before-cleanup/unit-file-before-cleanup.txt:14`).
The generated launcher embeds the install selection's home in its pathname
(`astrid/installer/boundary_registration.py:143`), but formerly did not set
HOME before importing Runtime (`:178` through the former `:183`). Thus
selection succeeds while pack discovery uses launchd's account home. The
candidate's Runtime startup is in the real-home log
(`runtime-real-home-runtime.log:46`), matching the failing receipt's identity.
The CLI installs under the isolated home
(`journey-task-candidate-working-task--journey-pack-chiptune.log:10`), so the
service never sees that outbox. Service.register deliberately retains the
handoff definition (`astrid/installer/service.py:1323`), unlike a fresh install.

Linux's original `service-pack-host.log:29` shows the old host stopping;
`runtime-real-home-service-pack-host.log:28` shows the new PID 9056 registering
successfully without Chiptune. Its optional bundled-pack quarantine messages
and Hivemind census warning also occur in the old log and do not mention
Chiptune; they are not its cause. The Runtime registration is current and the
host alive; its inventory simply lacks the pack. The original refresh log
says `registered` and the original hot-refresh receipt proves success.
For macOS handoff, `runtime-service-log-status.json:11` records
service-pack-host.log absent; the launchd stdout/stderr receipts are empty.
There is no receipt evidence of a digest rejection or a failing refresh
callback. Pending under a different HOME explains why no callback runs.

## Commit attribution: the supplied regression interval is not supported

The requested first-parent log has exactly the three named merges. Their diff
changes pack publication, committed refresh authorization, and verified
execution relocations. None changes these installer launch paths. The new
pre-success capture close is unconditional, so it does also run on Linux;
however Linux selects file-lease capture (`generic_host.py:4859`) whose cleanup
only closes file descriptors (`:4918`), not portable snapshot removal. The
receipt still lists the original installed pack after that cleanup.

The relevant files are byte-identical at 306c7b065 and 313bbd46f:

- update_job_platform.py Git blob `a751700e5e8f03f9e7d74362ec196b964cb51fcf`;
- boundary_registration.py Git blob `24f646a069fd7010a85336b8fc4824bdfe469200`.

`git blame` attributes the handoff launcher environment code to
**64392ea03** (2026-11-04). The Linux launch omission is already present in
**2958bacea**, the checkout's shallow history boundary; this checkout cannot
establish its original introducing commit. The Linux `_launch_home` darwin-only
branch is **2ccca8e4d4**; service HOME pinning was extended to Linux in
**040a2f72c**. All predate the named range. No evidence supports naming one of
35c170e39, 29fbd08c0, or 313bbd46f as the introducing commit. The supplied older
keep-going run's passing claim does not include its actual service HOME or
collection state here, so that contrast cannot establish causation. This is
an Agent launch-environment defect exposed by the isolated journey, not an
incorrect harness readiness check. No harness change or weaker gate is needed.

## Repair and proof

- Pass recorded HOME explicitly to Linux's transient update job, as the macOS
  update descriptor already does.
- Pin HOME in the generated handoff launcher to the same home already embedded
  in its install-selection path. Do this without changing the retained service
  definition or its strict ownership verification.
- Two tests in `agent/tests/test_installer_pack_home.py` use real install_group,
  actual GenericPackHost discovery, registration and outbox acknowledgement,
  with fake Runtime transport and simulated OS-manager environment inheritance.
  One installs/refreshes and executes/settles Chiptune (including capture
  cleanup), launches an update under the account manager, then restarts and
  registers. The other executes the generated handoff launcher
  under a different account home and adds/refreshes/registers the pack from the
  install shell. Both fail on untouched 313bbd46f (regression-before.log).
- Existing exact systemd argv assertion updated in test_update_job_platform.py.
- No changes to refresh authorization, snapshots, or publication policy.

These are local launch and registration proofs, not a rerun of the hosted
macOS/Linux matrix. Native manager verification and hosted receipts remain
follow-up validation for the release owner. No recovery command or external
issue/PR has been executed. This report is a ready-to-post incident draft.

## Local test record (complete)

All commands run from agent/ with the supplied venv, PYTHONPATH pointing at
agent/, no pytest cache provider, and TMPDIR/basetemp under this workdir's tmp/.
Disk is checked before every run and tmp contents are removed between runs.
The workspace remained below 600 MB through the core runs; installer wheel
fixtures have brought the observed peak to approximately 1.2 GB so far.

- Focused launch/handoff tests: **119 passed, 1 platform skip**
  (`focused-after.log`).
- Initial tests/core/pack: **502 passed, 14 known failures**, 40 selected browser
  cases excluded, and 7 browser-fixture setup errors. Those 7 cases were from
  three extra functions that also consume the browser fixture.
- Corrected transaction retry, excluding all ten browser-fixture functions:
  **143 passed, 47 excluded** (`transaction-tests.log`). All other valid pack
  test results carry forward unchanged. The 14 failures are exactly the supplied
  13 R8 refusal failures and V3 non-strict quarantine failure. Build-hook contract
  tests were not collected.
- tests/core/execution: **2133 passed, 17 failed, 3 skipped, 543 excluded by the
  configured lane, 47 errors** (`execution-tests.log`). Forty-five errors are
  `ModuleNotFoundError: tests.test_verified_host_launch`: tests import producer
  fixtures beside Runtime source, but the venv contains a wheel without those
  fixtures. The other two errors are the attempt-root admission fixture and
  an undeclared Darwin-only skip on Linux (the repository rejects ad hoc skips). The failed selectors were compared against the original launch/host modules
  as recorded below.
- Selected generic-host refresh/registration/outbox tests: **38 passed, 1 failed**
  (`refresh-registration-tests.log`). Failure expects the implicit personal
  collection from a host constructed without personal_collection=True; that
  constructor behavior is unchanged by this patch.
- Registration/schema/continuation/boundary companions: **129 passed, 1 failed**,
  2 integration-lane exclusions (`registration-companions.log`). Failure expects
  registration-recovery copy but receives the existing handoff-uninstall refusal.
- Every test_installer_*.py: **1932 passed, 123 failed, 18 skipped, 95 excluded**
  (`installer-tests.log`). All files were supplied explicitly by the serial runner.

Runtime environment limitation: ASTRID_RUNTIME_CHECKOUT is unset. The available
cx-base/runtime checkout is 9fc53b771134940aaac901e4cfc5d03c1db1a20a; its
runtime_protocol/service.py and astrid_runtime/bootstrap.py match the installed
wheel byte-for-byte. That checkout lacks the required 42ae24aff object. Matching
Runtime source was requested from the orchestrator; neither that checkout nor
the installed venv was modified.


## Final controls and outcome

- Final expanded Chiptune regressions: **2 passed** in 10.60s
  (`regression-final.log`). They check `chiptune.sfx`; Linux executes and settles
  the installed action before the update/restart and readiness check.
- Identical final test file using the original **313bbd46f** host and installer
  launch modules: **2 failed**, with exactly the missing ready capability after
  restart and unconsumed outbox after handoff (`negative-313bbd46f.log:62`, `:135`).
- Identical control using the corresponding **306c7b065** modules: **2 failed**
  with those same symptoms (`negative-306c7b065.log:62`, `:135`). These are explicit
  source overlays for the three relevant modules, not claims that an entire
  306c7b065 checkout or the historical hosted keep-going run was reproduced.
- The 142 failed selectors from execution, selected registration, companion,
  and installer suites, plus the two non-fixture-source errors, were retried
  together: **142 failed, 1 passed, 2 errors**. Loading the original 313bbd46f
  host and launch modules produced exactly the same failure/error node sets:
  **142 failed, 1 passed, 2 errors** (`execution-failure-retry.log`,
  `execution-failure-pristine.log`). The extra pass is the test whose teardown
  also errors. The overlay is confined to the test process; subprocesses still
  use the working tree. It is evidence of unchanged local failure behavior,
  not full pristine-tree release qualification.
- Exposing the matching local Runtime producer fixtures in a separate process
  (without altering venv/package files) resolved the 45 missing-fixture setup
  errors: **43 passed, 2 failed** (`runtime-fixture-retry.log`). The two failures
  are orchestrator imports of `external_pkg`. Both also fail with the original
  313bbd46f host and launch modules (`runtime-fixture-pristine.log`).

The source overlays are exported with git show and installed by the local
baseline_proof_plugin.py only for their test process. Runtime fixture exposure
first verifies that service.py, external_pack_sources.py, and
verified_host_launch.py match the installed wheel byte-for-byte. All temporary
plugin links inside agent/ were removed. Tests and controls preserve original
failure logs and their actual pytest exits; wrapper success is not a test pass.
The serial runner writes exact argv records to *.command.txt and inner exits to
test-exits.txt. The original first pack/focused commands remain in the tool
transcript; their selectors and results are described above.

Result: local repair and regression proof are complete; the broader local
suites are **not green**. The observed baseline/environment failures above are
reported rather than silently treated as passes or added to a skip list. The
hosted matrix was not rerun, and the supplied environment does not provide the
Runtime 42ae24aff source pin for native qualification.

For the release owner, apply the two launch-boundary changes to the candidate
and rerun direct-linux-fresh, direct-macos, and the direct-macos-fresh contrast
with the frozen harness. Review the resulting service HOME, task-prefixed
registration, and outbox receipts. Changes remain uncommitted as requested.
