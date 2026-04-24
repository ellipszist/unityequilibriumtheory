# Verification Spec

- Primary command:
  - `python docs/topics/0.14_Complex_Systems/Code/03_Research/Research_Biology_HRV.py`
- Inputs:
  - `Data/03_Research/biology_hrv/hrv_stress.csv`
  - `Data/03_Research/biology_hrv/physionet_16265_rr.csv`
  - `Data/03_Research/biology_hrv/physionet_16272_rr.csv`
  - `Data/03_Research/biology_hrv/physionet_16273_rr.csv`
- Baseline:
  - Topic-local plasma, biology, and brain-style working files plus cited references.
- Reported metrics:
  - scaling-fit residuals, classification consistency, or internal trend diagnostics reported by scripts
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_14_complex_systems_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
