# Free-first Robotics Stack Selection for PUI89

Last reviewed: 25 October 2026

## Decision

Keep Phase 1 as the standard-library Python autonomy lab. Do not install a robotics stack or download a VLM as part of this PR. The software below is available without a licence purchase, but installation consumes disk/RAM/CPU/GPU and may require compatible operating systems and hardware. A physical robot, flight controller, sensors, batteries, tools, network access and field testing are not free.

## Recommended shared stack

| Component | Role | Licence / cost position | Decision |
|---|---|---|---|
| ROS 2 Jazzy | Middleware and message interfaces between robot components | Open-source; no software licence fee. Jazzy is an LTS release with published support to May 2029 and Ubuntu 24.04 is a Tier 1 platform. Check individual packages and dependencies. | Preferred integration target after Phase 1 passes. |
| Nav2 | Mobile robot navigation: localisation, path planning, obstacle-aware behaviours | Open-source, but the repository contains Apache-2.0, BSD-3-Clause and LGPL components; check each package manifest for commercial distribution. | Use for ground/mobile robots only when a simulator is ready. |
| Gazebo Harmonic | Physics and sensor simulation | Open source; gz-sim is Apache-2.0, though components/plugins can have their own licences. Harmonic is the documented pairing for ROS 2 Jazzy on Ubuntu 24.04. | Add first as the future simulation backend; not yet installed. |
| ArduPilot SITL | Simulated autopilot for supported Copter, Plane, Rover and Sub vehicle classes | Free software under GPLv3 or later. Distribution/modified-firmware obligations matter for a future commercial product. | Flood project only, after a simulator is working and the licence obligations are understood. |
| PX4 SITL | Alternative simulated autopilot, especially drone-focused development | BSD-3-Clause; more permissive code licence. Do not install alongside ArduPilot initially. | Alternative to evaluate if flight simulation becomes the priority; choose one autopilot first. |
| SmolVLM-256M-Instruct | Small vision-language model candidate for image-description/question-answering experiments | Publisher model card shows Apache-2.0. The main model.safetensors file is 513 MB, while the full repository listing is about 3.54 GB because it includes additional artifacts. | Optional experiment only, after resource preflight and manual licence review; no download is done here. |

Official references:
- ROS 2 Jazzy release and support: https://www.openrobotics.org/blog/2024/5/ros-jazzy-jalisco-released
- Nav2 licence details: https://github.com/ros-navigation/navigation2/blob/main/LICENSE
- Gazebo Harmonic ROS pairing/install guidance: https://gazebosim.org/docs/harmonic/
- Gazebo simulator licence: https://github.com/gazebosim/gz-sim
- ArduPilot GPLv3 licence: https://docs.ardupilot.org/dev/docs/license-gplv3.html
- PX4 BSD-3-Clause licence: https://docs.px4.io/main/en/
- SmolVLM model card/files/licence: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/tree/main
- SmolVLM 513 MB weight file: https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct/blob/main/model.safetensors

Licences and file sizes can change; re-check the specific versions/components before redistribution or product use. This is an engineering selection note, not legal advice.

## What belongs in each project

### 1. Coconut Harvest AI
- Now: Python autonomy lab, dataset/provenance gate, world-state observations, failure reports and repeatable test cases.
- Next software integration: ROS 2 Jazzy + Gazebo Harmonic, with Nav2 for a simulated ground platform. Add an arm/cutting simulation only when the kinematic model and safety cases are explicit.
- Not needed yet: drone autopilot, multiple autopilots, real motor/arm commands, or physical 30 m reach claims.
- Optional VLM: use SmolVLM for descriptions of a rights-cleared image; compare outputs against human-reviewed labels. It is not a coconut detector or maturity classifier by itself.

### 2. Extreme Flood Rescue AI
- Now: scenario matrix for people/animals as targets, changing simulated water depth, hazards, stale sensors, communication loss and safe recovery.
- Next software integration: ROS 2 + Gazebo for simulated robot/sensor interfaces. Nav2 for an appropriate ground/amphibious rover simulation. Only then choose one simulated autopilot: ArduPilot SITL if its GPLv3 obligations suit the intended product, or PX4 SITL for a drone-focused BSD-3-Clause route.
- Vehicle families to model: multirotor reconnaissance aircraft; fixed-wing/VTOL only if a long-range mission justifies the complexity; unmanned surface boat; ground/amphibious rover. A submersible is a separately engineered future concept, not a feature to assume from a generic autopilot.
- Evidence limit: a 0–15 m scenario parameter is not real-world vehicle depth, buoyancy, waterproofing, current handling or rescue capacity.

### 3. Multimodal Narcotics Screening AI
- Now: mock sensor topics, input validity checks, UNKNOWN on missing/conflicting/low-confidence signals, audit records and human-review routing.
- Next software integration: ROS 2 + Gazebo + Nav2 for a simulated indoor inspection robot. Use mock camera/other sensor feeds first; only add X-ray or chemical-sensor interfaces when lawfully obtained, technically valid data and evaluation protocols exist.
- Not needed: flight or boat autopilot for routine indoor screening.
- Evidence/safety limit: SmolVLM can describe visible image content but does not establish chemical composition or prove narcotics. No AI output authorises accusation, detention, search, seizure or enforcement.

## Staged local adoption gate

1. Complete the repository's Python unit tests and scenario command. Fix regressions before adding dependencies.
2. Record operating system, Python version, free disk, available RAM and GPU/VRAM. Check nvidia-smi where available. Do not rely on a model's parameter count alone to estimate runtime memory.
3. Select a compatible local simulation OS. ROS 2 Jazzy's official Tier 1 Ubuntu target is Ubuntu 24.04; Gazebo Harmonic officially recommends this pairing. Windows/GPU/WSL combinations should be checked carefully rather than assumed equivalent.
4. Install only the simulator stack needed for one small example. Keep it in an isolated environment or separate OS installation where practical; do not mix random ROS/Gazebo distributions.
5. Run one simple robot with one sensor and record exact versions, configuration, scenario hash, pass/failure metrics and observed latency.
6. Only after the simulator test is reproducible, run the optional VLM offline smoke test. Check the exact model revision and model card, and allowlist required files; do not clone the entire model repository.
7. Connect VLM output to symbolic simulated proposals only. Preserve safety guards independently of the VLM. No physical actuator interface is included in the current autonomy lab.

## Free-first cost boundary

Phase 1 requires only Python's standard library and the files committed in this repository. It does not install packages, download models, call paid APIs, use cloud GPUs, or connect to hardware. ROS 2, Nav2, Gazebo, ArduPilot, PX4 and SmolVLM have no required software purchase fee under their published open-source/model licences, but licence conditions still apply. Internet bandwidth, disk space, computer capacity and all physical hardware/testing costs remain separate.

## Definition of done for this upgrade

- Existing test suite passes.
- Simulation run generates JSON failure/metrics report and CSV step ledger.
- The same configuration produces the same run identifier and deterministic scenario outcome counts.
- Fault injection shows safe-hold/UNKNOWN/recovery behavior as designed.
- No model is installed or downloaded until the resource and licence gate is explicitly passed.
- Any future simulator/model benchmark publishes actual inputs, versions, limitations and measured results—not projections.
