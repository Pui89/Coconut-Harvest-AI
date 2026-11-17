from __future__ import annotations

import re
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _requirement_names(lines: list[str]) -> set[str]:
    names = set()
    for line in lines:
        value = line.strip()
        if not value or value.startswith("#") or value.startswith("--"):
            continue
        match = re.match(r"([A-Za-z0-9_.-]+)", value)
        assert match is not None, f"Unrecognised requirement: {value}"
        names.add(match.group(1).lower().replace("_", "-").replace(".", "-"))
    return names


def test_torch_is_not_a_default_dependency() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    default_names = _requirement_names(project["dependencies"])
    assert "torch" not in default_names
    assert project["requires-python"] == ">=3.11"


def test_torch_extra_has_a_patched_version_floor() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    torch_requirements = project["optional-dependencies"]["torch"]
    assert any(item.startswith("torch>=2.15.0") for item in torch_requirements)


def test_cpu_requirements_select_official_cpu_wheel_index() -> None:
    lines = (ROOT / "requirements-cpu-torch.txt").read_text(encoding="utf-8").splitlines()
    assert "--index-url https://download.pytorch.org/whl/cpu" in lines
    assert any(line.startswith("torch>=2.15.0") for line in lines)


def test_requirements_manifest_matches_project_runtime_dependencies() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    project_names = _requirement_names(project["dependencies"])
    requirements_names = _requirement_names(
        (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    )
    assert requirements_names == project_names
