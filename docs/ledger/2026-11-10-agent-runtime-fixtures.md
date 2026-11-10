Date: 2026-11-10
Kind: issue
Source: Release 12 Track A A2 comparison
Resolved by: —

The shared Agent setup installs Runtime noneditably, so `runtime_protocol` resolves to site-packages without the adjacent Runtime producer tests that selected Agent custody fixtures import. The first restarted A2 comparison was stopped after 49% of R10 because those IDs could not be measured. A comparison preflight should verify the pinned Runtime import location and required producer fixtures before running; review any shared setup change against its other users. The corrected four-way attempt uses each pinned Runtime checkout editably and verifies both fixture imports.
