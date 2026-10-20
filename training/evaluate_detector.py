"""Evaluate a trained local coconut detector on the frozen YOLO test split."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def _test_images_for_path(path: Path, dataset_root: Path) -> list[Path]:
    """Resolve a test split directory, image, or YOLO image-list file."""
    if path.is_dir():
        return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)
    if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
        return [path]
    if path.is_file() and path.suffix.lower() == ".txt":
        images: list[Path] = []
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            entry = raw_line.strip()
            if not entry or entry.startswith("#"):
                continue
            candidate = Path(entry).expanduser()
            if not candidate.is_absolute():
                rooted = (dataset_root / candidate).resolve()
                relative_to_list = (path.parent / candidate).resolve()
                candidate = rooted if rooted.is_file() else relative_to_list
            else:
                candidate = candidate.resolve()
            if candidate.suffix.lower() not in IMAGE_SUFFIXES or not candidate.is_file():
                raise ValueError(f"Test list references a missing or unsupported image: {entry}")
            images.append(candidate)
        return images
    return []


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def validate_test_split(data_yaml: Path) -> dict[str, Any]:
    if not data_yaml.is_file():
        raise FileNotFoundError(f"Dataset YAML not found: {data_yaml}")
    config = yaml.safe_load(data_yaml.read_text(encoding="utf-8"))
    if not isinstance(config, dict) or "test" not in config:
        raise ValueError("Dataset YAML must define a held-out test split.")
    names = config.get("names")
    values = names.values() if isinstance(names, dict) else names if isinstance(names, list) else []
    if not any(str(v).strip().lower() in {"coconut", "coconuts"} for v in values):
        raise ValueError("Dataset classes must include an explicit coconut class.")
    root = Path(config.get("path", ".")).expanduser()
    if not root.is_absolute():
        root = (data_yaml.parent / root).resolve()
    configured_test = config["test"]
    splits = configured_test if isinstance(configured_test, list) else [configured_test]
    if not splits:
        raise ValueError("Dataset test split must not be empty.")
    image_count = 0
    for item in splits:
        if not isinstance(item, str) or not item.strip():
            raise ValueError("Dataset test paths must be non-empty strings.")
        path = Path(item).expanduser()
        if not path.is_absolute():
            path = root / path
        if not path.exists():
            raise FileNotFoundError(f"Test split path does not exist: {path}")
        images = _test_images_for_path(path, root)
        if not images:
            raise ValueError(f"Test split path contains no supported image files: {path}")
        image_count += len(images)
    if image_count == 0:
        raise ValueError("Held-out test split contains no supported images.")
    return config

def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if hasattr(value, "item"):
        try:
            return json_safe(value.item())
        except (ValueError, TypeError):
            pass
    if isinstance(value, float) and (value != value or value in (float("inf"), float("-inf"))):
        return None
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weights", required=True, help="Existing local trained .pt checkpoint.")
    parser.add_argument("--data", required=True, help="Dataset YAML with a held-out test split.")
    parser.add_argument("--output", default="reports/coconut_test_report.json")
    parser.add_argument("--imgsz", type=int, default=512)
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--device", default="0", help="0 for CUDA or cpu.")
    args = parser.parse_args()
    weights = Path(args.weights).expanduser().resolve()
    data_yaml = Path(args.data).expanduser().resolve()
    if not weights.is_file() or weights.suffix.lower() != ".pt":
        raise FileNotFoundError("--weights must point to an existing local .pt file.")
    if args.imgsz < 128 or args.batch < 1:
        raise ValueError("imgsz must be >=128 and batch must be >=1.")
    validate_test_split(data_yaml)
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise RuntimeError("Install apps/pui89_app/requirements-detector.txt first.") from exc
    model = YOLO(str(weights))
    names = getattr(model, "names", {})
    labels = list(names.values()) if isinstance(names, dict) else list(names)
    if not any(str(label).strip().lower() in {"coconut", "coconuts"} for label in labels):
        raise ValueError("The supplied checkpoint has no explicit coconut class.")
    metrics = model.val(
        data=str(data_yaml), split="test", imgsz=args.imgsz, batch=args.batch,
        device=args.device, plots=True, save_json=True,
        project=str(Path(args.output).expanduser().resolve().parent),
        name="ultralytics_test_artifacts", exist_ok=True, verbose=True,
    )
    values = json_safe(getattr(metrics, "results_dict", {}))
    report_path = Path(args.output).expanduser().resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "TEST_EVALUATION_FINISHED",
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "weights": str(weights), "weights_sha256": sha256_file(weights),
        "dataset_yaml": str(data_yaml), "dataset_yaml_sha256": sha256_file(data_yaml),
        "split": "test", "imgsz": args.imgsz, "batch": args.batch, "device": args.device,
        "class_names": labels, "metrics": values,
        "artifacts_dir": str(getattr(metrics, "save_dir", "")),
        "interpretation": "Metrics apply only to this dataset and split. They do not establish performance on independent farms, cameras, seasons, or robot safety.",
    }
    report_path.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path), "metrics": values}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
