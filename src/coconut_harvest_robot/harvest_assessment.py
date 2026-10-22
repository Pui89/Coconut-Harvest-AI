"""Conservative per-coconut harvest eligibility assessment.

This module classifies a supplied observation and returns a recommendation only.
It does not run a vision model, estimate 3D position, or command robot hardware.
Physical actuation requires an independent validated safety controller/interlocks.
"""
from dataclasses import dataclass
from enum import Enum
import math
from typing import Optional, Tuple


class MaturityClass(str, Enum):
    YOUNG_GREEN = "young_green"
    MATURE_GREEN = "mature_green"
    BROWN_AGING = "brown_aging"
    UNCERTAIN = "uncertain"


class HarvestDecision(str, Enum):
    STOP = "stop"
    REVIEW_REQUIRED = "review_required"
    ELIGIBLE_FOR_SUPERVISED_AUTHORIZATION = "eligible_for_supervised_authorization"


@dataclass(frozen=True)
class CoconutObservation:
    fruit_id: str
    maturity_class: MaturityClass
    class_confidence: float
    # Position must be in a declared, calibrated coordinate frame.
    position_3d_m: Optional[Tuple[float, float, float]] = None
    # Conservative bound in metres; None means unknown.
    position_uncertainty_m: Optional[float] = None
    # These flags must come from validated upstream checks, not guesses.
    location_valid: bool = False
    reachability_verified: bool = False
    within_verified_workspace: bool = False
    capture_ready: bool = False


@dataclass(frozen=True)
class HarvestSafetyContext:
    sensors_healthy: bool
    calibration_valid: bool
    localization_ready: bool
    obstacle_zone_clear: bool
    people_clear: bool
    overhead_hazards_clear: bool
    base_stable: bool
    environment_within_validated_limits: bool
    independent_interlock_ready: bool
    required_supervision_present: bool


@dataclass(frozen=True)
class HarvestAssessment:
    decision: HarvestDecision
    reason_codes: Tuple[str, ...]
    cutter_enabled: bool = False


def _finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def assess_coconut_for_harvest(
    observation: CoconutObservation,
    safety: HarvestSafetyContext,
    *,
    minimum_class_confidence: float = 0.80,
    maximum_position_uncertainty_m: float = 0.20,
    allowed_maturity: Tuple[MaturityClass, ...] = (MaturityClass.MATURE_GREEN,),
) -> HarvestAssessment:
    """Return a fail-closed recommendation; never enables the cutter.

    Threshold defaults are software placeholders for tests and must be calibrated
    from a representative validation study before operational use.
    """
    reasons = []

    if not isinstance(observation.fruit_id, str) or not observation.fruit_id.strip():
        reasons.append("invalid_fruit_id")

    if not _finite_number(minimum_class_confidence) or not 0.0 <= minimum_class_confidence <= 1.0:
        reasons.append("invalid_policy_threshold")
    if not _finite_number(maximum_position_uncertainty_m) or maximum_position_uncertainty_m < 0:
        reasons.append("invalid_policy_threshold")

    if not isinstance(observation.maturity_class, MaturityClass):
        reasons.append("invalid_maturity_class")
    elif observation.maturity_class is MaturityClass.UNCERTAIN:
        reasons.append("uncertain_maturity")
    elif observation.maturity_class not in allowed_maturity:
        reasons.append("maturity_not_selected")

    if not _finite_number(observation.class_confidence) or not 0.0 <= observation.class_confidence <= 1.0:
        reasons.append("invalid_class_confidence")
    elif _finite_number(minimum_class_confidence) and observation.class_confidence < minimum_class_confidence:
        reasons.append("low_class_confidence")

    coords = observation.position_3d_m
    if not observation.location_valid or not observation.reachability_verified:
        reasons.append("location_or_reachability_unverified")
    if not observation.within_verified_workspace:
        reasons.append("outside_or_unknown_verified_workspace")
    if (
        not isinstance(coords, (tuple, list))
        or len(coords) != 3
        or not all(_finite_number(v) for v in coords)
    ):
        reasons.append("invalid_or_missing_3d_position")
    if not _finite_number(observation.position_uncertainty_m):
        reasons.append("unknown_position_uncertainty")
    elif (
        _finite_number(maximum_position_uncertainty_m)
        and observation.position_uncertainty_m > maximum_position_uncertainty_m
    ):
        reasons.append("position_uncertainty_too_high")

    if not observation.capture_ready:
        reasons.append("capture_not_ready")

    safety_checks = (
        (safety.sensors_healthy, "sensor_fault"),
        (safety.calibration_valid, "calibration_invalid"),
        (safety.localization_ready, "localization_not_ready"),
        (safety.obstacle_zone_clear, "obstacle_zone_not_clear"),
        (safety.people_clear, "people_in_exclusion_zone_or_unknown"),
        (safety.overhead_hazards_clear, "overhead_hazard_or_unknown"),
        (safety.base_stable, "base_stability_not_confirmed"),
        (safety.environment_within_validated_limits, "environment_limits_not_confirmed"),
        (safety.independent_interlock_ready, "independent_interlock_not_ready"),
        (safety.required_supervision_present, "required_supervision_missing"),
    )
    reasons.extend(code for passed, code in safety_checks if not passed)

    if reasons:
        decision = (
            HarvestDecision.STOP
            if any(code in {
                "sensor_fault", "calibration_invalid", "localization_not_ready",
                "people_in_exclusion_zone_or_unknown", "overhead_hazard_or_unknown",
                "base_stability_not_confirmed", "environment_limits_not_confirmed",
                "independent_interlock_not_ready", "required_supervision_missing",
                "invalid_or_missing_3d_position", "unknown_position_uncertainty",
                "outside_or_unknown_verified_workspace", "location_or_reachability_unverified",
            } for code in reasons)
            else HarvestDecision.REVIEW_REQUIRED
        )
        return HarvestAssessment(decision, tuple(dict.fromkeys(reasons)), False)

    return HarvestAssessment(
        HarvestDecision.ELIGIBLE_FOR_SUPERVISED_AUTHORIZATION,
        ("all_software_preconditions_passed_physical_authorization_still_required",),
        False,
    )
