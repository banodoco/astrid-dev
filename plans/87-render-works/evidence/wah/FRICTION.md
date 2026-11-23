2026-11-22: Initial read script named inspect.py shadowed Python standard-library inspect and failed before connecting. Renamed it read_wah.py; no timeline change.

Attempt 1: TimelineEditError: commit(command_list) requires a clean local session
SDK Timeline.open repeatedly took approximately a minute before returning on this running stack; no restart attempted. The first command-list attempt was rejected locally because the candidate remained staged; restoring the original field made the session clean before the successful atomic commit.
