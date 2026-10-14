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
