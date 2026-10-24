#!/usr/bin/env python3
"""Optional, local-only Hugging Face zero-shot object-detection experiment.

This script is an exploratory demo. It does not train a model or validate system safety.
It never uploads the input image to a hosted inference API.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEFAULT_LABELS = [
    "coconut",
    "coconut bunch",
    "coconut palm"
]

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coconut Harvest AI: local Hugging Face vision demo")
    parser.add_argument("image", type=Path, help="Path to a local image file")
    parser.add_argument(
        "--label", action="append", dest="labels",
        help="Candidate text label; repeat to provide several. Defaults are project-specific.",
    )
    parser.add_argument(
        "--model", default="google/owlvit-base-patch32",
        help="Hugging Face model ID (model weights may download on first run).",
    )
    parser.add_argument("--threshold", type=float, default=0.20, help="Score threshold in [0, 1].")
    parser.add_argument(
        "--device", choices=("cpu", "cuda"), default="cpu",
        help="CPU is the safe default for limited VRAM; CUDA is opt-in.",
    )
    parser.add_argument("--json-out", type=Path, help="Optional path to save prediction JSON.")
    parser.add_argument("--annotated-image", type=Path, help="Optional path to save a preview image.")
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    if not args.image.is_file():
        print(f"Input image does not exist: {args.image}", file=sys.stderr)
        return 2
    if not 0.0 <= args.threshold <= 1.0:
        print("--threshold must be between 0 and 1.", file=sys.stderr)
        return 2
    labels = args.labels or DEFAULT_LABELS
    try:
        import torch
        from PIL import Image, ImageDraw
        from transformers import pipeline
    except ImportError as exc:
        print(
            "Missing optional dependency. Install a compatible local PyTorch, "
            "Transformers, and Pillow environment before running this experiment. "
            "No packages are installed automatically.",
            file=sys.stderr,
        )
        print(f"Import error: {exc}", file=sys.stderr)
        return 2

    if args.device == "cuda" and not torch.cuda.is_available():
        print("CUDA was requested but PyTorch cannot access a CUDA device.", file=sys.stderr)
        return 2

    try:
        with Image.open(args.image) as source:
            image = source.convert("RGB")
        detector = pipeline(
            task="zero-shot-object-detection",
            model=args.model,
            device=0 if args.device == "cuda" else -1,
        )
        raw = detector(image, candidate_labels=labels, threshold=args.threshold)
    except Exception as exc:  # report model, image, memory, and version errors without hiding them
        print(f"Vision experiment failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    predictions = []
    for item in raw:
        box = item.get("box", {})
        predictions.append({
            "label": str(item.get("label", "")),
            "score": float(item.get("score", 0.0)),
            "box_xyxy": {
                key: int(round(float(box[key])))
                for key in ("xmin", "ymin", "xmax", "ymax")
                if key in box
            },
        })

    report = {
        "project": "Coconut Harvest AI",
        "task": "zero-shot-object-detection",
        "model": args.model,
        "input_image": str(args.image),
        "device": args.device,
        "threshold": args.threshold,
        "candidate_labels": labels,
        "predictions": predictions,
        "status": "exploratory; not independently validated",
        "limitations": "A pretrained open-vocabulary model may miss coconuts or draw incorrect boxes, especially for small, overlapping, occluded or distant fruit. Outputs are not training labels and do not change the dataset approval gate. Do not use detections to command a cutter or robot arm."
    }
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    if args.annotated_image:
        with Image.open(args.image) as source:
            preview = source.convert("RGB")
        draw = ImageDraw.Draw(preview)
        for pred in predictions:
            box = pred["box_xyxy"]
            if len(box) == 4:
                coords = (box["xmin"], box["ymin"], box["xmax"], box["ymax"])
                draw.rectangle(coords, outline="red", width=3)
                draw.text((coords[0], max(0, coords[1] - 14)),
                          f'{pred["label"]} {pred["score"]:.2f}', fill="red")
        args.annotated_image.parent.mkdir(parents=True, exist_ok=True)
        preview.save(args.annotated_image)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
