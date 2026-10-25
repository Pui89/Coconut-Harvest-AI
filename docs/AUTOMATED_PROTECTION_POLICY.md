# Document automated protection policy for coconut harvesting

## Automated protection and fail-safe policy

This is the project's safety contract for software and future hardware integration. It is **not proof of a physically safe robot**.

### Required automated checks
- Reject missing, malformed, stale, or out-of-range sensor/model inputs; never silently substitute a safe-looking value.
- Keep detection confidence, maturity estimate, target geometry, and sensor freshness separate. Unknown or conflicting observations require a hold and review.
- Before any future arm or cutter command, require an independently verified target, a clear exclusion zone, valid localization/depth data, arm/workspace limits, stable-platform status, and a healthy safety monitor.
- Stop or inhibit motion on emergency-stop input, watchdog timeout, communication loss, stale sensor data, unexpected force/current, limit violation, or disagreement between perception and geometry.
- Require an explicit operator reset and a new safety check after a fault. Do not automatically resume a cutting sequence.
- Keep a timestamped audit record of the trigger, inputs, decision, and recovery; avoid storing unnecessary personal data.

### Automation boundaries
- Current software checks and CI may validate logic; they do not actuate or physically stop motors.
- Never cut based only on an image label or an unverified 3D estimate. Use human confirmation until end-to-end tests establish an appropriately bounded operating envelope.
- Dataset source permissions, annotation geometry, tree/source leakage checks, and held-out evaluation are release gates. Do not train on unapproved candidates or publish unmeasured accuracy.
- Physical safeguards still required: independent hardwired emergency stop, actuator power isolation, guarded cutting tool, mechanical travel limits, safe-state watchdog, and controlled orchard validation.

### Release gate
A change is not “proven safe” merely because unit tests pass. Record test cases and results, review failures, and keep physical validation status **not validated** until supported by documented evidence.
