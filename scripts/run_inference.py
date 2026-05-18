#!/usr/bin/env python
"""Run ASR inference on a Voices-in-the-Wild-Bench JSONL file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from voices_in_the_wild_bench.datasets import read_jsonl, write_jsonl
from voices_in_the_wild_bench.models import MODEL_REGISTRY


def resolve_audio_path(audio_path: str, audio_root: str | None) -> str:
    path = Path(audio_path)
    if path.exists():
        return str(path)
    if audio_root is not None:
        candidate = Path(audio_root) / str(audio_path).lstrip("/\\")
        if candidate.exists():
            return str(candidate)
    return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, choices=sorted(MODEL_REGISTRY))
    parser.add_argument("--model-path", default=None)
    parser.add_argument("--data-file", required=True)
    parser.add_argument("--audio-root", default=None)
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    model = MODEL_REGISTRY[args.model](model_path=args.model_path)
    records = read_jsonl(args.data_file)
    if args.limit is not None:
        records = records[: args.limit]

    outputs = []
    for record in tqdm(records, desc=f"Running {args.model}"):
        item = dict(record)
        audio_path = resolve_audio_path(item["audio_path"], args.audio_root)
        item["prediction"] = model.transcribe(audio_path)
        outputs.append(item)

    write_jsonl(args.output_file, outputs)


if __name__ == "__main__":
    main()
