"""Text error-rate metrics.

Chinese samples are evaluated with CER. English samples are evaluated with WER.
"""

from __future__ import annotations

import re
import unicodedata

def _strip_punctuation(text: str) -> str:
    chars = []
    for char in text:
        if unicodedata.category(char).startswith("P"):
            chars.append(" ")
        else:
            chars.append(char)
    return "".join(chars)


def normalize_english(text: str) -> list[str]:
    text = _strip_punctuation(str(text).lower())
    return text.split()


def normalize_chinese(text: str) -> list[str]:
    text = _strip_punctuation(str(text))
    text = re.sub(r"\s+", "", text)
    return [char for char in text if char]


def edit_distance(reference: list[str], prediction: list[str]) -> int:
    if not reference:
        return len(prediction)
    if not prediction:
        return len(reference)

    previous = list(range(len(prediction) + 1))
    for ref_idx, ref_token in enumerate(reference, 1):
        current = [ref_idx]
        for pred_idx, pred_token in enumerate(prediction, 1):
            insert_cost = current[pred_idx - 1] + 1
            delete_cost = previous[pred_idx] + 1
            replace_cost = previous[pred_idx - 1] + (ref_token != pred_token)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]


def wer(reference: str, prediction: str) -> tuple[int, int]:
    ref_tokens = normalize_english(reference)
    pred_tokens = normalize_english(prediction)
    return edit_distance(ref_tokens, pred_tokens), len(ref_tokens)


def cer(reference: str, prediction: str) -> tuple[int, int]:
    ref_chars = normalize_chinese(reference)
    pred_chars = normalize_chinese(prediction)
    return edit_distance(ref_chars, pred_chars), len(ref_chars)


def detect_language(record: dict) -> str:
    subset = str(record.get("subset", "")).lower()
    if "-zh-" in subset or subset.endswith("-zh") or subset.startswith("zh-"):
        return "zh"
    if "-en-" in subset or subset.endswith("-en") or subset.startswith("en-"):
        return "en"

    lang = str(record.get("lang", record.get("language", ""))).lower()
    if lang in {"zh", "cn", "chinese"}:
        return "zh"
    return "en"


def compute_error(record: dict) -> tuple[int, int, str]:
    language = detect_language(record)
    reference = str(record.get("answer", ""))
    prediction = str(record.get("prediction", ""))
    if language == "zh":
        errors, ref_len = cer(reference, prediction)
    else:
        errors, ref_len = wer(reference, prediction)
    return errors, ref_len, language
