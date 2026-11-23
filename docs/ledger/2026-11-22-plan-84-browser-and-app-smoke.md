Date: 2026-11-22
Kind: papercut
Source: Plan 84 hosted manager run, local trial and baseline
Resolved by: —

The whole-project manager startup asks every product worker to run `env/smoke.sh`, but that script accepts Agent, Runtime and VibeComfy only. The App worker instead ran its named sky-session Vitest test and recorded the command, six passing cases and exact starting commit. The run brief also said the installed browser needed no launch path, while the App dependency resolved a Playwright version whose default cache was absent. Explicitly using the installed Chrome binary with a recorded version and software drawing flags restored captures without a browser installation; the host subsequently supplied the managed browser path too. Give App a supported named-test smoke entry and have browser briefs name the actual installed executable and version. A startup capability check should validate those two concrete assumptions before workers spend time diagnosing them.
