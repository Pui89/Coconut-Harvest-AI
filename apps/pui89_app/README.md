# PUI89 Coconut Harvest AI Application

A simulation-first decision-support application for demonstrating sensor-quality checks, transparent candidate rules, conservative decisions and JSON reporting. It does not run a trained coconut detector by itself and never commands physical actuators.

## Interactive web demo

The Streamlit demo lets you upload a real orchard photo for display, adjust example sensor/candidate evidence, run the rule-based decision flow, and download a JSON result.

**Important:** the photo is not automatically analysed. The scores and decisions are based on manually supplied values and illustrative rules, not a trained computer-vision model or validated field measurements.

## Run the web demo locally

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r apps/pui89_app/requirements.txt
streamlit run apps/pui89_app/web_demo.py
```

Your browser should open the local app. Upload an orchard image if you want, adjust the sensor checks and candidate evidence, then click **Analyse candidate**. The JSON result can be downloaded from the page.

## Run the API

```bash
python -m pip install -r apps/pui89_app/requirements.txt
uvicorn apps.pui89_app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API schema and interactive requests.

## API

- `GET /health` — service status and actuator boundary.
- `POST /analyze` — sensor quality checks, candidate ranking and gated harvest proposals.
- `GET /metrics` — process-level request counters; not a model benchmark.

Example JSON:

```json
{
  "rgb_available": true,
  "depth_valid": true,
  "timestamp_skew_ms": 8,
  "candidates": [{
    "target_id": "coconut-01",
    "ripeness_score": 0.91,
    "localization_confidence": 0.94,
    "distance_m": 2.1,
    "obstacle_clearance_m": 0.45,
    "stable_track_frames": 12
  }]
}
```

## Safety and evidence

- Missing/degraded inputs or excessive timestamp skew trigger `SAFE_HOLD`.
- Candidates failing confidence, tracking, reachability or clearance gates are rejected or sent for review.
- `PROPOSAL_APPROVED_NOT_EXECUTED` means only that configured software gates passed; it is not authorization to move a robot.
- The Streamlit photo upload is for display only; it does not detect coconuts in the image.
- No trained model, real orchard accuracy, throughput or safety certification is claimed.
- Evaluate on held-out orchard data and report precision/recall, localization error, end-to-end latency, memory, abstention, failure cases and simulation-vs-field results separately.

## Tests

```bash
python -m unittest discover -s apps/pui89_app -p 'test_*.py' -v
```

## Optional local coconut detector

The demo can run a compatible, user-supplied Ultralytics `.pt` detector locally on CPU. It does **not** automatically download weights, contact a hosted inference API, or send robot commands.

Install the optional dependencies:

```bash
python -m pip install -r apps/pui89_app/requirements-detector.txt
```

Configure the path to an existing, trusted model file before starting the app.

**Windows Command Prompt**
```bat
set "PUI89_COCONUT_MODEL_PATH=C:\path\to\your\trusted-coconut-model.pt"
streamlit run apps/pui89_app/web_demo.py
```

**PowerShell**
```powershell
$env:PUI89_COCONUT_MODEL_PATH = "C:\path\to\your\trusted-coconut-model.pt"
streamlit run apps/pui89_app/web_demo.py
```

The adapter checks that the model file exists locally and that its labels include a class named `coconut` or `coconuts`. It will not silently substitute a generic pretrained model. PyTorch `.pt` weights may use pickle-based serialization: only load files from sources you trust. The model licence must permit your intended use.

If you do not have a trained, licensed coconut model, leave this feature unconfigured. The app's manual-evidence demo remains available. A model running successfully is not proof of accuracy; evaluate predictions on a frozen, labelled test set using [the detection evaluation protocol](../../docs/DETECTION_EVALUATION_PROTOCOL.md).

## End-to-end robot task simulation in the app

The Streamlit UI also includes an optional **End-to-end robot task simulation** panel. It accepts explicitly supplied target evidence (position, uncertainty, track age, timestamp age, clearance, reachability and confidence), applies conservative gates, requires explicit approval before emitting a simulated approach/tool/retract sequence, and lets you download a JSON report.

These are user-supplied inputs for exercising the software workflow. They are **not** inferred from the uploaded photo. The task sequence is not physics simulation, collision proof, or physical robot control. See [the workflow guide](../../docs/END_TO_END_ROBOT_WORKFLOW.md), [RGB-D camera-frame localization utility](rgbd_localization.py), and [IoU tracking baseline](iou_tracker.py).

Run the workflow without opening the UI:

```bash
python -m apps.pui89_app.run_robot_workflow
python -m pytest -q apps/pui89_app/test_robot_workflow.py apps/pui89_app/test_spatial_tracking.py
```


## End-to-end vision-to-simulation smoke test

To test the complete software decision path without a trained model, cloud service or physical robot, run:

```bash
python -m apps.pui89_app.vision_to_workflow \
  --proposal examples/coconut_robot_proposal.synthetic.example.json \
  --evidence examples/coconut_robot_evidence.synthetic.example.json \
  --human-approved \
  --output coconut_simulated_workflow_report.json
```

This uses synthetic example data and an identity transform only for software smoke testing. It is not real camera calibration, a detector result or a field measurement. The report simulates approach/tool/retract steps but always states that no actuator command was sent.

For real inference, use the local-only detector pipeline and provide a validated camera-to-robot-base transform plus independent uncertainty, tracking, obstacle-clearance and reachability evidence. Missing or invalid evidence should cause safe hold, not guessed coordinates.
