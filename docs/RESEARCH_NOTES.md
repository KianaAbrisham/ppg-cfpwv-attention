# Research provenance

Source notebooks: Springer.ipynb. Their SHA-256 hashes are in `provenance.json`.
Original notebook bytes were preserved separately; the package is a new implementation copy.

## Implementation changes

Preserves time as the LSTM sequence axis in the 2D branch; replaces the fixed reshape with dimensions derived from the convolution output. Spectrogram input now has one channel instead of three identical channels, explicit Hann windows, and training-only input normalization.

Across the project: strict subject-ID joins replace positional assumptions/truncation; fixed input
length replaces dataset-wide implicit padding length; regression target scaling occurs inside the
training partition; repeated notebook state is replaced by complete entry points and saved preprocessing.
The corrections and modeling changes can change the reported scores.

Spectrograms use 500 Hz by default, segment length 76, overlap `nperseg // 8`, constant detrending,
PSD output and a 1e-10 power floor before 10·log10. Tukey, when selected explicitly, uses alpha .25.
Zero padding and square image resizing are explicit modeling assumptions.

## Results and limitations

The source studies use 4,374 simulated cardiovascular profiles. The regression target is cf-PWV in m/s.
Performance on simulated profiles does not establish performance on wearable or patient recordings.
The original final CSV exports, paper checkpoints and complete final experiment record were not supplied.
Saved values in the old notebooks cannot certify that every cell is a publication-final experiment.

No published metric is presented as a result of this refactor. Before reporting corrected research
scores, verify subject/site correspondence, sampling rate, target units, and waveform columns; run the
full experiment and retain its configuration, input hashes and split records. Hardware/library versions
can affect exact numerical reproducibility. CPU is the validated target; other devices require validation.

## References

- Paper: https://doi.org/10.1007/s11760-024-03496-4
- Dataset: https://zenodo.org/records/3275625
- Signal processing: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html
- Keras serialization: https://keras.io/guides/serialization_and_saving/
- VGG preprocessing: https://keras.io/api/applications/vgg/
- ResNet weights: https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html
