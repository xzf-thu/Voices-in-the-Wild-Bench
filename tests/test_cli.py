import json
import subprocess
import sys


def test_evaluate_predictions_cli_writes_summary(tmp_path):
    pred_file = tmp_path / "predictions.jsonl"
    out_file = tmp_path / "results.json"
    pred_file.write_text(
        json.dumps(
            {
                "subset": "real-en-noise",
                "combination": "noise",
                "source_scenes": ["noise"],
                "answer": "hello world",
                "prediction": "hello world",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    subprocess.run(
        [
            sys.executable,
            "scripts/evaluate_predictions.py",
            "--prediction-file",
            str(pred_file),
            "--output-file",
            str(out_file),
        ],
        check=True,
    )

    result = json.loads(out_file.read_text(encoding="utf-8"))
    assert result["overall"]["error_rate"] == 0.0
    assert result["breakdown"]["noise"]["real"]["count"] == 1
