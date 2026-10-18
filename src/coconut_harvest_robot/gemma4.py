"""Optional local Gemma 4 31B IT multimodal inference adapter.

The model is large (~62.6 GB in the upstream repository). It uses cached local
weights by default; network downloads require explicit opt-in.

This adapter is for perception/reasoning only. Its output must still pass the
deterministic planner and safety gate before any robot action.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional


MODEL_ID = "google/gemma-4-31B-it"


class Gemma4Reasoner:
    """Run Gemma 4 31B IT with Hugging Face Transformers.

    Install the optional runtime dependencies from requirements.txt, then
    construct this class on a machine with sufficient GPU/CPU memory.
    """

    def __init__(
        self,
        model_id: str = MODEL_ID,
        max_new_tokens: int = 512,
        device_map: str = "auto",
    ) -> None:
        from transformers import AutoModelForMultimodalLM, AutoProcessor

        self.model_id = model_id
        self.max_new_tokens = max_new_tokens
        # Offline/cache-only by default. Opt in only after reviewing download size,
        # network usage, hardware requirements, and model license.
        allow_download = os.getenv("PUI89_ALLOW_MODEL_DOWNLOAD", "").strip().lower() in {
            "1", "true", "yes"
        }
        load_options = {"local_files_only": not allow_download}
        self.processor = AutoProcessor.from_pretrained(model_id, **load_options)
        self.model = AutoModelForMultimodalLM.from_pretrained(
            model_id,
            device_map=device_map,
            **load_options,
        )

    def reason(self, prompt: str, image: Optional[Any] = None) -> str:
        content = [{"type": "text", "text": prompt}]
        if image is not None:
            content.insert(0, {"type": "image", "image": image})

        messages = [{"role": "user", "content": content}]
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
        )
        generated = outputs[0][inputs["input_ids"].shape[-1] :]
        return self.processor.decode(generated, skip_special_tokens=True).strip()

    def structured_decision(
        self,
        observation: Dict[str, Any],
        image: Optional[Any] = None,
    ) -> Dict[str, Any]:
        prompt = (
            "You are the high-level reasoning module of a coconut harvesting robot. "
            "Analyze the orchard observation and return ONLY valid JSON with keys: "
            "goal, rationale, confidence, next_steps, target_id, requires_human_review. "
            "Never issue motor commands. Treat uncertain or occluded targets as needing "
            "inspection and require target verification before cutting.\n\n"
            f"Observation:\n{json.dumps(observation, default=str)}"
        )
        raw = self.reason(prompt, image=image)
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {
                "goal": "inspect",
                "rationale": raw,
                "confidence": 0.0,
                "next_steps": ["reobserve_target"],
                "target_id": None,
                "requires_human_review": True,
            }

        return parsed
