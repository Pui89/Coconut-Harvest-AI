#!/usr/bin/env python3
"""Free-first, offline project audit using only the Python standard library.

Run from any project root:
    python tools/free_first_audit.py
    python tools/free_first_audit.py --json audit-report.json

This tool never accesses the network, installs packages, downloads model weights,
or changes project files unless --json is explicitly supplied.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", "dist", "build"}
DATA_DIR_NAMES = {"data", "dataset", "datasets", "samples", "sample_data"}
DATA_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".csv", ".jsonl"}
MODEL_EXTENSIONS = {".pt", ".pth", ".onnx", ".engine", ".safetensors", ".ckpt", ".bin"}
MAX_HASH_BYTES = 200 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def walk_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root (default: current directory)")
    parser.add_argument("--json", type=Path, help="optional path for a JSON report; otherwise print to stdout")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"project root is not a directory: {root}")

    files = sorted(walk_files(root))
    python_files = [p for p in files if p.suffix == ".py"]
    syntax_errors = []
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path.relative_to(root)))
        except (SyntaxError, UnicodeDecodeError) as exc:
            syntax_errors.append({"path": str(path.relative_to(root)), "error": str(exc)})

    data_files = []
    large_model_files = []
    for path in files:
        rel = path.relative_to(root)
        if path.suffix.lower() in MODEL_EXTENSIONS:
            large_model_files.append({"path": str(rel), "bytes": path.stat().st_size})
        if path.suffix.lower() in DATA_EXTENSIONS and any(part.lower() in DATA_DIR_NAMES for part in rel.parts[:-1]):
            size = path.stat().st_size
            item = {"path": str(rel), "bytes": size}
            if size <= MAX_HASH_BYTES:
                item["sha256"] = sha256_file(path)
            else:
                item["sha256"] = None
                item["hash_skipped_reason"] = f"file exceeds {MAX_HASH_BYTES} byte safety limit"
            data_files.append(item)

    readme = root / "README.md"
    readme_text = readme.read_text(encoding="utf-8", errors="replace") if readme.exists() else ""
    docs_candidates = [
        root / "DATASET_CARD.md",
        root / "data" / "README.md",
        root / "data" / "DATASET_MANIFEST.csv",
        root / "docs" / "DATASET_CARD.md",
        root / "docs" / "dataset_manifest.csv",
    ]
    dataset_docs = [str(p.relative_to(root)) for p in docs_candidates if p.exists()]
    report = {
        "audit_type": "offline_free_first_project_audit",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(root),
        "network_used": False,
        "dependencies_installed": False,
        "model_weights_downloaded": False,
        "files_scanned": len(files),
        "python_files_scanned": len(python_files),
        "python_syntax_errors": syntax_errors,
        "dataset_files_found": len(data_files),
        "dataset_file_inventory": data_files,
        "dataset_documentation_candidates_found": dataset_docs,
        "dataset_documentation_follow_up": (
            "Review source, licence/permission, attribution, and split-group metadata for every data item."
            if not dataset_docs else
            "Confirm the discovered manifest/card covers every data item and its licence/permission."
        ),
        "model_or_checkpoint_files_found": large_model_files,
        "readme_found": readme.exists(),
        "readme_mentions_metrics_or_evaluation": any(
            term in readme_text.lower() for term in ("precision", "recall", "mAP", "evaluation", "benchmark")
        ),
        "limitations": [
            "A clean syntax scan does not prove tests pass, model quality, safety, or physical robot capability.",
            "This audit does not validate image annotations, dataset licences, train/test leakage, or sensor calibration.",
            "Large model files are listed but not hashed; no files are uploaded or modified unless --json is supplied.",
        ],
        "status": "REVIEW_REQUIRED" if syntax_errors or not dataset_docs else "INVENTORY_ONLY",
    }
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json:
        output = args.json if args.json.is_absolute() else root / args.json
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"Audit report written locally: {output}")
    else:
        print(rendered, end="")
    return 1 if syntax_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
