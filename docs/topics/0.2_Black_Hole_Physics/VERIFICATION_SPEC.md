# Verification Spec

- Primary command:
  - `python docs/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_CCBH_Analysis.py`
- Inputs:
  - `Data/03_Research/black_hole_data.json`
  - `Data/03_Research/black_hole_metadata.json`
  - `Data/03_Research/plasma_records.json`
  - `Data/BlackHole_Catalog.csv`
- Baseline:
  - Topic-local black-hole catalog files and cited observational comparison targets.
- Reported metrics:
  - relative error on mass-radius style observables and residual mismatch against selected references
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_2_black_hole_physics_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
