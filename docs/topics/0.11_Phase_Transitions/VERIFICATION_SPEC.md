# Verification Spec

- Primary command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Exponents.py`
- Inputs:
  - `Data/03_Research/__init__.py`
  - `Data/03_Research/black_hole_data.json`
  - `Data/03_Research/brownian_data.py`
  - `Data/03_Research/critical_exponents.json`
- Baseline:
  - NIST critical-point inputs and topic-local competitor or test scripts.
- Reported metrics:
  - critical-point residuals, exponent mismatch, and script-reported transition diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_11_phase_transitions_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
