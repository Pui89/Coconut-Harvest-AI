# Advanced Generative Simulation and Embodied Action Models

This layer documents three external Hugging Face model candidates for the coconut-harvest embodied-AI stack. Model weights are not bundled in this repository.

## 1. LTX-2.5-Diffusers

**Source:** Lightricks/LTX-2.5-Diffusers

Use LTX-2.5 as an offline video/audio world-simulation and dataset-augmentation candidate. Generate orchard scenes with wind, leaf motion, rain, fog, low light, occlusion, camera obstruction, tool-contact events and recovery scenarios.

It is **not** a runtime robot controller. Its gated access, community licence, training-data terms and resource requirements remain subject to review.

## 2. NVIDIA GR00T N1.7 3B

**Source:** nvidia/GR00T-N1.7-3B

Use GR00T as an embodied-action policy candidate for imitation learning, skill transfer and simulation-to-real research. Candidate skills include approach, grasp, cut, retract and verify.

GR00T outputs proposals that must pass the deterministic planner and safety gate before any execution. Its exact upstream revision, complete lineage, licence, dependencies and origin/control evidence remain pending review.

## 3. Google Gemma 4 31B IT

**Source:** google/gemma-4-31B-it — [Hugging Face](https://huggingface.co/google/gemma-4-31B-it)

Gemma 4 31B IT is a high-level multimodal reasoning candidate for orchard images and task context. It may analyze coconut targets, ripeness/quality cues, branch and workspace risk, occlusion, and uncertainty before a harvest candidate is sent to the deterministic planner.

The repository includes a runtime adapter at \`src/coconut_harvest_robot/gemma4.py\`. The model weights are not committed to GitHub. The model's large resource requirement, exact immutable revision, full weight/data lineage and licence conditions must be reviewed before any download or evaluation.

Gemma is **advisory only**. It never sends motor, cutter, gripper, or arm commands. Any proposed harvest decision must pass target verification, workspace/collision checks, human-exclusion checks, joint/force/torque limits, confidence gating, and the emergency-stop path.

## Combined architecture

\`\`\`
RGB / RGB-D / LiDAR / IMU
        |
        v
Future perception (not selected) + SAM3 + tracking
        |
        v
3D tree / branch / fruit world model
        |
        +--> Gemma-4-31B-it reasoning
        |        |
        |        +--> active perception
        |        +--> uncertainty / target verification
        |
        +--> future prediction
        |
        v
GR00T N1.7
(candidate actions only)
        |
        v
Deterministic safety gate
        |
        +--> workspace / collision
        +--> human exclusion
        +--> joint limits
        +--> velocity / force / torque
        +--> confidence / uncertainty
        +--> emergency stop
        |
        v
ROS2 / MoveIt2 / RRT*
        |
        v
Arm + gripper + cutting tool
        |
        v
Action verification -> memory update
\`\`\`

## Synthetic-data loop

\`\`\`
Isaac Sim / Isaac Lab
       +
LTX-2.5
       |
       v
Rare-event orchard video/audio
       |
       v
Perception + reasoning + action datasets
       |
       v
LeRobot training/evaluation
       |
       v
Simulation validation -> controlled real-robot validation
\`\`\`

## Safety invariant

Reasoning decides **what should happen**. The planner decides **how to execute it**. The deterministic safety controller decides **whether execution is allowed**.

No generative, VLM or action foundation model may bypass collision checking, workspace limits, human exclusion, force/torque limits or the physical emergency stop.
