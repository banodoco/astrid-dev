Date: 2026-11-23
Kind: issue
Source: Plan 88 TE-3 ripple repair
Resolved by: —

A delegated focused pytest command accidentally gained a trailing `.` after three named test files, starting repository-wide discovery against the run's local test limit. The manager noticed the actual process arguments and interrupted it; its partial output is not proof. The runner should reject broad positional paths when a run authorizes only explicit selectors, and display the final expanded command before execution so this failure is caught before pytest starts.
