# Inputs: installer consent

[Plan](plan.md) · [Tasks](tasks.md)

## Starting code

The following bases are historical observations from the 4 Nov 2026 audit, not execution bases. Freeze the then-current target for each changed repository before work; do not assume a recorded branch or SHA is still current.

| Repository | Historical branch + SHA | Retained work / donor SHAs / unpublished changes | Candidate branch | Intended destination |
|---|---|---|---|---|
| Agent | `pre-main` · `e50d9a6daf2124a21f9cdf78826253ddadec7f83` | Accepted donors, in order: `6087e0fbe7e2bd45c9911ff5cf1093614d715863` → `19229d2325879c12e01c6bcdc604fd743b158ece`. Both sibling tips are required; sibling merge probes passed. | Fresh isolated create-only branch from frozen destination base; candidate name TBD. | `pre-main` |
| App | `pre-main` · `878c28df7a6c80fa9aaa6540c5fccad95473e7c1` | Accepted donors, in order: `e97450cff0ed570cfaa077369b28c269b562bd1e` → `9ddff8efbc9e914efbe04cb49da2648c4feb4db4`. Both sibling tips are required; sibling merge probes passed. | Fresh isolated create-only branch from frozen destination base; candidate name TBD. | `pre-main` |
| Runtime | `pre-main` · `9fc53b771134940aaac901e4cfc5d03c1db1a20a` | Unchanged producer; not a merge input. Confirm contract artifacts against the actual frozen target. | None; unchanged. | Unchanged |
| VibeComfy | `main` · `e2905d068d5851b9c32856d32b8251852a01d6dd` (no `pre-main` observed) | Unchanged producer; not a merge input. | None; unchanged. | Unchanged |
| lifecycle | `main` · `db79345536985c701b7aff2eb5eec36667aae204` (no `pre-main` observed) | Unchanged producer; not a merge input. | None; unchanged. | Unchanged |

Earlier research snapshots were Agent `01eceda...` and App `878c28...`; they are not permanent targets. The observed lock comparison was `lock2776ba` versus Runtime `9fc53b771134940aaac901e4cfc5d03c1db1a20a`; verify against the actual frozen target. No unpublished retained work was specified beyond the four accepted donors. Record any discovered retained changes when freezing sources.

After independent review, promote the exact immutable candidate heads to `pre-main` by the destination's ordinary fast-forward/create procedure. Never overwrite an earlier candidate or publish to `main`, `int`, or `r1`. The four Agent/App donors above are the only feature inputs.

## Final heads (landed 7 Nov 2026)

| Repository | Final `main` head | Previous |
|---|---|---|
| Agent | `c5a970aa3c048db1ee9c5100d1db2b4444358592` | `0b6a7aef0` |
| App | `ae6c777ca8f4afa4c98a0319b58963d2f4bbe4f8` (merge of M-01's `7165b6e7f` with 4 vision commits) | `5fa4c0909` |
| Runtime | `9fc53b771134940aaac901e4cfc5d03c1db1a20a` (pin, unchanged) | same |

Both advanced by fast-forward. Donor work credited to Dylan (@matlowai).

## Provenance and evidence boundaries

The exact accepted donor SHAs and merge order are recorded **once** in [Starting code](#starting-code). The old source-audit summaries are not live execution evidence: freeze the target anew and rerun focused acceptance checks from [tasks.md](tasks.md). The earlier M-GPU orchestration and its advisor automations remain **stopped**; this project does not resume them.

## Constraints

- Use the shared [run contract](../../skills/astrid-dev-shared/run-contract.md) for routes, bindings, source identity, and proof; preserve the accepted scoped END review and existing authorization limits.
- Only Agent and App change. Runtime, VibeComfy, and lifecycle are unchanged producers; keep their pins unchanged. No CPU generation, CE, broad suites, or full UI/SDK suite are acceptance for this increment.
- Reuse accepted donor evidence; recheck only affected behavior on the composition and final immutable tuple. Confirm Runtime contract artifacts against the frozen target.
