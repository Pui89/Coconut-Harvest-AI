"""Typed Python adapters for the PUI89 Shared AI Core draft contracts.

Contract shape is pinned to PUI89 Shared AI Core JSON Schema 0.1.0-draft.
This module uses only the Python standard library and never controls hardware.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import math
from typing import Any, Mapping

CONTRACT_VERSION = "0.1.0-draft"
SCHEMA_SOURCE_COMMIT = "2d9eeb465e6ab571e7391ef6b78b72d4007ba7e5"
SCHEMA_SOURCE = (
    "https://github.com/Pui89/Pui89.github.io/tree/"
    + SCHEMA_SOURCE_COMMIT
    + "/schemas/pui89"
)

MODALITIES = {"rgb", "xray", "depth", "chemical", "audio", "thermal", "telemetry", "text", "other"}
QUALITIES = {"good", "degraded", "poor", "unknown"}
RIGHTS_STATUSES = {"cleared", "restricted", "unknown", "not_applicable"}
INTEGRITY_STATUSES = {"verified", "unverified", "failed", "unknown"}
UNCERTAINTY_LEVELS = {"low", "medium", "high", "unknown"}
FRESHNESS_STATES = {"fresh", "stale", "unknown"}
RISK_LEVELS = {"low", "medium", "high", "critical", "unknown"}
FAILURE_SEVERITIES = {"info", "low", "medium", "high", "critical", "unknown"}
SAFE_STATES = {"confirmed", "not_confirmed", "unknown"}


def _nonblank(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _timestamp(value: Any, field_name: str) -> None:
    _nonblank(value, field_name)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be an ISO 8601 date-time") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field_name} must include a timezone offset")


def _choice(value: Any, choices: set[str], field_name: str) -> None:
    if not isinstance(value, str) or value not in choices:
        raise ValueError(f"{field_name} must be one of {sorted(choices)}")


def _confidence(value: Any, field_name: str = "confidence") -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be null or a finite number from 0 to 1")
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{field_name} must be null or a finite number from 0 to 1")


def _string_list(value: Any, field_name: str, *, minimum: int = 0, unique: bool = False) -> None:
    if not isinstance(value, (list, tuple)) or len(value) < minimum:
        raise ValueError(f"{field_name} must be a list with at least {minimum} item(s)")
    if any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field_name} items must be strings")
    if unique and len(set(value)) != len(value):
        raise ValueError(f"{field_name} items must be unique")


@dataclass(frozen=True)
class Observation:
    observation_id: str
    source: str
    modality: str
    timestamp: str
    quality: str
    provenance: Mapping[str, Any]
    integrity_status: str
    value: Any = None
    payload_ref: str | None = None
    units: str | None = None
    confidence: float | None = None
    calibration: Mapping[str, Any] | None = None
    uncertainty: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        _nonblank(self.observation_id, "observation_id")
        _nonblank(self.source, "source")
        _choice(self.modality, MODALITIES, "modality")
        _timestamp(self.timestamp, "timestamp")
        _choice(self.quality, QUALITIES, "quality")
        _choice(self.integrity_status, INTEGRITY_STATUSES, "integrity_status")
        if self.value is None and (not isinstance(self.payload_ref, str) or not self.payload_ref.strip()):
            raise ValueError("either value or a non-empty payload_ref is required")
        if self.payload_ref is not None:
            _nonblank(self.payload_ref, "payload_ref")
        if self.units is not None and not isinstance(self.units, str):
            raise ValueError("units must be text or null")
        _confidence(self.confidence)
        if not isinstance(self.provenance, Mapping):
            raise ValueError("provenance must be an object")
        required = {"source_id", "method", "rights_status"}
        if not required.issubset(self.provenance):
            raise ValueError("provenance requires source_id, method and rights_status")
        if set(self.provenance) - (required | {"chain_of_custody_ref"}):
            raise ValueError("provenance contains unsupported fields")
        _nonblank(self.provenance["source_id"], "provenance.source_id")
        _nonblank(self.provenance["method"], "provenance.method")
        _choice(self.provenance["rights_status"], RIGHTS_STATUSES, "provenance.rights_status")
        custody = self.provenance.get("chain_of_custody_ref")
        if custody is not None and not isinstance(custody, str):
            raise ValueError("provenance.chain_of_custody_ref must be text or null")
        if self.calibration is not None and not isinstance(self.calibration, Mapping):
            raise ValueError("calibration must be an object or null")
        if self.uncertainty is not None:
            if not isinstance(self.uncertainty, Mapping):
                raise ValueError("uncertainty must be an object")
            if not {"level", "reason"}.issubset(self.uncertainty):
                raise ValueError("uncertainty requires level and reason")
            _choice(self.uncertainty["level"], UNCERTAINTY_LEVELS, "uncertainty.level")
            if not isinstance(self.uncertainty["reason"], str):
                raise ValueError("uncertainty.reason must be text")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.payload_ref is None:
            data.pop("payload_ref")
        if self.uncertainty is None:
            data.pop("uncertainty")
        return data


@dataclass(frozen=True)
class WorldStateRecord:
    world_state_id: str
    timestamp: str
    frame_id: str
    state: Mapping[str, Any]
    observation_refs: tuple[str, ...]
    freshness: str
    uncertainty: Mapping[str, Any]
    limitations: tuple[str, ...]
    known: tuple[str, ...] | None = None
    unknown: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        _nonblank(self.world_state_id, "world_state_id")
        _timestamp(self.timestamp, "timestamp")
        _nonblank(self.frame_id, "frame_id")
        if not isinstance(self.state, Mapping):
            raise ValueError("state must be an object")
        _string_list(self.observation_refs, "observation_refs", unique=True)
        _choice(self.freshness, FRESHNESS_STATES, "freshness")
        if not isinstance(self.uncertainty, Mapping) or not {"level", "reason"}.issubset(self.uncertainty):
            raise ValueError("uncertainty requires level and reason")
        _choice(self.uncertainty["level"], UNCERTAINTY_LEVELS, "uncertainty.level")
        if not isinstance(self.uncertainty["reason"], str):
            raise ValueError("uncertainty.reason must be text")
        _string_list(self.limitations, "limitations")
        if self.known is not None:
            _string_list(self.known, "known")
        if self.unknown is not None:
            _string_list(self.unknown, "unknown")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.known is None:
            data.pop("known")
        if self.unknown is None:
            data.pop("unknown")
        return data


@dataclass(frozen=True)
class ActionProposalRecord:
    proposal_id: str
    created_at: str
    proposed_action: str
    rationale: str
    evidence_refs: tuple[str, ...]
    preconditions: tuple[str, ...]
    risk_level: str
    human_approval_required: bool = True
    authority: str = "advisory_only"
    actuation_allowed: bool = False
    simulation_only: bool = True
    confidence: float | None = None
    expires_at: str | None = None

    def __post_init__(self) -> None:
        _nonblank(self.proposal_id, "proposal_id")
        _timestamp(self.created_at, "created_at")
        _nonblank(self.proposed_action, "proposed_action")
        _nonblank(self.rationale, "rationale")
        _string_list(self.evidence_refs, "evidence_refs", minimum=1)
        _string_list(self.preconditions, "preconditions")
        _choice(self.risk_level, RISK_LEVELS, "risk_level")
        _confidence(self.confidence)
        if self.expires_at is not None:
            _timestamp(self.expires_at, "expires_at")
        if self.human_approval_required is not True:
            raise ValueError("human_approval_required must remain true")
        if self.authority != "advisory_only":
            raise ValueError("authority must remain advisory_only")
        if self.actuation_allowed is not False:
            raise ValueError("actuation_allowed must remain false")
        if self.simulation_only is not True:
            raise ValueError("this adapter only permits simulation-only proposals")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FailureReport:
    failure_id: str
    reported_at: str
    failure_mode: str
    severity: str
    evidence_refs: tuple[str, ...]
    containment: str
    recovery_recommendation: str
    unresolved_uncertainty: tuple[str, ...]
    safe_state: str
    affected_component: str | None = None

    def __post_init__(self) -> None:
        _nonblank(self.failure_id, "failure_id")
        _timestamp(self.reported_at, "reported_at")
        _nonblank(self.failure_mode, "failure_mode")
        _choice(self.severity, FAILURE_SEVERITIES, "severity")
        _string_list(self.evidence_refs, "evidence_refs")
        _nonblank(self.containment, "containment")
        _nonblank(self.recovery_recommendation, "recovery_recommendation")
        _string_list(self.unresolved_uncertainty, "unresolved_uncertainty")
        _choice(self.safe_state, SAFE_STATES, "safe_state")
        if self.affected_component is not None and not isinstance(self.affected_component, str):
            raise ValueError("affected_component must be text or null")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.affected_component is None:
            data.pop("affected_component")
        return data
