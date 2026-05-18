"""NVIDIA Canary wrapper."""

from __future__ import annotations

from .base import ASRModel
from .utils import extract_text


class Canary1BV2(ASRModel):
    name = "canary-1b-v2"

    def __init__(
        self,
        model_path: str | None = None,
        source_lang: str = "en",
        target_lang: str = "en",
        batch_size: int = 8,
        **kwargs,
    ):
        super().__init__(model_path=model_path)
        import torch
        from nemo.collections.asr.models import EncDecMultiTaskModel

        self.model_path = model_path or "nvidia/canary-1b-v2"
        self.source_lang = kwargs.get("source_lang", source_lang)
        self.target_lang = kwargs.get("target_lang", target_lang)
        self.batch_size = int(kwargs.get("batch_size", batch_size))
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if self.model_path.endswith(".nemo"):
            self.model = EncDecMultiTaskModel.restore_from(self.model_path)
        else:
            self.model = EncDecMultiTaskModel.from_pretrained(self.model_path)
        self.model = self.model.to(self.device).eval()

    def transcribe(self, audio_path: str) -> str:
        output = self.model.transcribe(
            [audio_path],
            source_lang=self.source_lang,
            target_lang=self.target_lang,
            batch_size=self.batch_size,
        )
        return extract_text(output)
