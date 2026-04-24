# Verification Spec

- Primary command:
  - `python docs/topics/0.12_Vacuum_Energy_Casimir/Code/03_Research/Research_Casimir.py`
- Inputs:
  - `Data/03_Research/__init__.py`
  - `Data/03_Research/calibrated_superconductors.json`
  - `Data/03_Research/casimir_1998.json`
  - `Data/03_Research/casimir_data.py`
- Baseline:
  - Topic-local Casimir datasets, calibration files, and cited literature references.
- Reported metrics:
  - force residuals as a function of separation and mismatch against selected reference curves
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_12_vacuum_energy_casimir_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
