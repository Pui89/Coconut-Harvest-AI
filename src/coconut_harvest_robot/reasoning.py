"""High-level reasoning adapter for embodied coconut harvesting.

The reasoning model interprets perception/world state and proposes a task decision.
It must not command actuators directly; a deterministic safety/planning layer owns execution.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


DEFAULT_REASONING_MODEL = "google/gemma-4-31B-it"


@dataclass
class ReasoningDecision:
    goal: str
    rationale: str
    confidence: float
    next_steps: List[str] = field(default_factory=list)
    target_id: Optional[str] = None
    requires_human_review: bool = False


class CoconutReasoner:
    """Adapter boundary for Gemma 4 31B IT or another VLM/reasoning model."""

    def __init__(
        self,
        model: str = DEFAULT_REASONING_MODEL,
        infer: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
    ):
        self.model = model
        self.infer = infer

    def decide(self, observation: Dict[str, Any]) -> ReasoningDecision:
        if self.infer is None:
            return self._conservative_fallback(observation)
        raw = self.infer({
            "model": self.model,
            "task": "coconut_harvest_reasoning",
            "observation": observation,
            "constraints": [
                "do_not_control_motors",
                "respect_workspace_and_collision_constraints",
                "treat_occluded_targets_as_uncertain",
                "verify_target_before_cutting",
            ],
        })
        return ReasoningDecision(
            goal=str(raw.get("goal", "inspect")),
            rationale=str(raw.get("rationale", "")),
            confidence=float(raw.get("confidence", 0.0)),
            next_steps=list(raw.get("next_steps", [])),
            target_id=raw.get("target_id"),
            requires_human_review=bool(raw.get("requires_human_review", False)),
        )

    def _conservative_fallback(self, observation: Dict[str, Any]) -> ReasoningDecision:
        targets = observation.get("targets", [])
        if not targets:
            return ReasoningDecision("search", "No verified harvest target is available.", 0.35, ["scan_canopy"])
        target = targets[0]
        return ReasoningDecision(
            "inspect_target",
            "Use the first candidate only as an inspection target; verify ripeness, geometry and clearance before action.",
            0.55,
            ["verify_target", "check_branch_clearance", "plan_safe_approach"],
            str(target.get("id", "")),
        )
