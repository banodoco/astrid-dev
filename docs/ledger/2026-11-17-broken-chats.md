Date: 2026-11-17
Kind: fix
Source: Release 14 dispatch, 17 November 2026. Three original ChatGPT chats showed "Could not load this ChatGPT conversation". The Lead asked for replacements, and one of those chats then resumed. The owner asked for a rubric.
Resolved by: —

The dispatch workstream said to resume a quiet session and replace one quiet for six hours. It did not cover a chat that fails to load, and it gave no guard against a replacement and a revived original both writing to the same branch. Health is now read from the branch, not the chat:
- **Quiet for three hours:** resume it.
- **Broken:** it will not load after one reload, gives no reply 30 minutes after a resume, or has been quiet for six hours.
- **Replacing a broken session:** only once its branch has not moved for 30 minutes, starting from the branch head, which the replacement names in its first message.

The head guard makes a revived original stop. There are never two writers on one branch.

Follows: 2026-11-17-acted-on
