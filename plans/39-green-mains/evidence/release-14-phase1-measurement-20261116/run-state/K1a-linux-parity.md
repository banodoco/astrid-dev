# K1a — equivalent Linux gates with existing red behavior

Manager /root; follow-up messages are part of this brief. Route N, local additive commits only, no remote changes, never AskUserQuestion. Repository /workspace/scratch/cd53b069f320/p39-repair/astrid-agent, exact starting head 372e39cd309e519857c1dbb2c86d71f7ef724232, tree aabdeab6b08f14bff2205186b9ae1aa2f1f16380. Branch p39/k1a-linux-gates. Sole product writer for this card.

Independent authority: read p39-g2-evidence/agent/k1a-linux-gates/review.md, especially six concrete ownership boundaries. This NEW card replaces the former passing-pre-proof condition only for these exact OS-gate migrations. It does not authorize behavior repairs. Accepted prerequisite proof is exact selection and outcome parity, even when unrelated behavior is already red. Formal RS1 remains 0/1.

The task-created venv directory symlink has been repaired without dependency/version changes; evidence p39-g2-evidence/agent/environment-layout-correction/. Do not use historical symlink-environment logs as before proof. No environment/package/pin changes in this card.

Scope: only the existing module-level Linux skip gate in each of:
- tests/core/generation/test_engine_readiness.py
- tests/test_boundary_handoff.py
- tests/test_boundary_registration.py
- tests/test_installer_r0_entry.py
- tests/test_installer_update_legacy_record.py
- tests/test_update_from_field_states.py

Replace it with existing pytest.mark.linux_native at identical scope. Preserve every test body, assertion, fixture, parameter, all other marks and all other gates (including R0 manual artifact skip). No integration marker, default-off lane, scanner allowlist, expectation change, new quarantine or Plan38/55 behavior edit. Remove only imports exclusively used by the replaced OS gate if AST accounting makes it explicit.

Evidence root: /workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-linux-parity/. For each row sequentially:
1. Run the exact command below BEFORE editing that row, with PYTEST_ADDOPTS=-rA and --junitxml=<absolute evidence root>/<row>-before.xml. Save raw stdout/stderr and actual exit code. Command is:
   bash scripts/worker-env/agent-pytest.sh -q --junitxml=<path> <the exact file above>
2. Replace ONLY that module gate.
3. Run the identical command with only XML destination changed to <row>-after.xml, same PYTEST_ADDOPTS. Capture logs and exit.
4. Compare exact node-ID multisets, phase status, skip/deselection and full exception/assertion signatures. Ignore ONLY volatile temporary prefixes, addresses, process identifiers and elapsed time with explicit normalization documented; never ignore semantic text or changed failure categories. Record any before-to-after passing improvement separately, but do not accept unexplained differences as parity. If parity differs or ownership ambiguous, revert only your row change and HOLD that row for root review. Do not retry.
5. Independently AST compare before/after excluding only gate node and its provably dead import. Keep all failed tests visible.

Run only those six focused file proofs, one before and one after per attempted migration, sequentially. No full suite/policy proof or collection-only extra runs; JUnit is the case inventory. If a hung process reaches existing timeout, record it; do not change timeout to pass. Known engine setup errors do not prove unexecuted bodies pass.

Commit only accepted equivalent gates, additive commits. Final report: each row exact before/after counts, parity verdict, every retained failure cause, selected eligibility on supported Linux/macOS/Windows, commit/tree. Overall K1a remains incomplete including manual-artifact and Plan38 holds.
