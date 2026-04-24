# Verification Spec

- Primary command:
  - `python docs/topics/0.24_Artificial_Intelligence/Code/03_Research/Research_AI_Detective_V2.py`
- Inputs:
  - `Data/00_Foundation/foundation_basics.txt`
  - `Data/03_Research/deepseek_moe_data.json`
  - `Data/03_Research/scaling_laws.json`
  - `Data/03_Research/tiny_shakespeare.txt`
- Baseline:
  - GPT-style scaling-law files and topic-local AI model metadata.
- Reported metrics:
  - scaling residuals, efficiency comparisons, and script-reported benchmark diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_24_artificial_intelligence_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
