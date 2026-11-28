---
description: Steps for the Codex app toolkit rows: creating a thread, the hourly automation, opening and naming a ChatGPT chat in Chrome, and resuming one.
---

# Run Codex from the Codex app

**Environment:** the Codex app and ChatGPT on the web, driven from a Lead or manager session. The steps below are the ones recorded in the `TOOLKIT` comments on the Lead board ([banodoco/astrid-dev#2030](https://github.com/banodoco/astrid-dev/issues/2030)). For Codex Cloud chats, use the [Codex Cloud guide](../codex-cloud/README.md) instead.

The toolkit table in [releases/16/run.md](../../../releases/16/run.md) lists these rows. Each row is followed as recorded; a row not yet recorded is first tried once and then recorded on the Lead board.

## Create a thread

Create a manager session and send it its brief:

1. Read the manager brief (for example `manager-P93.md`, from the command table's file row) and copy its text block.
2. Replace only `{BOARD}` with the plan board URL. Leave the rest of the text unchanged.
3. Call `create_thread` with `title`, `model` (the recorded example is `gpt-6.1-terra`), `target={type:projectless}`, and the filled text as the `prompt`.

Record the session ID the call returns on the Lead board.

## Hourly automation

Schedule the hourly check:

1. Call `automation_update` with `kind=heartbeat`, `mode=create`, `destination=thread`, a `name`, `rrule=FREQ=HOURLY;BYMINUTE=17;BYSECOND=0`, and `status=ACTIVE`.
2. Set the prompt to the Lead loop prompt, pointing to the plan board and `run.md`.

`destination=thread` is required. The recorded example runs at :17 each hour.

## Open and name a ChatGPT chat

Open a new chat in Chrome and name it:

1. Open a new Chrome tab at `https://chatgpt.com/` and select **Chat**.
2. Open **Select ChatGPT model**. Use the power slider's arrow keys to choose **High**.
3. Paste the filled packet brief and send it.
4. Open **Home** and find the new chat under **Recents**.
5. Choose **Chat actions > Rename**, enter the packet chat name, and press Return.

## Resume a ChatGPT chat

1. Open the recorded `chatgpt.com` conversation URL in Chrome.
2. Paste the owner-authorized resume message into **Ask ChatGPT** and select **Send**.
3. Check that the conversation shows the message and **Thinking**.

## Not yet recorded

- The other modes in the chat's mode picker are not recorded yet. Only **High** appears in the comments above.
- The exact text of the hourly automation's prompt is not recorded; the comment names only what the prompt points to.
