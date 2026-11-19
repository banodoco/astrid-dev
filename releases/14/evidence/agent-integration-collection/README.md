# Agent #428 final hosted qualification

Source e84bbd52725cba1da7ac655771f840cb7af25fc2, destination 68e7aa8593d13eaeb6a55da1d97bed8b494df15b, previous executable 4ba3becd201779a4938aae50eada6e596bd098b4. All four current native archives agree by identity across reference selection, execution selection, native setup and JUnit testcase name/class multiplicity. Each ID belongs to one shard. All four raw exits were 1. [Source Lanes](https://github.com/banodoco/astrid-agent/actions/runs/44580869163)

|Shard|Current job|Native artifact|Selected|Calls|Call pass|Call fail|Setup error|Setup skip|Original S01 setup errors|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1|135760830820|14565176258|517|517|480|37|0|0|0|
|2|135760830740|14568302752|517|345|268|77|172|0|78|
|3|135760830760|14578048965|517|454|370|84|62|1|26|
|4|135760830794|14573251962|516|502|401|101|14|0|0|
|Union|||2067|1818|1519|299|248|1|104|

All 2,067 teardowns passed. On the actual destination each shard's original collection ended with 75 errors and exit 4. Its disjoint reference union selected exactly the same 2,067, with zero native executions. Original G1 jobs 133451220016, 133451220033, 133451219876 and 133451220087 each printed 516 primary IDs. All 2,064 were found in the current union. The historical 2,063 excludes one setup skip. Three current additions are the two Boolean parameters of test_duplicate_copies_a_head_that_already_fails_newer_rules and test_a_duplicate_of_a_valid_source_passes_the_full_validator_with_the_copy_flag_off. [Destination](https://github.com/banodoco/astrid-agent/actions/runs/44462370783) · [G1](https://github.com/banodoco/astrid-agent/actions/runs/43888589840)

All 5,952 primary phase keys match the previous executable. Three call outcomes changed. [Previous executable](https://github.com/banodoco/astrid-agent/actions/runs/44535552341)

- Shard 1, tests/core/execution/test_generic_host_child_bridge_d18.py::test_real_parent_bridge_dispatches_nested_validator_and_binds_receipt_to_child_attempt, PASS→FAIL. Line 1392 observed cancelled instead of failed. The subsequent binding checks did not execute.
- Shard 2, tests/editing_conformance/test_historical_shared_redo_authority.py::test_shared_redo_rechecks_source_archive_at_acceptance, FAIL→PASS.
- Shard 3, tests/integrations/test_managed_host_preparation.py::test_managed_host_prepares_before_sandboxed_worker[device-ambient], PASS→FAIL. Expected refusal and receipt-written wait passed. The receipt error was null at line 378, before the endpoint-ownership code and following launch/device assertions could complete. G1 passed this exact case. Attribution remains open. [G1 shard 3](https://github.com/banodoco/astrid-agent/actions/runs/43888589840/job/133451219876) · [Current shard 3](https://github.com/banodoco/astrid-agent/actions/runs/44580869163/job/135760830760)

Each original test was also invoked with pytest's ordinary integration selection on both 4ba and e84 on a local macOS host, with separate disposable homes/config roots, source-pinned Runtime 2537fed2, VibeComfy c27fe76b, and lifecycle 7f0b025e. The child-bridge case passed both times, exit 0. Log SHA256 values in parent/source order are c9763e84fbb2b611bd82c2ba8c169c5c03add4d3e9ea227f6def90923cbe4b88 and fa111a21e124a175c67c53de04bcc6d7d6bbbf7d8feae9b109ae0263fc1dd7d6. The device-ambient case errored in setup on both refs with UnsupportedPlatform (engine custody requires Linux), exit 1, no call. Log hashes are 2be9c9dcbd05aba3639fdd25c07d0a8920bab7815afe58ab64204ee7e71a698e and 6f7a12995ac1f8059c08cf6a1b9104595feac23a58873c8a0a80905c44222532. Both hosted outcomes remain recorded.

Opt-in retained 31 identical IDs with 19 passing and 12 failing calls. Installed wheel retained three identical setup errors and zero calls. Raw exits were 1 on all three refs for both lanes. Installed registry and selector each exited 1 on both executable heads. CI retained all 31,058 destination primary IDs plus four passing probes and all 619 subtest outcomes. The pin-copy guard and the real AT1.54 refusal passed. Readiness line 108 and the AT19 listener-owner refusal retain distinct dispositions. [Exact CI](https://github.com/banodoco/astrid-agent/actions/runs/44580875391)

The reviewed head landed at `b1e53baf` with parents `68e7aa85` and `e84bbd52`. Its tree `28adcd87` matches the qualifying source. The [child-bridge isolation receipt](child-bridge-isolation.json) includes both full source identities and raw exits. The two changed integration failures are tracked in [dev #1011](https://github.com/banodoco/astrid-dev/issues/1011).
