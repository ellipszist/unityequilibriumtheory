# Verification Spec

- Primary command:
  - `python docs/topics/0.23_Unity_Scale_Link/Code/03_Research/Research_Cross_Domain.py`
- Inputs:
  - `Data/03_Research/create_unified_data.py`
  - `Data/03_Research/economy/Bitcoin_yahoo_real.csv`
  - `Data/03_Research/economy/DowJones_yahoo_real.csv`
  - `Data/03_Research/economy/EUR_USD_yahoo_real.csv`
- Baseline:
  - Topic-local H0-tension, high-redshift, and unified-data working files.
- Reported metrics:
  - cross-dataset residuals, consistency scores, and scaling-trend diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_23_unity_scale_link_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
