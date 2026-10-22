"""Shared local-first fault monitoring and incident records.

This module detects only conditions explicitly reported to it by application code.
It is not an antivirus, intrusion detector, gunshot detector, or hardware safety controller.
Do not log passwords, tokens, private imagery, or other sensitive payloads.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from threading import RLock
from typing import Any


class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class Domain(str, Enum):
    SOFTWARE = "software"
    SENSOR = "sensor"
    POWER = "power"
    NETWORK = "network"
    SECURITY = "security"
    PHYSICAL = "physical"
    ENVIRONMENT = "environment"
    DATA = "data"
    UNKNOWN = "unknown"


class Response(str, Enum):
    CONTINUE_WITH_MONITORING = "continue_with_monitoring"
    LIMIT_OPERATION = "limit_operation"
    STOP_MISSION_AND_ALERT = "stop_mission_and_alert"
    ISOLATE_COMPROMISED_COMPONENT = "isolate_compromised_component"
    HUMAN_EMERGENCY_PROCEDURE = "human_emergency_procedure"
    MANUAL_RECOVERY = "manual_recovery"


@dataclass(frozen=True)
class FaultReport:
    code: str
    domain: Domain
    severity: Severity
    message: str
    source: str = "unspecified"
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FaultDecision:
    response: Response
    inhibit_hazardous_actions: bool
    alert_operator: bool
    require_human_review_before_resume: bool
    reason: str


# Conservative default map. Project-specific policy can make a response stricter.
_CRITICAL_RESPONSES = {
    Domain.SECURITY: Response.ISOLATE_COMPROMISED_COMPONENT,
    Domain.PHYSICAL: Response.HUMAN_EMERGENCY_PROCEDURE,
    Domain.UNKNOWN: Response.MANUAL_RECOVERY,
}


def decide_response(report: FaultReport) -> FaultDecision:
    """Return a conservative response suggestion; never controls hardware itself."""
    if report.severity is Severity.CRITICAL:
        response = _CRITICAL_RESPONSES.get(report.domain, Response.STOP_MISSION_AND_ALERT)
        return FaultDecision(
            response=response,
            inhibit_hazardous_actions=True,
            alert_operator=True,
            require_human_review_before_resume=True,
            reason=f"Critical {report.domain.value} fault: {report.code}",
        )
    if report.severity is Severity.WARNING:
        return FaultDecision(
            response=Response.LIMIT_OPERATION,
            inhibit_hazardous_actions=report.domain in {
                Domain.SENSOR, Domain.POWER, Domain.PHYSICAL, Domain.UNKNOWN
            },
            alert_operator=True,
            require_human_review_before_resume=True,
            reason=f"Warning {report.domain.value} fault: {report.code}",
        )
    return FaultDecision(
        response=Response.CONTINUE_WITH_MONITORING,
        inhibit_hazardous_actions=False,
        alert_operator=False,
        require_human_review_before_resume=False,
        reason=f"Informational event: {report.code}",
    )


class FaultMonitor:
    """Thread-safe in-memory incident log for local software integration.

    Persistent storage, alert delivery, OS-level malware detection, network IDS,
    physical threat sensors, and hardware shutdown must be integrated separately.
    """

    def __init__(self, max_events: int = 500) -> None:
        if max_events < 1:
            raise ValueError("max_events must be at least 1")
        self._max_events = max_events
        self._events: list[dict[str, Any]] = []
        self._lock = RLock()

    def report(self, report: FaultReport) -> dict[str, Any]:
        if not report.code.strip() or not report.message.strip():
            raise ValueError("fault code and message must not be empty")
        decision = decide_response(report)
        event = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "code": report.code,
            "domain": report.domain.value,
            "severity": report.severity.value,
            "message": report.message,
            "source": report.source,
            "decision": {
                "response": decision.response.value,
                "inhibit_hazardous_actions": decision.inhibit_hazardous_actions,
                "alert_operator": decision.alert_operator,
                "require_human_review_before_resume": decision.require_human_review_before_resume,
                "reason": decision.reason,
            },
        }
        # Deliberately omit report.details to avoid accidentally persisting secrets or PII.
        with self._lock:
            self._events.append(event)
            self._events = self._events[-self._max_events:]
        return event.copy()

    def snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return [event.copy() for event in self._events]

    def clear_for_test_or_acknowledgement(self) -> None:
        """Clear in-memory events only; production audit retention needs a separate policy."""
        with self._lock:
            self._events.clear()
