from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "audit_coconut_annotations.py"


def run_audit(tmp_path: Path, boxes: list[dict]) -> subprocess.CompletedProcess[str]:
    annotations = {
        "format": "pui89-coconut-annotations-v1",
        "images": [{"filename": "fixture.jpg", "width": 100, "height": 100, "boxes": boxes}],
    }
    source = tmp_path / "annotations.json"
    source.write_text(json.dumps(annotations), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--annotations", str(source)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_valid_boxes_are_reported_without_geometry_errors(tmp_path: Path) -> None:
    result = run_audit(tmp_path, [{"x": 0.1, "y": 0.1, "w": 0.2, "h": 0.2}])
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["box_count"] == 1
    assert report["geometry_error_count"] == 0
    assert report["images"][0]["status"] == "geometry_checks_passed"


def test_out_of_bounds_box_fails_with_geometry_error(tmp_path: Path) -> None:
    result = run_audit(tmp_path, [{"x": 0.9, "y": 0.1, "w": 0.2, "h": 0.2}])
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["geometry_error_count"] == 1
    assert any(x["issue"] == "box_outside_normalized_image_bounds" for x in report["images"][0]["errors"])


def test_overlap_and_border_are_review_warnings_not_errors(tmp_path: Path) -> None:
    result = run_audit(
        tmp_path,
        [
            {"x": 0.0, "y": 0.1, "w": 0.3, "h": 0.3},
            {"x": 0.1, "y": 0.1, "w": 0.3, "h": 0.3},
        ],
    )
    assert result.returncode == 0
    image = json.loads(result.stdout)["images"][0]
    assert image["status"] == "review_warnings"
    assert image["border_warnings"]
    assert image["overlap_warnings"]
