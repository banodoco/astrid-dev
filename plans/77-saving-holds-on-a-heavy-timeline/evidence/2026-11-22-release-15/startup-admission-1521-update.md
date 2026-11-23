# Plan 77 startup admission evidence for #1521

On this Linux sandbox, two installed Runtime revisions were compared against the same authenticated signed fixture with 300 clips, ten occurrences and restored head v30. Both comparisons used the direct lifecycle equivalent after a clean stop of the adopted realm. Restore and adoption were untimed setup. The ordinary managed restart of this exact fixture remains unresolved here.

| Trial | Stock release tree `23310dc8` | First cut `8dfa96ac` |
| --- | --- | --- |
| Default 120 s admission, command invocation to exit or health | Refused at 121.481 s, without health or editor access | Refused at 124.248 s, without health or editor access |
| Separate 600 s admission, Runtime birth to health | 159.499 s | 157.009 s |
| Separate 600 s admission, Runtime birth to fully writable editor | 482.812 s | 163.599 s |
| Same-process fresh browser reopen with zero intervening commit POSTs | 14.941 s | 36.445 s |

The separate 432-clip ordinary managed failure exercised a workspace-inspection subprocess on Round 5 Runtime `d7be2f04`. The 300-clip stock measurement failed inside the new direct Runtime daemon. The shared realm inspection path performs the semantic timeline history pass even after a clean shutdown. Prior clean admission metadata can skip some deep CAS and event-chain checks. The timeline verifier starts with an empty in-memory memo. [Inspection and clean marker](https://github.com/banodoco/astrid-runtime/blob/8dfa96aca3bbe08ffc9824cdf799354d028acbff/runtime_protocol/store.py#L7010-L7024) · [Unconditional history check](https://github.com/banodoco/astrid-runtime/blob/8dfa96aca3bbe08ffc9824cdf799354d028acbff/runtime_protocol/store.py#L7521-L7525)

The first cut narrows what the editor verifies after it reaches health. The startup history pass remains in its source. The current managed launcher cannot fall back to a writable editor or extend admission automatically. A configured OS login service can repeat the same launch after failure. Startup comes first in the next design because a refused restart blocks access to editing and saving.

Previous startup defaults stopped both daemons before browser navigation. With the separate 600-second ceiling, stock used 157.61 CPU seconds to health and the first cut used 155.62. Main-thread samples at 30 and 120 seconds place both in whole-realm history verification. Stock's compiled navigation took 320.083 seconds and the first cut's took 4.452 seconds. Both verified the same signed head with zero document commit POSTs. Main-thread samples at 30 and 120 seconds show `RealmStore.inspect_realm → integrity_errors → _verify_accepted_replay` and accepted sequential-capture validation. Stock's only scoped reopen history request took 7.600 seconds, and stock reached writable before the 15-second slow-reopen sampling point. The 36.445-second no-save reopen spent 34.542 seconds in its own verified-head request. A separate sample shows sequential-capture replay inside that request. The first profile's only verified-head request took 1.278 seconds and had already finished. Neither profile requested the history page, and the signed head remained unchanged. These samples identify the work; the memo miss cause remains open.

The two extended measurements are individual samples. The 300-clip ordinary managed restart and reopening after one confirmed save remain unresolved. [Managed 432-clip receipt](../2026-11-22-432clip/managed-start/RESULT.md) · [Paired measurements and sample hashes](round7-direct-restart.json)
