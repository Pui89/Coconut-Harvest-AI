import csv

from scripts.validate_real_image_review import validate_csv


FIELDS = [
    "image_file", "source_page", "license", "visible_coconut_count",
    "occluded_or_partly_hidden_count", "lighting_conditions",
    "background_clutter", "review_notes",
]


def _write_rows(tmp_path, rows):
    review_csv = tmp_path / "image_review.csv"
    with review_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return review_csv


def _row(image_name):
    return {
        "image_file": image_name,
        "source_page": "https://example.org/source",
        "license": "CC0 1.0 (test fixture; not a rights verification)",
        "visible_coconut_count": "2",
        "occluded_or_partly_hidden_count": "1",
        "lighting_conditions": "daylight",
        "background_clutter": "moderate",
        "review_notes": "synthetic test fixture only",
    }


def test_duplicate_image_rows_are_flagged(tmp_path):
    (tmp_path / "coconut.jpg").write_bytes(b"test image placeholder")
    review_csv = _write_rows(tmp_path, [_row("coconut.jpg"), _row("coconut.jpg")])

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 2
    assert reviewed == 1
    assert any("duplicate image_file entry: coconut.jpg" in error for error in errors)


def test_same_image_bytes_under_different_names_are_flagged(tmp_path):
    image_bytes = b"same synthetic image bytes"
    (tmp_path / "coconut.jpg").write_bytes(image_bytes)
    (tmp_path / "renamed-copy.jpg").write_bytes(image_bytes)
    review_csv = _write_rows(
        tmp_path, [_row("coconut.jpg"), _row("renamed-copy.jpg")]
    )

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 2
    assert reviewed == 1
    assert any(
        "image content duplicates coconut.jpg" in error
        and "renamed-copy.jpg" in error
        for error in errors
    )


def test_negative_coconut_count_is_rejected(tmp_path):
    (tmp_path / "coconut.jpg").write_bytes(b"synthetic image bytes")
    row = _row("coconut.jpg")
    row["visible_coconut_count"] = "-1"
    review_csv = _write_rows(tmp_path, [row])

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 1
    assert reviewed == 0
    assert any("visible_coconut_count must be a non-negative whole number" in error for error in errors)


def test_blank_count_requires_explicit_uncertainty_note(tmp_path):
    (tmp_path / "coconut.jpg").write_bytes(b"synthetic image bytes")
    row = _row("coconut.jpg")
    row["visible_coconut_count"] = ""
    review_csv = _write_rows(tmp_path, [row])

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 1
    assert reviewed == 0
    assert any("explain uncertainty in review_notes" in error for error in errors)


def test_blank_count_is_allowed_when_uncertainty_is_documented(tmp_path):
    (tmp_path / "coconut.jpg").write_bytes(b"synthetic image bytes")
    row = _row("coconut.jpg")
    row["visible_coconut_count"] = ""
    row["review_notes"] = "uncertain count due to occlusion"
    review_csv = _write_rows(tmp_path, [row])

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 1
    assert reviewed == 1
    assert errors == []


def test_empty_review_csv_fails_closed(tmp_path):
    review_csv = _write_rows(tmp_path, [])

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 0
    assert reviewed == 0
    assert errors == []
