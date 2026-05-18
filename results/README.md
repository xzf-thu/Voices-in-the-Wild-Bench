# Results

Leaderboard submissions should include aggregate and category-wise scores. Raw prediction files can be shared through releases, cloud storage, or issue attachments if size permits.

## Recommended Prediction Format

Use JSONL with one record per benchmark sample. Preserve the original metadata and fill the `prediction` field:

```json
{"index": 0, "audio_path": "audio/example.wav", "answer": "reference transcription", "subset": "sim-en-noise", "prediction": "model transcription"}
```

## Submission Checklist

- Model name and version.
- Organization or author.
- Date of evaluation.
- Whether the model used audio input directly or an ASR-plus-LLM pipeline.
- Overall score.
- Category-wise scores for all eight acoustic categories.
- Link to prediction file or reproducible evaluation log.
