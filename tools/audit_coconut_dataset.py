#!/usr/bin/env python3
"""Audit a local coconut candidate manifest and annotation drafts without promoting data.

This tool performs structural checks only. It does not inspect image pixels, verify
licence suitability, judge box correctness, or approve data for training.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit(manifest: Any, images_dir: Path, annotations_dir: Path | None = None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    checked_images = 0
    checked_annotations = 0
    total_boxes = 0
    candidates = manifest.get("candidates") if isinstance(manifest, dict) else None
    if not isinstance(candidates, list):
        return {
            "schema": "pui89-coconut-dataset-audit-v1",
            "passed_structural_checks": False,
            "training_approved_count": 0,
            "errors": ["manifest must contain a candidates list"],
            "warnings": ["Structural checks are not human visual QA or licence approval."],
        }

    seen_ids: set[str] = set()
    seen_files: set[str] = set()
    for idx, candidate in enumerate(candidates):
        where = f"candidates[{idx}]"
        if not isinstance(candidate, dict):
            errors.append(f"{where}: candidate must be an object")
            continue
        candidate_id = candidate.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            errors.append(f"{where}: missing candidate_id")
        elif candidate_id in seen_ids:
            errors.append(f"{where}: duplicate candidate_id {candidate_id!r}")
        else:
            seen_ids.add(candidate_id)

        filename = candidate.get("local_file")
        if candidate.get("downloaded") is True:
            if not isinstance(filename, str) or not filename.strip():
                errors.append(f"{where}: downloaded candidate has no local_file")
                continue
            rel = Path(filename)
            if rel.is_absolute() or ".." in rel.parts:
                errors.append(f"{where}: local_file must be a safe relative path")
                continue
            # Fetcher records repository-relative paths; also support a filename relative to --images-dir.
            path = rel if rel.is_file() else images_dir / rel.name
            if not path.is_file():
                errors.append(f"{where}: image file missing: {filename}")
                continue
            checked_images += 1
            folded = path.name.casefold()
            if folded in seen_files:
                errors.append(f"{where}: duplicate local filename {path.name!r}")
            seen_files.add(folded)
            actual_hash = sha256_file(path)
            if candidate.get("sha256") != actual_hash:
                errors.append(f"{where}: SHA-256 mismatch for {path.name}")
        else:
            warnings.append(f"{where}: candidate not downloaded; file/hash check skipped")

        if candidate.get("training_approved") is True:
            errors.append(f"{where}: candidate manifest must not self-approve training eligibility")
        if not candidate.get("file_page") or not candidate.get("license_short_name"):
            warnings.append(f"{where}: source page or licence metadata needs manual review")

        if annotations_dir is not None and isinstance(candidate_id, str):
            ann_path = annotations_dir / f"{candidate_id}.json"
            if ann_path.exists():
                checked_annotations += 1
                try:
                    payload = json.loads(ann_path.read_text(encoding="utf-8"))
                    if not isinstance(payload, dict) or payload.get("format") != "pui89-coconut-annotations-v1":
                        raise ValueError("unexpected annotation format")
                    imgs = payload.get("images")
                    if not isinstance(imgs, list) or not imgs:
                        raise ValueError("images must be a non-empty list")
                    local_names: set[str] = set()
                    for im_idx, item in enumerate(imgs):
                        if not isinstance(item, dict):
                            raise ValueError(f"images[{im_idx}] must be an object")
                        name = item.get("filename")
                        if not isinstance(name, str) or not name or Path(name).name != name or name in {".", ".."}:
                            raise ValueError(f"images[{im_idx}] filename must be a basename")
                        if name.casefold() in local_names:
                            raise ValueError(f"duplicate annotation filename {name!r}")
                        local_names.add(name.casefold())
                        width, height = item.get("width"), item.get("height")
                        if (not isinstance(width, (int, float)) or isinstance(width, bool)
                                or not math.isfinite(width) or width <= 0 or int(width) != width):
                            raise ValueError(f"{name}: invalid width")
                        if (not isinstance(height, (int, float)) or isinstance(height, bool)
                                or not math.isfinite(height) or height <= 0 or int(height) != height):
                            raise ValueError(f"{name}: invalid height")
                        boxes = item.get("boxes")
                        if not isinstance(boxes, list):
                            raise ValueError(f"{name}: boxes must be a list")
                        for b_idx, box in enumerate(boxes):
                            if not isinstance(box, dict):
                                raise ValueError(f"{name}: box {b_idx} must be an object")
                            vals = [box.get(k) for k in ("x", "y", "w", "h")]
                            if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) for v in vals):
                                raise ValueError(f"{name}: box {b_idx} has non-finite/non-numeric coordinates")
                            x, y, w, h = map(float, vals)
                            if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > 1.000001 or y + h > 1.000001:
                                raise ValueError(f"{name}: box {b_idx} is outside normalized bounds")
                            total_boxes += 1
                except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"{ann_path}: {exc}")

    return {
        "schema": "pui89-coconut-dataset-audit-v1",
        "passed_structural_checks": not errors,
        "candidates_in_manifest": len(candidates),
        "downloaded_images_checked": checked_images,
        "annotation_files_checked": checked_annotations,
        "annotation_boxes_checked": total_boxes,
        "training_approved_count": 0,
        "errors": errors,
        "warnings": warnings,
        "limitations": [
            "Structural checks do not inspect image pixels or confirm that boxes enclose real coconuts.",
            "Structural checks do not establish copyright/licence suitability or attribution compliance.",
            "Human visual review and independent QA remain mandatory; this tool never promotes data.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("data/candidate_images/source_manifest.json"))
    parser.add_argument("--images-dir", type=Path, default=Path("data/candidate_images"))
    parser.add_argument("--annotations-dir", type=Path, default=None,
                        help="Optional folder containing one <candidate_id>.json per candidate")
    parser.add_argument("--report", type=Path, default=Path("data/candidate_images/dataset_audit_report.json"))
    args = parser.parse_args()
    try:
        payload = json.loads(args.manifest.read_text(encoding="utf-8"))
        report = audit(payload, args.images_dir, args.annotations_dir)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Report written: {args.report}")
    return 0 if report["passed_structural_checks"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
