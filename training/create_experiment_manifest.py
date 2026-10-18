"""Create a local experiment manifest without downloading data or models.

The manifest records provenance/configuration; it does not run evaluation or claim results.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], check=True, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def resolve_path(value: str, base: Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def split_paths(config: dict[str, Any], key: str, yaml_dir: Path) -> list[Path]:
    root_value = config.get("path", ".")
    root = resolve_path(str(root_value), yaml_dir)
    values = config.get(key)
    if values is None:
        return []
    values = values if isinstance(values, list) else [values]
    paths = []
    for value in values:
        p = Path(str(value)).expanduser()
        paths.append(p.resolve() if p.is_absolute() else (root / p).resolve())
    return paths


def count_images(paths: list[Path]) -> int | None:
    total = 0
    for path in paths:
        if not path.exists():
            return None
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            total += 1
        elif path.is_file() and path.suffix.lower() == ".txt":
            # YOLO split lists contain one image path per line.
            for line in path.read_text(encoding="utf-8").splitlines():
                value = line.strip()
                if not value or value.startswith("#"):
                    continue
                listed = Path(value).expanduser()
                if not listed.is_absolute():
                    listed = (path.parent / listed).resolve()
                if listed.is_file() and listed.suffix.lower() in IMAGE_SUFFIXES:
                    total += 1
        elif path.is_dir():
            total += sum(
                1 for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in IMAGE_SUFFIXES
            )
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, help="Dataset YAML used for training/evaluation.")
    parser.add_argument("--weights", help="Optional local .pt checkpoint to checksum.")
    parser.add_argument("--output", default="reports/experiment_manifest.json")
    parser.add_argument("--experiment-id", default="coconut-experiment")
    parser.add_argument("--seed", type=int, help="Seed used by the run, if explicitly set.")
    parser.add_argument("--notes", default="", help="Short notes on protocol or known caveats.")
    args = parser.parse_args()

    data_yaml = Path(args.data).expanduser().resolve()
    if not data_yaml.is_file():
        parser.error(f"Dataset YAML not found: {data_yaml}")
    config = yaml.safe_load(data_yaml.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        parser.error("Dataset YAML must contain a YAML mapping.")
    names = config.get("names", {})
    class_names = list(names.values()) if isinstance(names, dict) else list(names) if isinstance(names, list) else []

    split_info = {}
    for split in ("train", "val", "test"):
        paths = split_paths(config, split, data_yaml.parent)
        split_info[split] = {
            "configured_paths": [str(p) for p in paths],
            "path_exists": all(p.exists() for p in paths) if paths else False,
            "image_count": count_images(paths) if paths else None,
        }

    weights_info = None
    if args.weights:
        weights = Path(args.weights).expanduser().resolve()
        if not weights.is_file():
            parser.error(f"Checkpoint not found: {weights}")
        weights_info = {
            "path": str(weights),
            "size_bytes": weights.stat().st_size,
            "sha256": sha256_file(weights),
        }

    torch_info: dict[str, Any] = {"installed": package_version("torch") is not None}
    if torch_info["installed"]:
        try:
            import torch
            torch_info.update({
                "version": torch.__version__,
                "cuda_available": torch.cuda.is_available(),
                "cuda_version": torch.version.cuda,
                "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            })
        except Exception as exc:
            torch_info["inspection_error"] = type(exc).__name__

    manifest = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "MANIFEST_ONLY_NO_EXPERIMENT_RUN",
        "git": {
            "commit": git_value("rev-parse", "HEAD"),
            "branch": git_value("branch", "--show-current"),
            "working_tree": "clean" if git_value("status", "--porcelain") == "" else "modified_or_unknown",
        },
        "environment": {
            "python": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "packages": {
                name: package_version(name)
                for name in ("ultralytics", "torch", "torchvision", "PyYAML", "Pillow", "numpy")
            },
            "torch": torch_info,
        },
        "dataset": {
            "yaml_path": str(data_yaml),
            "yaml_sha256": sha256_file(data_yaml),
            "class_names": class_names,
            "splits": split_info,
        },
        "weights": weights_info,
        "requested_seed": args.seed,
        "notes": args.notes,
        "warning": (
            "This manifest records configuration and file provenance only. "
            "It does not validate labels, prove licence rights, run training/evaluation, "
            "or establish model performance."
        ),
    }
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(output), "status": manifest["status"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
