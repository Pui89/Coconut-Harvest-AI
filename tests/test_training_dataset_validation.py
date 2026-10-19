from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from training.train_detector import validate_dataset_yaml


def make_dataset_config(root: Path, names: dict[int, str] | None = None) -> Path:
    for split in ("train", "val", "test"):
        (root / "images" / split).mkdir(parents=True)
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
