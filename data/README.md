# Dataset

The official dataset will be hosted on Hugging Face:

```text
https://huggingface.co/datasets/xzf-thu/Voices-in-the-Wild-Bench
```

This repository keeps only lightweight documentation and release metadata. Audio files and full JSONL annotations should be distributed through the dataset hosting page rather than committed to GitHub.

## Expected Files

```text
voices_wild_bench_aug.jsonl
audio.tar.gz
```

## JSONL Fields

| Field | Description |
|---|---|
| `index` | Integer sample index |
| `audio_path` | Path to the waveform file |
| `question` | Instruction given to the evaluated system |
| `answer` | Reference transcription or answer |
| `subset` | Source, language, and category label |
| `combination` | Acoustic category label |
| `source_scenes` | Atomic scenes used for this sample |
| `aug_params_m` | Perturbation parameters when available |
| `global_severity` | Normalized severity score when available |
| `speed_factor` | Optional speed perturbation factor |
| `name` | Stable sample name |
| `prediction` | Optional model output field |

## Public Category Names

The public benchmark uses the following category names:

| Internal / legacy name | Public name |
|---|---|
| `barrier` | `obstructed` |
| `crosstalk` | `recording` |
| `stutter` | `dropout` |

Other category names are unchanged.
