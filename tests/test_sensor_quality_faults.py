import importlib.util
import math
from pathlib import Path
import sys

import pytest


def load_source_module(name: str, relative_path: str):
    source = Path(__file__).resolve().parents[1] / relative_path
    spec = importlib.util.spec_from_file_location(name, source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sensor_quality = load_source_module(
    "coconut_harvest_sensor_quality_test_module",
    "src/coconut_harvest_robot/sensor_quality.py",
)
SensorObservation = sensor_quality.SensorObservation
SensorStatus = sensor_quality.SensorStatus
assess_sensor_health = sensor_quality.assess_sensor_health

def test_good_synchronized_sensors_are_ok():
    report = assess_sensor_health([
        SensorObservation(name="rgb", quality=1.0, timestamp_s=1.00),
        SensorObservation(name="depth", quality=0.9, timestamp_s=1.02),
    ])
    assert report.status is SensorStatus.OK
    assert report.timestamp_skew_s == pytest.approx(0.02)


@pytest.mark.parametrize("quality", [math.nan, math.inf, -math.inf, -0.1, 1.1])
def test_invalid_quality_fails_closed_as_degraded(quality):
    report = assess_sensor_health([
        SensorObservation(name="rgb", quality=quality, timestamp_s=1.0),
        SensorObservation(name="depth", quality=1.0, timestamp_s=1.01),
    ])
    assert report.status is SensorStatus.DEGRADED
    assert report.quality < 1.0
    assert any("invalid quality value" in reason for reason in report.reasons)


@pytest.mark.parametrize("timestamp", [math.nan, math.inf, -math.inf])
def test_non_finite_timestamp_fails_closed_as_unsynchronized(timestamp):
    report = assess_sensor_health([
        SensorObservation(name="rgb", quality=1.0, timestamp_s=timestamp),
        SensorObservation(name="depth", quality=1.0, timestamp_s=1.01),
    ])
    assert report.status is SensorStatus.UNSYNCHRONIZED
    assert math.isinf(report.timestamp_skew_s)
    assert any("non-finite" in reason for reason in report.reasons)


@pytest.mark.parametrize("max_skew", [math.nan, math.inf, -math.inf, -0.01])
def test_invalid_sync_tolerance_fails_closed(max_skew):
    report = assess_sensor_health([
        SensorObservation(name="rgb", quality=1.0, timestamp_s=1.0, max_skew_s=max_skew),
        SensorObservation(name="depth", quality=1.0, timestamp_s=1.01, max_skew_s=0.05),
    ])
    assert report.status is SensorStatus.UNSYNCHRONIZED
    assert any("tolerance is invalid" in reason for reason in report.reasons)


def test_missing_sensor_is_not_reported_as_ok():
    report = assess_sensor_health([
        SensorObservation(name="rgb", quality=1.0, timestamp_s=1.0),
        SensorObservation(name="depth", available=False, quality=1.0, timestamp_s=1.01),
    ])
    assert report.status is SensorStatus.DEGRADED
    assert any("missing" in reason for reason in report.reasons)
