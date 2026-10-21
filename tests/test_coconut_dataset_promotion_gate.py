import csv

from tools.coconut_dataset_promotion_gate import evaluate

RIGHTS = [
    "candidate_id", "filename", "source_page_url", "creator_credit",
    "licence_as_displayed", "licence_url", "source_page_checked_on",
    "independent_page_check", "attribution_recorded", "annotation_qa_status",
    "training_promotion",
]
REVIEWS = [
    "candidate_id", "filename", "visual_triage", "label_status",
    "source_page_independently_checked", "review_decision", "review_notes",
]


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path


def records():
    rights = dict(candidate_id="A1", filename="coconut.jpg",
        source_page_url="https://example.org/photo", creator_credit="Photographer",
        licence_as_displayed="CC BY 4.0", licence_url="https://creativecommons.org/licenses/by/4.0/",
        source_page_checked_on="2026-10-21", independent_page_check="checked",
        attribution_recorded="yes", annotation_qa_status="passed", training_promotion="approved")
    review = dict(candidate_id="A1", filename="coconut.jpg", visual_triage="positive_candidate",
        label_status="qa_passed", source_page_independently_checked="yes",
        review_decision="approved", review_notes="Independent box review completed.")
    return rights, review


def test_passes_only_when_both_ledgers_agree(tmp_path):
    rights, review = records()
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    report = evaluate(a, b)
    assert report["ready_for_training"] is True
    assert report["eligible_count"] == 1
    assert report["candidates"][0]["failed_gates"] == []


def test_pending_annotation_blocks_candidate(tmp_path):
    rights, review = records()
    rights["annotation_qa_status"] = "pending"
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    report = evaluate(a, b)
    assert not report["ready_for_training"]
    assert "annotation_qa_passed" in report["candidates"][0]["failed_gates"]


def test_filename_mismatch_blocks_candidate(tmp_path):
    rights, review = records()
    review["filename"] = "different.jpg"
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    report = evaluate(a, b)
    assert not report["candidates"][0]["eligible_for_training"]
    assert "review_filename_matches" in report["candidates"][0]["failed_gates"]


def test_archived_or_unapproved_labels_block_candidate(tmp_path):
    rights, review = records()
    review["label_status"] = "archived_9_boxes"
    review["review_decision"] = "excluded_from_active_training"
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    report = evaluate(a, b)
    assert not report["ready_for_training"]
    assert "label_qa_passed" in report["candidates"][0]["failed_gates"]
    assert "candidate_review_approved" in report["candidates"][0]["failed_gates"]


def test_duplicate_ids_are_structural_error(tmp_path):
    rights, review = records()
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights, rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    report = evaluate(a, b)
    assert report["errors"]
    assert not report["ready_for_training"]
