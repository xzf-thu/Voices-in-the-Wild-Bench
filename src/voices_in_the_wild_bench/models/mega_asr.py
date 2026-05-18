"""Mega-ASR wrapper.

Mega-ASR is the public name for the merged_v2 model used in the paper.
Pass the released checkpoint path with ``--model-path``.
"""

from __future__ import annotations

from .base import ASRModel


class MegaASR(ASRModel):
    name = "mega-asr"

    def __init__(self, model_path: str | None = None, **kwargs):
        super().__init__(model_path=model_path)
        if model_path is None:
            raise ValueError("Mega-ASR requires --model-path pointing to the released merged_v2 checkpoint.")

        import torch
        from qwen_asr import Qwen3ASRModel

        self.model = Qwen3ASRModel.from_pretrained(
            model_path,
            dtype=torch.bfloat16,
            device_map=kwargs.get("device_map", "cuda:0"),
            max_inference_batch_size=int(kwargs.get("max_inference_batch_size", 32)),
            max_new_tokens=int(kwargs.get("max_new_tokens", 256)),
        )

    def transcribe(self, audio_path: str) -> str:
        results = self.model.transcribe(audio=audio_path, language=None)
        if isinstance(results, list):
            return " ".join(item.text for item in results).strip()
        return results.text.strip()
