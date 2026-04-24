# Verification Spec

- Primary command:
  - `python docs/topics/0.17_Mass_Generation/Code/03_Research/Research_Higgs_Coupling.py`
- Inputs:
  - `Data/03_Research/download_data.py`
  - `Data/03_Research/higgs_coupling_data.json`
  - `Data/03_Research/higgs_mass_combined.json`
  - `Data/03_Research/lepton_data.json`
- Baseline:
  - PDG-derived topic files and topic-local verification scripts.
- Reported metrics:
  - mass residuals, ratio mismatch, and script-reported hierarchy diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_17_mass_generation_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
