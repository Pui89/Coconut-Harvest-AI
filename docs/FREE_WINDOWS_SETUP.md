# Free Windows Laptop Setup

This path is intentionally lightweight. It uses the rule-based agent and Python standard library only.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- No GPU required
- No API key, paid service, subscription, model download, or extra Python package required

## Run with one double-click

1. Download the repository from GitHub using **Code → Download ZIP**, then extract the ZIP.
2. Open the extracted `Coconut-Harvest-AI-main` folder.
3. Double-click `run_free_agent.bat`.
4. Read the readiness check and the agent's JSON output.

If Windows blocks the batch file, open Command Prompt in the extracted repository folder and run:

```bat
python scripts\check_local_agent_environment.py
python agents\harvest_planning_agent.py
```

## What the example proves—and what it does not

It demonstrates transparent rule-based candidate screening and proposal generation from synthetic example data. It does not use a camera, run a trained coconut detector, estimate real 3D coordinates, or control a robot.

## Keep costs at zero

Do not install a large language model yet. First confirm that the rule-based version runs. The optional Hugging Face/LLM stage can use substantial RAM, disk space, and possibly GPU memory; it is not needed for the initial agent and should only be considered after checking your actual laptop specifications and each model's licence.

No script in this setup intentionally contacts a paid inference service.
