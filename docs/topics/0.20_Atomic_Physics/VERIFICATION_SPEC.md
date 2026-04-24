# Verification Spec

- Primary command:
  - `python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Atomic_ThreeBody.py`
- Inputs:
  - `Data/03_Research/codata_2018_atomic.json`
  - `Data/03_Research/download_data.py`
  - `Data/03_Research/download_references.py`
  - `Data/03_Research/hydrogen_spectra_data.json`
- Baseline:
  - NIST spectral-line files and topic-local research scripts.
- Reported metrics:
  - wavelength or energy residuals and mismatch against selected spectral baselines
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_20_atomic_physics_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
