# Coconut Harvest AI Application

## Robot concept illustration

![Realistic-style low-cost Coconut Harvest AI concept with slim robotic arm, telescopic mast, and mixed-stage coconuts](docs/images/coconut-harvest-realistic-all-stage-concept.svg)

*Original realistic-style engineering concept artwork—not a photograph of a built robot. The concept shows young green, mature green/yellow-green, and brown/dry coconuts as separate per-fruit targets. Safe reach to 20–30 m palms, stability, cutting, fruit capture, and all-stage recognition remain unvalidated engineering goals.*


> **Complete-system architecture and acceptance gates:** [COMPLETE_SYSTEM_BLUEPRINT.md](docs/COMPLETE_SYSTEM_BLUEPRINT.md). This is a build-and-validation plan, not a claim of field-validated harvesting.
> **Current validation matrix:** [VALIDATION_MATRIX.md](docs/VALIDATION_MATRIX.md) — implementation evidence, automated checks, and remaining unvalidated capabilities.
> **All-stage coconut roadmap:** [COCONUT_STAGE_ROADMAP.md](docs/COCONUT_STAGE_ROADMAP.md) — proposed labels and workflow for young green, mature green, brown/dry, damaged, occluded, and uncertain fruit, with operator-selected harvest classes.
> **Candidate image triage (20 Oct 2026):** [CANDIDATE_IMAGE_TRIAGE_2026-10-20.md](docs/CANDIDATE_IMAGE_TRIAGE_2026-10-20.md) — contact-sheet triage of 30 candidates; this is not licence clearance or annotation approval.

## Per-coconut handling and image-quality review

The robot must make a separate decision for **each visible fruit**, even when a bunch contains different stages. The operator selects the intended harvest class before a task; the software filters candidates, but selection never overrides uncertainty, reach, collision, drop-zone, or human-confirmation checks.

| Per-fruit observation | Intended AI/application response | Robot action policy |
|---|---|---|
| Young green | Propose `young_green` only when the image and grower-defined criteria support it | Eligible only when the operator selected young fruit; otherwise skip |
| Mature green | Keep separate from young green; green colour alone is not proof of maturity | Eligible only after validated maturity criteria and required confirmation |
| Mature brown/dry | Propose `mature_brown_or_dry` with confidence and image evidence | Eligible only when selected and all safety/reach checks pass |
| Mixed-stage bunch | Detect and label each fruit independently; do not assign one label to the whole bunch | Filter each candidate separately |
| Partly hidden or overlapping | Mark visible fruit only when its boundary is supportable; flag occlusion/uncertainty | Request another view or human review; no automatic cut |
| Blurry, tiny, shadowed, or cropped at image edge | Mark uncertain if the whole fruit/class cannot be judged reliably | Do not cut automatically |
| Damaged or abnormal | Label for review, not as a normal harvest target | Reject from automatic harvesting unless a separately approved workflow applies |
| No safe reach, unclear 3D position, obstacle, person/animal nearby, or unsafe drop zone | Preserve the candidate record and explain the failed check | Do not issue a cutting action |
| Survey-only request | Detect/map candidates without choosing a harvest target | No cutting |

### Current candidate-image triage: what to keep, crop, replace, or exclude

The 30-image candidate set is **not approved for training**. The table below is first-pass visual triage from contact sheets, not final full-resolution inspection or licence clearance. Check the original file before cropping, drawing boxes, or accepting any image.

| Candidate ID(s) | Current issue / use | Recommended action |
|---|---|---|
| **0002, 0004** | Fruit are visible; existing boxes are only first-pass labels | **Review first at full resolution.** Check every box, missed fruit, false box, overlap, edge truncation, and stage label. Crop a *derived copy* only if the original fruit is too small to inspect; retain the untouched original and record crop coordinates/source hash. |
| **0001, 0010, 0014, 0015** | Possible fruit may be too distant or unclear in the contact sheet | Inspect original resolution. Keep only if individual fruit are genuinely visible and annotatable; otherwise retain as context/negative examples only if appropriate and rights-cleared. |
| **0003** | Collage/composite containing multiple coconut-related panels | Exclude from detector training unless the original panels are separated into individual files and each source/licence is independently verified. Do not draw boxes across the collage as if it were one natural scene. |
| **0007** | Harvest tool close-up, no fruit target | Exclude from fruit-detection positives; possibly retain in a separate tool/safety dataset later. |
| **0011** | Coconut processing scene, not a clear fruit-on-tree target | Exclude from fruit-detection positives unless the task and labels are explicitly changed. |
| **0018** | Appears to be a map/plantation graphic | Exclude from fruit-detection training. |
| **0023, 0024** | Seedlings/young plants rather than harvestable fruit targets | Exclude from harvest-fruit positives; do not label seedlings as young coconuts. |
| **0029** | Appears unrelated to coconut harvesting | Reject as irrelevant. |
| **0005–0009, 0012–0017, 0019–0022, 0025–0028, 0030** | Mostly harvesting context, people, tools, plantation panoramas, or distant palms; individual fruit are not clear in the contact sheet | Do not use as positive fruit examples based on the thumbnail. Inspect full resolution only if there is a specific reason; otherwise exclude from fruit positives or keep as separately labelled context/negative material after rights review. |

**Cropping and replacement rules**

- Never overwrite or delete the original image to improve a crop. Save crops as new files and record the parent filename/hash, crop coordinates, and source/licence.
- Crop only when the fruit remains naturally interpretable; do not crop away the stem, boundary, occlusion, or nearby fruit needed to understand the target. Keep some surrounding context.
- Do not enlarge a tiny fruit and treat interpolation as new visual evidence. If its boundary or stage cannot be judged, mark it uncertain or replace it with a better rights-cleared source.
- Replace an image only after checking source URL, creator, exact licence/permission, attribution requirements, dimensions, SHA-256, duplicate status, and annotation overlay.
- A photo of a palm, a person climbing, or a harvesting tool does not automatically provide a usable fruit-detection example.
- The contact-sheet review does not establish that all stages are represented. The set still needs verified examples of young green, mature green, mature brown/dry, damaged, occluded, and uncertain fruit.
- **Training remains blocked** until provenance/licence checks, independent box and maturity-label review, leakage-safe splits, and a frozen dataset manifest are complete. No model accuracy or physical harvesting capability should be claimed from these candidate images.

Full triage log: [CANDIDATE_IMAGE_TRIAGE_2026-10-20.md](docs/CANDIDATE_IMAGE_TRIAGE_2026-10-20.md).

## How the all-stage coconut robot is intended to work

The system is designed as a **human-supervised AI application connected to an agricultural robot**. It should first identify and assess each visible coconut, then propose a target based on the operator's chosen harvest stage. Detection is not the same as confirmed maturity, and a software demo is not proof of physical harvesting.

### 1. Choose a task

The operator selects one mode before the robot starts:

- **Young green:** consider only fruit confirmed under the project's grower-defined young-coconut criteria.
- **Mature green:** consider green fruit assessed as mature using validated criteria; do not infer maturity from green colour alone.
- **Mature brown/dry:** consider fruit assessed as mature or drying under the agreed criteria.
- **Selected combination:** consider only the classes selected by the operator.
- **Survey only:** detect, label, and map fruit without cutting.

The operator can also set a target limit and confirm the intended tree or row. The selection filters candidate fruit; it never disables a safety check.

### 2. See and classify each fruit

An RGB camera captures the bunch. A local vision model (once trained and validated) should detect individual coconuts and assign a provisional class, confidence, and image location. If available, calibrated depth or another validated sensor may help estimate 3D position.

Proposed classes include young green, mature green, mature brown/dry, damaged/abnormal, occluded/partial, and uncertain. A grower should define the class criteria for the local cultivar and intended use. Colour is a visual clue, not reliable proof of maturity on its own.

### 3. Filter targets and abstain when uncertain

The application compares each proposed class with the operator's selection. Fruit outside the selection is not sent to the harvest planner. Low-confidence, hidden, damaged, or ambiguous fruit is marked for review rather than cut automatically. Mixed-stage bunches are processed fruit by fruit, not assigned one class as a whole.

### 4. Check robot reach and safety

Before any physical action, the system must check that the target is within the validated reach envelope, the robot is stable, the path is clear, the tool is suitable, and the fruit can be lowered or dropped into a safe area. People and animals must be kept clear. A stop command, fault, lost sensor, collision risk, or unsafe condition must prevent cutting.

A small ground robot with a short arm cannot reach high palm crowns by itself. The high-reach mechanism, stability, cutting tool, fruit handling, and safe lowering method are separate engineering tasks that require supervised testing.

### 5. Ask for confirmation and record the outcome

The interface should show the target, predicted class, confidence, and proposed action. Human confirmation is required by default before cutting. The system should record whether the task was merely proposed, attempted, or independently confirmed as successful; it must not report a successful harvest without evidence.

### Development status and evidence

This workflow describes the intended design. It does **not** mean every class is already detected, that a trained all-stage model exists, or that the physical robot can harvest all coconut stages. The project must first complete image-source and licence checks, annotation review, a leakage-safe dataset split, local model training, and held-out per-class evaluation. Physical reach and harvesting must then be validated separately. See the [all-stage roadmap](docs/COCONUT_STAGE_ROADMAP.md) and [project status](docs/PROJECT_STATUS_2026-10-18.md).


> **A local-first AI application and simulation-first agricultural robot research project.** The goal is to explore whether computer vision, RGB-D localization, conservative task planning, and human-supervised safety gates can support safer coconut harvesting. This is a research prototype—not a finished or field-validated harvesting robot.

![Coconut Harvest AI workflow overview](docs/images/coconut-harvest-ai-overview.svg)

[Detailed project status, checks, next steps and future plan](docs/PROJECT_STATUS_2026-10-18.md)

## Product brief

See [docs/PRODUCT_BRIEF.md](docs/PRODUCT_BRIEF.md) for a concise description of the problem, current evidence, intended audiences, demonstration plan and milestones for potential partners and product stakeholders.


## Real-orchard robot design: mature-coconut detection and low-cost harvesting

**Design goal:** develop a cost-conscious agricultural AI system for coconut orchards, including tall palms approximately 20–30 m high. The first objective is dependable maturity assessment and fruit localization; physical harvesting is a separate engineering and safety challenge.

> **Important reach constraint:** a compact ground robot with a small arm cannot reach coconuts in a 20–30 m palm crown. Do not describe a short arm as capable of harvesting at that height. The system must separate ground-level perception and mobility from the high-reach harvesting method. Full autonomous harvesting remains a future research goal until a suitable mechanism is built and validated.

### Coconut-tree height range: 0–30 m

The **0–30 m range describes the trees the AI system may need to inspect—not a proven reach envelope for this robot**. The current artwork is conceptual; it does not demonstrate that the pictured arm can reach the crown or harvest successfully. The AI can be designed to detect, record, and rank fruit at different visible heights, but physical cutting is permitted only when a separately validated mechanism can reach the target safely.

| Approximate target height | Intended operating mode | Honest current status / gate |
|---|---|---|
| **0–3 m** | Ground-level perception and controlled, guarded test rig | First candidate band for supervised, non-cutting tests; harvesting still requires hardware, safety and success-rate validation |
| **3–6 m** | Extended mast or engineered lift/platform | Feasibility study only; verify stability, load, wind, reach and safe fruit capture before any cutting |
| **6–12 m** | Purpose-built high-reach or climbing system with independent retention | Research concept; not demonstrated by the pictured compact ground robot |
| **12–20 m** | Specialized access/harvesting mechanism, redundant retention and exclusion zone | Unvalidated research challenge; no claim of successful operation |
| **20–30 m** | Specialized tall-palm solution; assess alternatives to a ground-mounted arm | Out of current demonstrated capability; do not command a harvest based on AI detection alone |

**Per-tree decision:** estimate target height and uncertainty, check 3D localization, mechanism reach, stability, collision path, wind/conditions, fruit capture and a clear exclusion zone. If any check fails or is unknown, the system must report **SURVEY ONLY / NO CUT**. A target is counted as a successful harvest only after the fruit is safely detached and captured/controlled, verified by sensors or operator, and logged; a detection, simulation animation, or proposed cut is not a harvest success.

The project should report separate results by height band: detection precision/recall, localization error, reachability false-safe rate, safe task completion rate, successful fruit capture rate, fruit damage, aborts, collisions/near misses, and cycle time. Publish the denominator, failures, conditions and whether each result came from recorded images, simulation, or physical hardware. See [the full 0–30 m feasibility and acceptance plan](docs/TREE_HEIGHT_FEASIBILITY_0-30M.md).


### Proposed system architecture

```text
Ground robot / operator-guided platform
  ├── RGB camera (fruit appearance and colour)
  ├── Depth camera or LiDAR (range, obstacle and trunk geometry)
  ├── Optional IMU + wheel encoders (pose and motion estimate)
  ├── Onboard computer (initially existing laptop; edge computer later)
  └── Local AI application
       ├── Detect and track individual coconut candidates
       ├── Estimate maturity: mature/brown, green/immature, uncertain
       ├── Estimate 3D position and confidence when sensor data permits
       ├── Reject occluded, ambiguous or out-of-range targets
       ├── Record tree/cluster observations and review images
       └── Request human confirmation before any harvesting action

Separate harvesting subsystem (not yet validated)
  ├── Candidate A: human-operated pole/cutting tool guided by AI
  ├── Candidate B: purpose-built lightweight climbing/crown mechanism
  └── Candidate C: other engineered high-reach system after feasibility study
       └── Requires mechanical design, load analysis, redundant retention,
           controlled cutting, drop-zone management and supervised testing
```

The first two components to validate are **maturity detection** and **fruit localization**. Only after these work on representative orchard images should the project select and build a harvesting mechanism. A short arm may still be useful for a small controlled bench demonstrator, but it is not the high-reach solution.

### Operator-selectable harvest order: mature, young, or both

**The operator—not the AI alone—chooses which coconut stage to harvest for the current job.** Before a run, the local application should offer a clear harvest-order setting:

```text
HARVEST ORDER
  [ ] Mature coconuts (usually brown / mature-stage)
  [ ] Young coconuts (usually green / tender-stage)
  [ ] Both stages (show separate targets and ask before each action)

Additional controls:
  • Intended use: mature/dry coconut, drinking coconut, or grower-defined stage
  • Tree/row or selected cluster
  • Maximum targets and stop conditions
  • Human confirmation: ON by default
```

The AI should classify each visible fruit into **mature-stage**, **young-stage**, or **uncertain**; it then filters the candidate list using the operator's chosen order. For example, a mature-only job must not select a young coconut just because it is easy to reach. A young-only job must not select a mature coconut. If “both” is selected, the application should display the two classes separately and apply the correct harvest method for each only after that method has been engineered and validated.

“Brown” and “green” are visual clues, not universal ground truth: cultivar, lighting, weathering, and intended use can change what counts as harvest-ready. A grower should define the classes and labels for the orchard and product. If the model is uncertain, it must abstain and ask the operator rather than guess. The selected order changes **which targets the AI proposes**; it does not bypass reach, collision, drop-zone, tool, or safety checks. Any fruit high in a 20–30 m crown still requires a separately validated high-reach harvesting mechanism.

### How the robot should judge maturity

Colour is a useful signal, not a sufficient rule. Brown appearance can be affected by lighting, shadows, age, cultivar, dirt and image quality. The AI should combine visual cues where the dataset supports them and return **uncertain / request human review** when evidence is weak.

| Output | System behaviour |
|---|---|
| Mature/brown candidate | Show the detection, confidence and image evidence; mark for review |
| Green/immature candidate | Do not select for mature-fruit harvesting |
| Occluded, blurry or poorly lit fruit | Mark uncertain; ask for another viewpoint or human review |
| Conflicting maturity cues | Abstain rather than force a decision |
| Unsafe or unverified position | Do not issue a harvesting command |

A maturity label is not the same as proof that a coconut is ready for a particular use. Ground truth should be defined with an experienced grower and, where feasible, verified against harvest outcomes and the intended product (for example, mature dry coconut versus other harvest stages).

### Low-cost hardware plan

| Subsystem | Minimum viable starting point | Upgrade only when evidence shows it is needed |
|---|---|---|
| Camera | Existing phone/camera or affordable RGB camera for data collection | Calibrated RGB-D camera if range accuracy is needed |
| Range sensing | Fixed viewpoints and measured-distance trials first | RGB-D or 2D/3D LiDAR after testing sunlight, range and foliage effects |
| Compute | Existing laptop/desktop for offline inference | Low-power edge AI board after measuring latency and power |
| Mobility | Human-carried/handheld data collection first; then a simple wheeled base if useful | Tracked chassis only if orchard terrain tests justify it |
| Arm | No arm required for the first maturity-detection milestone | Small arm only for a safe, close-range bench demonstrator |
| Harvest mechanism | No automated cutting in the initial prototype | Separate high-reach feasibility study and risk review |
| Power/network | Local battery and offline logs; no cloud inference required | Size battery from measured system power and field duration |

Use free/open-source software and local processing wherever practical. Before buying hardware, collect representative data and test the proposed sensing setup. Prices, sensor ranges, sunlight performance and compute throughput must be checked against current vendor specifications and measured in the intended orchard; no specific hardware combination is guaranteed to work before those tests.

### Development and acceptance gates

1. **Define the harvest target.** Agree with an experienced grower on maturity classes, intended use, fruit-selection rules and unacceptable mistakes.
2. **Build a rights-cleared dataset.** Verify each image's source, licence, attribution, hash and relevance. Correct every selected annotation and complete an independent visual review. Do not train on the currently blocked candidate set.
3. **Train and evaluate a local baseline.** Freeze leakage-safe train/validation/test splits. Report precision, recall, mAP where appropriate, per-class results, false positives/negatives and failure examples. Do not publish estimated metrics as measured results.
4. **Test maturity classification.** Include different lighting, shadows, viewing angles, varieties, backgrounds, occlusion and fruit stages. Measure a confusion matrix and the rate of immature fruit incorrectly selected as mature.
5. **Measure localization separately.** Calibrate the sensor; compare estimated 3D positions with measured reference distances. Report error by range and condition, plus invalid/missing-depth rates.
6. **Run a supervised orchard survey.** Begin with perception-only trials from safe ground viewpoints. Record tree/cluster IDs, candidate locations, uncertainty and human corrections. Do not cut fruit.
7. **Select the harvesting mechanism.** Compare feasibility, reach, stability, mass, power, cost, maintenance and failure consequences. A lightweight climbing or high-reach mechanism needs a separate engineering design; do not assume a compact arm solves crown access.
8. **Validate safety before actuation.** Use simulation and guarded bench tests, independent emergency stop, fail-safe power behaviour, physical exclusion zones and human supervision. Never test cutting above people, roads, buildings, animals or unprotected equipment.
9. **Only then conduct controlled field harvesting trials.** Start with a qualified team, a documented risk assessment, a protected drop zone and staged acceptance criteria. Record success rate, damage, cycle time, intervention rate, downtime and near misses.

### Metrics to publish

- **Maturity:** precision/recall per maturity class, confusion matrix, and especially immature-fruit false-selection rate.
- **Detection:** precision, recall, mAP at stated thresholds, and results on a held-out test set.
- **Localization:** median and 95th-percentile 3D position error, invalid-depth rate, and performance by distance/lighting.
- **Field usability:** correct fruit candidates per tree, human correction rate, inference latency, power consumption and operating time.
- **Harvesting (only after a real trial):** successful detachment rate, fruit damage, missed targets, cycle time, operator interventions and safety incidents.

Always document dataset version, split manifest, model/checkpoint hash, code revision, device, software versions, confidence thresholds and test conditions. A CI pass, simulated run, concept illustration or model prediction is not evidence of successful physical harvesting.

### Current implementation status and honest scope

This section defines the **proposed engineering plan**, not a claim that the complete robot has been built. The repository's existing software prototype and automated tests do not establish a trained detector's held-out accuracy, maturity-classification reliability, real-world 3D localization, high-reach capability or successful physical harvesting. The dataset remains blocked pending image-rights checks, annotation correction and independent review, as described in the status notes above.

**Immediate priority:** finish the reviewed dataset and establish a reproducible local perception baseline. In parallel, gather grower input and conduct a no-cut feasibility study for safe access to fruit in tall palm crowns. Keep spending at $0 for now: use existing hardware, simulation and free/local tools until a specific purchase is justified by measured evidence.


## Latest automated CI verification — 20 October 2026

The latest Python test workflow passed on the current main-branch change in [run 39276683425](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39276683425). This confirms the configured automated software checks on that commit; it does **not** unblock the dataset, approve annotations, or establish detector accuracy or physical harvesting performance.

## Backup replacement candidates added — 20 October 2026

Because the first two candidates are still pending full-resolution download and annotation QA, three more alternatives have been recorded. Candidate C and D are listed as CC BY-SA 4.0; candidate E is listed as CC BY 4.0. They are **not approved training images** and must pass the same provenance, duplicate, annotation, geometry and independent visual-review gates. See [additional coconut image alternatives](docs/ADDITIONAL_COCONUT_IMAGE_ALTERNATIVES_2026-10-20.md). If any candidate fails, reject it and test the next alternative rather than forcing a poor label.

## New replacement candidates identified — 20 October 2026

Two additional Wikimedia Commons source pages with visible coconut clusters and CC BY-SA 4.0 licensing have been recorded for review. They are **candidates only**: they have not yet passed local download/hash verification, annotation, independent visual QA, or dataset approval. See [external replacement candidates and attribution checklist](docs/EXTERNAL_REPLACEMENT_CANDIDATES_2026-10-20.md). Do not train on or publish draft labels for these images until the review gates pass. A separate [preliminary visual triage of the original 30-image candidate batch](docs/PRELIMINARY_VISUAL_TRIAGE_2026-10-20.md) also records obvious task-mismatch images to exclude or review; it is not a licence or annotation approval.

## Latest status update — 20 October 2026

- **Current status: dataset is still blocked from training.** The first-pass labels have unresolved visual-review warnings. The 30-image contact sheet has now received a preliminary task-relevance screen; obvious mismatches are documented in [the visual-triage report](docs/PRELIMINARY_VISUAL_TRIAGE_2026-10-20.md). This screen is not source-rights clearance or label approval. The two previously reviewed labelled images (0002 and 0004) passed basic coordinate-boundary checks, but overlapping boxes on 0002 and border-touching boxes on 0004 still require human review; geometry checks alone do not approve annotations.
- **Dataset QA actions taken:** candidate 0033 was judged too shadowed for the first clean replacement; candidate 0032 (`Coconut_in_Coconut_Tree.jpg`) was selected for further review after checking the original Commons source page, CC BY-SA 4.0 terms, attribution and matching SHA-1. A temporary draft overlay/annotation was generated for 0034 and geometry-checked (valid coordinates, one border-touching box and one overlap warning at IoU 0.15). This is not label approval: the draft still needs boundary correction, missed-fruit review and independent second review.
- **Data handling:** unapproved images and labels must remain in temporary artifacts/review files. Do not commit or publish unverified images, annotations, or model outputs as a finished dataset. The earlier 30-image candidate artifact has its own expiry noted below; download it before 25 October 2026 if it is still needed.
- **Already evidenced:** the repository has dataset collection, provenance/review, annotation, conversion and split-audit tooling. The earlier candidate collection produced 30 candidates; that count is not the count of licence-cleared or training-ready images.
- **Not yet established:** an approved complete dataset, trained detector performance, held-out precision/recall/mAP, measured RGB-D localization accuracy, safe collision-free robot motion, or physical coconut harvesting.
- **Next sequence:** finish human correction and independent review of 0032/0034 → verify every selected image's rights and annotations → audit duplicates and group-separated splits → train a local baseline only after dataset approval → publish reproducible held-out metrics and failure examples → validate robot geometry and stop behavior in simulation. Two new Wikimedia source pages were re-opened and their original images visually checked in-browser; local downloads, hashes and annotations remain pending in [the candidate ledger](docs/EXTERNAL_REPLACEMENT_CANDIDATES_2026-10-20.md).
- **Cost and safety boundary:** remain local-first and free/open-source-first; no paid inference API or physical actuator commands are required for dataset QA. Concept art and passing CI are not evidence of field performance.

## Previous status update — 18 October 2026

- **Successful:** Python CI passed on 3.10/3.11/3.12 in [run 39096443251](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39096443251); candidate collection generated 30 image candidates and provenance/review files; Pages deployment passed. This verifies automated software checks only—not detector accuracy or physical harvesting.
- **Dataset QA update (19 Oct):** the 30-image candidate batch is triaged; candidates 0001, 0002, 0004 and 0014 have independently checked Commons source pages. Candidate 0010 was excluded from positive detection data after full-resolution review. The two labelled images (0002: 9 boxes; 0004: 6 boxes) were overlaid; the geometry audit found no out-of-bounds coordinates, but flagged two overlapping box pairs on 0002 and border-touching boxes on 0004. These are review warnings, not automatic corrections. Labels still need independent visual QA; the other 26 source pages are not cleared. See the [annotation QA audit](docs/ANNOTATION_QA_AUDIT_2026-10-19.md), [source-rights ledger](data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv), and [candidate batch report](docs/CANDIDATE_IMAGE_BATCH_2026-10-18.md).
- **Continuing:** full-resolution image and licence review, human annotation, dataset QA and leakage-safe splits.
- **Next:** download the temporary candidate artifact before 25 October 2026; label approved images; run dataset audits; then perform a reproducible local baseline and frozen held-out evaluation.
- **Future:** measure detection and RGB-D localization, validate robot geometry/collision/safe-stop behavior in simulation, and only later consider supervised non-cutting hardware tests.
- **Corrections:** no trained-detector metrics, RGB-D benefit, safe physical motion or real harvesting are established. CI success and concept artwork are not field-performance evidence. Free/local-first; no paid cloud service is required.



## Live project overview — 18 October 2026

This table is the current evidence-based status, not a claim that the full robot is complete.

| Area | Status now | Evidence / boundary |
|---|---|---|
| Application and workflow prototype | **Implemented prototype** | Local detector adapter, RGB-D proposal/localization interface, simple IoU tracking baseline, decision gates, simulation workflow and JSON audit reporting are present in the repository. |
| Software regression checks | **Partly verified by CI** | The recent free-image-candidate workflow and GitHub Pages deployment succeeded. These check those workflows only; check the [Actions page](https://github.com/Pui89/Coconut-Harvest-AI/actions) for the latest application/test workflow status. |
| Dataset preparation | **Tools implemented; dataset not yet validated** | Free candidate-image collector, licence/provenance gallery, offline bounding-box annotator, YOLO conversion, reviewed dataset builder and split-leakage audit are available. Candidate images still need human review, licence checks and labels. |
| Trained coconut detector | **Not yet evidenced** | No verified held-out benchmark result is claimed here. Do not treat a model adapter, demo, candidate gallery or synthetic fixture as proof of accurate detection. |
| RGB-D localization and tracking | **Prototype only** | Interfaces and a simple tracking baseline exist; real camera calibration, depth quality and localization error must be measured independently. |
| Robot planning and physical harvesting | **Not validated** | No claim of safe autonomous cutting, successful physical harvesting, orchard field trials or production readiness. No actuator commands are authorized by the current software workflow. |

### What has succeeded
- The repository contains separable application and robot-workflow components, automated tests, synthetic fixtures and audit-oriented reporting.
- Fail-closed decision gates are intended to reject missing or invalid evidence instead of treating it as a safe target.
- Free-first dataset preparation and offline annotation tools are in the repository; the workflow does not require a paid inference API.
- The latest candidate-image collection workflow completed successfully and collected **30 candidate images**; its gallery builder recorded 30 candidate records and the workflow uploaded a 15.6 MB artifact containing the images and provenance/review files. [View run and download the artifact](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196). These are **unreviewed candidates**, not a labelled dataset; some search results may be irrelevant, and some downloads were rate-limited. The artifact expires on 25 October 2026 unless downloaded beforehand.

### What is in progress
- Turn the candidate-image tools into a human-reviewed, licence-checked, labelled dataset.
- Create group-separated train/validation/test splits and audit for leakage before model training.
- Run a reproducible local baseline training and held-out evaluation; save commands, package versions, dataset provenance, checkpoint hash, raw outputs and failure examples.
- Measure localization/tracking separately from detection, then test the end-to-end workflow in simulation with explicit safety stops.

### Next actions, in order
1. Download the generated [coconut-image-candidates artifact](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196) before it expires; review the images and source licences. The collection workflow has already run on GitHub, so no local collection command is needed for this first batch.
2. Label only relevant, clearly visible coconuts using the [offline annotator](tools/coconut_annotator.html); exclude irrelevant or ambiguous images.
3. Build and audit dataset splits with the scripts linked in [training documentation](training/README.md). Keep image datasets and model weights out of Git.
4. Train a local baseline only after checking the base checkpoint licence and available hardware; freeze the test split before tuning.
5. Publish a results report with dataset size, split counts, precision, recall, mAP where applicable, false positives/negatives, latency, confidence threshold, hardware and known failure cases. If no run has been performed, mark results **not measured** rather than estimating numbers.
6. Validate RGB-D calibration and localization error; then improve robot-model geometry, reachability, collision checks and stop/fault behaviour in simulation.
7. Consider a guarded, non-cutting hardware feasibility test only after documented risk review and qualified supervision.

### Future target
A research-grade, locally runnable agricultural AI system with independently measured perception, localization and simulation performance; transparent safety limits; and a controlled path toward supervised field trials. Commercial claims about speed, safety, cost savings or superiority over other systems must wait for fair, documented comparisons.

**Current honest conclusion:** useful prototype and engineering/test scaffolding are in place. The key missing evidence is a real, reviewed dataset plus a trained detector's held-out results, followed by validated spatial and robot-safety tests.


## Project status at a glance

| Status | What it means today |
|---|---|
| **Implemented prototype** | Local detector adapter, camera-frame RGB-D localization, simple IoU tracking baseline, configurable decision gates, simulated task workflow, and JSON audit reporting are present in the codebase. |
| **Testable with synthetic inputs** | A deterministic simulation workflow and clearly labelled synthetic fixtures let developers test decisions without a physical robot or paid cloud inference. |
| **Automated CI** | The current feature branch passed both GitHub Actions jobs: the focused/application test workflow and the dedicated end-to-end simulation workflow. This validates software tests, not real-orchard accuracy or robot safety. |
| **Not demonstrated** | Autonomous physical harvesting, safe palm climbing, real cutting/grasping, field success rate, and production readiness. |

### What has been achieved

- Built separate AI-application and robot-workflow components that can be inspected and tested.
- Added fail-closed checks so missing or invalid evidence should not be treated as a safe robot target.
- Connected local vision proposals to a simulation-only workflow through an explicit calibration/evidence interface.
- Added unit and integration tests, synthetic fixtures, documentation, and a proposed CI test path.
- Added an offline browser-based coconut bounding-box annotator, a JSON-to-YOLO converter, and a train/validation/test leakage audit script.
- Kept the software local-first: no paid inference API, no automatic model-weight download, and no physical actuator commands.

### What is being worked on

- Keeping both GitHub Actions workflows green as the branch changes.
- Rechecking the demo and local run instructions from a clean checkout.
- Separating synthetic examples from measured results and documenting each limitation.
- Preparing a practical benchmark for detection, localization, tracking, safety rejection, and task simulation.

### What comes next

1. **Reproducibility:** keep the passing focused and repository test suites repeatable from a clean environment.
2. **Real-image benchmark:** assemble a permitted, labelled orchard dataset and report held-out detection precision/recall and failure cases.
3. **Spatial validation:** measure RGB-D localization error and validate camera-to-robot calibration; never use the synthetic identity transform for hardware.
4. **Physics simulation:** validate robot geometry, joint limits, reachability, collision checking, tool envelope, and safe-stop scenarios in a simulator.
5. **Controlled prototype:** only after independent risk review, test a guarded, non-cutting rig under qualified supervision.
6. **Commercial pilot:** compare measured safety, successful collection rate, cycle time, fruit damage, operator intervention, and total cost against the current harvesting process.

## Why a farm or company might evaluate this project

The possible value is a local-first, auditable, human-supervised workflow that can be tested before committing to expensive robot hardware. Its intended direction is to help operators assess targets and plan work while reducing the need for some hazardous climbing tasks. These benefits are hypotheses, not measured outcomes.

**Honest buying position:** this project is not ready to be sold as a functioning autonomous coconut-harvesting robot. A suitable current partner would be a research group, farm, or company interested in a feasibility study, data collaboration, or simulation benchmark. No claim of being better, faster, cheaper, or safer than another robot is justified until an agreed comparison is measured.

- [Buyer value, competitive comparison, and evidence required before a pilot](docs/BUYER_VALUE_AND_COMPETITIVE_POSITIONING.md)
- [End-to-end workflow and safety limitations](docs/END_TO_END_ROBOT_WORKFLOW.md)
- [Application setup and local detector requirements](apps/pui89_app/README.md)
- [Development roadmap](docs/DEVELOPMENT_ROADMAP.md)
- [Reproducible benchmark protocol](docs/REPRODUCIBLE_BENCHMARK_PROTOCOL.md)
- [One-command local baseline training and held-out evaluation](scripts/run_coconut_baseline.ps1)
- [Safety state machine and release gates](docs/SAFETY_STATE_MACHINE.md)
- [Research evidence matrix: implemented vs. unvalidated](docs/RESEARCH_EVIDENCE_MATRIX.md)
- [Cost and billing policy](docs/COST_SAFETY_AND_BILLING.md)
- [First candidate-image batch: provenance, preliminary visual triage, and required review](docs/CANDIDATE_IMAGE_BATCH_2026-10-18.md)

---

## Free local Hugging Face model plan

This repository's recommended local model, intended tasks, licence checks, setup notes, and no-surprise-billing rules are documented in **[HUGGINGFACE_LOCAL_MODELS.md](docs/HUGGINGFACE_LOCAL_MODELS.md)**.

**Cost boundary:** the plan uses downloaded local weights only; it does not require paid Hugging Face inference, cloud GPUs, paid notebooks, or a subscription. Model integration and performance must be verified by running tests locally.


## Quick start: create a free candidate-image review gallery (Windows)

This is the shortest practical route to start without owning coconut photos. It downloads a **small candidate batch** from Wikimedia Commons and builds a local gallery so you can reject irrelevant images and verify each source licence. It does not automatically label images or create a validated orchard dataset.

~~~powershell
# First change into the cloned repository folder (the folder containing README.md)
cd C:\\path\\to\\Coconut-Harvest-AI

python -m pip install -r tools/requirements-data.txt
python tools/collect_commons_coconuts.py --out data/commons_candidates --limit 30
python tools/build_candidate_gallery.py --collection-dir data/commons_candidates
Start-Process (Resolve-Path data/commons_candidates/review_gallery.html)
~~~

**Important on Windows:** run the commands above in **PowerShell**, not Command Prompt (`cmd.exe`), because `Start-Process` is a PowerShell command. Replace `C:\\path\\to\\Coconut-Harvest-AI` with your actual repository path. Before running anything, confirm you are at the repository root by running `dir`; you should see `README.md`, `apps`, `tools`, and `training`. If Python says `No module named 'apps'`, or says it cannot open `tools\\...`, you are in the wrong folder. In Command Prompt, you can open PowerShell by typing `powershell`, then change to the repository folder with `cd /d "C:\\path\\to\\Coconut-Harvest-AI"`. Do not run these repository commands from `C:\\Users\\ACER` unless that is actually where the repository's files are.

The downloaded images and gallery stay on your computer. The collector writes `provenance.csv` with source URLs and licence metadata. Open each original file page and verify the exact licence/attribution terms before using the image, especially for redistribution or commercial use. Search results may include non-orchard images; discard those rather than pretending they represent harvesting conditions.

**Then label reviewed images:** open [the offline annotator](tools/coconut_annotator.html) from a local checkout, choose the reviewed image files, draw a box around every clearly visible coconut, and export the JSON. Use the [reviewed dataset builder](training/build_dataset_from_annotations.py) to package the images and labels into reproducible group-separated train/validation/test splits after recording human review and licence verification. Keep the dataset and weights out of Git.

**Current collection status:** GitHub Actions has collected the first 30 candidate images and built a review gallery. The generated artifact is temporary (7-day retention). A valid dataset and real benchmark still require image relevance review, licence verification, annotation, independent group-separated train/validation/test splits, and an actual training/evaluation run.

## Start without your own photos

Use the free Wikimedia Commons collector to build a candidate image collection with recorded licence and attribution metadata: [collection guide](docs/FREE_IMAGE_COLLECTION_GUIDE.md), [collector script](tools/collect_commons_coconuts.py). It does not create labels automatically and it does not guarantee that each image is an orchard scene. Review every image and licence, then use the [offline browser annotator](tools/coconut_annotator.html) and [YOLO conversion script](tools/convert_annotations_to_yolo.py) to prepare reviewed labels before training.

## Train and evaluate a real coconut detector

Before reporting results, create a reproducibility manifest that records the dataset YAML checksum, configured split paths and image counts, Git commit, package versions, available GPU, and (if supplied) checkpoint SHA-256. From the repository root:

```powershell
python training/create_experiment_manifest.py --data "C:\datasets\coconut\coconut.yaml" --weights "runs\coconut\train\weights\best.pt" --experiment-id "coconut-test-v1" --output "reports\coconut-test-v1-manifest.json"
```

After evaluation, cross-check the manifest against the test report with [the provenance audit](training/audit_experiment_report.py):

```powershell
python training/audit_experiment_report.py --manifest "reports\coconut-test-v1-manifest.json" --report "reports\coconut_test_report.json" --output "reports\provenance_audit.json"
```

A non-zero exit means one or more provenance checks failed; inspect the JSON and resolve mismatched checksums or missing fields before sharing results. This verifies file identity consistency only, not label correctness or real-world performance.

The manifest is provenance metadata, **not an experiment result**. It does not validate image licences or labels, and it does not run training or evaluation. See [the script](training/create_experiment_manifest.py). The file is generated locally; review it before sharing because it includes local paths and environment details.

## Train and evaluate a real coconut detector

The local training, offline annotation, YOLO conversion, and held-out evaluation workflow is documented in [training/README.md](training/README.md). Tools include the [Commons image collector](tools/collect_commons_coconuts.py), [local review-gallery builder](tools/build_candidate_gallery.py), [offline annotator](tools/coconut_annotator.html), [reviewed dataset builder](training/build_dataset_from_annotations.py), [label QA preview gallery](tools/preview_yolo_labels.py), [annotation converter](tools/convert_annotations_to_yolo.py), and [dataset split audit](training/audit_dataset_splits.py). Dataset access/licensing and the current free-data search are documented in [FREE_DATASET_AND_TRAINING_WORKFLOW.md](docs/FREE_DATASET_AND_TRAINING_WORKFLOW.md).

These scripts do not include a trained checkpoint or claim accuracy. You must supply a permitted labelled dataset and an existing local base checkpoint, then run training and the frozen test evaluation yourself. The existing [RGB-D proposal pipeline](apps/pui89_app/local_first_pipeline.py) connects a local coconut model to a review-only JSON proposal; calibrated depth and safety evidence remain necessary, and no hardware commands are sent.

## Local development on an RTX 3050 laptop

The hardware-aware, zero-cost-first plan is in [LOCAL_EXPERIMENT_PLAN_RTX3050.md](docs/LOCAL_EXPERIMENT_PLAN_RTX3050.md). A read-only environment checker is available at [scripts/check_local_environment.py](scripts/check_local_environment.py); it does not install packages, download models, use the network, or change system settings. The plan is tailored to a reported RTX 3050 Laptop GPU with 4 GB VRAM and 16 GB system RAM. It distinguishes the existing synthetic prototype from future model experiments and measured results.

## Try the Interactive AI Application Example

Want to see an example instead of only reading about the concept? The repository includes a small Streamlit demo where you can upload an orchard photo for display, adjust example sensor/coconut evidence, run the decision-support rules, and download a JSON report.

**[Open the web demo source and setup instructions](apps/pui89_app/README.md)** · [View the interactive demo code](apps/pui89_app/web_demo.py)

Run it locally from the repository root:

```bash
python -m pip install -r apps/pui89_app/requirements.txt
streamlit run apps/pui89_app/web_demo.py
```

**Demo limitation:** the uploaded photograph is displayed for context but is not automatically analysed by a trained detector. The output is based on manually entered values and illustrative rules; it is not a real-world harvesting result or robot control system.


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

- **PUI89 Research** — universities, researchers, and potential product partners
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
- [12-Month Roadmap](docs/PUI89_12_MONTH_ROADMAP.md)
- [Cost Safety and Billing Policy](docs/COST_SAFETY_AND_BILLING.md)

## End-to-end simulation demo



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
│   │   ├── harvest_pipeline.svg
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
| Simulation workflow and model assets | Simulation-related files are included; physical harvesting is not demonstrated. |
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


## Local-first AI application and simulated agricultural robot

The current repository includes an optional local detector adapter, RGB-D camera-frame localization, a simple IoU tracking baseline, and a deterministic simulation-only harvesting workflow. The workflow accepts supplied candidate evidence, applies conservative preflight gates, produces an auditable JSON report, and simulates approach/tool/retract steps. It never sends physical actuator commands.

- [End-to-end workflow guide](docs/END_TO_END_ROBOT_WORKFLOW.md)
- [Application usage and local detector setup](apps/pui89_app/README.md)
- [Simulation example input](examples/end_to_end_robot_workflow.example.json)
- [Run the simulation](apps/pui89_app/run_robot_workflow.py)

From the repository root, run:

```bash
python -m apps.pui89_app.run_robot_workflow --input examples/end_to_end_robot_workflow.example.json
```

The example is synthetic evidence for software testing, not a measured field result. Local image inference requires a detector model that you supply and trust; no model weights are bundled or downloaded automatically. The RGB-D estimate is in the camera frame until calibrated transforms are validated. This remains a research prototype, not a physically validated harvesting robot.


### End-to-end workflow smoke test (synthetic data)

The following command connects a labelled synthetic proposal to the simulation-only task workflow. It is useful for testing the software path, not for measuring real detection or harvesting performance:

```bash
python -m apps.pui89_app.vision_to_workflow --proposal examples/coconut_robot_proposal.synthetic.example.json --evidence examples/coconut_robot_evidence.synthetic.example.json --human-approved --output coconut_simulated_workflow_report.json
```

The example uses a synthetic identity transform and synthetic robot evidence. **Do not reuse these values for a physical robot.** The workflow never sends actuator commands.

- [Visual workflow overview](docs/images/coconut-harvest-ai-overview.svg)
- [Competitive positioning and buyer validation checklist](docs/BUYER_VALUE_AND_COMPETITIVE_POSITIONING.md)


## Candidate review and first measured baseline — 18 October 2026

The first candidate batch has now been visually triaged across all 30 images. The review ledger, first-pass labels, benchmark script and raw benchmark report are committed under [data/review_batch_2026-10-18](data/review_batch_2026-10-18/README.md).

- **Review:** all 30 candidates have a recorded visual decision; most are excluded from attached-fruit detection due to irrelevant context, seedlings, distant fruit, or insufficiently clear targets.
- **Labels:** 15 first-pass boxes across two close-up images. These labels need independent QA; this is not yet a complete or representative dataset.
- **First measured baseline:** the fixed OpenCV HSV-contour heuristic returned 0.000 precision, 0.000 recall and 0.000 F1 at IoU ≥ 0.50 across those two images (20 predicted boxes, 15 reference boxes; mean CPU runtime 15.12 ms/image). This is a deliberately simple non-ML smoke test, not a trained detector benchmark.
- **Licensing:** source pages for candidates 0001, 0002 and 0004 were checked; other candidates are not independently cleared for dataset inclusion. Only 0002 and 0004 have first-pass boxes.
- **Still required:** independent annotation QA, source-page checks for every image proposed for inclusion, more independent orchard scenes, leakage-safe grouped splits, and a trained model with a frozen held-out evaluation. No generalization claim is supported by two images.
