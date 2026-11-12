Date: 2026-11-12
Source: Release 13 live and offline runs, 11–12 Nov (smell 8; decision log task 18)
About: F-002; Plan 40
Outcome: open

Five `test_warm_session` paid-expiry deletion tests have failed since Agent `b306b2be`. They guard money safety (a machine past its paid limit is deleted). Cause unknown: nobody has checked whether the tests are stale or the product stopped deleting. Do not leave this open: investigate as a small task, and if it cannot be fixed in that task, quarantine only under Plan 39's quarantine rule.
