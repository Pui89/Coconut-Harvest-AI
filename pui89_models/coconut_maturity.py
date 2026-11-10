"""PUI89 CPU-first visual appearance classifier (research baseline, not harvest advice).

Uses colour-histogram features and multinomial logistic regression implemented
with the Python standard library. Image decoding requires Pillow at runtime;
the model trainer never installs packages or downloads weights.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable, Sequence

CLASSES = ("young", "mature_green", "yellow", "brown_aging")
MODEL_FORMAT = "pui89-coconut-appearance-model"
MODEL_VERSION = "0.1.0"
HIST_BINS = 8
FEATURE_COUNT = HIST_BINS * 3 + 6


def softmax(logits: Sequence[float]) -> list[float]:
    if not logits:
        raise ValueError("logits must not be empty")
    peak = max(logits)
    exps = [math.exp(max(-60.0, min(60.0, x - peak))) for x in logits]
    total = sum(exps)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("invalid softmax normalizer")
    return [x / total for x in exps]


def extract_rgb_features(image_path: str | Path) -> list[float]:
    """Extract compact global RGB features; this is not an object detector."""
    try:
        from PIL import Image, ImageStat
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is required to read images. No package was installed. "
            "Use an already-installed Pillow environment or stop."
        ) from exc
    path = Path(image_path)
    with Image.open(path) as source:
        image = source.convert("RGB")
        image.thumbnail((256, 256))
        pixels = list(image.getdata())
        if not pixels:
            raise ValueError(f"image has no pixels: {path}")
        features: list[float] = []
        for channel in range(3):
            counts = [0] * HIST_BINS
            for pixel in pixels:
                counts[min(HIST_BINS - 1, pixel[channel] * HIST_BINS // 256)] += 1
            features.extend(count / len(pixels) for count in counts)
        stats = ImageStat.Stat(image)
        features.extend(value / 255.0 for value in stats.mean)
        features.extend(value / 255.0 for value in stats.stddev)
    if len(features) != FEATURE_COUNT:
        raise ValueError("unexpected feature-vector length")
    return features


def _validate_features(features: Sequence[float]) -> list[float]:
    values = [float(value) for value in features]
    if len(values) != FEATURE_COUNT or not all(math.isfinite(v) for v in values):
        raise ValueError(f"expected {FEATURE_COUNT} finite features")
    return values


def train(
    samples: Iterable[tuple[Sequence[float], str]],
    *,
    epochs: int = 400,
    learning_rate: float = 0.15,
    l2: float = 0.001,
) -> dict:
    """Fit a deterministic multiclass logistic model from labelled feature rows."""
    rows = [(_validate_features(x), label) for x, label in samples]
    if not rows:
        raise ValueError("no training samples")
    unknown = sorted({label for _, label in rows} - set(CLASSES))
    if unknown:
        raise ValueError(f"unsupported labels: {unknown}")
    missing = sorted(set(CLASSES) - {label for _, label in rows})
    if missing:
        raise ValueError(f"training data missing classes: {missing}")
    if epochs < 1 or learning_rate <= 0 or l2 < 0:
        raise ValueError("invalid training hyperparameters")

    means = [sum(row[j] for row, _ in rows) / len(rows) for j in range(FEATURE_COUNT)]
    variances = [
        sum((row[j] - means[j]) ** 2 for row, _ in rows) / len(rows)
        for j in range(FEATURE_COUNT)
    ]
    scales = [math.sqrt(v) if v > 1e-12 else 1.0 for v in variances]
    normalized = [
        ([(row[j] - means[j]) / scales[j] for j in range(FEATURE_COUNT)], CLASSES.index(label))
        for row, label in rows
    ]
    weights = [[0.0] * FEATURE_COUNT for _ in CLASSES]
    biases = [0.0] * len(CLASSES)
    rate = learning_rate / len(rows)

    for _ in range(epochs):
        grad_w = [[0.0] * FEATURE_COUNT for _ in CLASSES]
        grad_b = [0.0] * len(CLASSES)
        for vector, target in normalized:
            probabilities = softmax([
                biases[c] + sum(weights[c][j] * vector[j] for j in range(FEATURE_COUNT))
                for c in range(len(CLASSES))
            ])
            for c, probability in enumerate(probabilities):
                error = probability - (1.0 if c == target else 0.0)
                grad_b[c] += error
                for j, value in enumerate(vector):
                    grad_w[c][j] += error * value
        for c in range(len(CLASSES)):
            biases[c] -= rate * grad_b[c]
            for j in range(FEATURE_COUNT):
                weights[c][j] -= rate * (grad_w[c][j] + l2 * weights[c][j])

    return {
        "format": MODEL_FORMAT,
        "version": MODEL_VERSION,
        "classes": list(CLASSES),
        "feature_spec": {"name": "global_rgb_histogram_mean_std", "histogram_bins_per_channel": HIST_BINS},
        "normalization": {"mean": means, "scale": scales},
        "weights": weights,
        "biases": biases,
        "training": {
            "sample_count": len(rows),
            "class_counts": {label: sum(1 for _, y in rows if y == label) for label in CLASSES},
            "epochs": epochs,
            "learning_rate": learning_rate,
            "l2": l2,
            "confidence_calibrated": False,
        },
        "limitations": [
            "global colour features only; no fruit localization or object detection",
            "appearance classes are not botanical maturity or harvest-readiness certification",
            "requires representative, rights-cleared, human-reviewed images",
            "raw probabilities are uncalibrated and must not authorize harvesting",
        ],
    }


def predict_features(model: dict, features: Sequence[float], *, min_confidence: float = 0.65, min_margin: float = 0.15) -> dict:
    if model.get("format") != MODEL_FORMAT or model.get("version") != MODEL_VERSION:
        raise ValueError("unsupported model format/version")
    if tuple(model.get("classes", ())) != CLASSES:
        raise ValueError("model class order mismatch")
    values = _validate_features(features)
    means = model["normalization"]["mean"]
    scales = model["normalization"]["scale"]
    weights = model["weights"]
    biases = model["biases"]
    if len(means) != FEATURE_COUNT or len(scales) != FEATURE_COUNT:
        raise ValueError("invalid normalization metadata")
    vector = [(values[j] - means[j]) / scales[j] for j in range(FEATURE_COUNT)]
    probabilities = softmax([
        biases[c] + sum(weights[c][j] * vector[j] for j in range(FEATURE_COUNT))
        for c in range(len(CLASSES))
    ])
    ranked = sorted(enumerate(probabilities), key=lambda item: item[1], reverse=True)
    confidence = ranked[0][1]
    margin = confidence - ranked[1][1]
    accepted = confidence >= min_confidence and margin >= min_margin
    return {
        "status": "CLASSIFIED_NEEDS_HUMAN_CONFIRMATION" if accepted else "UNCERTAIN_NEEDS_REVIEW",
        "visual_class": CLASSES[ranked[0][0]] if accepted else "uncertain",
        "top_candidate": CLASSES[ranked[0][0]],
        "confidence_uncalibrated": confidence,
        "top_two_margin": margin,
        "class_probabilities_uncalibrated": {CLASSES[i]: probabilities[i] for i in range(len(CLASSES))},
        "human_review_required": True,
        "harvest_authorized": False,
        "model_version": MODEL_VERSION,
    }


def save_model(model: dict, path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_model(path: str | Path) -> dict:
    model = json.loads(Path(path).read_text(encoding="utf-8"))
    if model.get("format") != MODEL_FORMAT or model.get("version") != MODEL_VERSION:
        raise ValueError("unsupported model format/version")
    return model
