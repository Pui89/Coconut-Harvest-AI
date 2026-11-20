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
    return run_payload(tmp_path, annotations)


def run_payload(tmp_path: Path, payload: object) -> subprocess.CompletedProcess[str]:
    source = tmp_path / "annotations.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
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


def test_non_object_top_level_fails_with_clear_cli_error(tmp_path: Path) -> None:
    result = run_payload(tmp_path, [{"images": []}])
    assert result.returncode == 2
    assert "annotation JSON top level must be an object" in result.stderr
    assert "Traceback" not in result.stderr


def test_non_list_images_fails_with_clear_cli_error(tmp_path: Path) -> None:
    result = run_payload(tmp_path, {"images": {"filename": "x"}})
    assert result.returncode == 2
    assert "'images' must be a list" in result.stderr


def test_non_object_image_fails_with_clear_cli_error(tmp_path: Path) -> None:
    result = run_payload(tmp_path, {"images": [None]})
    assert result.returncode == 2
    assert "images[0] must be an object" in result.stderr
    assert "Traceback" not in result.stderr


def test_non_list_boxes_fails_with_clear_cli_error(tmp_path: Path) -> None:
    result = run_payload(tmp_path, {"images": [{"filename": "fixture.jpg", "boxes": {"x": 0.1}}]})
    assert result.returncode == 2
    assert "images[0].boxes must be a list" in result.stderr
    assert "Traceback" not in result.stderr


def test_non_object_box_is_recorded_as_geometry_error(tmp_path: Path) -> None:
    result = run_audit(tmp_path, [None])
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["images"][0]["errors"] == [{"box": 1, "issue": "box_must_be_an_object"}]


def test_nonfinite_and_boolean_coordinates_are_rejected(tmp_path: Path) -> None:
    result = run_audit(
        tmp_path,
        [
            {"x": float("nan"), "y": 0.1, "w": 0.2, "h": 0.2},
            {"x": True, "y": 0.1, "w": 0.2, "h": 0.2},
        ],
    )
    assert result.returncode == 1
    report = json.loads(result.stdout)
    assert report["geometry_error_count"] == 2
    assert all(image["human_visual_qa"] == "not_automated" for image in report["images"])


def test_invalid_overlap_threshold_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "annotations.json"
    source.write_text(json.dumps({"images": []}), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--annotations", str(source), "--overlap-iou-warning", "nan"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "must be a finite number between 0 and 1" in result.stderr
