"""Regression tests for the read-only combined Coconut dataset preflight."""
import csv
import json
from pathlib import Path

from tools.run_coconut_dataset_preflight import build_report

RIGHTS_FIELDS = [
    "candidate_id", "filename", "source_page_url", "creator_credit",
    "licence_as_displayed", "licence_url", "source_page_checked_on",
    "independent_page_check", "attribution_recorded", "annotation_qa_status",
    "training_promotion",
]
REVIEW_FIELDS = [
    "candidate_id", "filename", "visual_triage", "label_status",
    "source_page_independently_checked", "review_decision", "review_notes",
]


def _write_csv(path: Path, fields: list[str], row: dict[str, str]) -> Path:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)
    return path


def _inputs(tmp_path: Path, *, approved: bool = True):
    rights = {
        "candidate_id": "T1",
        "filename": "coconut.jpg",
        "source_page_url": "https://example.org/photo",
        "creator_credit": "Photographer",
        "licence_as_displayed": "CC BY 4.0",
        "licence_url": "https://creativecommons.org/licenses/by/4.0/",
        "source_page_checked_on": "2026-10-21",
        "independent_page_check": "checked",
        "attribution_recorded": "yes",
        "annotation_qa_status": "passed" if approved else "pending",
        "training_promotion": "approved" if approved else "pending",
    }
    review = {
        "candidate_id": "T1",
        "filename": "coconut.jpg",
        "visual_triage": "positive_candidate",
        "label_status": "qa_passed" if approved else "not_reviewed",
        "source_page_independently_checked": "yes",
        "review_decision": "approved" if approved else "pending",
        "review_notes": "Fixture only; not a real dataset approval.",
    }
    annotations = tmp_path / "annotations.json"
    annotations.write_text(json.dumps({
        "format": "pui89-coconut-annotations-v1",
        "images": [{
            "filename": "coconut.jpg",
            "width": 100,
            "height": 100,
            "boxes": [{"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4}],
        }],
        "human_qa_acknowledged": False,
        "training_approved": False,
    }), encoding="utf-8")
    rights_path = _write_csv(tmp_path / "rights.csv", RIGHTS_FIELDS, rights)
    review_path = _write_csv(tmp_path / "review.csv", REVIEW_FIELDS, review)
    return annotations, rights_path, review_path


def test_valid_geometry_and_ledgers_without_source_bytes_stays_incomplete(tmp_path):
    annotations, rights, review = _inputs(tmp_path)
    before = (annotations.read_bytes(), rights.read_bytes(), review.read_bytes())

    report = build_report(annotations, rights, review)

    assert report["geometry"]["status"] == "PASS"
    assert report["promotion_gate"]["status"] == "PASS"
    assert report["candidate_0032_source_fingerprint"]["status"] == "NOT_CHECKED"
    assert report["overall_status"] == "INCOMPLETE"
    assert report["geometry"]["human_visual_qa"] == "NOT_CHECKED_BY_AUTOMATION"
    assert (annotations.read_bytes(), rights.read_bytes(), review.read_bytes()) == before


def test_unapproved_ledger_stays_blocked_even_when_geometry_is_valid(tmp_path):
    annotations, rights, review = _inputs(tmp_path, approved=False)

    report = build_report(annotations, rights, review)

    assert report["geometry"]["status"] == "PASS"
    assert report["promotion_gate"]["status"] == "BLOCKED"
    assert report["overall_status"] == "BLOCKED"


def test_invalid_box_geometry_blocks_combined_preflight(tmp_path):
    annotations, rights, review = _inputs(tmp_path)
    payload = json.loads(annotations.read_text(encoding="utf-8"))
    payload["images"][0]["boxes"][0]["w"] = 1.5
    annotations.write_text(json.dumps(payload), encoding="utf-8")

    report = build_report(annotations, rights, review)

    assert report["geometry"]["status"] == "BLOCKED"
    assert report["overall_status"] == "BLOCKED"
    assert report["promotion_gate"]["status"] == "PASS"
