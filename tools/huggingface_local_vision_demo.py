#!/usr/bin/env python3
"""Offline Hugging Face OWL-ViT inference; weights must already be cached locally."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any

MODEL_ID = "google/owlvit-base-patch32"
MODEL_REVISION = "cbc355fb364588351c5d51c7f74465e8e7ec6f72"
PROJECT = "Coconut-Harvest-AI"
DEFAULT_LABELS = ["coconut fruit","coconut bunch","coconut palm tree","person","ladder","harvesting tool"]
TASK_SCOPE = "Coconut and worker scene localization only; not maturity grading, harvest readiness, height measurement, or safe cutting."

def build_report(*, image_path: str, image_sha256: str, model_id: str,
                 revision: str, labels: list[str], threshold: float,
                 detections: list[dict[str, Any]]) -> dict[str, Any]:
    if not 0.0 <= float(threshold) <= 1.0:
        raise ValueError("threshold must be in [0, 1]")
    return {
        "schema_version": "1.0", "project": PROJECT,
        "task": "zero-shot-object-detection",
        "model": {"id": model_id, "revision": revision},
        "input": {"image_path": image_path, "sha256": image_sha256},
        "candidate_labels": list(labels), "threshold": float(threshold),
        "detections": list(detections),
        "status": "MODEL_INFERENCE_REVIEW_ONLY",
        "human_review_required": True, "actuator_authorized": False,
        "scope": TASK_SCOPE,
        "limitations": [
            "Open-vocabulary detections can be wrong, incomplete, or overconfident.",
            "A missing detection is not evidence that an object or hazard is absent.",
            "Scores are not calibrated probabilities or validated project performance metrics.",
            "Never use alone for safety-critical, enforcement, rescue, or physical-control decisions."
        ]
    }

def parse_args():
    p = argparse.ArgumentParser(description=f"{PROJECT}: local-only Hugging Face OWL-ViT")
    p.add_argument("image", type=Path)
    p.add_argument("--label", action="append", dest="labels")
    p.add_argument("--model", default=MODEL_ID)
    p.add_argument("--revision", default=MODEL_REVISION)
    p.add_argument("--threshold", type=float, default=0.20)
    p.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    p.add_argument("--json-out", type=Path)
    return p.parse_args()

def main() -> int:
    args = parse_args()
    if not args.image.is_file() or not 0.0 <= args.threshold <= 1.0:
        print("Provide an existing image and a threshold in [0, 1].", file=sys.stderr)
        return 2
    labels = args.labels or DEFAULT_LABELS
    if not labels or any(not isinstance(x, str) or not x.strip() for x in labels):
        print("Candidate labels must be non-empty strings.", file=sys.stderr)
        return 2
    try:
        import torch
        from PIL import Image
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
    except ImportError as exc:
        print(f"Optional PyTorch/Transformers/Pillow dependency missing: {exc}", file=sys.stderr)
        print("Install nothing automatically; review versions and cost before manual setup.", file=sys.stderr)
        return 2
    if args.device == "cuda" and not torch.cuda.is_available():
        print("CUDA requested but unavailable.", file=sys.stderr)
        return 2
    try:
        processor = AutoProcessor.from_pretrained(
            args.model, revision=args.revision, local_files_only=True, trust_remote_code=False
        )
        model = AutoModelForZeroShotObjectDetection.from_pretrained(
            args.model, revision=args.revision, local_files_only=True,
            use_safetensors=True, trust_remote_code=False
        ).to(args.device).eval()
        with Image.open(args.image) as src:
            image = src.convert("RGB")
        inputs = processor(text=[labels], images=image, return_tensors="pt")
        inputs = {k: v.to(args.device) for k, v in inputs.items()}
        with torch.inference_mode():
            outputs = model(**inputs)
        sizes = torch.tensor([[image.height, image.width]], device=args.device)
        result = processor.post_process_object_detection(
            outputs=outputs, target_sizes=sizes, threshold=args.threshold
        )[0]
        detections = []
        for box, score, label_id in zip(result["boxes"], result["scores"], result["labels"]):
            detections.append({
                "label": labels[int(label_id)],
                "score": round(float(score.detach().cpu().item()), 6),
                "box_xyxy": [round(float(v), 2) for v in box.detach().cpu().tolist()]
            })
        digest = hashlib.sha256(args.image.read_bytes()).hexdigest()
        report = build_report(
            image_path=str(args.image), image_sha256=digest, model_id=args.model,
            revision=args.revision, labels=labels, threshold=args.threshold,
            detections=detections
        )
    except Exception as exc:
        print(f"Offline model inference failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("No download was attempted. Check local cache, revision, package compatibility, and RAM.", file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
