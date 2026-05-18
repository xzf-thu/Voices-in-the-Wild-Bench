"""Model wrappers for reproducible inference."""

from .base import ASRModel
from .mega_asr import MegaASR
from .whisper import WhisperLargeV3

MODEL_REGISTRY = {
    WhisperLargeV3.name: WhisperLargeV3,
    MegaASR.name: MegaASR,
}

__all__ = ["ASRModel", "MODEL_REGISTRY", "MegaASR", "WhisperLargeV3"]
