# Provisional App R13→R14 native journey inventory — 21 November 2026

**Diagnostic only, NOT publication qualification.** Published App `de7dd1e668aa6dcf3cbce013c701fa7c76615f99` vs pre-freeze App `e6ca6e8032fcb2e6ab42cb713bb5047ae023f2e4`. No workflows were dispatched. [R13 Lanes](https://github.com/banodoco/astrid-app/actions/runs/43860030963) / [R14 Lanes](https://github.com/banodoco/astrid-app/actions/runs/44639404982) and [R13 E2E](https://github.com/banodoco/astrid-app/actions/runs/43860030918) / [R14 E2E](https://github.com/banodoco/astrid-app/actions/runs/44639404948).

**Publication blockers beyond table:** (1) Native individual Vitest assertions **not in default console reports** (R13 Tests [43860030897](https://github.com/banodoco/astrid-app/actions/runs/43860030897) 1433 passing file suites, pre-freeze Tests [44639404891](https://github.com/banodoco/astrid-app/actions/runs/44639404891) 1441 passing file suites; this is not per-ID proof); (2) R13 Direct Journey [44078954757](https://github.com/banodoco/astrid-app/actions/runs/44078954757) passed, but the provisional App commit has NO matching Direct Journey run; (3) MIXED-VERSION FIX-17 rows are not landed or qualified; (4) candidate not frozen. No skipped/missing IDs are waived.

| Workflow/job | R13 native IDs | Pre-freeze R14 native IDs | PASS→FAIL | PASS→missing/skip | New failing | FAIL→PASS |
|---|---|---|---:|---:|---:|---:|
| Lanes / quick-journey | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| Lanes / checkout-lanes | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| E2E / extension-accessibility | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| E2E / playwright-default | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| E2E / playwright-timeline | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| E2E / extension-cross-browser | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| E2E / extension-visual | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |
| E2E / playwright-timeline-chrome-export | 0 (0 pass, 0 fail, 0 skip) | 0 (0 pass, 0 fail, 0 skip) | 0 | 0 | 0 | 0 |

Provisional per-job totals: **0 PASS→FAIL, 0 PASS→missing/skip, 0 newly failing, 0 FAIL→PASS**. Counts cannot replace complete native ID inventories; empty parsed IDs are a coverage blocker, never a pass.

## Lanes / quick-journey

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030963/job/133274123070) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404982/job/135966231963)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## Lanes / checkout-lanes

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030963/job/133274123559) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404982/job/135966231725)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## E2E / extension-accessibility

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030918/job/133274124462) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404948/job/135966230937)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## E2E / playwright-default

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030918/job/133274124145) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404948/job/135966231258)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## E2E / playwright-timeline

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030918/job/133274124303) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404948/job/135966231419)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## E2E / extension-cross-browser

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030918/job/133274124428) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404948/job/135966231496)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## E2E / extension-visual

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030918/job/133274124276) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404948/job/135966231501)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

## E2E / playwright-timeline-chrome-export

[R13 job](https://github.com/banodoco/astrid-app/actions/runs/43860030918/job/133274123824) · [Pre-freeze R14 job](https://github.com/banodoco/astrid-app/actions/runs/44639404948/job/135966231616)

**UNKNOWN COVERAGE:** one side has zero parsed native IDs; do not assume unchanged tests.
**PASS→FAIL unresolved: 0**
None parsed

**R13 PASS→missing/skip unresolved; potential rename requires provenance: 0**
None parsed

**New failing IDs: 0**
None parsed

**Provisional recoveries: 0**
None parsed

