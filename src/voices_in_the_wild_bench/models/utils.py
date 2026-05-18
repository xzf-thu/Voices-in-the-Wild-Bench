"""Small helpers shared by model wrappers."""

from __future__ import annotations

import os
from typing import Any


def require_model_path(model_name: str, model_path: str | None, env_var: str | None = None) -> str:
    if model_path:
        return model_path
    if env_var and os.getenv(env_var):
        return os.environ[env_var]
    raise ValueError(f"{model_name} requires --model-path or {env_var}.")


def one_audio_path(audio_path: str | list[str]) -> str:
    if isinstance(audio_path, list):
        if len(audio_path) != 1:
            raise ValueError("This wrapper expects one audio file per request.")
        return os.fspath(audio_path[0])
    return os.fspath(audio_path)


def extract_text(output: Any) -> str:
    if output is None:
        return ""
    if isinstance(output, list):
        parts = [extract_text(item) for item in output]
        return " ".join(part for part in parts if part).strip()
    if hasattr(output, "text"):
        return str(output.text).strip()
    if isinstance(output, dict):
        for key in ("text", "transcription", "prediction"):
            if key in output:
                return str(output[key]).strip()
    return str(output).strip()
