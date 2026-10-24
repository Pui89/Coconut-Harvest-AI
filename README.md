# Coconut Harvest AI


## Current verified status — 25 October 2026

**Stage:** local software, data-quality and evaluation foundations. This repository does not yet demonstrate a validated physical coconut-harvesting robot.

**Protection policy:** [Automated protection and fail-safe policy](docs/AUTOMATED_PROTECTION_POLICY.md). This documents required software safeguards and validation gates; it does not claim physical safety or validated operational performance.

- **SAM 3 segmentation:** the optional local smoke-test script and guide are merged ([PR #80](https://github.com/Pui89/Coconut-Harvest-AI/pull/80)). No SAM 3 inference result has been verified yet. Model weights are downloaded only when the script is run; check compatibility, access terms, disk space and GPU memory first.
- **Automated checks for the SAM 3 change:** the Python tests, main CI, security checks and Ruff helper review completed successfully for the change's pull-request commit. These checks do not measure segmentation accuracy.
- **Dataset gate:** the existing project snapshot reports 34 candidate records and 0 approved for training. Resolve label/geometry and source-permission reviews before training or publishing model metrics.
- **Fault-monitor contract:** documentation-only contract merged in [PR #79](https://github.com/Pui89/Coconut-Harvest-AI/pull/79). The Python fault-monitor component has unit tests, but the contract does not itself connect to physical actuators or provide hardware safety.
- **Next:** run the smoke test on one approved local image; review its mask manually; then complete the dataset gate and run a held-out detector benchmark with precision, recall, F1 and latency.
- **Evidence boundary:** CI success is software evidence only. Coconut detection, maturity classification, 3D targeting, harvest reach, cutting, capture and real-orchard operation remain unvalidated unless separately measured.


![Conceptual coconut harvesting robot design](docs/images/coconut-harvest-realistic-all-stage-concept.svg)

*Conceptual design illustration — not a photograph of a built robot and not evidence of a successful harvest. Reach, stability, tool design, fruit retention, safe lowering, and operation in real orchards remain unvalidated.*

## Optional local Hugging Face vision experiment

Try open-vocabulary coconut detection on a local image with [`tools/huggingface_local_vision_demo.py`](tools/huggingface_local_vision_demo.py). Read [`docs/HUGGINGFACE_LOCAL_VISION.md`](docs/HUGGINGFACE_LOCAL_VISION.md) first. This is an exploratory pretrained-model demo, not a trained or validated coconut detector; the dataset approval gate remains unchanged.

## Local fault-monitoring software (initial implementation)

A small, dependency-light Python module accepts explicit fault reports, suggests conservative responses, and keeps a bounded in-memory event log. It includes automated unit tests and a GitHub Actions test workflow. It is not an antivirus, intrusion detector, gunshot detector, or physical safety controller; hardware shutdown, persistent audit storage, alerts, and real-world threat detection require separate implementations and validation.

- [Fault monitor integration guide](docs/FAULT_MONITOR_INTEGRATION.md)
- [Fault monitor source](apps/pui89_safety/fault_monitor.py)
- [Fault monitor tests](tests/test_fault_monitor.py)



## Project status — 22 October 2026

**Current stage:** software and data-quality foundations; not yet a validated real-world harvesting robot.

- **Verified CI:** the latest commit's agent unit tests, Coconut AI regression tests, Python tests, main CI workflow, and GitHub Pages build/deployment all completed successfully. [Latest agent-test run](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39733576754) · [Latest main CI run](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39733576516).
- **Dataset gate:** 34 candidate records are in the current review snapshot; 0 are approved for training. Candidate source permissions, annotation correctness, and independent QA must be checked before training or performance claims.
- **Implemented:** local annotation/evaluation utilities, source-provenance workflow, structural dataset audit, rule-based safety decision support, and regression tests.
- **Next milestone:** run the candidate-fetch and dataset-audit commands, manually review suitable images, create human-checked annotations and a held-out test split, then publish actual detector metrics. The existing tiny baseline is not evidence of a trained coconut detector.
- **Limits:** CI success verifies software checks only; it does not demonstrate detector accuracy, GPU performance, robot-arm operation, or field harvesting.


## Fail-safe operating modes (software prototype)

The project defines three modes: **AI operation**, **limited safe operation**, and **manual recovery**. Fault responses are designed to fail conservatively:

| Problem | Expected robot response |
|---|---|
| AI model crashes | Stop harvesting and keep the cutter disabled; independent safety monitoring must remain active. |
| Camera or safety sensor fails | Stop autonomous movement if safe navigation cannot be confirmed; request operator recovery. |
| Wi-Fi or remote connection is lost | Stop the mission and enter a safe hold; do not continue hazardous work without required supervision. |
| Battery becomes low | Stop harvesting; return only if the route is verified, navigation is healthy, and sufficient reserve remains. Otherwise request recovery. |
| Main computer freezes | An independent watchdog and hardware safety circuit must disable hazardous actuators; software alone cannot guarantee this. |
| Robot gets stuck or tips | Disable cutting, stop or brake movement as appropriate to the physical hazard, alert the operator, and follow a planned recovery procedure. |

- [Fail-safe mode design and fault responses](docs/FAIL_SAFE_OPERATING_MODES.md)
- [System fault, hardware, electrical, and recovery playbook](docs/SYSTEM_FAULT_AND_HARDWARE_SAFETY.md)
- [Fail-safe decision selector](src/coconut_harvest_robot/failsafe.py)
- [Fail-safe tests](tests/test_failsafe.py)

**Status and limitation:** this is a software decision prototype, not a validated physical robot safety system. Real hardware requires independent emergency-stop circuitry, motor/arm interlocks, safe braking/holding behaviour, and staged physical validation.

## Free decision-support agent (current scope)

**Additional cost for this rule-based agent: $0.** It uses the repository's Python code and supplied inputs; it does not require a paid AI API, cloud service, or model download. Local Python/test tooling and GitHub usage remain subject to their own terms and limits.

**What it does:** Checks supplied target confidence, sensor health, depth, reachability, obstacle clearance, and human approval. It does not run a detector or command a robot arm.

```text
Orchard image / sensor measurements → rule-based safety checks → harvest recommendation or STOP → human approval
```

- **Run guide:** [Agent guide](docs/AGENT_GUIDE.md)
- **Important limitation:** this is a rule-based decision-support prototype, not proof of real-world performance. Hardware, optional third-party services, or future model training may have separate costs.


> **Product quality standard:** [benchmark protocol and fair comparison criteria](docs/PRODUCT_BENCHMARK_STANDARD.md). This defines what we need to measure; it does not claim market-leading performance.

> **Next research milestone — real detector evidence:** review image rights, annotate a small set of distinct orchard images, freeze a held-out test split, run an existing compatible local coconut detector, and publish its actual predictions plus precision/recall/F1 and latency. The current two-image baseline remains at precision 0 and recall 0 at IoU ≥ 0.50 until a new run is completed. [Follow the operator checklist](docs/FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md). Do not treat example CSV rows, reference photographs, or latency-only results as accuracy evidence.


## Run the project unit tests

Run the focused, lightweight unit tests locally with Python 3.10 or newer:

```bash
python -m pip install pytest
python -m py_compile agents/project_agent.py tests/test_project_agent.py tools/evaluate_coconut_detections.py tests/test_evaluate_coconut_detections.py tools/annotations_to_ground_truth_csv.py tests/test_annotations_to_ground_truth_csv.py
python -m pytest -q tests/test_project_agent.py tests/test_evaluate_coconut_detections.py tests/test_annotations_to_ground_truth_csv.py
```

A dedicated [GitHub Actions workflow](https://github.com/Pui89/Coconut-Harvest-AI/actions/workflows/agent-tests.yml) is configured to run the decision-agent, detector-evaluator, and annotation-converter tests on Python 3.10, 3.11, and 3.12 when relevant files change. Check the Actions page for the actual run status; adding this workflow does not itself mean the tests have passed.

## Start here — reviewer quick guide

- **Research case study:** [read the concise problem, current implementation, evidence limits, and proposed evaluation plan](docs/RESEARCH_CASE_STUDY.md).
- **Free/open-source model strategy:** [review license-first model selection and the reproducible coconut benchmark plan](docs/LICENSE_FIRST_MODEL_STRATEGY.md), including the hosted RT-DETR smoke test and license caveats.
- **Dataset readiness:** [see the current review-gate snapshot](docs/COCONUT_DATASET_READINESS.md): 34 candidate records reviewed, none approved for training yet, with an explicit no-cost annotation next step.
- **New image-source shortlist (review only):** [five Wikimedia coconut-image candidates with source-page, attribution, licence, and annotation-review requirements](docs/COCONUT_IMAGE_SOURCE_SHORTLIST_2026-10-22.md). None is automatically approved for training.

- **What works now:** [run the local planning prototype](#run-the-local-prototype), inspect the synthetic workflow, and review the annotation/evaluation tools.
- **What the evidence says:** [read the measured baseline](#current-evaluation-evidence), including the two-image HSV smoke test and its zero precision/recall result at IoU ≥ 0.50.
- **What comes next:** [follow the real-image benchmark checklist](docs/FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md) to establish image rights, review labels, run an existing compatible detector, and record reproducible results.
- **What is not yet proven:** a reliable trained coconut detector, generalisation across orchards, maturity classification, calibrated 3D targeting, or a physical robot harvesting coconuts.

**For a fair assessment:** automated tests demonstrate software behaviour; concept images explain the intended design; only reproducible held-out experiments establish model performance. This repository keeps those evidence types separate.


### Work locally on Windows

- **Annotate real coconut images (Windows):** [step-by-step offline annotation quick start](docs/WINDOWS_COCONUT_ANNOTATION_QUICKSTART.md). This avoids the common error of launching `tools\\coconut_annotator.html` from the wrong folder.

- **Run the demo app:** double-click [`RUN_COCONUT_APP.bat`](RUN_COCONUT_APP.bat). It requires Python and the app dependencies to be installed first.
- **Run a local detector latency benchmark:** double-click [`RUN_COCONUT_DETECTOR_BENCHMARK.bat`](RUN_COCONUT_DETECTOR_BENCHMARK.bat), then enter paths to an existing compatible coconut-trained `.pt` model and a permitted local test image. It checks imports but installs/downloads nothing. It measures latency only—not detection accuracy—and cannot run until you already have suitable model weights.
- **Label orchard images offline:** double-click [`OPEN_COCONUT_ANNOTATOR.bat`](OPEN_COCONUT_ANNOTATOR.bat). Select image files from your computer, draw boxes around visible coconuts, and export the annotation JSON. Images are processed in your browser and are not uploaded by this tool.
- **Important:** annotation quality and image reuse rights still need human review. Do not use the archived first-pass labels as training data; see [the review batch notes](data/review_batch_2026-10-18/README.md).

- **Commercial path:** [commercialisation roadmap](docs/COMMERCIALISATION_ROADMAP.md) — proposed first customer problem, software-first MVP, discovery questions, evidence gates, and a staged path toward robotics.
- **Customer discovery:** [orchard interview guide](docs/ORCHARD_CUSTOMER_DISCOVERY.md) — a 15-minute, no-cost interview script and evidence/consent rules to test whether the problem is real before building more.

## Support, sponsorship and open-source collaboration

PUI89 welcomes technical review, research collaboration, agricultural workflow feedback, rights-cleared image contributions, annotation review, reproducible benchmark work, and scoped sponsorship discussions.

- **Support and sponsorship brief:** [ways to collaborate with PUI89](https://github.com/Pui89/Pui89.github.io/blob/main/SUPPORT_AND_SPONSORSHIP.md)
- **Project website:** [PUI89 AI Robotics](https://pui89.github.io/)
- **Potential farm pilot:** [Coconut Orchard Pilot Brief](https://github.com/Pui89/Pui89.github.io/blob/main/COCONUT_ORCHARD_PILOT_BRIEF.md)

Please include the specific workflow, evidence, or milestone you can help with. Dataset contributions must include source and reuse permissions. No sponsor, field deployment, or performance outcome is implied by this invitation.

## Latest engineering update — 21 October 2026

- **Benchmark tooling:** the adaptive CPU microbenchmark with no additional package dependencies is available at [`tools/adaptive_compute_benchmark.py`](tools/adaptive_compute_benchmark.py), with regression tests in [`tests/test_adaptive_compute_benchmark.py`](tests/test_adaptive_compute_benchmark.py). It compares synthetic integer-reduction implementations; it is **not** an AI inference, energy-use, or robot-performance benchmark.
- **Input validation:** malformed benchmark argument types are now rejected clearly. The change was merged in [PR #36](https://github.com/Pui89/Coconut-Harvest-AI/pull/36).
- **Verification:** GitHub Actions passed the repository test suite on Python 3.10, 3.11, and 3.12 for the PR head before merge.
- **Evidence boundary:** this update does not change the initial real-image baseline reported below (precision 0 and recall 0 at IoU ≥ 0.50 on two images). Real-orchard generalization and physical harvesting remain unvalidated.
- **Fair model comparison:** added [`tools/compare_coconut_detectors.py`](tools/compare_coconut_detectors.py), regression tests, and a [comparison protocol](docs/FAIR_DETECTOR_COMPARISON.md). It ranks supplied prediction exports against the same reviewed ground truth and thresholds; it does not run models or claim better AI performance.
- **Reproducible detector evaluation:** added [`tools/evaluate_coconut_detections.py`](tools/evaluate_coconut_detections.py), unit tests, and a [CSV protocol](docs/REPRODUCIBLE_DETECTION_EVALUATION.md) for evaluating externally produced detector boxes. This tool does not run a model, and no new AI performance result is claimed.
- **Dataset split-leakage audit:** added [`tools/audit_dataset_split_leakage.py`](tools/audit_dataset_split_leakage.py), tests, and a [manifest guide](docs/DATASET_SPLIT_LEAKAGE_AUDIT.md). It checks recorded SHA-256 values and source-group IDs across splits; it does not compute file hashes or claim improved detector performance.
- **First real-image benchmark checklist:** added [the end-to-end manual workflow](docs/FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md), linking rights review, human annotations, geometry checks, split-leakage audit, and actual detector predictions. It explicitly stops short of claiming results until real inference is run.
- **Actual image-hash verification:** added [a local SHA-256 verifier](tools/verify_image_manifest_hashes.py), tests, and a [usage guide](docs/VERIFY_IMAGE_MANIFEST_HASHES.md). Unlike the manifest-only audit, it computes hashes from files on disk and flags exact-byte duplicates across splits; it does not detect resized or near-duplicate images.



**AI-assisted coconut detection, harvest-stage decision support, and agricultural robotics concept**

Coconut Harvest AI is a local-first software and robotics project exploring how computer vision, conservative planning, and human supervision could support coconut inspection and harvesting workflows.

The project aims to help an operator review individual coconuts, choose an intended harvest stage, assess candidate targets, and investigate safe robot integration. It is **not a finished or field-validated harvesting machine**.

![Coconut Harvest AI workflow overview](docs/images/coconut-harvest-ai-overview.svg)

### Real-world coconut imagery — illustrative references

<a href="https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg"><img src="https://commons.wikimedia.org/wiki/Special:FilePath/Fruiting_Coconut_Palm_Canopy.jpg?width=1400" alt="Fruiting coconut palm canopy with developing green coconuts; reference photograph for agricultural context" width="100%"></a>

*Fruiting Coconut Palm Canopy — an orchard-context reference photograph. [Open the source and licence details on Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg). This is not a PUI89 field capture, an annotated training image, an AI prediction, or evidence of detector performance.*

These source-linked photographs help explain the orchard setting and fruit visibility challenges. **They are illustrative references, not labelled training data or evidence of model performance.** Check each source page before reuse; the photos have not been added to the project's dataset.

| Reference | Intended use and rights |
|---|---|
| [Fruiting Coconut Palm Canopy](https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg) — [view original image](https://commons.wikimedia.org/wiki/Special:FilePath/Fruiting_Coconut_Palm_Canopy.jpg) | CC0 1.0, according to the source page. Candidate for an orchard-context visual; inspect at full resolution before use. |
| [Coconut palm plantation, Koh Mak, Thailand](https://commons.wikimedia.org/wiki/File:Koh_Mak_(island),_Thailand,_Coconut_palm_plantation.jpg) — [view original image](https://commons.wikimedia.org/wiki/Special:FilePath/Koh_Mak_(island),_Thailand,_Coconut_palm_plantation.jpg) | Photo by Vyacheslav Argenberg; CC BY 4.0, according to the source page. Attribution is required; verify licence details and record any changes before redistribution. |

**Data-quality rule:** a visually attractive orchard photo is not automatically suitable for detection training. Dataset inclusion requires rights review, original-file checks, target visibility, annotation QA, duplicate/leakage checks, and a reproducible evaluation split.

## Project at a glance

| Topic | Current position |
|---|---|
| Project type | Agricultural AI and robotics R&D |
| Available software | Rule-based planning agent, synthetic workflow demo, and manual image-review tools |
| Physical robot | Proposed concept; complete robot harvesting is not demonstrated |
| Real-image AI performance | Initial two-image baseline scored 0 precision and 0 recall at IoU ≥ 0.50; more data and reviewed labels are needed |
| Development approach | Local-first, using open-source tools where practical |
| Immediate focus | Rights-cleared data, annotation quality, reproducible evaluation, and simulation |

**Explore:** [Run the prototype](#run-the-local-prototype) · [Current evaluation evidence](#current-evaluation-evidence) · [Development roadmap](#development-roadmap) · [Safety and limitations](#safety-and-limitations)

**Engineering assurance:** [project requirements, hazard log, verification/validation gates, and evidence rules](docs/ENGINEERING_ASSURANCE_PLAN.md).

**Experiment records:** use the [reproducible experiment report template](docs/EXPERIMENT_REPORT_TEMPLATE.md) to record each dataset, model, threshold, metric, failure case, and rerun without overstating results.

**Dataset promotion gate:** [fail-closed rights + annotation approval checks](docs/COCONUT_DATASET_PROMOTION_GATE.md). This joins the current source-rights and candidate-review ledgers and intentionally blocks training until both record explicit, matching approvals.

**Research evaluation:** [reproducible research evidence checklist](docs/RESEARCH_EVIDENCE_CHECKLIST.md) for dataset controls, held-out metrics, run records, and the boundary between AI benchmarks and physical-robot claims.

**Immediate research next steps:** [focused evidence sprint](docs/RESEARCH_EVIDENCE_SPRINT.md) with the first real-image evaluation sequence, exact local commands, reproducibility requirements, and cost-control and safety boundaries.

**Limited-compute option:** [lightweight laptop-friendly workflow](docs/LIGHTWEIGHT_LAPTOP_WORKFLOW.md) prioritising CPU tests and data-quality checks before any large model download.

**Hardware-specific plan:** [16 GB RAM / 4 GB GPU compute profile](docs/COMPUTE_PROFILE_16GB_4GB_GPU.md) for this laptop class, including preflight checks, low-memory experiment choices, and evidence boundaries.



## Two parts of the project

<details>
<summary><strong>1. AI application — software for inspection and decision support</strong></summary>

The software side is intended to help a user review candidate coconuts, record the requested harvest stage, inspect uncertainty and safety checks, and produce an auditable planning report.

**Available now:** a rule-based planning agent, synthetic workflow demonstrations, and tools for manual image review and annotation quality checks.

**Not yet established:** reliable automatic coconut detection and maturity classification across real orchards, calibrated 3D fruit localization, or a validated model that can decide independently which fruit is ready to harvest.

</details>

<details>
<summary><strong>2. Physical AI robot — proposed machinery for future field work</strong></summary>

The robot concept shows how cameras and optional depth sensors could be combined with a mobile platform, a suitable reach mechanism, guarded cutting hardware, fruit retention or lowering, and independent safety controls.

**Current status:** concept and engineering workflow only. The repository does not demonstrate a complete physical robot performing validated coconut harvesting. The 0–30 m palm-height range is a long-term feasibility challenge, not a tested operating range.

</details>

**How they connect:** the application may recommend a candidate and a plan; a future robot would still need independently validated localization, reachability, hardware interlocks, human approval, and verified fruit collection. A software recommendation must never directly authorize a physical cut.


> **Current capability boundary:** this repository contains software prototypes, synthetic-data demonstrations, planning workflows, tests, and engineering concepts. Reliable all-stage detection, calibrated orchard-wide 3D localization, physical cutting and fruit collection, and autonomous operation at 0–30 m are not demonstrated capabilities. The 0–30 m range is a design challenge, not a proven robot reach specification.

## What the project includes

- **Local software workflow:** prototype code for reviewable candidate decisions and audit reports.
- **Harvest-planning agent:** a deterministic, rule-based tool that evaluates supplied candidate information; it does not detect fruit directly from image pixels.
- **Synthetic end-to-end demo:** exercises software gates and report generation without sending commands to physical actuators.
- **Real-image review workflow:** prepares a local manual-review sample and annotation sheet; it is not automatic detection.
- **Annotation overlay review tool:** a local OpenCV script renders existing boxes over original images for human QA; it does not certify annotations or detect fruit.
- **Robot concept and architecture:** outlines possible perception, target review, planning, and future hardware integration.
- **Cost-conscious development:** prioritizes local tools and open-source workflows, with no paid API required for the rule-based agent.

## How the system is intended to work

```text
Camera / optional depth sensors
            |
            v
Input quality and sensor checks
            |
            v
Coconut detection and stage assessment
            |
            v
Operator selects harvest stage or survey-only mode
            |
            v
Candidate review: uncertainty, location, reach and obstacles
            |
            v
Human approval + independent safety checks
            |
            v
Future validated robot mechanism (not implemented here)
            |
            v
Outcome verification and audit record
```

Each visible coconut should be assessed separately, including fruit in mixed-stage bunches. The operator's selected stage filters candidates but never overrides uncertainty or safety checks. If evidence is missing, a target is unclear, reach is unverified, or a hazard is detected, the intended response is **SURVEY ONLY / NO CUT**.

## Coconut stages and per-fruit decisions

| Observation | Intended software response | Intended action policy |
|---|---|---|
| Young green | Propose a class only when supported by agreed, validated criteria | Consider only if the operator selected this class and safety checks pass |
| Mature green | Keep separate from young green; green colour alone does not prove maturity | Require validated maturity criteria and confirmation |
| Mature brown/dry | Propose a provisional class with evidence and uncertainty | Consider only if selected and all safety checks pass |
| Mixed-stage bunch | Assess each fruit individually | Filter each candidate separately |
| Occluded, blurry, cropped, or ambiguous fruit | Mark uncertain or request another view | No automatic cut |
| Damaged or abnormal fruit | Flag for review | Exclude from normal automatic harvesting |
| Survey-only request | Detect or record candidates without selecting a harvest target | No cutting |

These are intended classes and policies, not a claim that a reliable model for every class is already trained. Local growers should define criteria appropriate to cultivar and intended use.

## How the system handles each coconut

The intended workflow treats **each visible fruit as a separate candidate**, even when several coconuts share one bunch. The operator's choice determines which maturity category is requested; it does not force the AI to label an uncertain fruit or permit an unsafe cut.

1. **Capture and inspect the view.** Check image sharpness, lighting, occlusion, and whether the fruit is sufficiently visible. Request another view or mark the candidate uncertain when the image is inadequate.
2. **Detect and separate candidates.** A future validated vision model should assign a distinct candidate ID and bounding region to each visible coconut. Overlapping fruit must not be assumed to be one fruit or confidently split without evidence.
3. **Estimate maturity with uncertainty.** Use validated visual and, where available, additional sensor evidence. Colour alone is not enough to reliably distinguish every young, mature-green, brown, or dry coconut.
4. **Apply the operator's selection.** Keep candidates that match the requested stage; label non-matching candidates as “not selected.” Keep survey-only mode available when the operator wants inspection without harvesting.
5. **Check localization and reach.** Verify the candidate's 3D position, tool approach, obstacles, robot stability, and whether the actual mechanism is validated for that height. If any required measurement is missing or outside the verified operating envelope, return **NO CUT**.
6. **Require approval and safety interlocks.** Before any future physical cutting trial, require explicit human approval and independent hardware safety controls. The software prototype in this repository does not command a real cutter.
7. **Verify the outcome.** A future system should confirm whether the fruit was safely retained or lowered and record failures separately. A detection, plan, simulated action, or attempted cut must never be counted as a successful harvest by itself.

| Example situation | Candidate decision | Cutting policy |
|---|---|---|
| Requested mature-green fruit, clear image, validated maturity evidence | Eligible for further review | Only after all reach, safety, and approval gates pass |
| Young green fruit when brown/dry fruit was requested | Not selected | No cut |
| Brown-looking fruit with uncertain maturity | Uncertain; request another view or human review | No cut |
| Fruit partly hidden behind leaves or another coconut | Incomplete evidence | No cut |
| Fruit appears reachable but 3D position or tool clearance is unverified | Reachability unknown | No cut |
| Fruit is above the mechanism's verified reach envelope | Out of range | No cut |
| Operator chooses survey-only mode | Record/review candidate only | No cut |
| A cut is attempted but fruit collection is not confirmed | Outcome unverified | Do not report harvest success |

**Implementation status:** This section documents the intended system behaviour. It does not mean that all seven stages, an all-maturity detector, 3D localization, physical cutting, or harvest verification are already implemented. Current implementation details and evaluation evidence are listed in the status and benchmark sections below.

## Robot concept


A future system may combine a mobile platform, camera and optional depth sensors, a suitable high-reach mechanism, a guarded cutting tool, fruit retention or lowering, emergency stops, and independent safety controls. A compact ground robot with a short arm cannot reach a 20–30 m palm crown by itself. Any high-reach design requires separate mechanical feasibility and safety validation.

### Tree-height scope

| Approximate height | Intended development scope | Current status |
|---|---|---|
| 0–3 m | Supervised perception and guarded test-rig feasibility | Candidate first test range; physical harvesting is not validated |
| 3–6 m | Study an engineered mast or lift | Concept/feasibility work |
| 6–12 m | Study purpose-built high-reach or climbing mechanisms | Not demonstrated |
| 12–20 m | Study specialist access, retention, and exclusion-zone requirements | Unvalidated engineering challenge |
| 20–30 m | Assess specialist solutions and alternatives to a ground-mounted arm | Outside demonstrated capability |

Detection at a height does not mean the robot can reach or harvest at that height. If reach, localization, stability, collision clearance, weather conditions, fruit capture, or the exclusion zone cannot be verified, the system must not initiate a cut.

## Implemented software vs. planned capabilities

| Area | Status |
|---|---|
| Rule-based harvest-planning agent | Code is available; evaluates supplied candidate fields and creates an auditable proposal |
| Synthetic end-to-end workflow | Available for software testing; synthetic inputs are not field evidence |
| Manual real-image review | Workflow and guide are available; this is not automatic detection |
| Coconut-specific model generalization | Not established; requires a larger, rights-cleared, independently reviewed dataset and held-out evaluation |
| Reliable all-stage maturity classification | Not established |
| Calibrated 3D localization and real robot reachability | Requires sensor calibration and independent validation |
| Physical cutting, collection, and autonomous harvesting | Not demonstrated |
| Safe operation at 0–30 m | Not demonstrated; long-term feasibility challenge |

## Current evaluation evidence

The first candidate batch was visually triaged across 30 images. Only two close-up images had first-pass boxes, totalling 15 reference boxes; the annotations still require independent review.

A simple OpenCV HSV-contour baseline was evaluated on those two images:

| Measure | Initial result |
|---|---:|
| Images evaluated | 2 |
| Reference boxes | 15 |
| Predicted boxes | 20 |
| Precision at IoU ≥ 0.50 | 0.000 |
| Recall at IoU ≥ 0.50 | 0.000 |
| F1 at IoU ≥ 0.50 | 0.000 |
| Mean CPU runtime | 15.12 ms/image |

This is a weak, simple non-ML smoke-test baseline, **not** a trained detector benchmark. Two images are insufficient to support generalization claims. The result is included transparently so the next experiments have a clear baseline.

**Reproducible evidence:** [raw benchmark report (JSON)](data/review_batch_2026-10-18/benchmark_report_v0.1.json) · [candidate review and annotation status](data/review_batch_2026-10-18/README.md) · [image-source rights audit](data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv) · [image hash manifest](data/review_batch_2026-10-18/image_sha256_manifest_2026-10-20.csv).

**Visual detection evidence status:** the repository currently has workflow/concept illustrations, but the initial benchmark does not establish successful real-image detection. A real annotated prediction overlay should be added only after the source image rights and annotations are verified and the model/script output can be reproduced. Do not use concept artwork as if it were an AI detection result.

Before training, the dataset still needs image-by-image source and licence checks, independent box and maturity-label review, a frozen manifest, duplicate checks, and leakage-safe splits grouped by scene/source.

## Run the local prototype

Use Python 3.10 or newer. Start with the standard-library planning agent, which does not require a paid API or model download.

```bash
git clone https://github.com/Pui89/Coconut-Harvest-AI.git
cd Coconut-Harvest-AI
python agents/harvest_planning_agent.py
python agents/harvest_planning_agent.py --input examples/agent_candidates.example.json --output agent_report.json
```

On Windows, see [Windows Setup Guide](docs/FREE_WINDOWS_SETUP.md).

### Synthetic end-to-end demo and tests

```bash
python -m pip install -e ".[dev]"
python demo_end_to_end.py
python -m pytest
```

These commands exercise the repository's software workflow and tests. Check the dependency and environment notes before installing optional packages. The demo uses synthetic or supplied evidence; it does not establish real-image detection accuracy or authorize physical robot control.

The focused [coconut proposal safety regression tests](tests/test_coconut_safety_pipeline.py) check unknown-depth rejection, camera-frame localization, and that human approval never authorizes actuator commands. The local RGB-D bridge also rejects different RGB/depth image dimensions; this does not replace validation of sensor alignment and calibration. See the [local detector and RGB-D workflow](training/README.md).

### Manual real-image review

See [Real Image Test Workflow](docs/REAL_IMAGE_TEST_WORKFLOW.md). The optional script can download two reference photographs from Wikimedia Commons and prepare a local review CSV plus source/licence notes. Review each source's licence and attribution requirements before reuse. This workflow is manual review, not automatic detection.

## Development roadmap

1. Verify the source, licence, attribution, and hash of every candidate image.
2. Independently review annotations and maturity labels; exclude unclear or unsuitable images.
3. Build a sufficiently varied dataset and create leakage-safe train/validation/test splits.
4. Train and evaluate a local baseline on held-out images; report per-class precision, recall, F1/mAP, failure cases, and runtime.
5. Test uncertainty handling, occlusion, false-safe reachability decisions, and stop conditions.
6. Develop and validate a simulation model for the robot geometry and reach envelope.
7. Consider supervised, low-height, non-cutting hardware trials only after documented simulation, risk assessment, and independent safety gates pass.

## Safety and limitations

- This repository is a development prototype, not a field-ready agricultural machine.
- Do not connect prototype software directly to motors, cutters, or manipulators.
- A software approval or simulated task is not proof that a physical action is safe.
- Any future physical trial needs independent safety controls, emergency stop, a clear exclusion zone, supervised operation, and documented risk assessment.
- A successful harvest must be independently verified; a detection, plan, animation, or attempted cut is not a harvest success.
- No claims are made for guaranteed labour savings, safety improvement, yield, commercial return, or reliable performance across all coconut stages.

## Documentation

- [Product brief](docs/PRODUCT_BRIEF.md)
- [Project status](docs/PROJECT_STATUS_2026-10-18.md)
- [Validation matrix](docs/VALIDATION_MATRIX.md)
- [Complete-system blueprint](docs/COMPLETE_SYSTEM_BLUEPRINT.md)
- [Coconut-stage roadmap](docs/COCONUT_STAGE_ROADMAP.md)
- [0–30 m tree-height feasibility plan](docs/TREE_HEIGHT_FEASIBILITY_0-30M.md)
- [Candidate image triage](docs/CANDIDATE_IMAGE_TRIAGE_2026-10-20.md)
- [Evaluation benchmark](docs/EVALUATION_BENCHMARK.md)
- [End-to-end simulation guide](docs/END_TO_END_SIMULATION.md)
- [Robot workflow guide](docs/END_TO_END_ROBOT_WORKFLOW.md)
- [Planning agent guide](agents/README.md)
- [Cost safety and billing policy](docs/COST_SAFETY_AND_BILLING.md)
- [CI and test runs](https://github.com/Pui89/Coconut-Harvest-AI/actions)

## Collaboration

Feedback and collaboration are welcome from coconut growers, agricultural cooperatives, agricultural machinery developers, robotics engineers, and open-source contributors. Useful contributions include rights-cleared orchard imagery, annotation review, reproducible benchmarks, simulation testing, and safety-focused engineering review.

## Licence and third-party assets

Check the repository's licence and each third-party dataset, image, model, and dependency licence before reuse. Inclusion in a demo or contact sheet does not automatically grant redistribution or training rights.


## Decision-support agent (rule-based prototype)

A local, standard-library-only agent module is available in [`agents/project_agent.py`](agents/project_agent.py), with focused tests in [`tests/test_project_agent.py`](tests/test_project_agent.py) and integration notes in [`docs/AGENT_GUIDE.md`](docs/AGENT_GUIDE.md). It produces reviewable recommendations from supplied observations; it does not run a perception model, call a hosted API, or issue actuator commands. These rules and tests are not evidence of trained-model accuracy or real-world validation.


## Automation roadmap (free-first)

The GitHub Actions workflow runs on relevant changes, manual dispatch, and a weekly schedule. Each test run writes test counts to the workflow summary; inspect the run logs if a report is missing.

**Next automated milestones**
1. Keep the test suite and dataset-structure/YOLO-label checks reproducible on supported Python versions.
2. Add safe checks for dataset-manifest provenance, SHA-256 integrity, exact duplicate files, and source-group leakage before any training run.
3. Generate a human-review queue for missing rights evidence, uncertain labels, and annotation QA; automation must never mark image rights or annotations as approved.
4. When a lawful, human-reviewed dataset is ready, run a repeatable baseline and publish measured metrics with the exact data split and environment.

**Gate:** the repository currently documents 34 candidate records and 0 approved for training. Do not train or publish accuracy claims until the current dataset status is rechecked and the approval gate is satisfied. These checks do not validate a physical harvesting robot.


---

## Free Local Automation Framework

This repository includes a shared PUI89 health-check script for repeatable, zero-cost local checks.

- [Automation guide](docs/PROJECT_AUTOMATION.md)
- [Local health-check script](scripts/pui89_project_health_check.py)

Run from the repository root:

```bat
python scripts\pui89_project_health_check.py
```

The checker verifies repository structure, scans Python source syntax, discovers test files, and prints a JSON report. It does not install packages, download models, use APIs, or call cloud services. To run tests, explicitly use `--run-tests`; pytest is run only if already installed.

**Project focus:** real-image dataset provenance, annotation integrity, detector evaluation, harvest-agent rules and explicit no-actuator safety boundary.

**Focused regression tests:** [Harvest planning safety regression tests](tests/test_harvest_planning_safety.py). Checks missing 3D position, unconfirmed reachability, invalid confidence, occlusion, maturity-stage filtering, survey-only behavior, and configured range limits.

**Evidence boundary:** a syntax scan is not a full test run; passing tests do not establish field performance or safety. Report only verified outcomes and keep proposed features separate from demonstrated results.

**Failure and security response:** see [failure and security response matrix](docs/FAILURE_AND_SECURITY_RESPONSE.md). This records design requirements and evidence boundaries; it does not claim every response is implemented or validated.


## Local image input

The existing Streamlit app can display an uploaded image. Image display does not itself perform AI detection; image analysis requires a compatible local coconut model and separate validation. This project does not include a live webcam workflow.


## Autonomous systems (software-level supervisor)

- [Autonomous system architecture, project-specific inputs, tests, and safety limits](docs/AUTONOMOUS_SYSTEMS.md)
- [Supervisor implementation](pui89_autonomy/supervisor.py) · [unit tests](tests/test_autonomy_supervisor.py)

The supervisor evaluates supplied status values and recommends an advisory mode: autonomous candidate, safe hold, manual recovery, or stopped. It does not acquire sensor data or command hardware. An autonomous-candidate result is not a safety certification; physical systems require independent safety controls and validation.

## Free-first AI engineering stack

This project adopts a small, cost-controlled toolchain rather than adding multiple overlapping AI platforms.

- **Computer vision:** OpenCV and PyTorch for local image processing and model experiments when the dataset is approved and hardware preflight passes.
- **Automation:** Python scripts and GitHub Actions for repeatable checks, annotation/data audits, and test summaries; Actions usage remains subject to GitHub quotas.
- **Testing and observability:** pytest, Ruff where configured, structured run records, versioned manifests, and reproducible benchmark reports.
- **Agent workflow:** use the existing rule-based decision-support agent first. Add LangGraph or another agent framework only if a concrete multi-step requirement cannot be handled cleanly with current code.
- **Retrieval:** use repository documentation and ordinary local search first; consider FAISS/Chroma only if a measured retrieval need appears.

**Cost and evidence guardrails:** no paid API, hosted inference, cloud GPU, subscription, or model download is required by this plan. Ask before introducing any cost. Review each model/weight licence separately. Do not begin detector training until image rights, annotations, independent review, and leakage-safe splits pass the existing data gates. CI passing is not detector or physical-robot validation.
