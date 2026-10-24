#!/usr/bin/env python3
"""Run an optional, local SAM 3 text-prompt segmentation smoke test.

This script downloads model files only when you run it. It never downloads images.
The SAM 3 repository may require Hugging Face access approval and license acceptance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, type=Path, help="Path to a local image file.")
    parser.add_argument("--prompt", required=True, help="Text prompt describing the object to segment.")
    parser.add_argument("--model-id", default="facebook/sam3-base", help="Hugging Face model ID.")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/sam3-smoke-test"))
    parser.add_argument("--score-threshold", type=float, default=0.30)
    parser.add_argument("--mask-threshold", type=float, default=0.50)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.image.is_file():
        raise SystemExit(f"Image file does not exist: {args.image}")
    if not args.prompt.strip():
        raise SystemExit("--prompt must not be empty")
    if not 0.0 <= args.score_threshold <= 1.0:
        raise SystemExit("--score-threshold must be between 0 and 1")
    if not 0.0 <= args.mask_threshold <= 1.0:
        raise SystemExit("--mask-threshold must be between 0 and 1")

    try:
        import torch
        from PIL import Image
        from transformers import AutoModel, AutoProcessor
    except ImportError as exc:
        raise SystemExit(
            "Missing optional dependencies. Install compatible torch, transformers, and Pillow "
            "versions in a virtual environment; see docs/SEGMENTATION_SMOKE_TEST.md."
        ) from exc

    image = Image.open(args.image).convert("RGB")
    processor = AutoProcessor.from_pretrained(args.model_id)
    model = AutoModel.from_pretrained(args.model_id)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    inputs = processor(images=image, text=args.prompt, return_tensors="pt")
    inputs = {key: value.to(device) if hasattr(value, "to") else value for key, value in inputs.items()}
    with torch.inference_mode():
        outputs = model(**inputs)

    results = processor.post_process_instance_segmentation(
        outputs,
        threshold=args.score_threshold,
        mask_threshold=args.mask_threshold,
        target_sizes=[image.size[::-1]],
    )
    result = results[0]
    masks = result["masks"].detach().cpu()
    scores = result["scores"].detach().cpu().tolist()
    boxes = result["boxes"].detach().cpu().tolist()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    mask_dir = args.output_dir / "masks"
    mask_dir.mkdir(parents=True, exist_ok=True)
    for index, mask in enumerate(masks):
        pixels = (mask.squeeze().numpy().astype("uint8") * 255)
        Image.fromarray(pixels, mode="L").save(mask_dir / f"mask_{index:03d}.png")

    summary = {
        "model_id": args.model_id,
        "image": str(args.image),
        "image_width": image.width,
        "image_height": image.height,
        "prompt": args.prompt,
        "device": device,
        "score_threshold": args.score_threshold,
        "mask_threshold": args.mask_threshold,
        "instance_count": len(scores),
        "scores": scores,
        "boxes_xyxy": boxes,
        "mask_files": [str(mask_dir / f"mask_{index:03d}.png") for index in range(len(scores))],
        "warning": "Smoke test only; not a validated project benchmark or safety certification.",
    }
    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(f"\nSaved summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
