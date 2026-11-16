# K1a Linux-gate bounded card evidence

Repository: `/workspace/scratch/cd53b069f320/p39-repair/astrid-agent`

Base: `16ef29bf8cd9d9df82c6f2a892feff3dffc44d70` (tree `f155b695df8c89b375e761ae1a4f51470c41bc85`).

All proof raw output and exit values are saved in this directory as numbered `*-pre.log`, `*-pre.exit`, and, for migrated rows, `*-post.log`, `*-post.exit`. Each proof was invoked exactly as listed in `K1a-linux-gates.md`, sequentially. Failed proofs were not retried and their gates and expectations were left unchanged.

## Dispositions

| # | Card | Disposition | Pre / post exact result | Evidence / cause |
|---|---|---|---|---|
| 1 | `tests/core/generation/test_engine_readiness.py` | HOLD, unchanged | pre: 9 passed, 60 errors, exit 1; no post | `01-engine-readiness-pre.log`: setup errors because the retained supervisor was unavailable until the engine deadline; representative error is `CustodyUnresolved("supervisor unavailable; explicit recovery required")`. The independently cleared ownership finding only authorized changing the Linux OS gate; it does not authorize masking this failure. |
| 2 | `tests/test_boundary_handoff.py` | HOLD, unchanged | pre: 36 passed, 44 failed, exit 1; no post | `02-boundary-handoff-pre.log`: several cases fail with `Managed paths cannot contain links` at the worker `astrid-agent.env/venv` path or `runtime_checkout must be an explicit absolute pinned checkout path`; other exact assertion details are retained in the raw log. |
| 3 | `tests/test_boundary_registration.py` | HOLD, unchanged | pre: 8 passed, 64 failed, exit 1; no post | `03-boundary-registration-pre.log`: failure evidence includes the worker `astrid-agent.env/venv` symlink rejection (`Managed paths cannot contain links`). |
| 4 | `tests/test_installer_r0_entry.py` | HOLD, unchanged | pre: 49 passed, 1 failed, exit 1; no post | `04-installer-r0-entry-pre.log`: `test_captures_match_real_r0_evidence` takes an undeclared direct skip because local R0 evidence is absent. The manual-artifact gate was not changed. |
| 5 | `tests/test_installer_update_end_to_end.py` | MIGRATED | pre: 4 passed, exit 0; post: 4 passed, exit 0 | Only module `pytestmark` changed from the exact Linux skip to `pytest.mark.linux_native`. This covers the real Update request/helper path with loopback prepare URLs and simulated `systemctl`/`systemd-run`. AST comparison confirms all other module content is identical; 4 selected cases before and after. |
| 6 | `tests/test_installer_update_legacy_record.py` | HOLD, unchanged | pre: 10 passed, 1 failed, exit 1; no post | `06-update-legacy-record-pre.log`: `test_sweep_resolves_a_record_without_home_once_its_unit_has_finished` expected `failed`, received `recovery-needed`. |
| 7 | `tests/test_update_from_field_states.py` | HOLD, unchanged | pre: 18 passed, 30 failed, exit 1; no post | `07-update-from-field-states-pre.log`: failures include `runtime_checkout must be an explicit absolute pinned checkout path` and `Managed paths cannot contain links` at `astrid-agent.env/venv`. |
| 8 | `tests/test_installer_app_update.py::test_running_foreground_lock_refuses_with_xdg_override_before_writes` | MIGRATED | pre: 1 passed, exit 0; post: 1 passed, exit 0 | Only that test's Linux skip decorator changed to `pytest.mark.linux_native`. Its contract is the XDG-filtered Pinokio foreground-lock refusal before writes. AST comparison after removing that decorator is identical; selected case count 1 before and after. |
| 9 | `tests/test_installer_pinokio_custody.py::test_custody_retains_foreground_and_legacy_locks_when_xdg_is_filtered` | MIGRATED | pre: 1 passed, exit 0; post: 1 passed, exit 0 | Only that test's Linux skip decorator changed to `pytest.mark.linux_native`. Its contract is retention/release of the two Linux lock paths while XDG is filtered and custody is attached/closed. This is the ownership-cleared XDG case. AST comparison after removing that decorator is identical; selected case count 1 before and after. |

## Eligibility and scope

`tests/lanes.py` defines `linux_native` as available only on Linux and associates it with `unit-shard-ubuntu-latest`; it is not default-off. Thus the three migrated cases remain eligible in the Ubuntu default unit shard. Native Windows and Darwin do not select them because their test contracts are Linux systemd/XDG or Linux lock-path simulations. No Windows or Darwin behavior is asserted by these tests. The migrations add no `integration` mark and change no lane lists, bodies, assertions, fixtures, parameters, or other marks.

Plan 38 boundaries were read from `plans/38-one-process-identity/{plan.md,tasks.md}`. Plan 38 owns process birth identity, peer custody/signaling, and source-closure provider work. The three migrated contracts exercise installer update scheduling/simulation and Linux XDG lock behavior, and do not assert native provider/token identity, process birth parity, host spawn, or closure semantics. Plan 55 boundaries were read from `plans/55-local-speed/{plan.md,tasks.md}`. The update-job tests are not warm local generation jobs and make no warm-session, transport, or settlement budget assertion. The exact native audit-token test remains untouched.

The full baseline files for the three migrations are saved under `baseline/`. AST comparisons on the current source, after removing only the exact gate node in each compared tree, found identical ASTs. For the module-mark migration, the module test names are unchanged; post/pre pytest selected counts match exactly (4/4). For each selector migration the exact node ID and count remain the same (1/1).

This evidence covers only these nine bounded cards; it is not an overall K1a completion claim.
