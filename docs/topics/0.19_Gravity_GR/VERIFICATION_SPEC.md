# Verification Spec

- Primary command:
  - `python docs/topics/0.19_Gravity_GR/Code/03_Research/Research_G_Constant.py`
- Inputs:
  - `Data/03_Research/codata_2018_gravity.json`
  - `Data/03_Research/download_data.py`
  - `Data/03_Research/download_references.py`
  - `Data/03_Research/eotwash_2007_data.json`
- Baseline:
  - CODATA-style gravity inputs and topic-local short-range comparison files.
- Reported metrics:
  - relative error on gravity benchmarks and residual mismatch on selected comparison curves
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_19_gravity_gr_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
