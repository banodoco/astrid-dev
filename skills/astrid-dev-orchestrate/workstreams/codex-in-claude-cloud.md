# Workstream: Codex hosted inside Claude Cloud

Choose this when a **Claude Cloud session runs Codex locally**, rather than coordinating independent Codex Cloud chats. Follow the existing [Codex-in-Claude Cloud guide](../codex-in-claude-cloud/README.md) for installation, runners, keep-alive and recovery; leave its scripts and relative paths there.

1. **Default:** the Claude session is the accountable plan manager and sends bounded task cards to Codex workers; it reviews proof and integrates the work.
2. **Optional Codex manager:** only for a justified, self-directed run; the Claude host remains accountable for that run and must supervise process liveness as the guide requires.
3. Use the same canonical `tasks.md`, run records, permissions and proof rules as [Manage](../../astrid-dev-manage/SKILL.md). Don't create parallel task queues or treat the hosted Codex process as an independent plan owner.

For cross-plan work run by a Release Lead, the [multi-manager dispatch](multi-manager-dispatch.md) workstream is a separate coordination layer; this guide describes *how one manager session runs Codex*, not a second release manager.
