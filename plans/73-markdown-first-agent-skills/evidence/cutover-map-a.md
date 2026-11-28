# MSC-3 cutover map — half A (P73-02)

Migration base: `24dbb8dcd4c7628307c1ddd727a9df79827d041e`. Source main merged by MSC-1 (M, last main revision ported): `2761114f93452d7c3110b71a9b55a5d4dc36490d`. Project packet base: `7f9f997899b9c69b75ecb20382c77f390cdd00c1`.

Each source's last commit is its latest path-specific commit reachable from M. The seven existing documents carry the net change of meaning in the source range; four new role-owned documents carry the complete source procedure without a standalone skill flag. Shared routing rules stay at the canonical run-contract link, including the per-card review rule restored by P73-03. This is the half-A map only.

| Source path | Destination path | Last source commit at M | Disposition |
| --- | --- | --- | --- |
| `skills/roles/astrid-dev-lead/SKILL.md` | `agent/roles/leader.md` | `e092cc55fcf5555b008005bf18062df4966b4cbc` | ported |
| `skills/roles/astrid-dev-lead/workstreams/multi-manager-release.md` | `agent/roles/leader/lane-orchestrators.md` | `9cb8eb9d1b136f902f64fff00c8799e0b3b06e07` | ported |
| `skills/roles/astrid-dev-lead/workstreams/lane-orchestrators.md` | `agent/roles/leader/lane-orchestrators.md` | `e092cc55fcf5555b008005bf18062df4966b4cbc` | new |
| `skills/roles/astrid-dev-manage/SKILL.md` | `agent/roles/manager.md` | `e092cc55fcf5555b008005bf18062df4966b4cbc` | ported |
| `skills/roles/astrid-dev-manage/workstreams/chatgpt-packet.md` | `agent/roles/manager/chatgpt-packet.md` | `9cb8eb9d1b136f902f64fff00c8799e0b3b06e07` | ported |
| `skills/roles/astrid-dev-manage/workstreams/whole-project.md` | `agent/roles/manager/whole-project.md` | `e092cc55fcf5555b008005bf18062df4966b4cbc` | ported |
| `skills/roles/astrid-dev-manage/workstreams/ai-studio-packet.md` | `agent/roles/manager/ai-studio-packet.md` | `3af388f316a1dc93911c81f8498257272412e73d` | new |
| `skills/roles/astrid-dev-manage/workstreams/astra-reflection.md` | `agent/roles/manager/astra-reflection.md` | `3af388f316a1dc93911c81f8498257272412e73d` | new |
| `skills/roles/astrid-dev-manage/workstreams/live-loop.md` | `agent/roles/manager/live-loop.md` | `0fb17c72085c5c05f463d9dd93daca740fa67307` | new |
| `skills/shared/glossary.md` | `agent/shared/glossary.md` | `0fb17c72085c5c05f463d9dd93daca740fa67307` | ported |
| `skills/shared/workstreams/astrid-dev-plan/SKILL.md` | `agent/shared/workstreams/plan.md` | `7cfc8e12ab810e8778184f8b9f7e184b673d8651` | ported |
