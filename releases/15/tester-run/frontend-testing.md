# Test the actual Release 15 frontend (Windows and Linux)

This is the browser section of the [tester brief](tester-brief.md) and [technical matrix](test-matrix.md). First [prepare and verify the installed snapshot](prepare-build.md). The installer alone does not install the frontend: astrid.haus may serve a different App. Run the exact compatible App commit from the receipt. This is a real local editor connected to the installed Runtime, not a fake editor preview.

## Start the pinned editor

Read the App's README at the **exact App SHA** (the [Release 15 candidate README](https://github.com/banodoco/astrid-app/blob/cc1d48f016fde55ad6b0609c619d8a4bcec56823/README.md#run-astrid-fully-on-your-computer) is the reference as of 25 November). The supported local launcher works from Terminal or PowerShell. It attaches to the installed compatible Runtime or starts it using its recorded environment. It does **not** isolate your existing workspace. Back up existing work first, create a disposable project, close conflicting tabs with consent and do not edit/delete real projects. Do not connect a candidate App to a different or unverified installed tuple. An installed-side-only snapshot created by repinning to a newer Agent must have a separately verified compatible App before this section counts.

Prerequisites: Git, Node.js 20.19 or newer **in the Node 20 release line**, npm registry/network access, available port 5180, enough disk for a separate checkout and npm dependencies, and an accessible supported browser. Check these and obtain consent before provisioning anything. Do not overwrite an existing source checkout. In a new session-owned directory, use the full App SHA recorded in the receipt (replace FULL_APP_SHA before executing):

```sh
git clone --no-checkout https://github.com/banodoco/astrid-app.git astrid-test-app
cd astrid-test-app
git checkout --detach FULL_APP_SHA
git rev-parse HEAD
npx -y npm@11 ci
npm run dev:local
```

Run commands in order, checking exit status and exact HEAD before continuing. Keep the terminal open and capture launcher output. Open [the local editor](http://127.0.0.1:5180/tools/video-editor?connect=1) or its verified printed URL. Use a separate browser profile if practical. Confirm Connected and that the actual active Agent/Runtime/VibeComfy match the receipt. Record the exact checkout, clean tracked state, local URL and connected Runtime identity/realm; use launcher/doctor evidence, not just a page that loads. Do not expose the local proxy publicly.

If the launcher reports incompatibility, a port conflict, repair needed, missing tools or a failed npm install, record the exact reason. Never use the normal public installer, npm run update, a moving default branch, or a fake Runtime to make the test pass. Only stop a process you own or have permission to stop. The `astrid-release` isolated stack tool is macOS/APFS-specific and not required here. Linux/Windows native startup on this exact candidate remains real-machine evidence to collect, not a guaranteed pass.

## UI cases (real browser)

Ask the tester to perform actions with you, or operate the real browser if you have that capability and their permission. If you cannot control the browser, guide them and record observations they confirm; do not claim automated proof. Use small non-sensitive local clips, images and audio they approve, or outputs from the CLI cells. Keep all edits in a new disposable project/timeline. Do not use paid providers without a separately agreed budget.

| Cell | What to try | What counts as success |
| --- | --- | --- |
| UI-0 Connect | Open the pinned local editor and create a new test project/timeline. | Connected to the verified real Runtime; project opens without blank/error state. |
| UI-1 Import and drag | Import two or three small media items; drag onto the timeline, move one, trim or reorder, add a second track if supported. | Visible clips, expected ordering and lengths, playable preview; no missing items or unexpected duplication. |
| UI-2 Save and reopen | Make a clear edit (e.g. move a clip or rename a track), wait for the UI's save confirmation, record elapsed time. Reload, then leave and reopen the same timeline. | Clip count, order, positions, trims and names survive; no persistent saving, error or unconfirmed-save state. Repeat with a second edit. Do not reload an unconfirmed save as normal success. |
| UI-3 Agent setup | Open the editor's agent/chat surface. Check detected choices and readiness (Astrid's agent, Codex, Claude Code, Hermes where offered). Choose one available agent or follow the actual setup/sign-in flow with consent. | Correct readiness/status, clear setup steps and a usable selected agent; no secrets in logs or screenshots. |
| UI-4 Agent conversation | Send a harmless project-aware request, e.g. “Describe the clips and tracks in this test timeline.” If permitted, ask it to make one small reversible edit. | Actual reply reflects the selected project; a requested edit appears in the UI, saves and survives reopen. A reply alone is not edit/persistence proof. |
| UI-5 Reconnect | After saves are confirmed, reload and reopen the chat/project; optionally stop and restart only the session-owned editor. | Connection, saved timeline and expected chat/session state recover without lost work. |
| UI-6 Creative exploration | Make something the tester wants, play it, optionally render a short output if available. | Report the experience and any rendering issues; inspect actual output, not just a success label. |

Agent providers may need installed executables, valid login, API credit or internet. Use existing authorized credentials or have the person sign in locally; never ask them to share a secret in chat or evidence. Test one available real provider; do not require buying credit or signing up for all providers. Note untested providers separately. Missing credentials or authorization is SKIPPED/BLOCKED, not a product failure by itself.

For each cell record pass/fail/skipped/blocked, exact action, observed result, timings, project/timeline identity (redacted), evidence and the person's feedback. Note a feature absent or a broken setup flow rather than inventing controls. Keep the pinned App source unmodified; any fix is separate from baseline. The Release 15 qualifier's [verdict](https://github.com/banodoco/astrid-dev/issues/1836#issuecomment-7172609349) records slow heavy saves and other known limits; report actual behavior rather than treating those as exemptions.

## Finish

Collect redacted screenshots/logs, active tuple and UI cell results in the same session issue. Stop the local editor with Ctrl+C in its own terminal; the existing Runtime may keep running. Do not stop the tester's own services or delete their projects. Offer to remove only the disposable test project and scratch checkout after the tester approves. If the tester wants to retain their creation, preserve it. Follow matrix cleanup and record the final installed version. Label any served App observations separately; if this section was blocked, mark pinned App NOT TESTED and retain the useful installed-side results.
