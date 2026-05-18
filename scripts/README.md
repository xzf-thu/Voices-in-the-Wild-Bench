# Scripts

This directory contains the public reproduction entry points.

Run inference:

```shell
python scripts/run_inference.py \
  --model whisper-large-v3 \
  --data-file data/examples.jsonl \
  --audio-root /path/to/voices_wild_bench \
  --output-file outputs/predictions.jsonl
```

Evaluate predictions:

```shell
python scripts/evaluate_predictions.py \
  --prediction-file outputs/predictions.jsonl \
  --output-file outputs/results.json
```

Chinese samples are scored with CER; English samples are scored with WER.
