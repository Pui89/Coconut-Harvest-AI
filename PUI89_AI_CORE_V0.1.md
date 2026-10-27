# PUI89 AI Core v0.1

A small, local-first shared interface for the PUI89 AI projects. The same initial core is mirrored across the three repositories so project-specific integrations can begin consistently.

## Included

- Dependency-free world-state records and confidence validation.
- Simulation-only action proposals; no robot commands are executed.
- JSON failure-report writer.
- Standard-library automated tests.

## Run tests

From the repository root, using Python 3.10 or newer:

```bash
python -m unittest discover -s tests -v
```

No model weights, paid APIs, cloud services, or third-party packages are required for these checks.

## Safety and evidence boundary

This is an initial interface scaffold, not a validated perception model, robot controller, or end-to-end system. Confidence values are supplied by callers and are not calibrated by this package. All actions remain proposals for human review or simulation. Hardware execution is out of scope.

## Next validation steps

1. Run the tests on the target laptop and supported Python version.
2. Add project-specific adapters only after existing repository structure is reviewed.
3. Record measured test outcomes; do not claim tests passed until run in the target environment.
4. Check dependency licences and resource requirements before adding optional models or simulators.
