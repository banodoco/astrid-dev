# OT-1 — baseline and parity oracles after Plans 71–73

Recorded 25 November 2026 by the orchestrator on a fresh clone of astrid-dev `main` at `7cf00a5ed5ded3f4ca1b34b97214d693ab584fdd` (the merge of Plan 73; the later `cc4520eb` adds only Plan 95's records). These are the oracles OT-19 to OT-22 compare against.

| Oracle | Command | Result |
| --- | --- | --- |
| Repository check | `python3 scripts/astrid_dev.py check` | exit 0 |
| Full unit suite | `python3 -m unittest discover -s scripts -p "test_*.py"` | 700 tests OK, exit 0 |
| Public vision export | `python3 scripts/export_public_vision.py --revision 0000000000000000000000000000000000000000 --output <file>` | prints "Public vision content OK: 4 pillars, 4 principles, 22 gaps, 95 projects"; output file SHA-256 `aea22cb5faec26b5a121f04b1c126e1d4bdc8d278dd3e8e7c010625c4533cdf6` |
| Golden output | `sha256sum scripts/fixtures/golden.txt` | `42ffd1ff63aa41430a30bf5aeb43196738359093b5f3f607dc14467ed2a72a68` |
| Skill build output | `python3 scripts/astrid_dev.py skills build` twice; SHA-256 of the sorted per-file SHA-256 list of `.generated/skills` excluding the `repo` symlinks | `264d74d49a4726bc9098da7efc102ae7b40afd2f6236d20d40e319a06ebfe724`, identical on both builds |
| Project delivery | `python3 scripts/project_delivery.py check` | "Validated 249 records and 307 typed relationships" |

**Limit.** The packet card also names the outputs of `project_delivery.py goal <real goal id>` and `issue <frozen issue>`. The orchestrator did not find a goal or issue id that prints output on this tree (the commands print nothing and exit 0 for the pillar and gap-derived ids it tried), so OT-22 compares the `check` result and the `test_project_delivery*.py` tests, which cover goal and issue traversal on fixtures, instead. If OT-19 finds a real id, it adds the output hash here.

Hosted CI on the Plan 73 merge: `documentation`, `vision-consumer-contract` and CodeQL green. One timing test (`test_installed_symlink_polling_during_repeated_exchanges`) failed once on a hosted run and passed on the re-run and on every local run; it is tracked as a follow-up.

**Otto repository (OT-2).** `banodoco/otto`, public, MIT licence and placeholder README, `main` at `16e02f53fac8d9c5f8c65edc1bf3beb13b9420dc`. Branch protection on `main` is not set: it needs the owner or an organisation admin (a manual step). No secret is configured.
