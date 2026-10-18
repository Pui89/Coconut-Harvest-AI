# Coconut Harvest Robot — cinematic 4D concept

**Status:** concept storyboard and video prompt; not a validated harvesting machine.

## 30-second sequence
1. **0–5 s — Orchard dawn:** camera tracks between coconut palms with warm humid haze and dew on leaves.
2. **5–10 s — Robot reveal:** low dolly around a compact yellow-and-forest-green tracked platform; show stereo/RGB-D cameras, guarded end-effector and harvest basket.
3. **10–17 s — Perception:** camera moves over the shoulder as a visualization highlights a coconut bunch and estimates its position; show target confidence as an illustrative overlay, not a measured result.
4. **17–24 s — Safe approach:** robot stops at a marked exclusion zone; a telescoping arm aligns slowly with a mock target. No person stands under the target.
5. **24–30 s — Design hero:** robot retreats with the secured mock bunch in a padded collection basket; title: “PUI89 Coconut Harvest — precision agriculture concept”.

## Video-generation prompt
Generate a photorealistic cinematic 3D concept film, 16:9, 4K look, 24 fps, 30 seconds. A compact yellow-and-dark-green tracked orchard robot moves slowly through a realistic Thai coconut plantation. It has a stable low chassis, RGB-D/stereo vision mast, compact guarded telescoping arm, controlled cutting/gripping end-effector and padded collection basket. Warm sunrise, humid air, detailed soil and palm textures, physically plausible arm motion, consistent robot proportions across shots, slow dolly and orbit camera work, realistic metal and rubber materials. Use clean minimal AR overlays to illustrate perception and target localization. Never depict a person beneath a coconut bunch, uncontrolled falling coconuts, or a blade near a human. End card: “PUI89 Coconut Harvest — concept visualization”. No claims of tested picking performance.

## Suggested open-source workflow
- Blender for modeling and animation.
- FreeCAD for arm links, guards, mounts and mechanical layout.
- ROS 2 + Gazebo for later motion and collision simulation.
- OpenCV for a future vision prototype; evaluate on a documented dataset before claiming accuracy.
- Kdenlive for editing, titles and sound.

## Safety and realism checklist
- [ ] Animate a guarded tool and explicit keep-out zone.
- [ ] Include a fail-safe stop and conservative approach speed in the concept.
- [ ] Test reach, stability and collision envelopes in simulation before hardware.
- [ ] Label target boxes and confidence values as illustrative.
- [ ] Do not present the animation as a real-world harvesting demonstration.
