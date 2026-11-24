# Advanced Generative Simulation and Embodied Action Models

This layer documents three external Hugging Face model candidates for the coconut-harvest embodied-AI stack. Model weights are not bundled in this repository.

## 1. LTX-2.5-Diffusers

**Source:** Lightricks/LTX-2.5-Diffusers

Use LTX-2.5 as an offline video/audio world-simulation and dataset-augmentation component. Generate orchard scenes with wind, leaf motion, rain, fog, low light, occlusion, camera obstruction, tool-contact events and recovery scenarios.

It is **not** a runtime robot controller. Its exact model and component licences, gated-access terms, upstream revisions, weight hashes and training-data rights remain subject to review before any download or use.

## 2. NVIDIA GR00T N1.7 3B

**Source:** nvidia/GR00T-N1.7-3B

Use GR00T as an embodied-action policy candidate for imitation learning, skill transfer and simulation-to-real experiments. Candidate skills include approach, grasp, cut, retract and verify.

GR00T outputs proposals that must pass the deterministic planner and safety gate before execution. Its full base-model, dependency, dataset and checkpoint lineage must be verified before admission.

## 3. Google Gemma 4 31B IT

**Source:** google/gemma-4-31B-it — [Hugging Face](https://huggingface.co/google/gemma-4-31B-it)

Gemma 4 31B IT is the high-level multimodal reasoning layer for orchard images and task context. It can analyze coconut targets, ripeness/quality cues, branch and workspace risk, occlusion, and uncertainty before a harvest candidate is sent to the deterministic planner.

The repository includes a runtime adapter at `src/coconut_harvest_robot/gemma4.py`. Model weights are not committed to GitHub. Any download must remain disabled until explicit approval, exact immutable revision, weight hash, model/data rights and resource requirements are reviewed. Transformers and vLLM are supported by the model card.

Gemma is **advisory only**. It never sends motor, cutter, gripper, or arm commands. Any proposed harvest decision must pass target verification, workspace/collision checks, human-exclusion checks, joint/force/torque limits, confidence gating, and the emergency-stop path.

## Combined architecture

```
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
```

## Synthetic-data loop

```
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
```

## Safety invariant

Reasoning decides **what should happen**. The planner decides **how to execute it**. The deterministic safety controller decides **whether execution is allowed**.

No generative, VLM or action foundation model may bypass collision checking, workspace limits, human exclusion, force/torque limits or the physical emergency stop.
