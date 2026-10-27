"""Simulation-first action proposals. This module never executes robot commands."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ActionProposal:
    action: str
    rationale: str
    confidence: float
    requires_human_review: bool = True
    simulation_only: bool = True
    executed: bool = False

    def __post_init__(self) -> None:
        if not self.action.strip():
            raise ValueError("action must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.simulation_only or self.executed:
            raise ValueError("v0.1 permits proposals only; execution is prohibited")

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def propose_action(action: str, rationale: str, confidence: float) -> ActionProposal:
    """Create a non-executable proposal for review or simulation."""
    return ActionProposal(action=action, rationale=rationale, confidence=confidence)
