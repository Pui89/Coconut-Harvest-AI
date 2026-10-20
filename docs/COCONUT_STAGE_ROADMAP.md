# All-Stage Coconut AI Robot Roadmap

## Goal

Develop a low-cost, local-first coconut perception system that can identify different visible coconut development and condition states, while allowing the operator to choose which class or classes are eligible for harvesting.

**Status:** The local rule-based planning agent now supports operator-selected stage filtering for supplied candidate records, with a synthetic example and automated tests. This is not an image-based maturity classifier, trained all-stage detector, or proof that a physical robot can harvest any stage. The dataset, labels, model, reach mechanism, and safety controls must be validated separately.

## Proposed visual label set

Use these as proposed annotation labels. Have an experienced coconut grower define the local criteria before treating labels as biological maturity ground truth.

| Label | Meaning | Default harvest behaviour |
|---|---|---|
| `flower_or_infant` | Flowers or extremely small newly forming fruit, only if included in the project's scope | Never harvest automatically |
| `young_green` | Developing green coconut under the agreed local criteria | Consider only if the operator explicitly selects this class and grower criteria allow it |
| `mature_green` | Coconut assessed as mature under local criteria but still green | Consider only if selected and confirmed by the maturity rule |
| `mature_brown_or_dry` | Brown/drying mature coconut under agreed criteria | Consider only if selected and confirmed |
| `damaged_or_abnormal` | Visible damage, decay, or abnormal appearance | Reject for automatic harvest; request human review |
| `occluded_or_partial` | Fruit is too hidden or cropped to assess reliably | Do not harvest automatically |
| `uncertain_stage` | The stage cannot be established confidently | Do not harvest automatically |

A single fruit may have different colour depending on cultivar, age, weather, lighting, and camera. Colour alone must not be treated as proof of maturity. If a fruit is visible but maturity cannot be verified from the image, annotate it as uncertain rather than guessing.

## Implemented prototype: operator-selected modes

The standard-library-only agent at [`agents/harvest_planning_agent.py`](../agents/harvest_planning_agent.py) implements stage filtering for supplied candidate records. Its command-line demo defaults to `all_mature`:

- `young_green`: only operator-selected young green candidates.
- `mature_green`: only mature green candidates.
- `mature_brown_or_dry`: only mature brown/dry candidates.
- `all_mature`: mature green and mature brown/dry candidates.
- `selected_combination`: explicitly list selected eligible stages with repeated `--selected-stage` options.
- `survey_only`: never propose a harvest target.

The agent rejects uncertain, damaged, occluded, and flower/infant candidates in stage-filtered modes. It also requires supplied 3D coordinates and explicit reachability under the default checks. Results are for simulation review only; no actuator commands are sent.

Reproduce the synthetic example from the repository root:

```bash
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode all_mature
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode young_green
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode survey_only
python -m pytest -q tests/test_harvest_planning_agent.py
```

**Important:** stage labels in the example are synthetic inputs. This agent does not classify image pixels or infer maturity. The stage-selection logic demonstrates the operator's intended selection policy, not a working trained vision system.

## Planned operator controls

The full operator interface should additionally support:

- **Harvest selection:** young green / mature green / mature brown or dry / selected combination / survey only.
- **Target limit:** maximum number of fruit per tree or task.
- **Confidence rule:** low-confidence or uncertain fruit is sent for review.
- **Human confirmation:** enabled by default before any cutting action.
- **Stop controls:** stop on people or animals nearby, unstable robot pose, unexpected movement, tool fault, collision risk, loss of communications, or an unsafe drop zone.

Selecting a class is only a request filter. It never overrides safety checks, reach limits, tool constraints, or the need to confirm the fruit is safe to harvest.

## Perception and decision pipeline

1. Capture an image using an existing RGB camera; use depth only if available and validated.
2. Detect each visible coconut separately using a model trained and evaluated on reviewed data.
3. Assign a provisional visual class and confidence.
4. Mark fruit as uncertain when the image does not support a reliable decision.
5. Apply the operator's requested class filter (the supplied-record rule-agent portion is implemented; image-derived classification is not yet established).
6. Estimate target location only with a calibrated, tested method.
7. Check reach, collision clearance, robot stability, tool state, and drop zone.
8. Show the proposed target and class to the operator.
9. Execute only after required confirmation and safety interlocks pass.
10. Record the result for review; do not label a target as successfully harvested unless a sensor or human verifies the outcome.

## Dataset and evaluation requirements

Before training:

- Verify the original image source, reuse licence, required attribution, and file integrity for every image.
- Review every bounding box and class label; use an independent second review for maturity labels.
- Include diverse cultivars, lighting, viewpoints, backgrounds, occlusion, bunches containing mixed stages, and difficult negative examples.
- Split data by tree, orchard, capture session, or source group to reduce leakage between training and test sets.
- Keep an untouched held-out test set.
- Report per-class precision, recall, confusion matrix, and missed/incorrect maturity selections. Report localization metrics where appropriate.
- Do not publish a performance number until the experiment has actually been run and its configuration and data split are recorded.

## Free, local-first implementation order

1. Audit and preserve existing candidate images and metadata.
2. Confirm image licences and remove uncleared files from the training set.
3. Define label rules with a knowledgeable grower.
4. Independently review annotations and add missing stages only when evidence supports the label.
5. Train a small local baseline using free/open-source tools on available hardware.
6. Evaluate per class on a leakage-safe held-out set.
7. Connect reviewed image-derived classes to the operator-selected filtering workflow.
8. Test perception and stop behaviour in simulation or bench tests.
9. Validate reach and physical harvesting separately under supervised, controlled conditions.

No paid API, cloud inference, or paid dataset is required by this roadmap. Training speed and feasibility depend on available hardware.

## Current limitations

The project's previously recorded status reports candidate images and first-pass boxes, but not a fully licence-cleared, independently reviewed, all-stage dataset or a trained detector with valid held-out metrics. The operator-selection rule is implemented only for supplied stage labels; all-stage image detection and classification remain goals until those gates are completed.

A compact ground robot cannot reach high palm crowns with a short arm alone. High-reach hardware, stability, cutting, fruit handling, and safe lowering require separate engineering and validation. Never claim real-world harvesting for a stage based only on detection images or a software demo.
