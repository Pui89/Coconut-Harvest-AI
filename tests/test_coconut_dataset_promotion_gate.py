import csv

from tools.coconut_dataset_promotion_gate import evaluate, main

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



def test_cli_report_file_ends_with_real_newline(tmp_path, monkeypatch, capsys):
    rights, review = records()
    rights["annotation_qa_status"] = "pending"
    rights_path = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    review_path = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    output_path = tmp_path / "report.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "coconut_dataset_promotion_gate",
            "--rights-csv", str(rights_path),
            "--review-csv", str(review_path),
            "--output", str(output_path),
        ],
    )

    assert main() == 1
    capsys.readouterr()
    report_text = output_path.read_text(encoding="utf-8")
    assert report_text.endswith("\n")
    assert not report_text.endswith("\\n")


def test_blank_filename_blocks_candidate_even_when_both_ledgers_match(tmp_path):
    rights, review = records()
    rights["filename"] = ""
    review["filename"] = ""
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    report = evaluate(a, b)
    candidate = report["candidates"][0]
    assert not candidate["eligible_for_training"]
    assert not report["ready_for_training"]
    assert "filename_present" in candidate["failed_gates"]
    assert "review_filename_present" in candidate["failed_gates"]
    assert "review_filename_matches" in candidate["failed_gates"]




def test_non_http_source_or_licence_urls_block_candidate(tmp_path):
    rights, review = records()
    rights["source_page_url"] = "javascript:alert(1)"
    rights["licence_url"] = "file:///private/licence"
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    candidate = evaluate(a, b)["candidates"][0]
    assert not candidate["eligible_for_training"]
    assert "source_page_is_http_url" in candidate["failed_gates"]
    assert "licence_url_is_http_url" in candidate["failed_gates"]


def test_invalid_source_page_check_date_blocks_candidate(tmp_path):
    rights, review = records()
    rights["source_page_checked_on"] = "2026-02-30"
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    candidate = evaluate(a, b)["candidates"][0]
    assert not candidate["eligible_for_training"]
    assert "source_page_check_date_valid" in candidate["failed_gates"]


def test_valid_https_urls_and_iso_date_pass_metadata_checks(tmp_path):
    rights, review = records()
    a = write_csv(tmp_path / "rights.csv", RIGHTS, [rights])
    b = write_csv(tmp_path / "review.csv", REVIEWS, [review])
    candidate = evaluate(a, b)["candidates"][0]
    assert candidate["eligible_for_training"]
