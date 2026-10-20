# Coconut Harvest Planning Agent

A zero-cost-first, local decision-support prototype for the Coconut Harvest AI repository. It uses only the Python standard library.

## Run it

From the repository root, Python 3.10 or later is sufficient:

```bash
python agents/harvest_planning_agent.py
python agents/harvest_planning_agent.py --output agent_report.json
```

The command-line demo defaults to `--harvest-mode all_mature`, which considers only candidates labelled `mature_green` or `mature_brown_or_dry`. All example values are synthetic.

## Operator-selected harvest modes

Use a JSON file such as [the synthetic all-stage candidate example](../examples/all_stage_harvest_candidates.example.json):

```bash
# Mature green AND mature brown/dry
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode all_mature

# Mature green only
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode mature_green

# Mature brown/dry only
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode mature_brown_or_dry

# Young green only (only if the operator intentionally requests this class)
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode young_green

# Survey only: never propose a harvest target
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode survey_only

# Explicitly select a combination of mature stages
python agents/harvest_planning_agent.py --input examples/all_stage_harvest_candidates.example.json --harvest-mode selected_combination --selected-stage mature_green --selected-stage mature_brown_or_dry
```

Each candidate has a `target_id`, `confidence` (0–1), optional `x_m`, `y_m`, `z_m` coordinates, a `reachable` value, an `occluded` flag, and a `stage` label. Supported stage labels are:

- `young_green`
- `mature_green`
- `mature_brown_or_dry`
- `flower_or_infant`
- `damaged_or_abnormal`
- `occluded_or_partial`
- `uncertain_stage`

The operator's mode filters which supplied stage labels may be considered. Uncertain, damaged, occluded, and infant/flower candidates are not eligible for automatic harvest in the stage-filtered modes. Missing 3D position or unconfirmed reachability is rejected. Survey-only mode always returns no harvest proposal.

## What the prototype does—and does not do

1. Applies transparent confidence, range, occlusion, stage-selection and reachability checks.
2. Ranks candidates that pass those configured checks for **simulation review only**.
3. Emits a JSON proposal with reasons for rejected candidates and the selected mode.
4. Explicitly records that no actuator command was sent and physical execution is not authorized.

**Critical limitation:** this agent does not detect coconuts from image pixels or determine their biological maturity. Candidate stage labels are supplied by a caller or a human reviewer. Colour alone is not proof of maturity; local class criteria should be defined with a knowledgeable grower. The example JSON is synthetic and is not a real orchard dataset or model output.

## Zero-cost implementation

The core version needs no model download, API key, subscription, or cloud service. For a later vision experiment, use a locally supplied, appropriately licensed model only after dataset provenance, annotation review, leakage-safe splits, and held-out evaluation are complete. Do not add direct motor, cutter, gripper, or actuator access to this agent.

## Safety boundary

`ELIGIBLE_FOR_SIMULATION_REVIEW` means only that supplied fields passed this prototype's configured checks. It is not a finding that a target is safe to harvest. A real robot needs calibrated sensors, validated reachability and independent collision checking, a robot-specific safety controller, emergency-stop tests, and supervised trials. Never connect this script directly to physical actuators.
