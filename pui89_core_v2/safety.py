"""Fail-closed safety evaluation for non-executable action proposals.

Standard-library only. This module never executes a proposal or calls hardware.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class GateDecision:
    decision: str
    reasons: tuple[str, ...]
    proposal_id: str | None
    world_state_id: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def evaluate_proposal(
    proposal: Mapping[str, Any],
    world_state: Mapping[str, Any],
    observations: Sequence[Mapping[str, Any]],
    *,
    human_authorized: bool = False,
    now: datetime | None = None,
    max_state_age_seconds: int = 30,
) -> GateDecision:
    """Return ALLOW_FOR_HUMAN_REVIEW or HOLD/BLOCKED; never execute anything.

    ALLOW_FOR_HUMAN_REVIEW means only that the supplied evidence passed these
    baseline checks. It is not permission to actuate hardware or make a
    consequential decision. A separate project-specific interlock is required.
    """
    reasons: list[str] = []
    proposal_id = proposal.get("proposal_id") if isinstance(proposal, Mapping) else None
    state_id = world_state.get("state_id") if isinstance(world_state, Mapping) else None

    if not isinstance(proposal, Mapping) or not isinstance(world_state, Mapping):
        return GateDecision("BLOCKED", ("proposal_or_world_state_not_an_object",), proposal_id, state_id)

    required_proposal = {
        "proposal_id", "project_id", "world_state_id", "intent",
        "preconditions", "risk", "authorization", "decision",
    }
    missing = sorted(required_proposal - proposal.keys())
    if missing:
        reasons.append("proposal_missing_fields:" + ",".join(missing))

    if proposal.get("decision") != "PROPOSED":
        reasons.append("proposal_not_in_proposed_state")

    if proposal.get("world_state_id") != world_state.get("state_id"):
        reasons.append("world_state_reference_mismatch")

    if world_state.get("status") != "CURRENT":
        reasons.append("world_state_not_current")

    timestamp = _parse_timestamp(world_state.get("created_at"))
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        reasons.append("evaluation_clock_must_be_timezone_aware")
    elif timestamp is None:
        reasons.append("world_state_timestamp_missing_or_invalid")
    else:
        age = (current.astimezone(timezone.utc) - timestamp).total_seconds()
        if age < 0:
            reasons.append("world_state_timestamp_in_future")
        elif age > max_state_age_seconds:
            reasons.append("world_state_stale")

    claims = world_state.get("claims")
    if not isinstance(claims, list) or not claims:
        reasons.append("world_state_has_no_evidence_linked_claims")
    else:
        for index, claim in enumerate(claims):
            if not isinstance(claim, Mapping):
                reasons.append(f"claim_{index}_invalid")
                continue
            if claim.get("value_status") in {"UNKNOWN", "CONFLICTED", "STALE"}:
                reasons.append(f"claim_{index}_{str(claim.get('value_status')).lower()}")
            if not claim.get("evidence_ids"):
                reasons.append(f"claim_{index}_has_no_evidence")

    observation_ids = {
        item.get("observation_id")
        for item in observations
        if isinstance(item, Mapping) and isinstance(item.get("observation_id"), str)
    }
    expected_ids = set(proposal.get("supporting_observation_ids") or [])
    if not expected_ids:
        reasons.append("proposal_has_no_supporting_observations")
    elif not expected_ids.issubset(observation_ids):
        reasons.append("supporting_observation_missing")

    for item in observations:
        if not isinstance(item, Mapping) or item.get("observation_id") not in expected_ids:
            continue
        if item.get("status") != "valid":
            reasons.append("supporting_observation_not_valid")
        source = item.get("source")
        if not isinstance(source, Mapping) or source.get("integrity_status") != "verified":
            reasons.append("supporting_observation_provenance_not_verified")

    risk = proposal.get("risk")
    if not isinstance(risk, Mapping):
        reasons.append("risk_assessment_missing")
    elif risk.get("level") in {"critical", "high", "unknown"}:
        reasons.append("risk_level_requires_hold")

    authorization = proposal.get("authorization")
    if not isinstance(authorization, Mapping) or authorization.get("status") != "approved":
        reasons.append("explicit_human_authorization_missing")
    if not human_authorized:
        reasons.append("human_authorization_not_supplied_to_gate")

    if reasons:
        return GateDecision("HOLD", tuple(dict.fromkeys(reasons)), proposal_id, state_id)

    return GateDecision(
        "ALLOW_FOR_HUMAN_REVIEW",
        ("baseline_checks_passed_no_execution_performed",),
        proposal_id,
        state_id,
    )
