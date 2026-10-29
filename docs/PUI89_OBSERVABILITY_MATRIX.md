# PUI89 Observability Matrix — coconut-harvest

**Purpose:** define consistent, evidence-led observation from software to system, AI model, workflow stages, and physical hardware when actually connected. This is a monitoring plan, not proof of robot validation.

## Layers to observe

| Layer | What to record | Example signals | Evidence boundary |
|---|---|---|---|
| Software | Build, imports, tests, exceptions, dependency versions | commit SHA, test counts, failure code, duration | CI proves only the code paths it actually runs |
| Hardware and sensors | Device connection, sensor health, calibration, timestamps, power/temperature where available, emergency stop | connected/disconnected, stale frame, calibration ID, fault | Mark NOT_CONNECTED until a real device/test rig supplies evidence |
| System | CPU/RAM/disk, process health, queue depth, timeouts, communications | resource snapshot, timeout count, restart count | Hosted CI is not a deployed robot or the user's laptop |
| AI model | Model identifier/version/hash, licence, runtime, input quality, uncertainty, abstention | loaded/not loaded, latency, UNKNOWN, missing input | Model and benchmark not run must remain NOT_RUN |
| Workflow steps | Ordered stage, input/output reference, duration, outcome, failure reason | validate → observe → assess → propose → review → close | Record each step separately; do not imply unrun stages passed |
| Safety and human review | Safe hold, manual takeover, review record, audit completeness | stop reason, reviewer reference, timestamp | Software policy tests are not certified physical safety |

## Project-specific workflow

1. Validate image/dataset provenance and label integrity. 2. Check image quality and maturity-stage uncertainty. 3. Propose detection/segmentation output with confidence and UNKNOWN/abstain support. 4. Record tree/fruit geometry only when measured inputs exist. 5. Propose cutting/capture/basket actions in simulation only. 6. Require human approval and independent safety review before any hardware experiment. Height coverage up to 30 m, maturity accuracy, arm reach, cutting reliability and worker/animal safety are not established without evidence.

## Status vocabulary

- `PASS` / `FAIL`: a named check actually ran with a timestamp and evidence reference.
- `NOT_RUN`: a defined check has not been run.
- `NOT_CONNECTED`: the required hardware or external component is not connected.
- `UNKNOWN`: state cannot be determined reliably.
- `BLOCKED`: a prerequisite, licence, calibration, dataset permission or review is missing.

Unknown must never silently become pass.

## Evidence record minimum

Record UTC timestamp, project and commit, layer/check ID, status, duration if measured, concise failure code, evidence/artifact reference, and environment/model/sensor version where relevant. Minimise sensitive data in CI logs. Keep raw images, location trails, personal data and sensitive operational evidence out of public logs.

## Staged acceptance sequence

1. Software syntax and unit tests.
2. Runtime resource and timeout checks in the actual target environment.
3. Model/licence preflight and inference checks only when a model is intentionally installed.
4. Sensor connection, freshness, calibration and fault injection on approved test equipment.
5. Repeatable simulation with missing, stale, conflicting and malformed inputs.
6. Controlled hardware tests only after simulation and independent safety review.
7. Independent evaluation and authorised pilot before operational claims.

## Free-first implementation boundary

The starter report generator uses Python's standard library and makes no network calls, installs no packages, downloads no models, reads no sensors and issues no actuator commands. It emits an honest baseline; it does not collect live telemetry. Do not add scheduled jobs by default.

## Evidence boundary

A successful software test is not proof of physical performance. Publish measured results only with reproducible scenarios, configuration, sample counts and measurement conditions. Keep proposed features separate from demonstrated capabilities.
