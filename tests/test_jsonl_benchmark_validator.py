"""Regression tests for the JSONL benchmark-record validator.

These tests validate report structure only; they do not run a detector or establish
perception, harvesting, or field performance.
"""
import math

from benchmarks.validate_results import validate_record


def valid_record():
    return {
        "scenario": "validator-test",
        "metric": "example_score",
        "value": 0.5,
        "unit": "fraction",
        "split": "synthetic",
        "seed": 0,
        "source": "synthetic",
        "notes": "Validator fixture only; not a performance claim.",
    }


def test_valid_record_passes():
    assert validate_record(valid_record(), 1) == []


def test_missing_required_fields_are_reported():
    record = valid_record()
    del record["source"]
    errors = validate_record(record, 3)
    assert any("missing fields: source" in error for error in errors)


def test_boolean_is_not_accepted_as_numeric_value():
    record = valid_record()
    record["value"] = True
    assert any("value must be a finite number" in error for error in validate_record(record, 1))


def test_non_finite_values_are_rejected():
    for value in (math.nan, math.inf, -math.inf):
        record = valid_record()
        record["value"] = value
        assert any("value must be a finite number" in error for error in validate_record(record, 1))


def test_seed_must_be_an_integer_and_not_boolean():
    for seed in (True, 1.5, "7"):
        record = valid_record()
        record["seed"] = seed
        assert any("seed must be an integer" in error for error in validate_record(record, 1))


def test_required_text_fields_must_not_be_blank():
    for field in ("scenario", "metric", "unit", "split", "source", "notes"):
        record = valid_record()
        record[field] = "   "
        assert any(f"{field} must be a non-empty string" in error for error in validate_record(record, 1))


def test_non_object_record_is_rejected():
    assert "record must be a JSON object" in validate_record(["not", "an", "object"], 4)[0]
