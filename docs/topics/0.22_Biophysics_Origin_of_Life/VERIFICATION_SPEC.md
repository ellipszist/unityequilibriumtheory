# Verification Spec

- Primary command:
  - `python docs/topics/0.22_Biophysics_Origin_of_Life/Code/03_Research/Research_Biomarker_Identification.py`
- Inputs:
  - `Data/03_Research/03_Research/chb_mit_reference.json`
  - `Data/03_Research/03_Research/chb01_summary.txt`
  - `Data/03_Research/03_Research/seizure_phase_data.json`
  - `Data/03_Research/chb_mit_reference.json`
- Baseline:
  - Topic-local evidence assets, downloaded files, and cited biological references.
- Reported metrics:
  - complexity-score consistency, classification diagnostics, or residual mismatch on selected proxy benchmarks
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_22_biophysics_origin_of_life_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
