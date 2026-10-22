# Fault monitor integration guide

This is a **free, local-first software component** for receiving fault reports, suggesting conservative responses, and keeping a bounded in-memory incident list. It adds no third-party dependencies.

## Scope

- Handles explicitly reported software, sensor, power, network, security, physical, environmental, data, and unknown faults.
- Critical faults recommend inhibiting hazardous actions, alerting the operator, and requiring human review before resuming.
- Security-critical events recommend isolating the affected component; physical threats require human emergency procedures.
- Sensitive `details` are intentionally excluded from the event log.

## Run tests

From the repository root, install the project's existing development test dependency if needed, then run:

```bash
python -m pytest tests/test_fault_monitor.py -q
```

## Minimal integration example

```python
from pui89_safety.fault_monitor import Domain, FaultMonitor, FaultReport, Severity

monitor = FaultMonitor()
event = monitor.report(FaultReport(
    code="CAMERA_UNAVAILABLE",
    domain=Domain.SENSOR,
    severity=Severity.CRITICAL,
    message="Camera heartbeat expired; autonomy must not rely on this camera.",
    source="perception",
))
print(event["decision"])
```

## Important limits

- This is **not** an antivirus, EDR, network intrusion-detection system, gunshot detector, person detector, or tamper sensor.
- It does not disable motors, cutters, propellers, weapons, or any physical actuator.
- A real robot must connect this decision layer to separately engineered, independent hardware safety circuits and project-specific state machines.
- Do not use log messages to store passwords, API keys, personal data, sensitive case evidence, or raw images.
- Physical violence, robbery, and suspected gunfire require human emergency procedures and local emergency services—not autonomous pursuit or confrontation.
- Every fault response must be validated for the particular robot. An abrupt power cut can itself be dangerous on a slope, with a suspended load, on a boat, or in flight.
