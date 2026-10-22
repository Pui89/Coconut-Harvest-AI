import pytest

from pui89_safety.fault_monitor import (
    Domain, FaultMonitor, FaultReport, Response, Severity, decide_response,
)


def test_critical_sensor_fault_inhibits_hazardous_actions():
    decision = decide_response(FaultReport("CAMERA_LOST", Domain.SENSOR, Severity.CRITICAL, "Camera unavailable"))
    assert decision.inhibit_hazardous_actions
    assert decision.alert_operator
    assert decision.require_human_review_before_resume
    assert decision.response is Response.STOP_MISSION_AND_ALERT


def test_critical_security_fault_isolates_component():
    decision = decide_response(FaultReport("INTEGRITY_FAIL", Domain.SECURITY, Severity.CRITICAL, "Integrity check failed"))
    assert decision.response is Response.ISOLATE_COMPROMISED_COMPONENT
    assert decision.inhibit_hazardous_actions


def test_critical_physical_threat_calls_for_human_emergency_procedure():
    decision = decide_response(FaultReport("PHYSICAL_THREAT", Domain.PHYSICAL, Severity.CRITICAL, "Operator reported threat"))
    assert decision.response is Response.HUMAN_EMERGENCY_PROCEDURE
    assert decision.require_human_review_before_resume


def test_warning_limits_operation():
    decision = decide_response(FaultReport("LOW_BATTERY", Domain.POWER, Severity.WARNING, "Battery reserve low"))
    assert decision.response is Response.LIMIT_OPERATION
    assert decision.inhibit_hazardous_actions


def test_info_keeps_monitoring():
    decision = decide_response(FaultReport("HEARTBEAT_OK", Domain.SOFTWARE, Severity.INFO, "Heartbeat received"))
    assert decision.response is Response.CONTINUE_WITH_MONITORING
    assert not decision.alert_operator


def test_monitor_records_safe_fields_but_not_details():
    monitor = FaultMonitor(max_events=2)
    event = monitor.report(FaultReport(
        "BAD_COMMAND", Domain.SECURITY, Severity.CRITICAL, "Rejected command",
        details={"password": "must-not-be-recorded"},
    ))
    assert event["decision"]["inhibit_hazardous_actions"] is True
    assert "details" not in event
    assert "password" not in str(monitor.snapshot())


def test_monitor_bounds_event_history():
    monitor = FaultMonitor(max_events=2)
    for i in range(3):
        monitor.report(FaultReport(f"EVENT_{i}", Domain.SOFTWARE, Severity.INFO, "Test event"))
    assert [e["code"] for e in monitor.snapshot()] == ["EVENT_1", "EVENT_2"]


def test_invalid_report_rejected():
    with pytest.raises(ValueError):
        FaultMonitor().report(FaultReport("", Domain.UNKNOWN, Severity.CRITICAL, "bad"))


def test_invalid_capacity_rejected():
    with pytest.raises(ValueError):
        FaultMonitor(max_events=0)
