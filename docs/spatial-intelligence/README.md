# Coconut Harvest AI: Spatial Intelligence integration profile

See `INTEGRATION_PROFILE.json` for the machine-readable project contract.

## Intended use
Advisory palm, trunk, crown and target-relative geometry for later manipulation research.

## Planned tasks
- Palm trunk/crown and cluster-relative geometry
- Distance and coordinate-frame checks for synthetic arm reach fixtures
- Geometry evidence kept separate from maturity classification

## Safety boundaries
- LiDAR geometry does not classify coconut maturity.
- No grasp, cut, worker-clearance or arm trajectory safety is established.
- No harvesting robot hardware or field performance is claimed.

The common software interfaces are under development in [Shared AI Core PR #26](https://github.com/Pui89/PUI89-Shared-AI-Core/pull/26), which is still draft and unmerged. This file documents the intended integration contract only; no runtime import or sensor integration is yet claimed.

Before runtime integration, require lawful data provenance, calibration, synchronized timestamps, sensor-health checks, uncertainty handling, synthetic fault tests and human review. No physical actuation is enabled.

**Status:** profile documentation added; runtime adapter, real sensor integration, accuracy and field validation pending. No paid service or hardware purchase required.
