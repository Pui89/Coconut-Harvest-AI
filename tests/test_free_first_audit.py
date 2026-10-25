from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "free_first_audit.py"


def run_audit(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_audit_is_offline_and_hashes_small_dataset_files(tmp_path: Path) -> None:
    image = tmp_path / "data" / "images" / "sample.jpg"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"synthetic-test-image-bytes")
    (tmp_path / "example.py").write_text("answer = 42\n", encoding="utf-8")
    (tmp_path / "data" / "DATASET_MANIFEST.csv").write_text(
        "path,source,licence,split\nsample.jpg,synthetic,not-applicable,test\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("Evaluation protocol and recall metrics.\n", encoding="utf-8")

    result = run_audit(tmp_path, "--json", "audit.json")

    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "audit.json").read_text(encoding="utf-8"))
    assert report["network_used"] is False
    assert report["dependencies_installed"] is False
    assert report["model_weights_downloaded"] is False
    assert report["python_syntax_errors"] == []
    assert report["dataset_files_found"] == 2
    image_record = next(
        item for item in report["dataset_file_inventory"] if item["path"] == "data/images/sample.jpg"
    )
    assert image_record["sha256"] == hashlib.sha256(image.read_bytes()).hexdigest()
    assert report["dataset_documentation_candidates_found"]


def test_audit_reports_python_syntax_errors_without_installing_anything(tmp_path: Path) -> None:
    (tmp_path / "broken.py").write_text("def broken(:\n", encoding="utf-8")

    result = run_audit(tmp_path)

    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["python_syntax_errors"]
    assert report["network_used"] is False


def test_audit_skips_virtual_environment_files(tmp_path: Path) -> None:
    venv_file = tmp_path / ".venv" / "lib" / "ignored.py"
    venv_file.parent.mkdir(parents=True)
    venv_file.write_text("this is intentionally not valid Python (:\n", encoding="utf-8")

    result = run_audit(tmp_path)

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["python_files_scanned"] == 0
    assert report["python_syntax_errors"] == []
