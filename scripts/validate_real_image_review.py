"""Validate a manually completed coconut image-review CSV.

Standard-library annotation quality check only; not an image detector.
No downloads, installs, network access, or uploads occur.
Run from the repository root: python scripts/validate_real_image_review.py
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "real_image_samples" / "image_review.csv"
REQUIRED_FIELDS = {
    "image_file", "source_page", "license", "visible_coconut_count",
    "occluded_or_partly_hidden_count", "lighting_conditions",
    "background_clutter", "review_notes",
}
COUNT_FIELDS = ("visible_coconut_count", "occluded_or_partly_hidden_count")
REVIEW_FIELDS = ("lighting_conditions", "background_clutter")
UNKNOWN_WORDS = ("unknown", "uncertain", "uncountable", "not countable", "not visible")


def validate_csv(csv_path: Path) -> tuple[int, int, list[str]]:
    errors: list[str] = []
    if not csv_path.is_file():
        return 0, 0, [
            f"Review CSV not found: {csv_path}",
            "First run: python scripts/prepare_real_image_review.py --download",
        ]
    reviewed_rows = total_rows = 0
    seen_image_names: set[str] = set()
    seen_image_hashes: dict[str, str] = {}
    try:
        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            missing = sorted(REQUIRED_FIELDS - set(reader.fieldnames or []))
            if missing:
                return 0, 0, [f"CSV is missing required columns: {', '.join(missing)}"]
            for line_number, row in enumerate(reader, start=2):
                total_rows += 1
                row_errors: list[str] = []
                image_name = (row.get("image_file") or "").strip()
                if not image_name or Path(image_name).name != image_name or image_name in {".", ".."}:
                    errors.append(f"line {line_number}: image_file must be a simple filename.")
                    continue
                duplicate_name = image_name in seen_image_names
                if duplicate_name:
                    row_errors.append(
                        f"line {line_number}: duplicate image_file entry: {image_name}"
                    )
                else:
                    seen_image_names.add(image_name)

                image_path = csv_path.parent / image_name
                if not image_path.is_file():
                    row_errors.append(f"line {line_number}: image file not found beside CSV: {image_name}")
                elif not duplicate_name:
                    try:
                        digest = hashlib.sha256(image_path.read_bytes()).hexdigest()
                    except OSError as exc:
                        row_errors.append(
                            f"line {line_number}: could not read image file {image_name}: {exc}"
                        )
                    else:
                        previous_name = seen_image_hashes.get(digest)
                        if previous_name is not None:
                            row_errors.append(
                                f"line {line_number}: image content duplicates {previous_name} "
                                f"even though the filename differs: {image_name}"
                            )
                        else:
                            seen_image_hashes[digest] = image_name

                if not (row.get("source_page") or "").strip():
                    row_errors.append(f"line {line_number}: source_page is blank.")
                if not (row.get("license") or "").strip():
                    row_errors.append(f"line {line_number}: license is blank.")

                notes = (row.get("review_notes") or "").strip().lower()
                explicitly_unknown = any(word in notes for word in UNKNOWN_WORDS)
                for field in COUNT_FIELDS:
                    value = (row.get(field) or "").strip()
                    if not value:
                        if not explicitly_unknown:
                            row_errors.append(
                                f"line {line_number}: {field} is blank; enter a non-negative whole number "
                                "or explain uncertainty in review_notes."
                            )
                        continue
                    try:
                        if int(value) < 0:
                            raise ValueError
                    except ValueError:
                        row_errors.append(
                            f"line {line_number}: {field} must be a non-negative whole number."
                        )
                for field in REVIEW_FIELDS:
                    if not (row.get(field) or "").strip():
                        row_errors.append(f"line {line_number}: {field} is blank.")
                if row_errors:
                    errors.extend(row_errors)
                else:
                    reviewed_rows += 1
    except (OSError, csv.Error) as exc:
        return 0, total_rows, [f"Could not read CSV: {exc}"]
    return total_rows, reviewed_rows, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to the review CSV.")
    args = parser.parse_args()
    csv_path = args.csv if args.csv.is_absolute() else ROOT / args.csv
    total, reviewed, errors = validate_csv(csv_path)
    print("Coconut Harvest AI — manual image-review validation")
    print(f"CSV: {csv_path}")
    print(f"Rows found: {total}")
    print(f"Complete rows with image files present: {reviewed}")
    print("AI detection metrics: NOT measured")
    print("3D localization / reachability / robot safety: NOT measured")
    if errors:
        print(f"Findings ({len(errors)}):")
        for error in errors:
            print(f"- {error}")
        print("Status: NEEDS REVIEW")
        return 1
    if total == 0:
        print("Status: NO REVIEW ROWS")
        return 1
    print("Status: CSV checks passed; this validates annotations only, not AI predictions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
