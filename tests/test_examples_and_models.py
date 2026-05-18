from pathlib import Path

from voices_in_the_wild_bench.datasets import public_category, read_jsonl
from voices_in_the_wild_bench.models import MODEL_REGISTRY


def test_examples_cover_all_public_categories_and_audio_files_exist():
    root = Path(__file__).resolve().parents[1]
    records = read_jsonl(root / "data" / "examples.jsonl")

    categories = {public_category(record) for record in records}

    assert categories == {
        "noise",
        "far_field",
        "obstructed",
        "distortion",
        "recording",
        "echo",
        "dropout",
        "mixed",
    }

    for record in records:
        assert (root / "data" / record["audio_path"]).exists()


def test_public_model_registry_includes_reproducible_wrappers():
    assert {
        "whisper-large-v3",
        "mega-asr",
        "canary-1b-v2",
        "kimi-audio",
        "parakeet-tdt-0.6b-v3",
        "qwen3-asr-1.7b",
        "step-audio-2-mini",
    }.issubset(MODEL_REGISTRY)
