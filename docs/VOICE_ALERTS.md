# Coconut Harvest AI — Local Voice Alerts

## Purpose

Announce robot state and operator warnings. The voice module must never control motion or authorize cutting.

This is an **optional local text-to-speech (TTS) layer**. It does not add or validate the project's vision model, sensor integration, or real-world performance. No hosted inference API is required by the setup below, and no paid service should be enabled.

## Recommended models

- **English:** [Kokoro-82M on Hugging Face](https://huggingface.co/hexgrad/Kokoro-82M) — model card lists the Apache-2.0 license.
- **Thai / multilingual experiment:** [SakThai TTS on Hugging Face](https://huggingface.co/Nanthasit/sakthai-tts-model) — model card lists MIT for this packaging and describes local GGUF CPU inference. Thai-script output is described as experimental; test pronunciation and numbers before operational use.
- Use the model files locally. Do not use Hugging Face hosted Inference Providers or other hosted APIs if the requirement is zero usage charges.

Check the current model card and any included voice/data licenses before redistribution or commercial deployment.

## Local English smoke test (Kokoro)

Install dependencies yourself in a virtual environment on a computer you control. The first run may download model files and therefore needs internet access and disk space. Runtime is local after the required files are available.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
python -m pip install "kokoro>=0.9.2" soundfile
```

Kokoro's official model card also lists `espeak-ng` as a dependency on Linux-based setups. Follow the model's current installation instructions for your operating system.

Create `tts_smoke_test.py`:

```python
from kokoro import KPipeline
import soundfile as sf

# 'a' selects the American English pipeline.
pipeline = KPipeline(lang_code="a")
text = "Voice system test. This is an advisory message only."

for index, (_graphemes, _phonemes, audio) in enumerate(
    pipeline(text, voice="af_heart")
):
    sf.write(f"voice_test_{index}.wav", audio, 24000)
    print(f"Saved voice_test_{index}.wav")
```

Run `python tts_smoke_test.py`, then play the WAV file locally. This is a manual test only; it does not connect TTS to the project's live detection pipeline.

## Example messages for this project

- “Person detected. Robot movement stopped.”
- “Coconut target uncertain. Request operator review.”
- “Harvest action is not authorized. Waiting for human confirmation.”

## Safety requirements

- A separate, validated safety controller—not text-to-speech—must stop the robot when a person enters a protected zone.
- Only speak status messages produced by the application; never convert an unverified detection into a claim that harvesting is safe.
- Keep speech output advisory. It must not trigger motors, grippers, or cutting tools.

## Cost and privacy checklist

- [ ] Use local inference only; do not configure a hosted inference endpoint or API key.
- [ ] Do not add billing-enabled cloud services to the workflow.
- [ ] Do not commit model weights, generated audio, private case data, credentials, or API tokens to Git.
- [ ] Test messages with recorded/simulated inputs before any field use.
- [ ] Provide a visual/text fallback if audio fails or the environment is too noisy.
- [ ] Verify language, pronunciation, latency, accessibility, and model license before deployment.

**Status:** Integration guide and smoke-test example only. The model is not automatically installed, the voice output is not yet connected to live project events, and no field-safety validation is claimed.
