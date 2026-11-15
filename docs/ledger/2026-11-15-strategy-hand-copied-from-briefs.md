Date: 2026-11-15
Kind: issue
Source: The owner, reading strategy.md on 15 November 2026; Plan 58's planning read
Resolved by: —

`strategy.md` copies each release's state, highlight and plan list from `releases/<N>.md` by hand, and CI compares the copies (`check_docs.py`, `strategy_errors`). The version map and the sequence table are separate, so nobody can read a version, its releases and their plans in one place; version 0.1 is eleven bare plan links, and versions 0.2 to 0.9 are eight identical stubs. The owner called the page "pretty flat in terms of understanding". The checker also reads the table back as its source for the version rules. Plan 48 recorded the hand copy and deferred generating it; nothing has since.
