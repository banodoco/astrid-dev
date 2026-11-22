"""Deterministic unit coverage for the A-5 preparation helpers only.

These synthetic observations exercise validation logic. They do not exercise
production instrumentation, a real target, physical delay, or the live gate.
"""
from __future__ import annotations

import copy
import unittest

from tests.integrations.attribution_a5_checks import (
    GROUPS,
    PREFLIGHT_STAGES,
    REMAINDER,
    check_receipts,
    check_sample,
)
from tests.integrations.attribution_a5_count_policy import (
    METRICS,
    check_counts,
)


def make_policy(group, *, attempts=1, required=None):
    required = required or {"dispatch": 1, "SDK admission preflight": 1}
    preflights = {
        name: {"required": name in required,
               "reason": "synthetic route includes this preflight" if name in required
               else "synthetic route omits this preflight"}
        for name in PREFLIGHT_STAGES
    }
    return {group: {str(attempts): {"required_counts": dict(required),
                                    "preflights": preflights}}}


def make_sample(*, wall=10.0, span=10.0, named_seconds=9.0, rows=None):
    if rows is None:
        rows = [
            {"stage": "dispatch", "occurrence_id": 1,
             "seconds": named_seconds - 1.0},
            {"stage": "SDK admission preflight", "occurrence_id": 2,
             "seconds": 1.0},
            {"stage": REMAINDER, "seconds": span - named_seconds},
        ]
    return {"ok": True, "wall_seconds": wall,
            "collector_span_seconds": span, "timings": rows,
            "attempt_count": 1}


def make_receipt(group_index, sample_index):
    attempt = f"a-{group_index}-{sample_index}"
    base = float(group_index * 100 + sample_index * 10)
    return {
        "attempt_id": attempt,
        "task_id": f"task-{group_index}-{sample_index}",
        "target_prompt_id": f"target-{group_index}-{sample_index}",
        "task_attempt_id": attempt,
        "target_attempt_id": attempt,
        "drained": True,
        "spawn_monotonic": base,
        "admission_monotonic": base + 1,
        "target_ack_monotonic": base + 2,
        "exit_monotonic": base + 3,
        "drained_monotonic": base + 4,
    }


def make_count_policy(*, minimum=0, maximum=4):
    return {
        "version": 1,
        "groups": {
            group: {
                "1": {
                    metric: {"min": minimum, "max": maximum,
                             "rationale": "synthetic unit policy"}
                    for metric in METRICS
                }
            }
            for group in GROUPS
        },
    }


class AttributionA5SampleTests(unittest.TestCase):
    def test_independent_w_s_r_c_partition_and_reports_both_gaps(self):
        sample = make_sample(wall=10.0, span=9.5, named_seconds=9.0)
        result = check_sample("same", sample, clock_tolerance_seconds=0,
                              stage_policy=make_policy("same"))

        self.assertEqual(result["wall_seconds"], 10.0)  # W
        self.assertEqual(result["named_seconds"], 9.0)  # S
        self.assertEqual(result["remainder_seconds"], 0.5)  # R
        self.assertEqual(result["collector_span_seconds"], 9.5)  # C
        self.assertEqual(result["wall_minus_collector_seconds"], 0.5)  # W-C
        self.assertEqual(result["uncovered_share"], 0.1)  # (W-S)/W

        # The same W/C with only 8s of named work has 20% uncovered wall
        # and must fail the independent per-sample coverage bound.
        over_bound = make_sample(wall=10.0, span=9.5, named_seconds=8.0)
        with self.assertRaisesRegex(ValueError, "exceeds 10%"):
            check_sample("same", over_bound, clock_tolerance_seconds=0,
                         stage_policy=make_policy("same"))

    def test_rejects_missing_or_duplicate_remainder(self):
        for rows in (
            [{"stage": "dispatch", "occurrence_id": 1, "seconds": 8.0},
             {"stage": "SDK admission preflight", "occurrence_id": 2, "seconds": 1.0}],
            make_sample()["timings"] + [{"stage": REMAINDER, "seconds": 0.0}],
        ):
            with self.subTest(rows=rows), self.assertRaisesRegex(ValueError, "remainder"):
                check_sample("same", make_sample(rows=rows),
                             clock_tolerance_seconds=0,
                             stage_policy=make_policy("same"))

    def test_rejects_nonfinite_negative_and_overlapping_partition(self):
        bad_rows = [
            [{"stage": "dispatch", "occurrence_id": 1, "seconds": float("nan")},
             {"stage": "SDK admission preflight", "occurrence_id": 2, "seconds": 1.0},
             {"stage": REMAINDER, "seconds": 0.0}],
            [{"stage": "dispatch", "occurrence_id": 1, "seconds": 8.0},
             {"stage": "SDK admission preflight", "occurrence_id": 2, "seconds": 1.0},
             {"stage": REMAINDER, "seconds": -1.0}],
            [{"stage": "dispatch", "occurrence_id": 1, "seconds": 8.0},
             {"stage": "SDK admission preflight", "occurrence_id": 2, "seconds": 1.0},
             {"stage": REMAINDER, "seconds": 2.0}],
        ]
        for rows in bad_rows:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                check_sample("same", make_sample(rows=rows),
                             clock_tolerance_seconds=0,
                             stage_policy=make_policy("same"))

    def test_rejects_duplicate_occurrence_identity(self):
        rows = [
            {"stage": "dispatch", "occurrence_id": 7, "seconds": 8.0},
            {"stage": "SDK admission preflight", "occurrence_id": 7,
             "seconds": 1.0},
            {"stage": REMAINDER, "seconds": 1.0},
        ]
        with self.assertRaisesRegex(ValueError, "occurrence identity"):
            check_sample("same", make_sample(rows=rows),
                         clock_tolerance_seconds=0,
                         stage_policy=make_policy("same"))

    def test_controlled_external_gap_of_1_5_seconds_crosses_ten_percent(self):
        # Synthetic parent wall is 11.5s, collector span is 10s, and named
        # work is 10s. The controlled 1.5s outside-collector gap alone makes
        # (W-S)/W exceed 10%; no upper time ceiling participates.
        sample = make_sample(wall=11.5, span=10.0, named_seconds=10.0)
        with self.assertRaisesRegex(ValueError, "exceeds 10%"):
            check_sample("same", sample, clock_tolerance_seconds=0,
                         stage_policy=make_policy("same"))

    def test_each_of_five_groups_has_five_samples_with_positive_required_work(self):
        policy = {group: make_policy(group)[group] for group in GROUPS}
        for group in GROUPS:
            samples = [make_sample() for _ in range(5)]
            for sample in samples:
                result = check_sample(group, sample,
                                      clock_tolerance_seconds=0,
                                      stage_policy=policy)
                self.assertGreater(result["stage_counts"]["dispatch"], 0)
                self.assertGreater(result["stage_counts"]["SDK admission preflight"], 0)

    def test_missing_required_stage_and_zero_required_work_fail(self):
        missing = make_sample(rows=[
            {"stage": "dispatch", "occurrence_id": 1, "seconds": 9.0},
            {"stage": REMAINDER, "seconds": 1.0},
        ])
        with self.assertRaisesRegex(ValueError, "below"):
            check_sample("same", missing, clock_tolerance_seconds=0,
                         stage_policy=make_policy("same"))
        zero = make_sample(rows=[
            {"stage": "dispatch", "occurrence_id": 1, "seconds": 9.0},
            {"stage": "SDK admission preflight", "occurrence_id": 2,
             "seconds": 0.0},
            {"stage": REMAINDER, "seconds": 1.0},
        ])
        with self.assertRaisesRegex(ValueError, "no positive work"):
            check_sample("same", zero, clock_tolerance_seconds=0,
                         stage_policy=make_policy("same"))


class AttributionA5ReceiptTests(unittest.TestCase):
    def test_five_samples_per_group_have_unique_matched_drained_receipts(self):
        groups = {
            group: [make_receipt(group_index, sample_index)
                    for sample_index in range(5)]
            for group_index, group in enumerate(GROUPS)
        }
        self.assertIsNone(check_receipts(groups))

    def test_rejects_duplicate_missing_mismatched_or_undrained_receipt(self):
        groups = {
            group: [make_receipt(group_index, sample_index)
                    for sample_index in range(5)]
            for group_index, group in enumerate(GROUPS)
        }
        mutations = []
        duplicate = copy.deepcopy(groups)
        duplicate["same"][1]["task_id"] = duplicate["same"][0]["task_id"]
        mutations.append((duplicate, "distinct"))
        missing = copy.deepcopy(groups)
        del missing["same"][0]["target_prompt_id"]
        mutations.append((missing, "missing"))
        mismatch = copy.deepcopy(groups)
        mismatch["same"][0]["target_attempt_id"] = "another-attempt"
        mutations.append((mismatch, "unmatched"))
        undrained = copy.deepcopy(groups)
        undrained["same"][0]["drained"] = False
        mutations.append((undrained, "not drained"))
        for changed, message in mutations:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                check_receipts(changed)


class AttributionA5CountPolicyTests(unittest.TestCase):
    def test_exact_metrics_accept_zero_only_under_explicit_lower_bound(self):
        policy = make_count_policy(minimum=0, maximum=2)
        sample = {"attempt_count": 1, "counts": {metric: 0 for metric in METRICS}}
        self.assertEqual(check_counts("same", sample, policy), sample["counts"])

    def test_missing_zero_deleted_and_ratchet_violations_fail_closed(self):
        policy = make_count_policy(minimum=1, maximum=2)
        good = {"attempt_count": 1, "counts": {metric: 1 for metric in METRICS}}

        missing = copy.deepcopy(good)
        del missing["counts"][next(iter(METRICS))]
        with self.assertRaisesRegex(ValueError, "missing or unexpected"):
            check_counts("same", missing, policy)

        zero = copy.deepcopy(good)
        zero["counts"][next(iter(METRICS))] = 0
        with self.assertRaisesRegex(ValueError, "expected 1..2"):
            check_counts("same", zero, policy)

        deleted = copy.deepcopy(good)
        deleted["counts"] = {}
        with self.assertRaisesRegex(ValueError, "missing or unexpected"):
            check_counts("same", deleted, policy)

        over_ratchet = copy.deepcopy(good)
        over_ratchet["counts"][next(iter(METRICS))] = 3
        with self.assertRaisesRegex(ValueError, "expected 1..2"):
            check_counts("same", over_ratchet, policy)


if __name__ == "__main__":
    unittest.main()
