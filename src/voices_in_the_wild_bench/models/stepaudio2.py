"""Step-Audio 2 wrapper."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .base import ASRModel
from .utils import one_audio_path, require_model_path


class StepAudio2Mini(ASRModel):
    name = "step-audio-2-mini"

    def __init__(self, model_path: str | None = None, code_path: str | None = None, **kwargs):
        super().__init__(model_path=model_path)
        self.model_path = require_model_path("Step-Audio-2-mini", model_path, "STEP_AUDIO2_MODEL_PATH")
        package_dir = code_path or os.getenv("STEP_AUDIO2_CODE_PATH")
        if package_dir:
            sys.path.insert(0, str(Path(package_dir).resolve()))

        from stepaudio2 import StepAudio2

        self.model = StepAudio2(self.model_path)
        self.max_new_tokens = int(kwargs.get("max_new_tokens", 256))
        self.system_prompt = kwargs.get(
            "system_prompt",
            "You are an automatic speech recognition model. Transcribe the audio exactly.",
        )

    def transcribe(self, audio_path: str) -> str:
        audio = one_audio_path(audio_path)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "human", "content": [{"type": "audio", "audio": audio}]},
            {"role": "assistant", "content": None},
        ]
        _, text, _ = self.model(messages, max_new_tokens=self.max_new_tokens)
        return str(text).strip()
