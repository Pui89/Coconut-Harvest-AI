# Coconut Harvest AI — Product Readiness Gates

**Purpose:** move from prototype foundations toward a credible, testable agricultural-AI product without overstating capability.

## Current boundary
The repository does not yet demonstrate a validated physical harvesting robot. Candidate image records are not approved training data until source permission, annotation quality and provenance have been reviewed. CI success is not a detection-accuracy result.

## Work sequence
1. **Data rights and quality:** maintain source URL, creator, license, retrieval date, checksum, annotation version and reviewer for every image. Reject unknown permissions and malformed geometry.
2. **Dataset release gate:** approve only reviewed records; keep near-duplicates, orchard/tree identity, video frames and sessions grouped when splitting train/validation/test to reduce leakage.
3. **Reproducible baseline:** freeze dataset manifest, model/version, config, random seed, environment and commit SHA. Report precision, recall, F1, per-class metrics, confusion matrix, latency and failures; never invent scores.
4. **Decision support:** keep detection, maturity estimation, localization and harvest recommendation as separate outputs with confidence and an abstain/needs-review path.
5. **Robotics boundary:** no actuator command or physical cut until calibrated sensors, kinematics, collision checks, reachable workspace, emergency stop and hardware interlocks are independently tested.
6. **Product evidence:** publish a short demo, installation steps, known limitations, benchmark protocol and issue-reporting route. Test with growers before choosing commercial claims.

## Release gates
- **Gate A — data:** all evaluation images have verified usage rights and reviewed annotations.
- **Gate B — model:** a reproducible held-out benchmark exists, including failure cases and latency on stated hardware.
- **Gate C — workflow:** deterministic tests cover invalid inputs, low confidence, stale sensors and no-detection conditions.
- **Gate D — field pilot:** supervised field trials and safety review before claims about yield, reliability or real harvesting.

## Free-first policy
Use local tools and small, explicitly licensed samples first. Do not download large weights or datasets automatically; document size, access terms, storage and license before a human starts a download.

## Commercial boundary
Potential first product: human-reviewed coconut detection and harvest-planning assistance. Automated cutting, height reach, maturity accuracy and commercial return remain unverified until measured.