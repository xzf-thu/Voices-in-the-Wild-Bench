"""Model wrappers for reproducible inference."""

from .base import ASRModel
from .canary import Canary1BV2
from .kimi_audio import KimiAudio
from .mega_asr import MegaASR
from .parakeet import ParakeetTDT06BV3
from .qwen3_asr import Qwen3ASR
from .stepaudio2 import StepAudio2Mini
from .whisper import WhisperLargeV3

MODEL_REGISTRY = {
    WhisperLargeV3.name: WhisperLargeV3,
    MegaASR.name: MegaASR,
    Canary1BV2.name: Canary1BV2,
    KimiAudio.name: KimiAudio,
    ParakeetTDT06BV3.name: ParakeetTDT06BV3,
    Qwen3ASR.name: Qwen3ASR,
    StepAudio2Mini.name: StepAudio2Mini,
}

__all__ = [
    "ASRModel",
    "MODEL_REGISTRY",
    "Canary1BV2",
    "KimiAudio",
    "MegaASR",
    "ParakeetTDT06BV3",
    "Qwen3ASR",
    "StepAudio2Mini",
    "WhisperLargeV3",
]
