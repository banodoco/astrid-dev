# MSC-3 cutover map — half B (P73-03)

Migration base: `24dbb8dcd4c7628307c1ddd727a9df79827d041e`.

Source main (MSC-1 integration, M): [`2761114f93452d7c3110b71a9b55a5d4dc36490d`](https://github.com/banodoco/astrid-dev/tree/2761114f93452d7c3110b71a9b55a5d4dc36490d). All 14 listed source blobs were also identical at packet record SHA `5caf5a54c1542c07e87acfaa05ca12805a7635e8`. The last source commit is the newest commit on that path reachable from M, not the commit that adds this map. The [Step 1 decision](https://github.com/banodoco/astrid-dev/issues/1882#issuecomment-7150881506) approves these destinations and the combined proof of half A and B.

| Source path | Destination path | Last source commit at M | Disposition |
| --- | --- | --- | --- |
| `skills/roles/astrid-dev-orchestrate/SKILL.md` | `agent/roles/orchestrator.md` | [`e092cc55fcf5555b008005bf18062df4966b4cbc`](https://github.com/banodoco/astrid-dev/commit/e092cc55fcf5555b008005bf18062df4966b4cbc) | ported |
| `skills/roles/astrid-dev-orchestrate/workstreams/codex-cloud-sessions.md` | `agent/roles/orchestrator/codex-cloud-sessions.md` | [`e092cc55fcf5555b008005bf18062df4966b4cbc`](https://github.com/banodoco/astrid-dev/commit/e092cc55fcf5555b008005bf18062df4966b4cbc) | ported |
| `skills/roles/astrid-dev-orchestrate/workstreams/multi-manager-dispatch.md` | `agent/roles/orchestrator/multi-manager-dispatch.md` | [`9cb8eb9d1b136f902f64fff00c8799e0b3b06e07`](https://github.com/banodoco/astrid-dev/commit/9cb8eb9d1b136f902f64fff00c8799e0b3b06e07) | ported |
| `skills/roles/astrid-dev-orchestrate/workstreams/lane-orchestrator.md` | `agent/roles/orchestrator/lane-orchestrator.md` | [`bddff85e9e9ae93b82d53c52d8e98ea5fcad091e`](https://github.com/banodoco/astrid-dev/commit/bddff85e9e9ae93b82d53c52d8e98ea5fcad091e) | new |
| `skills/roles/astrid-dev-orchestrate/workstreams/measurement-box/README.md` | `agent/guides/measurement-box/README.md` | [`9acd469a5045273fe89b6511b294d515692e3dd5`](https://github.com/banodoco/astrid-dev/commit/9acd469a5045273fe89b6511b294d515692e3dd5) | new |
| `skills/roles/astrid-dev-orchestrate/workstreams/codex-in-claude-cloud/README.md` | `agent/guides/codex-in-claude-cloud/README.md` | [`2415aa26392d51bef2e19099e0f687ee4cc0584f`](https://github.com/banodoco/astrid-dev/commit/2415aa26392d51bef2e19099e0f687ee4cc0584f) | ported |
| `skills/roles/astrid-dev-orchestrate/workstreams/codex-in-claude-cloud/manager-brief.md` | `agent/guides/codex-in-claude-cloud/manager-brief.md` | [`2415aa26392d51bef2e19099e0f687ee4cc0584f`](https://github.com/banodoco/astrid-dev/commit/2415aa26392d51bef2e19099e0f687ee4cc0584f) | ported |
| `skills/shared/run-contract.md` | `agent/shared/run-contract.md` | [`9cb8eb9d1b136f902f64fff00c8799e0b3b06e07`](https://github.com/banodoco/astrid-dev/commit/9cb8eb9d1b136f902f64fff00c8799e0b3b06e07) | ported |
| `skills/shared/workstreams/astrid-dev-release/SKILL.md` | `agent/shared/workstreams/release.md` | [`281bf01a5f170540ba3b4505a5e6aa14405eff4e`](https://github.com/banodoco/astrid-dev/commit/281bf01a5f170540ba3b4505a5e6aa14405eff4e) | ported |
| `skills/shared/workstreams/astrid-dev-release/qualification.md` | `agent/shared/release-qualification.md` | [`281bf01a5f170540ba3b4505a5e6aa14405eff4e`](https://github.com/banodoco/astrid-dev/commit/281bf01a5f170540ba3b4505a5e6aa14405eff4e) | new |
| `skills/shared/workstreams/astrid-dev-green/SKILL.md` | `agent/shared/workstreams/green.md` | [`6c9719c4d8afc4859697b77c15d1dff1a623ee61`](https://github.com/banodoco/astrid-dev/commit/6c9719c4d8afc4859697b77c15d1dff1a623ee61) | ported |
| `skills/shared/workstreams/astrid-dev-iterate/SKILL.md` | `agent/shared/workstreams/iterate.md` | [`0fb17c72085c5c05f463d9dd93daca740fa67307`](https://github.com/banodoco/astrid-dev/commit/0fb17c72085c5c05f463d9dd93daca740fa67307) | ported |
| `skills/shared/workstreams.md` | `agent/README.md` | [`00f5d0ac0df2facb72033ddd3dcf15bc193112bc`](https://github.com/banodoco/astrid-dev/commit/00f5d0ac0df2facb72033ddd3dcf15bc193112bc) | ported — unchanged since migration base; map only |
| `skills/shared/workstreams/astrid-dev-release/references/sources.md` | `agent/shared/release-sources.md` | [`7f3e388d7a15b8dac71faa25d168ac0397cd4f77`](https://github.com/banodoco/astrid-dev/commit/7f3e388d7a15b8dac71faa25d168ac0397cd4f77) | ported — unchanged since migration base; map only |

The two map-only rows require no edits. The workstream structure, discovery, authority and authoring instructions move to the Markdown-first `agent/README.md` contract; legacy skill-directory names, generated indexes and `sync.sh` mechanics are superseded by that layout and generated packaging, not new rules. Release source provenance is preserved in `agent/shared/release-sources.md` (original body plus required metadata).

The old routing copies in the orchestrator and hosted Codex guides are represented by the shared `agent/shared/run-contract.md` routing and per-card review rules, not separate authorities. New lane, measurement and qualification documents are not independently packaged. The four final cross-half links into the leader and manager documents are intentionally resolved by half A; no placeholder or fallback legacy link is used. Standalone sibling link failures and combined exact-candidate proof are handled as the decision specifies.

Proof selectors (orchestrator only): `scripts/test_agent_documents.py scripts/test_skill_builder.py scripts/test_workstreams.py scripts/test_views.py`. No proof result is claimed here.
