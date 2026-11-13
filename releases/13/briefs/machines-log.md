# Machines lane log (rulings and events; newest last)

- 23:30 Ruling (REVIEW; upheld by orchestrator): widened test rule (b). Fixtures that build an acquisition attempt without paid authority may carry realistic paid limits + deadline (setup only, assertions unchanged): test_acquisition_catalog_id, test_provider_gate_review._fresh_acquisition. Condition: LT names or adds a test that no-paid-limits/no-deadline cannot reach allocation_ready or create.
- 23:35 Ruling (REVIEW; upheld): K1's own checkpoint tests claim the machine first (_claim_machine), owner decision O3; assertions unchanged. K1 r13/machines-k1 bc3e6e7bc.
- 23:41 Event: container restart; Codex workers resumed from their session ids; WIP snapshots pushed (restv2-wip2 850b259e7, lt-wiring-wip3 3d44e203e).
- 23:57 Ruling: LT wiring r2 stopped at the three-attempt rule (b1 pending restart); escalated r3 to Astra as writer; review then goes to Sol or an independent Opus. Snapshot lt-wiring-wip4 e0f81e86f.
- 23:58 Process (owner): orchestrator hourly; message only merge-ready SHAs or blockers; test rows with the test lane directly; rulings recorded here.
- 00:19 Ruling (advisor, adopted by orchestrator, REVIEW): LT wiring is out of R13; the Astra writer was stopped. WIP kept (lt-wiring-wip4 e0f81e86f; design r13/machines-lt 58a7241c8). R13 machines scope: M1 + K1 + M2 (with M2c) + v2. M3, M4, LT wiring and M5–M9 come after release. Order: K1, then v2 (live claim/job/release on v2 before any other machines merge).
- 00:20 K1 seven-file landing proof green (217 passed); compose 05346e9fd merged cleanly; targeted re-proof running.
