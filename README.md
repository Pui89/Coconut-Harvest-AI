# Coconut Harvest AI Application

> **End-to-end AI application + agricultural robot research prototype.** The workflow links optional local image detection, target-evidence checks, conservative target selection, a human-approved simulated task sequence, and an auditable JSON report. It does not currently prove calibrated 3D localization, physics-validated motion, physical harvesting, or commercial readiness.

## Run the end-to-end workflow now

Python 3.10+; this workflow runner uses the standard library and needs no model download, paid API, cloud service, or robot hardware.

```bash
python -m apps.pui89_app.run_robot_workflow
```

The report is printed as JSON. The example is synthetic/illustrative, not a real camera observation or benchmark. To save a report:

```bash
python -m apps.pui89_app.run_robot_workflow --input examples/end_to_end_robot_workflow.example.json --output workflow-report.json
```

**What this demonstrates:** candidate ranking, explicit rejection reasons, stale/invalid evidence handling, a human-approval gate, simulation-only approach/tool/retract task records, an audit report, plus separately testable IoU tracking and calibrated RGB-D box-to-camera-frame localization utilities. **What it does not demonstrate:** validated coconut detection from the example JSON, production-grade video tracking, calibrated localization in the robot/world frame, robot kinematics, physics simulation, independent collision checking, physical actuation, or a successful harvest. The RGB-D utility requires aligned depth and known intrinsics; the IoU tracker is a simple baseline, not a benchmarked tracker.

- [End-to-end workflow guide and tests](docs/END_TO_END_ROBOT_WORKFLOW.md)
- [Workflow implementation](apps/pui89_app/robot_workflow.py)
- [Runner](apps/pui89_app/run_robot_workflow.py)
- [Illustrative input](examples/end_to_end_robot_workflow.example.json)
- [Workflow tests](apps/pui89_app/test_robot_workflow.py)
- [RGB-D camera-frame localization utility](apps/pui89_app/rgbd_localization.py)
- [IoU target tracker baseline](apps/pui89_app/iou_tracker.py)
- [Spatial localization and tracking tests](apps/pui89_app/test_spatial_tracking.py)
- [AI application setup and optional local detector](apps/pui89_app/README.md)

---

## Free local Hugging Face model plan

This repository's recommended local model, intended tasks, licence checks, setup notes, and no-surprise-billing rules are documented in **[HUGGINGFACE_LOCAL_MODELS.md](docs/HUGGINGFACE_LOCAL_MODELS.md)**.

**Cost boundary:** the plan uses downloaded local weights only; it does not require paid Hugging Face inference, cloud GPUs, paid notebooks, or a subscription. Model integration and performance must be verified by running tests locally.


## Local development on an RTX 3050 laptop

The hardware-aware, zero-cost-first plan is in [LOCAL_EXPERIMENT_PLAN_RTX3050.md](docs/LOCAL_EXPERIMENT_PLAN_RTX3050.md). A read-only environment checker is available at [scripts/check_local_environment.py](scripts/check_local_environment.py); it does not install packages, download models, use the network, or change system settings. The plan is tailored to a reported RTX 3050 Laptop GPU with 4 GB VRAM and 16 GB system RAM. It distinguishes the existing synthetic prototype from future model experiments and measured results.

## AI Application Overview

## Try the Interactive AI Application Example

Want to see an example instead of only reading about the concept? The repository includes a small Streamlit demo where you can upload an orchard photo for display, adjust example sensor/coconut evidence, run the decision-support rules, and download a JSON report.

**[Open the web demo source and setup instructions](apps/pui89_app/README.md)** · [View the interactive demo code](apps/pui89_app/web_demo.py)

Run it locally from the repository root:

```bash
python -m pip install -r apps/pui89_app/requirements.txt
streamlit run apps/pui89_app/web_demo.py
```

**Demo limitation:** by default, the uploaded photograph is displayed for context but is not automatically analysed. An optional local detector can be configured using a trusted, existing `.pt` model file whose class labels include coconut; see [local detector setup](apps/pui89_app/README.md#optional-local-coconut-detector). The default manual-evidence workflow remains illustrative and is not a real-world harvesting result or robot control system. No detector accuracy is claimed without evaluation on labelled held-out images.


## How the AI Application Works

The **AI application** is the software layer that runs on a computer. It takes orchard images and, when available, depth and robot-state data; checks input quality; analyses candidate coconuts; records uncertainty; and produces a reviewable harvest-plan proposal and JSON audit report.

```text
Orchard image + optional depth / robot-state data
                    |
                    v
         Input quality and sensor checks
                    |
                    v
          AI vision / target proposals
                    |
                    v
      Spatial and temporal evidence (3D/4D)
                    |
                    v
 Harvestability + uncertainty + missing-data checks
                    |
                    v
            Candidate plan proposal
                    |
                    v
       Safety checks, review and JSON report
```

**AI application concept image**

![AI application concept: coconut orchard perception and planning](docs/images/coconut-harvest-ai-demo.svg)

![AI application 3D/4D concept visualization](docs/images/coconut-harvest-ai-4d-concept.svg)

**Real-world image used as application context**

![Real coconut fruits growing on a palm](https://commons.wikimedia.org/wiki/Special:FilePath/Fruiting_Coconut_Palm_Canopy.jpg?width=1100)

*Photograph by Paul The Writer, shared under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). [Original image and licence](https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg). This is a real-world visual reference, not an image processed or evaluated by the current prototype.*

**What it does and does not prove:** the repository provides a simulation-first software prototype and concept visualizations. Coconut-specific detection accuracy, ripeness assessment, and real-time 3D/4D tracking require representative labelled data and measured validation. The application proposes and reports; the documented demo does not directly control physical actuators.

---

## How the AI Robot Works

The **AI robot** is the proposed physical or simulated machine that could use the application's proposals. In a future validated system, cameras and other calibrated sensors observe the tree and workspace; perception estimates target locations; a planner proposes a movement; and an independent safety layer checks that movement before an authorized controller could execute it.

```text
RGB / depth / optional LiDAR + robot-state sensors
                    |
                    v
        Perception and target tracking
                    |
                    v
             3D / 4D scene model
                    |
                    v
        Harvest task / motion proposal
                    |
                    v
 Independent collision and safety validation
                    |
                    v
      Authorized controller (future stage)
                    |
                    v
        Verify outcome and record evidence
```

![Existing coconut harvesting robot concept illustration](docs/images/coconut_harvest_robot_photo.svg)

![3D/4D coconut harvesting robot concept](docs/coconut_harvest_robot_3d_4d_concept.svg)

**Real-world image of the harvesting task**

![Real photograph of a person harvesting coconuts from a palm](https://commons.wikimedia.org/wiki/Special:FilePath/Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG?width=1100)

*Photograph by Rudolph A. Furtado, shared under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). [Original image and licence](https://commons.wikimedia.org/wiki/File:Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG). This shows human harvesting for real-world context; it is not a robot trial or proof of autonomous harvesting.*

**Current robot status and safety boundary:** the repository includes software prototypes, simulation assets and robot concept/model files. It does not establish that a physical robot can safely climb a palm, cut or grasp coconuts, avoid every collision, or harvest autonomously in an orchard. Do not connect this prototype directly to physical motors, cutters or manipulators. Any future hardware work needs calibrated sensors, independent collision/workspace validation, emergency-stop testing, supervised low-risk trials and a documented safety review.

---

## How the Coconut Harvest AI Application Works

Coconut Harvest AI is a **simulation-first research prototype** for exploring how computer vision, spatial reasoning, harvestability assessment, and safety checks could support coconut harvesting. The workflow below explains the intended system and distinguishes existing prototype behavior from work that still needs real-world validation.

### End-to-end workflow

```text
Orchard RGB image + optional depth / LiDAR / robot-state data
                         |
                         v
              1. Input and sensor checks
       Check data quality, health, and time alignment
                         |
                         v
              2. Perception proposal
       Extract visual features and identify candidate targets
       Coconut-specific detection requires validated model/data
                         |
                         v
              3. Spatial and temporal reasoning
       Associate depth with targets; estimate 3D position
       Track target state over time when suitable data are available
                         |
                         v
              4. Harvestability assessment
       Review ripeness evidence, visibility, confidence,
       reachability, clearance, and missing/contradictory inputs
                         |
                         v
              5. Plan proposal
       Generate a candidate approach / waypoint sequence
                         |
                         v
              6. Deterministic safety gate
       Reject unsafe, incomplete, or unverified proposals;
       require independent collision and workspace validation
                         |
                         v
              7. Report and operator review
       Save decision status, reasons, and an auditable JSON report
```

### What each stage does

1. **Input:** Start with synthetic scenes or recorded orchard images. RGB-D cameras and LiDAR can be integrated, but sensor calibration and timestamp synchronization must be checked before trusting spatial measurements.
2. **Perception:** A vision model extracts features and may propose coconut/tree targets. A model architecture or a generic pretrained checkpoint alone does not prove accurate coconut detection; this requires labelled, representative orchard data and held-out evaluation.
3. **3D/4D scene understanding:** Depth and sensor calibration can help estimate target locations in 3D. The 4D layer refers to tracking how targets and the robot scene change over time; it is not a claim that a validated real-time 4D system is already operating in an orchard.
4. **Harvestability:** The system can consider supplied evidence such as ripeness, occlusion, localization confidence, reachability, clearance, and tracking stability. A score is only as reliable as its inputs and validation.
5. **Planning:** The planner proposes candidate waypoints or a harvesting sequence. A proposed path must not be described as collision-free unless an independent, validated collision checker has verified it.
6. **Safety gate:** The prototype can reject proposals and use conservative states such as `SAFE_HOLD`, `BLOCKED`, or `PROPOSAL_APPROVED_NOT_EXECUTED`. Approval means only that configured software checks passed; it is not authorization to move a physical robot.
7. **Reporting:** The end-to-end demo emits a JSON audit report containing the decision status and reasons. The documented demo does **not** send actuator commands.

### Run the prototype locally

From the repository root:

```bash
python -m pip install -e ".[dev]"
python demo_end_to_end.py
python -m pytest
```

See the [end-to-end simulation guide](docs/END_TO_END_SIMULATION.md), [pipeline implementation](src/coconut_harvest_robot/end_to_end.py), [demo script](demo_end_to_end.py), and [evaluation benchmark](docs/EVALUATION_BENCHMARK.md).

### Current implementation vs. future validation

| Area | What this repository currently supports | What is still needed |
|---|---|---|
| Software workflow | Prototype pipeline, configured checks, and JSON reporting | Reproducible tests across representative scenarios |
| Vision | Neural feature-processing prototype | Labelled orchard dataset, trained/validated coconut detector, held-out metrics |
| Harvestability | Assessment of supplied evidence and configured scores | Ground-truth maturity labels and evaluation of decision quality |
| 3D/4D reasoning | Prototype spatial/temporal architecture | Calibrated sensors, measured localization error, validated target tracking |
| Motion planning | Candidate trajectory/waypoint proposal | Independent collision checking, robot-kinematics and physics validation |
| Robot execution | Documented integration path and simulation assets | Validated ROS 2/controller integration, hardware tests, risk assessment |
| Field harvesting | Not demonstrated by the software demo | Supervised field trials and documented success, failure, and safety results |

### Safety and evidence limits

This is **not yet a validated autonomous harvesting robot**. The demo uses synthetic inputs and/or explicitly supplied evidence rather than proving that a trained model correctly detects and harvests coconuts in real orchards. Concept images and animations illustrate the idea; they are not experimental results. Do not connect this prototype directly to physical motors, cutters, or manipulators. Before any hardware trial, require calibrated sensors, independent collision/workspace checks, emergency-stop verification, supervised low-risk testing, and documented safety review.


### Platform scope: AI application + embodied robotics

**This platform is designed to support both an AI application and embodied AI in a robot.** These are two connected layers of one research platform:

- **AI application layer (runs on a computer):** orchard-image/data processing, coconut target detection and tracking experiments, harvestability assessment, uncertainty reporting, visualization, and reviewable harvest-plan proposals.
- **Embodied robotics layer (robot-facing architecture):** connect perception and planning to a simulated or physical agricultural robot through interfaces such as ROS 2, with localization, 3D scene understanding, reachability/collision checks, manipulation planning, and independent safety supervision.
- **Shared pipeline:** sensor/data quality → perception and tracking → 3D/temporal world model → task planning → safety validation → operator review and audit.

The software application can be developed and evaluated on a computer without robot hardware. The embodied layer is the intended robotics integration path; **do not interpret this architecture or concept artwork as proof that physical robot integration, safe manipulation, or field harvesting has been completed or validated.** Begin with synthetic/recorded data and simulation, then require measured benchmarks and independent safety validation before hardware trials.


### Quick start

Clone the renamed repository and install the project dependencies:

```bash
git clone https://github.com/Pui89/Coconut-Harvest-AI.git
cd Coconut-Harvest-AI
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python demo_end_to_end.py
python -m pytest
```

The end-to-end demo and tests are intended for local development with the project's documented inputs. Start with synthetic or recorded data; do not connect the prototype directly to physical actuators or use it as the sole basis for consequential decisions.

**Workflow:** sensor/data quality checks → perception and multimodal evidence → 3D/temporal scene representation → uncertainty and unknown-case handling → reviewable plan or screening proposal → audit record.

**Documentation:** [End-to-end simulation guide](docs/END_TO_END_SIMULATION.md) · [Evaluation benchmark](docs/EVALUATION_BENCHMARK.md)

## PUI89 AI Robotics Platform

**Autonomous multimodal embodied-AI platform for orchard harvesting.**

This repository is one vertical implementation of the **PUI89 AI Robotics** platform for agriculture. The common architecture is:

```text
Multimodal Sensors
      ↓
Quality / Health Gate
      ↓
Perception + Tracking
      ↓
3D / 4D World Model
      ↓
Uncertainty + OOD
      ↓
Foundation-Model Reasoning
      ↓
Task Planning
      ↓
Deterministic Safety Supervisor
      ↓
ROS 2 / Robot Control
      ↓
Telemetry / Evidence
      ↓
MLOps / Fleet Learning
```

### Product tiers

- **PUI89 Research** — universities, robotics competitions, researchers
- **PUI89 Professional** — farms, plantations, agricultural operators
- **PUI89 Enterprise** — large corporations, governments, logistics, ports, infrastructure

### Cross-environment research

The same perception/world-model/uncertainty/safety interfaces are designed to transfer between agriculture, disaster response and security/inspection. Transfer must be measured with the repository benchmark; it is not assumed from architecture alone.

- [Optional DINOv2 + Anomalib integration, end-to-end verification and tests](docs/OPEN_SOURCE_VISION_INTEGRATION.md)
- [ROS 2 + Nav2 + Gazebo Sim + Open3D integration guide and environment preflight](docs/ROBOTICS_STACK_INTEGRATION.md)

### Evidence standard

This project separates **targets, prototypes and measured results**. Production or field-validation claims require reproducible benchmark evidence, failure testing, and documented safety validation.

See:
- [PUI89 Benchmark](docs/PUI89_BENCHMARK.md)
- [Cross-Environment Transfer Benchmark](docs/PUI89_TRANSFER_BENCHMARK.md)
- [Product Tiers](docs/PUI89_PRODUCT_TIERS.md)
- [Failure and UNKNOWN Protocol](docs/PUI89_FAILURE_AND_UNKNOWN_PROTOCOL.md)
- [MLOps Model Lifecycle](docs/PUI89_MLOPS_MODEL_LIFECYCLE.md)
- [Research, Competition and Commercial Evidence](docs/PUI89_RESEARCH_COMPETITION_INVESTOR.md)
- [12-Month Roadmap](docs/PUI89_12_MONTH_ROADMAP.md)
- [Cost Safety and Billing Policy](docs/COST_SAFETY_AND_BILLING.md)

## Robot concept and development status

PUI89 Coconut Harvest Robot is a **simulation-first research concept** for investigating safer coconut harvesting. The proposed architecture compares a trunk-climbing platform with alternatives such as a ground-based arm. The mechanical approach is not yet validated; physical climbing and cutting must not be assumed to work.

![Coconut harvest robot concept](docs/images/coconut_harvest_robot_photo.svg)

### 3D / 4D concept visualization

![3D/4D coconut harvest robot concept](docs/coconut_harvest_robot_3d_4d_concept.svg)

These repository graphics are concept visualizations, not evidence of a completed or field-tested robot. Any animation illustrates a proposed trajectory rather than measured robot performance.

- [Concept design, subsystems, safety boundaries and acceptance criteria](docs/CONCEPT_DESIGN.md)
- [Simulation-first development roadmap and release gates](docs/DEVELOPMENT_ROADMAP.md)
- [Robot description (URDF)](robots/coconut_harvester.urdf)
- [Simulation demos](sim/)
- [Evaluation benchmark](docs/EVALUATION_BENCHMARK.md)

### End-to-end simulation demo

Run the safety-gated software workflow with synthetic orchard inputs:

~~~bash
python -m pip install -e ".[dev]"
python demo_end_to_end.py
python -m pytest
~~~

**Workflow stages**
1. **Sensor health:** evaluate sensor quality and timestamp alignment; unhealthy or unsynchronized inputs trigger a safe hold.
2. **Perception proposal:** process RGB and depth tensors through the current prototype pipeline.
3. **Harvestability review:** score explicitly supplied evidence for perception/localization confidence, ripeness, reachability, clearance, occlusion, and tracking stability.
4. **Safety gate:** reject proposals without independent collision validation or when other configured safety conditions fail.
5. **Audit report:** emit a JSON report with status, decision reasons, prototype trajectory waypoint count, and the actuator-command invariant.

**Possible report status:** `SAFE_HOLD`, `BLOCKED`, or `PROPOSAL_APPROVED_NOT_EXECUTED`. An approval status means only that a software proposal passed the configured checks; it is **not** permission to operate a physical robot.

- [End-to-end workflow, tests, safety gates and limitations](docs/END_TO_END_SIMULATION.md)
- [Pipeline implementation](src/coconut_harvest_robot/end_to_end.py)
- [Synthetic demo](demo_end_to_end.py)
- [End-to-end tests](tests/test_end_to_end.py)
- [CI results](https://github.com/Pui89/Coconut-Harvest-AI/actions)

**Evidence and safety limits:** The demo uses generated synthetic imagery and hand-supplied evidence; these are fixtures, not measured detection or harvesting results. The trajectory planner is not independently collision-validated, and the report never sends actuator commands. Do not use this prototype to control a physical robot. Gazebo Sim/Isaac Sim physics validation, calibrated sensor evaluation, independent collision checking, and a documented safety review remain future acceptance gates.

### First engineering priority

1. Audit the current URDF, demo scripts, dependencies and tests.
2. Make a reproducible palm-trunk simulation with configurable dimensions and contact assumptions.
3. Validate robot frames, joint limits, collision geometry and safety states.
4. Establish a held-out vision dataset and publish raw benchmark logs before reporting metrics.
5. Only after simulation and risk review, assess a low-height, tethered, non-cutting physical rig.

**Evidence policy:** clearly distinguish design targets, simulation measurements and physical measurements. Do not claim autonomous harvesting, field readiness, or safety validation without reproducible evidence.

## Prototype pipeline overview

This repository sketches the intended harvesting pipeline. The current implementation is a research prototype and does not provide validated autonomous harvesting or safe physical control. The end-to-end demo produces a report only; it is not evidence of real-world performance.

- **Vision prototype**: neural feature extraction from RGB/depth tensors; coconut-specific detection needs dataset validation
- **Spatial prototype**: feature fusion intended to support future 3D localization
- **Planning prototype**: candidate waypoint generation; collision-free motion is not verified
- **Action boundary**: no physical gripper, cutter, or motor command is issued
- **Real orchard validation**: RGB-D/LiDAR calibration and held-out farm-data evaluation remain future work

## Pipeline overview

![Harvest pipeline](docs/images/harvest_pipeline.svg)

## System Architecture

### Perception Pipeline

```
Input (RGB + Depth)
    |
    v
Preprocessing
  - normalization
  - geometric alignment
    |
    v
Coconut Detector (CNN)
  - bounding box regression
  - ripeness classification
    |
    v
Tree Segmentation
  - trunk localization
  - branch geometry
  - canopy boundary
    |
    v
Depth Analyzer
  - height estimation
  - distance calculation
  - 3D point cloud projection
    |
    v
Spatial Feature Extractor
  - coconut 3D position
  - reachability scoring
  - obstacle map
```

### Motion Planning Pipeline

```
Target Coconut (3D position + ripeness)
    |
    v
Reachability Analysis  - robot workspace check
  - collision detection
  - approach angle planning
    |
    v
Trajectory Generator
  - RRT* path planning
  - smooth arm kinematics
  - gripper pre-positioning
    |
    v
Motion Validator
  - joint limit check
  - velocity profile
  - safety margins
    |
    v
Execution Plan
  - approach → grasp → retract → place
```

### Action Execution Pipeline

```
Execution Plan
    |
    v
Robot Controller
  - inverse kinematics
  - motor commands
  - feedback control
    |
    v
End Effector
  - gripper force control
  - cutting mechanism
  - drop/place logic
    |
    v
Result Logging
  - success/failure
  - fruit placement
  - next target
```

## Project Structure

```text
.
├── README.md
├── ARCHITECTURE.md
├── requirements.txt
├── pyproject.toml
├── demo.py
├── docs
│   ├── images
│   │   ├── coconut_harvest_robot_photo.svg
│   │   ├── harvest_pipeline.svg
│   │   ├── coconut_robot_realistic.svg
│   │   ├── coconut_robot_cartoon.svg
│   │   └── coconut_robot_drone_view.svg
│   ├── TECHNICAL_OVERVIEW.md
│   └── ORCHARD_DATA.md
├── src
│   └── coconut_harvest_robot
│       ├── __init__.py
│       ├── config.py
│       ├── data.py
│       ├── vision.py
│       ├── spatial.py
│       ├── planner.py
│       ├── action_model.py
│       ├── kinematic_solver.py
│       ├── pipeline.py
│       └── utils.py
├── tests
│   ├── test_pipeline.py
│   ├── test_planner.py
│   └── test_kinematics.py
└── data
    └── sample_orchard_scenes
```

## Installation

```bash
git clone https://github.com/Pui89/Coconut-Harvest-AI.git
cd Coconut-Harvest-AI
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick start

```bash
python demo.py
```

## Example usage

```python
import torch
from coconut_harvest_robot.pipeline import HarvestPipeline

## Open-source Harvest Planning Agent (new prototype)

A small, local, deterministic decision-support agent is available at
[`agents/harvest_planning_agent.py`](agents/harvest_planning_agent.py). It evaluates supplied coconut candidates, explains rejected targets, ranks candidates that pass configured checks, and outputs an auditable JSON proposal.

- [Agent setup and limitations](agents/README.md)
- [Open-source agent development and evaluation plan](docs/OPEN_SOURCE_AGENT_GUIDE.md)
- [Example candidate input](examples/agent_candidates.example.json)
- [Agent tests](tests/test_harvest_planning_agent.py)

Run from the repository root with Python 3.10+:

```bash
python agents/harvest_planning_agent.py
python agents/harvest_planning_agent.py --input examples/agent_candidates.example.json --output agent_report.json
```

The baseline uses only Python's standard library; no paid API, hosted inference endpoint, or model download is required. The example inputs are synthetic. The agent does not detect coconuts itself, validate real robot reachability, perform independent collision checking, or control hardware. Its output is for simulation review only; physical robot execution is not authorized.


## Free Windows Laptop Quick Start

To try the rule-based planning agent without installing extra Python packages or downloading an AI model:

1. Download the repository ZIP using **Code → Download ZIP**, then extract it.
2. Open the extracted repository folder.
3. Double-click `run_free_agent.bat`.

The launcher checks your Python version and reports optional packages without installing anything. Alternatively, run `python scripts\\check_local_agent_environment.py` and then `python agents\\harvest_planning_agent.py` from Command Prompt.

See [Free Windows Setup](docs/FREE_WINDOWS_SETUP.md). This starter run uses synthetic candidate data and is not a real camera, trained detector, or physical robot test.


---

## Real Coconut Image Review — Free Local Workflow

The repository now includes a **manual real-image review workflow** using openly referenced coconut photographs. It prepares a local image sample and CSV annotation sheet without installing packages or downloading an AI model.

**[Read the real-image workflow guide](docs/REAL_IMAGE_TEST_WORKFLOW.md)**

From the repository root on Windows, run:

```bat
python scripts/prepare_real_image_review.py --download
```

The script downloads two reference photographs from Wikimedia Commons on demand and creates a local review CSV plus source/licence notes. It does not upload images or annotations to GitHub.

**Important status distinction:** this is a real-image *manual review* workflow, not automatic coconut detection. The current rule-based agent does not analyse image pixels; it consumes candidate fields supplied by another component or a person. A normal RGB photo does not establish calibrated 3D position or robot reachability. No detector accuracy, depth accuracy, or robot safety performance is claimed.

---

## Example: How a Coconut Harvesting AI Robot Could Help Replace High-Risk Climbing Work

The concept below shows one possible **AI-assisted coconut harvesting workflow**. The aim is to reduce the need for a worker to climb a tall palm to inspect and harvest coconuts. A robot would observe the canopy from a suitable platform, propose a target, check whether a tool can reach it safely, and ask a human operator to approve the task. The robot design and method must be validated before this could be used in a real plantation.

![Illustrated coconut harvesting AI robot workflow showing sensing, target assessment, safety checks and human supervision](docs/images/coconut_harvest_robot_workflow_concept.svg)

*Illustration is a concept visualization, not a photograph of a built robot or evidence of a successful harvest.*

### Example task: from tree to collected coconut

1. **Observe the tree:** a camera and, if available, a calibrated depth sensor capture the tree and coconut cluster. The system checks whether the data are usable.
2. **Propose a target:** a vision model could identify candidate coconuts and estimate their positions. It must report uncertainty and leave unclear or occluded fruit for human review.
3. **Check reach and risk:** a planner could propose a tool approach. Independent checks must verify reachability, collisions, branches, people in the work zone, and safe tool operation. If checks fail or data are missing, the robot must hold position and request help.
4. **Human authorization:** a trained operator reviews the proposed target and plan, and can stop the task at any time. Remote supervision is not a substitute for physical safety controls.
5. **Harvest and verify (future capability):** only after mechanical design, guarded tooling, safety interlocks, and controlled tests are validated could an approved controller perform a cut or grasp. Sensors would then check whether the coconut was actually collected; uncertain outcomes would be reported rather than guessed.

### What is working now, and what is not

| Capability | Current evidence in this repository |
|---|---|
| AI application / decision-support prototype | Code and demo workflows exist; the demo uses supplied or synthetic evidence and does not itself prove accurate coconut detection from uploaded photographs. |
| Harvest plan proposal and audit report | Prototype software can produce reviewable proposals and reports; these are not commands to physical actuators. |
| Robot concept illustration and model assets | Design concepts and simulation-related files are included. |
| Reliable detection of real coconuts, ripeness, and 3D position | **Not yet established.** Requires representative labelled orchard data, calibrated sensors, and measured validation. |
| Robot physically climbing or reaching a palm, cutting/grasping fruit, and collecting it | **Not demonstrated.** Requires a validated mechanical system, controlled simulation, hardware tests, and risk assessment. |
| Replacing a worker entirely | **Not a current capability or claim.** The intended benefit is to reduce hazardous climbing and support a human-supervised harvesting workflow. |

### Free, simulation-first development plan

1. Run the existing local software demo and tests.
2. Create a repeatable simulated palm, robot reach envelope, and guarded tool model; validate the geometry and joint limits.
3. Test target-location error, reachability, collision rejection, safe-stop behavior, and task completion in simulation. Record results and failures instead of inventing performance numbers.
4. Only after documented simulation and safety gates pass, consider low-height, tethered, non-cutting hardware trials under supervision.

**Safety boundary:** this repository is a research prototype, not a field-ready harvesting robot. Do not connect its current prototype directly to motors, cutters, or manipulators, and do not use it as the sole basis for a real harvest. A human operator, independent safety system, emergency stop, exclusion zone, and documented risk assessment remain necessary for any future physical trial.



---
