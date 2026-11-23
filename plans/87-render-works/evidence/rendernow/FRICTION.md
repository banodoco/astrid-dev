# Render friction

Exact argv: see probe-command.json and full-command.json; timestamped output in progress.log.

Preflight: storage helper fixed/estimate-render-storage.py:39 hard-codes expected_version37. Used an otherwise identical copy in rendernow/ with version38 and report output redirected. No product code changed.

Snapshot: product online consistent copy exists at runtime_protocol/backup.py:678; it duplicates CAS and holds realm mutex. Deferred until render completes to preserve disk reserve. No stack downtime.
