"""Shared project-local safeguards for PUI89 mock model adapters."""
from __future__ import annotations
from datetime import datetime
from typing import Any

FORBIDDEN_COMMAND_KEYS = {
    "actuate", "actuator_command", "hardware_command", "physical_action",
    "execute_action", "robot_command", "motor_command", "movement_command",
}

def parse_timestamp(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be valid ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include a timezone")
    return parsed

def reject_command_fields(value: Any) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_COMMAND_KEYS:
                raise ValueError(f"physical command field is forbidden: {key}")
            reject_command_fields(child)
    elif isinstance(value, list):
        for child in value:
            reject_command_fields(child)

def build_review_envelope(*, project_id: str, request: dict[str, Any],
                          observation: dict[str, Any], modality: str,
                          limitations: list[str]) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("request must be an object")
    reject_command_fields(request)
    required = {"request_id", "timestamp", "evidence"}
    missing = sorted(required - request.keys())
    if missing:
        raise ValueError("missing required field(s): " + ", ".join(missing))
    request_id = request["request_id"]
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("request_id must be a non-empty string")
    request_time = parse_timestamp(request["timestamp"])
    evidence = request["evidence"]
    if not isinstance(evidence, dict):
        raise ValueError("evidence must be an object")
    for key in ("source_id", "source_ref"):
        if not isinstance(evidence.get(key), str) or not evidence[key].strip():
            raise ValueError(f"evidence.{key} must be a non-empty string")
    if evidence.get("evidence_kind") != "synthetic":
        raise ValueError("mock adapters accept synthetic evidence only")
    evidence_time = parse_timestamp(evidence.get("timestamp"))
    if evidence_time > request_time:
        raise ValueError("evidence timestamp cannot be later than request timestamp")
    lineage = evidence.get("lineage")
    if not isinstance(lineage, list) or not lineage or not all(
        isinstance(item, str) and item.strip() for item in lineage
    ):
        raise ValueError("evidence.lineage must contain non-empty provenance IDs")
    if not isinstance(observation, dict):
        raise ValueError("observation must be an object")
    evidence_record = {
        "source_id": evidence["source_id"],
        "source_type": "project_mock_fixture",
        "source_ref": evidence["source_ref"],
        "timestamp": evidence["timestamp"],
        "evidence_kind": "synthetic",
        "modality": modality,
        "lineage": lineage,
    }
    message = {
        "agent_id": f"{project_id}.mock_adapter",
        "task_id": request_id,
        "timestamp": request["timestamp"],
        "source_ids": [evidence["source_id"]],
        "observations": [observation],
        "claims": [],
        "confidence": None,
        "confidence_interpretation": "not_applicable",
        "uncertainty": ["Synthetic fixture only; no model inference or calibrated confidence."],
        "limitations": limitations,
        "status": "HUMAN_REVIEW",
        "requested_action": "REQUEST_HUMAN_REVIEW",
    }
    return {
        "schema_version": "1.0",
        "request_id": request_id,
        "project_id": project_id,
        "adapter": {
            "id": f"{project_id}.mock_adapter",
            "mode": "MOCK",
            "model_id": None,
            "model_revision": None,
            "inference_performed": False,
        },
        "status": "MOCK_OBSERVATION_REVIEW_REQUIRED",
        "evidence": evidence_record,
        "agent_message": message,
        "observations": [observation],
        "proposed_actions": [],
        "policy_result": {
            "action": "REQUEST_HUMAN_REVIEW",
            "reason": "project-specific mock observation requires independent review",
            "simulation_only": True,
            "physical_actuation_permitted": False,
        },
        "physical_actuation_permitted": False,
        "limitations": limitations + [
            "Synthetic fixture is not a real sensor observation or model prediction.",
            "No model weights, inference runtime, network service or external API was used.",
            "No physical robot action is available through this adapter.",
        ],
    }
