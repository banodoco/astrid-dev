# Tasks — Agent tests

[Plan](plan.md) · [Inputs](inputs.md)

**Owner:** the planning session `session_011EzfW1gtAhRQwk8pgJMzhG`.

| Task | Route | Depends | Scope | Done when | Progress |
| --- | --- | --- | --- | --- | --- |
| AT-1 Format, runner and check | X | — | `agent-tests/README.md`, `scripts/agent_tests.py`, `scripts/test_agent_tests.py`, the `agent-tests` check, the `agent-test` command | Unit tests pass; `check` passes | [x] |
| AT-2 Golden path | S | — | `agent-tests/golden-path.md`, from three `N` inventories | Every line cites a document or a parent rule | [x] |
| AT-3 Home in improve and the principles | X | AT-1 | `improve.md` (Agent tests, Synthesize), principle 11, glossary, `extending.md`, `agent/README.md`, ledger | `check` passes; skills build | [x] |
| AT-4 H3 chain cases | X | AT-2 | Five cases under `agent-tests/cases/h3-*` | `agent-test list`; `check` | [x] |
| AT-5 General cases | N | AT-2 | Six cases | `check`; each Expect line grounded | [ ] |
| AT-6 Write the four parent rules at their homes | X | AT-2, owner answers | `run-contract.md` (authority, clock, host), `start-session.md` (hand-off); remove the copies they replace | The cases that found them re-run clean | [ ] |
| AT-7 Run and record every case | N actors, high-judgment judge | AT-4, AT-5 | `agent-tests/results/` | `agent-test status` shows every case run | [ ] |
| AT-R Review | high-judgment | AT-1 to AT-7 | Read-only | Verdict; findings become rows `AT-R.<n>` | [ ] |

## Load-bearing moments

- **After each task:** `python3 -m unittest discover -s scripts -p "test_agent_tests.py"` and `python3 scripts/astrid_dev.py check`.
- **Before review:** the full astrid-dev CI on the PR.
