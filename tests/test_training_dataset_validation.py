from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from training.train_detector import validate_dataset_yaml


def make_dataset_config(root: Path, names: dict[int, str] | None = None) -> Path:
    for split in ("train", "val", "test"):
        image_dir = root / "images" / split
        image_dir.mkdir(parents=True)
        # The validator checks dataset structure and suffixes, not image decoding.
        (image_dir / f"{split}-example.jpg").write_bytes(b"test fixture; not a real image")
    config = {
        "path": str(root),
        "train": "images/train",
        "val": "images/val",
        "test": "images/test",
        "names": names or {0: "coconut"},
    }
    path = root / "coconut.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return path


def test_accepts_existing_coconut_dataset_splits(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path)
    config = validate_dataset_yaml(config_path, require_test=True)
    assert config["names"] == {0: "coconut"}


def test_rejects_dataset_without_explicit_coconut_class(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path, names={0: "fruit"})
    with pytest.raises(ValueError, match="explicit coconut class"):
        validate_dataset_yaml(config_path)


def test_rejects_missing_validation_split_path(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path)
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["val"] = "images/missing-validation"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="val"):
        validate_dataset_yaml(config_path)


def test_rejects_empty_image_split(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path)
    (tmp_path / "images" / "val" / "val-example.jpg").unlink()
    with pytest.raises(ValueError, match="val path contains no supported image files"):
        validate_dataset_yaml(config_path)


def test_rejects_non_contiguous_class_ids(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path, names={1: "coconut"})
    with pytest.raises(ValueError, match="contiguous from zero"):
        validate_dataset_yaml(config_path)


def test_accepts_yolo_text_file_with_existing_image(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path)
    image = tmp_path / "images" / "train" / "train-example.jpg"
    list_file = tmp_path / "train-images.txt"
    list_file.write_text(str(image), encoding="utf-8")
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["train"] = str(list_file)
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    validate_dataset_yaml(config_path)


def test_accepts_yolo_list_paths_relative_to_dataset_root(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path)
    (tmp_path / "train-images.txt").write_text(
        "images/train/train-example.jpg\n", encoding="utf-8"
    )
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["train"] = "train-images.txt"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")
    validate_dataset_yaml(config_path)


def test_class_names_are_matched_to_numeric_ids(tmp_path: Path) -> None:
    config_path = make_dataset_config(tmp_path, names={0: "other", 1: "coconut", 2: "fruit"})
    validate_dataset_yaml(config_path)


def test_rejects_malformed_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "broken.yaml"
    config_path.write_text("names: [coconut\ntrain: [", encoding="utf-8")
    with pytest.raises(ValueError, match="Dataset YAML is invalid"):
        validate_dataset_yaml(config_path)
