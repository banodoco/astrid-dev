Date: 2026-11-23
Kind: fix
Source: Release 15 Lead session, 23 November 2026 (setting up ChatGPT dispatch for Plans 87 and 89)
Resolved by: —

The run contract maps a packet's Route to its ChatGPT session's mode (N High, X Extra High, S Pro), but the dispatch workstreams mentioned it only in passing, and Release 14 ran every packet writer in Extra High. The owner restated the mapping. It is now a table in multi-manager dispatch, with "never run every packet in one mode". The Lead's packet step says to route honestly because the Route sets the mode, and a packet session checks its own mode in its first STATUS. Follows: 2026-11-23-hourly-lead
