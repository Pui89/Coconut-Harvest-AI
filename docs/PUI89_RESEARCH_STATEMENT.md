# PUI89 Research Statement

## Research direction
**Reliable Multimodal Embodied AI for Safety-Critical Autonomous Robots**

The three PUI89 robotics projects are designed as controlled experimental platforms for one research program rather than as unrelated applications.

## Central question
How can multimodal foundation models, 3D/4D world models, uncertainty estimation and safety-constrained planning enable reliable embodied intelligence when robots operate in dynamic, partially observed and safety-critical environments?

## Core hypotheses
1. A shared world-model interface can transfer useful representations across substantially different physical environments.
2. Explicit uncertainty/OOD estimation improves decision quality compared with confidence-only perception.
3. Foundation models are most useful as high-level reasoning/planning components when deterministic safety supervisors remain authoritative.
4. Cross-environment evaluation reveals failure modes that single-domain benchmarks hide.

## Experimental domains
- agriculture: coconut harvesting and manipulation;
- disaster response: flood mapping, hazard perception and autonomous reconnaissance;
- security/inspection: multimodal evidence fusion, anomaly screening and human review.

## Contributions to target
- multimodal 3D/4D world model;
- uncertainty-aware embodied reasoning;
- safe abstention and UNKNOWN behavior;
- foundation-model task planning under deterministic constraints;
- cross-environment transfer benchmark;
- reproducible simulation-to-real evaluation.

## Evidence
The project will distinguish concept, simulation, lab prototype, controlled field test and validated deployment. Every reported result should include dataset/version, hardware, software commit, metrics, failure cases and limitations.

## Engineering stack
ROS 2/Nav2 can provide modular navigation, planning, recovery and state-estimation interfaces; Nav2's current documentation describes its planner/controller/behavior architecture and ROS 2 integration. citeturn0search5turn0search7

Safety engineering should be treated as a separate verification discipline. ISO 3691-4:2023 covers safety requirements and verification for driverless industrial trucks and systems, including autonomous mobile robots in its scope; the standard is under revision, so the applicable requirements for a particular deployment must be assessed rather than assumed. citeturn0search2turn0search4

AI risk management should cover design, development, deployment and test/evaluation. NIST AI RMF provides a voluntary framework for trustworthy AI risk management, and NIST released a critical-infrastructure profile concept note in April 2026. citeturn0search0turn0search6

## PhD, competition and company value
The same evidence package supports three goals:
- **PhD:** publishable research questions and reproducible experiments;
- **competitions:** measurable autonomous missions and robust failure recovery;
- **company:** field-tested products, customer KPIs, reusable software and fleet data.
