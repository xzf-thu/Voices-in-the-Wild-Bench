"""Aggregate CER/WER results into benchmark breakdowns."""

from __future__ import annotations

from collections import defaultdict

from voices_in_the_wild_bench.datasets import PUBLIC_CATEGORIES, public_category, split_type
from voices_in_the_wild_bench.metrics import compute_error


def _empty_bucket() -> dict:
    return {"errors": 0, "reference_length": 0, "count": 0}


def _finalize(bucket: dict) -> dict:
    ref_len = bucket["reference_length"]
    error_rate = 0.0 if ref_len == 0 else round(bucket["errors"] / ref_len * 100, 2)
    return {
        "error_rate": error_rate,
        "errors": bucket["errors"],
        "reference_length": ref_len,
        "count": bucket["count"],
    }


def evaluate_records(records: list[dict]) -> dict:
    overall = _empty_bucket()
    by_category = {
        category: {"real": _empty_bucket(), "sim": _empty_bucket()}
        for category in PUBLIC_CATEGORIES
    }
    by_language = defaultdict(_empty_bucket)

    for record in records:
        errors, ref_len, language = compute_error(record)
        category = public_category(record)
        split = split_type(record)

        for bucket in [overall, by_language[language]]:
            bucket["errors"] += errors
            bucket["reference_length"] += ref_len
            bucket["count"] += 1

        if category not in by_category:
            by_category[category] = {"real": _empty_bucket(), "sim": _empty_bucket()}
        if split not in by_category[category]:
            by_category[category][split] = _empty_bucket()

        bucket = by_category[category][split]
        bucket["errors"] += errors
        bucket["reference_length"] += ref_len
        bucket["count"] += 1

    return {
        "overall": _finalize(overall),
        "by_language": {lang: _finalize(bucket) for lang, bucket in by_language.items()},
        "breakdown": {
            category: {split: _finalize(bucket) for split, bucket in splits.items()}
            for category, splits in by_category.items()
        },
    }
