# Safety State Machine and Release Gates

This is a design specification for research and simulation. It is not a certified safety system and must not be used as the sole protection for physical machinery.

## Intended states

- **IDLE** — no task is active; actuator output is not enabled.
- **CHECK_INPUTS** — validate sensor health, timestamps, coordinate frames, and data completeness.
- **PERCEIVE** — generate candidate targets and uncertainty estimates.
- **ASSESS_TARGET** — check visibility, evidence quality, and whether the target is eligible for further planning.
- **PLAN** — generate a proposed motion without executing it.
- **VALIDATE_PLAN** — check joint limits, workspace, collisions, tool envelope, and required clearances.
- **WAIT_FOR_OPERATOR** — display the plan and evidence; require explicit authorization for any future controlled execution.
- **EXECUTE** — reserved for a separately validated controller and approved test environment; disabled in the current software prototype.
- **VERIFY_OUTCOME** — compare observed outcome with the expected result and log discrepancies.
- **ABORT** — cancel the current task and return to a non-executing condition.
- **FAULT** — latch a fault until the required reset procedure is completed.

## Fail-closed transitions

Any missing, stale, malformed, or inconsistent input must prevent the system from authorizing execution. A detector confidence score alone is not a safety signal.

Examples:
- Invalid sensor status -> FAULT or ABORT.
- Missing depth when 3D position is required -> return to perception or ABORT.
- Uncertain coordinate transform -> reject the motion proposal.
- Collision, joint-limit, or workspace violation -> reject the plan.
- Planner timeout or invalid trajectory -> ABORT.
- Operator rejection -> ABORT.
- Emergency-stop signal -> controller-specific emergency-stop path and latched FAULT; software state transitions are not a substitute for a hardware emergency stop.
- Unexpected motion or failed outcome verification -> stop request and FAULT.

## Required independent checks before any hardware work

1. Validate robot kinematics and the robot description against the actual machine.
2. Verify physical and virtual joint limits, workspace boundaries, and tool geometry.
3. Validate sensor calibration and time synchronization independently.
4. Test collision checking with adversarial and boundary cases.
5. Verify emergency-stop hardware and power isolation using an approved procedure.
6. Establish guarded workspace, exclusion zone, operating procedure, and trained supervision.
7. Obtain documented risk assessment and independent review.
8. Begin with a non-cutting, low-energy, low-height test; no overhead cutting or autonomous palm climbing.
9. Keep a human able to stop the experiment and retain an auditable log.

## Safety evidence checklist

| Evidence | Status |
|---|---|
| Unit tests for invalid/missing sensor input | Must be verified against current test run |
| Invalid-plan rejection tests | Must be verified against current test run |
| Robot geometry and joint limits validated | Not established by documentation alone |
| Simulator collision scenarios passed | Not established until simulator run and logs exist |
| Hardware emergency stop verified | Not tested / no claim |
| Independent risk assessment | Not completed / no claim |
| Physical harvesting safety validated | Not demonstrated |

## Boundary

The current project is a software and simulation-first research prototype. The planning output is a proposal, not an actuator command. Do not connect this prototype directly to cutters, motors, climbing mechanisms, or manipulators. A passing software test suite does not establish safe physical operation.
