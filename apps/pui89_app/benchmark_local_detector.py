"""Benchmark a trusted local coconut detector at several input sizes.

Example (from the repository root):
    python -m apps.pui89_app.benchmark_local_detector \
        --model "C:/models/coconut.pt" --image "data/sample.jpg" --device auto

No weights are downloaded and no image is uploaded. Timing excludes model loading,
but includes the detector adapter and result post-processing. Use the same labelled
images and settings when comparing accuracy; latency alone is not a quality metric.
"""
from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from PIL import Image

from apps.pui89_app.local_detector import (
    detect_coconuts,
    load_local_coconut_model,
    resolve_inference_device,
)


def _sync_if_cuda(device: str) -> None:
    if device == "0":
        import torch

        torch.cuda.synchronize()


def benchmark(model_path: str, image_path: str, device: str, sizes: list[int],
              warmup: int, repeats: int, confidence: float) -> dict:
    image_file = Path(image_path).expanduser()
    if not image_file.is_file():
        raise FileNotFoundError(f"Image file not found: {image_file}")

    model, coconut_ids = load_local_coconut_model(model_path)
    image = Image.open(image_file).convert("RGB")
    resolved_device = resolve_inference_device(device)
    rows = []

    for size in sizes:
        # Warm-up separately; do not include it in the recorded samples.
        for _ in range(warmup):
            detect_coconuts(model, image, coconut_ids, confidence=confidence,
                            image_size=size, device=device)
        _sync_if_cuda(resolved_device)

        samples = []
        detection_count = 0
        for _ in range(repeats):
            _sync_if_cuda(resolved_device)
            started = perf_counter()
            detections = detect_coconuts(
                model, image, coconut_ids, confidence=confidence,
                image_size=size, device=device,
            )
            _sync_if_cuda(resolved_device)
            samples.append(perf_counter() - started)
            detection_count = len(detections)

        ordered = sorted(samples)
        # Nearest-rank p95: the smallest sample at or above the 95th percentile.
        import math
        p95_index = min(len(ordered) - 1, max(0, math.ceil(0.95 * len(ordered)) - 1))
        rows.append({
            "image_size": size,
            "repeats": repeats,
            "warmup_runs": warmup,
            "median_seconds": round(statistics.median(samples), 6),
            "mean_seconds": round(statistics.mean(samples), 6),
            "p95_seconds": round(ordered[p95_index], 6),
            "last_run_detection_count": detection_count,
            "timing_scope": "adapter inference plus result post-processing; model load excluded",
        })

    return {
        "status": "BENCHMARK_COMPLETED",
        "model_file": Path(model_path).expanduser().name,
        "image_file": image_file.name,
        "image_width_pixels": image.width,
        "image_height_pixels": image.height,
        "device": "cuda:0" if resolved_device == "0" else "cpu",
        "confidence_threshold": confidence,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "results": rows,
        "limitations": [
            "Single-image latency is not detector accuracy or mAP.",
            "Detection counts are not ground-truth correctness measurements.",
            "Compare accuracy on labelled held-out images before choosing a resolution.",
            "Results depend on model, driver, software versions, thermals, and background load.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Path to an existing trusted coconut-trained .pt file")
    parser.add_argument("--image", required=True, help="Path to one local test image")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--sizes", type=int, nargs="+", default=[384, 512, 640])
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--confidence", type=float, default=0.25)
    parser.add_argument("--output", default="coconut_latency_benchmark.json")
    args = parser.parse_args()

    if args.warmup < 0 or args.repeats < 1:
        parser.error("--warmup must be >= 0 and --repeats must be >= 1")
    if not 0.0 <= args.confidence <= 1.0:
        parser.error("--confidence must be between 0 and 1")
    if not args.sizes or any(size < 32 or size > 4096 for size in args.sizes):
        parser.error("--sizes must contain values between 32 and 4096")
    report = benchmark(args.model, args.image, args.device, args.sizes,
                       args.warmup, args.repeats, args.confidence)
    output = Path(args.output).expanduser()
    output.write_text(json.dumps(report, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Saved report: {output.resolve()}")


if __name__ == "__main__":
    main()
