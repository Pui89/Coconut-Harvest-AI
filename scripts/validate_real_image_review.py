"""Validate a manually completed coconut image-review CSV.

This is a standard-library data-quality check, not an image detector.
It does not download files, install packages, access the network, or upload data.
Run from the repository root:
    python scripts/validate_real_image_review.py
    python scripts/validate_real_image_review.py --csv data/real_image_samples/image_review.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "real_image_samples" / "image_review.csv"
REQUIRED_FIELDS = {
    "image_file",
    "source_page",
    "license",
    "visible_coconut_count",
    "occluded_or_partly_hidden_count",
    "lighting_conditions",
    "background_clutter",
    "review_notes",
}
COUNT_FIELDS = ("visible_coconut_count", "occluded_or_partly_hidden_count")
REVIEW_FIELDS = ("lighting_conditions", "background_clutter")


def parse_nonnegative_integer(value: str, field: str, line_number: int) -> int:
    value = value.strip()
    if not value:
        raise ValueError(f"line {line_number}: '{field}' is blank; enter a count or leave it explicitly marked unknown in review_notes.")
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"line {line_number}: '{field}' must be a whole number, got {value!r}.") from exc
    if parsed < 0:
        raise ValueError(f"line {line_number}: '{field}' cannot be negative.")
    return parsed


def validate_csv(csv_path: Path) -> tuple[int, int, list[str]]:
    errors: list[str] = []
    if not csv_path.is_file():
        return 0, 0, [
            f"Review CSV not found: {csv_path}",
            "First run: python scripts/prepare_real_image_review.py --download",
        ]

    reviewed_rows = 0
    total_rows = 0
    try:
        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = sorted(REQUIRED_FIELDS - headers)
            if missing:
                return 0, 0, [f"CSV is missing required columns: {', '.join(missing)}"]

            for line_number, row in enumerate(reader, start=2):
                total_rows += 1
                image_name = (row.get("image_file") or "").strip()
                if not image_name:
                    errors.append(f"line {line_number}: image_file is blank.")
                    continue

                # Only accept a filename, not an arbitrary path supplied by a CSV.
                if Path(image_name).name != image_name or image_name in {".", ".."}:
                    errors.append(f"line {line_number}: image_file must be a filename, not a path.")
                    continue

                image_path = csv_path.parent / image_name
                if not image_path.is_file():
                    errors.append(f"line {line_number}: image file not found beside the CSV: {image_name}")
                if not (row.get("source_page") or "").strip():
                    errors.append(f"line {line_number}: source_page is blank.")
                if not (row.get("license") or "").strip():
                    errors.append(f"line {line_number}: license is blank.")

                counts: dict[str, int] = {}
                row_ok = True
                for field in COUNT_FIELDS:
                    value = (row.get(field) or "").strip()
                    if not value:
                        row_ok = False
                        continue
                    try:
                        counts[field] = parse_nonnegative_integer(value, field, line_number)
                    except ValueError as exc:
                        errors.append(str(exc))
                        row_ok = False

                for field in REVIEW_FIELDS:
                    if not (row.get(field) or "").strip():
                        row_ok = False

                if not row_ok:
                    errors.append(
                        f"line {line_number}: review is incomplete; fill both counts and lighting/background, "
                        "or record uncertainty in review_notes and keep counts blank."
                    )
                elif all(image_path.is_file() for _ in [0]):
                    reviewed_rows += 1
    except (OSError, csv.Error) as exc:
        return 0, total_rows, [f"Could not read CSV: {exc}"]

    return total_rows, reviewed_rows, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to the manually completed review CSV.")
    args = parser.parse_args()
    csv_path = args.csv if args.csv.is_absolute() else ROOT / args.csv

    total, reviewed, errors = validate_csv(csv_path)
    print("Coconut Harvest AI — manual image-review validation")
    print(f"CSV: {csv_path}")
    print(f"Rows found: {total}")
    print(f"Complete rows with image files present: {reviewed}")
    print("AI detection metrics: NOT measured by this tool")
    print("3D localization / reachability / robot safety: NOT measured by this tool")

    if errors:
        print(f"Findings ({len(errors)}):")
        for item in errors:
            print(f"- {item}")
        print("Status: NEEDS REVIEW")
        return 1

    if total == 0:
        print("Status: NO REVIEW ROWS")
        return 1

    print("Status: CSV checks passed; this validates annotations only, not AI predictions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
