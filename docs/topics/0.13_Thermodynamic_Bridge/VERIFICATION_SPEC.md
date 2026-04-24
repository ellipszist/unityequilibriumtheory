# Verification Spec

- Primary command:
  - `python docs/topics/0.13_Thermodynamic_Bridge/Code/03_Research/Research_Landauer.py`
- Inputs:
  - `Data/03_Research/__init__.py`
  - `Data/03_Research/berut_2012.json`
  - `Data/03_Research/cattaneo_data.json`
  - `Data/03_Research/experimental_data.py`
- Baseline:
  - Berut-style, Cattaneo-style, and topic-local thermodynamic data files.
- Reported metrics:
  - relative error on dissipation or entropy-linked observables and consistency of bridge trends
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_13_thermodynamic_bridge_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
