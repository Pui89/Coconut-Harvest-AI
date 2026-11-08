"""PUI89 AI Core v2 — fail-closed decision-gate reference implementation.

This package creates advisory gate decisions only. It never controls hardware.
"""
from .safety import GateDecision, evaluate_proposal

__all__ = ["GateDecision", "evaluate_proposal"]
