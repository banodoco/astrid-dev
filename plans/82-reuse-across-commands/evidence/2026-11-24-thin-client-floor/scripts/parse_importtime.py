"""Summarise `python -X importtime` stderr: total, by top-level package (self time), top cumulative top-level imports."""
import json, re, statistics, sys
def parse(path):
    rows = []
    for line in open(path, errors="replace"):
        m = re.match(r"import time:\s+(\d+) \|\s+(\d+) \| (\s*)(\S+)", line)
        if m: rows.append((int(m[1]), int(m[2]), len(m[3]) // 2, m[4]))
    total = sum(c for s, c, lvl, n in rows if lvl == 0)
    bypkg = {}
    for s, c, lvl, n in rows:
        top = n.split(".")[0]
        key = top if top in ("astrid", "vibecomfy", "astrid_runtime_client", "runtime_protocol", "yaml", "jsonschema", "numpy", "PIL", "pydantic") else "other (stdlib and third-party)"
        bypkg[key] = bypkg.get(key, 0) + s
    top = sorted([(c, n) for s, c, lvl, n in rows if lvl == 0], reverse=True)[:15]
    return {"modules": len(rows), "total_s": total / 1e6, "self_by_package_s": {k: round(v / 1e6, 4) for k, v in sorted(bypkg.items(), key=lambda kv: -kv[1])},
            "top_level_cumulative_s": [(n, round(c / 1e6, 4)) for c, n in top]}
res = [parse(p) for p in sys.argv[1:]]
print(json.dumps({"runs": res, "median_total_s": round(statistics.median(r["total_s"] for r in res), 4),
                  "median_modules": statistics.median(r["modules"] for r in res)}, indent=1))
