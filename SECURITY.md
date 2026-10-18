# Security Policy

## Scope

This repository covers an autonomous agricultural robot that combines perception, AI reasoning, navigation, manipulation, cloud/fleet services, and safety-critical interfaces. Security failures must never be allowed to bypass the robot's deterministic safety controls.

## Security principles

- **AI proposes; deterministic control validates.** Foundation models and vision models never directly issue unrestricted actuator commands.
- **Fail closed.** Authentication, authorization, integrity, sensor-health, localization, or safety failures must block autonomous actuation when required.
- **Least privilege.** Robot services, operators, CI jobs, and cloud services receive only the permissions they need.
- **Defense in depth.** Security controls exist at device, network, application, model, data, CI/CD, and fleet-management layers.
- **Traceability.** Software, firmware, AI models, configuration, and deployment events must be versioned and auditable.
- **No secrets in Git.** Credentials, private keys, tokens, certificates, production telemetry, and sensitive farm data must not be committed.

## Threats considered

- Unauthorized operator or remote access
- Compromised robot credentials or service accounts
- Malicious or tampered firmware, container, model, or configuration
- Supply-chain compromise of dependencies or model weights
- Unsafe commands injected through APIs, dashboards, ROS 2 topics, or AI-generated plans
- Network interception, replay, spoofing, or denial of service
- Sensor spoofing or degraded localization
- Theft or leakage of farm, customer, telemetry, imagery, or model data
- Compromise of OTA update infrastructure
- Compromise of one robot spreading to the fleet

## Required production controls

Production deployment should implement:

1. Unique device identity and certificate-based authentication.
2. Mutual TLS for robot-to-service communications.
3. Role-based access control for operators, maintainers, and administrators.
4. Secure boot and hardware-backed key storage where supported.
5. Signed firmware, signed application artifacts, signed AI models, and verified update manifests.
6. Anti-rollback protection for firmware and model releases.
7. Encrypted data in transit and at rest.
8. Network segmentation between safety/control, perception, management, and cloud interfaces.
9. Strict allowlists for actuator-control APIs and ROS 2 bridges.
10. Audit logs for login, authorization, configuration changes, model changes, OTA updates, safety overrides, and remote-control events.
11. Vulnerability scanning, dependency review, SBOM generation, and provenance for releases.
12. Tested backup, recovery, credential rotation, incident response, and fleet-wide revocation procedures.

## AI/model security

Models are treated as untrusted software/data until verified. Each production model should have:

- immutable version identifier
- source/provenance
- license information
- SHA-256 digest
- training/evaluation dataset provenance
- validation results
- approved deployment target
- signing metadata
- rollback version

Prompt injection, malicious scene content, corrupted sensor evidence, or adversarial model output must not bypass the deterministic safety supervisor.

## Responsible disclosure

Please do not publicly disclose an unpatched vulnerability involving robot control, authentication, remote access, secrets, OTA updates, or fleet infrastructure. Report security issues privately to the repository owner through an appropriate GitHub security channel when available.

## Security status

This project is a development/commercialization-stage robotics platform. The presence of these controls does **not** mean the physical robot is certified or production-safe. Hardware security, functional safety, penetration testing, field validation, and applicable regulatory review remain deployment requirements.
