"""PUI89 coconut-harvest decision-support API; no actuator authority."""
from __future__ import annotations

from collections import Counter
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="PUI89 Coconut Harvest AI", version="1.0.0",
              description="Simulation-first harvest planning proposals with explicit safety gates. No motor commands.")
COUNTERS: Counter[str] = Counter()


class Candidate(BaseModel):
    target_id: str = Field(min_length=1, max_length=80)
    ripeness_score: float = Field(ge=0, le=1)
    localization_confidence: float = Field(ge=0, le=1)
    distance_m: float = Field(ge=0)
    obstacle_clearance_m: float = Field(ge=0)
    stable_track_frames: int = Field(ge=0)


class AnalyzeRequest(BaseModel):
    rgb_available: bool
    depth_valid: bool
    timestamp_skew_ms: float = Field(ge=0)
    candidates: list[Candidate] = Field(default_factory=list, max_length=500)


class CandidateDecision(BaseModel):
    target_id: str
    status: Literal["REVIEW", "REJECTED", "PROPOSAL_APPROVED_NOT_EXECUTED"]
    reasons: list[str]
    score: float


@app.get("/health")
def health():
    return {"status": "ok", "service": "coconut-harvest-ai", "actuator_authority": False}


@app.get("/metrics")
def metrics():
    return {"requests_total": COUNTERS["analyze"], "metric_type": "service counters, not model-performance benchmarks"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    COUNTERS["analyze"] += 1
    sensor_reasons = []
    if not req.rgb_available:
        sensor_reasons.append("RGB_UNAVAILABLE")
    if not req.depth_valid:
        sensor_reasons.append("DEPTH_INVALID")
    if req.timestamp_skew_ms > 30:
        sensor_reasons.append("TIMESTAMP_SKEW_EXCEEDED")
    if sensor_reasons:
        return {"status": "SAFE_HOLD", "sensor_reasons": sensor_reasons,
                "decisions": [], "actuator_commands_sent": False}

    decisions = []
    for c in req.candidates:
        reasons = []
        if c.localization_confidence < 0.80:
            reasons.append("LOCALIZATION_CONFIDENCE_LOW")
        if c.stable_track_frames < 5:
            reasons.append("TRACK_NOT_STABLE")
        if c.distance_m > 3.0:
            reasons.append("OUTSIDE_CONFIGURED_REACH")
        if c.obstacle_clearance_m < 0.30:
            reasons.append("CLEARANCE_INSUFFICIENT")
        if c.ripeness_score < 0.65:
            reasons.append("RIPENESS_BELOW_CONFIGURED_THRESHOLD")
        score = round(0.45 * c.ripeness_score + 0.40 * c.localization_confidence
                      + 0.15 * min(c.stable_track_frames / 10, 1), 4)
        if any(x in reasons for x in ("LOCALIZATION_CONFIDENCE_LOW", "TRACK_NOT_STABLE")):
            status = "REVIEW"
        elif reasons:
            status = "REJECTED"
        else:
            status = "PROPOSAL_APPROVED_NOT_EXECUTED"
            reasons.append("CONFIGURED_SOFTWARE_GATES_PASSED_NOT_PHYSICAL_SAFETY_VALIDATION")
        decisions.append(CandidateDecision(target_id=c.target_id, status=status,
                                            reasons=reasons, score=score).model_dump())
    decisions.sort(key=lambda x: x["score"], reverse=True)
    return {"status": "ANALYZED", "decisions": decisions,
            "actuator_commands_sent": False,
            "limitations": ["Scores are heuristic, not calibrated probabilities.",
                            "Collision validation and physical robot safety certification are not provided."]}
