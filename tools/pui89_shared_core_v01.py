"""Map Coconut adapter records to PUI89 Shared AI Core v0.1 contracts.

The mapping preserves caller-supplied labels as evidence, marks quality unknown,
and emits only a non-executable human-review proposal. It does not infer
maturity, validate a detector, or control harvesting hardware.
"""
from __future__ import annotations

from datetime import datetime

SCHEMA_VERSION = "0.1.0"
ALLOWED_MODALITIES = {
    "rgb", "depth", "thermal", "audio", "lidar", "radar", "imu",
    "gps", "xray", "chemical", "text", "other",
}


def _require_timestamp(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO-8601 string")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("timestamp must be valid ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include a timezone")
    return value


def build_coconut_v01_records(record: dict) -> dict:
    """Translate a validated legacy Coconut record into v0.1 shared records."""
    if not isinstance(record, dict):
        raise ValueError("record must be an object")
    evidence = record.get("evidence")
    message = record.get("message")
    if not isinstance(evidence, dict) or not isinstance(message, dict):
        raise ValueError("record must contain evidence and message objects")

    observation_id = evidence.get("source_id")
    timestamp = _require_timestamp(evidence.get("timestamp"))
    modality = evidence.get("modality")
    if not isinstance(observation_id, str) or not observation_id.strip():
        raise ValueError("evidence.source_id must be a non-empty string")
    if modality not in ALLOWED_MODALITIES:
        raise ValueError("evidence.modality is not supported by Shared AI Core v0.1")

    # The current Coconut adapter receives a label from its caller; it is not
    # proof of a camera reading or a model prediction.
    source_type = "simulation" if evidence.get("evidence_kind") == "synthetic" else "human"
    claims = message.get("claims", [])
    observations = message.get("observations", [])
    payload = {
        "domain": "coconut_harvest",
        "observations": observations,
        "claims": claims,
        "limitations": message.get("limitations", []),
    }
    uncertainty_items = message.get("uncertainty", [])
    observation = {
        "schema_version": SCHEMA_VERSION,
        "observation_id": observation_id,
        "observed_at": timestamp,
        "source": {
            "source_id": observation_id,
            "source_type": source_type,
            "device_or_system": "PUI89 Coconut caller-supplied adapter",
        },
        "modality": modality,
        "payload": payload,
        "quality": {
            "status": "unknown",
            "notes": "Caller-supplied label; independent sensor/model verification not established.",
        },
        "uncertainty": {
            "description": "; ".join(str(item) for item in uncertainty_items)
            or "Uncertainty not supplied.",
        },
        "provenance": {
            "recorded_at": timestamp,
            "dataset_or_file": evidence.get("source_ref", ""),
        },
    }

    proposal = {
        "schema_version": SCHEMA_VERSION,
        "proposal_id": f"coconut-human-review:{observation_id}",
        "created_at": timestamp,
        "objective": "Request human review of the caller-supplied coconut maturity label.",
        "actions": [{
            "action_id": f"review:{observation_id}",
            "description": "Have a qualified human reviewer verify the maturity label and evidence.",
            "risk_level": "unknown",
            "preconditions": [
                "Review the original observation and its provenance.",
                "Do not treat the supplied maturity label as independently verified.",
            ],
            "expected_effect": "A human reviewer confirms, rejects, or requests more evidence.",
            "hazards": [
                "Incorrect maturity classification may cause an unsuitable harvest decision.",
                "Worker and animal safety must be assessed separately.",
            ],
            "evidence_refs": [observation_id],
        }],
        "authority": {
            "mode": "advisory_only",
            "human_approval_required": True,
            "execution_authorized": False,
        },
        "uncertainties": [str(item) for item in uncertainty_items]
        or ["No uncertainty details were supplied."],
    }
    return {"observation": observation, "action_proposal": proposal}
