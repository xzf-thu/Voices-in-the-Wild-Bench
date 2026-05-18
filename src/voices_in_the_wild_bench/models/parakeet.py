"""NVIDIA Parakeet wrapper."""

from __future__ import annotations

from .base import ASRModel
from .utils import extract_text


class ParakeetTDT06BV3(ASRModel):
    name = "parakeet-tdt-0.6b-v3"

    def __init__(
        self,
        model_path: str | None = None,
        batch_size: int = 8,
        timestamps: bool = False,
        long_form: bool = False,
        att_context_size: list[int] | tuple[int, int] | None = None,
        **kwargs,
    ):
        super().__init__(model_path=model_path)
        import torch
        import nemo.collections.asr as nemo_asr

        self.model_path = model_path or "nvidia/parakeet-tdt-0.6b-v3"
        self.batch_size = int(kwargs.get("batch_size", batch_size))
        self.timestamps = bool(kwargs.get("timestamps", timestamps))
        self.long_form = bool(kwargs.get("long_form", long_form))
        self.att_context_size = kwargs.get("att_context_size", att_context_size)
        if self.long_form and self.att_context_size is None:
            self.att_context_size = [256, 256]

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        if self.model_path.endswith(".nemo"):
            self.model = nemo_asr.models.ASRModel.restore_from(self.model_path)
        else:
            self.model = nemo_asr.models.ASRModel.from_pretrained(model_name=self.model_path)
        self.model = self.model.to(self.device).eval()

        if self.att_context_size is not None:
            self.model.change_attention_model(
                self_attention_model="rel_pos_local_attn",
                att_context_size=list(self.att_context_size),
            )

    def transcribe(self, audio_path: str) -> str:
        output = self.model.transcribe(
            [audio_path],
            batch_size=self.batch_size,
            timestamps=self.timestamps,
        )
        return extract_text(output)
