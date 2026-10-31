"""Coconut Harvest project adapter: mock maturity observations only."""
from __future__ import annotations
from typing import Any
from pui89_project_adapter_common import build_review_envelope

MATURITY_LABELS = {"young_green", "developing", "mature_green", "brown_aging"}

def adapt_coconut_mock(request: Any) -> dict[str, Any]:
    if not isinstance(request, dict):
        raise ValueError("request must be an object")
    sample = request.get("mock_observation")
    if not isinstance(sample, dict):
        raise ValueError("mock_observation must be an object")
    label = sample.get("candidate_maturity_label")
    if label not in MATURITY_LABELS:
        raise ValueError("candidate_maturity_label must be one of the four documented classes")
    cues = sample.get("visual_cues")
    if not isinstance(cues, list) or not cues or not all(
        isinstance(cue, str) and cue.strip() for cue in cues
    ):
        raise ValueError("visual_cues must be a non-empty list of descriptive strings")
    observation = {
        "domain": "coconut_harvest",
        "observation_type": "candidate_maturity_cues",
        "candidate_maturity_label": label,
        "visual_cues": cues,
        "interpretation": "unverified_candidate_for_human_review",
    }
    return build_review_envelope(
        project_id="coconut_harvest",
        request=request,
        observation=observation,
        modality="rgb_mock_fixture",
        limitations=[
            "Candidate maturity label is supplied by a synthetic test fixture.",
            "This adapter does not inspect an image or run a detector.",
            "It does not determine harvest readiness or authorize cutting, climbing or capture.",
            "Tree-height and physical robot capabilities are not established by this test.",
        ],
    )
