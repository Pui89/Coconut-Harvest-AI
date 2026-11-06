"""PUI89 SHIELD warning classification reference logic.

This module is a software policy reference only. It does not read hardware sensors,
control actuators, stop vehicles, isolate batteries, or certify safety.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class WarningState(str, Enum):
    NORMAL = "NORMAL"
    ADVISORY = "ADVISORY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"
    UNKNOWN_DEGRADED = "UNKNOWN_DEGRADED"


@dataclass(frozen=True)
class HazardAssessment:
    """Evidence-bounded input to the SHIELD policy classifier."""
    observation_valid: bool
    sensor_conflict: bool = False
    advisory: bool = False
    severity: str = "unknown"
    imminent_hazard_confirmed: bool = False
    evidence_refs: Tuple[str, ...] = ()


def classify_warning(assessment: HazardAssessment) -> WarningState:
    """Return a warning state; never issue a physical command.

    Independently confirmed imminent hazards take precedence. Invalid, missing,
    conflicting or unsupported observations fail to UNKNOWN_DEGRADED. Remaining
    severity thresholds must be defined and validated separately per project.
    """
    if assessment.imminent_hazard_confirmed:
        if not assessment.evidence_refs:
            return WarningState.UNKNOWN_DEGRADED
        return WarningState.EMERGENCY

    if not assessment.observation_valid or assessment.sensor_conflict:
        return WarningState.UNKNOWN_DEGRADED

    severity = assessment.severity.lower()
    if severity in {"critical", "high", "medium", "low"} and not assessment.evidence_refs:
        return WarningState.UNKNOWN_DEGRADED
    if severity == "critical":
        return WarningState.CRITICAL
    if severity == "high":
        return WarningState.WARNING
    if assessment.advisory or severity == "medium":
        return WarningState.ADVISORY
    if severity in {"low", "none"}:
        return WarningState.NORMAL
    return WarningState.UNKNOWN_DEGRADED


def proposal_requires_human_review(*, physical_action: bool = True) -> bool:
    """Physical-action proposals require human review; this never authorizes execution."""
    return bool(physical_action)
