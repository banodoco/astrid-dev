# App native inventory reconciliation

The [official hosted verdict](https://github.com/banodoco/astrid-app/actions/runs/44611474919/artifacts/14575905046) ingested six original native suites using the unchanged destination collector. The proposed evidence in [app-native-census.json.gz](app-native-census.json.gz) has SHA-256 `d3c7f8c9f4e4d6deb5d7b0d9c370e1578ac86a7329ba252c405792666cfd1f7a`. The sealed 21,250-row inventory at `0700e981` had SHA-256 `5d7e92666e59879c65760718e6204515a1e71217eeae7a4d638870c18aadccd0` throughout the comparison.

| Evidence in the gzip JSON | Rows | Disposition |
| --- | ---: | --- |
| Proposed passing additions | 824 | 263 App, 465 full Node, 21 installer, 9 boundary and 66 Darwin. Each identity was absent from the sealed set. Recheck against the updated sync and review before admission. |
| Linux skips | 26 | Each has a declared base skip, a registered reason and a matching Darwin pass. Policy disposition is open. |
| Missing seeded App IDs | 4 | Possible correspondences are recorded. The old identities remain protected. |
| Changed App source bindings | 15 | Preserve both bindings for review. The official evaluator stops at the first mismatch. |

The evidence contains identities, original observations and provenance. Completing this comparison requires the [P39-28 packet](../../packets/R14-P39-28.md) and a fresh trusted verdict. [Activation issue](https://github.com/banodoco/astrid-dev/issues/984)
