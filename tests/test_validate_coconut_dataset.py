from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "apps" / "pui89_app" / "validate_coconut_dataset.py"
SPEC = importlib.util.spec_from_file_location("validate_coconut_dataset", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def make_split(root: Path, split: str, image_bytes: bytes) -> None:
    image_dir = root / "images" / split
    label_dir = root / "labels" / split
    image_dir.mkdir(parents=True)
    label_dir.mkdir(parents=True)
    (image_dir / "sample.jpg").write_bytes(image_bytes)
    (label_dir / "sample.txt").write_text("", encoding="utf-8")


def test_flags_exact_duplicate_image_across_splits(tmp_path: Path) -> None:
    for split in ("train", "val", "test"):
        make_split(tmp_path, split, b"same exact image bytes")
    report = MODULE.validate_dataset(tmp_path, class_count=1)
    assert report["status"] == "FAIL"
    assert any("Exact duplicate image content appears in split" in e["message"] for e in report["errors"])


def test_different_image_bytes_do_not_trigger_cross_split_duplicate(tmp_path: Path) -> None:
    for index, split in enumerate(("train", "val", "test")):
        make_split(tmp_path, split, f"unique image fixture {index}".encode())
    report = MODULE.validate_dataset(tmp_path, class_count=1)
    assert not any("Exact duplicate image content appears in split" in e["message"] for e in report["errors"])


def test_rejects_non_positive_class_count(tmp_path: Path) -> None:
    report = MODULE.validate_dataset(tmp_path, class_count=0)
    assert report["status"] == "FAIL"
    assert any("class_count must be >= 1" in e["message"] for e in report["errors"])
