#!/usr/bin/env python3
"""Convert complete unittest -v logs into baseline-diff status lines."""
import re
import sys
from pathlib import Path

CASE = re.compile(r"^(?P<method>test_\w+) \((?P<module>test_\w+)\.(?P<class>\w+)\.(?P<same>test_\w+)\) \.\.\. (?P<tail>.*)$")
COUNT = re.compile(r"^Ran (\d+) tests? in ")


def convert(source, target):
    lines = Path(source).read_text(errors="replace").splitlines()
    expected = next((int(m.group(1)) for line in lines if (m := COUNT.match(line))), None)
    if expected is None:
        raise SystemExit(f"{source}: missing unittest summary count")
    out = []
    i = 0
    while i < len(lines):
        m = CASE.match(lines[i])
        if m:
            if m.group("method") != m.group("same"):
                raise SystemExit(f"{source}:{i+1}: method/node mismatch")
            tail = m.group("tail").strip()
            if tail in ("ok", "FAIL", "ERROR", "expected failure", "unexpected success"):
                status = tail
            elif i + 1 < len(lines) and lines[i+1].strip() in ("ok", "FAIL", "ERROR"):
                i += 1
                status = lines[i].strip()
            else:
                raise SystemExit(f"{source}:{i+1}: ambiguous unittest outcome: {tail!r}")
            node = f"scripts/{m.group('module')}.py::{m.group('class')}::{m.group('method')}"
            tag = "FAILED" if status in ("FAIL", "ERROR", "unexpected success") else "PASSED"
            out.append(f"{tag} {node}")
        i += 1
    if len(out) != expected:
        raise SystemExit(f"{source}: summary says {expected}, parsed {len(out)} cases")
    Path(target).write_text("\n".join(out) + "\n")
    print(f"{source}: {len(out)} cases -> {target}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: unittest-to-baseline.py INPUT.log OUTPUT.log")
    convert(sys.argv[1], sys.argv[2])
