# Verification Spec

- Primary command:
  - `python docs/topics/0.18_Mathnicry/Code/03_Research/Research_BSD_Elliptic_Unity.py`
- Inputs:
  - `Data/Download_Quantum_Data.py`
- Baseline:
  - Classical theorem statements, topic-local proof scripts, and internal diagnostic outputs.
- Reported metrics:
  - consistency checks, bounded-domain counterexample searches, and script-reported scaling or stability diagnostics
- Fixed threshold:
  - Working threshold for this standards pass: the primary script must run without error, use the stated input package, and write a summary artifact under Result/artifacts/. A stronger numeric acceptance threshold must be frozen in a later BASELINE_COMPARISON.md pass.
- Artifact target:
  - Result/artifacts/0_18_mathnicry_verification.json
- Interpretation:
  - Treat output as an internal benchmark artifact only. Do not upgrade claim language to 'solved', 'verified', or 'exact' until a topic-specific baseline-comparison pass is complete.
