Date: 2026-11-11
Kind: issue
Source: Release 12 Track B GPU preparation
Resolved by: —

The GPU validation skill requires an account balance before spending and routes balance actions through runpod-lifecycle or `astrid machines`, but the pinned lifecycle `f2948817eeb94af8dee76be21f6d673724f1606e` exposes no supported balance or billing operation. Its cost summary projects current pod rates, not historical billed spend. Release 12 therefore needs the account owner to supply the provider Billing page balance and transactions, or a reviewed lifecycle balance capability, before reconciliation. A future workflow should name a supported balance source and preserve the no-raw-API rule.
