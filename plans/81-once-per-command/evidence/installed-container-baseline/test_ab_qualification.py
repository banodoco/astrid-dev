"""Release qualification requires sound load, receipts, and generation ratios."""
import json
import tempfile
import unittest
from pathlib import Path

from ab_summary import summarize

ARMS = {"before": {}, "after": {}, "vc48": {}}


def records(after=0.5):
    rows = []
    for group in ("same", "changed", "timeline"):
        for arm in ("before", "after"):
            for index in ("warmup", 1, 2):
                name = f"{group}-{arm}-{index}"
                row = {"name": name, "group": group, "arm": arm, "ok": True,
                       "exit_code": 0, "wall_seconds": 1.0 if arm == "before" else after,
                       "load_before": [0.99, 0, 0], "load_after": [1.01, 0, 0]}
                row["accepted_revision_id" if group == "timeline" else "kernel_task_id"] = name
                if group == "timeline":
                    row["timeline_status"] = "accepted"
                rows.append(row)
    for group in ("same", "changed", "timeline"):
        for arm in ARMS:
            for index in (("warmup", 1, 2, 3, 4, 5) if arm == "vc48" else (3, 4, 5)):
                name = f"{group}-{arm}-{index}"
                row = {"name": name, "group": group, "arm": arm, "ok": True,
                       "exit_code": 0, "wall_seconds": 1.0 if arm == "before" else after,
                       "load_before": [0.99, 0, 0], "load_after": [1.01, 0, 0]}
                row["accepted_revision_id" if group == "timeline" else "kernel_task_id"] = name
                if group == "timeline":
                    row["timeline_status"] = "accepted"
                rows.append(row)
    return rows


class QualificationTests(unittest.TestCase):
    def summary(self, rows, threshold=1.0, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            result = summarize(rows, tmp, "test", threshold, ARMS, 5, quiet=True, **kwargs)
            self.assertTrue((Path(tmp) / "summary-ab.json").exists())
            return result

    def test_release_recipe_and_diagnostic_evidence(self):
        for arms, samples in (({"before": {}, "after": {}}, 1),
                              (ARMS, 1), ({"before": {}, "after": {}}, 5),
                              (ARMS, 4), (ARMS, 6)):
            with self.subTest(arms=arms, samples=samples), tempfile.TemporaryDirectory() as tmp:
                rows = [r for r in records(after=0.4) if r["arm"] in arms and
                        (r["name"].endswith("-warmup") or int(r["name"].rsplit("-", 1)[1]) <= samples)]
                if samples == 6:
                    for group in ("same", "changed", "timeline"):
                        for arm in arms:
                            row = next(r.copy() for r in rows if r["name"] == f"{group}-{arm}-5")
                            row["name"] = f"{group}-{arm}-6"
                            field = "accepted_revision_id" if group == "timeline" else "kernel_task_id"
                            row[field] = row["name"]
                            rows.append(row)
                for row in rows:
                    row["door_port"] = 17340
                    identity = {"port": 17340, "address_hex": "0100007F", "socket_table": "tcp",
                                "socket_inode": "42", "pid": 100, "start_ticks": 10, "exe": "fixture",
                                "cwd": "fixture", "selected_version": "fixture", "manifest_shas": {},
                                "scope": "fixture"}
                    row["listener_before"] = row["listener_after"] = identity
                result = summarize(rows, tmp, "diagnostic", 1.0, arms, samples, quiet=True,
                                   require_attestation=True)
                self.assertFalse(result["qualification"]["passed"])
                self.assertEqual(result["records"], rows)
                self.assertEqual(json.loads((Path(tmp) / "summary-ab.json").read_text())["records"], rows)

    def test_load_must_be_finite_and_below_the_actual_gate(self):
        for invalid in (1.0, 1.01, float("nan"), float("inf"), -1, True, None):
            with self.subTest(load=invalid):
                rows = records()
                rows[0]["load_before"] = [invalid]
                self.assertFalse(self.summary(rows)["qualification"]["passed"])

    def test_receipts_are_required_and_distinct_across_generation_groups(self):
        for field, target, source in (("kernel_task_id", 6, 0), ("accepted_revision_id", 13, 12)):
            with self.subTest(field=field):
                rows = records()
                rows[target][field] = rows[source][field]
                self.assertFalse(self.summary(rows)["qualification"]["passed"])
        for group, field in (("same", "kernel_task_id"), ("timeline", "accepted_revision_id")):
            rows = records()
            next(r for r in rows if r["group"] == group).pop(field)
            self.assertFalse(self.summary(rows)["qualification"]["passed"])

    def test_timeline_status_must_be_accepted(self):
        for status in (None, "rejected", ""):
            rows = records()
            next(r for r in rows if r["group"] == "timeline")["timeline_status"] = status
            self.assertFalse(self.summary(rows)["qualification"]["passed"])

    def test_ratio_boundary_and_failed_evidence_are_recorded(self):
        self.assertTrue(self.summary(records())["qualification"]["passed"])
        self.assertFalse(self.summary(records(after=1.0))["qualification"]["passed"])
        result = self.summary(records(after=0.5004))
        self.assertFalse(result["qualification"]["passed"])
        self.assertEqual(len(result["records"]), len(records()))

    def test_exploratory_load_and_legacy_cannot_qualify(self):
        self.assertFalse(self.summary(records(), threshold=2.0)["qualification"]["passed"])
        rows = records()
        for r in rows:
            r.pop("kernel_task_id", None)
            r.pop("accepted_revision_id", None)
        self.assertFalse(self.summary(rows, legacy_missing_collector_span=True)["qualification"]["passed"])


if __name__ == "__main__":
    unittest.main()
