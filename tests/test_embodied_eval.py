import json

import pytest

from tools.embodied_eval import summarize_results, validate_result, write_report


def case(case_id="case-001", status="pass", **extra):
    return {
        "case_id": case_id,
        "scenario": "smoke-test",
        "expected": "target-reached",
        "observed": "target-reached",
        "status": status,
        "safety_violations": [],
        **extra,
    }


def test_valid_result_has_no_errors():
    assert validate_result(case()) == []


def test_missing_fields_are_reported():
    assert "missing required fields: expected, observed, scenario, status" in validate_result(
        {"case_id": "case-001"}
    )[0]


def test_safety_violation_cannot_be_marked_pass():
    errors = validate_result(case(safety_violations=["entered-no-go-zone"]))
    assert any("cannot have status='pass'" in error for error in errors)


def test_summary_excludes_blocked_cases_from_pass_rate():
    report = summarize_results([
        case("a", "pass"),
        case("b", "fail", observed="target-not-reached"),
        case("c", "blocked"),
    ])
    assert report["valid_status_counts"] == {"pass": 1, "fail": 1, "blocked": 1}
    assert report["completed_cases"] == 2
    assert report["pass_rate"] == 0.5


def test_summary_flags_duplicate_case_ids():
    report = summarize_results([case("duplicate"), case("duplicate")])
    assert any("duplicate case_id" in error for item in report["validation_errors"] for error in item["errors"])


def test_write_report_creates_readable_json(tmp_path):
    output = tmp_path / "reports" / "evaluation.json"
    report = write_report("example-project", [case()], output)
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["project"] == "example-project"
    assert saved["schema_version"] == "1.0"
    assert saved["valid_status_counts"]["pass"] == 1
    assert report["total_records"] == 1


def test_empty_completed_set_has_no_pass_rate():
    assert summarize_results([case("blocked", "blocked")])["pass_rate"] is None


def test_invalid_project_name_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        write_report(" ", [], tmp_path / "report.json")
