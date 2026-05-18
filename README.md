<h1 align="center">Voices-in-the-Wild-Bench</h1>

<p align="center">
  <strong>Benchmarking Robust Speech Understanding in Real-World Voice Interaction</strong>
</p>

<p align="center">
  <a href="https://xzf-thu.github.io/Voices-in-the-Wild-Bench/">Leaderboard</a> |
  <a href="https://arxiv.org/abs/YOUR_PAPER_ID">Paper</a> |
  <a href="https://huggingface.co/datasets/xzf-thu/Voices-in-the-Wild-Bench">Dataset</a> |
  <a href="https://github.com/xzf-thu/Voices-in-the-Wild-Bench/issues">Submit Results</a>
</p>

> Voices-in-the-Wild-Bench is a bilingual benchmark for evaluating how robust speech and voice assistant systems are under realistic acoustic conditions, including noise, far-field speech, obstruction, recording artifacts, echo, dropout, and mixed perturbations.

## News

* **`2026.05.18`** Added reproducible evaluation utilities, example records, and initial model wrappers for Whisper-Large-v3 and Mega-ASR.
* **`2026.05.16`** Initial repository skeleton released.

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

dataset = load_dataset("xzf-thu/Voices-in-the-Wild-Bench", split="test")
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

Voices-in-the-Wild-Bench evaluates Chinese samples with CER and English samples with WER. Prediction files should preserve the original sample metadata and fill the `prediction` field with the model response.

```shell
python scripts/evaluate_predictions.py \
  --prediction-file path/to/predictions.jsonl \
  --output-file results/model_results.json
```

The script reports overall error rate, language-wise scores, and the real/synthetic breakdown for each acoustic category.

### Running Models

The repository includes lightweight wrappers for selected reproducible systems. Full model checkpoints should be downloaded separately and passed with `--model-path` when required.

```shell
python scripts/run_inference.py \
  --model whisper-large-v3 \
  --data-file data/examples.jsonl \
  --audio-root /path/to/voices_wild_bench \
  --output-file outputs/whisper_large_v3.jsonl
```

Mega-ASR is the public name for our merged_v2 model:

```shell
python scripts/run_inference.py \
  --model mega-asr \
  --model-path /path/to/Mega-ASR \
  --data-file data/examples.jsonl \
  --audio-root /path/to/voices_wild_bench \
  --output-file outputs/mega_asr.jsonl
```

`data/examples.jsonl` contains a few lightweight records for checking the expected format. The full benchmark data should be downloaded from the dataset hosting page.

## Leaderboard

The full leaderboard is hosted with GitHub Pages:

```text
https://xzf-thu.github.io/Voices-in-the-Wild-Bench/
```

The table below reports breakdown results by acoustic scenario. Scores are error rates; lower is better. `Real.` and `Sim.` denote real-recorded and synthetic speech, respectively.

| Model | Noise Real. | Noise Sim. | Far. Real. | Far. Sim. | Obst. Real. | Obst. Sim. | Echo. Real. | Echo. Sim. | Record. Real. | Record. Sim. | Elc.Dis. Real. | Elc.Dis. Sim. | Trans.Drop. Real. | Trans.Drop. Sim. | Mixed Real. | Mixed Sim. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Closed-source models** |||||||||||||||||
| Gemini3-Flash | 7.63 | 10.61 | 5.14 | 1.90 | 3.73 | 2.65 | 8.75 | 14.86 | 8.38 | 19.85 | 3.15 | 7.56 | 5.47 | 7.65 | 7.99 | 9.62 |
| Seed-ASR | 8.21 | 8.11 | 3.06 | 3.19 | 3.10 | 2.76 | 16.55 | 18.21 | 18.48 | 23.33 | 3.89 | 5.71 | 7.97 | 7.46 | 6.88 | 9.29 |
| GPT-4o-trans. | 13.19 | 45.78 | **1.87** | 2.39 | **1.57** | 2.77 | 15.62 | 28.76 | 13.37 | 22.60 | 3.70 | 8.43 | 8.76 | 7.71 | 5.62 | 11.00 |
| **Open-source models** |||||||||||||||||
| Whisper-L-v3 | 16.57 | 18.19 | 3.38 | 6.85 | 3.06 | 6.01 | 25.34 | 39.87 | 18.33 | 31.81 | 3.74 | 8.77 | 7.04 | 8.05 | 8.91 | 14.79 |
| Qwen2.5-Omni | 11.92 | 17.88 | 2.35 | 2.44 | 2.40 | 2.08 | 20.01 | 32.64 | 13.71 | 30.09 | 2.46 | 5.96 | 6.34 | 5.88 | 6.40 | 10.29 |
| Kimi-Audio | 35.10 | 14.59 | 2.71 | 1.92 | 2.49 | 1.64 | 24.00 | 26.58 | 8.73 | 18.09 | 1.83 | **2.78** | 4.54 | 6.33 | 4.44 | 6.19 |
| Qwen3-ASR | 7.51 | 9.52 | 2.23 | **1.54** | 1.73 | 1.27 | 10.40 | 14.61 | 9.57 | 19.42 | **1.54** | 3.41 | 4.16 | 4.19 | 3.30 | 5.39 |
| **Our model** |||||||||||||||||
| Mega-ASR | 6.33 | 8.26 | 2.35 | 1.61 | 1.62 | **1.23** | **8.62** | 12.59 | 7.65 | 14.21 | 1.71 | 3.72 | **2.59** | **2.62** | 2.73 | 4.57 |
| Mega-ASR w/ router | **6.12** | **8.09** | 2.33 | 1.69 | 1.80 | 1.41 | 8.66 | **12.22** | **6.91** | **13.23** | 1.60 | 3.35 | 2.72 | 2.88 | **2.63** | **4.53** |

## Submission

We welcome result submissions through the GitHub issue tracker. Please include:

- Model name and version.
- Evaluation date.
- Decoding or inference settings.
- Aggregate score and category-wise scores.
- A link to the prediction file or reproducible evaluation log.

Submit results here:

```text
https://github.com/xzf-thu/Voices-in-the-Wild-Bench/issues
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
