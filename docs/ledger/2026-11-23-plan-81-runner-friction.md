Date: 2026-11-23
Kind: issue
Source: Plan 81 Part 2b manager run
Resolved by: —

The run collided review-finding card IDs across parts, and a 45-minute worker limit forced repeated handoffs while hosted comparisons were still running. The installed timing also encountered a proxy that refused GitHub archive tarballs although Git fetch worked. Give findings part-qualified IDs, permit a durable monitor handoff for long hosted jobs, and check archive access before timing so the run can stage pinned sources from local Git when needed.
