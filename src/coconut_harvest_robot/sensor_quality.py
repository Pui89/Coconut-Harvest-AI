from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum


class SensorStatus(str, Enum):
    OK = "OK"
    DEGRADED = "DEGRADED"
    MISSING = "MISSING"
    UNSYNCHRONIZED = "UNSYNCHRONIZED"


@dataclass(frozen=True)
class SensorObservation:
    name: str
    available: bool = True
    quality: float = 1.0
    timestamp_s: float | None = None
    max_skew_s: float = 0.05


@dataclass(frozen=True)
class SensorHealthReport:
    status: SensorStatus
    quality: float
    timestamp_skew_s: float
    reasons: tuple[str, ...]


def assess_sensor_health(
    observations: list[SensorObservation],
) -> SensorHealthReport:
    if not observations:
        return SensorHealthReport(
            SensorStatus.MISSING, 0.0, float("inf"), ("no sensors supplied",)
        )

    active = [observation for observation in observations if observation.available]
    if not active:
        return SensorHealthReport(
            SensorStatus.MISSING, 0.0, float("inf"), ("all sensors unavailable",)
        )

    reasons: list[str] = []
    quality_values: list[float] = []
    for observation in active:
        quality = observation.quality
        if not math.isfinite(quality) or not 0.0 <= quality <= 1.0:
            reasons.append(f"sensor {observation.name!r} has invalid quality value")
            quality_values.append(0.0 if not math.isfinite(quality) else min(1.0, max(0.0, quality)))
        else:
            quality_values.append(quality)

    invalid_timestamps = [
        observation.name
        for observation in active
        if observation.timestamp_s is not None
        and not math.isfinite(observation.timestamp_s)
    ]
    timestamps = [
        observation.timestamp_s
        for observation in active
        if observation.timestamp_s is not None
        and math.isfinite(observation.timestamp_s)
    ]
    if invalid_timestamps:
        skew = float("inf")
        reasons.append(
            "sensor timestamps are non-finite: " + ", ".join(invalid_timestamps)
        )
    else:
        skew = max(timestamps) - min(timestamps) if len(timestamps) > 1 else 0.0

    if any(quality < 0.5 for quality in quality_values):
        reasons.append("one or more sensors are degraded")
    if len(active) != len(observations):
        reasons.append("one or more sensors are missing")

    allowed_skew = min(observation.max_skew_s for observation in active)
    if not math.isfinite(allowed_skew) or allowed_skew < 0.0:
        reasons.append("sensor synchronization tolerance is invalid")
        skew = float("inf")
    elif skew > allowed_skew:
        reasons.append("sensor timestamps are not synchronized")

    if invalid_timestamps or not math.isfinite(allowed_skew) or allowed_skew < 0.0 or skew > allowed_skew:
        status = SensorStatus.UNSYNCHRONIZED
    elif reasons:
        status = SensorStatus.DEGRADED
    else:
        status = SensorStatus.OK

    return SensorHealthReport(
        status=status,
        quality=sum(quality_values) / len(quality_values),
        timestamp_skew_s=skew,
        reasons=tuple(dict.fromkeys(reasons)),
    )
