"""Optional, fail-closed adapters for DINOv2 and Anomalib.

No weights are downloaded at import time. Model outputs are screening signals only:
they are not identity claims, and they never authorize robot motion.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
from typing import Any


@dataclass(frozen=True)
class ScreeningRecord:
    schema_version: str
    model_name: str
    status: str
    score: float | None
    evidence_id: str
    human_review_required: bool = True
    actuator_authorized: bool = False


def _finite_score(value: Any) -> float:
    """Convert a scalar-like score and reject NaN/Inf/out-of-range values."""
    if hasattr(value, "detach"):
        value = value.detach()
    if hasattr(value, "cpu"):
        value = value.cpu()
    if hasattr(value, "item"):
        value = value.item()
    score = float(value)
    if not math.isfinite(score) or not 0.0 <= score <= 1.0:
        raise ValueError("score must be finite and in [0, 1]")
    return score


def make_screening_record(model_name: str, score: Any | None, *, threshold: float = 0.5) -> ScreeningRecord:
    """Create a reproducible review record; never authorizes actuation."""
    if not model_name or not isinstance(model_name, str):
        raise ValueError("model_name must be a non-empty string")
    threshold = _finite_score(threshold)
    normalized = None if score is None else _finite_score(score)
    # Missing/invalid evidence abstains; threshold is only a triage threshold.
    status = "ABSTAIN" if normalized is None else ("REVIEW_FLAG" if normalized >= threshold else "REVIEW_CLEAR")
    payload = {
        "schema_version": "1.0",
        "model_name": model_name,
        "status": status,
        "score": normalized,
        "human_review_required": True,
        "actuator_authorized": False,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
    evidence_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return ScreeningRecord(**payload, evidence_id=evidence_id)


def verify_screening_record(record: ScreeningRecord | dict[str, Any]) -> bool:
    """Verify integrity and mandatory fail-safe fields. This is not a signature."""
    if isinstance(record, ScreeningRecord):
        data = asdict(record)
    elif isinstance(record, dict):
        data = dict(record)
    else:
        return False
    required = {"schema_version", "model_name", "status", "score", "evidence_id",
                "human_review_required", "actuator_authorized"}
    if not required.issubset(data):
        return False
    if data["schema_version"] != "1.0" or not isinstance(data["model_name"], str) or not data["model_name"]:
        return False
    if data["human_review_required"] is not True or data["actuator_authorized"] is not False:
        return False
    if data["status"] not in {"ABSTAIN", "REVIEW_FLAG", "REVIEW_CLEAR"}:
        return False
    score = data["score"]
    if score is not None:
        try:
            if not math.isfinite(float(score)) or not 0.0 <= float(score) <= 1.0:
                return False
        except (TypeError, ValueError):
            return False
    if (data["status"] == "ABSTAIN") != (score is None):
        return False
    payload = {k: data[k] for k in (
        "schema_version", "model_name", "status", "score",
        "human_review_required", "actuator_authorized"
    )}
    expected = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                                         allow_nan=False).encode("utf-8")).hexdigest()
    return data["evidence_id"] == expected


class DINOv2EmbeddingAdapter:
    """Thin wrapper around an explicitly supplied Hugging Face DINOv2 model/processor.

    Supply already-loaded objects to avoid implicit downloads. Embeddings are generic
    visual features, not substance classification or proof of object identity.
    """
    def __init__(self, model: Any, processor: Any):
        self.model = model
        self.processor = processor

    def encode(self, image: Any) -> Any:
        import torch  # optional dependency, imported only when used
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.inference_mode():
            outputs = self.model(**inputs)
        features = getattr(outputs, "pooler_output", None)
        if features is None:
            features = outputs.last_hidden_state[:, 0, :]
        if not torch.isfinite(features).all():
            raise ValueError("DINOv2 produced non-finite features")
        return features


class AnomalibScoreAdapter:
    """Normalize an Anomalib prediction into a scalar triage score.

    Pass a predictor compatible with the installed Anomalib version. Anomaly means
    distributional difference only; it does not imply danger or illegal contents.
    """
    def __init__(self, predictor: Any):
        self.predictor = predictor

    def score(self, image: Any) -> float:
        prediction = self.predictor.predict(image)
        candidates = ("pred_score", "anomaly_score", "score")
        for name in candidates:
            value = getattr(prediction, name, None)
            if value is not None:
                # Anomalib versions may return a one-item tensor/list.
                if hasattr(value, "numel") and value.numel() != 1:
                    value = value.max()
                elif isinstance(value, (list, tuple)):
                    if not value:
                        continue
                    value = max(value)
                return _finite_score(value)
        if isinstance(prediction, dict):
            for name in candidates:
                if name in prediction:
                    value = prediction[name]
                    if isinstance(value, (list, tuple)):
                        if not value:
                            continue
                        value = max(value)
                    return _finite_score(value)
        raise ValueError("Anomalib prediction did not expose a scalar anomaly score")
