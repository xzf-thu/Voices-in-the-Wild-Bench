<h1 align="center">Voices-in-the-Wild-Bench</h1>

<p align="center">
  <strong>Benchmarking Robust Speech Understanding in Real-World Voice Interaction</strong>
</p>

<p align="center">
  <a href="https://prummn.github.io/Voices-in-the-Wild-Bench/">Leaderboard</a> |
  <a href="https://arxiv.org/abs/YOUR_PAPER_ID">Paper</a> |
  <a href="https://huggingface.co/datasets/prummn/Voices-in-the-Wild-Bench">Dataset</a> |
  <a href="https://github.com/prummn/Voices-in-the-Wild-Bench/issues">Submit Results</a>
</p>

> Voices-in-the-Wild-Bench is a bilingual benchmark for evaluating how robust speech and voice assistant systems are under realistic acoustic conditions, including noise, far-field speech, obstruction, recording artifacts, echo, dropout, and mixed perturbations.

## News

* **`2026.05.16`** Initial repository skeleton released. Dataset card, leaderboard page, and evaluation code will be updated as the public release is finalized.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Data Format](#data-format)
- [Evaluation](#evaluation)
- [Leaderboard](#leaderboard)
- [Submission](#submission)
- [Citation](#citation)

## Overview

Voices-in-the-Wild-Bench is designed to test speech recognition and voice-interaction systems in conditions that are closer to real-world usage than clean studio speech. The benchmark contains **5,000** audio examples, covering both synthetic and real-recorded speech, balanced across Chinese and English.

The benchmark focuses on transcription-oriented robust speech understanding. Each sample includes an audio path, an instruction, a reference answer or transcription, and metadata describing the acoustic condition.

## Dataset

The dataset will be released on Hugging Face:

```python
from datasets import load_dataset

dataset = load_dataset("prummn/Voices-in-the-Wild-Bench", split="test")
```

### Dataset Composition

| Group | # Samples | Description |
|---|---:|---|
| Synthetic speech | 3,500 | Generated speech samples with controlled perturbations |
| Real-recorded speech | 1,500 | Human-recorded speech from 16 speakers |
| Chinese | 2,500 | Mandarin Chinese speech |
| English | 2,500 | English speech |
| Total | 5,000 | Full benchmark set |

### Acoustic Categories

| Category | # Samples | Description |
|---|---:|---|
| `noise` | 500 | Background noise and additive acoustic interference |
| `far_field` | 500 | Distant microphone and reverberant capture conditions |
| `obstructed` | 500 | Speech affected by physical or spectral obstruction |
| `distortion` | 500 | Clipping, nonlinear distortion, and signal degradation |
| `recording` | 500 | Recording coloration, channel effects, and related artifacts |
| `strong_echo` | 500 | Echo-heavy and reverberant speech |
| `dropout` | 500 | Missing, repeated, or discontinuous speech segments |
| `mixed` | 1,500 | Combinations of multiple acoustic conditions |

The current audio release is organized around seven single-condition categories. The `mixed` category contains combined perturbations and will be described in the dataset card.

## Data Format

Each JSONL record follows the structure below:

```json
{
  "index": 0,
  "audio_path": "/path/to/audio.wav",
  "question": "Please transcribe the audio content into text.",
  "answer": "reference transcription",
  "subset": "sim-zh-noise",
  "combination": "noise",
  "source_scenes": ["noise"],
  "global_severity": 0.93,
  "speed_factor": null,
  "name": "sample_name",
  "prediction": ""
}
```

Important fields:

- `audio_path`: path to the waveform file.
- `question`: instruction given to the evaluated system.
- `answer`: reference transcription or answer.
- `subset`: subset label encoding source type, language, and acoustic condition.
- `combination`: acoustic category label.
- `source_scenes`: atomic acoustic scenes used to build the sample.
- `global_severity`: normalized perturbation severity when available.
- `prediction`: optional field for model outputs.

## Evaluation

Evaluation scripts are under preparation and will be released in a future update. The intended workflow is:

```shell
python scripts/evaluate.py --prediction_file path/to/predictions.jsonl
```

Prediction files should preserve the original sample metadata and fill the `prediction` field with the model response.

## Leaderboard

The leaderboard will be hosted with GitHub Pages:

```text
https://prummn.github.io/Voices-in-the-Wild-Bench/
```

We will report aggregate performance as well as category-wise performance across the eight acoustic categories.

## Submission

We welcome result submissions through the GitHub issue tracker. Please include:

- Model name and version.
- Evaluation date.
- Decoding or inference settings.
- Aggregate score and category-wise scores.
- A link to the prediction file or reproducible evaluation log.

Submit results here:

```text
https://github.com/prummn/Voices-in-the-Wild-Bench/issues
```

## Citation

If you use Voices-in-the-Wild-Bench in your research, please cite:

```bibtex
@article{voicesinthewildbench2026,
  title={Voices-in-the-Wild-Bench: Benchmarking Robust Speech Understanding in Real-World Voice Interaction},
  author={Anonymous Authors},
  journal={arXiv preprint arXiv:YOUR_PAPER_ID},
  year={2026}
}
```
