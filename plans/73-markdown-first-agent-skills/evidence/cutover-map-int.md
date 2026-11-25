# MSC-9 cutover map — absorption round 1 (P73-INT)

Previous ported main: `2761114f93452d7c3110b71a9b55a5d4dc36490d`. Source main: `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8`. Project base after main merge: `bd7b63600de248ed671091c295994995c91eb131`.

[Source comparison](https://github.com/banodoco/astrid-dev/compare/2761114f93452d7c3110b71a9b55a5d4dc36490d...fd8a9a04accc2634e2cd9f7ba4916da3679f0da8); [Part A](https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7152197122); [Part B authority](https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7152948954). The relevant source commits below carry the original edits; `ff119a093a0a46240275ecd06c877fb9aa0314b3` also carries the two Plan 84 replacements in its merge diff. The existing split maps remain unchanged.

| Source path | Destination path | Source main | Relevant commit | Disposition |
| --- | --- | --- | --- | --- |
| `skills/roles/astrid-dev-manage/workstreams/ai-studio-packet.md` | `agent/roles/manager/ai-studio-packet.md` | `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8` | [`ce5d02d7345bc0ea00088e6d6fd81b4e23b43ee4`](https://github.com/banodoco/astrid-dev/commit/ce5d02d7345bc0ea00088e6d6fd81b4e23b43ee4) | Ported two changed lines; require the specified active lab run and explicit route/current run board; remove obsolete Plan 84 link. |
| `skills/roles/astrid-dev-manage/workstreams/astra-reflection.md` | `agent/roles/manager/astra-reflection.md` | `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8` | [`ce5d02d7345bc0ea00088e6d6fd81b4e23b43ee4`](https://github.com/banodoco/astrid-dev/commit/ce5d02d7345bc0ea00088e6d6fd81b4e23b43ee4) | Ported one changed line; require a current lab run with an explicit run board. |
| `skills/shared/workstreams/astrid-dev-gap/SKILL.md` | `agent/shared/workstreams/gap.md` | `fd8a9a04accc2634e2cd9f7ba4916da3679f0da8` | [`4a7c93b81ee507545d8bcf5c5327aae8fd564004`](https://github.com/banodoco/astrid-dev/commit/4a7c93b81ee507545d8bcf5c5327aae8fd564004) | Ported five changed lines with three-level relative links to the canonical gap rule; records the existing migrated home missing from the split maps. |

Incoming links into `skills/` are deferred to MSC-6 by the orchestrator's decision. Proof is reserved to the orchestrator; no proof pass is asserted here.
