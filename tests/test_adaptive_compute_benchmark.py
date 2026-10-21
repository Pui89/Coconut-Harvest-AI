from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "adaptive_compute_benchmark.py"


def test_strategies_match_reference_for_empty_and_nonempty_workloads() -> None:
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        from adaptive_compute_benchmark import run_benchmark

        for size in (0, 1, 17, 1_000):
            report = run_benchmark(size=size, repeats=1, threshold=10)
            assert report["all_outputs_match_reference"] is True
            assert all(report["correctness"].values())
    finally:
        sys.path.pop(0)


@pytest.mark.parametrize(
    ("size", "repeats", "threshold", "message"),
    [
        (1.5, 1, 1, "size must be a non-negative integer"),
        (True, 1, 1, "size must be a non-negative integer"),
        (1, 1.5, 1, "repeats must be a positive integer"),
        (1, False, 1, "repeats must be a positive integer"),
        (1, 1, 2.5, "threshold must be a positive integer"),
        (1, 1, True, "threshold must be a positive integer"),
    ],
)
def test_non_integer_arguments_raise_clear_value_error(size, repeats, threshold, message):
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        from adaptive_compute_benchmark import run_benchmark

        with pytest.raises(ValueError, match=message):
            run_benchmark(size=size, repeats=repeats, threshold=threshold)
    finally:
        sys.path.pop(0)


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (["--size", "-1"], "size must be a non-negative integer"),
        (["--repeats", "0"], "repeats must be a positive integer"),
        (["--threshold", "0"], "threshold must be a positive integer"),
        (["--size", "1.5"], "invalid int value"),
    ],
)
def test_invalid_arguments_fail_with_cli_error(args: list[str], message: str) -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert message in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_emits_machine_readable_report() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--size", "10", "--repeats", "1", "--threshold", "5"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    report = json.loads(result.stdout)
    assert report["format"] == "pui89-adaptive-compute-cpu-benchmark-v1"
    assert report["workload"]["adaptive_choice"] == "builtin"
    assert report["all_outputs_match_reference"] is True
