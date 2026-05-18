from voices_in_the_wild_bench.datasets import public_category, split_type
from voices_in_the_wild_bench.metrics import cer, wer
from voices_in_the_wild_bench.reporting import evaluate_records


def test_public_category_maps_legacy_names_and_mixed_conditions():
    assert public_category({"combination": "barrier", "source_scenes": ["barrier"]}) == "obstructed"
    assert public_category({"combination": "crosstalk", "source_scenes": ["crosstalk"]}) == "recording"
    assert public_category({"combination": "noise_stutter", "source_scenes": ["noise", "stutter"]}) == "mixed"


def test_split_type_uses_subset_prefix():
    assert split_type({"subset": "real-en-noise"}) == "real"
    assert split_type({"subset": "sim-zh-mixed"}) == "sim"


def test_english_wer_and_chinese_cer():
    assert wer("hello world", "hello brave world") == (1, 2)
    assert cer("你好世界", "你好世") == (1, 4)


def test_evaluate_records_aggregates_by_category_and_split():
    records = [
        {
            "subset": "real-en-noise",
            "combination": "noise",
            "source_scenes": ["noise"],
            "answer": "hello world",
            "prediction": "hello brave world",
        },
        {
            "subset": "sim-zh-noise",
            "combination": "noise",
            "source_scenes": ["noise"],
            "answer": "你好世界",
            "prediction": "你好世",
        },
        {
            "subset": "sim-en-mixed",
            "combination": "noise_stutter",
            "source_scenes": ["noise", "stutter"],
            "answer": "clean speech",
            "prediction": "clean speech",
        },
    ]

    result = evaluate_records(records)

    assert result["overall"]["errors"] == 2
    assert result["overall"]["reference_length"] == 8
    assert result["overall"]["error_rate"] == 25.0
    assert result["breakdown"]["noise"]["real"]["error_rate"] == 50.0
    assert result["breakdown"]["noise"]["sim"]["error_rate"] == 25.0
    assert result["breakdown"]["mixed"]["sim"]["error_rate"] == 0.0
