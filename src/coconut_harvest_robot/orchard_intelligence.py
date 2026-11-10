"""Evidence-first orchard perception records for Coconut Harvest AI.

This module consumes human annotations or upstream detector outputs. It does not
inspect image pixels, train/run a model, infer height from perspective, or control
robot hardware. Unknown or unverified measurements remain unknown.
"""
from __future__ import annotations

from collections import Counter
import math
from typing import Any, Mapping

MATURITY_CLASSES = frozenset({
    "young_green", "mature_green", "brown_aging", "uncertain"
})
HEIGHT_BANDS = (
    (0.0, 5.0, "H1_0_5m"),
    (5.0, 10.0, "H2_over5_10m"),
    (10.0, 15.0, "H3_over10_15m"),
    (15.0, 20.0, "H4_over15_20m"),
    (20.0, 25.0, "H5_over20_25m"),
    (25.0, 30.0, "H6_over25_30m"),
)
ALLOWED_HEIGHT_METHODS = frozenset({
    "field_tape", "laser_rangefinder", "survey_or_point_cloud",
    "published_measurement", "other"
})


def _finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def height_band(height_m: Any, *, status: str, method: str,
                evidence_ref: str | None) -> dict[str, Any]:
    """Assign a 0-30 m band only to a positive, verified, evidenced measurement."""
    result = {
        "height_m": None,
        "height_band": "UNKNOWN",
        "height_status": status if isinstance(status, str) else "invalid",
        "height_method": method if isinstance(method, str) else None,
        "evidence_ref": evidence_ref if isinstance(evidence_ref, str) else None,
    }
    if status != "verified":
        return result
    if (
        not isinstance(method, str)
        or method not in ALLOWED_HEIGHT_METHODS
        or not isinstance(evidence_ref, str)
        or not evidence_ref.strip()
    ):
        result["height_status"] = "review_required"
        return result
    if not _finite_number(height_m) or height_m < 0:
        result["height_status"] = "invalid_measurement"
        return result
    result["height_m"] = float(height_m)
    if height_m > 30:
        result["height_band"] = "OUT_OF_RANGE"
    else:
        for lower, upper, label in HEIGHT_BANDS:
            if (height_m >= lower if lower == 0 else height_m > lower) and height_m <= upper:
                result["height_band"] = label
                break
    return result


def validate_fruit_observation(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a single-fruit annotation/prediction without claiming vision inference."""
    if not isinstance(record, Mapping):
        raise TypeError("fruit observation must be a mapping")
    errors: list[str] = []
    fruit_id = record.get("fruit_id")
    image_id = record.get("image_id")
    maturity = record.get("maturity_class")
    source_kind = record.get("source_kind")
    confidence = record.get("class_confidence")
    bbox = record.get("bbox_xyxy_normalized")

    if not isinstance(fruit_id, str) or not fruit_id.strip():
        errors.append("missing_fruit_id")
    if not isinstance(image_id, str) or not image_id.strip():
        errors.append("missing_image_id")
    if not isinstance(maturity, str) or maturity not in MATURITY_CLASSES:
        errors.append("unsupported_or_missing_maturity_class")
    if not isinstance(source_kind, str) or source_kind not in {
        "human_annotation", "model_prediction", "synthetic_test"
    }:
        errors.append("unsupported_source_kind")
    if not _finite_number(confidence) or not 0.0 <= confidence <= 1.0:
        errors.append("invalid_class_confidence")
    if (
        not isinstance(bbox, (list, tuple)) or len(bbox) != 4
        or not all(_finite_number(v) for v in bbox)
        or not (0 <= bbox[0] < bbox[2] <= 1)
        or not (0 <= bbox[1] < bbox[3] <= 1)
    ):
        errors.append("invalid_normalized_bbox")

    review = record.get("review_status", "pending")
    if not isinstance(review, str) or review not in {"pending", "reviewed", "rejected"}:
        errors.append("invalid_review_status")
    if source_kind == "model_prediction" and review != "reviewed":
        disposition = "human_review_required"
    elif source_kind == "synthetic_test":
        disposition = "synthetic_only"
    elif review == "rejected":
        disposition = "rejected"
    elif errors:
        disposition = "invalid_record"
    else:
        disposition = "annotation_reviewed_not_ground_truth"

    # This engine never promotes a fruit to an automatic harvest target.
    return {
        "fruit_id": fruit_id if isinstance(fruit_id, str) else None,
        "image_id": image_id if isinstance(image_id, str) else None,
        "maturity_class": maturity if isinstance(maturity, str) and maturity in MATURITY_CLASSES else "unknown",
        "source_kind": source_kind if isinstance(source_kind, str) else "unknown",
        "class_confidence": float(confidence) if _finite_number(confidence) else None,
        "bbox_xyxy_normalized": list(bbox) if isinstance(bbox, (list, tuple)) else None,
        "review_status": review if isinstance(review, str) else "invalid",
        "disposition": disposition,
        "errors": errors,
        "harvest_authorized": False,
    }


def build_orchard_report(*, tree_record: Mapping[str, Any],
                         fruit_records: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Combine verified tree-height metadata with per-fruit evidence records."""
    if not isinstance(tree_record, Mapping):
        raise TypeError("tree_record must be a mapping")
    if not isinstance(fruit_records, list):
        raise TypeError("fruit_records must be a list")
    tree = height_band(
        tree_record.get("height_m"),
        status=tree_record.get("height_status", "unverified"),
        method=tree_record.get("height_method", ""),
        evidence_ref=tree_record.get("height_evidence_ref"),
    )
    fruits = [validate_fruit_observation(item) for item in fruit_records]
    counts = Counter(item["maturity_class"] for item in fruits)
    return {
        "schema": "pui89-coconut-orchard-intelligence-v0.1",
        "tree": tree,
        "fruit_count": len(fruits),
        "maturity_counts": dict(sorted(counts.items())),
        "fruit_observations": fruits,
        "decision_boundary": {
            "image_classification_performed": False,
            "height_inferred_from_pixels": False,
            "automatic_harvest_authorized": False,
            "note": (
                "Consumes supplied annotations or model outputs only. "
                "Tree height requires a verified measurement and evidence reference. "
                "All harvest decisions remain subject to separate validated safety gates."
            ),
        },
    }
