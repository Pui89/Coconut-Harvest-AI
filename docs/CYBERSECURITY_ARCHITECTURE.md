# Cybersecurity Architecture

## Goal

Protect the coconut-harvesting robot across its complete lifecycle: development, manufacturing, deployment, operation, maintenance, OTA updates, fleet management, and decommissioning.

The security program is aligned conceptually with **NIST CSF 2.0** and **NIST Secure Software Development Framework (SSDF)** practices, while recognizing that agricultural robotics has additional physical-safety and operational constraints. NIST CSF 2.0 explicitly emphasizes governance and supply-chain risk, while SSDF organizes secure development around preparing the organization, protecting software, producing well-secured software, and responding to vulnerabilities.

## Security zones

```
                         CLOUD / FLEET
                    +----------------------+
                    | API + RBAC + Audit   |
                    | Model Registry       |
                    | OTA / Update Service  |
                    +----------+-----------+
                               |
                         mTLS / allowlist
                               |
                 +-------------v-------------+
                 | ROBOT MANAGEMENT ZONE     |
                 | telemetry / diagnostics   |
                 +-------------+-------------+
                               |
                    authenticated bridge
                               |
        +----------------------v----------------------+
        | ROBOT COMPUTE / AI ZONE                     |
        | perception | world model | planner | VLM   |
        +----------------------+----------------------+
                               |
                  policy + deterministic validation
                               |
        +----------------------v----------------------+
        | SAFETY / CONTROL ZONE                       |
        | watchdog | limits | E-stop | controller    |
        +----------------------+----------------------+
                               |
                     CAN / EtherCAT / drives
                               |
        +----------------------v----------------------+
        | ACTUATORS / SENSORS / MOBILE BASE           |
        +---------------------------------------------+
```

## Trust boundaries

### 1. AI boundary

Perception models, VLMs, generative models, and external prompts are untrusted inputs to the mission planner. Their output is a proposal only.

### 2. Network boundary

Cloud, operator consoles, maintenance laptops, and external APIs are untrusted until authenticated and authorized.

### 3. Actuator boundary

No network message or model output should directly bypass the deterministic safety supervisor.

### 4. Update boundary

Firmware, containers, dependencies, model weights, configuration, and calibration files must pass integrity and authorization checks before deployment.

## Identity and access

Production robots should have unique identities rather than shared credentials.

Recommended roles:

| Role | Access |
|---|---|
| Operator | Mission monitoring, approved commands, E-stop |
| Maintainer | Diagnostics, calibration, maintenance workflows |
| ML Engineer | Model staging/evaluation, no direct actuator authority |
| Fleet Admin | Robot enrollment, deployment, revocation |
| Security Admin | Certificates, policies, incident response |

Use short-lived credentials where practical, certificate rotation, MFA for human administrative access, and immediate revocation for lost or compromised devices.

## Network security

- Prefer mutually authenticated TLS for IP-based services.
- Segment robot control from cloud/management traffic.
- Do not expose ROS 2, actuator interfaces, debug ports, or management services directly to the public Internet.
- Use explicit service allowlists.
- Rate-limit remote APIs.
- Record security-relevant network events.
- Provide a safe local operating mode if cloud connectivity is lost.

## OTA and model integrity

A production update should follow:

```
artifact -> hash -> signature -> provenance -> policy check
         -> compatibility check -> staged rollout
         -> health validation -> commit
         -> rollback on failure
```

Never allow an unsigned or untrusted model/firmware package to become active.

Recommended deployment states:

**STAGED -> CANARY -> APPROVED -> FLEET -> ROLLBACK**

## Secrets

Never commit:

- API keys
- passwords
- private keys
- cloud credentials
- device certificates
- signing keys
- production database credentials
- customer tokens

Use a managed secret store or hardware-backed keystore for production.

## Logging and audit

Security and safety audit events should include:

- timestamp
- robot/device ID
- software/model versions
- authenticated principal
- event type
- authorization result
- relevant target/mission ID
- configuration or model hash
- safety-gate decision
- update result
- failure/incident identifier

Logs must be protected against unauthorized modification and retained according to the operational/security policy.

## Supply-chain security

Track provenance for:

- Python dependencies
- OS packages
- ROS 2 packages
- containers
- firmware
- AI model weights
- datasets
- calibration artifacts
- third-party hardware SDKs

Generate an SBOM for releases and review high-risk dependencies before deployment.

## Incident response

Recommended response states:

```
DETECT -> CONTAIN -> SAFE STOP -> REVOKE -> INVESTIGATE
       -> PATCH -> VALIDATE -> CANARY -> RECOVER -> REVIEW
```

A suspected compromise of a robot should support remote credential/certificate revocation and a safe physical operating state.

## Security verification

Before commercial field deployment:

- dependency and secret scans
- static analysis
- container/image scanning if containers are used
- API authorization tests
- authentication and certificate-rotation tests
- OTA signature/rollback tests
- ROS 2/network exposure review
- fuzzing of external interfaces where appropriate
- adversarial AI/model tests
- sensor spoofing/degradation tests
- incident-recovery drills
- independent penetration testing
- hardware-specific security assessment

These controls are an engineering baseline, not a certification claim.

## Reference frameworks

- NIST Cybersecurity Framework (CSF) 2.0
- NIST SP 800-218 Secure Software Development Framework
- NIST Cybersecurity Supply Chain Risk Management guidance
- IEC 62443 concepts for industrial automation/security lifecycle
- Applicable agricultural machinery safety and cybersecurity requirements for the final product
