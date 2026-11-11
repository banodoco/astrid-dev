Date: 2026-11-11
Kind: fix
Source: Owner request
Resolved by: —

Nothing said what to do with open pull requests, especially outside contributors', when a release is specified, and there was no written process for reviewing one. The Release skill now takes stock of open pull requests across every repository the release touches, sorts each into this release, a later one or not as it stands, works out how the chosen ones fit together, and records them in the release brief. A new Merge skill reviews one pull request: cheap helpers check for suspicious content, best practice, right place, fit with the philosophy and proof; a lead critic judges their findings against the diff; then it is merged, sent back with every finding at once, or brought to the owner. It never runs a contributor's code with credentials.
