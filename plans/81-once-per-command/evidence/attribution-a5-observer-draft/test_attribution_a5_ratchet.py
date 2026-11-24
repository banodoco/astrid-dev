"""Synthetic adversarial coverage for the A-5 count baseline ratchet.

These tests exercise only baseline comparison policy. They do not validate
evidence references, production counters, or the live attribution gate.
"""
from __future__ import annotations

import copy
import unittest

from tests.integrations.attribution_a5_ratchet import (
    GROUPS,
    METRICS,
    PREFLIGHTS,
    baseline_digest,
    compare_baseline,
)


def make_baseline():
    return {
        "version": 1,
        "groups": {
            group: {
                "1": {
                    "metrics": {
                        metric: {"min": 1, "max": 4}
                        for metric in METRICS
                    },
                    "stages": {"dispatch": 1, "SDK admission preflight": 1},
                    "preflights": {
                        stage: {
                            "required": stage == "SDK admission preflight",
                            "evidence": f"oracle/{group}/1/{stage}",
                        }
                        for stage in PREFLIGHTS
                    },
                }
            }
            for group in GROUPS
        },
    }


def compare(prior, candidate, *, introductions=None, minimum_changes=None,
            pinned_prior_digest=None):
    return compare_baseline(
        prior,
        candidate,
        pinned_prior_digest=(pinned_prior_digest or baseline_digest(prior)),
        introductions={} if introductions is None else introductions,
        minimum_changes={} if minimum_changes is None else minimum_changes,
    )


def case_introductions(group, case, policy):
    references = {(group, case): "synthetic case evidence"}
    for field in ("metrics", "stages"):
        references.update({(group, case, field, name): "synthetic item evidence"
                           for name in policy[field]})
    return references


class AttributionA5RatchetTests(unittest.TestCase):
    def test_prior_must_match_pinned_digest(self):
        prior = make_baseline()
        with self.assertRaisesRegex(ValueError, "pinned digest"):
            compare(prior, copy.deepcopy(prior), pinned_prior_digest="0" * 64)

    def test_rejects_removed_group_case_metric_and_stage(self):
        prior = make_baseline()

        prior_with_extra_group = copy.deepcopy(prior)
        prior_with_extra_group["groups"]["legacy_group"] = copy.deepcopy(
            prior_with_extra_group["groups"]["same"]
        )
        candidate = copy.deepcopy(prior_with_extra_group)
        del candidate["groups"]["legacy_group"]
        with self.assertRaisesRegex(ValueError, "groups removed"):
            compare(prior_with_extra_group, candidate)

        candidate = copy.deepcopy(prior)
        candidate["groups"]["same"]["2"] = copy.deepcopy(candidate["groups"]["same"]["1"])
        del candidate["groups"]["same"]["1"]
        prior_with_two_cases = copy.deepcopy(prior)
        prior_with_two_cases["groups"]["same"]["2"] = copy.deepcopy(prior_with_two_cases["groups"]["same"]["1"])
        with self.assertRaisesRegex(ValueError, "cases removed"):
            compare(prior_with_two_cases, candidate)

        candidate = copy.deepcopy(prior)
        prior_with_extra_metric = copy.deepcopy(prior)
        prior_with_extra_metric["groups"]["same"]["1"]["metrics"]["custom_metric"] = {"min": 1, "max": 2}
        candidate = copy.deepcopy(prior_with_extra_metric)
        del candidate["groups"]["same"]["1"]["metrics"]["custom_metric"]
        with self.assertRaisesRegex(ValueError, "metrics removed"):
            compare(prior_with_extra_metric, candidate)

        prior_with_extra_stage = copy.deepcopy(prior)
        prior_with_extra_stage["groups"]["same"]["1"]["stages"]["other stage"] = 1
        candidate = copy.deepcopy(prior_with_extra_stage)
        del candidate["groups"]["same"]["1"]["stages"]["other stage"]
        with self.assertRaisesRegex(ValueError, "stages removed"):
            compare(prior_with_extra_stage, candidate)

    def test_rejects_count_max_increase_and_positive_minimum_removed(self):
        prior = make_baseline()
        candidate = copy.deepcopy(prior)
        metric = candidate["groups"]["same"]["1"]["metrics"]["hash_calls"]
        metric["max"] += 1
        with self.assertRaisesRegex(ValueError, "maximum increased"):
            compare(prior, candidate)

        candidate = copy.deepcopy(prior)
        candidate["groups"]["same"]["1"]["metrics"]["hash_calls"]["min"] = 0
        with self.assertRaisesRegex(ValueError, "positive minimum removed"):
            compare(prior, candidate)

    def test_positive_minimum_reduction_requires_evidence(self):
        prior = make_baseline()
        prior["groups"]["same"]["1"]["metrics"]["hash_calls"]["min"] = 3
        candidate = copy.deepcopy(prior)
        candidate["groups"]["same"]["1"]["metrics"]["hash_calls"]["min"] = 2
        with self.assertRaisesRegex(ValueError, "minimum change"):
            compare(prior, candidate)

        evidence_key = ("same", "1", "metrics", "hash_calls")
        compare(prior, candidate, minimum_changes={evidence_key: "oracle/optimized-hash-count"})

    def test_stage_minimum_change_requires_evidence(self):
        prior = make_baseline()
        candidate = copy.deepcopy(prior)
        candidate["groups"]["same"]["1"]["stages"]["dispatch"] = 2
        with self.assertRaisesRegex(ValueError, "minimum change"):
            compare(prior, candidate)

        evidence_key = ("same", "1", "stages", "dispatch")
        compare(prior, candidate, minimum_changes={evidence_key: "oracle/dispatch-route"})

    def test_new_group_and_case_need_their_own_introduction_references(self):
        prior = make_baseline()
        candidate = copy.deepcopy(prior)
        candidate["groups"]["new_group"] = copy.deepcopy(candidate["groups"]["same"])
        candidate["groups"]["new_group"]["2"] = copy.deepcopy(candidate["groups"]["new_group"]["1"])
        with self.assertRaisesRegex(ValueError, "introduction"):
            compare(prior, candidate)
        with self.assertRaisesRegex(ValueError, "introduction"):
            compare(prior, candidate, introductions={
                ("new_group", None): "oracle/new-group",
            })
        references = {("new_group", None): "oracle/new-group"}
        for case, policy in candidate["groups"]["new_group"].items():
            references.update(case_introductions("new_group", case, policy))
        compare(prior, candidate, introductions=references)

        candidate = copy.deepcopy(prior)
        candidate["groups"]["same"]["2"] = copy.deepcopy(candidate["groups"]["same"]["1"])
        with self.assertRaisesRegex(ValueError, "introduction"):
            compare(prior, candidate)
        compare(prior, candidate, introductions=case_introductions(
            "same", "2", candidate["groups"]["same"]["2"]))

    def test_new_metric_and_stage_need_per_item_references(self):
        prior = make_baseline()
        candidate = copy.deepcopy(prior)
        candidate["groups"]["same"]["1"]["metrics"]["custom_hash_metric"] = {
            "min": 1, "max": 2,
        }
        candidate["groups"]["same"]["1"]["stages"]["new operation"] = 1
        metric_key = ("same", "1", "metrics", "custom_hash_metric")
        stage_key = ("same", "1", "stages", "new operation")
        with self.assertRaisesRegex(ValueError, "introduction"):
            compare(prior, candidate)
        with self.assertRaisesRegex(ValueError, "introduction"):
            compare(prior, candidate, introductions={metric_key: "oracle/custom-metric"})
        compare(prior, candidate, introductions={
            metric_key: "oracle/custom-metric",
            stage_key: "oracle/new-operation",
        })


if __name__ == "__main__":
    unittest.main()
