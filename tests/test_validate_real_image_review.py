import csv

from scripts.validate_real_image_review import validate_csv


def test_duplicate_image_rows_are_flagged(tmp_path):
    image = tmp_path / "coconut.jpg"
    image.write_bytes(b"test image placeholder")
    review_csv = tmp_path / "image_review.csv"
    fields = [
        "image_file", "source_page", "license", "visible_coconut_count",
        "occluded_or_partly_hidden_count", "lighting_conditions",
        "background_clutter", "review_notes",
    ]
    row = {
        "image_file": "coconut.jpg",
        "source_page": "https://example.org/source",
        "license": "CC0 1.0 (test fixture; not a rights verification)",
        "visible_coconut_count": "2",
        "occluded_or_partly_hidden_count": "1",
        "lighting_conditions": "daylight",
        "background_clutter": "moderate",
        "review_notes": "synthetic test fixture only",
    }
    with review_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)
        writer.writerow(row)

    total, reviewed, errors = validate_csv(review_csv)

    assert total == 2
    assert reviewed == 1
    assert any("duplicate image_file entry: coconut.jpg" in error for error in errors)
