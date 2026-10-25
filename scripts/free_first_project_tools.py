"""Free-first, offline, standard-library project validation tools.

No network, model download, paid API, telemetry, or hardware control.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable, Mapping


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json_report(path: str | Path, payload: Mapping[str, Any]) -> None:
    """Write deterministic, human-readable JSON locally; never uploads the report."""
    Path(path).write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def finite_unit_interval(value: Any) -> bool:
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and math.isfinite(value)
        and 0.0 <= value <= 1.0
    )


def required_nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_annotation(record: Mapping[str, Any]) -> list[str]:
    """Validate a normalized xyxy box and minimum source provenance fields."""
    errors = []
    for key in ("image_path", "source_id", "licence", "sha256"):
        if not required_nonempty_text(record.get(key)):
            errors.append(f"{key} must be supplied and non-empty")
    digest = record.get("sha256")
    if required_nonempty_text(digest) and (len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest.lower())):
        errors.append("sha256 must be a 64-character hexadecimal digest")
    box = record.get("bbox_xyxy")
    if not isinstance(box, (list, tuple)) or len(box) != 4:
        errors.append("bbox_xyxy must contain four normalized coordinates")
    else:
        x1, y1, x2, y2 = box
        if not all(finite_unit_interval(v) for v in box):
            errors.append("bbox coordinates must be finite numbers in [0, 1]")
        elif not (x1 < x2 and y1 < y2):
            errors.append("bbox must have positive width and height")
    if not required_nonempty_text(record.get("maturity_class")):
        errors.append("maturity_class must be supplied")
    return errors


def audit_records(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Summarize manifest/annotation quality without opening images or training."""
    rows = list(records)
    errors = []
    seen_hashes: dict[str, int] = {}
    for index, row in enumerate(rows):
        for issue in validate_annotation(row):
            errors.append({"row": index, "issue": issue})
        digest = row.get("sha256")
        if digest is not None:
            if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest.lower()):
                errors.append({"row": index, "issue": "sha256 must be a 64-character hexadecimal digest"})
            elif digest.lower() in seen_hashes:
                errors.append({"row": index, "issue": f"duplicate content hash matches row {seen_hashes[digest.lower()]}"})
            else:
                seen_hashes[digest.lower()] = index
    return {
        "record_count": len(rows),
        "valid_record_count": len(rows) - len({e["row"] for e in errors}),
        "error_count": len(errors),
        "training_approved": bool(rows) and not errors,
        "errors": errors,
        "note": "Manifest checks do not establish image rights, label correctness, or model performance; review those independently.",
    }


def binary_classification_metrics(y_true: Iterable[int | bool], y_pred: Iterable[int | bool]) -> dict[str, float | int]:
    """Compute reproducible binary metrics without third-party dependencies.

    Inputs must be equal-length, non-empty sequences containing only 0/1 or bool.
    This reports metrics; it does not certify a model or set a deployment threshold.
    """
    truth, predicted = list(y_true), list(y_pred)
    if not truth or len(truth) != len(predicted):
        raise ValueError("y_true and y_pred must be non-empty and have equal lengths")
    if any(not isinstance(v, bool) and (not isinstance(v, int) or v not in (0, 1)) for v in truth + predicted):
        raise ValueError("labels must contain only integer 0/1 values or booleans")
    truth = [int(v) for v in truth]
    predicted = [int(v) for v in predicted]
    tp = sum(t == 1 and p == 1 for t, p in zip(truth, predicted))
    tn = sum(t == 0 and p == 0 for t, p in zip(truth, predicted))
    fp = sum(t == 0 and p == 1 for t, p in zip(truth, predicted))
    fn = sum(t == 1 and p == 0 for t, p in zip(truth, predicted))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "sample_count": len(truth), "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "accuracy": (tp + tn) / len(truth), "precision": precision,
        "recall": recall, "f1": f1,
    }
