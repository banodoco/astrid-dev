Date: 2026-11-11
Kind: fix
Source: Owner, watching Plan 48's Phase 1 run
Resolved by: —

Plan 48's run had four layers (owner, a session that wrote the brief, a Claude session hosting Codex, the Codex manager) and nobody answered for it finishing. The orchestrate skill told the hosting session to be an idle advisor, yet only that session could keep Codex alive, reach the owner or run the tasks bound to a Claude model. So it spoke of "the manager" as someone else, acted only when prodded, and left a conflicting progress PR open. The brief also came from a peer session, which both skills say is not authority, and it was long enough to contradict the skill it pointed to. The roles were recorded only in the git-ignored `run.yaml`, which no one else can read.

Now the run contract says every run has exactly one accountable agent and who it is in each setup: the manager in its own session, or the hosting session when Codex is hosted. A `Run start` line in the plan's `inputs.md` records it. The orchestrate skill has a five-line start message that the owner sends, and a rule against stacking advisors. The Codex brief names the host and has Codex write `READY` for tasks it can't run.
