"""Model-optional agentic workflow coordinator.

This standard-library-only coordinator sequences input validation, the existing
project decision agent, an independent policy gate, and an evidence summary.
It makes no network calls, invokes no shell commands, and never executes actions.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from agents.project_agent import run_agent


def _report(
    *,
    project: str,
    status: str,
    evidence_sha256: str | None,
    trace: list[dict[str, str]],
    decision: dict[str, Any] | None = None,
    issues: list[str] | None = None,
) -> dict[str, Any]:
    """Create a stable, privacy-conscious workflow result."""
    return {
        "schema_version": 1,
        "project": project,
        "status": status,
        "evidence_sha256": evidence_sha256,
        "decision": decision,
        "issues": list(issues or []),
        "trace": trace,
        "human_review_required": True,
        "execution_performed": False,
        "network_access_used": False,
        "model_inference_used": False,
        "actuator_commands_issued": False,
    }


def run_agentic_workflow(observation: Any) -> dict[str, Any]:
    """Run the finite local workflow and return an advisory proposal.

    The observation is not written to disk. Evidence hashing uses canonical JSON
    with NaN/Infinity disallowed. Only the existing project agent is called; no
    arbitrary tool names or LLM-produced code can be executed.
    """
    trace: list[dict[str, str]] = [
        {"step": "workflow_start", "status": "started"}
    ]

    if not isinstance(observation, dict):
        trace.append({"step": "input_validation", "status": "failed"})
        return _report(
            project="pui89",
            status="INCONCLUSIVE",
            evidence_sha256=None,
            trace=trace,
            issues=["Observation must be a JSON-compatible object."],
        )

    try:
        canonical = json.dumps(
            observation, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
    except (TypeError, ValueError, OverflowError):
        trace.append({"step": "input_validation", "status": "failed"})
        return _report(
            project="pui89",
            status="INCONCLUSIVE",
            evidence_sha256=None,
            trace=trace,
            issues=["Observation is not valid finite JSON data."],
        )

    evidence_sha256 = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    trace.append({"step": "input_validation", "status": "passed"})
    try:
        raw_decision = run_agent(observation)
        serializer = getattr(raw_decision, "to_dict", None)
        if not callable(serializer):
            raise TypeError("Project agent returned no structured serializer.")
        decision = serializer()
    except (AttributeError, TypeError, ValueError, OverflowError):
        trace.append({"step": "project_agent", "status": "failed"})
        return _report(
            project="pui89",
            status="INCONCLUSIVE",
            evidence_sha256=evidence_sha256,
            trace=trace,
            issues=["The project decision agent did not return a valid structured decision."],
        )

    if not isinstance(decision, dict):
        trace.append({"step": "project_agent", "status": "failed"})
        return _report(
            project="pui89",
            status="INCONCLUSIVE",
            evidence_sha256=evidence_sha256,
            trace=trace,
            issues=["The project decision agent did not return a structured object."],
        )

    project = decision.get("project")
    if not isinstance(project, str) or not project.strip():
        project = "pui89"
    trace.append({"step": "project_agent", "status": "completed"})

    # The policy gate fails closed if the domain agent ever changes its contract.
    policy_issues: list[str] = []
    if decision.get("requires_human_approval") is not True:
        policy_issues.append("The project decision must require human approval.")
    if decision.get("actuator_command") is not None:
        policy_issues.append("Actuator commands are prohibited in this workflow.")
    if not isinstance(decision.get("recommendation"), str):
        policy_issues.append("The project decision must provide a string recommendation.")
    if not isinstance(decision.get("status"), str):
        policy_issues.append("The project decision must provide a string status.")
    if not isinstance(decision.get("reasons"), list):
        policy_issues.append("The project decision must provide a reasons list.")

    if policy_issues:
        trace.append({"step": "policy_gate", "status": "blocked"})
        return _report(
            project=project,
            status="BLOCKED_BY_POLICY",
            evidence_sha256=evidence_sha256,
            trace=trace,
            decision=None,
            issues=policy_issues,
        )

    trace.append({"step": "policy_gate", "status": "passed"})
    trace.append({"step": "evidence_summary", "status": "created"})
    return _report(
        project=project,
        status="PROPOSAL_READY_FOR_HUMAN_REVIEW",
        evidence_sha256=evidence_sha256,
        trace=trace,
        decision=decision,
        issues=[],
    )
