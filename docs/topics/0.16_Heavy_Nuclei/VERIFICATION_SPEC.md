# Verification Spec

- Primary command:
  - `python docs/topics/0.16_Heavy_Nuclei/Code/03_Research/Research_Fission.py`
- Inputs:
  - `Data/03_Research/ame2020_heavy/ame2020_heavy.json`
  - `Data/03_Research/ame2020_heavy_nuclei.json`
  - `Data/03_Research/download_data.py`
  - `Data/AME2020_mass.txt`
- Baseline:
  - AME2020 heavy-nuclei files and topic-local fission comparison scripts.
- Reported metrics:
  - binding-energy residuals, fission benchmark mismatch, and stability-trend diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_16_heavy_nuclei_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
