# Physical AI stack — Coconut Harvest AI

## Planned architecture

1. **Vision-language model (VLM):** optionally describe an uploaded/recorded image and propose candidate objects or ambiguities. It must not replace the validated detector or maturity classifier.
2. **Task/action LLM:** translate an approved goal such as “inspect the selected mature-green coconut” into a short, structured high-level plan.
3. **Perception and geometry:** detector/classifier, image coordinates, depth/range estimates and uncertainty.
4. **World state:** track fruit IDs, maturity estimates, arm/platform state, obstacles and timestamps. Keep estimates separate from ground truth.
5. **Task planner and verifier:** check reachability, target identity, tool availability and preconditions before a step is proposed.
6. **Autonomy supervisor:** retain the existing supervisor as an independent gate. The LLM cannot bypass it.
7. **Evidence and evaluation:** log model/version, input reference, proposed plan, rejected steps and measured detection/planning metrics.

## Safe starter action vocabulary

Use high-level allowlisted actions such as `inspect_target`, `estimate_reachability`, `request_human_confirmation`, `plan_approach`, and `verify_capture`. Do not expose direct cutter, motor, or arm commands to an LLM.

## Current implementation status

- `pui89_autonomy/llm_interfaces.py` provides dependency-free data contracts and validators for vision findings and action plans.
- It does **not** load or run a VLM/LLM, connect to an API, detect coconuts, or control a robot.
- Keep the current local-image workflow; this does not add a live-camera workflow.
- No harvest operation should be described as validated until physical tests establish reach, stability, cutting, capture and human-safety performance.

## Next steps

1. Establish a tested local vision baseline on correctly licensed, leakage-safe data.
2. Test structured plans against fixed scenarios and invalid/ambiguous observations.
3. Add a local model adapter only after checking model license, hardware fit, download size and reproducible evaluation.
4. Keep all real hardware actions disabled until independent engineering safety validation.
