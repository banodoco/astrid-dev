# PDC-5 — Integrated qualification of Plan 72 (25 November 2026)

[Plan 72](../../../../plan.md) · [Tasks](../../../../tasks.md)

**Qualified head:** `project/72-composable-project-delivery` at `7c956ded1767fc2565a0a74f6706398785481da9`. It contains PDC-1 (`c29908e5`), PDC-2 (`a523fdc0`), PDC-3 ([#1904](https://github.com/banodoco/astrid-dev/pull/1904), merged at `23e74d34`), PDC-4 ([#1919](https://github.com/banodoco/astrid-dev/pull/1919), packet head `f0a20eef7cccc55d23974ba3dcdd411b97132ffb`) and current `main` `b92ec11631b2c14f2c3cc089d18cd8597e52ec7e`. This evidence file is the only commit added after it.

## Results

| Proof | Result |
| --- | --- |
| `python3 scripts/astrid_dev.py check` | exit 0 |
| `python3 -m unittest discover -s scripts -p "test_*.py"` | 553 tests, OK |
| `astrid_dev.py list` | shows `project-delivery always Validate authored project-delivery relationships` |
| Public export, `python3 scripts/export_public_vision.py --revision 0000000000000000000000000000000000000000 --output <file>` | `main` `b92ec116` and this head both write 194,514 bytes, SHA-256 `03635f424df9f26846388b14a2c9cc562a46ae72632d0e2594bf1f3a4c46be1d`; `cmp` reports identical. (The 190,022-byte figure in the packet was measured earlier on an older tree; the comparison that matters is main against head.) |
| `python3 scripts/project_delivery.py check` | `Validated 248 records and 297 typed relationships`, exit 0 |
| `python3 scripts/project_delivery.py goal principle:open-by-design/open-decisions-and-working-knowledge` | prints goal → gap → project → release paths, for example `goal:principle:open-by-design/open-decisions-and-working-knowledge -> gap:CA-003 (primary) -> project:53 (primary) -> release:14`; exit 0 |
| `python3 scripts/project_delivery.py issue 578` | `issue:578 -> release:14` (frozen Release 14 ledger); exit 0 |
| `goal principle:nonexistent/nothing` and `issue 4242424` | no output, exit 0: an unknown id returns no recorded relationship and is not an error, as the guide in `docs/extending.md` states |
| Hosted `documentation` and `vision-consumer-contract` | on the completion pull request for this head (see the PR) |

## Limits

- The no-output result for an unknown id is the existing behaviour; PDC-5 documents it and does not change it.
- Plan 72's own checks run here; Plans 71 and 73 are not part of this head.
