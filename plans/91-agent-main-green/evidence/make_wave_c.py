#!/usr/bin/env python3
"""List the Wave C cards: every failing ID that no Wave A or B card owns, grouped by test file.

A card owns an ID when the ID's cluster is in the card's "ci" or "lanes" list, or when the ID's test
file matches one of the card's "files" globs (a file already in a card's scope stays with that card).
IDs are counted once per (job, id).

Usage: make_wave_c.py RELEASE_DIR   (reads assignment.json, ci-failing-ids.tsv and lanes-failing-ids.tsv
there; writes wave-c-cards.md and prune-candidates.md there). Standard library only. Re-run after a re-measure with
cluster_failures.py.
"""
import collections
import fnmatch
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
assignment = json.loads((root / "assignment.json").read_text())
by_cluster = {"ci": {}, "lanes": {}}
globs = []
for card, owned in assignment.items():
    if card == "note":
        continue
    for lane in ("ci", "lanes"):
        for number in owned.get(lane, []):
            by_cluster[lane][f"C{number}"] = card
    globs += [(pattern, card) for pattern in owned.get("files", [])]

counts = collections.Counter()
by_file = collections.defaultdict(set)
seen = set()
for lane in ("ci", "lanes"):
    for line in (root / f"{lane}-failing-ids.tsv").read_text().splitlines()[1:]:
        cluster, outcome, job, test_id = line.split("\t")
        if (job, test_id) in seen:
            continue
        seen.add((job, test_id))
        path = test_id.split("::")[0]
        card = by_cluster[lane].get(cluster) or next((c for p, c in globs if fnmatch.fnmatch(path, p)), None)
        counts[card or "Wave C"] += 1
        if card is None:
            by_file[path].add(f"{lane}:{cluster}")
            by_file[path, "n"] = by_file.get((path, "n"), set()) | {(job, test_id)}

files = [p for p in by_file if isinstance(p, str)]
area = collections.defaultdict(list)
for path in files:
    parts = path.split("/")
    area["/".join(parts[:2]) if len(parts) > 2 else path].append(path)
lines = ["# Wave C cards", "",
         f"{counts['Wave C']} failing IDs that no Wave A or B card owns, in {len(files)} test files. "
         "One card per row: the IDs in that file, fixed by cause under the [triage rules](../../tasks.md#triage-rules). "
         "A file with more than one cause splits into one card per cause. The manager gives a worker several rows "
         "from one area at a time, up to about ten IDs.", "",
         "| Card | IDs | Test file | Clusters |", "| --- | ---: | --- | --- |"]
number = 0
for key in sorted(area, key=lambda k: -sum(len(by_file[p, "n"]) for p in area[k])):
    for path in sorted(area[key], key=lambda p: -len(by_file[p, "n"])):
        number += 1
        clusters = ", ".join(sorted(by_file[path], key=lambda r: (r.split(":")[0], int(r.split(":C")[1]))))
        lines.append(f"| AG-C{number} | {len(by_file[path, 'n'])} | `{path}` | {clusters} |")
lines += ["", "## IDs per owner", "", "| Owner | IDs |", "| --- | ---: |"]
order = lambda k: (k == "Wave C", k[:4], int(k[4:]) if k[4:].isdigit() else 0)
lines += [f"| {k} | {v} |" for k, v in sorted(counts.items(), key=lambda kv: order(kv[0]))]
lines += ["", f"Total: {sum(counts.values())} distinct (job, id) pairs."]
(root / "wave-c-cards.md").write_text("\n".join(lines) + "\n")

# Prune candidates: IDs whose cluster message points at removed, retired, moved or legacy code, plus the
# clusters assigned to AG-P1. AG-P1 sorts each into retire, redundant or keep before any card fixes it.
import re
PRUNE = re.compile(r"ImportError|AttributeError|ModuleNotFound|has no attribute|cannot import|retired|\\b410\\b|"
                   r"invalid choice|unknown executor|not discovered|legacy|historical|bootstrap entry|moved to|"
                   r"copy-only|\\bR[N0-9]+ requires|git archive|archive object|authentic|migrat|v[12] manifest|"
                   r"schema_version.?[12]\\b|deprecat|old format|upgrade boundary", re.I)
PRUNE_OWNERS = {"AG-P1", "AG-P2", "AG-A5"}  # owned outright, or legacy upgrade paths the prune pass sorts first
message = {}
for lane, name in (("ci", "ci-clusters.md"), ("lanes", "lanes-clusters.md")):
    for row in (root / name).read_text().splitlines():
        if row.startswith("| C"):
            cells = [c.strip() for c in row.strip("|").split("|")]
            message[lane, cells[0]] = cells[3]
prune_rows = collections.defaultdict(set)
seen = set()
for lane in ("ci", "lanes"):
    for line in (root / f"{lane}-failing-ids.tsv").read_text().splitlines()[1:]:
        cluster, outcome, job, test_id = line.split("\t")
        if (job, test_id) in seen:
            continue
        seen.add((job, test_id))
        owner = by_cluster[lane].get(cluster) or next((c for p, c in globs if fnmatch.fnmatch(test_id.split("::")[0], p)), None)
        if owner == "AG-A1":
            continue  # a known CI-setup cause, not a deprecation
        if owner in PRUNE_OWNERS or PRUNE.search(message.get((lane, cluster), "")) or PRUNE.search(test_id):
            prune_rows[test_id.split("::")[0], f"{lane}:{cluster}", owner or "Wave C"].add((job, test_id))
total = sum(len(v) for v in prune_rows.values())
out = ["# Prune candidates", "",
       f"{total} failing IDs whose failure points at removed, retired, moved or legacy code, or that AG-P1 owns outright. "
       "Selected by message and test name, so some are false leads. AG-P1 sorts every row before its owning card "
       "fixes anything: **retire** (delete, citing the retiring change or D5's support line), **redundant** (delete, "
       "citing the passing test that covers the same behaviour) or **keep** (current behaviour, or updating from the "
       "previous published release: the owning card fixes it). AG-P1 sorts the `ci:` rows and AG-P2 the `lanes:` rows. See "
       "[D5](../../inputs.md#owner-decisions).", "",
       "| IDs | Test file | Cluster | Owning card | Message |", "| ---: | --- | --- | --- | --- |"]
for (path, ref, owner), ids in sorted(prune_rows.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    lane, cluster = ref.split(":")
    out.append(f"| {len(ids)} | `{path}` | {ref} | {owner} | {message.get((lane, cluster), '')[:90]} |")
(root / "prune-candidates.md").write_text("\n".join(out) + "\n")
print(f"prune candidates: {total} IDs in {len({k[0] for k in prune_rows})} files")
print(f"Wave C: {counts['Wave C']} IDs in {len(files)} files; owned by A/B: {sum(v for k, v in counts.items() if k != 'Wave C')}; total {sum(counts.values())}")
print({k: v for k, v in sorted(counts.items(), key=lambda kv: order(kv[0]))})
