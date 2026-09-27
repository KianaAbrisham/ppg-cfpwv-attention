# CNN–BiLSTM–Attention for PPG cf-PWV Estimation

[![Checks](https://github.com/KianaAbrisham/ppg-cfpwv-attention/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/KianaAbrisham/ppg-cfpwv-attention/actions/workflows/checks.yml)

Estimate carotid–femoral pulse wave velocity (cf-PWV, m/s) from photoplethysmography (PPG) using convolutional layers, a bidirectional LSTM, and temporal attention. This Python project compares waveform and spectrogram inputs through a shared training, evaluation, and saved-model inference workflow.

**Author:** [Kiana Pilevar Abrisham](https://github.com/KianaAbrisham)  
**Related publication:** [Advancing PPG-based cf-PWV estimation with an integrated CNN-BiLSTM-Attention model](https://doi.org/10.1007/s11760-024-03496-4) (2024)

Refactored from the author's research notebooks, with subject-ID checks, training-only preprocessing statistics, repeatable data splits, and automated tests. Both model paths have completed software checks on artificial data. Full reproduction of the paper's numerical results has not been established; see the [validation record](docs/VALIDATION.md).

## Models

| Option | Input | Architecture |
| --- | --- | --- |
| `waveform` | One-dimensional PPG samples | Conv1D → pooling → BiLSTM → temporal attention → regression |
| `spectrogram` | Single-channel log-power spectrogram | Conv2D → pooling → time-axis sequence → BiLSTM → temporal attention → regression |

Both models use TensorFlow/Keras and train from random initialization. Spectrogram generation uses SciPy. The spectrogram branch preserves the time axis for the LSTM and does not resize the input into a square image.

## Quick start

Use **Python 3.12** in this repository's folder. Create an isolated environment:

```bash
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on Linux/macOS, or `.venv\Scripts\activate` in Windows Command Prompt. Linux CPU is the validated environment.

Install dependencies, run the tests, and train both model paths on the demo data:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python train.py --demo --models waveform spectrogram --output runs/demo
```

The demo creates **72 artificial waveforms**, uses **512 samples per waveform**, and trains for **one epoch in each of two outer folds**. These fixtures exercise the software; they are independent of PWDB and their scores do not measure research or clinical performance. Use a new output folder for each training run.

Reload the first waveform checkpoint and write predictions:

```bash
python predict.py --model-dir runs/demo/waveform/fold_1 --signals runs/demo/demo_input/signals.csv --output runs/demo/new_predictions.csv
```

The prediction CSV contains `subject_id`, `predicted_cfpwv_m_s`, and `model_status`. This command demonstrates checkpoint reuse on demo inputs. Predictions from one saved fold are not an ensemble or an all-data refit.

The [executed quickstart notebook](notebooks/01_quickstart.ipynb) shows training, inference, and plots. The [validation record](docs/VALIDATION.md) describes the local checks and GitHub Actions coverage.

## Use research data

The related study uses [PWDB](https://zenodo.org/records/3275625), an in-silico dataset of virtual adults. Original research CSV exports and paper-trained checkpoints are not included. `prepare_data.py` converts existing wide CSV exports into the schema below; it does not download or process the raw PWDB release automatically.

| File | Required columns | Meaning |
| --- | --- | --- |
| `signals.csv` | `subject_id`, `s0000`, `s0001`, … | One waveform per subject from one artery; sample columns in time order |
| `targets.csv` | `subject_id`, `cfpwv_m_s` | Finite, positive cf-PWV values in m/s |

Targets are matched by subject ID. IDs must be unique, and both files must contain exactly the same subjects. The loader rejects constant or empty waveforms, internal missing samples, infinities, and metadata mixed into sample columns. Shorter waveforms, including trailing empty sample cells, are zero-padded; longer waveforms are rejected rather than silently cropped.

For existing wide exports, substitute the actual source column names:

```bash
python prepare_data.py --signals original_signals.csv --targets original_targets.csv --signal-id-column subject_id --target-id-column subject_id --target-column cfpwv_m_s --task regression --output data/converted
```

Quote column names containing spaces. Use `--drop-signal-columns` to remove exported indexes or metadata explicitly. If both files lack IDs, use `--assume-row-aligned` only after independently verifying their subject order.

Train both architectures with the same subject splits:

```bash
python train.py --signals data/converted/signals.csv --targets data/converted/targets.csv --site digital --models waveform spectrogram --weights none --output runs/digital-01
```

Set `--site` to the verified artery: `digital`, `radial`, or `brachial`. Use separate runs for different arteries; do not treat multiple records from the same subject as independent subjects. Confirm the waveform sample order, target units, and acquisition settings before training.

Research defaults are `--length 2000`, `--fs 500`, `--nperseg 76`, `--window hann`, five folds, a maximum of 500 epochs, early-stopping patience 50, batch size 16, and seed 42. Choose the input length and sampling rate from the dataset specification. The pipeline does not resample signals. Run `python train.py --help` for all options.

## Evaluation and outputs

Each outer fold reserves a test partition; 20% of the remaining subjects form the validation partition. Spectrogram normalization and target scaling are fitted on the inner training subjects only. Waveform inputs retain their supplied amplitude scale. Early stopping monitors validation loss, and held-out predictions use the best validation weights, converted back to m/s.

Evaluation reports **MAE and RMSE (m/s), R², and MAPE (%)**, alongside a baseline that predicts the training subjects' mean target. Both architectures use the same partitions. Fold standard deviations describe variation across folds; they are not confidence intervals. Repeated model or hyperparameter selection requires nested cross-validation or a separate final test set.

Each run saves:

- Configuration, dependency versions, input hashes, and subject IDs for every split.
- Per-fold preprocessing, `.keras` checkpoints, loss history, metrics, and baseline results.
- Held-out predictions, evaluation plots, per-fold metrics, and a summary across folds.

Timing reports the median and 95th percentile of 20 synchronous, batch-one forward passes after three warmups; input preprocessing is excluded. Checkpoint size measures the complete saved Keras archive, including training state.

## Repository guide

| Location | Contents |
| --- | --- |
| [`ppg/`](ppg/) | Data validation, preprocessing, architectures, training, and inference |
| [`train.py`](train.py), [`predict.py`](predict.py), [`prepare_data.py`](prepare_data.py) | Command-line entry points |
| [`tests/`](tests/) | Input, split, preprocessing, and checkpoint regression tests |
| [`notebooks/01_quickstart.ipynb`](notebooks/01_quickstart.ipynb) | Executed artificial-data walkthrough |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | Completed checks, evidence, and coverage limits |
| [`docs/RESEARCH_NOTES.md`](docs/RESEARCH_NOTES.md) | Source provenance and changes from the research notebook |
| [`.github/workflows/checks.yml`](.github/workflows/checks.yml) | Automated CPU tests and waveform demo |

Citation metadata are available in [`CITATION.cff`](CITATION.cff). Performance on simulated profiles alone does not establish performance on patient or wearable recordings.
