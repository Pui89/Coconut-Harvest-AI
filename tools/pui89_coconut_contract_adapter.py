"""Coconut-specific adapter to the pinned PUI89 Shared AI Core contract draft.

Only caller-supplied findings are mapped. This module does not run a detector,
infer a maturity class, or authorize harvesting or hardware actuation.
"""
from __future__ import annotations

from pui89_autonomy.llm_interfaces import VisionFinding, validate_vision_finding
from pui89_core.contracts import Observation


def build_coconut_observation(
    finding: VisionFinding,
    *,
    observation_id: str,
    timestamp: str,
    modality: str = "rgb",
    quality: str = "unknown",
    rights_status: str = "unknown",
    calibration: dict | None = None,
    integrity_status: str = "unverified",
) -> Observation:
    """Map a validated, caller-supplied finding into a provenance-bearing observation.

    The finding confidence is retained as an input score, not represented as
    calibrated probability. Rights and integrity default to unknown/unverified.
    """
    issues = validate_vision_finding(finding)
    if issues:
        raise ValueError("; ".join(issues))
    value = {
        "label": finding.label,
        "bbox_xyxy": list(finding.bbox_xyxy) if finding.bbox_xyxy is not None else None,
        "notes": finding.notes,
    }
    return Observation(
        observation_id=observation_id,
        source=finding.source_id,
        modality=modality,
        timestamp=timestamp,
        quality=quality,
        provenance={
            "source_id": finding.source_id,
            "method": "caller_supplied_vision_finding",
            "rights_status": rights_status,
        },
        integrity_status=integrity_status,
        value=value,
        confidence=finding.confidence,
        calibration=calibration,
        uncertainty={
            "level": "unknown",
            "reason": "input confidence is not established as calibrated; detector performance is not asserted",
        },
    )
