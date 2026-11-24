# Pin witnesses on the Plan 77 and Plan 81 frozen inputs

The source audit examined the exact current first-cut sources App `846ce8ca`, Agent `b7f0e96a`, Runtime `77c38d03`, the current release controls App `e3dbad64`, Agent `8807f820`, Runtime `23310dc8`, and frozen Plan 81 Part 1 Agent `a2938366` and Runtime `72b129e5`. Plan 81 Part 1 has no App branch. The audit searched 29 distinct Runtime commit families from the consumer lock histories and exact candidate sources. The raw matches identify each exact tree and line. [Exact queries' result](source-pin-literal-audit.json)

## Fields that follow the actual landed pin

| Repository and current line | Treatment |
| --- | --- |
| Agent `runtime.lock.json:71` and `astrid/resources/runtime.lock.json:71` | Official generator uses the actual landed Runtime merge commit. Both copies remain byte-identical. |
| Agent `tests/test_vendor_lock.py:76` | The fixed expected SHA follows the generator's output. Keep the path set, 16-artifact count, format and lock-check assertions byte-identical. |
| Agent `tests/test_windows_path_budget.py:23`, coupled at line 125 | The fixed Runtime archive SHA follows the same generator output. Keep the named path witnesses, size limits and every other test byte. |
| App `runtime.lock.json:63` and `public/install-manifest.json:8` | Official regeneration uses the accepted Runtime and Agent merge commits. The rehearsal verified all consumer artifact bytes. |
| Runtime | No current or older consumer pin from the 29 searched commit families appeared in the exact audited Runtime trees. |

The Lead's written 23 November rulings require the two Agent fixed SHA literals in the same regeneration commit as both generated locks. Copy the value from the generator's `source_commit` and verify it equals the Runtime commit that actually landed in `release/15/main`. That release pin commit changes just the two lock files and one literal in each of the two existing test files. The Agent landing PR names both witness lines. The final independent reviewer confirms the generated identity, byte-identical remaining assertions, and PR disclosure. Rehearsal identities remain scratch evidence. The first-cut rehearsal already observed the stale fixed vendor-lock outcome on both locally repinned inputs. [Rehearsal and results](RESULT.md)

## Historical references retained

- Agent frozen Plan 81 `tests/integrations/us2-command-count-capture-evidence.md:10` names stock `3c28211f` for the completed dated capture. It stays fixed.
- Agent `scripts/check_journey_evidence.py:82`, `scripts/journey_version_jumps.py:49` and `tests/upgrade/releases.json:40` keep Release 9's exact `f4c7a462` baseline.
- Agent `tests/test_diagnostics_callers.py:107` and `tests/test_installer_app_update.py:553` use `744cf248` in comments that explain the existing diagnostic message assertions. The assertions and comments stay in place.
- App `scripts/astrid-release/hosted-proof.md:17` and `scripts/astrid-release/hosted-proof.py:332` keep Release 13's exact `6855dfa8` control. The proof checks Release 13 before checking the SHA.
- App `src/integrations/runtime/contract-metadata.ts:19` describes the Timeline ABI provenance at `95920f84`; the code checks the contract version and component digest. `src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts:427` records the shape at `4c18af59` in the test name.
- Runtime's independent source read also found historical FIX-12 proof and schema provenance in `docs/evidence/r14-fix-12/README.md:9,31,65,89–100`, `docs/evidence/r14-fix-12/focused-proof.json:4,6`, `docs/evidence/r14-fix-12/release-baseline.json:2`, `docs/findings/2026-10-16-transcript-merge-findings.md:11,30` and `contract/schemas/timeline-config.schema.provenance.json:5,16` with its existing assertion in `tests/test_shot_composition_contract.py:218`. These keep their original identities.

Repeat the exact audit on the actual frozen sources after Plans 81 and 40 land. New active matches go to the Lead before any change.
