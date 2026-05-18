"""Kimi-Audio wrapper."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .base import ASRModel
from .utils import one_audio_path, require_model_path


class KimiAudio(ASRModel):
    name = "kimi-audio"

    def __init__(
        self,
        model_path: str | None = None,
        code_path: str | None = None,
        load_detokenizer: bool = False,
        prompt: str = "Please transcribe the following audio:",
        output_type: str = "text",
        **kwargs,
    ):
        super().__init__(model_path=model_path)
        self.model_path = require_model_path("Kimi-Audio", model_path, "KIMI_AUDIO_MODEL_PATH")
        self.prompt = kwargs.get("prompt", prompt)
        self.output_type = kwargs.get("output_type", output_type)
        self.load_detokenizer = bool(kwargs.get("load_detokenizer", load_detokenizer))

        package_dir = code_path or os.getenv("KIMI_AUDIO_CODE_PATH")
        if package_dir:
            sys.path.insert(0, str(Path(package_dir).resolve()))

        from kimia_infer.api.kimia import KimiAudio as KimiAudioModel

        self.model = KimiAudioModel(
            model_path=self.model_path,
            load_detokenizer=self.load_detokenizer,
        )
        self.sampling_params = {
            "audio_temperature": 0.8,
            "audio_top_k": 10,
            "text_temperature": 0.0,
            "text_top_k": 1,
            "audio_repetition_penalty": 1.0,
            "audio_repetition_window_size": 64,
            "text_repetition_penalty": 1.1,
            "text_repetition_window_size": 64,
            "max_new_tokens": 256,
        }
        self.sampling_params.update(kwargs.get("sampling_params", {}))

    def transcribe(self, audio_path: str) -> str:
        audio = one_audio_path(audio_path)
        messages = [
            {"role": "user", "message_type": "text", "content": self.prompt},
            {"role": "user", "message_type": "audio", "content": audio},
        ]
        _, text = self.model.generate(
            messages,
            **self.sampling_params,
            output_type=self.output_type,
        )
        return str(text).strip()
