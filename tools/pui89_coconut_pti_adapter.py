"""Coconut-specific PTI adapter for a human-reviewed maturity candidate.

Maps one caller-supplied VisionFinding into the existing shared contracts.
It does not run a model, verify botanical maturity, assess harvest readiness,
or authorize cutting, lifting, robot motion, or other physical action.
"""
from __future__ import annotations

from pui89_autonomy.llm_interfaces import VisionFinding
from pui89_core.contracts import ActionProposalRecord, WorldStateRecord
from tools.pui89_coconut_contract_adapter import build_coconut_observation


_MATURITY_ALIASES = {
    "young": "young_green",
    "young_green": "young_green",
    "mature_green": "mature_green",
    "yellow": "yellow",
    "brown": "brown",
    "brown_aging": "brown",
}


def normalize_maturity_candidate(label: str) -> str:
    """Normalize known visual labels; preserve unknown labels as unknown."""
    key = label.strip().lower().replace(" ", "_")
    return _MATURITY_ALIASES.get(key, "unknown")


def build_coconut_pti_packet(
    finding: VisionFinding,
    *,
    observation_id: str,
    state_id: str,
    proposal_id: str,
    timestamp: str,
    frame_id: str = "orchard-frame-unverified",
) -> dict:
    """Build Observation, WorldState and advisory review proposal records.

    The confidence value is retained as an uncalibrated model/input score.
    The returned proposal can request human review only; it cannot authorize
    harvest operations or physical actuation.
    """
    observation = build_coconut_observation(
        finding,
        observation_id=observation_id,
        timestamp=timestamp,
        modality="rgb",
        quality="unknown",
        rights_status="unknown",
        integrity_status="unverified",
    )
    maturity = normalize_maturity_candidate(finding.label)

    world_state = WorldStateRecord(
        world_state_id=state_id,
        timestamp=timestamp,
        frame_id=frame_id,
        state={
            "entity_category": "coconut_candidate",
            "visual_maturity_candidate": maturity,
            "source_label": finding.label,
            "confidence_uncalibrated": finding.confidence,
            "harvestability": "not_assessed",
            "height_m": None,
            "height_status": "unverified",
        },
        observation_refs=(observation_id,),
        freshness="unknown",
        uncertainty={
            "level": "unknown",
            "reason": (
                "Input confidence is uncalibrated; visual class is not verified "
                "botanical maturity or harvest readiness."
            ),
        },
        limitations=(
            "Caller-supplied finding only; no detector inference was run.",
            "No botanical maturity or harvest-readiness assessment was performed.",
            "Tree height, reach, stability and physical safety were not assessed.",
        ),
        unknown=(
            "Human confirmation of the visual maturity candidate is required.",
            "Actual harvestability is unknown.",
            "Tree height and physical reach feasibility are unverified.",
        ),
    )

    proposal = ActionProposalRecord(
        proposal_id=proposal_id,
        created_at=timestamp,
        proposed_action="request_human_maturity_review",
        rationale=(
            "Review the candidate maturity label and source image before any "
            "harvest planning; this record is not a harvest instruction."
        ),
        evidence_refs=(observation_id,),
        preconditions=(
            "Authorized human reviewer inspects the source image.",
            "Image provenance and reuse rights are independently reviewed.",
            "Harvest readiness is assessed separately from visual appearance.",
        ),
        risk_level="unknown",
        human_approval_required=True,
        authority="advisory_only",
        actuation_allowed=False,
        simulation_only=True,
        confidence=None,
    )

    return {
        "observation": observation.to_dict(),
        "world_state": world_state.to_dict(),
        "action_proposal": proposal.to_dict(),
        "status": "HUMAN_REVIEW_REQUIRED",
        "execution_authorized": False,
        "physical_actuation_authorized": False,
    }
