# Coconut Harvest AI — anomaly evidence integration profile

This folder defines a **documentation-only** integration boundary for the PUI89 shared anomaly evidence contract.

- Profile: [INTEGRATION_PROFILE.json](INTEGRATION_PROFILE.json)
- Shared contract name: `anomaly_evidence@0.1.0`
- Current state: profile documented; runtime adapter and model weights are not configured.
- No paid service, package installation, model download, dataset import or hardware action is enabled.

The profile identifies candidate anomaly scopes and safety boundaries. An anomaly score is never sufficient authority for a physical action or consequential decision. All outputs remain subject to provenance, uncertainty, sensor-health and human-review gates.

**Do not describe this project as using PaDiM, PatchCore or EfficientAD until an adapter is implemented, licensed assets are reviewed, real tests pass and evidence is recorded.**
