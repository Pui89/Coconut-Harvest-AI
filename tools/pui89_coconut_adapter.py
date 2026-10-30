"""Coconut Harvest adapter for the shared PUI89 policy contract.

This module maps an explicitly supplied observation into a common evidence/message
record. It does not run a detector, infer maturity, or command harvesting hardware.
"""
from __future__ import annotations

from pui89_agent_contract import validate_evidence, validate_message

ALLOWED_MATURITY_LABELS = {
    "young_green", "developing", "mature_green", "brown_aging",
}


def build_coconut_message(*, observation_id, source_ref, timestamp,
                          maturity_label, modality="rgb",
                          evidence_kind="inferred", confidence=None,
                          uncertainty=None, limitations=None):
    """Build a validated proposal from caller-supplied, not model-generated, data."""
    if maturity_label not in ALLOWED_MATURITY_LABELS:
        raise ValueError("maturity_label must be one of the four defined classes")
    evidence = {
        "source_id": observation_id,
        "source_type": "coconut_observation",
        "source_ref": source_ref,
        "timestamp": timestamp,
        "evidence_kind": evidence_kind,
        "modality": modality,
        "lineage": [observation_id],
    }
    message = {
        "agent_id": "coconut-harvest-adapter",
        "task_id": f"coconut-maturity:{observation_id}",
        "timestamp": timestamp,
        "source_ids": [observation_id],
        "observations": [{
            "observation_id": observation_id,
            "domain": "coconut_harvest",
            "modality": modality,
        }],
        "claims": [{
            "claim_id": f"maturity:{observation_id}",
            "claim_key": "coconut_maturity",
            "value": maturity_label,
            "evidence_ids": [observation_id],
        }],
        "confidence": confidence,
        "uncertainty": uncertainty or ["caller-supplied label; not independently verified"],
        "limitations": limitations or [
            "Adapter does not run or validate an AI detector.",
            "Maturity label is supplied by the caller.",
            "No harvesting action or physical capability is authorized.",
        ],
        "status": "PROPOSED",
        "requested_action": "VERIFY",
    }
    errors = validate_evidence(evidence) + validate_message(message, {observation_id: evidence})
    if errors:
        raise ValueError("; ".join(errors))
    return {"message": message, "evidence": evidence}


def evaluate_coconut_snapshot(records, *, now, max_evidence_age_seconds=3600):
    """Route adapter records through the shared PUI89 policy simulator."""
    from pui89_adaptive_orchestrator import evaluate

    messages = [record["message"] for record in records]
    evidence_by_id = {record["evidence"]["source_id"]: record["evidence"]
                      for record in records}
    return evaluate(
        messages,
        evidence_by_id,
        now=now,
        required_claim_keys=("coconut_maturity",),
        max_evidence_age_seconds=max_evidence_age_seconds,
    )
