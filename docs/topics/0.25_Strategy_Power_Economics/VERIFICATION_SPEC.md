# Verification Spec

- Primary command:
  - `python docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_8_Billion_Resonance.py`
- Inputs:
  - `Data/03_Research/Bitcoin_yahoo_real.csv`
  - `Data/03_Research/daily_economic_snapshot.json`
  - `Data/03_Research/Gold_yahoo_real.csv`
  - `Data/03_Research/SP500_yahoo_real.csv`
- Baseline:
  - Global_Economy_2024, Bitcoin Yahoo data, and topic-local research scripts.
- Reported metrics:
  - fit residuals, trend mismatch, and script-reported stability diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_25_strategy_power_economics_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
