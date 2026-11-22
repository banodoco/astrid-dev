# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: public-astrid-vision-entry.spec.ts >> header continuity at 390px >> opening every popup keeps the header and background stationary at 390px
- Location: tests/e2e/public-astrid-vision-entry.spec.ts:26:5

# Error details

```
Error: browserType.launch: Executable doesn't exist at /tmp/codex-xdg-cache/ms-playwright/webkit-2287/pw_run.sh
╔════════════════════════════════════════════════════════════╗
║ Looks like Playwright was just installed or updated.       ║
║ Please run the following command to download new browsers: ║
║                                                            ║
║     npx playwright install                                 ║
║                                                            ║
║ <3 Playwright Team                                         ║
╚════════════════════════════════════════════════════════════╝
```