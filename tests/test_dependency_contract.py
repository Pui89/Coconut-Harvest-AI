from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def requirement_names(lines: list[str]) -> set[str]:
    names = set()
    for line in lines:
        value = line.strip()
        if not value or value.startswith("#") or value.startswith("--"):
            continue
        match = re.match(r"([A-Za-z0-9_.-]+)", value)
        if match is None:
            raise AssertionError(f"Unrecognised requirement: {value}")
        names.add(match.group(1).lower().replace("_", "-").replace(".", "-"))
    return names


class DependencyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project = tomllib.loads(
            (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        )["project"]

    def test_torch_is_not_a_default_dependency(self) -> None:
        default_names = requirement_names(self.project["dependencies"])
        self.assertNotIn("torch", default_names)
        self.assertEqual(self.project["requires-python"], ">=3.11")

    def test_torch_extra_has_patched_version_floor(self) -> None:
        torch_requirements = self.project["optional-dependencies"]["torch"]
        self.assertTrue(any(item.startswith("torch>=2.15.0") for item in torch_requirements))

    def test_cpu_requirements_select_official_cpu_wheel_index(self) -> None:
        lines = (ROOT / "requirements-cpu-torch.txt").read_text(encoding="utf-8").splitlines()
        self.assertIn("--index-url https://download.pytorch.org/whl/cpu", lines)
        self.assertTrue(any(line.startswith("torch>=2.15.0") for line in lines))

    def test_requirements_manifest_matches_project_runtime_dependencies(self) -> None:
        project_names = requirement_names(self.project["dependencies"])
        requirements_names = requirement_names(
            (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        )
        self.assertEqual(requirements_names, project_names)


if __name__ == "__main__":
    unittest.main()
