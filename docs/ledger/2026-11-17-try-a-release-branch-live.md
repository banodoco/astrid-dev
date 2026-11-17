Date: 2026-11-17
Kind: fix
Source: the owner, 17 November 2026
Resolved by: —

The Release skill now has a section, "Try a release or plan branch live", for the `astrid-release` tool that runs a release or plan branch as an isolated local stack with a copy of the developer's realm, and step 8 links to it. It states what the tool does and its limits (no `update` to new commits yet, one start retry, macOS only), and that a live try is not landing proof or a tester build.

Follows: 2026-11-16-release-branches-per-repository
