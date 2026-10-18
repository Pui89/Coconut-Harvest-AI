"""Optional local-only adapter for a user-supplied coconut detector.

No model is downloaded automatically. Only load model files you trust.
This module never sends actuator commands or makes network requests itself.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any


def coconut_class_ids(names: Any) -> set[int]:
    """Return class IDs whose labels explicitly identify coconut(s)."""
    items = names.items() if isinstance(names, dict) else enumerate(names)
    result: set[int] = set()
    for class_id, label in items:
        normalized = str(label).strip().lower().replace("_", " ").replace("-", " ")
        if normalized in {"coconut", "coconuts"} or normalized.startswith("coconut "):
            result.add(int(class_id))
    return result


def load_local_coconut_model(model_path: str | Path) -> tuple[Any, set[int]]:
    """Load an existing local Ultralytics .pt file and require a coconut class.

    A missing path is rejected before importing Ultralytics, preventing an
    accidental fallback to an online model name or automatic model download.
    """
    path = Path(model_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(
            f"Local model file does not exist: {path}. Set PUI89_COCONUT_MODEL_PATH "
            "to an existing trusted local weights file."
        )
    if path.suffix.lower() != ".pt":
        raise ValueError("Only local .pt model files are supported by this adapter.")
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError(
            "Local detector support is optional. Install the detector extra with "
            "'python -m pip install -r apps/pui89_app/requirements-detector.txt'."
        ) from exc

    model = YOLO(str(path))
    class_ids = coconut_class_ids(model.names)
    if not class_ids:
        raise ValueError(
            "The supplied model's class labels do not include 'coconut'. "
            "A generic pretrained model is not automatically a coconut detector."
        )
    return model, class_ids


def detect_coconuts(
    model: Any,
    image: Any,
    class_ids: set[int],
    *,
    confidence: float = 0.25,
    image_size: int = 640,
) -> list[dict[str, Any]]:
    """Run local inference and return coconut bounding boxes in pixel coordinates."""
    if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be finite and in [0, 1]")
    if image_size < 32 or image_size > 4096:
        raise ValueError("image_size must be between 32 and 4096 pixels")
    if not class_ids:
        raise ValueError("At least one verified coconut class ID is required")

    results = model.predict(
        source=image,
        conf=confidence,
        imgsz=image_size,
        device="cpu",
        verbose=False,
    )
    detections: list[dict[str, Any]] = []
    if not results:
        return detections
    result = results[0]
    boxes = getattr(result, "boxes", None)
    if boxes is None:
        return detections

    xyxy = boxes.xyxy.detach().cpu().tolist()
    scores = boxes.conf.detach().cpu().tolist()
    classes = boxes.cls.detach().cpu().tolist()
    names = getattr(result, "names", getattr(model, "names", {}))
    for coordinates, score, raw_class_id in zip(xyxy, scores, classes):
        class_id = int(raw_class_id)
        if class_id not in class_ids:
            continue
        if len(coordinates) != 4 or not all(math.isfinite(float(v)) for v in coordinates):
            continue
        x1, y1, x2, y2 = (float(value) for value in coordinates)
        if x2 <= x1 or y2 <= y1 or not math.isfinite(float(score)):
            continue
        label = names.get(class_id, str(class_id)) if isinstance(names, dict) else names[class_id]
        detections.append({
            "class_id": class_id,
            "class_name": str(label),
            "confidence": float(score),
            "bbox_xyxy_pixels": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)],
        })
    return detections
