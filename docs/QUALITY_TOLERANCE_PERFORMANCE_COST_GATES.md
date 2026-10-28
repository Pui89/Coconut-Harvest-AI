# Quality, tolerance, performance, safety and cost gates

**Status:** proposed engineering acceptance plan for a software/design prototype. Numerical limits below must be set from the actual hardware, task, risk assessment and measured capability; this document does not claim that the robot currently meets them.

## 1. Tolerance means measured uncertainty—not a guessed number

For every target, record:
- image/sensor timestamp and freshness;
- detection confidence and an explicit unknown/abstain state;
- target-position estimate plus its uncertainty and coordinate frame;
- estimated fruit size/maturity class and disagreement between sensors;
- arm reach, joint limits, tool alignment, clearance, payload and basket capacity;
- environmental conditions, calibration status and the reason for each rejected action.

Do not invent a universal centimetre tolerance. Establish a task-specific error budget from camera calibration, depth/pose estimation, arm repeatability, flex, backlash, tree movement and tool width. Measure each term and the combined worst-case or statistically justified uncertainty. If the target's uncertainty region intersects a person/animal exclusion zone, another fruit, the trunk, power lines, or an unknown obstacle, inhibit cutting.

## 2. Hard safety gates

- A separate deterministic safety layer must veto AI/agent proposals; a VLM/VLA or language model must never directly command a cutter.
- No cut unless target identity, maturity, pose, reach, stability, tool guard, clearance, basket availability, communications and operator authorization are all valid.
- Any stale, missing, conflicting or out-of-range safety input => stop motion, keep the cutter disabled, report the reason, and require deliberate recovery.
- Use a risk-assessed exclusion zone around the arm, falling fruit and lowering path. Keep workers and animals—including monkeys—outside that zone. Do not approach, chase, trap, injure or use food/bait to attract wildlife. If an animal enters or cannot be reliably excluded, stop and wait for it to leave.
- Require an accessible emergency stop, controlled restart, guarded cutter, secure fruit capture/lowering and a documented recovery procedure before any physical trial. AI-based person/animal detection alone is not a safety-rated protective device.

## 3. Performance evidence

Test separate metrics rather than one vague “accuracy” score:
- maturity classification: per-class precision/recall and confusion matrix on a held-out, source-separated dataset;
- localization: position error in stated units, median and 95th percentile, with sensor/calibration conditions;
- harvesting simulation: valid task completion, fruit damage proxy, missed/false target, dropped-object and safety-veto counts;
- robustness: repeat scenarios with occlusion, glare, shadows, wind/tree motion, partial views, stale data, sensor disagreement and low confidence;
- reliability: successful cycles, recoverable faults, unrecoverable faults, and time-to-safe-state;
- efficiency: cycle time and energy/resource use, measured alongside safety and quality.

Report sample size, dataset split, environment, software commit, units and failure cases. Do not treat synthetic scenarios as real-world performance evidence.

## 4. Tolerance/fault test matrix

At minimum, inject: small/large pose error, depth bias, camera shift, delayed frame, disconnected sensor, conflicting maturity labels, arm-limit boundary, blocked basket, communications loss, worker/animal entering the exclusion zone and emergency stop. Expected result for every unsafe or ambiguous case: no cut; safe stop; explicit failure report. Use simulation/mock tests first; physical tests require an expert-approved risk assessment and guarded test area.

## 5. Cost and maintainability gates

- Default to Python standard library, existing local tools and deterministic synthetic fixtures.
- No paid API, cloud GPU, recurring scheduled workflow, large model download or new dependency unless separately approved with licence, storage, RAM/VRAM and recurring-cost checks.
- Log cost as: hardware + sensors + fabrication + power + maintenance + consumables + software/service charges. Do not claim “low cost” until a bill of materials and lifecycle estimate exist.
- Prefer replaceable modules, documented interfaces, calibration checks, local logs and manual recovery over complex dependencies.

## 6. Release gates

1. Software unit/negative tests pass and reports match raw evidence.
2. Simulation robustness tests pass with all injected faults accounted for.
3. Dataset provenance, licences, splits and annotation quality are reviewed.
4. Independent mechanical/electrical risk assessment defines physical safeguards and numerical tolerances.
5. Controlled, instrumented hardware tests demonstrate each bounded claim.
6. Customer pilot, operator training, maintenance and incident reporting are complete before operational claims.

Passing one gate does not imply passing the next. This plan is not certification or proof of physical safety.
