import csv

import pytest

from tools.summarize_dataset_readiness import summarize


FIELDS = [
    "candidate_id", "filename", "source_page_url", "creator_credit",
    "licence_as_displayed", "licence_url", "source_page_checked_on",
    "independent_page_check", "attribution_recorded", "annotation_qa_status",
    "training_promotion",
]


def _write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _row(**overrides):
    row = dict(
        candidate_id="0001", filename="coconut.jpg",
        source_page_url="https://example.org/image", creator_credit="Test creator",
        licence_as_displayed="CC0 1.0", licence_url="https://example.org/licence",
        source_page_checked_on="2026-10-21", independent_page_check="checked",
        attribution_recorded="yes", annotation_qa_status="passed",
        training_promotion="approved",
    )
    row.update(overrides)
    return row


def test_all_gates_must_pass(tmp_path):
    path = _write_csv(tmp_path / "audit.csv", [_row()])
    report = summarize(path)
    assert report["ready_for_training"] is True
    assert report["eligible_count"] == 1
    assert report["candidates"][0]["failed_gates"] == []


def test_unresolved_rights_and_annotation_fail_closed(tmp_path):
    path = _write_csv(
        tmp_path / "audit.csv",
        [_row(independent_page_check="no", annotation_qa_status="pending")],
    )
    report = summarize(path)
    assert report["ready_for_training"] is False
    assert report["eligible_count"] == 0
    assert "independent_page_check" in report["candidates"][0]["failed_gates"]
    assert "annotation_qa_passed" in report["candidates"][0]["failed_gates"]


def test_empty_audit_is_not_ready(tmp_path):
    path = _write_csv(tmp_path / "audit.csv", [])
    report = summarize(path)
    assert report["candidate_count"] == 0
    assert report["ready_for_training"] is False


def test_missing_required_column_fails(tmp_path):
    path = tmp_path / "audit.csv"
    path.write_text("candidate_id,filename\n0001,coconut.jpg\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing required columns"):
        summarize(path)


def test_duplicate_candidate_ids_are_reported(tmp_path):
    path = _write_csv(tmp_path / "audit.csv", [_row(), _row(filename="other.jpg")])
    report = summarize(path)
    assert any("duplicate candidate_id" in error for error in report["errors"])
    assert report["ready_for_training"] is False
