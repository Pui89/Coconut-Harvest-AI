"""Train an Ultralytics detector from an existing local checkpoint and dataset.

The script refuses model names/URLs: --model must be a local .pt file. It never
downloads a base model or dataset. Training artifacts are written locally.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def _image_paths_for_split(path: Path) -> list[Path]:
    """Return image files referenced by a split directory, image, or YOLO list file."""
    if path.is_dir():
        return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)
    if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
        return [path]
    if path.is_file() and path.suffix.lower() == ".txt":
        image_paths: list[Path] = []
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            entry = raw_line.strip()
            if not entry or entry.startswith("#"):
                continue
            candidate = Path(entry).expanduser()
            if not candidate.is_absolute():
                candidate = path.parent / candidate
            candidate = candidate.resolve()
            if candidate.suffix.lower() not in IMAGE_SUFFIXES or not candidate.is_file():
                raise ValueError(f"Dataset list references a missing or unsupported image: {entry}")
            image_paths.append(candidate)
        return image_paths
    return []


def validate_dataset_yaml(data_yaml: Path, require_test: bool = False) -> dict[str, Any]:
    """Validate the YAML structure, coconut class, split paths, and non-empty image splits."""
    if not data_yaml.is_file():
        raise FileNotFoundError(f"Dataset YAML not found: {data_yaml}")
    try:
        config = yaml.safe_load(data_yaml.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Dataset YAML is invalid: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError("Dataset YAML must contain a mapping.")
    names = config.get("names")
    if isinstance(names, dict):
        class_names = [str(v).strip().lower() for _, v in sorted(names.items(), key=lambda pair: str(pair[0]))]
        try:
            class_ids = sorted(int(k) for k in names)
        except (TypeError, ValueError) as exc:
            raise ValueError("Dataset class mapping keys must be integer IDs.") from exc
        if class_ids != list(range(len(class_ids))):
            raise ValueError("Dataset class IDs must be contiguous from zero.")
    elif isinstance(names, list):
        class_names = [str(v).strip().lower() for v in names]
    else:
        raise ValueError("Dataset YAML must define names as a list or mapping.")
    if not class_names or not any(n in {"coconut", "coconuts"} for n in class_names):
        raise ValueError("Dataset classes must include an explicit coconut class.")
    configured_root = config.get("path", ".")
    if not isinstance(configured_root, str) or not configured_root.strip():
        raise ValueError("Dataset path must be a non-empty string when provided.")
    root = Path(configured_root).expanduser()
    if not root.is_absolute():
        root = (data_yaml.parent / root).resolve()
    splits = ("train", "val", *(("test",) if require_test else ()))
    for split in splits:
        if split not in config:
            raise ValueError(f"Dataset YAML is missing required {split} split.")
        values = config[split] if isinstance(config[split], list) else [config[split]]
        if not values:
            raise ValueError(f"Dataset {split} split must not be empty.")
        image_count = 0
        for item in values:
            if not isinstance(item, str) or not item.strip():
                raise ValueError(f"Dataset {split} paths must be non-empty strings.")
            path = Path(item).expanduser()
            if not path.is_absolute():
                path = root / path
            if not path.exists():
                raise FileNotFoundError(f"Dataset {split} path does not exist: {path}")
            images = _image_paths_for_split(path)
            if not images:
                raise ValueError(f"Dataset {split} path contains no supported image files: {path}")
            image_count += len(images)
        if image_count == 0:
            raise ValueError(f"Dataset {split} split contains no supported images.")
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Existing trusted local .pt checkpoint.")
    parser.add_argument("--data", required=True, help="YOLO dataset YAML.")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=512, help="Start at 512 for a 4 GB GPU.")
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--device", default="0", help="0 for first CUDA GPU, or cpu.")
    parser.add_argument("--workers", type=int, default=0, help="Conservative default on Windows.")
    parser.add_argument("--project", default="runs/coconut")
    parser.add_argument("--name", default="train")
    args = parser.parse_args()
    model_path = Path(args.model).expanduser().resolve()
    data_yaml = Path(args.data).expanduser().resolve()
    if not model_path.is_file() or model_path.suffix.lower() != ".pt":
        raise FileNotFoundError("--model must be an existing local .pt file; model IDs and URLs are refused.")
    if args.epochs < 1 or not 128 <= args.imgsz <= 2048 or args.batch < 1 or args.workers < 0:
        raise ValueError("Invalid training settings.")
    validate_dataset_yaml(data_yaml)
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Install apps/pui89_app/requirements-detector.txt first.") from exc
    project = Path(args.project).expanduser()
    model = YOLO(str(model_path))
    results = model.train(
        data=str(data_yaml), epochs=args.epochs, imgsz=args.imgsz,
        batch=args.batch, device=args.device, workers=args.workers,
        project=str(project), name=args.name, exist_ok=False,
        pretrained=True, cache=False, plots=True, verbose=True,
    )
    save_dir = Path(getattr(results, "save_dir", project / args.name)).resolve()
    best = save_dir / "weights" / "best.pt"
    summary = {
        "status": "TRAINING_FINISHED",
        "model_initial_checkpoint": str(model_path),
        "dataset_yaml": str(data_yaml),
        "save_dir": str(save_dir),
        "best_weights": str(best) if best.is_file() else None,
        "best_weights_exists": best.is_file(),
        "epochs_requested": args.epochs,
        "imgsz": args.imgsz, "batch": args.batch, "device": args.device,
        "warning": "Training completion is not evidence of accuracy. Evaluate on a frozen, labelled test split.",
    }
    (save_dir / "training_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
