# Coconut Harvest AI — Failure and Security Response Matrix

## Purpose and status

This document records conservative failure-response requirements for design, simulation, and future verification. It is **not** proof that these responses are implemented in hardware or validated in the field. Follow applicable law, workplace procedures, and qualified safety/security guidance during any real deployment.

## Response matrix

| Failure or threat | Required safe response | Current evidence boundary |
|---|---|---|
| AI model crashes, returns invalid output, or confidence is missing | Reject the candidate; keep cutting disabled; record the fault; require operator review before restart. | Planning agent has conservative input checks; model-crash detection and runtime interlocks are not demonstrated. |
| Camera, depth, LiDAR, or calibration is missing/stale | Stop target approach and cutting proposal; mark position/reachability unknown; request inspection/recalibration. | Design requirement; not hardware-tested. |
| Arm, cutter, gripper, platform, or reachability status is uncertain | No movement/cutting proposal; require a verified safe state and human inspection. | Agent requires explicit reachability input; physical interlocks are not implemented/validated. |
| Power loss, low battery, overheating, or motor fault | Disable cutting; use hardware-defined safe stop/brake behavior; preserve state if possible; inspect before restart. | Software-only guidance; hardware response must be designed and tested by qualified engineers. |
| Wi-Fi, remote operator, or control heartbeat is lost | Do not continue an autonomous harvest; stop using a validated safe procedure and wait for authorized recovery. | No physical robot or remote-control fail-safe has been validated. |
| Malformed images, corrupted annotations, or untrusted model files | Reject invalid inputs; do not load untrusted weights; retain source/hash records; require review. | Data provenance tools are being developed; this is not a complete malware scanner. |
| Cyberattack, unauthorized login, malware, or suspicious command | Isolate affected computer/network; disable remote commands; preserve logs; rotate credentials from a trusted device; restore only from a verified clean backup. | Security response policy only; no penetration test or secure hardware controller is demonstrated. |
| Theft, tampering, impact, fire, or other physical damage | Do not operate; isolate energy sources only if safe and authorized; secure the area and arrange inspection. | Physical protection and incident response require real-world engineering and local procedures. |
| Person enters the work zone or emergency stop is activated | Cutting must be inhibited and motion stopped through an independent, validated safety system. | Safety requirement; no certified safety controller or real-person sensing is claimed. |

## Common principles

1. **Fail closed:** missing, stale, contradictory, or invalid inputs must not be interpreted as proof of safety or as a positive/negative classification.
2. **Human oversight:** uncertain or high-impact decisions require authorized human review.
3. **Separate safety controls:** software checks are not substitutes for independent, appropriately engineered emergency stops, brakes, interlocks, and safe power isolation.
4. **Security incidents:** do not retaliate or execute untrusted instructions. Isolate affected systems where safe, preserve logs and hashes, use trusted recovery media/backups, and follow the organization's incident process.
5. **Evidence:** each test record should include scenario ID, software version/commit, environment, input, expected response, actual response, pass/fail, and reviewer.
6. **No invented validation:** mark items as `REQUIREMENT`, `SIMULATED`, `TESTED`, or `FIELD-VALIDATED` only when the evidence supports that status.

## Verification plan

- Convert each applicable row into a repeatable unit or simulation test.
- Test normal, boundary, malformed-input, failure-injection, recovery, and repeated-run behavior.
- Require safe-stop and recovery tests to pass before considering hardware integration.
- Do not describe the project as physically safe, certified, or operational based only on software tests.

