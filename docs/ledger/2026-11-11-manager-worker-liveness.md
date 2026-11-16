Date: 2026-11-11
Kind: issue
Source: Release 12 manager resumption
Resolved by: —

At the fourth release check-in, both managers resumed but previously active workers and test processes were absent; a prior scheduled chat wake did not establish that worker processes or their completion messages would survive. Track B's P20 candidate and exact-base logs had complete summaries, while its intended exact-candidate P40 log was absent and its R10 comparison had no final receipt. The cause of termination is not established. On every resume, inventory actual workers, process IDs, branch heads and test exit receipts before reporting activity; treat missing or incomplete logs as interrupted, preserve them, and restart only the unfinished work. A future orchestration mechanism should explicitly supervise worker survival and wake the manager promptly on termination, rather than relying on a chat wake alone.
