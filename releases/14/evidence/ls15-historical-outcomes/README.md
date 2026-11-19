# P55-09 historical pytest outcomes

The receipt answers [mailbox request 7012517139](https://github.com/banodoco/astrid-dev/issues/796#issuecomment-7012517139). It covers the historical destination e3795656 and candidate e7570b62. The current 978fb66c comparison is separate.

| Source job (attempt 1) | Head | Primary IDs | Passed | Failed | Error | Skipped | Pytest step exit |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Base integration 3](https://github.com/banodoco/astrid-agent/actions/runs/44465860262/job/135363367286) | e3795656 | 523 | 364 | 96 | 62 | 1 | 1 |
| [Candidate integration 3](https://github.com/banodoco/astrid-agent/actions/runs/44476086205/job/135396881455) | e7570b62 | 526 | 357 | 106 | 62 | 1 | 1 |
| [Base unit 6](https://github.com/banodoco/astrid-agent/actions/runs/44465854222/job/135363346114) | e3795656 | 5,003 | 4,774 | 219 | 4 | 6 | 1 |

[Download the gzip-compressed JSON](historical-outcomes.json.gz). Its SHA-256 is `c959ffa2b4d523827b0b58ffbf2c02ab347669c5006a1fd1c05b8109ca9498ee` (117,089 bytes). Each job record includes the full commit, run, raw-log SHA-256 and byte count. The three original jobs ran pytest directly. Their exit codes come from the corresponding Steps logs.

**Matching an exact pytest ID.** Look it up in `jobs[job_id].outcomes_by_id`. If absent, hash the exact unmodified full pytest node ID as UTF-8, without a newline, and look up its lowercase SHA-256 hex digest in `outcomes_by_full_id_sha256`. That table preserves exact identity when a parameter contains paths, URL-like text, or other unrestricted literals. Every observed primary ID has exactly one representation. Readback matched all 6,052 job/ID outcomes to the three original logs.

The unit-6 pytest summary reports 252 failures, including 33 failed subtests under three parents. Primary outcomes and failed-subtest counts by parent are separate. The receipt retains the observed outcome of each parent and pytest’s separate 93-passing-subtests total. It does not enumerate individual subtest identities. General ERROR or SKIPPED outcomes use the status printed by pytest; they do not establish a test-body outcome.

**Nine historical regressions.** The `integration_changes` list gives each ID, its PASS→FAIL change in the call phase, the original reported exception, repository-relative frames and the candidate log line where its traceback starts. Four audio assertions report no child engine events. Five image/video cases propagate a worker-startup assertion. Those frames show where each historical run stopped. Behavior after the failure and production causation remain unverified. Candidate-only and base-only IDs in shard 3 can migrate across shards, so this receipt alone cannot qualify the full integration suite.
