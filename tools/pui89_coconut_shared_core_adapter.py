"""Map Coconut Harvest records into advisory-only PUI89 Shared AI Core contracts.

This adapter transforms supplied records only. It does not inspect pixels, run
models, infer harvest readiness, or control hardware.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping

SCHEMA_VERSION = "0.1.0"
_SOURCE_TYPES = {"sensor", "human", "dataset", "simulation", "software", "external"}
_FORBIDDEN_KEYS = {
    "actuate", "actuator_command", "hardware_command", "physical_action",
    "execute_action", "robot_command", "motor_command", "movement_command",
    "cut_command", "climb_command",
}


def _timestamp(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{field} must include a timezone")
    return value


def _reject_physical_commands(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_KEYS:
                raise ValueError(f"physical command field is forbidden: {key}")
            _reject_physical_commands(child)
    elif isinstance(value, list):
        for child in value:
            _reject_physical_commands(child)


def build_failure_report(
    failure_event: Mapping[str, Any], *, evidence_refs: list[str] | None = None
) -> dict[str, Any]:
    """Convert an explicitly supplied failure event; never invent one."""
    if not isinstance(failure_event, Mapping):
        raise ValueError("failure_event must be an object")
    occurred_at = _timestamp(failure_event.get("occurred_at"), "occurred_at")
    component = failure_event.get("system_or_component")
    severity = failure_event.get("severity")
    summary = failure_event.get("summary")
    if not isinstance(component, str) or not component.strip():
        raise ValueError("system_or_component is required")
    if severity not in {"informational", "low", "moderate", "high", "critical", "unknown"}:
        raise ValueError("unsupported failure severity")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("failure summary is required")
    refs = evidence_refs if evidence_refs is not None else []
    if not isinstance(refs, list) or not all(isinstance(ref, str) and ref.strip() for ref in refs):
        raise ValueError("evidence_refs must contain non-empty strings")
    return {
        "schema_version": SCHEMA_VERSION,
        "failure_id": str(failure_event.get("failure_id") or "coconut-failure-unassigned"),
        "occurred_at": occurred_at,
        "system_or_component": component,
        "severity": severity,
        "summary": summary,
        "observed_result": str(failure_event.get("observed_result") or "Not supplied"),
        "evidence_refs": refs,
        "response_status": "open",
    }


def build_shared_core_records(
    request: Mapping[str, Any],
    orchard_report: Mapping[str, Any],
    *,
    failure_event: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Translate supplied orchard records into five shared contract records.

    The optional FailureReport is emitted only when a caller supplies an
    explicit failure event. No harvest action is proposed or authorized.
    """
    if not isinstance(request, Mapping) or not isinstance(orchard_report, Mapping):
        raise ValueError("request and orchard_report must be objects")
    _reject_physical_commands(request)
    _reject_physical_commands(orchard_report)

    request_id = request.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("request_id is required")
    observed_at = _timestamp(request.get("timestamp"), "timestamp")
    evidence = request.get("evidence")
    if not isinstance(evidence, Mapping):
        raise ValueError("evidence must be an object")
    source_id = evidence.get("source_id")
    source_ref = evidence.get("source_ref")
    source_type = evidence.get("source_type")
    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("evidence.source_id is required")
    if not isinstance(source_ref, str) or not source_ref.strip():
        raise ValueError("evidence.source_ref is required")
    if source_type not in _SOURCE_TYPES:
        raise ValueError("evidence.source_type must be a supported shared source type")
    evidence_at = _timestamp(evidence.get("timestamp"), "evidence.timestamp")
    if datetime.fromisoformat(evidence_at.replace("Z", "+00:00")) > datetime.fromisoformat(observed_at.replace("Z", "+00:00")):
        raise ValueError("evidence timestamp cannot be later than request timestamp")
    lineage = evidence.get("lineage")
    if not isinstance(lineage, list) or not lineage or not all(
        isinstance(item, str) and item.strip() for item in lineage
    ):
        raise ValueError("evidence.lineage must contain provenance identifiers")

    fruits = orchard_report.get("fruit_observations")
    tree = orchard_report.get("tree")
    if not isinstance(fruits, list) or not isinstance(tree, Mapping):
        raise ValueError("orchard_report must contain fruit_observations and tree records")
    if orchard_report.get("decision_boundary", {}).get("automatic_harvest_authorized") is not False:
        raise ValueError("orchard report must explicitly keep automatic harvest unauthorized")
    for fruit in fruits:
        if not isinstance(fruit, Mapping) or fruit.get("harvest_authorized") is not False:
            raise ValueError("every fruit record must explicitly keep harvest unauthorized")

    observation_id = f"coconut-{request_id}-observation"
    passport_id = f"coconut-{request_id}-passport"
    quality_status = "unknown" if not fruits else (
        "degraded" if any(fruit.get("errors") for fruit in fruits) else "usable"
    )
    provenance = {
        "recorded_at": observed_at,
        "dataset_or_file": source_ref,
    }
    for field in ("license", "content_hash", "operator"):
        value = evidence.get(field)
        if isinstance(value, str) and value.strip():
            provenance[field] = value

    observation = {
        "schema_version": SCHEMA_VERSION,
        "observation_id": observation_id,
        "observed_at": observed_at,
        "source": {"source_id": source_id, "source_type": source_type},
        "modality": "rgb",
        "payload": {
            "domain": "coconut_harvest",
            "tree": dict(tree),
            "fruit_count": len(fruits),
            "maturity_counts": dict(orchard_report.get("maturity_counts", {})),
            "fruit_observations": [dict(fruit) for fruit in fruits],
            "interpretation": "supplied_record_for_human_review",
        },
        "quality": {
            "status": quality_status,
            "notes": "Structured-record integrity only; image quality and model performance are not assessed.",
        },
        "uncertainty": {
            "description": "No image inference or confidence calibration is performed by this adapter.",
            "method": "not_assessed",
        },
        "provenance": provenance,
    }

    entities = [{
        "entity_id": str(fruit.get("fruit_id") or f"fruit-{index + 1}"),
        "category": "coconut_fruit",
        "state": {
            "maturity_class": fruit.get("maturity_class", "unknown"),
            "disposition": fruit.get("disposition", "unknown"),
            "review_status": fruit.get("review_status", "pending"),
        },
        "evidence_refs": [observation_id],
    } for index, fruit in enumerate(fruits)]
    unknowns = [
        "Harvest readiness is not determined.",
        "No image pixels or model inference were evaluated by this adapter.",
        "Tree height remains unverified unless supported by independent measurement evidence.",
    ]
    if tree.get("height_band") in (None, "UNKNOWN"):
        unknowns.append("Verified tree-height band is unavailable.")
    world_state = {
        "schema_version": SCHEMA_VERSION,
        "state_id": f"coconut-{request_id}-world-state",
        "updated_at": observed_at,
        "evidence_refs": [observation_id],
        "entities": entities,
        "unknowns": unknowns,
        "notes": "Time-bounded orchard record assembled from caller-supplied evidence.",
    }
    action_proposal = {
        "schema_version": SCHEMA_VERSION,
        "proposal_id": f"coconut-{request_id}-review-proposal",
        "created_at": observed_at,
        "objective": "Request human review of supplied coconut observations; do not harvest.",
        "world_state_ref": world_state["state_id"],
        "actions": [],
        "authority": {
            "mode": "advisory_only",
            "human_approval_required": True,
            "execution_authorized": False,
        },
        "uncertainties": unknowns,
    }
    evidence_passport = {
        "schema_version": SCHEMA_VERSION,
        "passport_id": passport_id,
        "created_at": observed_at,
        "project_id": "coconut-harvest-ai",
        "subject_ref": observation_id,
        "conclusion": {
            "statement": "Candidate coconut observations are available for review; harvest readiness is not established.",
            "status": "conditional",
        },
        "evidence": {
            "supporting_refs": [observation_id],
            "conflicting_refs": [],
            "missing_items": [
                "Independently reviewed real-image labels and provenance.",
                "Held-out detection and maturity-classification evaluation.",
                "Validated geometry, reachability and project-specific harvest safety gates.",
            ],
            "provenance_status": "partial",
        },
        "uncertainty": {
            "description": "No calibrated model confidence or harvest-readiness estimate is produced.",
            "assessment_method": "not_assessed",
            "calibration_status": "not_assessed",
        },
        "safety": {
            "gate_status": "not_evaluated",
            "risk_level": "unknown",
            "gate_notes": "Human review required; no cutting, climbing, capture or robot movement authority.",
        },
        "human_review": {"review_required": True, "status": "pending"},
        "verification": {
            "status": "not_tested",
            "evidence_refs": [],
            "verification_scope": "Adapter transformation only; not model or field validation.",
        },
        "execution_authorized": False,
    }

    failure_report = (
        build_failure_report(failure_event, evidence_refs=[observation_id])
        if failure_event is not None else None
    )
    return {
        "observation": observation,
        "world_state": world_state,
        "action_proposal": action_proposal,
        "failure_report": failure_report,
        "evidence_passport": evidence_passport,
        "scope": "record-transformation-only",
        "model_inference_performed": False,
        "physical_actuation_permitted": False,
    }
