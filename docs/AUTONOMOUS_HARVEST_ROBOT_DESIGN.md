# Autonomous Coconut Harvest Robot — Engineering Design

> **Status: proposed engineering design, not a completed physical robot.** This document describes a credible development path for a robot intended to reduce the need for a person to climb a coconut palm. The repository currently contains research prototypes and concept assets; it does not demonstrate autonomous field harvesting.

## 1. What the robot should do

The goal is to move the risky work away from a human climber. A supervised robot would:

1. Move to a palm from the ground and establish a stable working position.
2. Capture RGB images and, where available, depth data of the crown and coconut bunches.
3. Propose candidate bunches and report confidence, visibility, and unknown conditions.
4. Estimate 3D target locations only when camera calibration and depth quality are valid.
5. Check whether the target is reachable and whether the proposed tool path has verified clearance.
6. Present a harvest proposal for operator approval.
7. In a future validated hardware system, position a purpose-built cutting/gripping tool, secure the bunch or fruit, cut only after all interlocks pass, and control the fall into a designated collection area.
8. Confirm the result, record failures, and return to a safe state.

**The software in this repository does not currently perform all these steps.** In particular, coconut detection from image pixels, mature-fruit classification, calibrated 3D localization, validated collision-free manipulation, cutting, and physical collection require further implementation and testing.

## 2. Choose a mechanical approach

### Preferred research route: ground-based mobile platform with a telescopic mast or lift

A ground-based platform avoids relying on a robot to climb a flexible, irregular palm trunk. It could carry a camera mast and, if the reach and stability calculations support it, a lightweight manipulator and specialized tool. A high-reach platform has serious overturning, wind, terrain, and falling-object hazards; it must not be built or operated without a qualified mechanical/safety review.

### Alternative: trunk-climbing robot

A trunk-climber could reduce the required arm reach, but gripping force, bark variability, moisture, trunk taper, obstacles, dynamic stability, and safe recovery are difficult problems. Treat this as a separate research branch until a tethered low-height prototype passes mechanical tests.

### Do not assume a drone can harvest

A drone may help inspect the canopy, but carrying and safely operating a cutting tool near branches and people creates substantial payload, endurance, and safety challenges. An inspection drone should not be treated as a harvesting solution without separate engineering validation.

## 3. System architecture

```text
RGB camera + optional calibrated depth / LiDAR
                    |
                    v
        Sensor-health and calibration checks
                    |
                    v
       Coconut / bunch detection proposal
                    |
                    v
  Confidence + occlusion + unknown-case handling
                    |
                    v
       3D localization (only if valid depth)
                    |
                    v
      Reachability and workspace assessment
                    |
                    v
       Motion planning + collision checking
                    |
                    v
    Independent safety supervisor / interlocks
                    |
                    v
       Human approval during development
                    |
                    v
    Authorized controller (future hardware only)
                    |
                    v
      Outcome verification + audit log
```

The vision model proposes targets; it does not authorize cutting. A separate deterministic safety supervisor must be able to reject a proposal regardless of the model's confidence.

## 4. Harvest sequence and safe states

Use explicit states rather than a single “autonomous” switch:

- `IDLE`: no motion request.
- `OBSERVE`: capture data and check sensor health.
- `TARGET_PROPOSED`: one or more candidates are available for review.
- `NEEDS_REVIEW`: confidence, maturity, localization, or context is insufficient.
- `PLAN_REJECTED`: target unreachable, clearance invalid, or required evidence missing.
- `APPROVED_NOT_EXECUTED`: software checks passed, but no physical motion has been commanded.
- `EXECUTION_ENABLED`: a future, separately validated controller may act only when all hardware interlocks and operator authorization are present.
- `SAFE_HOLD`: stop requesting motion when a sensor fails, data are stale, communications are lost, or a safety check fails.
- `FAULT`: require diagnosis and deliberate reset.

The current prototype should remain in software-only proposal/report mode. Never connect its output directly to motors, a cutter, or a manipulator.

## 5. Required subsystems

| Subsystem | Purpose | Evidence needed before field use |
|---|---|---|
| RGB perception | Propose coconuts/bunches and visible attributes | Labelled orchard dataset, held-out precision/recall, per-condition results |
| Depth / 3D localization | Estimate target position | Calibration procedure, localization error and invalid-depth tests |
| Maturity assessment | Avoid harvesting the wrong fruit | Ground-truth labels and agreement with qualified agricultural assessment |
| Scene / tracking model | Maintain target identity over time | Tracking metrics across occlusion and camera movement |
| Mobility and stabilization | Position the platform safely | Terrain, slope, stability, braking and weather limits assessed by qualified engineers |
| Manipulator and end-effector | Reach, secure and cut the target | Kinematics, payload, tool design, force limits and supervised bench tests |
| Collision and workspace safety | Reject hazardous motion | Independent geometry checks, adversarial tests and documented safety review |
| Collection and fall-zone control | Reduce risk from falling fruit | Containment design, exclusion-zone procedures and failure tests |
| Operator interface and audit | Review proposals and record outcomes | Clear status, emergency-stop procedure, timestamped logs and traceable test results |

## 6. Simulation-first implementation plan

### Stage A — verify the existing software

- Run the current test suite and end-to-end synthetic demo.
- Record the exact command, software versions, test results, and limitations.
- Do not label synthetic fixtures as real orchard performance.

### Stage B — create a reproducible orchard scene

- Model a palm trunk, ground plane, target bunches, camera frames, and a simple robot envelope.
- Make trunk dimensions, target heights, camera pose, and sensor noise configurable.
- Check coordinate frames, units, and joint limits before attempting motion planning.

### Stage C — evaluate perception with real images

- Use appropriately licensed images and document their provenance.
- Create annotations and a fixed train/validation/test split before tuning a detector.
- Report metrics only after running the actual model on the held-out set.
- A photo alone cannot provide calibrated target depth or prove reachability.

### Stage D — test planning without actuators

- Convert a reviewed target into a candidate approach pose.
- Check workspace, joint limits, self-collision, environmental collision, and uncertainty.
- Reject plans when the scene is incomplete or the collision checker cannot make a valid determination.
- Save a JSON report; do not issue motor or cutter commands.

### Stage E — independent safety and hardware review

Only after simulation and bench testing, a qualified team can assess a non-cutting, tethered, low-height prototype. Physical trials require appropriate guarding, an exclusion zone, emergency-stop verification, a risk assessment, and trained supervision. Cutting and field harvesting are separate release gates.

## 7. Free and local development policy

The software workflow is designed to start with local tools, synthetic data, and openly licensed datasets. No paid API, subscription, or cloud GPU is required for the design work described here. Downloading large models or installing robotics simulators may require substantial disk space and hardware; check licenses and system requirements before downloading. This document does not install software or incur charges.

## 8. Minimum evidence for the claim “harvests instead of a human”

Do not make that claim until a controlled, documented trial measures at least:

- successful bunch/fruit harvests divided by attempted harvests;
- missed targets and incorrect cuts;
- fruit damage and collection success;
- cycle time per target compared with a defined human baseline;
- localization and tool-position error;
- emergency stops, unsafe proposals, and near misses;
- performance across different palm heights, lighting, weather, occlusion, and terrain;
- maintenance, setup time, and operating constraints.

Report sample size, test conditions, failures, and confidence intervals where appropriate. A concept image, successful software test, or simulated trajectory is not proof of field harvesting.

## 9. Current status

This file is a design and validation plan. It does not assert that a physical robot has been built, that a coconut-specific detector has been validated, or that a robot has harvested coconuts autonomously. The next practical step is to verify the existing simulation and software tests, then add one measurable capability at a time.
