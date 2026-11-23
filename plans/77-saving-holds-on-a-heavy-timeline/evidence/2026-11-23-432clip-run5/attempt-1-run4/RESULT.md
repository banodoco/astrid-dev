# Run 4 partial receipt — installer stopped

UTC 2026-11-23. The single attempt stopped in section 1. No pod was created.

- Amendment setup block: `source run4-manager/setup-block.sh`, 05:04:29–05:04:36 UTC, exit 0. Fetches completed, both worktrees were created and both pin commits made. Output was observed in the operator session; no separate full setup log was captured.
- Section 1 pre-install checks: `source run4-manager/section1-pre.sh`, 05:04:57–05:04:58 UTC, exit 0. Local mirrors and offline `checkManifest` completed by 05:05:19 UTC. Commands and checker are in `run4/receipts/`; OMP transport was substituted with `/root/codex/p77box/omp-cache` at `78f0e0960f471c2c62b943272a48c33366f239fe`. Private manifest checker output is `run4/receipts/manifest-check.txt`, and manifest hashes are `preinstall-inputs.sha256`.
- `run4_space before_install 25`: 05:05:42 UTC, 32260376 KiB available, exit 0, `run4/receipts/run4-disk-preflight.log`. After-restore and before-browser measurements were not reached.
- Installer: `setsid nohup bash run4/receipts/install-command.sh`; start 05:05:42 UTC, end 05:05:49 UTC, exit 1. `install.log` says Astrid could not finish. The installer detail log at `run4/stack/home/.local/state/astrid-runtime/logs/install.log` reports `failed to find branch, tag, or commit` for Runtime `77c38d037f98f744bd8f41c15d95429c124a8003` during `uv pip install`, with `git rev-parse ...^0` exiting 128. Receipt wrapper, exit and timestamps are in `run4/receipts/`. At 05:06:05 UTC orphaned Git processes 5294, 5296, 5298 and 5300 remained in session 5148, associated with the Agent mirror fetch. No retry was started.

Exact tuple (`firstcut-432-reviewed-pins/exact-tuple.txt`):

```text
846ce8cafdf8ca2e58a101a18242c9e50358f89c
b7f0e96a4934ddb4c123eab791a6e18efb8f79ac
f0ffe045411295fcbd9f73262d2506b7cd83e706
f19aed4c515df9bbaf85c4482bc4fed6aa243f9c
77c38d037f98f744bd8f41c15d95429c124a8003
```

Original App manifest SHA-256 `eff2d1deb0da5b2910b21f6b21802b92bc53498c951f3dd20a22c6c2e595ac7e`; private manifest SHA-256 `bb5ac43699b8cce71036af417fb638cc6be10e1f8f9f9a1f721bc2066172182e`; verified schema digest `sha256:2c6a76e17b4441398ab91e3e9d6283a719fd5b08807447db9dbf2ecc5e1339a2`.

Sections 2–6 were not run. There is no working restore, adoption, health time, cold or reopen time, browser request count, or timeline commit POST count for this run. The authenticated read-back is not proved. Proof restore, backup and stopped source were not re-hashed in this run; their unchanged status was not independently verified. No Runtime owner was intentionally started. Created roots are `run4/`, including `run4/stack/` and `run4/receipts/`, and `firstcut-432-reviewed-pins/`, including its App and Agent worktrees and exact tuple. Operator scripts and this result are in `run4-manager/`. Partial installation and receipts are retained.
