# Validation record

This record distinguishes the completed software checks from full research evaluation. Documentation was updated on **2026-09-27**; the recorded local checks and GitHub Actions run below were completed on **2026-09-24**.

## Local validation

**Environment:** Linux CPU, Python 3.12.14, TensorFlow CPU 2.20.0, Keras 3.11.3. Package versions and run arguments are recorded in [`smoke_results/run.json`](smoke_results/run.json).

| Check | Recorded result |
| --- | --- |
| Automated test suite | 10 test cases passed |
| Subject-ID matching and invalid-input rejection | Passed |
| Disjoint, complete, repeatable train/validation/test splits | Passed |
| Training-partition scaling and explicit spectrogram window | Passed |
| Native checkpoint save/reload | Passed for `waveform` and `spectrogram` |
| Actual training | Both architectures completed one epoch per fold, with two outer folds |
| Reloaded trained predictions compared with saved held-out predictions | Passed for both architectures |
| CSV converter round trip | Preserved IDs, waveforms, and targets |
| Quickstart notebook | Five code cells executed, with saved outputs and no exceptions |
| Notebook schema and Python syntax | Passed |
| Original research notebook hash | Unchanged |
| Dependency consistency | `pip check` passed |

Evidence:

- [`test_output.txt`](test_output.txt): actual automated test output. A Keras/NumPy deprecation warning was emitted; the suite finished with `OK`.
- [`integration_checks.json`](integration_checks.json): trained-checkpoint and converter checks.
- [`smoke_results/`](smoke_results/): recorded run configuration, environment, and small-run metrics.
- [`../notebooks/01_quickstart.ipynb`](../notebooks/01_quickstart.ipynb): executed training, inference, and plots.
- [`provenance.json`](provenance.json): source notebook hash and reproduction status.

Both models were trained from random initialization on **72 artificial software-fixture waveforms**, with 512 samples per waveform. The saved metrics are integration-test evidence. They do not establish convergence, physiological simulation quality, published accuracy, or clinical performance.

Paths inside the recorded configuration identify the original validation runtime. Large model checkpoints are excluded from the repository and can be regenerated with the demo command.

## GitHub Actions

The [Checks run on 2026-09-24](https://github.com/KianaAbrisham/ppg-cfpwv-attention/actions/runs/36019445195) completed successfully for commit [`1059f9f`](https://github.com/KianaAbrisham/ppg-cfpwv-attention/commit/1059f9f911ed907c6e2bc823cc1d8871ec974464).

The [workflow](../.github/workflows/checks.yml) installs the pinned requirements on Ubuntu with Python 3.12, then runs:

```bash
python -m unittest discover -s tests -v
python train.py --demo --output runs/ci-demo
```

The test suite checks checkpoint serialization for both model architectures. The workflow's training command uses the default demo model, **`waveform` only**. The separate local validation above covers actual training of both architectures. This record refers to that specific successful run; the repository badge reports the current workflow status.

## Coverage limits

Original research CSV exports, paper-trained checkpoints, and a complete final experiment record were unavailable. Full PWDB experiments and reproduction of the publication's numerical results have not been verified. GPU, Windows, and macOS execution have not been validated.

For a new full experiment, retain the configuration, input hashes, subject splits, preprocessing, checkpoints, and held-out predictions. Review the [research notes](RESEARCH_NOTES.md) before comparing its results with the paper.

## Public-source conversion verified — 2026-09-28

The official PWDB v0.2 waveform archive, haemodynamic targets and provided fiducials were downloaded and verified against publisher checksums. All 4,374 subject IDs were aligned explicitly, all waveform values passed a CSV round-trip check, and the target units and sampling rate were checked against the source documentation. Four additional tests verify shuffled-ID alignment and rejection of duplicate IDs, missing subjects and corrupt cached downloads. See [public data setup](PUBLIC_DATA.md) and the [conversion manifest](public_data/conversion_manifest.json). These checks validate data preparation; they do not establish numerical reproduction of a paper.
