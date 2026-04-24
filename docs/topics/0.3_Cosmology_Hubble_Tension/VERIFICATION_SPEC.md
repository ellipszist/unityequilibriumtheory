# Verification Spec

- Primary command:
  - `python docs/topics/0.3_Cosmology_Hubble_Tension/Code/03_Research/Research_Hubble_Comparison.py`
- Inputs:
  - Planck 2018 H0 reference
  - SH0ES 2022 H0 reference
- Reported metrics:
  - Absolute H0 gap
  - Relative percentage error in gap explanation
  - Hubble-frame coupling and its source
- Fixed threshold:
  - Current script uses an internal pass threshold of `< 20%` relative error
- Artifact target:
  - `Result/artifacts/hubble_comparison_validation.json`
- Interpretation:
  - Treat output as an internal comparison record, not external cosmology validation
  - The comparison must not optimize beta against the H0 values; the accepted coupling source
    is `sqrt(alpha_em)` from the central constants module
