"""Create SHA-256 and human-review manifests for a local candidate image batch.

This tool records file identity and prepares review fields. It does not verify
licence rights, identify coconut maturity, label fruit, or approve training.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    collection = args.collection_dir.expanduser().resolve()
    images = collection / "images"
    provenance = collection / "provenance.csv"
    if not images.is_dir() or not provenance.is_file():
        parser.error("collection-dir must contain images/ and provenance.csv")
    with provenance.open(newline="", encoding="utf-8-sig") as stream:
        source_rows = list(csv.DictReader(stream))
    by_file = {row.get("local_file", ""): row for row in source_rows}
    image_paths = sorted(path for path in images.iterdir() if path.is_file())
    args.output_dir.mkdir(parents=True, exist_ok=True)
    hash_rows, review_rows = [], []
    for index, path in enumerate(image_paths, start=1):
        relative = f"images/{path.name}"
        source = by_file.get(relative, {})
        digest = sha256_file(path)
        candidate_id = f"COC-{index:04d}"
        hash_rows.append({"candidate_id": candidate_id, "filename": path.name,
                          "relative_path": relative, "sha256": digest,
                          "bytes": path.stat().st_size})
        review_rows.append({
            "candidate_id": candidate_id, "filename": path.name, "sha256": digest,
            "source_page_url": source.get("file_page_url", ""),
            "creator_credit": source.get("credit", "") or source.get("artist", ""),
            "declared_license": source.get("license_short_name", ""),
            "rights_review": "UNREVIEWED", "visual_relevance": "UNREVIEWED",
            "tree_attached": "UNKNOWN", "appearance_class": "UNREVIEWED",
            "biological_maturity": "NOT_ESTABLISHED", "target_product": "UNSELECTED",
            "product_suitability": "NOT_ESTABLISHED", "human_reviewer": "",
            "review_notes": "", "training_approved": "false",
        })
    def write_csv(path: Path, rows: list[dict], empty_fields: list[str]) -> None:
        fields = list(rows[0]) if rows else empty_fields
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    write_csv(args.output_dir / "image_hash_manifest.csv", hash_rows,
              ["candidate_id", "filename", "relative_path", "sha256", "bytes"])
    review_fields = ["candidate_id", "filename", "sha256", "source_page_url",
        "creator_credit", "declared_license", "rights_review", "visual_relevance",
        "tree_attached", "appearance_class", "biological_maturity", "target_product",
        "product_suitability", "human_reviewer", "review_notes", "training_approved"]
    write_csv(args.output_dir / "human_review_template.csv", review_rows, review_fields)
    summary = {
        "candidate_count": len(image_paths), "hashed_file_count": len(hash_rows),
        "rights_approved_count": 0, "human_reviewed_count": 0,
        "training_approved_count": 0,
        "status": "CANDIDATES_ONLY_HUMAN_REVIEW_REQUIRED",
        "important_boundary": "SHA-256 confirms file identity only; it does not establish licence rights, visual relevance, maturity, product suitability, annotation correctness, or training approval.",
    }
    (args.output_dir / "batch_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
