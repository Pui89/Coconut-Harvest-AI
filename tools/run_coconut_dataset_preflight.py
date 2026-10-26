#!/usr/bin/env python3
"""Run a free, local-only Coconut Harvest AI dataset preflight.

This combines the existing geometry audit and fail-closed ledger promotion gate.
Optional candidate-0032 source fingerprint checking is read-only by default.
It never edits annotations or sets human-review/training approval flags.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audit_coconut_annotations import audit as audit_geometry
from coconut_dataset_promotion_gate import evaluate as evaluate_promotion
from record_coconut_source_hash import record_source_hash


def build_report(
    annotations: Path,
    rights_csv: Path,
    review_csv: Path,
    overlap_threshold: float = 0.15,
    candidate_0032_annotations: Path | None = None,
    image_0032: Path | None = None,
) -> dict[str, Any]:
    """Create a combined report without changing input files."""
    geometry = audit_geometry(annotations, overlap_threshold)
    promotion = evaluate_promotion(rights_csv, review_csv)

    source_check: dict[str, Any]
    if image_0032 is None and candidate_0032_annotations is None:
        source_check = {
            "status": "NOT_CHECKED",
            "reason": "Pass both --candidate-0032-annotations and --image-0032 to check source bytes.",
        }
    elif image_0032 is None or candidate_0032_annotations is None:
        source_check = {
            "status": "BLOCKED",
            "reason": "Both --candidate-0032-annotations and --image-0032 are required together.",
        }
    else:
        try:
            source_check = record_source_hash(
                candidate_0032_annotations,
                image_0032,
                rights_csv,
                write_source_sha256=False,
            )
            source_check["status"] = (
                "PASS" if source_check.get("source_identity_passed") else "BLOCKED"
            )
        except (OSError, ValueError) as exc:
            source_check = {"status": "BLOCKED", "reason": str(exc)}

    geometry_ok = geometry.get("geometry_error_count") == 0
    ledger_ready = promotion.get("ready_for_training") is True
    source_ok = source_check.get("status") == "PASS" if image_0032 is not None else None
    if not geometry_ok or not ledger_ready or source_check.get("status") == "BLOCKED":
        overall = "BLOCKED"
    elif source_ok is False:
        overall = "BLOCKED"
    elif source_ok is None:
        overall = "INCOMPLETE"
    else:
        overall = "PRECHECKS_PASS_HUMAN_REVIEW_STILL_REQUIRED"

    return {
        "format": "pui89-coconut-dataset-preflight-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "overall_status": overall,
        "scope": "Read-only checks. No labels, ledgers, approval flags, or source hashes are modified.",
        "geometry": {
            "status": "PASS" if geometry_ok else "BLOCKED",
            "image_count": geometry.get("image_count"),
            "box_count": geometry.get("box_count"),
            "geometry_error_count": geometry.get("geometry_error_count"),
            "human_visual_qa": "NOT_CHECKED_BY_AUTOMATION",
            "report": geometry,
        },
        "promotion_gate": {
            "status": "PASS" if ledger_ready else "BLOCKED",
            "candidate_count": promotion.get("candidate_count"),
            "eligible_count": promotion.get("eligible_count"),
            "blocked_count": promotion.get("blocked_count"),
            "top_blockers": promotion.get("top_blockers"),
            "errors": promotion.get("errors"),
        },
        "candidate_0032_source_fingerprint": source_check,
        "limitations": [
            "Geometry checks cannot confirm boxes align with fruit or detect missed fruit.",
            "Ledger checks validate recorded fields, not legal rights or actual human review.",
            "A source fingerprint pass is not label approval or permission to train.",
            "No model is trained and no detector accuracy or physical robot capability is measured.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", type=Path, required=True,
                        help="Annotation JSON file to geometry-audit")
    parser.add_argument("--rights-csv", type=Path, required=True,
                        help="Source-rights ledger CSV")
    parser.add_argument("--review-csv", type=Path, required=True,
                        help="Candidate visual-review ledger CSV")
    parser.add_argument("--output", type=Path, default=Path("coconut-preflight-report.json"),
                        help="Report destination (default: coconut-preflight-report.json)")
    parser.add_argument("--overlap-iou-warning", type=float, default=0.15,
                        help="Overlap warning threshold from 0 to 1 (default: 0.15)")
    parser.add_argument("--candidate-0032-annotations", type=Path,
                        help="Single-image candidate 0032 draft JSON for source fingerprint check")
    parser.add_argument("--image-0032", type=Path,
                        help="Exact local original image bytes for candidate 0032 (read-only)")
    args = parser.parse_args()

    if not 0 <= args.overlap_iou_warning <= 1:
        parser.error("--overlap-iou-warning must be between 0 and 1")
    if (args.image_0032 is None) != (args.candidate_0032_annotations is None):
        parser.error("--image-0032 and --candidate-0032-annotations must be supplied together")

    protected = {
        args.annotations.resolve(),
        args.rights_csv.resolve(),
        args.review_csv.resolve(),
    }
    if args.candidate_0032_annotations:
        protected.add(args.candidate_0032_annotations.resolve())
    if args.image_0032:
        protected.add(args.image_0032.resolve())
    if args.output.resolve() in protected:
        parser.error("--output must not overwrite any input file")

    try:
        report = build_report(
            args.annotations,
            args.rights_csv,
            args.review_csv,
            args.overlap_iou_warning,
            args.candidate_0032_annotations,
            args.image_0032,
        )
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"Preflight failed to run: {exc}", file=sys.stderr)
        return 2

    print(rendered, end="")
    return 0 if report["overall_status"] == "PRECHECKS_PASS_HUMAN_REVIEW_STILL_REQUIRED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
