"""Adversarial edge cases for benchmark metadata validation.

Passing these tests means the report is structurally checkable, not that its
metrics are scientifically valid or reflect a real robot run.
"""
from copy import deepcopy

import pytest

from tools.validate_benchmark_report import validate_report
from test_benchmark_report_validator import valid_report


@pytest.mark.parametrize("report", [None, [], "not a report", 7, True])
def test_non_object_top_level_is_rejected(report):
    errors = validate_report(report)
    assert errors
    assert "$ must contain a JSON object" in errors[0]


@pytest.mark.parametrize("value", [True, False, "0.9", None, [], {}])
def test_non_numeric_metric_leaf_is_rejected(value):
    report = deepcopy(valid_report())
    report["metrics"]["perception"]["precision"] = value
    assert any("$.metrics.perception.precision" in error for error in validate_report(report))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_nested_metric_is_rejected(value):
    report = deepcopy(valid_report())
    report["metrics"]["systems"]["cycle_time_seconds"] = value
    assert any("must be finite" in error for error in validate_report(report))


def test_empty_nested_metric_group_is_rejected():
    report = deepcopy(valid_report())
    report["metrics"]["empty_group"] = {}
    assert any("$.metrics.empty_group" in error for error in validate_report(report))


@pytest.mark.parametrize("field", ["project", "run_id"])
def test_blank_identifiers_are_rejected(field):
    report = deepcopy(valid_report())
    report[field] = "   "
    assert any(f"$.{field} must be a non-empty string" in error for error in validate_report(report))


@pytest.mark.parametrize("timestamp", ["not-a-date", "", None, "2026-10-09T02:00:00"])
def test_invalid_or_timezone_naive_timestamps_are_rejected(timestamp):
    report = deepcopy(valid_report())
    report["run_date_utc"] = timestamp
    errors = validate_report(report)
    assert any("$.run_date_utc" in error for error in errors)


def test_boolean_config_seed_is_not_accepted_as_a_valid_seed():
    # A bool is an int subclass in Python; explicitly reject it as a seed.
    # This assertion documents a strictness requirement and will fail until
    # the validator enforces the intended integer-only seed contract.
    report = deepcopy(valid_report())
    report["config"]["seed"] = True
    errors = validate_report(report)
    assert any("$.config.seed" in error for error in errors)
