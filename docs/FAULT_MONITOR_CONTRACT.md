# PUI89 Fault Monitor Contract

This document defines the shared software interface and expected behaviour for the local-first fault monitor used by PUI89 projects.

## Scope and limitations

The fault monitor records conditions explicitly reported by application code and suggests a conservative response. It is not a hardware safety controller, antivirus, intrusion-detection system, chemical detector, or physical threat sensor. It does not independently detect faults, stop motors, isolate networks, or deliver alerts. Those capabilities require separate integrations and verification.

Do not place passwords, access tokens, private imagery, unnecessary personal data, or other sensitive payloads in fault messages or metadata.

## Public interface

The implementation exposes:

- `Severity`: `INFO`, `WARNING`, and `CRITICAL`.
- `Domain`: `SOFTWARE`, `SENSOR`, `POWER`, `NETWORK`, `SECURITY`, `PHYSICAL`, `ENVIRONMENT`, `DATA`, and `UNKNOWN`.
- `Response`: `CONTINUE_WITH_MONITORING`, `LIMIT_OPERATION`, `STOP_MISSION_AND_ALERT`, `ISOLATE_COMPROMISED_COMPONENT`, `HUMAN_EMERGENCY_PROCEDURE`, and `MANUAL_RECOVERY`.
- `FaultReport`: a fault code, domain, severity, message, optional source, and optional details.
- `FaultDecision`: suggested response plus flags for inhibiting hazardous actions, alerting an operator, and requiring human review before resuming.
- `decide_response(report)`: a deterministic response recommendation.
- `FaultMonitor(max_events=500)`: a thread-safe, bounded in-memory event log with `report`, `snapshot`, and `clear_for_test_or_acknowledgement`.

## Response policy

| Report severity | Expected recommendation |
| --- | --- |
| `INFO` | Continue with monitoring; no alert or hazardous-action inhibition by default |
| `WARNING` | Limit operation, alert the operator, and require human review before resuming; inhibit hazardous actions for sensor, power, physical, or unknown domains |
| `CRITICAL` | Inhibit hazardous actions, alert the operator, and require human review before resuming; use a domain-specific conservative response where defined |

Critical security faults recommend isolating the compromised component; critical physical faults recommend a human emergency procedure; critical unknown faults recommend manual recovery. Other critical faults recommend stopping the mission and alerting the operator.

These are software recommendations only. Integrating systems must enforce any required safe state independently and must not treat a returned recommendation as proof that hardware has stopped.

## Input validation and data handling

Implementations must reject invalid report types, blank required text, invalid enum values, and overlong fields. Event capacity must be a positive integer; booleans are not valid capacities. The event history must remain bounded. Returned events and snapshots must be defensive copies so callers cannot mutate internal state. Arbitrary `details` must not be copied into persisted event records because they may contain secrets or personal data.

Events include a UTC timestamp, fault code, domain, severity, message, source, and the structured decision. The monitor is in-memory only; persistence, retention policy, alert delivery, and access controls are separate responsibilities.

## Required regression coverage

Each project must test:

1. Critical faults inhibit hazardous actions, alert the operator, and require human review.
2. Domain-specific critical responses match the policy above.
3. Warnings limit operation and apply domain-specific inhibition.
4. Informational events use the monitoring response.
5. Invalid, blank, and overlong inputs are rejected.
6. Invalid event capacities are rejected, including booleans.
7. Sensitive `details` are excluded from event output.
8. Event history is bounded.
9. Returned events and snapshots cannot mutate internal state.
10. Representative software, sensor, power, network, security, physical, environmental, data, and unknown critical faults never recommend continuing hazardous autonomy.

## Change control

Keep the public names, enum values, event keys, and policy aligned across the three repositories. Any intentional behavioural change must update this contract and the regression tests together. A passing unit-test suite does not validate physical robot safety or real-world performance.
