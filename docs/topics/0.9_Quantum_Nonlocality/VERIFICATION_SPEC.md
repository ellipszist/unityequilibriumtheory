# Verification Spec

- Primary command:
  - `python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_Bell_Inequality.py`
- Inputs:
  - `Data/03_Research/bell_inequality_data.json`
  - `Data/03_Research/bell_test_2015.json`
  - `Data/03_Research/bell_test_data.py`
  - `Data/03_Research/double_slit_c60.json`
- Baseline:
  - Topic-local Bell datasets and cited experimental references.
- Reported metrics:
  - Bell-parameter residuals, violation consistency checks, and script-reported fit diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_9_quantum_nonlocality_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
