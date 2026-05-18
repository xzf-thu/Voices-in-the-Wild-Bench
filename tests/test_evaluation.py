from voices_in_the_wild_bench.datasets import public_category, sanitize_public_record, split_type
from voices_in_the_wild_bench.metrics import cer, wer
from voices_in_the_wild_bench.reporting import evaluate_records


def test_public_category_maps_legacy_names_and_mixed_conditions():
    assert public_category({"combination": "barrier", "source_scenes": ["barrier"]}) == "obstructed"
    assert public_category({"combination": "crosstalk", "source_scenes": ["crosstalk"]}) == "recording"
    assert public_category({"combination": "strong_echo", "source_scenes": ["strong_echo"]}) == "echo"
    assert public_category({"combination": "noise_stutter", "source_scenes": ["noise", "stutter"]}) == "mixed"


def test_split_type_uses_subset_prefix():
    assert split_type({"subset": "real-en-noise"}) == "real"
    assert split_type({"subset": "sim-zh-mixed"}) == "sim"


def test_sanitize_public_record_removes_private_perturbation_fields_and_renames_metadata_only():
    record = {
        "index": 1,
        "audio_path": "audio/audio_aug_mixed/strong_echo/foo_stutter.wav",
        "question": "Please transcribe the audio content into text.",
        "answer": "the word stutter may appear in a transcript",
        "subset": "sim-en-strong_echo",
        "combination": "strong_echo",
        "source_scenes": ["strong_echo"],
        "aug_params_m": [{"effect": "add_echo"}],
        "global_severity": 0.5,
        "speed_factor": None,
        "name": "foo_strong_echo_stutter",
        "prediction": "",
    }

    public = sanitize_public_record(record)

    assert "combination" not in public
    assert "source_scenes" not in public
    assert "aug_params_m" not in public
    assert "global_severity" not in public
    assert "speed_factor" not in public
    assert public["audio_path"] == "audio/audio_aug_mixed/echo/foo_dropout.wav"
    assert public["subset"] == "sim-en-echo"
    assert public["name"] == "foo_echo_dropout"
    assert public["answer"] == "the word stutter may appear in a transcript"


def test_public_category_can_be_inferred_from_public_subset_and_path():
    assert public_category({"subset": "sim-en-echo", "audio_path": "audio/audio_aug_mixed/echo/a.wav"}) == "echo"
    assert public_category({"subset": "sim-en-mixed", "audio_path": "audio/audio_aug_mixed/noise_dropout/a.wav"}) == "mixed"


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
