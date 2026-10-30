#!/usr/bin/env python3
"""PUI89 standard-library agent message and evidence provenance contract.

This module validates records and flags explicit claim disagreement. It does not
run AI agents, infer truth, calibrate confidence, or resolve conflicts.
"""
from __future__ import annotations

from datetime import datetime
import re
from typing import Any

MESSAGE_REQUIRED = {
    "agent_id", "task_id", "timestamp", "source_ids", "observations",
    "claims", "confidence", "uncertainty", "limitations", "status",
    "requested_action",
}
EVIDENCE_REQUIRED = {
    "source_id", "source_type", "source_ref", "timestamp",
    "evidence_kind", "modality", "lineage",
}
EVIDENCE_KINDS = {"observed", "inferred", "synthetic", "derived", "unknown"}
MESSAGE_STATUSES = {"PROPOSED", "NEEDS_EVIDENCE", "SAFE_HOLD", "HUMAN_REVIEW", "STOPPED"}
ALLOWED_ACTIONS = {
    "CONTINUE", "REQUEST_EVIDENCE", "VERIFY", "SAFE_HOLD",
    "REQUEST_HUMAN_REVIEW", "STOP",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _timestamp_error(value: Any) -> bool:
    if not _nonempty_string(value):
        return True
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.tzinfo is None or parsed.utcoffset() is None
    except (ValueError, TypeError, AttributeError):
        return True


def validate_evidence(record: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["evidence must be an object"]
    for key in sorted(EVIDENCE_REQUIRED - record.keys()):
        errors.append(f"missing required field: {key}")
    for key in ("source_id", "source_type", "source_ref", "modality"):
        if key in record and not _nonempty_string(record[key]):
            errors.append(f"{key} must be a non-empty string")
    if "timestamp" in record and _timestamp_error(record["timestamp"]):
        errors.append("timestamp must be ISO 8601 with timezone")
    if record.get("evidence_kind") not in EVIDENCE_KINDS:
        errors.append("evidence_kind is invalid")
    if "lineage" in record and (
        not isinstance(record["lineage"], list)
        or not all(_nonempty_string(item) for item in record["lineage"])
    ):
        errors.append("lineage must be an array of non-empty source/transformation IDs")
    digest = record.get("source_hash")
    if digest is not None and (
        not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest)
    ):
        errors.append("source_hash must be a 64-character SHA-256 hex digest or null")
    return errors


def validate_message(message: Any, evidence_by_id: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(message, dict):
        return ["message must be an object"]
    for key in sorted(MESSAGE_REQUIRED - message.keys()):
        errors.append(f"missing required field: {key}")
    for key in ("agent_id", "task_id"):
        if key in message and not _nonempty_string(message[key]):
            errors.append(f"{key} must be a non-empty string")
    if "timestamp" in message and _timestamp_error(message["timestamp"]):
        errors.append("timestamp must be ISO 8601 with timezone")
    source_ids = message.get("source_ids")
    if not isinstance(source_ids, list) or not all(_nonempty_string(x) for x in source_ids):
        errors.append("source_ids must be an array of non-empty IDs")
        source_ids = []
    elif len(source_ids) != len(set(source_ids)):
        errors.append("source_ids must not contain duplicates")
    for key in ("observations", "claims", "uncertainty", "limitations"):
        if key in message and not isinstance(message[key], list):
            errors.append(f"{key} must be an array")
    if isinstance(message.get("observations"), list) and not all(
        isinstance(item, dict) for item in message["observations"]
    ):
        errors.append("observations entries must be objects")
    if isinstance(message.get("claims"), list):
        for index, claim in enumerate(message["claims"]):
            if not isinstance(claim, dict):
                errors.append(f"claims[{index}] must be an object")
                continue
            for key in ("claim_id", "claim_key", "value"):
                if key not in claim or not _nonempty_string(str(claim[key])):
                    errors.append(f"claims[{index}].{key} must be non-empty")
            refs = claim.get("evidence_ids", [])
            if not isinstance(refs, list) or not all(_nonempty_string(x) for x in refs):
                errors.append(f"claims[{index}].evidence_ids must be an array of IDs")
            elif any(ref not in source_ids for ref in refs):
                errors.append(f"claims[{index}].evidence_ids must be included in source_ids")
    confidence = message.get("confidence")
    if confidence is not None and (
        not isinstance(confidence, (int, float)) or isinstance(confidence, bool)
        or not 0.0 <= confidence <= 1.0
    ):
        errors.append("confidence must be null or a finite number from 0 to 1")
    if message.get("confidence_interpretation", "uncalibrated") not in {
        "uncalibrated", "calibrated", "not_applicable"
    }:
        errors.append("confidence_interpretation is invalid")
    if message.get("status") not in MESSAGE_STATUSES:
        errors.append("status is invalid")
    if message.get("requested_action") not in ALLOWED_ACTIONS:
        errors.append("requested_action is invalid")
    if evidence_by_id is not None:
        for source_id in source_ids:
            if source_id not in evidence_by_id:
                errors.append(f"source_ids references unknown evidence: {source_id}")
        if isinstance(message.get("claims"), list):
            for index, claim in enumerate(message["claims"]):
                if isinstance(claim, dict):
                    for evidence_id in claim.get("evidence_ids", []):
                        if evidence_id not in evidence_by_id:
                            errors.append(f"claims[{index}] references unknown evidence: {evidence_id}")
    return errors


def detect_disagreements(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return differing values for the same explicit claim_key; never vote or average."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for message in messages:
        if not isinstance(message, dict) or not isinstance(message.get("claims"), list):
            continue
        for claim in message["claims"]:
            if not isinstance(claim, dict) or not _nonempty_string(claim.get("claim_key")):
                continue
            grouped.setdefault(claim["claim_key"], []).append({
                "agent_id": message.get("agent_id"),
                "value": claim.get("value"),
                "claim_id": claim.get("claim_id"),
                "evidence_ids": claim.get("evidence_ids", []),
            })
    disagreements = []
    for claim_key, entries in sorted(grouped.items()):
        distinct = {repr(entry["value"]) for entry in entries}
        if len(distinct) > 1:
            disagreements.append({
                "claim_key": claim_key,
                "status": "DISAGREEMENT_REQUIRES_REVIEW",
                "entries": entries,
                "resolution": None,
            })
    return disagreements
