# Verification Spec

- Primary command:
  - `python docs/topics/0.26_Cosmic_Dynamic_Frame/Code/03_Research/Research_Cosmic_Flows.py`
- Inputs:
  - `Data/03_Research/Laniakea_Flows.json`
  - `Data/Cosmicflows_3_Subset.csv`
  - `Data/Download_Cosmic_Data.py`
  - `Data/Pioneer_Anomaly_Data.csv`
- Baseline:
  - Cosmicflows-3 subset, Pioneer anomaly files, and topic-local research scripts.
- Reported metrics:
  - residuals on flow or anomaly observables and internal comparison diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_26_cosmic_dynamic_frame_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
