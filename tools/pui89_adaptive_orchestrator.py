"""Deterministic policy simulator for validated PUI89 agent messages."""
from datetime import datetime
from pui89_agent_contract import detect_disagreements, validate_evidence, validate_message


def _parse_time(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must include timezone")
    return parsed


def evaluate(messages, evidence_by_id, *, now, required_claim_keys=(),
             min_evidence_per_claim=1, max_evidence_age_seconds=3600,
             critical_stop=False):
    """Return a fail-closed policy decision; never authorizes physical actuation."""
    if min_evidence_per_claim < 1 or max_evidence_age_seconds < 0:
        raise ValueError("invalid policy thresholds")
    current = _parse_time(now)

    if critical_stop or any(
        isinstance(m, dict) and
        (m.get("status") == "STOPPED" or m.get("requested_action") == "STOP")
        for m in messages
    ):
        action, reason = "STOP", "critical stop is latched"
    else:
        errors = []
        for i, message in enumerate(messages):
            errors.extend(
                f"message[{i}]: {error}"
                for error in validate_message(message, evidence_by_id)
            )
        referenced_ids = set()
        for message in messages:
            if isinstance(message, dict) and isinstance(message.get("source_ids"), list):
                referenced_ids.update(
                    sid for sid in message["source_ids"] if isinstance(sid, str)
                )
        for sid in sorted(referenced_ids):
            if sid in evidence_by_id:
                errors.extend(
                    f"evidence[{sid}]: {error}"
                    for error in validate_evidence(evidence_by_id[sid])
                )
        if errors:
            action, reason = "SAFE_HOLD", "invalid message or evidence provenance"
        elif any(m.get("status") == "SAFE_HOLD" or
                 m.get("requested_action") == "SAFE_HOLD" for m in messages):
            action, reason = "SAFE_HOLD", "safety hold requested"
        elif any(m.get("status") == "HUMAN_REVIEW" or
                 m.get("requested_action") == "REQUEST_HUMAN_REVIEW"
                 for m in messages):
            action, reason = "REQUEST_HUMAN_REVIEW", "human review requested"
        else:
            used = {sid for m in messages for sid in m["source_ids"]}
            stale = []
            for sid in sorted(used):
                try:
                    age = (current - _parse_time(evidence_by_id[sid]["timestamp"])).total_seconds()
                except (KeyError, TypeError, ValueError):
                    stale.append(sid)
                    continue
                if age < 0 or age > max_evidence_age_seconds:
                    stale.append(sid)

            by_claim = {}
            for message in messages:
                for claim in message["claims"]:
                    by_claim.setdefault(claim["claim_key"], set()).update(claim["evidence_ids"])
            missing = [key for key in required_claim_keys
                       if len(by_claim.get(key, set())) < min_evidence_per_claim]
            if missing or stale or not messages:
                action, reason = "REQUEST_EVIDENCE", "required evidence missing, stale, future-dated, or no messages"
            elif detect_disagreements(messages):
                action, reason = "REQUEST_SPECIALIST_VERIFICATION", "unresolved agent disagreement"
            elif any(m["status"] == "NEEDS_EVIDENCE" or
                     m["requested_action"] == "REQUEST_EVIDENCE" for m in messages):
                action, reason = "REQUEST_EVIDENCE", "agent requested additional evidence"
            else:
                action, reason = "CONTINUE", "policy checks passed for this simulation snapshot"

    return {
        "action": action,
        "reason": reason,
        "simulation_only": True,
        "physical_actuation_permitted": False,
        "message_count": len(messages),
        "evidence_count": len(evidence_by_id),
        "disagreements": detect_disagreements(messages),
        "limitations": [
            "No AI model, specialist agent, external tool, or robot was executed.",
            "Evidence presence and age do not establish truth or sensor quality.",
            "Confidence is not calibrated or treated as probability.",
            "CONTINUE is not authorization for physical action.",
        ],
    }
