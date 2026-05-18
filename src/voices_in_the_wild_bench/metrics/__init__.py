"""CER/WER metrics for Voices-in-the-Wild-Bench."""

from .error_rate import cer, compute_error, detect_language, wer

__all__ = ["cer", "compute_error", "detect_language", "wer"]
