"""Shared PUI89 observation and world-state safety contract.

This module is dependency-free. It supports decision proposals and simulation only;
it never authorizes physical actuation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any


@dataclass(frozen=True)
class Observation:
    value: Any
    source: str | None
    observed_at: float | None
    confidence: float | None
    calibrated: bool | None = None


@dataclass(frozen=True)
class Assessment:
    status: str
    reasons: tuple[str, ...] = ()

    @property
    def requires_human_review(self) -> bool:
        return self.status != "ACCEPT"

    @property
    def may_enter_simulation(self) -> bool:
        return self.status in {"ACCEPT", "REVIEW"}

    @property
    def may_actuate_hardware(self) -> bool:
        # This shared contract intentionally never authorizes hardware actions.
        return False


def assess_observation(
    observation: Observation,
    *,
    now: float,
    max_age_seconds: float = 5.0,
    min_confidence: float = 0.70,
    require_calibration: bool = False,
    require_human_review: bool = False,
) -> Assessment:
    """Classify one observation for planning; never authorize an actuator."""
    if isinstance(now, bool) or not isinstance(now, (int, float)) or not math.isfinite(now):
        raise ValueError("now must be a finite number")
    if isinstance(max_age_seconds, bool) or not isinstance(max_age_seconds, (int, float)) or not math.isfinite(max_age_seconds) or max_age_seconds < 0:
        raise ValueError("max_age_seconds must be finite and non-negative")
    if isinstance(min_confidence, bool) or not isinstance(min_confidence, (int, float)) or not math.isfinite(min_confidence) or not 0.0 <= min_confidence <= 1.0:
        raise ValueError("min_confidence must be finite and between 0 and 1")

    reasons: list[str] = []
    if observation.value is None:
        return Assessment("REJECT", ("missing_value",))
    if not observation.source:
        reasons.append("missing_source_provenance")
    if observation.observed_at is None:
        reasons.append("missing_timestamp")
    elif isinstance(observation.observed_at, bool) or not isinstance(observation.observed_at, (int, float)) or not math.isfinite(observation.observed_at):
        return Assessment("REJECT", ("invalid_timestamp",))
    elif observation.observed_at > now:
        return Assessment("REJECT", ("timestamp_in_future",))
    elif now - observation.observed_at > max_age_seconds:
        reasons.append("stale_observation")

    confidence = observation.confidence
    if confidence is None:
        reasons.append("missing_confidence")
    elif isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
        return Assessment("REJECT", ("invalid_confidence_range",))
    elif confidence < min_confidence:
        reasons.append("low_confidence")

    if observation.calibrated is False:
        reasons.append("sensor_not_calibrated")
    elif require_calibration and observation.calibrated is not True:
        reasons.append("calibration_unverified")
    if require_human_review:
        reasons.append("human_review_required")

    if reasons:
        return Assessment("REVIEW", tuple(reasons))
    return Assessment("ACCEPT", ("eligible_for_planning_or_simulation_only",))


@dataclass
class WorldState:
    """Minimal timestamped observation ledger with conservative conflict checks."""
    _observations: dict[str, list[Observation]] = field(default_factory=dict)

    def update(self, key: str, observation: Observation) -> None:
        if not key.strip():
            raise ValueError("world-state key must not be empty")
        self._observations.setdefault(key, []).append(observation)

    def assess(
        self,
        key: str,
        *,
        now: float,
        max_age_seconds: float = 5.0,
        min_confidence: float = 0.70,
    ) -> Assessment:
        observations = self._observations.get(key, [])
        if not observations:
            return Assessment("REJECT", ("unknown_world_state",))

        assessments = [
            assess_observation(
                item,
                now=now,
                max_age_seconds=max_age_seconds,
                min_confidence=min_confidence,
            )
            for item in observations
        ]

        # A missing or malformed timestamp cannot be safely ordered against
        # other observations. Reject the combined state instead of allowing
        # max() to raise TypeError or silently selecting a different reading.
        if any(
            "missing_timestamp" in result.reasons
            or "invalid_timestamp" in result.reasons
            for result in assessments
        ):
            return Assessment("REJECT", ("unorderable_observation_timestamp",))

        usable = [
            item for item, result in zip(observations, assessments)
            if result.status == "ACCEPT"
        ]
        if len(usable) > 1:
            first_value = usable[0].value
            if any(item.value != first_value for item in usable[1:]):
                return Assessment("REVIEW", ("conflicting_fresh_observations",))

        latest = max(
            enumerate(observations),
            key=lambda pair: (
                pair[1].observed_at
                if pair[1].observed_at is not None else float("-inf"),
                pair[0],
            ),
        )[1]
        result = assess_observation(
            latest,
            now=now,
            max_age_seconds=max_age_seconds,
            min_confidence=min_confidence,
        )
        if len(usable) > 1 and result.status == "ACCEPT":
            return Assessment("ACCEPT", ("consistent_fresh_observations",))
        return result

    def keys(self) -> tuple[str, ...]:
        return tuple(sorted(self._observations))
