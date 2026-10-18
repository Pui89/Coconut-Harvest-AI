# End-to-end AI application + robot workflow

## Purpose

This guide documents a reproducible, simulation-only workflow that connects target evidence to target selection, conservative preflight checks, a simulated task sequence, and an auditable JSON report. It is intended to strengthen the research prototype and make the AI application/robot boundary explicit.

## Run it

From the repository root with Python 3.10+ (the runner uses only the Python standard library):

```bash
python -m apps.pui89_app.run_robot_workflow
```

Use an alternate JSON input or save the report:

```bash
python -m apps.pui89_app.run_robot_workflow --input examples/end_to_end_robot_workflow.example.json --output workflow-report.json
```

The example file is intentionally illustrative. It is not a labelled dataset, an actual camera output, a calibrated robot measurement, or a benchmark result.

## Pipeline

1. **Image perception:** the optional local detector can produce pixel bounding boxes and confidence scores from a user-supplied, trusted local model. The runner does not itself load a model or infer detections from images.
2. **Tracking:** the workflow accepts track age as supplied evidence and rejects unstable tracks. It does not implement multi-object tracking across video frames.
3. **3D localization:** metric coordinates, uncertainty, timestamp, reachability and obstacle clearance are inputs from a future calibrated localization/perception component. A 2D box is never converted into a guessed 3D position.
4. **Target planning:** valid candidates are ranked deterministically by confidence, then distance. Candidates missing required evidence are rejected with reason codes.
5. **Human approval:** no simulated task sequence is emitted until approval is present in the input. Approval only allows the software simulation to continue; it is not physical authorization.
6. **Robot task sequence:** the adapter emits approach, tool-sequence, and retract *preview* steps. These are task-sequence records, not physics simulation, inverse kinematics, or validated collision-free trajectories.
7. **Safety and recovery:** emergency-stop input, absent targets, stale observations, invalid boxes, missing 3D position, uncertain localization, poor clearance, and unconfirmed reachability cause a safe hold/rejection rather than guessed values.
8. **Audit report:** JSON contains status, state history, selected target, rejected-candidate reasons, planned steps and explicit no-hardware/no-harvest-verification fields.

## State machine

```text
IDLE
  ├─ no target / emergency stop / invalid evidence ─> SAFE_HOLD
  └─ valid candidate ─> TARGET_SELECTED
                         ├─ no human approval ─> SAFE_HOLD / AWAITING_HUMAN_APPROVAL
                         └─ human approval ─> PLAN_VALIDATED
                                               └─ EXECUTING_SIMULATION
                                                   └─ COMPLETED_SIMULATION
```

## Tests

```bash
python -m pip install pytest
python -m pytest -q apps/pui89_app/test_robot_workflow.py
```

CI runs these tests on relevant pull requests. Passing tests establish the behaviour of these software cases only. They do not establish detector accuracy, localization accuracy, collision-free motion, physical safety or successful harvesting.

## Integration path

- **Now:** local app, optional user-supplied detector adapter, JSON task workflow, conservative evidence gates, tests.
- **Next:** connect detector output to stable video tracking; connect a calibrated RGB-D pipeline with uncertainty estimates; define a robot-frame transform and robot-specific reachability service.
- **Simulation stage:** integrate a named robot model, joints, tool geometry, orchard/branch obstacles and a physics simulator; compare planned vs. executed trajectories and inject faults.
- **Hardware stage:** only after independent collision checking, risk assessment, emergency-stop/interlock validation and supervised testing. Keep the physical actuator adapter disabled until those gates are independently approved.

## Evidence boundary

| Capability | Status of this workflow |
|---|---|
| Deterministic target selection from supplied candidates | Implemented and unit-tested |
| Reject missing/invalid/stale inputs | Implemented and unit-tested |
| Require explicit human approval before emitting simulated steps | Implemented and unit-tested |
| JSON audit report and explicit no-actuator flag | Implemented and unit-tested |
| Detect coconuts directly from every uploaded image | Not established; optional model adapter needs a suitable trained model and evaluation |
| Track targets across real video | Not implemented in this workflow |
| Calibrated metric 3D localization | External evidence input only; not implemented here |
| Robot kinematics and physics/collision simulation | Not implemented by this workflow |
| ROS 2 hardware execution or physical harvesting | Not implemented; no actuator commands are sent |
| Commercial readiness or safety certification | Not established |

The workflow is a practical integration step for research, not a claim that an autonomous harvesting robot is ready for real-world or commercial operation.
