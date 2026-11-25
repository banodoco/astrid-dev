# MSC-9 cutover map — absorption round 2 (P73-INT)

Previous ported main: `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8`. Source main: `dbabcdbed2b31e46156cfb454242cbd711727256`. Project base after main merge: `65f7b72d91ad5f9c3a7d6c629b49c81ce8bb68fe`.

[Source comparison](https://github.com/banodoco/astrid-dev/compare/2761114f93452d7c3110b71a9b55a5d4dc36490d...9def7d1259c731b7bd85ff44e944383ff2eb548a); [Part A](https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7163190859); [Part B authority](https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7163605384). Three earlier changes are recorded in the round-1 map and are not repeated here. The existing maps remain unchanged.

| Source path | Destination path | Source main | Relevant commit | Disposition |
| --- | --- | --- | --- | --- |
| `skills/roles/astrid-dev-lead/SKILL.md` | `agent/roles/leader.md` | `dbabcdbed2b31e46156cfb454242cbd711727256` | [`9def7d1259c731b7bd85ff44e944383ff2eb548a`](https://github.com/banodoco/astrid-dev/commit/9def7d1259c731b7bd85ff44e944383ff2eb548a) | Ported six added lines: responsibilities 7 and 8, conditional decisions and harm-based shipping/freeze policy. |
| `skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md` | `agent/roles/leader/multi-manager-release.md` | `dbabcdbed2b31e46156cfb454242cbd711727256` | [`9def7d1259c731b7bd85ff44e944383ff2eb548a`](https://github.com/banodoco/astrid-dev/commit/9def7d1259c731b7bd85ff44e944383ff2eb548a) | Ported packet-owned fixes, distinct failing test ids, conditional rulings, manager cadence and candidate pin ownership; retained Markdown-first routing and Rulings. |
| `skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md` | `agent/roles/orchestrator/multi-manager-dispatch.md` | `dbabcdbed2b31e46156cfb454242cbd711727256` | [`9def7d1259c731b7bd85ff44e944383ff2eb548a`](https://github.com/banodoco/astrid-dev/commit/9def7d1259c731b7bd85ff44e944383ff2eb548a) | Ported 20-minute dispatch pass and packet-owned proof follow-up; re-pointed the single relative link to the Leader check-in anchor. |

The historical run-record wording stays untouched by decision. Proof is reserved to the orchestrator; no proof pass is asserted here.
