# Verification Spec

- Primary command:
  - `python docs/topics/0.4_Superconductivity_Superfluids/Code/03_Research/Experiment_Superconductor_Data.py`
- Inputs:
  - `Data/03_Research/__init__.py`
  - `Data/03_Research/calibrated_superconductors.json`
  - `Data/03_Research/casimir_data.py`
  - `Data/03_Research/casimir_force_data.json`
- Baseline:
  - Supercon working files, calibrated superconducting datasets, and cited material references.
- Reported metrics:
  - relative error on transition-temperature or materials-response benchmarks
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_4_superconductivity_superfluids_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
