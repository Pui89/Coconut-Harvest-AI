# Local-First Vision-to-Robot Proposal — Status

## Current status

This proposal is retained as an architectural research record. The object-detection integration previously described here is retired and is not part of the active application. No detector framework, model checkpoint or weights are currently selected or approved.

## Active software boundary

- Images and depth files remain local to the operator's environment.
- Image annotations and maturity assessments are human supplied.
- Dataset rights, provenance, image quality and label review must be recorded before model evaluation.
- Spatial estimates require documented camera calibration and RGB/depth alignment.
- Every proposal remains advisory and requires human review.
- No software output authorises cutting, gripping, lifting, movement or any other physical actuation.

## Future detector gate

A future detector may be considered only after independent code/weight licensing, provenance, security, CPU/RAM feasibility and held-out coconut-dataset evaluation. Do not install detector packages or download model weights before that review.

A successful software test or synthetic example does not establish field accuracy, safe localisation or harvesting capability.
