# The 432-clip read-back runbook, run once (22 November 2026)

Raw records of the one run of [the read-back runbook](../../2026-11-22-release-15/432-clip-readback-runbook.md) on the build machine hosted by the [Release 15 Lead session](https://claude.ai/code/session_011EzfW1gtAhRQwk8pgJMzhG). Nothing here is interpreted; the reading belongs to [Plan 77](../../../plan.md)'s record. [RESULT.md](RESULT.md) is the run's own account, step by step.

**Tuple:** App `be9cc2407306eff06252c0d54be1c7f5afcacf3f`, Agent `18adee8034973837a97fcd7392cd67f4566fa992`, Runtime `d7be2f0458a55c1f26e1138a125ffefe382f56f4`.

- **Section 1, stock install into a fresh stack:** exit 0. Its first launch was interrupted before it created anything and was started again unchanged in its own session; the interrupted launcher's files are kept with `.interrupted` names. The tooling checkout was made as a worktree of the machine's partial clone, because a local clone of it had no file contents (`tools-checkout.txt`, `tools-worktree.txt`, `tools-verification.txt`).
- **Section 2, authenticated restore into a fresh working root:** exit 0; the proof copy and the working database both have SHA-256 `5d1c249a7564cbdd3acd2e82dd2506998e1341a5b4786f070e9a0080b0ccbbf8`.
- **Section 3, the one adoption (admission 1800 s):** 19:33:18Z to 19:38:39Z, exit 1, "adopted realm failed final integrity checks": two `timeline_commit_history` rows reported `interrupted`, every other check ok (`round5-432-readback-receipts/adopt.json`).
- **The one further step ordered by Plan 77's host:** the offline doctor on the working restore with `--admission-timeout 1800`, 19:41:35Z to 19:46:21Z, exit 0, deep verification ok and no revision errors (`working-doctor.json`, `working-doctor-cpu.txt`). Both databases were re-hashed afterwards and are unchanged.
- **Sections 4 to 6 did not run.** No resume, no `up`, no retry, no cleanup.

**Not in Git:** `round5-432-readback-receipts/restore.json` (1,276 bytes, SHA-256 `4e07bf731ff1b84edb8e87dec699292c21eab63c811d20088bf840dd41a4e800`) carries the backup's key identifier, so [a copy with that field withheld](round5-432-readback-receipts/restore-summary.json) is committed in its place. The backup, the restores, the support directory and the key stay on the build machine; the key was never opened.
