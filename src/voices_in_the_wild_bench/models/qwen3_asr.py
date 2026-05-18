"""Qwen3-ASR wrapper."""

from __future__ import annotations

from .base import ASRModel
from .utils import extract_text


class Qwen3ASR(ASRModel):
    name = "qwen3-asr-1.7b"

    def __init__(self, model_path: str | None = None, **kwargs):
        super().__init__(model_path=model_path)
        import torch
        from qwen_asr import Qwen3ASRModel

        self.model_path = model_path or "Qwen/Qwen3-ASR-1.7B"
        self.model = Qwen3ASRModel.from_pretrained(
            self.model_path,
            dtype=kwargs.get("dtype", torch.bfloat16),
            device_map=kwargs.get("device_map", "cuda:0"),
            max_inference_batch_size=int(kwargs.get("max_inference_batch_size", 32)),
            max_new_tokens=int(kwargs.get("max_new_tokens", 256)),
        )

    def transcribe(self, audio_path: str) -> str:
        return extract_text(self.model.transcribe(audio=audio_path, language=None))
