# System Fault and Hardware Safety Playbook

**Status: design guidance only. This document does not certify a robot or replace a hazard analysis.** The physical machine, actuators, tools, battery, wiring, operating environment, and applicable standards must be assessed by qualified people before hardware use.

## Safety priority

1. Protect people first; do not prioritize completing a harvest.
2. On uncertain safety state, stop the task and prevent hazardous motion/cutting.
3. Keep independent safety functions active where the hardware design permits.
4. Alert the operator, record the fault without exposing secrets, and require a deliberate recovery check.
5. Never automatically restart cutting or motion after a serious fault.

## Fault response matrix

| Fault or situation | Required response to design and test |
|---|---|
| AI/model crash, timeout, invalid output, or low confidence | Cancel harvest action; inhibit cutter; retain independent safety monitoring. |
| Camera, depth sensor, encoder, IMU, or safety sensor missing/stale/conflicting | Treat affected perception as unavailable; stop autonomous movement when safe navigation cannot be established. |
| Localization, route, or target position uncertain | Do not approach, climb, or cut; hold safely and request operator review. |
| Wi-Fi, telemetry, or operator heartbeat lost | Enter the pre-tested loss-of-link state; inhibit cutting and hazardous motion. Do not assume that stopping abruptly is safe on every slope or load. |
| Low battery, voltage sag, overheating, or power fault | Stop harvesting; use a return route only if navigation, braking, and reserve are verified. Otherwise request recovery. |
| Main computer or control process hangs/reboots | Independent watchdog and hardware safety chain should remove hazardous actuator enable; test this without relying on the main computer. |
| Motor/arm jam, unexpected movement, collision, stuck vehicle, or tip-over | Inhibit cutter and hazardous motion; use the hardware-specific brake/hold response; alert operator and follow a recovery plan. |
| Electrical short, damaged cable, water ingress, smoke, unusual heat, or burning smell | Stop operation if safe, isolate power using the designed disconnect, keep people clear, and request qualified inspection. Do not touch exposed conductors or wet electrical equipment. |
| Emergency-stop activated or guard/interlock open | Keep hazardous outputs disabled until the cause is checked and an intentional, authorised reset is performed. E-stop reset must not itself restart motion. |
| Memory/storage full, corrupted config, invalid calibration, clock/logging failure | Refuse unsafe mission start if required evidence/configuration is unavailable; retain a safe stop path and show a clear fault. |
| Unexpected object/person, poor visibility, wind/rain, unstable ground, or unsafe tree/load condition | Suspend harvesting and movement that could endanger people; request reassessment. |
| Software update, configuration change, or unknown fault | Do not run an autonomous harvest until the change is checked and relevant regression/safety tests pass. |

## Hardware and electrical design checklist

- Use a physical, reachable emergency stop and a safety-rated/independent means to disable hazardous actuator energy where required by the risk assessment.
- Keep the safety path independent of AI, operating-system processes, wireless networking, and ordinary application code.
- Select fuses/over-current protection, wire gauge, connectors, insulation, grounding, battery protection, enclosure ingress protection, and thermal limits for the actual hardware by qualified design—not by guesswork.
- Prevent unexpected restart after power recovery, watchdog reset, communication recovery, or emergency-stop reset.
- Define safe braking/holding behaviour for the arm and mobile base; a sudden power cut can itself create a falling-load hazard.
- Guard cutting tools and pinch/crush zones; add suitable interlocks and a maintenance lockout/isolation procedure.
- Check electrical isolation, strain relief, connector retention, water/dust ingress, temperatures, battery condition, and cable damage before each test.
- Never bypass interlocks or test cutting tools near people. Begin with software simulation, then disconnected-actuator tests, then low-energy controlled tests in a secured area.

## Recovery and verification

For every fault, document: detection signal; maximum detection time; safe output state; whether braking or holding is required; operator alert; reset authority; recovery steps; test setup; expected result; actual result; and evidence link. Test single faults and plausible combinations (for example, low battery plus lost link). Mark untested cases **NOT TESTED**; do not claim the system handles every possible failure.

## Current project boundary

The repository contains software decision logic and documentation, not a certified hardware safety controller. This playbook does not prove that physical electrical, mechanical, environmental, or emergency-stop protections exist. Have a qualified robotics/electrical safety professional review the design before connecting or operating hazardous hardware.
