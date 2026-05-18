#!/usr/bin/env python
"""Evaluate a prediction JSONL file with Chinese CER and English WER."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from voices_in_the_wild_bench.datasets import read_jsonl
from voices_in_the_wild_bench.reporting import evaluate_records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prediction-file", required=True, help="JSONL file with answer and prediction fields.")
    parser.add_argument("--output-file", default=None, help="Optional path for the JSON summary.")
    args = parser.parse_args()

    records = read_jsonl(args.prediction_file)
    result = evaluate_records(records)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.output_file:
        output = Path(args.output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
