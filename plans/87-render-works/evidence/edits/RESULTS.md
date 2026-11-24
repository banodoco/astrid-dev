# Almost Ready — five edit receipts

Timeline `77f906f3242c48179ab86ca7c3e62eb4` (trial v2), project `801a01b3a87941a1ab25958c488afdbf`. All five edits are published, one revision each. Canonical commit order: A, B, C, E, D. D automatically re-read after an atomic head conflict and succeeded on its second evaluation.

| Edit | Result | Previous revision | Accepted revision | Changed clip IDs |
|---|---|---|---|---|
| A | Verified done | `authoring-parent-revision-606c2a9209b066899a64a790dd661c00dc00e29edd8f4320296d9902ceae2f19` | `authoring-parent-revision-dbbb9ebef60a9cb24aa047bcaaf6dcbd05162b0347a8262b74be7b4fa299b6f9` | 1 |
| B | Verified done | `authoring-parent-revision-dbbb9ebef60a9cb24aa047bcaaf6dcbd05162b0347a8262b74be7b4fa299b6f9` | `authoring-parent-revision-796f0de2cc86df2702adb066b7e84104ae3e7e80c13486ce71d49fd556ac46e6` | 1 |
| C | Verified done | `authoring-parent-revision-796f0de2cc86df2702adb066b7e84104ae3e7e80c13486ce71d49fd556ac46e6` | `authoring-parent-revision-c723b4406d110fb1cd6a721a2e42c0c1201c0e2119e2c5b33c3aaa31090939fc` | 1 |
| D | Verified done | `authoring-parent-revision-d97a25287963eb336a687c8889338fe017b877d5969b91bd5ce32449f1596059` | `authoring-parent-revision-fe54bd8ce50106cdd4803f23c83ea210afe8c85f03d743a617537f6d9fe2cac1` | 1 |
| E | Verified done | `authoring-parent-revision-c723b4406d110fb1cd6a721a2e42c0c1201c0e2119e2c5b33c3aaa31090939fc` | `authoring-parent-revision-d97a25287963eb336a687c8889338fe017b877d5969b91bd5ce32449f1596059` | 337 |

Final observed head: `authoring-parent-revision-fe54bd8ce50106cdd4803f23c83ea210afe8c85f03d743a617537f6d9fe2cac1`; publication `txn-669ef0d42177421e9180aa7d6da6d336`.

Fresh Runtime reads and independent row comparisons verify:

- A: `clip-1` removed; total clip count 621 → 620. No other clip changed.
- B: all five requested join names, in order; join `at` values retained.
- C: first three camera rows retained; seven requested rows replace the remainder. Existing camera/composer/message formulas remain. Source `discord-core.ts:142–160` computes one-frame linear segments without intermediate integer frames, then the requested 178–217 linear coast.
- D: only `c23-desloppify-arrow` changed. Authored `at=13.600333`, `hold=1.533334`; absolute start 55.933333, end 57.466667 seconds. Its legacy word anchor could not be recaptured through the internal-clip API; supported cut-relative `on=+3.133333s` preserves this start relative to c23 at 52.8 seconds. This follows the cut, rather than future word timing. `nudge` was avoided because it globally retimes unrelated rows.
- E: 341 → 99 plate stills, 242 removals and 95 retimed survivors (337 changed clip IDs). Exactly the same re-derived ID/asset subsequence as the previous plan. Coverage is frames [860,1270), with no frame gaps/overlaps; holds are 95×4f, 2×5f, 1×7f, 1×13f. All stills meet the four-frame minimum. `c17-39-am-type` and `c17-40-am-flap` are byte-for-byte unchanged. Kept authored rows retain their pre-existing sub-millisecond decimal rounding; the invariant is frame coverage.
- End: 196.566667 seconds, rounded 3:16.57. The editor truncates its label to 3:16.56; see defect 11.

The old 1,781,813-byte request was a dry run. It could not publish; all 341 time-lapse clips were present on our initial independent head read. Retrying in its original mode revealed Broken pipe. The 1 MiB endpoint cap is verified source; the exact early-response/socket sequence is inferred because the owner suppresses request logging. Runtime itself was healthy. Sandbox `r6-write-sandbox` / `r6-write-test` committed a trivial edit and a fresh read confirmed it (`sandbox-test.log`).

Independent SDK outboxes restored supported commits while retaining the original poisoned default outbox. The default outbox remains blocked because the product exposes no safe abandon-preview route. No Runtime restart, managed-install patch, database mutation, render, or GitHub post was performed.

Full receipts, independent audit, and E plan:

- `A-receipt.json` … `E-receipt.json`, alongside before/after bundle snapshots.
- `audit.json` and `audit_edits.py`: compare each exact accepted publication against its actual previous publication; D uses E’s accepted snapshot as its before after the stale-head retry.
- `E-rederived-plan.json` / `E.log`: full frame/asset proof.
- `DEFECTS.md`: reproductions, verbatim errors, installed file:line references, deliberate/defect classification, severity, and minimum fixes.

Editor stills: see `verify/exact-frame-evidence.json` and `verify/frame-*.png` (all eight frames captured and visually inspected). The editor was used only through playback, seeking, and full screen; no Save/Render actions.
