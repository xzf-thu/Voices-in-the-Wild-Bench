"""Common model wrapper interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ASRModel(ABC):
    name: str

    def __init__(self, model_path: str | None = None, **kwargs):
        self.model_path = model_path

    @abstractmethod
    def transcribe(self, audio_path: str) -> str:
        raise NotImplementedError
