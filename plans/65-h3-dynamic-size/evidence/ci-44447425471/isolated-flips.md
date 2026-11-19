# Isolated checks for candidate-only CI failures

Base `b50371baf101d6f706269fab38cdf3a7a5eb2013`; candidate `513204189161c4f72abc73e4fe7d46d7e97ac534`. Each test node was run alone three times per side on CPU, using `astrid-dev/env/agent-pytest.sh -q -rA`, with independently provisioned pinned environments. Base and candidate ran concurrently, one test process per side.

| Test | Base | Candidate | Classification |
|---|---|---|---|
| `tests/core/generation/test_readiness_missing_models.py::test_the_download_plan_and_readiness_agree[True]` | 3 passed | 3 passed | Runner-environment sensitivity; see Plan 39 AT12. |
| `tests/test_installer_autostart.py::test_saved_off_reconciles_all_activation_routes_with_real_backend[local-rollback]` | 3 passed | 3 passed | Runner-environment sensitivity; hosted startup detail was withheld. |
| `tests/test_pinokio_platform_adapter.py::test_secret_never_appears_in_receipt_state_or_cli_output` | 3 failed | 3 failed | Runner-environment sensitivity; all local failures report the listener-owner error. See Plan 39 AT19. |

These hosted failures are not considered Plan 65 regressions under the host ruling; they remain red CI results, not green. The local Pinokio failures precede secret assertions. The relevant tests, installer activation and adapter paths are unchanged between revisions. The checks do not prove the precise cause of any individual hosted flip.

For shard 6, the candidate and base both report 33 more failures than distinct FAILED node IDs in the short summary. Per the host ruling, treat the counts as matched and the short summary as collapsing those entries; no missing IDs are inferred.

## Local logs

Files below are retained in `run/ci-comparison/`. SHA-256 fingerprints identify the raw logs; the result column is the pytest terminal outcome. Raw log contents are not copied here.

| Log | SHA-256 | Result |
|---|---|---|
| `isolated-base-readiness-1.log` | `e555108969be82ccc5e5d163b2bc347a04b14dedd809aa316c187f64165b2e02` | passed |
| `isolated-base-readiness-2.log` | `5b2859b2951bfb18394e0f8c2d57d9c0517abd7250c7925ef5c6af582c19cc21` | passed |
| `isolated-base-readiness-3.log` | `4877015e9f9eae3fe8bc74c832b6f2a200785c3a7248dda2155078c376f55278` | passed |
| `isolated-base-installer-1.log` | `6027c64dad150e5ad41d911ffcae004a507ecb579add5a0ce2324536f6e49538` | passed |
| `isolated-base-installer-2.log` | `b483aaac634122ac70299b3cd55df7ddab7c3e53d175714cebb8b031bae7f15e` | passed |
| `isolated-base-installer-3.log` | `84e6df0bee8e87a0011ddfe75fb6480626718e16a5b247c18f5497c98211326e` | passed |
| `isolated-base-pinokio-1.log` | `291fc85377a1175d0e59b9d439188a5571de21a12535141957ac75deafffb132` | failed: listener-owner error |
| `isolated-base-pinokio-2.log` | `34b17937123382e53b860bb6af8c8bc67f31138d42300b62106c304251bb7cf8` | failed: listener-owner error |
| `isolated-base-pinokio-3.log` | `1a7195e40d3807b8407e9724c72c72680e21377640651586a8eee0acc3af83b4` | failed: listener-owner error |
| `isolated-head-readiness-1.log` | `2e6d16abf463cef6ced40734dd4e5185bf337341fcc8736f2ed6d96fd0776832` | passed |
| `isolated-head-readiness-2.log` | `b889503112515cff987461f050d52c60a032f366dc91b1846080e603e33bfb1e` | passed |
| `isolated-head-readiness-3.log` | `7baab008d516c5efb38221e1034ec7ea8bd3dedc415988c5259d3e63d70a16e6` | passed |
| `isolated-head-installer-1.log` | `7c66f62e28af2c6ca838569534a2d8a96a5dd35b3aaec2ac3c0b9cfa55a4f9b6` | passed |
| `isolated-head-installer-2.log` | `e4791e17377ba3c9dea453c1ebcd36fc238f14d937e3f10db161890c87aa1727` | passed |
| `isolated-head-installer-3.log` | `1272f82da50b0510d73c7d8b515243a471f24b2d588dfa10c1baa112d076dee4` | passed |
| `isolated-head-pinokio-1.log` | `f961f8796c90b89df63abf19d7b4c60567a53b3ea5579a77af435a0d6f4933a9` | failed: listener-owner error |
| `isolated-head-pinokio-2.log` | `74b1245e115d09d60631159f4238b72203c0236cd27ec4038498d03f78b77016` | failed: listener-owner error |
| `isolated-head-pinokio-3.log` | `9df79f71e30bca73a27234bc78a2c130b02736eed378cbee88992d7dbe1f6044` | failed: listener-owner error |
