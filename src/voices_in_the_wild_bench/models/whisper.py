"""Whisper wrapper."""

from __future__ import annotations

from .base import ASRModel


class WhisperLargeV3(ASRModel):
    name = "whisper-large-v3"

    def __init__(
        self,
        model_path: str | None = None,
        language: str | None = None,
        device: str | None = None,
        **kwargs,
    ):
        super().__init__(model_path=model_path)
        import torch
        from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

        resolved_model = model_path or "openai/whisper-large-v3"
        cuda_available = torch.cuda.is_available()
        dtype = torch.float16 if cuda_available else torch.float32
        pipeline_device = 0 if cuda_available and device is None else (device or -1)

        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            resolved_model,
            torch_dtype=dtype,
            low_cpu_mem_usage=True,
            use_safetensors=True,
        )
        processor = AutoProcessor.from_pretrained(resolved_model)
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=dtype,
            device=pipeline_device,
        )
        self.language = language

    def transcribe(self, audio_path: str) -> str:
        generate_kwargs = {"task": "transcribe", "max_new_tokens": 128}
        if self.language:
            generate_kwargs["language"] = self.language
        result = self.pipe(audio_path, generate_kwargs=generate_kwargs)
        return result.get("text", "").strip()
