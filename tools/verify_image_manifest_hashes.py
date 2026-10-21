#!/usr/bin/env python3
"""Verify dataset-manifest SHA-256 values against actual local image files.

Standard-library only. Detects exact-byte duplicates across splits; it does not
detect resized/near-duplicate images or assess labels.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import defaultdict
from pathlib import Path

REQUIRED = {"image_id", "filename", "split", "group_id", "sha256"}
SPLITS = {"train", "validation", "test", "challenge", "unassigned"}

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def verify(manifest: Path, images_dir: Path) -> dict:
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = list(reader)
    root = images_dir.resolve()
    errors, results = [], []
    actual_hashes = defaultdict(list)
    for line, row in enumerate(rows, start=2):
        rec = {key: (row.get(key) or "").strip() for key in REQUIRED}
        issues = []
        for key in ("image_id", "filename", "split", "group_id", "sha256"):
            if not rec[key]:
                issues.append(key + "_required")
        if rec["split"] and rec["split"] not in SPLITS:
            issues.append("invalid_split")
        relative = Path(rec["filename"]) if rec["filename"] else Path(".")
        if relative.is_absolute():
            issues.append("absolute_filename_not_allowed")
        target = (root / relative).resolve()
        if target != root and root not in target.parents:
            issues.append("filename_escapes_images_directory")
        actual = None
        if not issues and target.is_file():
            try:
                actual = sha256_file(target)
            except OSError as exc:
                issues.append("file_read_error:" + str(exc))
        elif not issues:
            issues.append("image_file_missing")
        if actual is not None:
            if rec["sha256"].lower() != actual:
                issues.append("manifest_sha256_mismatch")
            actual_hashes[actual].append({"line": line, "image_id": rec["image_id"],
                "filename": rec["filename"], "split": rec["split"]})
        errors.extend("line " + str(line) + ": " + issue for issue in issues)
        results.append({"line": line, "image_id": rec["image_id"], "filename": rec["filename"],
            "split": rec["split"], "declared_sha256": rec["sha256"].lower(),
            "actual_sha256": actual, "issues": issues, "passed": not issues})
    duplicates = []
    for digest, items in sorted(actual_hashes.items()):
        splits = sorted({item["split"] for item in items})
        if len(items) > 1 and len(splits) > 1:
            duplicates.append({"sha256": digest, "splits": splits, "files": items,
                "issue": "identical_file_bytes_across_splits"})
            errors.append("identical file bytes occur across splits: " + ", ".join(splits))
    return {"schema": "pui89-coconut-image-manifest-verification-v1",
        "manifest": manifest.name, "images_directory": str(root), "row_count": len(rows),
        "verified_file_count": sum(item["actual_sha256"] is not None for item in results),
        "manifest_hash_mismatches": sum("manifest_sha256_mismatch" in item["issues"] for item in results),
        "missing_or_unreadable_files": sum(any(issue.startswith(("image_file_missing", "file_read_error")) for issue in item["issues"]) for item in results),
        "exact_duplicate_cross_split_findings": duplicates, "errors": errors,
        "passed": bool(rows) and not errors,
        "limitations": ["SHA-256 is computed from local file bytes and compared with the manifest.",
            "Detects exact-byte duplicates only, not resized or visually similar images.",
            "Does not verify licences, annotations, source-group independence, or model performance."],
        "files": results}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--images-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = verify(args.manifest, args.images_dir)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
